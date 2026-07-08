---
name: make-ai-operating-system
description: "WHAT: the architect/compiler for AI operating systems (AIOS, a 'claude system') -- reads the option space, picks the shape, interviews you, emits the directory + operating program. WHEN: 'make me a system / harness / agent-environment for X'; designing a new way of running Claude; building any new claude-system of the doc-mirror class."
---

# MAKE AN AI OPERATING SYSTEM (AIOS) — the architect

## WHAT A CLAUDE SYSTEM IS (the definition — internalize before anything)
A claude system is **the context-part of what used to be an agent module.** We used to write agent
CLASSES — methods, states, interconnected logic for "on session start do X", "each turn do Y", "when
you learn something make a skill/rule shaped like Z", "remember context like this", "set up the task
list like that", "end the session like this", "loop like this". A claude system is that SAME
behavioral program — but **externalized into markdown the agent reads and neurally executes**, instead
of code a runtime calls. The agent IS the interpreter.

So a claude system =
- **an environment** — a directory laid out a certain way (the "object's state/fields"), AND
- **an operating program in markdown** — the agent's lifecycle methods as context files:
  *session-start · do-a-turn · session-end · memory/rehydrate · skill+rule creation (when/what shape)
  · work-tracking (queue / task-list / progress-tracker) · run-mode (how it runs).*

The ESSENCE is the lifecycle-program-as-context. Everything specific (does it produce an artifact?
a bijection + closure test? components? continuous vs cron loop?) is just **which methods THIS
system's program happens to define.** doc-mirror is ONE fully-worked instance (its methods = read
root→descend, doc(m)-on-change, commit, harvest, compact, rehydrate, brainhook loop) — it is an
EXAMPLE, not the template. Do not force doc-mirror's artifact/closure machinery onto every system.

## RUN-MODES (the "how it runs" method — at least these flavors)
- **hand-invoked** — a skill/procedure the user triggers. (Lightest. Often just one skill, no dir-env.)
- **intermittent** — a dir with a QUEUE + a skill to add to it + a cron/scheduled agent that wakes,
  drains the queue, exits. (e.g. a license auditor you queue deps to and cron works through.)
- **continuous** — a brainhook Stop-loop that re-injects a prompt every turn until the user breaks it
  out; idle via sleep; compact + SessionStart rehydrate. (doc-mirror's flavor.)
A request that needs NO autonomous running at all is probably just a skill/component, not a system —
say so.

## THE STATE-MACHINE SHAPE (how a CONTINUOUS system is actually structured — the core insight)
A tight continuous claude system IS a state machine, and it reifies onto the components 1:1. When you
design a continuous (or intermittent) AIOS, author these five parts:
- **states = skills** — each state of the work is its own skill (`{subgraph} + {explanation} + {CoR}`).
  The agent is always *inside* one; you never improvise a step outside a state.
- **transitions = each state's CoR + a CURSOR** — the state's CoR ends by advancing a persisted cursor
  (the "you are here" pin, resumable across compacts) and naming the next state.
- **the CORE LOOP = a resident attention-chain PRIME** — the unsaid priming, re-injected every turn
  (Stop hook / SessionStart), that shapes how the agent understands each turn. It is NOT a CoR you
  paste; the per-turn CoR the agent EMITS is the said activation of this priming.
- **transition enforcement = a PreToolUse hook** — gates nonsensical state changes (single-shot,
  forceable), so the agent catches itself. The catastrophe-surface guard.
- **reification = the diagrams** (`SYSTEM.md` + a state-graph doc + an always-on rule) — the machine
  explained back to the agent so it stays legible.
doc-mirror is the worked instance: states = `doc-mirror-{init,seework,change,prompts}`; cursor =
`docmirror-cursor`; core loop + router = `doc-mirror-boot`; hook =
`docmirror_transition_guard`; reification = `STATE_GRAPH.md`.

**The positioning (why this matters to people):** what the market calls an "AI Operating System" is
exactly this — **the folder the AI lives in + a frontend, with the core loop + states-as-skills + hooks
on top.** The folder-structure-the-agent-lives-in IS the OS; agents and skills sit on top of it. When
you design one, you are not "adding plugins" — you are authoring the OS the agent runs in.

## STEP 1 — READ THE OPTION SPACE FIRST (before interviewing — you cannot architect blind)
Equip/read, as relevant to the request:
- `understand-advanced-claude-code` — the 7 components (CLAUDE.md, skills, hooks, MCPs, slash-commands,
  subagents, plugins) + system-level patterns. This is the vocabulary you reason in.
- The reference instance: `gnosys-plugin-v2/doc-mirror-system/SYSTEM.md` + `context/architecture.md`
  + `DOC_MIRROR_SYSTEM.md` — ONE worked claude system, to see a full program rendered as context.
- `claude-system-diagram-set` rule (the SYSTEM.md 4-diagram standard).
- `meta-prompt-engineering` (to refine every emitted artifact), `compile-claude-code-component`
  (to build any component the design needs, per-component), `add-to-defaults` (to persist skills).

## STEP 2 — ARCHITECT THE SHAPE (reason out loud about the design space for THIS request)
Before asking the user anything, think through the option space aloud, e.g.:
"A licensing thing… could be a single skill, or a skill + an MCP, or a dir the agent loops in via
cron+queue, or a whole harness. A team is overkill. Probably: a dir with a queue + an add-to-queue
skill + a cron runner — i.e. intermittent run-mode, light program." Narrow to 1-2 candidate shapes
WITH the reasoning, so the interview is about confirming/choosing, not blank discovery.

## STEP 3 — INTERVIEW (AskUserQuestion-driven; skip if running auto/headless with a given spec)
Ask ONE question at a time, 2-4 options each (recommended-first, from your STEP-2 reasoning) +
free-type. Don't ask a fixed form — ask the questions YOUR reasoning surfaced. The decisions to land:
1. **SHAPE** — single skill / skill+MCP / dir-env + intermittent (cron+queue) / dir-env + continuous
   (brainhook loop) / harness/team. (Pick from your candidates.)
2. **RUN-MODE** — hand-invoked / intermittent / continuous (this picks which lifecycle methods exist).
3. **THE LIFECYCLE METHODS to author** — for the chosen run-mode, which of: session-start, do-a-turn,
   session-end, memory/rehydrate, skill+rule-creation (when + what shape), work-tracking
   (queue/task-list/progress-tracker). A continuous loop needs all; a hand-invoked skill needs few.
4. **WHAT IT PRODUCES + HOW ORGANIZED** — output(s), and (only if it produces an artifact SET) the
   organization + any closure check. (Artifact/closure is OPTIONAL — many systems just act/track.)
5. **COMPONENTS** — which of hooks/skills/MCPs/subagents (0..N) it needs. Default few. Build each later
   with `compile-claude-code-component`.

## STEP 4 — EMIT (do only what the shape needs; review each artifact as produced)
- Create the directory environment (the geometry from the interview).
- Write the **operating program as markdown** — the chosen lifecycle methods as context files
  (a CLAUDE.md at minimum; + per-method files / a queue / a progress-tracker as the run-mode needs).
- For a continuous system: fork the doc-mirror loop hooks (brainhook + session_start + sleep + commit
  + toggle), repoint the prompt. Build → test standalone → wire → LEAVE OFF (never enable a
  self-blocking Stop hook in the build session). For an intermittent system: write the queue + the
  add-to-queue skill + the cron runner spec (do not install the cron without user say-so).
- **SYSTEM.md** — the 4 ASCII diagrams (LAYER/FLOW/GEOMETRY/LIFECYCLE), `===ONLY EDIT IF SYSTEM
  CHANGES===`, read-first (per the diagram-set rule). A trivial single-dir/single-file system may
  inline an abbreviated map in its CLAUDE.md instead.
- **Components** (if any) — invoke `compile-claude-code-component` once per component.
- **REVIEW each artifact as produced** (never batch): (a) `meta-prompt-engineering` theoretical pass —
  every fragment commands in the correct direction, unambiguous, no info loss; (b) SHOW the user the
  artifact/diff → AskUserQuestion approve/revise/scrap → loop until approved. The user is the
  architect; do not advance on your own say-so. Later artifacts build on earlier ones.

## STEP 5 — CLOSURE
Well-formed when: the dir-environment exists; the operating program (the chosen lifecycle methods) is
authored as context; SYSTEM.md/inline-map exists; the run-mode mechanism is in place (skill / cron+queue
wired-but-not-installed / brainhook wired-but-OFF); every component built; and the user has signed off
on every artifact. Methods/layers the shape didn't need are correctly ABSENT — a one-skill answer is
complete as one skill. Do not invent machinery the shape didn't call for.

## ALTITUDES (don't confuse)
- **L0 instance** — a specific claude system (e.g. doc-mirror).
- **L1 init** — `doc-mirror-init`: rebuild the doc-mirror instance into a dir (guarded).
- **L2 architect** — THIS skill: design a NEW claude system of ANY shape from a request.

With `understand-advanced-claude-code` (know the components) + `compile-claude-code-component` (build
one) + this skill (architect the system) + `meta-prompt-engineering` (refine), this is the skill set
for actually using Claude Code for real: program the agent's behavior as context, not as code.
