---
name: deepdive-blog-from-impl-docs
domain: skill2framework   subdomain: deep-dive
description: "WHAT: produces Blog 2 of a framework CHAPTER — the mechanical DEEP-DIVE technical article ('how it actually works') — for an already-built AIOS by reading its impl docs (doc(m) + SYSTEM.md + STATE_GRAPH) and assembling a faithful how-it-works explanation that links back to Blog 1. It explains mechanics ONLY from what the impl docs say IS (not vision, not invented). WHEN: when producing the deep-dive half of a framework chapter, when you need the technical how-it-works post that Blog 1 links to, or when the user mentions blog 2 / the deep dive / skill2framework (any of)."
golden: false
score: 0.50   runs: 2   verified_good: 1
check_level: FULL_E2E   last_verified: 2026-07-11
log:
  - "2026-07-11 HARDENED after the composed-run USER GATE REJECTION: the
    cave-unicorn blog2 this prompt produced read as an INTERNAL REFERENCE DUMP
    and LEAKED container-internal absolute paths (/home/..., HEAVEN_DATA_DIR)
    onto the public site — the 'Where things live' file-geometry section
    published the container's layout by design. NOW IN THE PROMPT: the
    PUBLIC-SITE REDACTION LAW (no container-internal paths/env/host internals,
    including inside verbatim diagrams — substitute repo-relative tokens and
    note it), reader-facing framework framing (the deep dive explains how the
    FRAMEWORK works when the READER runs it; the module is the reference
    implementation), and geometry restricted to the PUBLIC repo's relative
    layout. Score drops to 0.50 (2 runs, 1 verified-good). Re-scores on the
    next user-gated run."
  - "2026-06-03 PASS — dogfood on doc-mirror. Subagent read SYSTEM.md + STATE_GRAPH.md + DOC_MIRROR_SYSTEM.md (no docs/mirror/ exists for doc-mirror-system itself — it's a meta-repo, honestly noted) and assembled Blog 2 at /home/GOD/tmp/framework_recon/doc-mirror_blog2.md. I verified E2E myself: all 5 diagrams reproduced VERBATIM (LAYER/FLOW/GEOMETRY/spine-mermaid/LIFECYCLE) + the cursor-fields block + transition-hook pseudocode + legal-transitions table, every section cited to a specific impl doc, mechanics-only (no vision, nothing invented), back-links to Blog 1, ends on the code link. Faithful + complete."
---
## PROMPT

You produce **Blog 2 of a framework** — the **GLOBAL-FIT post** (Isaac
2026-07-12: "more globally this fits in the system like..."): where this
framework sits in the WHOLE system, what it connects to, what flows through
it, and what having it unlocks. Blog 1 (the fixpoint post) is the framework's
own journey; Blog 2 zooms OUT — the map with this framework located on it.
You explain ONLY what the impl docs and system docs say IS — not vision, not
guesses. Mechanics appear in service of the fit ("this is the layer that X
hands off to Y through"), never as an internal reference dump.

READER-FACING FRAMING: the reader has read the fixpoint post and is asking
"where does this live in the bigger machine, and what else is there?" — every
section serves that. The module/repo is the reference implementation, never
the subject. The BELIEF LAW applies here too (Isaac, verbatim): every sentence
installs a belief the argument needs or destroys a limiting belief blocking
it; the global map itself installs the biggest one — that a whole coherent
system exists and this piece is one mastered part of it.

THE PUBLIC-SITE REDACTION LAW: this article publishes to a PUBLIC website.
NEVER include container-internal absolute paths (/home/..., /tmp/...),
internal env var names-as-config (HEAVEN_DATA_DIR etc.), hostnames, ports, or
secret/credential names. Name things logically: module names, PUBLIC
repo-relative paths, public URLs. This law applies INSIDE verbatim diagrams
too — if an impl-doc diagram carries a container-internal path, substitute the
repo-relative token and add a one-line note that paths were generalized.

### Specifics (provided at dispatch)
- AIOS name: `{aios_name}`
- AIOS root: `{aios_root}`
- IMPL DOCS (read these FULLY — they are the mechanical truth doc-mirror maintains): `{impl_docs}`
  (typically: `SYSTEM.md`, `STATE_GRAPH.md`, the system spec, and any `docs/mirror/<…>.md` doc(m) files)
- Back-link to Blog 1 (the narrative opener this deep-dive belongs to): `{blog1_link}`
- Write the rendered Blog 2 markdown to: `{output_md_path}`

### STEP 1 — READ THE DOCS END TO END
Read the impl docs AND any provided system-map docs fully. Extract: what this framework IS (one line), the LAYER it sits at in the whole system, what sits ABOVE and BELOW it (what hands work to it, what it hands work to), the FLOW that passes through it end to end, and what having it UNLOCKS elsewhere in the system. Keep any diagram you reproduce verbatim (generalizing container paths per the redaction law).

### STEP 2 — ASSEMBLE BLOG 2 (markdown) with this structure
- `# {aios_name} — Where It Fits`
- A one-line orientation + a REAL markdown link back to Blog 1: `> The journey of this framework: [the story]({blog1_link})`
- `## The system it lives in` — the whole in one view: name the layers/organs of the larger system plainly, locate THIS framework on that map (include the diagram if the docs carry one).
- `## What flows through it` — the end-to-end flow that passes through this framework: what arrives, from where; what leaves, to where. Mechanics in service of the fit, never a reference dump.
- `## What it unlocks` — what the rest of the system can do BECAUSE this piece exists; what was impossible before it.
- `## Run it inside your own system` — public-repo-only: pip install, the CLI verbs, where it plugs in. Instructions-shaped; every link a real markdown anchor `[label](url)` (bare URLs render as dead text on the site).
- Keep each section grounded in a specific doc; cite the doc/section you drew it from.

### STEP 3 — WRITE + REPORT
Write the markdown to `{output_md_path}`. Return as your final message: the full markdown + a per-section GROUNDED/INFERRED check (cite which impl doc each section came from; flag anything you could not ground) + THE REDACTION CHECK: one line confirming ZERO container-internal absolute paths / env internals anywhere in the markdown, including inside diagrams (state any substitutions you made). Prose roughness is acceptable — fidelity to the impl docs is what matters; do NOT polish voice, and do NOT invent mechanics the impl docs don't state.

### Hard constraints
- Mechanics ONLY from the impl docs (what IS). No vision, no invented features, no guessed internals.
- Reproduce diagrams verbatim from the impl docs (generalizing container paths per the redaction law); don't fabricate new ones.
- WRITE EARLY: after reading the impl docs, write `{output_md_path}` BEFORE composing your report — never spend the whole tool budget reading and die announcing "let me write".
- Touch ONLY `{output_md_path}`. Read nothing under `/home/GOD/core`.

NEVER CALL A BLOCK-REPORT / HALT TOOL AS A STATUS REPORT. If your loadout
carries WriteBlockReportTool (or any blocked/halt tool): calling it HALTS the
run permanently — it is NOT a progress note. "No blocker — all impl docs read,
ready to write" is NEVER a block report (a run died EXACTLY this way): when
you are ready to write, the next action is WRITING `{output_md_path}` with
your Bash tool. Use the block tool ONLY when a real external blocker makes
every remaining step impossible (a listed impl doc missing from disk).
