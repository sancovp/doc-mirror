# Doc-Mirror Files Are CLI-Only — Read-Only To You Except Through The CLI — VITAL NON-NEGOTIABLE

These files are **READ-ONLY to you**. You **NEVER** create or edit them by hand — not with Write,
Edit, MultiEdit, a Bash redirect (`>`/`>>`/`tee`/`sed -i`), a `cp`/`mv`/`rm`, or a Python heredoc. The
**ONLY** way you ever write them is by invoking the doc-mirror **CLI**, which categorizes what you say
and writes/updates/reorganizes the files for you. The syntax on these files is the entire point: a
hand-edit bypasses it and propagates exactly the drift this whole system exists to kill.

## The managed files (any path matching these) — CLI-ONLY, never hand-touch
- `**/docs/mirror/**`      (doc(m) = IMPL)        — written by re-derive + `doc-mirror-commit`
- `**/docs/vision/**`      (vision(m) = VISION)   — written by `journal` projection
- `**/context/journal/**`  (the thinklog)          — written by `journal` ONLY
- `**/context/progress-tracker.md` (the queue)     — written by the `tracker` CLI (`register`/`active` for
  the ROOT REPO ORDER router; `add`/`strike` for the PLAN pointers), never by hand

## What you do instead (always)
- To record a thought / decision / finding / intent / open-fork → `journal "<msg>"` (you supply the
  TYPE: VISION/COMMIT/INTENT/DECISION/OPEN/FINDING; the system files + organizes it). NEVER append to a
  journal/vision/tracker file yourself.
- To update a `doc(m)` for a changed module → re-derive it, then `doc-mirror-commit <m> "<what>" "<why>"
  "<origin>"`. NEVER hand-write a doc(m).
- To update the PLAN / REPO ORDER → `tracker add <vision-ref>` / `tracker strike <ref>` / `tracker
  register <repo>` / `tracker active <repo>`. NEVER hand-edit the progress-tracker.
- To READ them → `cat`/`sed -n`/`grep`/`vision <tag>`/`plan`/`projects`/`tracker show` are fine. Reading
  is allowed; writing is not.

## Why (so this never gets rationalized away)
Even when asked to "update the rehydration files" or "capture this," the correct action is to call the
CLI — not to edit the file. If the CLI can't yet express it, that is a CLI gap to FIX, not a license to
hand-edit. A hand-edit is never the answer, in any scenario, with zero exceptions. The
`docmirror_readonly_guard` PreToolUse hook enforces this; if it blocks you, you used the wrong path —
switch to the CLI.
