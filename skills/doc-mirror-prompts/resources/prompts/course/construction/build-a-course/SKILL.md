---
name: build-a-course
domain: course   subdomain: construction
description: "WHAT: builds a complete teach-while-showing-your-system COURSE — the kind that teaches a generic skill for free and sells your advanced system through the GAP, by walking primitives beginner->advanced, showing your system do each one 'right and forever', with the funnel woven in (lead magnets throughout, ONE hard CTA at the capstone, upsells after). It is a SKILLCHAIN: derive the module spine, then LOOP construct-a-module -> roll-up-the-whole-course until closure. WHEN: when the user wants to build/author a course or curriculum, reverse-engineer a course, turn a system/harness into a sellable course, make a 'learn X while I show you my Y' course, or mentions course-builder / universal course template / course construction (any of)."
golden: false
score: 0.00   runs: 0   verified_good: 0
check_level: FULL_E2E   last_verified: ""
log: []
---
## PROMPT

You build a complete **teach-while-showing-your-system course**. This is a SKILLCHAIN, not a one-shot:
you DERIVE a module spine, then LOOP `construct-module -> roll-up-the-whole-course` once per module, and
the roll-up is the GATE that must pass before the next module. You cannot generate a coherent multi-module
course in one shot — you climb it module-by-module, re-grounding the whole at each step.

### The three reference docs (READ ALL THREE FIRST — they are in this skill's `resources/`)
- `resources/universal-course-template.md` — the SHAPE: the invariant module structure (interleaved
  CONCEPT + BUILD modules, the special modules, the two beat patterns, the woven funnel, the threaded
  theses) and the full `{variable}` list. This is the spec each constructed module must satisfy.
- `resources/course-construction-loop.md` — the PROCEDURE you run: STEP 0 derive spine -> STEP 1 init the
  rollup -> STEP 2 LOOP[construct module, then roll up the whole course] -> STEP 3 closure. Follow it exactly.
- `resources/claude-code-course-pattern.md` — a WORKED INSTANCE (the variables bound to a Claude-Code
  primitives course, `{system}` = a harness shown at every beat). Use it as the model for how to bind
  the variables when the course teaches Claude Code.

### Specifics (provided at dispatch — bind every variable; NONE are hard-coded)
- `{transformation}` / `{proof}` — where the learner ends up + honestly-marked outcomes.
- `{core_thesis}` + `{supporting_theses[]}` — the ideas repeated in every module's benefit beat.
- `{primitives[]}` — the skills/concepts to teach, in beginner->advanced (complexity-ladder) order = the spine.
- `{system}` — the advanced implementation shown at EVERY concept beat (the product being sold by the gap).
- `{builds[]}` — the live build demos to interleave.
- `{highest_leverage_system}` · `{capstone_build}` · `{climax_differentiator}` — the special-position modules.
- `{lead_magnets[]}` · `{hard_CTA}` · `{upsells[]}` — the funnel beats.
- `{host_systems}` — (IF PROVIDED) the existing MARKETING + FUNNEL + STORY structures to write the module
  content INTO. If given, every module's funnel/story beat must land inside these structures, not invent new ones.
- `{output_dir}` — where the running COURSE DOC + per-module files are written.

### RUN THE CHAIN (this is the EvalChain — each module's roll-up is the per-module OK-stable-signal gate)
1. **STEP 0 — derive the SPINE** from the variables (one CONCEPT module per `{primitive}` in ladder order;
   interleave `{builds[]}`; place THESIS early, HIGHEST-LEVERAGE mid-late, CAPSTONE + CLIMAX late). Output
   the spine as titled one-line modules (KIND, which primitive/build, which `{system}` artifact shown).
2. **STEP 1 — initialize the rollup**: create the running COURSE DOC in `{output_dir}` (hook/promise,
   `{core_thesis}`, the spine, the funnel-beat map, the "course-shape-in-one-paragraph").
3. **STEP 2 — THE LOOP, once per module M in spine order:**
   - **a. CONSTRUCT M fully** — apply its beat pattern (CONCEPT: primitive -> plain analogy -> "but in
     {system} I do it like THIS" (a real artifact) -> the forever-benefit ({core_thesis}) -> funnel nudge;
     BUILD: docs/goal -> plain architecture -> diagram -> grill the plan -> anneal vs ground truth -> ship).
     Author REAL content grounded in the real `{system}` artifact, not a stub. If `{host_systems}` given,
     write the funnel/story beat into them.
   - **b. ROLL UP (the GATE)** — integrate M into the COURSE DOC; re-check coherence (does M build on every
     prior module? does beginner->advanced still hold? does `{core_thesis}` thread M's benefit? forward-refs
     to fix?); update the funnel-beat map (hard CTA still ONLY at the capstone?); re-derive the
     "course-shape-in-one-paragraph". **If the rollup reveals incoherence, FIX the spine / prior modules
     BEFORE continuing — do not advance on an incoherent rollup.**
   - **c. Continue to M+1** built on the coherent whole.
4. **STEP 3 — CLOSURE**: every module constructed AND integrated; the rollup reads as ONE coherent
   beginner->advanced arc; `{core_thesis}` threads every benefit beat; funnel beats placed (magnets
   throughout, ONE hard CTA at capstone, upsells after); the CLIMAX lands as "the most important thing".

### REPORT (final message)
Return: the final spine, the path to the finished COURSE DOC, the per-module file list, the funnel-beat map,
and the one-paragraph course shape. Flag any module where the rollup forced a spine/prior-module fix (that
is the chain working, not a failure). Confirm closure criteria met or name exactly what is missing.

### Hard constraints
- NO specifics baked in — every particular is a bound variable (per `prompts-contain-no-specifics`).
- The roll-up is non-optional and is the gate; authoring all modules then stapling them is the failure mode.
- You never PITCH; the gap between "how you'd do it" and "how {system} does it forever" is the entire sale.
- Ground every "how I do it" beat in a REAL `{system}` artifact you can cite — not a described one.
