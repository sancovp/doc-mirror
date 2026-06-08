#!/usr/bin/env python3
"""
docmirror_readonly_guard — PreToolUse hook. Makes the doc-mirror managed files READ-ONLY to the
agent EXCEPT through the doc-mirror CLIs. The agent NEVER edits them by hand; it `journal`s /
`doc-mirror-commit`s, and the SYSTEM writes them. The syntax on these files is the whole point — a
direct hand-edit bypasses categorization/projection and propagates the exact disease we are killing.

Blocks (deny) when the agent tries to WRITE a managed file directly:
  - Write / Edit / MultiEdit whose file_path is a managed file
  - Bash whose command writes/redirects/mutates a managed file (>, >>, tee, sed -i, mv, cp, rm,
    truncate, dd, python open('w'/'a'), .write(, write_text(, a heredoc into it)
ALLOWS: reading them (cat/sed -n/grep/head/tail), and invoking the CLIs (`journal ...`,
`doc-mirror-commit ...`, etc.) — those carry no managed-path + write-operator in the agent's command;
the CLI process writes the file itself, which is exactly the sanctioned path.

PreToolUse contract: print a JSON deny decision (and exit 2) to block; exit 0 silently to allow.
"""
import json
import re
import sys

# substrings that mark a doc-mirror MANAGED file (CLI-only)
MANAGED = (
    "/docs/mirror/",
    "/docs/vision/",
    "/context/journal/",
    "/context/progress-tracker.md",
)
# write/mutate indicators in a Bash command (reads have none of these)
WRITE_OPS = (
    ">", ">>", "| tee", "|tee", " tee ", "sed -i", "truncate", " dd ",
    "write_text(", ".write(", "open(", " mv ", " cp ", " rm ", "rename(", ">|",
)
# the doc-mirror CLIs that are the SANCTIONED writers — never block these invocations
SANCTIONED = ("journal", "doc-mirror-commit", "docmirror-", "vision", "plan", "projects", "tracker")

DENY = (
    "BLOCKED: that is a doc-mirror MANAGED file (docs/mirror, docs/vision, context/journal, or a "
    "progress-tracker). These are READ-ONLY to you — you NEVER edit them by hand. Use the CLI: "
    "`journal \"<msg>\"` (you supply the TYPE; the system files+organizes it), `doc-mirror-commit "
    "<m> ...` for doc(m), `vision <tag>` to read. Hand-editing bypasses the syntax and propagates "
    "drift — that is the entire thing we are preventing."
)


def _path_is_managed(p: str) -> bool:
    if not p:
        return False
    return any(m in p for m in MANAGED)


SANCTIONED_PROGS = ("journal", "doc-mirror-commit", "vision", "plan", "projects", "tracker")


def _segment_program(seg: str) -> str:
    """The actual program a shell segment runs (skipping leading env-assignments / wrappers)."""
    toks = seg.strip().split()
    k = 0
    while k < len(toks):
        t = toks[k]
        if t in ("export", "cd", "sudo", "time", "env", "nohup", "setsid"):
            k += 1
            continue
        if "=" in t and "/" not in t.split("=", 1)[0] and not t.startswith("-"):  # VAR=val prefix
            k += 1
            continue
        return t.split("/")[-1]  # basename of the program token
    return ""


def _seg_is_sanctioned(seg: str) -> bool:
    """A segment whose program is a doc-mirror CLI is the SANCTIONED write path — its args may name
    managed paths (and prose like '->') without that counting as a hand-edit."""
    prog = _segment_program(seg)
    return prog in SANCTIONED_PROGS or prog.startswith("docmirror-")


# A redirect that TARGETS a path (the capture is the target token). `2>/dev/null`, `>/tmp/x` etc.
# only count as a managed write when the target itself is a managed path — so reads with a benign
# stderr redirect next to a managed path (e.g. `sed -n p ctx/journal/x 2>/dev/null`) are NOT blocked.
_REDIRECT_RE = re.compile(r">>?\s*([^\s;|&]*)")
# explicit mutators that take a path ARGUMENT (managed path anywhere in the segment = it's the target).
_MUTATORS = ("| tee", "|tee", " tee ", "sed -i", "truncate", " dd ", " mv ", " cp ", " rm ",
             "rename(", "write_text(", ".write(", "open(")


def _seg_writes_managed(seg: str) -> bool:
    for m in _REDIRECT_RE.finditer(seg):           # a redirect whose TARGET is a managed path
        if any(mp in m.group(1) for mp in MANAGED):
            return True
    if any(op in seg for op in _MUTATORS) and any(mp in seg for mp in MANAGED):  # mutator + managed arg
        return True
    return False


def _bash_writes_managed(cmd: str) -> bool:
    """Block iff some shell SEGMENT (a) actually WRITES a managed path (redirect TARGET is managed, or a
    mutator op targets one) AND (b) is NOT a sanctioned CLI invocation. Per-segment + target-aware, so
    reads that merely mention a managed path (incl. with a benign `2>/dev/null`) pass, and a sanctioned
    `journal "...docs/vision..."` passes, while a raw `echo x > docs/vision/y` is still blocked."""
    if not cmd:
        return False
    for seg in re.split(r";|&&|\|\||\n", cmd):
        if not any(m in seg for m in MANAGED):
            continue
        if not _seg_writes_managed(seg):
            continue  # mentions a managed path but does not write one = a read = fine
        if _seg_is_sanctioned(seg):
            continue  # the sanctioned writer (journal/doc-mirror-commit/…) — allowed
        return True
    return False


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        sys.exit(0)  # can't parse -> don't trap
    tool = data.get("tool_name", "")
    ti = data.get("tool_input", {}) or {}

    blocked = False
    if tool in ("Write", "Edit", "MultiEdit", "NotebookEdit"):
        blocked = _path_is_managed(ti.get("file_path", "") or ti.get("notebook_path", ""))
    elif tool == "Bash":
        blocked = _bash_writes_managed(ti.get("command", ""))

    if blocked:
        print(json.dumps({
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "deny",
                "permissionDecisionReason": DENY,
            }
        }))
        print(DENY, file=sys.stderr)
        sys.exit(2)
    sys.exit(0)


if __name__ == "__main__":
    main()
