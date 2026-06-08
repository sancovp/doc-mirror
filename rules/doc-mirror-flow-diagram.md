# Doc-Mirror Flow — the one diagram (always-in-context orientation)

Two views of the same system. The LAW: every doc-layer file is exactly one of — doc(m)=IMPL,
vision(m)=VISION, the 6 context files, a named synthesis, a repo-local rule/skill, the dated journal.
Full law: `doc-mirror-is-the-only-system.md` + the `doc-mirror` skill.

## 1. THE LAYERS — up holds pointers DOWN (where everything lives)

```
        ┌─────────────────────────────────────────────────────────────┐
ROOT    │ context/progress-tracker.md  = REPO ORDER (which repo active) │  cross-repo
        │ context/journal/YYYY-MM.md   = GLOBAL thinklog ([repo] tags)  │  ──┐ pointers
        └───────────────────────────────┬─────────────────────────────┘    │ down
                                         │ points down to the active repo   │
   ┌─────────────────────────────────────▼────────────────────────────┐    │
   │ LEAF repo  <C>/context/                                           │    │
   │   6 index files (project-overview/architecture/code-standards/    │    │
   │     ai-workflow-rules/ui-context) — NAVIGATION, point down        │    │
   │   progress-tracker.md — ORDERED POINTERS into vision(m) (seq+stage)│    │
   │   journal/YYYY-MM.md  — this repo's thinklog                       │    │
   └───────────────┬──────────────────────────────┬────────────────────┘    │
                   │ point down                    │ point down               │
        ┌──────────▼───────────┐        ┌──────────▼───────────┐             │
        │ docs/mirror/<rel>.md  │ 1:1 ↔ │ docs/vision/<rel>.md  │             │
        │ doc(m) = IMPL         │ paired│ vision(m) = VISION     │◀── canon+   │
        │ (what the code IS)    │       │ (ideas/decisions,      │   symlinks  │
        │                       │       │  tagged HYPEREDGES)    │   to other  │
        └──────────▲────────────┘       └────────────────────────┘   tagged repos
                   │ mirrors 1:1
            ┌──────┴───────┐
            │  the CODE     │  (modules; the manifest enumerates them)
            └───────────────┘
```

## 2. THE CYCLE — think → build → project (how it runs over time)

```
   journal "<msg>"  ── the single write surface (thinklog) ──┐
        │                                                     │ projects out:
        ├─ DECISION/idea about m ─────────────────────────────▶ vision(m)   (the backlog)
        ├─ OPEN (can't resolve) ─▶ docmirror-sleep ─▶ echoes to Isaac
        ├─ rollup since last commit ──────────────────────────▶ commit body
        │
   build the idea (code change)
        │
        ▼
   doc-mirror-commit <m> "<what>" [why] [ORIGIN]
        │  • REFUSES code change whose doc(m) wasn't re-derived (anti-drift)
        │  • REFUSES code change with no ORIGIN (must realize a vision / fix a bug)
        ▼
   doc(m) updated (IMPL)  +  the realized idea GRADUATES vision(m) → doc(m)  +  git commit (changelog)
        │
        ▼
   CLOSURE TEST (do not skip): (i) manifest ↔ doc(m) biject  (ii) every doc(m) has a vision(m)
                               (iii) 6 context files present  (iv) no illegal files
```

**Read this first when working in any doc-mirror repo.** Orient from the layers (view 1), operate by the
cycle (view 2). git log = changelog (what changed); journal = thinklog (what you thought) — never the same.
