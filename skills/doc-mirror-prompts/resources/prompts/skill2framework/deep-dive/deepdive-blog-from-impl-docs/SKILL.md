---
name: deepdive-blog-from-impl-docs
domain: skill2framework   subdomain: deep-dive
description: "WHAT: produces Blog 2 of a framework CHAPTER — the mechanical DEEP-DIVE technical article ('how it actually works') — for an already-built AIOS by reading its impl docs (doc(m) + SYSTEM.md + STATE_GRAPH) and assembling a faithful how-it-works explanation that links back to Blog 1. It explains mechanics ONLY from what the impl docs say IS (not vision, not invented). WHEN: when producing the deep-dive half of a framework chapter, when you need the technical how-it-works post that Blog 1 links to, or when the user mentions blog 2 / the deep dive / skill2framework (any of)."
golden: false
score: 1.00   runs: 1   verified_good: 1
check_level: FULL_E2E   last_verified: 2026-06-03
log:
  - "2026-06-03 PASS — dogfood on doc-mirror. Subagent read SYSTEM.md + STATE_GRAPH.md + DOC_MIRROR_SYSTEM.md (no docs/mirror/ exists for doc-mirror-system itself — it's a meta-repo, honestly noted) and assembled Blog 2 at /home/GOD/tmp/framework_recon/doc-mirror_blog2.md. I verified E2E myself: all 5 diagrams reproduced VERBATIM (LAYER/FLOW/GEOMETRY/spine-mermaid/LIFECYCLE) + the cursor-fields block + transition-hook pseudocode + legal-transitions table, every section cited to a specific impl doc, mechanics-only (no vision, nothing invented), back-links to Blog 1, ends on the code link. Faithful + complete."
---
## PROMPT

You produce **Blog 2 of a framework chapter** — the **mechanical DEEP DIVE**: a faithful "how it actually works" technical article for an already-built AIOS, assembled from its impl docs. Blog 1 is the narrative; Blog 2 is the mechanics. You explain ONLY what the impl docs say the system IS — not vision, not guesses.

### Specifics (provided at dispatch)
- AIOS name: `{aios_name}`
- AIOS root: `{aios_root}`
- IMPL DOCS (read these FULLY — they are the mechanical truth doc-mirror maintains): `{impl_docs}`
  (typically: `SYSTEM.md`, `STATE_GRAPH.md`, the system spec, and any `docs/mirror/<…>.md` doc(m) files)
- Back-link to Blog 1 (the narrative opener this deep-dive belongs to): `{blog1_link}`
- Write the rendered Blog 2 markdown to: `{output_md_path}`

### STEP 1 — READ THE IMPL DOCS END TO END
The impl docs already separate the mechanical content for you (that is the whole point — you assemble, you don't reverse-engineer the code). Extract: the LAYERS (what it is, statically), the FLOW (the runtime cycle), the GEOMETRY (file tree / where things live), and the LIFECYCLE/STATE MACHINE (states + transitions). Pull the actual ASCII diagrams from `SYSTEM.md`/`STATE_GRAPH.md` verbatim — do not redraw them.

### STEP 2 — ASSEMBLE BLOG 2 (markdown) with this structure
- `# {aios_name} — How It Works (Deep Dive)`
- A one-line orientation + a link back to Blog 1: `> The story of why this exists: {blog1_link}`
- `## The architecture` — the layers/components (from the LAYER view; include the diagram).
- `## How it runs` — the runtime cycle (from the FLOW view; include the diagram).
- `## Where things live` — the file geometry (from the GEOMETRY view).
- `## The state machine` — states + transitions (from the LIFECYCLE view; include the diagram).
- `## The invariants` — the rules/closure-tests the system holds itself to (if the impl docs state them).
- Keep each section grounded in a specific impl doc; cite the doc/section you drew it from.

### STEP 3 — WRITE + REPORT
Write the markdown to `{output_md_path}`. Return as your final message: the full markdown + a per-section GROUNDED/INFERRED check (cite which impl doc each section came from; flag anything you could not ground). Prose roughness is acceptable — fidelity to the impl docs is what matters; do NOT polish voice, and do NOT invent mechanics the impl docs don't state.

### Hard constraints
- Mechanics ONLY from the impl docs (what IS). No vision, no invented features, no guessed internals.
- Reproduce diagrams verbatim from the impl docs; don't fabricate new ones.
- Touch ONLY `{output_md_path}`. Read nothing under `/home/GOD/core`.
