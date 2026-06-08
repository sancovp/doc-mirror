#!/usr/bin/env python3
"""
docmirror_transition_guard — PreToolUse hook on the `Skill` tool. The TRANSITION-VALIDATION guard of
the doc-mirror state machine (STATE_GRAPH.md): the catastrophe-surface guard that lets the agent CATCH
ITSELF. It checks that each move between doc-mirror state-skills is sensical (an edge in the LEGAL
TRANSITIONS table). It is a SINGLE-SHOT, FORCEABLE nudge — not a police:

  - invoked skill is NOT a doc-mirror-{state} skill  -> ALLOW (not our concern).
  - invoked skill is `doc-mirror-boot`  -> ALLOW + RESET the machine (last_state=None, counter=0).
  - invoked skill IS a doc-mirror-{state} skill:
      from = sidecar.last_state ; to = the invoked state
      (from -> to) legal?
        YES -> ALLOW. record transition; last_state=to; block_counter=0 (reset on success).
        NO, block_counter==0 -> BLOCK ONCE (deny + exit 2) with a warning: blocked one time to
            double-check; journal -t DECISION why + RE-INVOKE to force; use doc-mirror-boot to understand the
            machine. block_counter=1.
        NO, block_counter>=1 -> ALLOW (forced). record FORCED deviation; last_state=to; block_counter=0.

"Never block twice in a row." A successful move to a different state clears the counter, so each new
out-of-sequence jump gets exactly ONE check. The forced-deviation history IS the "is the transition
history sensical" metric — auditable after the fact.

PreToolUse contract (matches docmirror_readonly_guard): print a JSON deny decision + stderr and exit 2
to block; exit 0 to allow. Sidecar (hook-owned, NOT the cursor): <root>/.docmirror/transitions.json (root-relative).
"""
import json
import os
import sys
from datetime import datetime
from pathlib import Path


def _root() -> Path:
    """Resolve the system root the SAME way the doc-mirror CLIs do, so the transition sidecar is
    ROOT-RELATIVE (per-system) like the cursor — env DOCMIRROR_MONOREPO / ~/.docmirror_root / git / cwd."""
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


# ROOT-RELATIVE (per-system), matching the cursor. Env DOCMIRROR_TRANSITIONS overrides explicitly.
SIDECAR = Path(os.environ.get("DOCMIRROR_TRANSITIONS") or (_root() / ".docmirror" / "transitions.json"))
ENTRY = "doc-mirror-boot"

# the doc-mirror STATE skills (the gated set) -> their phase name.
STATES = {
    "doc-mirror-init": "init",
    "doc-mirror-seework": "seework",
    "doc-mirror-change": "change",
    "doc-mirror-prompts": "prompt",
}

# LEGAL TRANSITIONS — SINGLE SOURCE OF TRUTH: STATE_GRAPH.md "LEGAL TRANSITIONS" table. Keep in sync.
# from -> set of legal `to`. None (start / post-reset) => any entry is legal. The ONLY nonsensical
# edges are change->boot and prompt->boot (booting a fresh codebase mid-module = lost the thread).
LEGAL = {
    None:      {"init", "seework", "change", "prompt"},
    "init":    {"init", "seework", "change", "prompt"},
    "seework": {"init", "seework", "change", "prompt"},
    "change":  {"seework", "change", "prompt"},
    "prompt":  {"seework", "change", "prompt"},
}

EMPTY = {"last_state": None, "block_counter": 0, "history": []}


def _load() -> dict:
    if SIDECAR.exists():
        try:
            return {**EMPTY, **json.loads(SIDECAR.read_text())}
        except Exception:
            pass
    return dict(EMPTY)


def _save(s: dict) -> None:
    try:
        SIDECAR.parent.mkdir(parents=True, exist_ok=True)  # <root>/.docmirror/ may not exist yet
        SIDECAR.write_text(json.dumps(s, indent=2))
    except Exception:
        pass


def _skill_name(ti: dict) -> str:
    s = ti.get("skill") or ti.get("name") or ""
    return s.split(":")[-1].strip()  # strip any plugin: namespace prefix


def main() -> None:
    try:
        data = json.load(sys.stdin)
    except Exception:
        sys.exit(0)  # can't parse -> don't trap

    if data.get("tool_name", "") != "Skill":
        sys.exit(0)

    ti = data.get("tool_input", {}) or {}
    skill = _skill_name(ti)

    if skill == ENTRY:
        s = _load()
        s["last_state"] = None
        s["block_counter"] = 0
        _save(s)
        sys.exit(0)

    if skill not in STATES:
        sys.exit(0)  # not a gated state skill

    to = STATES[skill]
    s = _load()
    frm = s.get("last_state")
    ts = datetime.now().isoformat(timespec="seconds")

    if to in LEGAL.get(frm, set()):
        s["history"].append({"from": frm, "to": to, "ts": ts, "forced": False})
        s["last_state"] = to
        s["block_counter"] = 0  # reset on a successful transition
        _save(s)
        sys.exit(0)

    # nonsensical transition
    if s.get("block_counter", 0) == 0:
        s["block_counter"] = 1
        _save(s)  # note: do NOT advance last_state — a re-invoke must see the same (from->to)
        msg = (
            f"⚠️ doc-mirror transition check: {frm} -> {to} is NOT a legal transition in the "
            f"state machine (STATE_GRAPH.md LEGAL TRANSITIONS). Blocked ONE TIME to double-check this "
            f"action.\n"
            f"If you MEANT it (an emergent deviation): journal -t DECISION why you swapped "
            f"(\"swapped emergently to {to} because...\"), then RE-INVOKE doc-mirror-{to} to force it "
            f"through (you will not be blocked again).\n"
            f"To gain understanding of the compiler/state machine, just use the "
            f"doc-mirror-boot skill."
        )
        print(json.dumps({
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "deny",
                "permissionDecisionReason": msg,
            }
        }))
        print(msg, file=sys.stderr)
        sys.exit(2)

    # block_counter >= 1 -> forced through (recorded as a deviation)
    s["history"].append({"from": frm, "to": to, "ts": ts, "forced": True})
    s["last_state"] = to
    s["block_counter"] = 0
    _save(s)
    print(f"✓ forced transition {frm} -> {to} recorded as a deviation. Ensure you journaled why.",
          file=sys.stderr)
    sys.exit(0)


if __name__ == "__main__":
    main()
