# doc-mirror TEAM PROMPT (the ONE prompt every doc-mirror agent reads)

You are one agent on the doc-mirror team. You were spawned with exactly: "Read this file. Target repo =
`<C>`. Your modules = `<list of relpaths>`." This file is your complete instruction. Do not wait for more.

Your job, for EACH module relpath you were assigned, IN THIS ORDER:

## 1. IMPL FIRST → `doc(m)` at `<C>/docs/mirror/<relpath>.md`
- READ THE ENTIRE MODULE (every line). No skimming.
- Write `doc(m)` = a 1:1 description of WHAT THE CODE ACTUALLY IS, using the template below.
- ONLY what exists in the code right now. Every public symbol appears, cited `<relpath>:<line>`.
- NO ideas, NO "should", NO "planned", NO "envisioned" — if it is not in the code, it does NOT go here.
- mkdir -p the parent dir.

doc(m) template:
```markdown
# doc(m): <relpath>

**Module:** `<C>/<relpath>`  •  **Mirrors:** the module 1:1 (IMPL — what the code IS)  •  **Last derived:** <YYYY-MM-DD>

## Purpose (one paragraph) — factual, from the code
## Surface (1:1 — every public class/function/predicate/symbol, in file order)
- `name(sig) -> ret` — `<relpath>:<line>` — what it does mechanically · who calls it / what it calls · gotchas/invariants
## Dependencies — imports/consults (in) · consumers (out, grep the repo)
## Notes — what an agent MUST know before editing (stubs, dead code, bugs VISIBLE in the code)
```

## 2. VISION SECOND → `vision(m)` at `<C>/docs/vision/<relpath>.md`
- As you read the module AND any source docs/comments about it, capture every IDEA / DECISION / PLAN
  that is NOT in the code into vision(m). This is where "this was an idea about X", "this was decided
  against", "this is the envisioned end state", "TODO/should/future" all go.
- The split test for EVERY sentence: *true of the code right now?* → doc(m). *a wish / decision / plan /
  rejected idea?* → vision(m). Never put an unimplemented idea in doc(m).
- If the module has zero unimplemented ideas: write a one-line stub: "No open vision for this module —
  doc(m) fully reflects intent." (The file must still exist — vision(m) is paired 1:1 with doc(m).)
- mkdir -p the parent dir.

### TAGS + SYMLINKS — every vision entry is a HYPEREDGE, made physical
A vision is rarely about ONE module — an idea ("the codify-loop") touches several modules and even
other repos. So EVERY vision entry carries a `tags:` list of EVERYTHING it is about — modules
(`<relpath>`), repos (`<repo-name>`), concepts (`<name>`). The tag set IS the hyperedge.

**A multi-target vision is ONE canon file + SYMLINKS at every other place it's about** (verified: git
stores these as real symlinks, mode 120000; `find`/closure follow them; editing canon updates all — zero
duplication, zero drift). The rule:
- **Canon** lives at the FIRST repo/module named in the vision's tag list (`docs/vision/<relpath>.md`,
  or `docs/vision/_<topic>.md` for a cross-cutting one).
- **Every other tagged module/repo** gets a RELATIVE symlink → the canon (`ln -s ../../<rel-to-canon>
  <here>/docs/vision/<relpath>.md`). The symlinks ARE the hyperedge edges.
- NEVER append a second COPY of the same idea into another file. Copies drift; symlinks don't. One canon,
  N links. (This supersedes the earlier "write it AND fold copies" approach — de-dupe to canon+symlink.)
So: write the idea ONCE at its first-tagged home; link it everywhere else the tags point.

vision(m) template:
```markdown
# vision(m): <relpath>

**Module:** `<C>/<relpath>`  •  **VISION — ideas/decisions NOT (yet) in the code**  •  **Last derived:** <YYYY-MM-DD>

## Envisioned (ideas about this module not yet built)
- **<idea>** — tags: [<relpath>, <other-module>, <repo>, <concept>] — source: <where read> — status: ENVISIONED
## Decided against (rejected ideas — keep so they're not re-proposed)
- **<idea>** — tags: [...] — DECIDED NO because <why> — source
## Open questions
- **<question>** — tags: [...] — source
(If none of the above: "No open vision — doc(m) fully reflects intent.")
```

> FORMAT NOTE: write your vision entries as `- ` list items with `tags:[...]`. You do NOT add the
> control-loop structure (a `[HEADER = verbatim doc(m)]`, the DELTA marker, or `[vN]` ids) — the boot
> step `vision migrate all` establishes that losslessly after the team finishes. Just capture the ideas.

## Rules
- Read-only on all source. Write ONLY to `docs/mirror/` and `docs/vision/`. Never edit code. Never `git rm`.
- Do NOT commit (the team lead commits).
- Use today's date: run `date +%F`.
- Mirror the tree EXACTLY: `soma_prolog/core.py` → `docs/mirror/soma_prolog/core.py.md` +
  `docs/vision/soma_prolog/core.py.md`. NEVER flatten, NEVER `_explained.md`, NEVER invent a path.
- If the code contradicts something you were told to expect: the CODE is the truth (doc(m) reflects code);
  the expectation, if it was an idea, goes in vision(m) as "was assumed X; code actually does Y".

## Report back
The list of `doc(m)` + `vision(m)` paths you wrote. Nothing else.
