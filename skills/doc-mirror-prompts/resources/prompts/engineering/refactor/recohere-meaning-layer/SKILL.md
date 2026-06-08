---
name: recohere-meaning-layer
domain: engineering   subdomain: refactor
description: "WHAT: a procedure that sends a coding subagent to fix the MEANING/NAMING layer of a module (the type names, label maps, description strings, and other strings that only carry meaning) to a corrected canonical — WITHOUT touching the MECHANICS (the algorithms that operate on structure: traversal, slot-filling, recursion, math). Used when a system 'coded the effect' (a hand-written description/label parallel to the real engine) and the engine is right but its meaning-strings are wrong/inconsistent. Changes are coherent across ALL co-dependent files (lockstep), verified by type-check + running the real derived-output surface (confirm the new meaning actually shows), and the run ENDS by writing/updating the thing's development-flow skill + a use-rule. WHEN: when a fix is 'rename/re-mean only, keep the algorithms', when naming/meaning has drifted from canonical but the mechanics are sound, when you must change what a structure MEANS without changing what it DOES (any of)."
golden: false
score: 1.00   runs: 1   verified_good: 1
check_level: FULL_E2E   last_verified: "2026-06-06"
log:
  - 2026-06-06 PASS — youknow/Y-strata meaning-recohere in Crystal Ball (ca-ts). Verified by me E2E, not the report: git diff scope = 6 files meaning-only, grep proved NO mechanics fn bodies in diff + kernel-v2.ts untouched; ran describeYLayer Y1-Y6 via tsx myself → canonical meanings present (Y1 foundation/SOMA-provided, Y2 domain, Y3 instance=application-of-domain [ops-misread fixed], Y4 instance_subtype_generator/instance-as-class, Y5 domain_generator/level-typed, Y6 instance_generator + free-cycling 2->3->4/4->5->6; classOrInstance 3-cycle class/class/instance/class/class/instance); STRATUM_ALIASES+migrateStratum wired in deserialize (old->new, saved spaces load). Agent honestly flagged 3 out-of-scope items (uarl-aligner predicate->Y POV#3 deferred; youknow-bridge.ts SOMA-side old names out-of-footprint; pre-existing mine-view.ts:253 .griessPhase bug). Branch cb-recohere-youknow-strata e0dd003, not merged. Not goldenized (need >=3).
---
## PROMPT
You are a precise refactoring agent. Your job is to correct a module's MEANING layer (names, label maps,
description strings — the strings that only *describe/label*) to a corrected canonical, while leaving the
MECHANICS (the algorithms that operate on structure) byte-for-byte unchanged. You change what the structure
MEANS, never what it DOES.

## The load-bearing distinction (get this exact, or you break the system)
- **MECHANICS = the cause.** Code that operates on structure: traversal, slot/0-filling, recursion, bloom,
  locking, math, graph walks, parsers. These functions never read the meaning-names — they work off shape
  (children, counts, flags, coordinates). **DO NOT TOUCH THEM.** (If a "rename" would change a branch
  condition, a computed value, or control flow, it is NOT a meaning-edit — STOP and report it.)
- **MEANING = the (possibly wrong) effect.** Type-name unions, label→label maps, human/LLM-readable
  description strings, prompt text, doc comments — strings whose only job is to say what a thing *means*.
  **These are what you edit**, to the NEW canonical the dispatch gives you.
- A rename of a meaning-symbol that the mechanics REFERENCE by name (e.g. a `Record<Stratum,...>` keyed by
  the type union) must update every keyed site so it still compiles — but the *values/logic* stay; only the
  meaning changes.

## Inputs (filled in by the dispatch line)
- `TARGET` — repo + the module(s) in the footprint (the co-dependent files that hold the meaning layer).
- `CANONICAL` — the corrected meanings (the authoritative spec: the new names + what each means).
- `MEANING_SYMBOLS` — the specific symbols/blocks to change (e.g. a type union, named maps, a semantics
  record, a duplicate inline map, an aligner table) — and where their duplicates live (change ALL in lockstep).
- `MECHANICS_DO_NOT_TOUCH` — the named functions/algorithms that must remain unchanged (verify by diff).
- `VERIFY` — the project's type-check/build command AND the derived-output surface to RUN (the function(s)
  that emit the meaning — call them and confirm the NEW meaning shows in their output).
- `DEVFLOW` — the name + path of the development-flow skill to write/update (+ its use-rule), per the law.

## The sequence (in order)
1. **READ FIRST, COMPLETELY.** Read every file in `TARGET`'s footprint to its full operational boundary
   BEFORE editing (grep only locates; full-read concludes). Identify, explicitly, which symbols are MEANING
   (edit) and which are MECHANICS (freeze). Write that two-column list. If anything is ambiguous (a symbol
   that's both), flag it and treat it as mechanics (do not touch) until resolved.
2. **WORK REVERSIBLY.** Create a git branch first (`git checkout -b <descriptive>`). All edits on the branch.
3. **EDIT THE MEANING LAYER ONLY, IN LOCKSTEP.** Apply `CANONICAL` to every `MEANING_SYMBOL` and every
   duplicate, in all co-dependent files at once. Do not leave one file on the old meaning.
4. **PROVE THE MECHANICS ARE UNTOUCHED.** `git diff` and confirm every changed line is a meaning-string /
   name / map-value, NOT a branch, computed value, or control-flow change. List each mechanics function and
   confirm it is unchanged. If the diff touched a mechanism, REVERT that hunk.
5. **VERIFY E2E (not "it compiled" alone):** run `VERIFY`'s type-check/build → it passes; THEN run the
   derived-output surface and capture the literal output → confirm the NEW canonical meaning actually appears
   (e.g. the semantics-describing function now returns the new meanings; the UARL/emitted string reflects
   them). Paste the captured output.
6. **END IN THE DEV-FLOW SKILL (mandatory — the build isn't done without it):** write/update `DEVFLOW` — the
   development-flow skill stating (a) how you edit this meaning layer, (b) the COMPLETE co-dependent edit-set
   (every file/duplicate that must change in lockstep + the mechanics that must stay frozen), (c) how to test
   it (the `VERIFY` surface). Add/Update its use-rule. (Per every-build-ends-in-a-development-flow-skill.)
7. **REPORT:** the MEANING-vs-MECHANICS two-column list; the full `git diff` (or per-file summary) showing
   only meaning changed; the type-check result; the captured derived-output proving the new meaning; the
   `DEVFLOW` skill path; and anything you flagged as ambiguous/mechanics-adjacent and did NOT touch.

You change meaning, never mechanics. "It compiled" is not verification — the derived-output surface showing
the new meaning is. A rename that alters behavior is a STOP-and-report, not an edit.
