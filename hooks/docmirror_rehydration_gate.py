#!/usr/bin/env python3
"""
docmirror_rehydration_gate — PreToolUse hook. The REHYDRATION GATE of the doc-mirror state machine: an
agent CANNOT do work in a NEW conversation without first rehydrating the last conversation's journal.

A new conversation is marked by the SessionStart boundary hook (docmirror_session_boundary.py), which
writes <root>/.docmirror/rehydration.json {rehydrated: false}. While rehydrated==false this gate BLOCKS
every work-tool EXCEPT the ones needed to actually DO the rehydration (the DMN carton queries, Read, and
the read/unlock Bash commands). After the agent runs the DMN algorithm + `docmirror-rehydrated` (which
flips rehydrated=true), the gate allows everything.

ALLOWED while rehydrated==false (the rehydration-read + unlock surface):
  - any tool_name starting with `mcp__carton__`   (the DMN rehydration queries)
  - tool_name == `Read`                            (overflow files + code reading)
  - tool_name == `Bash` ONLY when the command is a rehydration-read / unlock command:
      `docmirror-rehydrated`, `docmirror-cursor show`, `docmirror-read ...`, or a pure read
      (cat/grep/sed/head/tail/less/wc/ls) of context/journal/ or /tmp/heaven_data/query_overflow/ paths.
BLOCKED while rehydrated==false: Edit, Write, NotebookEdit, MultiEdit, Task/Agent dispatch, and any Bash
  not on the allowlist.

FAIL-SAFE (critical, non-negotiable): if rehydration.json is MISSING, UNPARSEABLE, or <root> cannot be
resolved -> ALLOW (exit 0). NEVER hard-lock the agent out of a broken / un-initialized state. The gate
blocks ONLY when it can DEFINITIVELY read rehydrated==false. rehydrated==true -> always ALLOW.

PreToolUse contract (matches docmirror_readonly_guard): print a JSON deny decision + stderr and exit 2 to
block; exit 0 to allow.
"""
import json
import os
import re
import sys
from pathlib import Path


def _root() -> Path:
    """SAME resolution as docmirror-cursor / journal — root-relative, per-system."""
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
    return Path(os.environ.get("DOCMIRROR_REHYDRATION") or (_root() / ".docmirror" / "rehydration.json"))


BLOCK_MSG = (
    "🚫 NOT REHYDRATED. A new conversation started; you must rehydrate the last conversation's journal "
    "FIRST. Run the doc-mirror-memory-net (DMN) algorithm STEP 1–4 (it is the only way you know what is "
    "true — the compaction summary is NOT rehydration), then run `docmirror-rehydrated` to unlock. Only "
    "carton queries + Read are allowed until then."
)

# Bash commands allowed while NOT rehydrated: the unlock CLI + the rehydration-read CLIs.
_UNLOCK_RE = re.compile(r"(^|[\s;&|(])docmirror-rehydrated(\s|$)")
_CURSOR_SHOW_RE = re.compile(r"(^|[\s;&|(])docmirror-cursor\s+show(\s|$)")
_READ_CLI_RE = re.compile(r"(^|[\s;&|(])docmirror-read(\s|$)")
# pure file-reads (no mutation) of the journal / overflow paths
_READ_PROGS = ("cat", "grep", "egrep", "fgrep", "sed", "head", "tail", "less", "more", "wc", "ls", "find")
_READ_PATHS = ("context/journal/", "/tmp/heaven_data/query_overflow/")
# mutation indicators that disqualify a Bash command from the read allowlist
_MUTATORS = (">", ">>", "| tee", "|tee", " tee ", "sed -i", "truncate", " dd ", " mv ", " cp ",
             " rm ", "rmdir", "mkdir", "rename(", "write_text(", ".write(", "open(", "chmod", "chown")


def _bash_allowed_during_rehydration(cmd: str) -> bool:
    """Conservative allowlist: TRUE only for the unlock CLI or a pure rehydration-read command."""
    if not cmd:
        return False
    # the unlock + read-CLIs are always fine (they don't mutate work artifacts)
    if _UNLOCK_RE.search(cmd) or _CURSOR_SHOW_RE.search(cmd) or _READ_CLI_RE.search(cmd):
        return True
    # otherwise: must be a PURE read (a known read program) of a journal/overflow path, no mutators.
    if any(mu in cmd for mu in _MUTATORS):
        return False
    if not any(p in cmd for p in _READ_PATHS):
        return False
    # every shell segment must start with a known read program
    for seg in re.split(r";|&&|\|\||\|", cmd):
        toks = seg.strip().split()
        if not toks:
            continue
        # skip leading wrappers / env-assignments
        k = 0
        while k < len(toks) and (toks[k] in ("cd", "sudo", "time", "env", "nohup", "setsid")
                                 or ("=" in toks[k] and "/" not in toks[k].split("=", 1)[0]
                                     and not toks[k].startswith("-"))):
            k += 1
        if k >= len(toks):
            continue
        prog = toks[k].split("/")[-1]
        if prog not in _READ_PROGS:
            return False
    return True


def _tool_allowed_during_rehydration(tool: str, ti: dict) -> bool:
    if tool.startswith("mcp__carton__"):
        return True
    if tool == "Read":
        return True
    # Skill is allowed while locked: doc-mirror-boot + doc-mirror-memory-net (the orient +
    # rehydration skills) are themselves the way OUT of the lock. Skills are knowledge/instructions,
    # they do not mutate — the actual work-tools (Edit/Write/Bash-mutate/Task) stay blocked, so a
    # skill that says "do X" still cannot DO X until the agent has rehydrated + unlocked.
    if tool == "Skill":
        return True
    if tool == "Bash":
        return _bash_allowed_during_rehydration(ti.get("command", "") or "")
    return False


def main() -> None:
    # FAIL-SAFE: any failure to read a definitive rehydrated==false -> ALLOW.
    try:
        data = json.load(sys.stdin)
    except Exception:
        sys.exit(0)  # can't parse -> don't trap

    try:
        sf = _state_file()
        if not sf.exists():
            sys.exit(0)  # FAIL-SAFE: no record -> allow (un-initialized; never hard-lock)
        rec = json.loads(sf.read_text())
        rehydrated = rec.get("rehydrated")
    except Exception:
        sys.exit(0)  # FAIL-SAFE: unparseable / unreadable -> allow

    if rehydrated is not False:
        sys.exit(0)  # rehydrated==true (or missing key) -> allow everything

    # rehydrated is DEFINITIVELY False -> gate is ARMED.
    tool = data.get("tool_name", "")
    ti = data.get("tool_input", {}) or {}
    if _tool_allowed_during_rehydration(tool, ti):
        sys.exit(0)

    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": BLOCK_MSG,
        }
    }))
    print(BLOCK_MSG, file=sys.stderr)
    sys.exit(2)


if __name__ == "__main__":
    main()
