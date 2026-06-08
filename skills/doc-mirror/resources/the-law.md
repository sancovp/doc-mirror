# THE LAW + DETERMINISTIC ADDRESSING (the invariant — check it after every run)

> Reference resource for the `doc-mirror` skill. The agent-facing flow is the operating state graph
> (`doc-mirror-system/STATE_GRAPH.md`); this file holds the classification law + the fixed paths that
> EVERY pathway obeys. (Also stated globally in the `doc-mirror-is-the-only-system` rule.)

## THE LAW

For a codebase `C`, every file in its documentation layer is EXACTLY ONE of:

```
(a) doc(m)  = IMPL      — a 1:1 explanation of what module m ∈ C ACTUALLY IS (the code that exists).
                        Path: docs/mirror/<relpath>.md. Made FIRST, always.
(b) vision(m) = VISION  — every IDEA/DECISION about module m that is NOT (yet) in the code: "this was
                        an idea about this", "this was decided no", "this is envisioned, not built".
                        Paired 1:1 with doc(m). Path: docs/vision/<relpath>.md. (Module-less / cross-cutting
                        vision → docs/vision/_<topic>.md.) An idea only graduates OUT of vision(m) when
                        the code exists — then it moves into doc(m) (impl) and leaves vision.
(c) a named synthesis — connects NAMED modules (filename = the modules it connects)
(d) an index file     — one of the 6 fixed context/ files
(e) a repo-local rule/skill — <C>/.claude/rules/<slug>.md or <C>/.claude/skills/<name>/SKILL.md
                        (harvested as you work; see the @harvest pathway)
(f) the journal       — the dated THINKLOG: one global index that projects to per-repo
                        thinklogs. git-tracked, dated, append-only.
```
**IMPL FIRST, THEN VISION.** doc(m) records ONLY what the code IS. ANY idea about any part of any code
that is NOT implemented goes in vision(m) — NEVER in doc(m). When reading source/docs an agent says
"this was an idea about X" / "this was decided against" / "this is the envisioned end state" → that line
goes in vision(m), not impl. This is how the system never again conflates "wrote a spec" with "built it":
impl = what is, vision = what is wished/decided/rejected. The journal PROJECTS into both (you journal a
decision → it lands in the relevant vision(m); you implement it → it moves to doc(m)).

The journal is a FILE (the thinklog of what you THOUGHT/decided). git log is the changelog of what
CHANGED. Not the same; neither replaces the other.

NOTHING ELSE. Zero random documents. A "random document" = a file named by a session, a topic, a fix, or
an investigation, that is not (a)…(f). (A DATED thinklog file is legal — kind (f); a vision(m) at its
mirrored path is legal — kind (b); the disease was topic/fix/session-NAMED sprawl AND putting
unimplemented ideas into impl docs.) If a file does not classify as one of the six, it is illegal: delete
it or fold its content into the doc(m) (if implemented) or vision(m) (if it is an idea/decision) of the
module it is about.

This LAW is the closure test. A run is correct iff, afterward, EVERY file in the doc layer classifies and
the doc-set bijects with the module-set.

## DETERMINISTIC ADDRESSING (so the structure is identical every run)

Fixed, computable paths — no agent ever invents a location:

```
module m at <C>/<relpath>           ⟶  doc(m)=IMPL at  <C>/docs/mirror/<relpath>.md
module m's ideas/decisions          ⟶  vision(m) at   <C>/docs/vision/<relpath>.md   (paired 1:1 with doc(m))
cross-cutting / module-less vision  ⟶  <C>/docs/vision/_<topic>.md
vision ABOUT a different repo D     ⟶  <D>/docs/vision/<relpath>.md  (or <D>/docs/vision/_<topic>.md)
   HAD-during ≠ IS-ABOUT: the journal line stays in the repo you were IN (provenance / [tag]); the
   vision(m) projects to the repo it is ABOUT. An idea had during SOMA work about dragonbones lands in
   automation/dragonbones/docs/vision/, NOT base/soma-prolog/docs/vision/. Subject decides the home.
the 6 index files                   ⟶  <C>/context/{project-overview,architecture,
                                         code-standards,ai-workflow-rules,ui-context,
                                         progress-tracker}.md
a synthesis of modules x,y,z        ⟶  <C>/docs/synthesis/<x>__<y>__<z>.md
a repo-local rule / skill           ⟶  <C>/.claude/rules/<slug>.md  /  <C>/.claude/skills/<name>/SKILL.md
the auditable module manifest       ⟶  <C>/docs/mirror/_MANIFEST.txt  (the enumerator output)
the GLOBAL journal index            ⟶  $DOCMIRROR_JOURNAL_DIR/YYYY-MM.md   (one place; "{now} UPDATED {repo}: {msg}")
the per-repo journal projection     ⟶  <C>/context/journal/YYYY-MM.md      (the actual "{now} {msg}" lines for C)
```

`doc(m)` path is a pure function of `m`'s path (mirror the tree). One module ⟷ exactly one doc. Given
`C`, the entire target layout is computable before any doc is written.
