# THE PROCEDURE + doc(m) TEMPLATE + CLOSURE TEST (the @boot-a-codebase detail)

> Reference resource for the `doc-mirror` skill. This is the deep how-to for the
> `@pathway:boot-a-codebase` leg of `STATE_GRAPH.md` (mirror a codebase the first time). Run the steps
> in order; the closure test is the gate. Addressing + the classification LAW: `resources/the-law.md`.

## THE PROCEDURE (run these steps in order, every time)

### 1. ENUMERATE (the deterministic work-list)
Run the FIXED enumerator and write its output to the manifest. Same command ⟶ same module set ⟶ same
structure:
```bash
cd <C>
find . -type f \( -name '*.py' -o -name '*.pl' -o -name '*.ts' -o -name '*.js' \
   -o -name '*.tsx' -o -name '*.jsx' -o -name '*.go' -o -name '*.rs' \) \
  -not -path './.git/*' -not -path '*/__pycache__/*' -not -path '*/node_modules/*' \
  -not -path '*/.venv/*' -not -path '*/venv/*' -not -path '*/build/*' \
  -not -path '*/dist/*' -not -path '*/.egg-info/*' -not -path '*/_deprecated/*' \
  | sort | tee docs/mirror/_MANIFEST.txt
```
(Adjust the extension set to the codebase's languages; record the exact command used at the top of
`_MANIFEST.txt` so the enumeration is reproducible.) The manifest IS the module-set `M`. `_deprecated/` is
excluded — dead code is not mirrored.

### 2. doc(m)=IMPL FIRST, THEN vision(m) (ONE team, ONE templated prompt — the bijection)
ONE team of agents does this. Each agent is spawned IDENTICALLY — you say only:
`"Read templates/team_doc_prompt.md. Target repo = <C>. Your modules = <list>."`
You do NOT hand-write per-agent instructions — the prompt file (`templates/team_doc_prompt.md`, authored
+ tested once, lives in THIS skill) IS the instruction. Never improvise a prompt to an agent.

The templated prompt makes the agent, per module, in this order:
1. **IMPL first** — read the module ENTIRELY, write `doc(m)` at `docs/mirror/<relpath>.md` = what the code
   ACTUALLY IS (the doc(m) template below; canonical example
   `base/soma-prolog/docs/mirror/soma_prolog/core.py.md`). ONLY what exists. No ideas, no "should".
2. **VISION second** — as it reads the module AND any source docs about it, every line that is an
   IDEA / DECISION / envisioned-not-built / decided-against about that module goes in `vision(m)` at
   `docs/vision/<relpath>.md`. If the module has zero unimplemented ideas, vision(m) is a one-line stub
   saying so. Cross-cutting ideas (no single module) → `docs/vision/_<topic>.md`.
The split rule the agent applies to EVERY sentence: *is this true of the code right now?* → impl.
*is it a wish / decision / plan / rejected idea?* → vision. Never mix.

### 3. SYNTHESIZE THE 6 INDEX FILES (the connection layer)
A synthesizer agent reads the doc(m) set and writes the 6 `context/` files. They are NAVIGATION: each
points DOWN to the relevant doc(m)/vision(m). They never restate module internals — they connect and
route. (Templates: `<repo-root>/six_file_methodology/`.)

**`progress-tracker.md` is ORDERED POINTERS into vision(m) — NOT a copy of the work.** Vision BUBBLES UP:
the work content lives in `vision(m)` (the backlog); the tracker holds only SEQUENCE + STAGE, pointing
DOWN. A queue item is:
`- [ ] TODO {repo, docs/vision/<relpath>.md (or _<topic>.md)} — <one-line what> — stage: TODO|DOING|DONE`
NEVER restate the vision's content in the tracker (that duplicates → drifts — the disease). A vision entry
is a TODO until it GRADUATES to doc(m) (built). The ROOT `context/progress-tracker.md` is the cross-repo
ordered pointer (the REPO ORDER table → which repo is active); each leaf tracker is the in-repo ordered
pointer into that repo's vision(m).

### 3.5 LAYER THE STACK (EMERGENT — not explained, computed)
Once the impl doc(m) exist you KNOW every module's intra-repo imports, so the architecture stack is
DERIVABLE: run `docmirror-layers <C>` → writes `docs/mirror/_LAYERS.json` bucketing modules by import
depth (L0 = foundation data; L1 = leaf modules with no intra-repo imports; LN = outer facades; LT = tests).
Then `docmirror-system <C>` → renders `docs/SYSTEM.md` (the top-level LAYER diagram) from it. Re-run both
whenever the import graph changes. Deterministic step of every run, never designed per-repo.

### 3.6 NORMALIZE + CHECK THE VISION LAYER (into the control-loop format)
The team wrote `vision(m)` as idea entries; normalize them to the control-loop format and verify:
- `vision migrate all` — LOSSLESS: establishes `[HEADER = verbatim doc(m)] + MARKER + [DELTA: [vN]-ided
  appends]` and re-bases each module HEADER to its `doc(m)`. (Refuses to write if any line would be lost.)
- `vision check all` — the vision-layer closure test: every file has the MARKER, unique `[vN]` ids, and
  every module `HEADER == doc(m)`. Exit 0 = clean.
This makes `vision(m)` participate in the control loop: `vision diff`/`stats`/`project` (the backlog view)
and `doc-mirror-commit --realizes <ids>` (graduate vision→impl). Re-run after any later vision edits.

### 4. NAMED SYNTHESES (only when a cross-module story needs telling)
If modules interlock in a way no single doc(m) captures, write a synthesis named by the modules it
connects (`docs/synthesis/<a>__<b>.md`). Never named by a session/topic/date.

### 5. THE JOURNAL — see `resources/fork-and-loop.md` + the `use-the-journal` rule + `@pathway:record-a-thought`.

### 6. CLOSURE TEST (prove the run is invariant — do not skip)
```bash
cd <C>
# (i) IMPL bijection — every module has exactly one doc(m), every doc(m) maps to exactly one module:
comm -3 <(sed 's#^\./##' docs/mirror/_MANIFEST.txt | sed 's#$#.md#' | sort) \
        <(cd docs/mirror && find . -name '*.md' -not -name '_MANIFEST.txt' | sed 's#^\./##' | sort)
# ^ MUST print nothing. Any line = a gap (module without doc) or an orphan (doc without module).
# (ii) VISION pairing — every module has a vision(m) too (may be a "no open ideas" stub):
comm -3 <(sed 's#^\./##' docs/mirror/_MANIFEST.txt | sed 's#$#.md#' | sort) \
        <(cd docs/vision 2>/dev/null && find . -name '*.md' | grep -v '^\./_' | sed 's#^\./##' | sort)
# ^ MUST print nothing too (excluding docs/vision/_<topic>.md cross-cutting files).
# (iii) 6 index files present:
ls context/{project-overview,architecture,code-standards,ai-workflow-rules,ui-context,progress-tracker}.md
# (iv) no illegal files: every .md under docs/ + context/ classifies under THE LAW; ANY unimplemented
# idea sitting in a doc(m) instead of its vision(m) is ILLEGAL (impl must be code-only):
find docs context -name '*.md' | sort
```
If `comm -3` prints anything, or any file fails to classify under THE LAW, the run is NOT done. Fix (write
the missing doc / delete or fold the illegal file) and re-test. (Filename drift note: sonnet writers
sometimes emit `<name>_<ext>_explained.md`; normalize to `<relpath>.md` before the closure test — see the
`doc-mirror-normalize-doc-filenames-before-closure` rule.)

## doc(m) TEMPLATE (fixed shape — every doc(m) looks like this)

```markdown
# doc(m): <relpath>

**Module:** `<C>/<relpath>`  •  **Mirrors:** the module 1:1  •  **Last derived:** <YYYY-MM-DD>

## Purpose (one paragraph)
What this module is and why it exists in the codebase.

## Surface (1:1 — every public thing, in file order)
For EACH class / function / predicate / exported symbol:
- `name(signature) -> return`  — `<relpath>:<line>`
  - what it does (mechanically)
  - why it exists / who calls it / what it calls
  - any non-obvious behavior, gotcha, or invariant

## Dependencies
- imports / consults / requires (what this module pulls in)
- consumers (what pulls this module in), if known from the rest of the mirror

## Notes
Anything an agent must know before editing this module.
```

Cite by `path:line` throughout. The doc IS the module, explained. No summaries that lose detail — 1:1
means every symbol appears.
