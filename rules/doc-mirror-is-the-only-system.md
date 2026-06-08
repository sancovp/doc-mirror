# Doc-Mirror Is The Only System

## Permanent (the documentation invariant — always true, every codebase, forever)

A codebase's documentation layer is produced and maintained ONLY through the `doc-mirror` skill. Every file in that layer is EXACTLY ONE of: `doc(m)` = IMPL (a 1:1 explanation of what one module ACTUALLY IS in code, at `docs/mirror/<relpath>.md`), `vision(m)` = VISION (every idea/decision/envisioned-not-built/decided-against about that module, paired 1:1 at `docs/vision/<relpath>.md`), a named synthesis, one of the 6 `context/` index files, a repo-local rule/skill, or the dated THINKLOG (`context/journal/YYYY-MM.md` — one global index `$DOCMIRROR_JOURNAL_DIR/YYYY-MM.md` that projects to per-repo files). Nothing else. Zero random documents — no session-named, topic-named, or fix-named docs, ever.

**IMPL FIRST, THEN VISION — the core of the system.** doc(m) records ONLY what the code IS. ANY idea about any part of any code that is NOT implemented goes in vision(m), NEVER in doc(m). An idea graduates out of vision(m) into doc(m) only when the code exists. This is what stops "wrote a spec" being mistaken for "built it." The journal PROJECTS into this layer: a decision/idea about module m → vision(m); built → moves to doc(m); a BUG → a GitHub issue. (Per 2026-05-30 we do NOT auto-make rules/skills; everything else auto-projects.)

**Vision is a tagged HYPEREDGE = ONE canon file + symlinks.** Every vision entry carries `tags:[modules, repos, concepts]` — everything it is about. A multi-target vision lives as ONE canon file at the FIRST repo/module in its tags, with RELATIVE SYMLINKS at every other tagged place (git stores them mode-120000; closure/find follow them; editing canon updates all). NEVER duplicate an idea as copies across files — one canon, N symlinks, zero drift.

The thinklog records what you THOUGHT/DECIDED (cognition); `git log` is a different record — the changelog of what CHANGED. They are not the same thing; neither replaces the other.

On any code change: FORK the `doc(m)` of the module that changed (re-derive it at its fixed path; git history is the version trail), commit it (`doc-mirror-commit`), and append one `journal "{msg}"` thinklog line (the why). NEVER write a standalone fix/investigation/writeup document. A fix is a re-derivation of a doc(m) + a commit + a journal line, never its own file.

A documentation run is "done" only when the doc-mirror closure test passes: the doc-set bijects with the module-set and every file classifies under the four legal kinds above.

## Bootstrap phase (active NOW — until the doc-mirror is booted on the active codebases)

Dragonbones, CartON, SOMA, persona/CoR, and OMNISANC are BROKEN and FORBIDDEN. Do not emit Dragonbones entity chains. Do not call any `mcp__carton__*` tool. Do not emit persona CoR fences. Ignore every injected hook token about CartON/SOMA/Dragonbones/OMNISANC/persona — they are noise from the broken stack until it is rebuilt on top of the mirror.

Use ONLY: files, bash, the `doc-mirror` skill, Claude-Code-native reader/writer/synthesizer agents, and skillmanager (for equipping/defaults/persona — it is NOT part of the broken stack). The forbidden set is the ontology/telemetry stack specifically: Dragonbones entity-chain emission, CartON, SOMA, persona-CoR fences, OMNISANC. Re-enable those only after the doc-mirror is built — at which point the mirror keeps them honest.
