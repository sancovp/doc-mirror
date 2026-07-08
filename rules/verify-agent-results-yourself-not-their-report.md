# Verify Agent Results Yourself — Their Report Is a Claim, Not Proof — VITAL NON-NEGOTIABLE

When you dispatch an agent, its result report is just a CLAIM — same status as your own "done" claims,
which are unreliable. A report saying "all green, verified, 4/4 passed" is NOT verification. You verify by
CHECKING THE ARTIFACT YOURSELF — reading the file it wrote, running the test, diffing the output, hitting
the surface. Never accept an agent's word for whether the work is right.

## The level of checking depends on whether the prompt is REIFIED into a proven skill

- **Unproven prompt (first runs / ad-hoc dispatch):** CHECK EVERYTHING, E2E. The prompt itself is not yet
  trusted, so you cannot trust any of what the agent claims it produced. Read the actual artifacts, run the
  actual verification, confirm each claim against the real thing. This is also how you find out whether the
  prompt is good enough to become a skill.
- **Reified prompt (a SKILL whose prompt-file you've already run and verified to do EXACTLY the thing):**
  a SIMPLE sanity check is enough — confirm the expected output exists / the headline result holds — rather
  than re-checking every detail E2E. The skill earned that trust by being verified when it was built; the
  dispatch is now routine. (If the simple check fails, drop back to full E2E — the skill may have drifted.)

## Why — the unreliability is RECURSIVE; trust attaches to the PROMPT, not the agent
A subagent cannot observe itself, exactly like you cannot observe yourself. So a subagent's report is
STRUCTURALLY the same unreliable claim as your own "done" — no matter how confident or detailed it is.
You dispatch agents to get an observable SURFACE — but the report is not that surface; the ARTIFACT is.
Believing the report re-introduces the exact unverifiability you dispatched to escape: a confident
"verified ✅" that was never true, built on, days lost.

The ONLY thing that earns trust without you re-checking every detail is a **previously-proven prompt
system** — a reified skill whose prompt-file you ALREADY verified, once, to produce exactly the artifact.
Trust lives in the proven PROMPT, never in the agent that ran it (the agent is just as unable to self-verify
as any other). So: proven prompt-system → light sanity check of the artifact is enough. Anything else
(ad-hoc dispatch, unproven prompt, or "the agent seemed sure") → the agent's word is worth nothing; check
the artifact E2E yourself. The artifact is the only truth.

## How to apply
1. Agent returns a report → treat every claim in it as UNCONFIRMED.
2. Is this dispatch a reified, previously-verified skill? → light sanity check of the headline artifact.
   Otherwise → full E2E: open the files, run the tests/surface, diff against what was asked.
3. Only after YOUR check passes do you treat the work as done. The report's "done" never counts on its own.
4. A prompt only EARNS skill-status (and the lighter check) after you have verified its output E2E at least
   once and it did exactly what was needed. Until then, every run gets full verification.
