# FORK-ON-CHANGE + THE JOURNAL + THE LOOP (the @change / @think / loop detail)

> Reference resource for the `doc-mirror` skill. Deep how-to for maintaining a mirror once booted —
> the `@pathway:change-a-module`, `@pathway:record-a-thought`, and the top-level loop legs of
> `STATE_GRAPH.md`. The operating spine + cursor are in `STATE_GRAPH.md`; this is the prose behind it.

## FORK-ON-CHANGE (the maintenance invariant — ONE git commit per change)

The fork mechanic IS git. A module change and its re-derived `doc(m)` land in ONE atomic commit, and
`git log -p docs/mirror/<m>.md` is that module's **diffed markdown lineage**. No separate versioning
scheme — git is the version trail.

When module `m` changes:
1. RE-DERIVE `doc(m)` from the changed module (a fresh reader/writer pass). This is the AGENT's job — it
   is semantic (what changed + why), which no script can supply. Replace `doc(m)` at its fixed path; bump
   `**Last derived:**`.
2. COMMIT the code change + the re-derived `doc(m)` TOGETHER, explanation as the message:
   ```
   doc-mirror-commit <m-relpath> "<what changed>" "<why>" "<ORIGIN: vision it realizes / bug it fixes>"
   ```
   The helper is DUMB plumbing: it stages `m` + `docs/mirror/<m>.md`, formats the commit, and **REFUSES
   to commit a code change whose doc was not re-derived** (anti-drift) and **REFUSES a change with no
   ORIGIN** (must realize a vision / fix a bug). It contains no LLM — you supply the meaning, it enforces
   the convention.
3. Re-run the SYNTHESIZER over the affected `context/` files when structure changed.
4. NEVER append a standalone "fix writeup" / "investigation" / "what-I-changed" doc. A fix is a
   re-derivation of the `doc(m)` of the module it touched + one commit. That is all.

git log is the CHANGELOG (what changed, per atomic commit). The JOURNAL is the THINKLOG (why you changed
it, what you decided, what's still open) — a separate dated file. Write the commit for the change; write
the `journal` line for the thinking. Different records, both kept.

A fix is never its own document. This is the single rule that kills the disease (the numbered pile).

## THE JOURNAL (the dated thinklog — one global that projects to per-repo)

The journal records what you THOUGHT and DECIDED — the cognition behind the changes. git log is a
different record (what CHANGED); it does not hold thinking, so it is NOT the journal.

- You append with `journal -t <TYPE> --repo <name|path> --tags <module-or-topic,...> "<msg>"`. ROUTING is
  by `--repo`, else the cursor's `active_repo`, else `-g` (global) — NEVER cwd. It writes the GLOBAL index
  + the repo's thinklog, and PROJECTS vision-types into the vision layer: a module-tag → its paired
  vision(m); a topic-tag → `<repo>/docs/vision/_<topic>.md` (auto-created), each append getting a stable
  `[vN]` id. EVERY type projects EXCEPT COMMIT (the impl-changer). It RAISES if a vision-type can't be
  homed (no module-tag + no repo) — add `--tags`/`--repo`, or `-g`. You NEVER hand-edit the journal/vision/
  tracker files (the `docmirror_readonly_guard` hook blocks it; use the CLI). Full syntax: the
  `use-the-journal` rule.
- Append the moment you: set an INTENT, make/receive a DECISION (+ why + alternatives rejected), hit an
  unclear fork (write it as `-t OPEN`, then `docmirror-sleep` — the sleep echoes the OPEN back to Isaac;
  NEVER auto-decide architecture/irreversible forks), discover a FINDING, or reject a HYPOTHESIS.

**THE JOURNAL PROJECTS OUT (the point of it).** A journal line about a module is not terminal — a
DECISION/idea/rejection about module m → into that module's `vision(m)`. When the idea gets BUILT → it
moves from vision(m) into `doc(m)` (impl). So: think it (journal) → it lands as vision → you build it → it
becomes impl. That flow is why impl and vision are separate, paired files. (Per 2026-05-30 we do NOT
auto-make rules/skills — those stay manual; everything else auto-projects.)

## THE LOOP (how you actually operate — everything immediate, nothing batched)

The loop runs via the **brainhook Stop hook** (`~/.claude/hooks/docmirror_brainhook.py`), which re-injects
`~/.claude/docmirror_loop_prompt.txt` + the current cursor leg every Stop so you keep working on-script;
and the **SessionStart hook** re-boots the cascade after a compact. Per turn you are at the phase your
**cursor** (`docmirror-cursor`) names; act ONLY on that phase's leg. The phases + branches are the
operating state graph (`STATE_GRAPH.md`). In brief:

1. ORIENT: read SYSTEM.md → ROOT progress-tracker (active repo) → that repo's `context/` → the doc(m).
   Read the cursor; resume its phase.
2. SELECT/do the next queue item via the matching pathway.
3. **Commit immediately** on any module change (the @change pathway): re-derive `doc(m)`, then
   `doc-mirror-commit` (code+doc atomic, full what/why/ORIGIN). Keep the tree clean — never batch. Then
   `journal` the THINKING.
4. **Harvest** rules/skills the moment you notice one (the @harvest pathway): repo-local `cat >`. If you
   learn a rule/skill and don't write it, it evaporates.
5. **Idle** only via `docmirror-sleep` (8h, 9-min chunks). **Compact** at a seam: clean tree → journaled →
   `self_compact &` → 👍.

Emit is just `cat` / the CLIs — no pipeline. You supply the meaning; the file IS the artifact.
