#!/usr/bin/env python3
"""PreToolUse(Bash) guard: block shell command-substitution inside doc-mirror WRITE-CLI messages.

THE TRAP THIS PREVENTS (a real 2026-06-25 accident): a doc-mirror write CLI takes a prose message
as an ARGUMENT, e.g.  journal -t DECISION "... run `switch_persona.py megnomorph` to ..."  — when that
message is DOUBLE-quoted (or unquoted), bash performs COMMAND SUBSTITUTION on the backticks / $(...)
BEFORE the CLI ever sees the text, so the embedded command ACTUALLY RUNS (and its stdout is spliced into
the message). That fired a live persona switch. A rule alone did not prevent it; this hook does.

WHAT IT DOES: if a Bash command invokes a doc-mirror write CLI (journal / docmirror-done /
docmirror-cursor / docmirror-task / tracker / vision / doc-mirror-commit) AND contains a backtick or
$( that is NOT inside single quotes, it BLOCKS (exit 2) with guidance. Single-quoted backticks are safe
(bash does not substitute inside single quotes), so those pass. Normal commands (git, python with $(...))
are untouched — the guard only fires for the prose-message write CLIs.

THE SAFE PATTERN it nudges toward: single-quote the whole message, or write command names as PLAIN TEXT
with no backticks / $().
"""
import json
import logging
import os
import re
import sys

_ERR_LOG = os.path.join(os.environ.get("HEAVEN_DATA_DIR", "/tmp/heaven_data"),
                        "docmirror_journal_guard_errors.log")
logging.basicConfig(filename=_ERR_LOG, level=logging.ERROR,
                    format="%(asctime)s %(levelname)s %(message)s")
_logger = logging.getLogger("docmirror_journal_guard")

WRITE_CLIS = (
    "journal", "docmirror-done", "docmirror-cursor", "docmirror-task",
    "tracker", "vision", "doc-mirror-commit",
)
# a write CLI at a command position: start of string, or after ; | & or &&/|| or newline
_CLI_RE = re.compile(
    r"(?:^|[\n;&|])\s*(?:" + "|".join(re.escape(c) for c in WRITE_CLIS) + r")\b"
)
_SINGLE_QUOTED = re.compile(r"'[^']*'")


def _has_substitution_outside_single_quotes(command: str) -> bool:
    # Remove single-quoted spans (bash never substitutes inside '...'); check the remainder.
    remainder = _SINGLE_QUOTED.sub("", command)
    return ("`" in remainder) or ("$(" in remainder)


def main() -> None:
    try:
        data = json.load(sys.stdin)
    except Exception:
        # Fail OPEN (a guard hook must never crash-block the agent), but log the traceback so a
        # real hook bug is observable instead of silently swallowed. logging.exception captures it.
        _logger.exception("journal_substitution_guard: stdin JSON parse failed")
        sys.exit(0)
    if data.get("tool_name") != "Bash":
        sys.exit(0)
    command = (data.get("tool_input") or {}).get("command", "") or ""
    if not _CLI_RE.search(command):
        sys.exit(0)  # not a doc-mirror write CLI invocation
    if not _has_substitution_outside_single_quotes(command):
        sys.exit(0)  # no risky substitution
    sys.stderr.write(
        "BLOCKED: this command invokes a doc-mirror write CLI (journal/docmirror-*/tracker/vision/"
        "doc-mirror-commit) AND contains a backtick or $( OUTSIDE single quotes. In a double-quoted or "
        "unquoted message, bash COMMAND-SUBSTITUTES those BEFORE the CLI sees them — the embedded command "
        "actually RUNS (this caused a live accidental persona switch on 2026-06-25).\n"
        "FIX: write command names as PLAIN TEXT with no backticks/$(), or SINGLE-QUOTE the whole message "
        "(bash does not substitute inside '...'). Then re-run.\n"
    )
    sys.exit(2)  # block; stderr is shown back to the agent


if __name__ == "__main__":
    main()
