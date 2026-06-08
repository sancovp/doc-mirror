---
name: doc-mirror-seework
description: "WHAT: the SEEWORK state of the doc-mirror machine — the backlog dispatcher: read the always-true VIEW (vision diff = vision(m) − doc(m) = what is NOT-yet-built), take the next prioritized pointer from the tracker, and route to the state that does it. WHEN: Use immediately when the situation is — you need to decide what to do next / 'what needs doing?': after init completes, after a change lands, after a prompt task finishes, or right after doc-mirror-boot when the cursor names no pending module (any of)."
---

# doc-mirror-seework — the SEEWORK state (read the backlog, pick the next gap, route)

You are in the **seework** state. This is the dispatcher: it does no code/doc work itself — it reads the
backlog VIEW, picks the next gap from your prioritized plan, and transitions to the state that does it
(`change`, `prompt`, or `init`). Operates under **THE LAW** (the `doc-mirror` skill).

## The subgraph (this state's shape)

```mermaid
stateDiagram-v2
    [*] --> R_view: R — the BACKLOG = the VIEW: vision stats (gaps by project) -> vision project <p> -> vision diff <m>
    R_view --> PLANNED
    state PLANNED <<choice>>
    PLANNED --> S_pick: [a prioritized PLAN exists in the tracker -> take its next pointer]
    PLANNED --> S_plan: [no plan yet -> PRIORITIZE the gaps (judgment) -> `tracker add <vision-ref>` = write ordered pointers into vision gaps]
    S_plan --> S_pick
    S_pick --> RECONCILE
    state RECONCILE <<choice>>
    RECONCILE --> T_change: [pointer's gap is code/doc to write -> cursor=change ; call doc-mirror-change]
    RECONCILE --> T_prompt: [pointer's gap needs an agent task -> cursor=prompt ; call doc-mirror-prompts]
    RECONCILE --> T_init:   [pointer is an unmirrored repo -> cursor=init ; call doc-mirror-init]
    RECONCILE --> S_strike: [pointer's gap CLOSED (realized → left vision) -> `tracker strike <ref>` drops the pointer, re-view]
    RECONCILE --> WAIT_idle:[view shows no gaps for the active repo -> idle]
    S_strike --> R_view
```

## What this state is (the tracker vs the view)

The **VIEW** is the always-true backlog, DERIVED from `vision(m) − doc(m)` — you never write it; you read
it with the `vision` CLI:
- `vision stats` — gaps by project (where the work is).
- `vision project <p>` / `vision <tag>` — the gaps for one project/tag.
- `vision diff <m>` — for module `m`, exactly what is in vision(m) but not yet in doc(m) = NOT-yet-built.

The **progress-tracker** is the MANUAL prioritized PLAN = an ordered list of POINTERS into vision gaps
(you author it because priority is a judgment call). It is a CLI-ONLY managed file — you NEVER hand-edit
it; the **`tracker` CLI is its actuator** (`tracker add <ref>` / `tracker strike <ref>` for the PLAN;
`tracker register`/`tracker active <repo>` for the ROOT REPO ORDER router — `tracker show` to read it).
Because it is pointers, the view RECONCILES it (`plan check`): a pointer whose gap is now closed = done
(`tracker strike` it); a gap with no pointer = un-planned backlog. So the tracker is **manual to write
(via the CLI) but mechanically auditable** — it can never *silently* go stale.

Routing the picked pointer:
- it's **code/doc to write** for a specific module → `change`.
- it needs an **agent to DO a task** (a dispatch) → `prompt`.
- it's an **unmirrored repo** → `init`.
- its gap is **already closed** (the idea graduated to doc(m)) → `tracker strike <ref>`, re-view.
- **no gaps** for the active repo → `idle`.

## CoR (this state's binding + transition)

Now that I've read `doc-mirror-seework`, I will read the VIEW (`vision stats` → `vision project`/`diff`
for the active repo), then take the next prioritized pointer from the tracker (or PRIORITIZE the gaps and
write the plan first with `tracker add <ref>` if none exists). Then I route: if the pointer is code/doc to
write I `docmirror-cursor set --phase change` and call `doc-mirror-change`; if it needs an agent task I set
`--phase prompt` and call `doc-mirror-prompts`; if it's an unmirrored repo I set `--phase init` and call
`doc-mirror-init`; if its gap is already closed I `tracker strike <ref>` and re-view; if there are no gaps
I go idle (`docmirror-sleep`).
I `journal` the pick + the why. If prioritization itself is a fork I cannot resolve (needs Isaac's call on
what matters): I `journal -t OPEN "<fork + why>"`, `docmirror-cursor set --phase open`, and `docmirror-sleep`.
