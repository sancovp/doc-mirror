#!/usr/bin/env python3
"""
docmirror_brainhook — the doc-mirror work-loop Stop hook (our fork of autopoiesis brainhook).

Blocks Stop while enabled, re-injecting the doc-mirror loop prompt each turn so the agent
re-anchors into the six-file/doc-mirror system. Every Nth turn (default 10) it also appends
the HARVEST reminder (how to emit a rule/skill) so reusable learnings don't evaporate.

OURS — not the plugin. Reads prompt paths WE own; uses OUR state files. No broken-stack imports.
Forked from twi-marketplace/autopoiesis brainhook.py (kept its degenerate-loop safety).

Enable:  docmirror-brainhook   (toggles /tmp/docmirror_brainhook_state.txt on/off)
Steer:   edit ~/.claude/docmirror_loop_prompt.txt        (re-read fresh every Stop)
         edit ~/.claude/docmirror_harvest_reminder.txt   (the every-N harvest checkpoint)

Stop-hook contract: print {"decision":"approve"} to allow stop, {"decision":"block","reason":...} to continue.
"""
import json
import logging
import sys
import traceback
from pathlib import Path

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    filename="/tmp/docmirror_brainhook.log",
)
logger = logging.getLogger("docmirror_brainhook")

STATE_FILE = Path("/tmp/docmirror_brainhook_state.txt")
COUNTER_FILE = Path("/tmp/docmirror_brainhook_turn.txt")
PROMPT_FILE = Path.home() / ".claude" / "docmirror_loop_prompt.txt"
HARVEST_REMINDER_FILE = Path.home() / ".claude" / "docmirror_harvest_reminder.txt"
HARVEST_EVERY = 10  # show the harvest reminder every Nth blocked turn
# Journal-types reminder: appended EVERY turn (you must always be told the journal syntax).
# Canonical source = the doc-mirror skill templates dir; ~/.claude copy is a fallback.
JOURNAL_REMINDER_FILE = Path.home() / ".claude" / "skills" / "doc-mirror" / "templates" / "journal_reminder.txt"
JOURNAL_REMINDER_FALLBACK = Path.home() / ".claude" / "docmirror_journal_reminder.txt"

DEFAULT_PROMPT = (
    "You are in a doc-mirror brainhook session. Read the ROOT progress-tracker "
    "(<repo-root>/context/progress-tracker.md), descend to the active repo's "
    "context/, commit changes with doc-mirror-commit as you go, and idle with docmirror-sleep "
    "if the queue is empty. (Prompt file missing — using fallback.)"
)


def is_enabled() -> bool:
    try:
        return STATE_FILE.exists() and STATE_FILE.read_text().strip().lower() == "on"
    except Exception:
        return False


def bump_turn() -> int:
    """Increment + return the per-loop turn counter. Resets implicitly when the file is cleared."""
    try:
        n = int(COUNTER_FILE.read_text().strip()) if COUNTER_FILE.exists() else 0
    except Exception:
        n = 0
    n += 1
    try:
        COUNTER_FILE.write_text(str(n))
    except Exception as e:
        logger.warning(f"counter write error: {e}")
    return n


def get_prompt() -> str:
    try:
        if PROMPT_FILE.exists():
            return PROMPT_FILE.read_text().strip()
    except Exception as e:
        logger.warning(f"prompt read error: {e}\n{traceback.format_exc()}")
    return DEFAULT_PROMPT


def get_harvest_reminder() -> str:
    try:
        if HARVEST_REMINDER_FILE.exists():
            return HARVEST_REMINDER_FILE.read_text().strip()
    except Exception as e:
        logger.warning(f"harvest reminder read error: {e}")
    return ""


def get_journal_reminder() -> str:
    """The journal-types reminder — appended EVERY blocked turn. Canonical source is the doc-mirror
    skill templates dir; falls back to the ~/.claude copy. Empty string if neither exists (fail-open)."""
    for f in (JOURNAL_REMINDER_FILE, JOURNAL_REMINDER_FALLBACK):
        try:
            if f.exists():
                return f.read_text().strip()
        except Exception as e:
            logger.warning(f"journal reminder read error: {e}")
    return ""


def get_cursor_block() -> str:
    """The live CURSOR (current phase + its leg) — appended EVERY blocked turn so the script's
    'you are here' pin is always in front of the agent (the soft-script + hard-cursor coupling).
    Runs the docmirror-cursor CLI; fail-open to '' so a cursor bug never traps the agent."""
    import subprocess
    for bin_path in ("docmirror-cursor", str(Path.home() / ".local" / "bin" / "docmirror-cursor")):
        try:
            out = subprocess.run([bin_path, "show"], capture_output=True, text=True, timeout=3)
            if out.returncode == 0 and out.stdout.strip():
                return ("\n--- YOUR CURSOR (the 'you are here' pin — act ONLY on this phase's leg) ---\n"
                        + out.stdout.strip())
            return ""
        except FileNotFoundError:
            continue
        except Exception as e:
            logger.warning(f"cursor read error: {e}")
            return ""
    return ""


def _output(decision: str, reason: str = None):
    result = {"decision": decision}
    if reason:
        result["reason"] = reason
    print(json.dumps(result))
    sys.exit(0)


def check_degenerate_loop(hook_input) -> bool:
    """3+ consecutive sub-100-char assistant responses = degenerate loop."""
    try:
        tp = hook_input.get("transcript_path")
        if not tp or not Path(tp).exists():
            return False
        import subprocess
        out = subprocess.run(["tail", "-20", tp], capture_output=True, text=True, timeout=2).stdout
        short = 0
        for line in reversed(out.strip().split("\n")):
            try:
                entry = json.loads(line)
            except (json.JSONDecodeError, KeyError):
                continue
            if entry.get("type") == "assistant":
                msg = entry.get("message", {})
                if not isinstance(msg, dict):
                    break
                text = "".join(
                    b.get("text", "")
                    for b in msg.get("content", [])
                    if isinstance(b, dict) and b.get("type") == "text"
                )
                if len(text.strip()) < 100:
                    short += 1
                else:
                    break
        return short >= 3
    except Exception as e:
        logger.warning(f"degenerate check error: {e}")
        return False


LAPSE_WARNING = (
    "⚠️ ATTENTION LAPSE — 3+ short responses in a row to this hook. You are burning "
    "context doing nothing. Break the loop: do the next progress-tracker task, OR "
    "idle with docmirror-sleep, OR tell the user you are waiting. Do NOT reply short again."
)


def main():
    try:
        hook_input = json.load(sys.stdin)
    except Exception:
        hook_input = {}
    try:
        if not is_enabled():
            _output("approve")
        if check_degenerate_loop(hook_input):
            logger.warning("degenerate loop -> lapse warning")
            _output("block", LAPSE_WARNING)
        # normal blocked turn: the loop prompt, + the JOURNAL reminder EVERY turn, + the HARVEST reminder every Nth.
        turn = bump_turn()
        prompt = get_prompt()
        journal_reminder = get_journal_reminder()
        if journal_reminder:
            prompt = f"{prompt}\n\n{journal_reminder}"
        cursor_block = get_cursor_block()
        if cursor_block:
            prompt = f"{prompt}\n{cursor_block}"
        if turn % HARVEST_EVERY == 0:
            reminder = get_harvest_reminder()
            if reminder:
                prompt = f"{prompt}\n\n{reminder}"
        _output("block", prompt)
    except Exception as e:
        logger.error(f"fatal: {e}\n{traceback.format_exc()}")
        _output("approve")  # fail-open: never trap the agent on a bug


if __name__ == "__main__":
    main()
