#!/usr/bin/env python3
"""
docmirror_session_start — cross-compaction rehydration for the doc-mirror work loop.

brainhook (Stop) won't fire on the FIRST turn after a compact — so the loop instructions
would be missing exactly when the agent most needs to re-boot the context cascade. This
SessionStart hook fills that gap: if the doc-mirror loop is ON, it injects the SAME prompt
brainhook uses (single source of truth: ~/.claude/docmirror_loop_prompt.txt), prefixed with
a "you just compacted — rehydrate" note. If the loop is OFF, it stays silent.

The prompt itself boots the cascade: read progress-tracker (the queue) -> the other 6 files
-> doc(m) -> equip the doc-mirror skill -> resume harvesting.

SessionStart contract: whatever we print on stdout is injected as context for the new session.
Print nothing (exit 0) to inject nothing.
"""
import os
import sys
from datetime import datetime
from pathlib import Path

STATE_FILE = Path("/tmp/docmirror_brainhook_state.txt")
PROMPT_FILE = Path.home() / ".claude" / "docmirror_loop_prompt.txt"


def _monorepo() -> Path:
    """Repo root, NO hardcoded path: env → ~/.docmirror_root → git toplevel → cwd."""
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


MONOREPO = _monorepo()
GLOBAL_JOURNAL_DIR = Path(os.environ.get("DOCMIRROR_JOURNAL_DIR", str(MONOREPO / "context" / "journal")))


def loop_on() -> bool:
    try:
        return STATE_FILE.exists() and STATE_FILE.read_text().strip().lower() == "on"
    except Exception:
        return False


def recent_thinklog(n: int = 12) -> str:
    """Last n lines of the current month's GLOBAL thinklog — the record of what we THOUGHT
    (decisions/open forks), which the summarizer cannot reconstruct. Empty string if none."""
    try:
        f = GLOBAL_JOURNAL_DIR / f"{datetime.now():%Y-%m}.md"
        if not f.exists():
            return ""
        lines = [l for l in f.read_text().splitlines() if l.strip()]
        return "\n".join(lines[-n:])
    except Exception:
        return ""


def main():
    # Consume stdin if present (SessionStart may pass JSON); we don't need it.
    try:
        sys.stdin.read()
    except Exception:
        pass

    if not loop_on():
        sys.exit(0)  # loop off -> inject nothing

    try:
        prompt = PROMPT_FILE.read_text().strip()
    except Exception:
        prompt = ("doc-mirror loop is ON but the prompt file is missing. "
                  "Read <repo>/context/progress-tracker.md and resume the loop.")

    think = recent_thinklog()
    think_block = (
        "\n--- RECENT THINKING (global thinklog tail — what we DECIDED / what's OPEN; "
        "the summarizer cannot reconstruct this) ---\n" + think + "\n"
    ) if think else ""

    print(
        "=== DOC-MIRROR REHYDRATION (post-compact / session start) ===\n"
        "You just started a fresh context (likely after a compact) while the doc-mirror "
        "work loop is ACTIVE. The summarizer may have dropped things — do NOT trust it. "
        "Re-boot the context cascade from files before doing anything:\n"
        f"  1. Read {MONOREPO}/context/progress-tracker.md — the ROOT queue (REPO ORDER → active repo).\n"
        "  2. Descend to that repo's context/progress-tracker.md + the other 5 context files + the doc(m) for the module you'll touch.\n"
        "  3. Read the RECENT THINKING below (the thinklog = what we thought/decided; `journal` appends it). git log is the changelog, separate.\n"
        "  4. Equip the `doc-mirror` skill. The flow is SCRIPTED by the operating state graph "
        "(doc-mirror-system/STATE_GRAPH.md). Run `docmirror-cursor show` to RESUME the exact phase you were "
        "in (the cursor survives the compact, like a saved state) and act on that phase's leg.\n"
        f"{think_block}"
        "\n--- (the active loop prompt) ---\n"
        f"{prompt}"
    )
    sys.exit(0)


if __name__ == "__main__":
    main()
