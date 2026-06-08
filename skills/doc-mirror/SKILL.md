---
name: doc-mirror
description: The invariant procedure that produces and maintains a 1:1 documentation mirror of ANY codebase. Use whenever you need to understand, document, begin working on, or re-sync a codebase, or when a module changes. Produces the SAME deterministic structure every run for every agent. Forbids random documents.
---

# DOC-MIRROR — the operating state graph (index)

This skill is the GENERATOR + the OPERATING LOOP. It produces a 1:1 documentation mirror of a codebase,
and it is the **state graph the agent runs in** while working any doc-mirror repo. Two agents running it
on the same codebase produce the SAME structure — that invariance is the point.

**The flow is SCRIPTED. You do not improvise it.** Before every action: read your cursor
(`docmirror-cursor show`) → it names your current **phase** → act ONLY on that phase's leg. The full
script (the spine + every branch + every pathway) is the operating state graph:

  → **`<repo-root>/doc-mirror-system/STATE_GRAPH.md`** (read it; it is the map)

The hard layer (the "you are here" pin) is the cursor CLI `docmirror-cursor`
(show / set --phase / leg / advance / clear). The soft layer (this script) is injected every turn by the
brainhook + session_start hooks and carried always-on by the `doc-mirror-consult-state-graph-before-acting`
rule. This SKILL.md is the INDEX: each phase → its pathway in STATE_GRAPH.md → its deep resource/CLI.

## THE PHASES (each = one leg; pick via SELECT, resume via the cursor)

| phase / pathway | when | steps (STATE_GRAPH @pathway) | deep resource / CLI |
|---|---|---|---|
| **orient** | session start / post-compact / new turn | read SYSTEM.md → ROOT tracker (active repo) → 6 ctx → doc(m) → cursor | `SYSTEM.md`, root `context/progress-tracker.md` |
| **select** | a turn with a free cursor | exhaustive `<<choice>>` over the 7 pathways below | `STATE_GRAPH.md` top-level graph |
| **change** | a module changed / code to write | read-whole → edit (or dispatch+verify) → re-derive doc(m) → `doc-mirror-commit` → closure CHECK → graduate vision→doc(m) | `resources/fork-and-loop.md`; `doc-mirror-commit` |
| **init** | active codebase not mirrored | guard → register → 6 ctx → enumerate → team doc(m)+vision(m) → synthesize → layers → closure test | `resources/the-procedure.md`; `doc-mirror-init` skill; `templates/team_doc_prompt.md` |
| **prompt** | need an agent to DO a task | search prompt index → dispatch a proven prompt-skill, else author CoR-first + test + reify | `doc-mirror-prompts` skill |
| **think** | a thought/decision/finding/fork | choose TYPE → `journal -t <TYPE>` (system files+organizes+projects); OPEN → sleep → Isaac | `resources/fork-and-loop.md`; `use-the-journal` rule; `journal` |
| **seework** | "what needs doing?" | BACKLOG = the VIEW (`vision stats`→`vision project <p>`→`vision diff <m>`, derived/always-true); the tracker = your MANUAL prioritized PLAN of pointers into the gaps, reconciled by the view | `vision stats/project/diff`, `plan`, `projects` |
| **harvest** | reusable rule/skill noticed | RULE→`.claude/rules/<slug>.md` or SKILL→`.claude/skills/<name>/SKILL.md` (WHAT+WHEN desc) | `docmirror_harvest_reminder.txt` |
| **idle** | queue empty / clean seam | context high → `self_compact &` → 👍 ; queue empty → `docmirror-sleep` | `docmirror-sleep` |
| **(stuck)** | cannot resolve a fork | `X` → `journal -t OPEN` → `docmirror-sleep` (echoes to Isaac) — the ONLY off-script exit; never auto-decide | — |

## THE INVARIANT (THE LAW — check after every run)

Every file in a codebase's doc layer is EXACTLY ONE of: doc(m)=IMPL · vision(m)=VISION · named synthesis ·
one of the 6 context files · a repo-local rule/skill · the dated journal. Nothing else. The closure test
is the gate. Full statement + the deterministic addressing: **`resources/the-law.md`** (and the global
`doc-mirror-is-the-only-system` rule). doc(m) records ONLY what the code IS; any unbuilt idea goes in
vision(m). Managed files (docs/mirror, docs/vision, context/journal, progress-tracker) are CLI-ONLY —
never hand-edit them (the `docmirror_readonly_guard` hook enforces it; use `journal` / `doc-mirror-commit`
/ `tracker` — each managed file has its CLI actuator).

## VISION IS MEGA PRE-MODULE, THEN GRADUATES BY TAG (how a design becomes modular)

A design with no code yet has no module to pair vision against — so ALL of it accumulates in ONE topic
vision file (`docs/vision/_<topic>.md`). That mega-vision is CORRECT, not a bug: it is the only honest
home for a pre-build design. **Modularity is CODE-derived** — it arrives only when modules exist. As each
module is built (its `doc(m)` lands), GRADUATE its slice of the mega out by TAG:
- `vision tag <topic> vN +<component> -<old>` — label entries by their planned component (stashes the
  prior set as `was:[...]@ts`; the entry does NOT move, only its routing label changes).
- `vision graduate <relpath> --from <topic> --by-tags <component>` — MOVE every entry tagged
  `<component>` from the topic INTO the built module's paired `vision(m)` (REFUSES unless
  `docs/mirror/<relpath>.md` exists). Lossless. The mega shrinks toward empty as the system gets built.

Never split a topic into topics by hand — that is drift. The ONLY reorg is **tag-routed graduation INTO
a built module**. (id-based `doc-mirror-commit --realizes <ids> --realizes-from <topic>` is the same move
when you know the exact ids instead of a tag.)

## CoR (bind this to the codebase in front of you)

Now I am in a doc-mirror session. I read my cursor (`docmirror-cursor show`) before acting; it names my
phase, and I act only on that phase's leg from `STATE_GRAPH.md`. When I do code: I read the whole module,
re-derive its `doc(m)`, and `doc-mirror-commit` code+doc atomically with an ORIGIN. When I think: I
`journal -t <TYPE>` and let the system file it — I never hand-edit the managed files. When I hit a fork I
cannot resolve, I `journal -t OPEN` and `docmirror-sleep` rather than freestyle. The run is done only when
the closure test passes and every file classifies under THE LAW.
