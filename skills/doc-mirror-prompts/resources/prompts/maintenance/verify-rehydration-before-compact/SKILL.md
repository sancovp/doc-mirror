---
name: verify-rehydration-before-compact
domain: maintenance   subdomain: continuity
description: "WHAT: the EMPIRICAL continuity test — before compacting (or AFK/handoff), dispatch a fresh subagent to REHYDRATE a target from the durable layer ALONE (journal + the files it points to, no other context) and report what it reconstructed; you compare that to what it ACTUALLY needs to know, and patch every gap into the journal as a lossless pointer BEFORE you compact. Also states the storage discipline the test enforces: a stored note is a lossless POINTER to its exact source, never a lossy summary. WHEN: right before any self_compact / planned compaction / AFK / session handoff; or whenever you need to prove the durable layer is continuable; or when you catch yourself about to store a digested summary instead of a retrieval pathway (any of)."
golden: false
score: 1.00   runs: 1   verified_good: 1
check_level: FULL_E2E   last_verified: 2026-06-02
log:
  - 2026-06-02 PASS — pre-compact run. Fresh subagent reconstructed BOTH the read-layer design AND the ingestion incident from the durable layer (journal+cursor+vision+task-backup) ALONE, accurately. The real gap (429-deployed was buried in a -t COMMIT entry that doesn't project to vision) + verify-forward (empirically confirmed: +226 new Iteration_Summary, max ts 2026-06-02T19:57) were patched into the journal; the rest were test-setup (files not named) or correctly-open items. Durable layer proven continuable.
---
## THE STORAGE DISCIPLINE THIS TEST ENFORCES (why it exists)

A stored note carries TWO things and needs BOTH: (1) an **accurate idea-summary** — the *correct idea*
of what is stored, so you (or any reader, including the human) know WHAT it is and whether to descend,
WITHOUT loading it; and (2) a **lossless pointer to its exact source** — the search query you ran, the
`file:line`, the journal entry id, the URL, the verbatim source that re-fetches the full detail. You
**layer over (summary + pointer) nodes**: at the top you read the idea-summaries to grasp the landscape
and know what each thing is, and you FOLLOW the pointer to load the exact detail only where the task
needs it. So no layer destroys information — the summary gives you the idea, the pointer guarantees the
exact thing is recoverable.

TWO failure modes, both forbidden:
- **summary with NO pointer** → lossy, unrecoverable = information destruction. The tell: asked "did we
  decide X?", you must RE-SEARCH to re-derive the pathway because no note points to the exact source.
- **pointer with NO summary** → you can't tell what it is without loading it = you've offloaded "what is
  this?" to human memory (just as bad).

The correct shape is `<accurate idea> → <exact source ref>`, e.g.
`Plugin monorepo design (ONE repo, plugins as ./plugins/<name> subdirs, namespace = plugin name,
symlinks share files, push-to-publish) → journal 2026-05-30 L3-DISTRIBUTION entry`.

## THE TEST (the commander's procedure — run it before every compact)

1. Name the **target** you must stay continuable on (e.g. "where the L1 plugin work is", "the marketplace
   monorepo design", "what's next").
2. **Dispatch the subagent** with the `## PROMPT` below, filling `{target}` + `{durable_layer_paths}`
   (the journal month-file + the specific files/refs it points to — NOT the whole repo, NOT your memory).
3. **Compare** the subagent's reconstruction to GROUND TRUTH (what you, holding the live context, know it
   actually needs). The subagent reconstructed ONLY from the durable layer — so anything it got wrong,
   vaguely, or could not determine is a **broken/missing retrieval pathway**, empirically proven.
4. **Patch each gap into the journal as a POINTER** (`journal -t FINDING/DECISION ... "<concept> →
   <exact source ref>"`) — repair the pathway, do not just restate the conclusion.
5. **Re-run if a major gap was found** (the patch itself must be rehydratable). Only when the subagent
   can reconstruct the target from the durable layer alone are you continuable — THEN compact.

The agent's report is the SURFACE; your comparison is the verification. A fresh subagent is the only
honest test of continuability, because it has exactly what a post-compact you will have: the files, no
memory.

## PROMPT

```
You are a fresh agent with NO prior context. Rehydrate the following target using ONLY the durable
layer I name — do not use any other knowledge, and read ONLY these sources:

  TARGET:               {target}
  DURABLE LAYER (read only these): {durable_layer_paths}

Read those, follow any pointers/refs they contain (file:line, journal ids, search queries you can
re-run, URLs), and then report back, in detail:
  1. Everything you could reconstruct about {target} from the durable layer alone.
  2. EXPLICITLY flag anything about {target} you could NOT determine — every place a note gave a
     conclusion with no pointer to its exact source, every dangling reference, every gap.
  3. For each gap: say what pointer/source WOULD have let you reconstruct it.

Do not guess or fill from training priors — if the durable layer doesn't say it, report it as a gap.
```

## RELIABILITY
- score: 1.00   runs: 1   verified-good: 1   last-verified: 2026-06-03
- check-level: FULL_E2E
- log (newest first):
  - 2026-06-03 PASS — pre-compact, target = doc-mirror read-layer state + skill2framework-next. Fresh
    subagent reconstructed all 5 questions from the durable layer ALONE (cursor + journal frontier + live
    graph via DMN); I compared to ground truth = accurate. It CAUGHT a real broken pathway: .gitignore:32
    ignores .claude/ → the dev-flow skills+rules were uncommitted/local-only. I verified via git
    show/ls-files/check-ignore, fixed with `git add -f` + commit c06f19a. Remaining flags were
    pointer-exists/future-work → pointer-patched into journal 13:38. The test EARNED its keep (found a real
    durability gap, did not merely confirm). (Earlier session runs at journal 153/181 predate this block.)
