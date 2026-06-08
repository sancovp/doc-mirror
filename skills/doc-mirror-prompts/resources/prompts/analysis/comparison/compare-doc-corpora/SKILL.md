---
name: compare-doc-corpora
domain: analysis   subdomain: comparison
description: "WHAT: compare two documentation corpora and produce a structured gap/overlap analysis — what ideas in A are present/partial/absent in B, what B has that A lacks, where they agree vs diverge. WHEN: when you need to compare a reference/older corpus against a current one (e.g. an old design corpus vs our vision layer), find gaps, or reconcile two bodies of docs (any of)."
golden: false
score: 0.75   runs: 4   verified_good: 3
check_level: FULL_E2E   last_verified: 2026-05-30
log:
  - "2026-05-30 PASS — soma RE-RUN (cite-scoped, corpus-B = mirror∪vision): output 144 lines. Verified: REALIZED has_done_signal/has_verification in docs/mirror/soma_partials.pl.md; UCF-substance cites (hasInclusionMapArgument/BindingDriftCatastrophe) real in docs/mirror/uarl.owl.md while term 'UCF' greps 0 (correct nuance); assert_typed_value in vision still 0 (prior mis-cite did NOT recur); ABSENT (sovereignty/hyperon/vajrayana/worker-refiner) all grep 0. Cite-scope held both ways — the FAIL's fix is proven."
  - "2026-05-30 PASS — dragonbones RE-RUN (cite-scoped, corpus-B = mirror∪vision): output 127 lines. Verified: REALIZED `_flush_to_starlog_diary` is in docs/mirror/compiler.py.md (IMPL half ✓); STILL-ENVISIONED Operadic/PLANNED is in docs/vision (VISION half ✓); ABSENT claims (worker-refiner/sovereignty/vajrayana) grep 0 under docs ✓. CITE-SCOPE fix held — every cite landed in the correct half. (Score recovering after the soma FAIL.)"
  - "2026-05-30 FAIL — soma trial: cite-scope broke. Agent cited `assert_typed_value` + `flow-partials-core` to the VISION layer as its 'strongest agreement PRESENT', but those live in code/IMPL (soma_partials.pl, docs/mirror, .claude/rules) — grep of docs/vision = 0. Conflated IMPL/code with the compared (vision) layer → likely inverts that mapping into a vision GAP. (Independently-verified parts held: aideas_1 dedup true, Hyperon-disconnected verbatim, janus-safety + DOLCE grounded in vision.) FIX APPLIED: added CITE-SCOPE rule (every B-cite must grep under CORPUS_B_DIR; code/IMPL-only = ABSENT-in-B, not PRESENT). Re-run soma with hardened prompt."
  - "2026-05-30 PASS — dragonbones trial: output 230 lines; spot-checked 4 A-cites + 4 B-cites all exist; A 20_DSL_CLOSURE has 'closure' x7; 'DB=syntax+parser+telemetry only' divergence grounded in giint_types/compiler; constants.py.md chain-ladder (🛫Flight/🎯Mission/🌳Canopy/🎭Operadic, PLANNED) matches claim. Citations real both sides. (ran prompt + neighborhood-summary steer; step 0 added to prompt after.)"
---
## PROMPT

<background>
You compare TWO documentation corpora and produce a structured gap/overlap analysis. `CORPUS_A` is the
REFERENCE (here: an older design/research corpus). `CORPUS_B` is our CURRENT layer (here: `docs/vision/<m>.md`
= ideas/decisions/envisioned-not-built for a codebase). Goal: which ideas in A are captured / partial /
absent in B, what B has that A lacks, and where they agree vs diverge/contradict.
</background>

<inputs>
- `SYSTEM` = {the system being compared, e.g. soma | dragonbones}
- `CORPUS_A_DIR` = {path to the reference corpus}
- `CORPUS_B_DIR` = {path to our current/vision layer}
- `OUTPUT_FILE` = {path to write the comparison artifact}
</inputs>

<procedure>
0. FIRST check each corpus for a PRE-BUILT map — a `summaries/`, `neighborhood*`, `index`, `_MANIFEST`, `00_MASTER_SUMMARY`, or `OVERVIEW` layer. If present, THAT is the topic map: read it first, use it as the backbone, and only drill into raw files for specific citations. Don't re-derive a map that already exists.
1. Build CORPUS_A's TOPIC MAP (from its summaries layer if present, else every `.md`, recurse): each major idea/theme → 1-line gloss + `(fileA:section)`.
2. Build CORPUS_B's TOPIC MAP likewise.
3. For each major idea in A, classify against B: `PRESENT` (cite B file) | `PARTIAL` (cite + what's missing) | `ABSENT`.
4. List ideas in B NOT in A (new / diverged since A).
5. Flag `AGREE` vs `DIVERGE/CONTRADICT` pairs — cite BOTH sides.
6. Write `OUTPUT_FILE` (format below). Cite BOTH sides for every mapping (`fileA:section ↔ fileB:section`).
</procedure>

<honesty>
- Cite both sides for every mapping; quote a short snippet as evidence.
- **CITE-SCOPE (critical): every B-cite MUST be a string actually greppable in a file UNDER `CORPUS_B_DIR`.
  `grep` it before you write it. NEVER cite code, IMPL/mirror docs, rules, or any other layer as if it
  were in B.** If an A-idea is realized in code/IMPL but is NOT in the B layer, that is `ABSENT` (in B),
  noted as "realized in code/IMPL, NOT in {B layer}" — that is a FINDING (graduated or undocumented),
  NOT `PRESENT`. Same rule for A-cites: greppable under `CORPUS_A_DIR` or don't cite it.
- If a mapping is unsure, mark `UNCERTAIN` — do NOT force it.
- Never invent content in either corpus. If you didn't finish reading something, say so.
- Counts must be real command output (`find … | wc -l`), not estimates.
</honesty>

<output_format>
Write `OUTPUT_FILE` as markdown:
`# {SYSTEM}: {CORPUS_A} ↔ {CORPUS_B}`
`## A topic map` — `[idea — gloss — (fileA)]`
`## B topic map` — `[idea — gloss — (fileB)]`
`## Classification` — table `[idea | PRESENT|PARTIAL|ABSENT | A-cite | B-cite | note]`
`## Gaps: in A, not in B` — candidate vision(m) additions, each with `(fileA:section)` + 1-line why-it-matters
`## In B, not in A` — new since A
`## Agree vs Diverge` — table `[pair | A-says | B-says | verdict]`
`## Confidence + what wasn't fully read`
Then RETURN a short summary: counts (present/partial/absent), top 5 gaps, top divergences, confidence.
</output_format>
