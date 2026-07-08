#!/usr/bin/env python3
"""
docmirror_session_boundary — SessionStart hook (matchers: startup, compact, clear). Tracks the
CONVERSATION BOUNDARY for the doc-mirror rehydration gate: doc-mirror keeps track of conversation
boundaries by recording, per conversation, whether the agent has rehydrated the last conversation's
journal yet.

A NEW conversation starting (a different session_id than the one recorded, or no record at all) marks
"rehydration required" — it writes <root>/.docmirror/rehydration.json with rehydrated=false. The
PreToolUse gate (docmirror_rehydration_gate.py) then blocks work-tools until the agent runs the DMN
rehydration algorithm and `docmirror-rehydrated` flips the flag back to true.

If the SAME session_id is seen again (a SessionStart re-fire within the same conversation), the record
is left UNTOUCHED — re-marking would wrongly re-lock an already-rehydrated conversation.

SessionStart contract: this hook NEVER blocks/crashes the session. Everything is wrapped; it always
exits 0. Resolves <root> the SAME way the doc-mirror CLIs do (env DOCMIRROR_MONOREPO / ~/.docmirror_root
/ git toplevel / cwd), so the boundary record is ROOT-RELATIVE (per-system), exactly like the cursor.
"""
import json
import os
import sys
from datetime import datetime
from pathlib import Path


def _root() -> Path:
    """Resolve the system root the SAME way docmirror-cursor does (root-relative, per-system)."""
    e = os.environ.get("DOCMIRROR_MONOREPO")
    if e:
        return Path(e)
    cfg = Path.home() / ".docmirror_root"
    try:
        if cfg.exists() and cfg.read_text().strip():
            return Path(cfg.read_text().strip())
    except Exception:
        pass
    try:
        import subprocess
        top = subprocess.run(["git", "rev-parse", "--show-toplevel"],
                             capture_output=True, text=True, timeout=3).stdout.strip()
        if top:
            return Path(top)
    except Exception:
        pass
    return Path.cwd()


def _state_file() -> Path:
    # Env DOCMIRROR_REHYDRATION overrides explicitly (matches the cursor's DOCMIRROR_CURSOR pattern).
    return Path(os.environ.get("DOCMIRROR_REHYDRATION") or (_root() / ".docmirror" / "rehydration.json"))


def main() -> None:
    try:
        data = json.load(sys.stdin)
    except Exception:
        sys.exit(0)  # can't parse -> never trap the session

    try:
        session_id = str(data.get("session_id", "") or "")
        sf = _state_file()

        recorded_id = None
        if sf.exists():
            try:
                recorded_id = json.loads(sf.read_text()).get("conversation_id")
            except Exception:
                recorded_id = None  # unparseable record -> treat as a new boundary, rewrite it

        # New conversation (no record, OR a different session_id) -> mark rehydration required.
        if recorded_id != session_id:
            rec = {
                "conversation_id": session_id,
                "boundary_ts": datetime.now().isoformat(),
                "rehydrated": False,
                "rehydrated_ts": None,
                "entries_read": None,
            }
            sf.parent.mkdir(parents=True, exist_ok=True)
            sf.write_text(json.dumps(rec, indent=2))
        # else: same conversation re-firing SessionStart -> leave the record untouched.
    except Exception:
        pass  # NEVER crash the session

    sys.exit(0)


if __name__ == "__main__":
    main()
