---
name: doc-mirror-change
description: "WHAT: change ONE module -- read its full boundary, make the change, re-derive its doc(m), doc-mirror-commit with an ORIGIN, run closure, graduate the realized vision(m) -> doc(m). WHEN: a specific module changed or has code/doc to write -- after seework picks a code gap, or after a prompt produced an artifact to verify and commit."
---

# doc-mirror-change — the CHANGE state (re-derive doc(m), commit, graduate vision→impl)

You are in the **change** state. A module changed (or you are about to change one). This state makes the
change correctly and keeps the mirror honest. It operates under **THE LAW** (the `doc-mirror` skill — the
doc(m) template, deterministic addressing, the closure test, and FORK-ON-CHANGE). Read THE LAW's doc(m)
template and fork-on-change section if you don't have them in context.

## The subgraph (this state's shape)

```mermaid
stateDiagram-v2
    [*] --> S_boundary: R — read the ENTIRE module + its doc(m) + every caller in the chain (no guessing)
    S_boundary --> MODE
    state MODE <<choice>>
    MODE --> T_prompt:  [USING-mode on a target repo: you are commander -> cursor=prompt ; call doc-mirror-prompts]
    MODE --> S_edit:    [BUILDING the system itself, WITH Isaac: author directly]
    S_edit --> S_rederive: re-derive doc(m) at docs/mirror/<relpath>.md (what the code now IS)
    S_rederive --> S_commit: doc-mirror-commit <m> "<what>" "<why>" "<ORIGIN: vision it realizes / bug it fixes>"
    S_commit --> CHECK
    state CHECK <<choice>>
    CHECK --> S_graduate: [closure passes: doc(m)<->module biject; ORIGIN cited]
    CHECK --> S_gap:      [commit REFUSED: doc not re-derived, or no ORIGIN]
    S_gap --> S_rederive
    S_graduate --> [*]: the realized idea GRADUATES vision(m) -> doc(m); journal; advance cursor -> seework
```

## What this state is

1. **S_boundary — get the complete operational boundary in ONE read.** Read the ENTIRE module + its
   current doc(m) + every caller in the dependency chain. No guessing, no progressive edits while
   gathering context (rules: `complete-operational-boundary-before-edit`, `read-entire-file-before-any-change`).

2. **MODE — who makes the change.**
   - **USING-mode** (doing development on a target repo, the loop running): you are the COMMANDER, not
     the hands. Transition to `doc-mirror-prompts` to dispatch an agent against a prompt-file, then VERIFY
     the artifact yourself (the report is a claim, not proof). You return here to re-derive + commit.
   - **BUILDING-the-system-WITH-Isaac mode** (authoring the steering layer / the system itself, with
     Isaac): author directly. This is the explicit exception to commander-not-hands.

3. **S_rederive — re-derive doc(m)** at `docs/mirror/<relpath>.md` = what the code NOW IS (bump
   `**Last derived:**`). A fix is a re-derivation of the doc(m), NEVER a standalone fix/investigation doc.

4. **S_commit — `doc-mirror-commit <m> "<what>" "<why>" "<ORIGIN>"`.** The helper stages `m` +
   `docs/mirror/<m>.md`, rolls up your journal lines since the last commit into the body, and REFUSES a
   code change whose doc wasn't re-derived OR that cites no ORIGIN (a vision it realizes / a bug it fixes).
   A refusal is the CHECK failing → fix the gap, re-commit.

5. **S_graduate — closure + graduation.** Closure passes (doc(m)↔module biject; ORIGIN cited) → the
   realized idea GRADUATES out of vision(m) into doc(m) (it's built now). `journal` the decision.
   - **If this change BIRTHS a NEW module** (its `doc(m)` did not exist before), also graduate its design
     IN from the mega-topic by tag: `vision graduate <relpath> --from <topic> --by-tags <component>` —
     the design vision sorts out of the mega into the new module's `vision(m)` (lossless; see THE LAW's
     "VISION IS MEGA PRE-MODULE, THEN GRADUATES BY TAG").

## CoR (this state's binding + transition)

Now that I've read `doc-mirror-change`, I will get the COMPLETE boundary of `{{module}}` (entire module +
its doc(m) + every caller) in one read. Then: if I'm in USING-mode I `docmirror-cursor set --phase prompt`
and call `doc-mirror-prompts` to dispatch the change (then verify the artifact myself and return); if I'm
BUILDING the system WITH Isaac I author the change directly. Then I re-derive doc(m), run `doc-mirror-commit
<m> "<what>" "<why>" "<ORIGIN>"`, and if it refuses I fix the gap and re-commit. On closure pass the idea
GRADUATES vision(m) → doc(m); I `journal` the why, `docmirror-cursor set --phase seework`, and call
`doc-mirror-seework`. If I cannot make the change correctly (architecture fork / irreversible / needs
Isaac): I `journal -t OPEN "<fork + why>"`, `docmirror-cursor set --phase open`, and `docmirror-sleep`.
