# Prompt-Skill Reliability Scoring — each prompt-skill is a science factory

A PROMPT-SKILL is a skill whose job is to dispatch a subagent against a prompt-file (per
`commander-not-hands-dispatch-everything`). Because a subagent's report is an unreliable claim
(`verify-agent-results-yourself-not-their-report`), every prompt-skill must carry an empirical
RELIABILITY record in its SKILL.md that is ADJUSTED each time it's run and checked. Opening such a
skill = opening the science factory for that skill's process: you see its track record, and you add
to it every run. This applies ONLY to prompt-skills (skills that command subagents); a plain
knowledge/understand skill needs no reliability block.

## The RELIABILITY block (required in every prompt-skill's SKILL.md)

```
## RELIABILITY
- score: <0.00–1.00>        # verified-good runs / total runs (your E2E checks, not agent reports)
- runs: <N>  verified-good: <M>  last-verified: <YYYY-MM-DD>
- check-level: FULL_E2E | SANITY    # FULL_E2E until proven; SANITY once score is high + stable
- log (newest first):
  - <YYYY-MM-DD> PASS|FAIL — <what you checked in the artifact, E2E> — <fix/prompt-tweak if FAIL>
```

## The protocol (every dispatch is a trial)
1. Dispatch the skill's prompt-file. Agent reports. **Its report does not adjust the score** — your
   CHECK does.
2. CHECK THE ARTIFACT yourself (FULL_E2E if `check-level: FULL_E2E`; a light SANITY check if the skill
   has earned `SANITY`). 
3. Record the trial: append a PASS/FAIL log line (what you actually checked), bump `runs`, bump
   `verified-good` iff PASS, recompute `score`, set `last-verified`.
4. On FAIL: the prompt was wrong → fix the prompt-file (that's the science — the experiment improved the
   apparatus), reset `check-level` to FULL_E2E, and note the tweak in the log. A FAIL is data, not waste.
5. **Graduation:** a skill moves to `check-level: SANITY` only after enough consecutive verified-good runs
   that you trust the prompt (heuristic: score ≥ 0.9 over ≥ 3 runs, no recent FAIL). Any SANITY failure →
   back to FULL_E2E. (This is the "previously-proven prompt-system" the verify-yourself rule trusts.)

## Why
The whole system is AI commanding AI; the only verifiable trust is a proven prompt + your own artifact
check. The reliability block makes "proven" EMPIRICAL and VISIBLE instead of vibes: a number earned by
checked runs, sitting in the skill, telling the next invocation how hard to verify. It also turns every
use into an experiment that improves the prompt — the skill becomes a self-calibrating science factory
for its process, not a static instruction. No prompt-skill is "trusted" by assertion; it is trusted by
its logged, checked track record.
