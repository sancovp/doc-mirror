# Trace Bug Chain To Exact Symptom

This is universal bug-investigation methodology. It applies to every domain: application code, configuration, network behavior, race conditions, UI rendering, build pipelines, hardware faults, database state, infrastructure. The discipline is identical regardless of the kind of system you are debugging.

## The principle

A bug is not found until you can trace forward from the wrong code (or wrong configuration, wrong state, wrong assumption — whatever the root cause is) step by mechanical step to the EXACT observable symptom, with no "and presumably" or "this would somehow cause" between any two steps. Every arrow in the chain must be a deterministic consequence you can point at: a specific file:line, an observable variable state, a measurable system event, a documented protocol behavior. Not an adjacency, not an intuition, not a plausible-sounding inference.

If your chain ends at "and so something goes wrong," you have A problem, not THE problem. Keep tracing.

## The closure test is empirical

Re-running the chain mentally should reproduce the observed effect EXACTLY, not a generic version of it.

- If the symptom is "a returned value is 7 when it should be 3," the chain must produce 7 — not just "the wrong number."
- If the symptom is "the page renders correctly in Chrome but not Firefox," the chain must produce that Firefox-specific output — not just "the page breaks."
- If the symptom is "every nth request fails with a particular error code," the chain must produce both the periodicity n and the specific error code — not just "occasional failures."
- If the symptom is "a stored value grew to a specific size with a specific repeating block structure," the chain must produce that size and that structure — not just "the value got large."

The exact shape of the symptom is the proof you have the full chain. If your chain only produces a generic version, you are missing a link.

## Why partial fixes leave the symptom alive

Many production bugs are downstream of multiple wrong things compounding. Finding ONE wrong thing and prescribing a fix can leave the symptom intact because the remaining wrong things still produce most of the bad behavior.

The shape of the observed symptom is the proof of how many wrong things are involved. If you fix one and the symptom changes shape but persists, the chain has links you have not yet identified. Do not declare the bug fixed until the symptom is gone in the exact shape that was reported.

## Template for any bug

For any bug, before prescribing a fix, write this down explicitly:

```
Observable symptom: <exact, measurable, reproducible — values, bytes, byte counts,
                    timing, sequences, structure. Not a paraphrase.>

Plausible-but-incomplete hypothesis: <the first thing that looks suspect — write it
                                       down so you do not get anchored to it>

Chain:
  step 1: <initial state, input, or trigger>
  step 2: <line X does Y, produces Z>          ← file:path:line, deterministic
  step 3: <line A reads Z, does B, produces C> ← file:path:line, deterministic
  ...
  step N: <produces the EXACT observable symptom from step 0>

Why each link is required: <removing any single fix from the chain must leave the
                            exact symptom alive. If removing a fix only changes the
                            symptom's magnitude or frequency, that fix was only
                            partial.>
```

If you cannot fill in this template all the way to the exact symptom, you have not found the bug. Keep reading code, keep running experiments, keep gathering observations.

## The discipline

- Describe before prescribe. Stay in description until the chain closes.
- Citing principles or architectural intuitions instead of specific code/state references is the tell that you are in autocomplete mode, not investigation mode.
- A fix-shaped sentence with no traceable causal chain to the EXACT observed symptom is autocomplete, not a fix.
- When you think you have found the bug, write the chain out explicitly. If your chain reproduces a vague version of the symptom but not its exact shape, you have not found it.
- Prescription only after the chain closes at the exact symptom.
