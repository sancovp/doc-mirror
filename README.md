# doc-mirror

<!-- SCALABLE-PUBLISHING:AUTOGEN START (managed block — do not edit between these markers) -->

![Stars](https://img.shields.io/github/stars/sancovp/doc-mirror.svg?style=social) ![Updated](https://img.shields.io/badge/updated-2026_06_19-lightgrey.svg)

⭐ 0 stars • 🕑 Updated 2026-06-19

📦 Auto-published from the monorepo • [CHANGELOG](./CHANGELOG.md) • [sancovp/doc-mirror](https://github.com/sancovp/doc-mirror)

<!-- SCALABLE-PUBLISHING:AUTOGEN END -->

**A Claude Code plugin that turns your Claude Code into a documentation-and-development *operating
system* for any codebase.**

doc-mirror is a *claude system* (an "AI operating system"): not a single command, but a **folder the
agent lives in + a core loop it runs every turn + skills, hooks, rules, and CLIs on top.** Installing
this plugin gives your Claude Code that operating system — it adds skills, hooks, rules, and CLI tools,
and **changes nothing else about your setup.**

What it does: it keeps a **1:1 documentation mirror** of a codebase — one explanation file per source
module — and it develops the codebase through a small, fixed **state machine** so the documentation
never drifts from the code, and the agent never improvises a flow.

---

## The one idea

Two agents running doc-mirror on the same codebase produce the **same** structure. That invariance is
the whole point. It comes from three rules:

1. **Every doc file is exactly one legal kind** (see *The Law* below). No random session/fix/topic
   documents, ever.
2. **The agent is a state machine, not a freestyler.** It is always *inside* one state; it does that
   state's work, advances a saved cursor, and loops. The flow is scripted, not invented each turn.
3. **Documentation is paired with code and committed together** (*fork-on-change*), so the docs can
   never silently fall behind the code.

---

## How it runs — the core loop

Every session (and after every compaction), the first thing the agent does is use the **`doc-mirror-boot`**
skill. Boot primes the agent with the core loop, shows it the whole state machine, and routes it — via
the **cursor** (a persisted "you are here" pin) — into the one state it is currently in:

```
doc-mirror-boot  →  read the cursor  →  enter the state it names  →  do that state's leg
                 →  advance the cursor + journal the why  →  loop  (back to boot, or exit)
```

The **states are skills**:

| state (skill)         | what it is |
|-----------------------|------------|
| `doc-mirror-init`     | first-time mirror an unmirrored codebase (enumerate modules → write a doc per module → synthesize the index files → closure test) |
| `doc-mirror-seework`  | the dispatcher: read the backlog, pick the next gap, route to the state that does it |
| `doc-mirror-change`   | a module changed → re-derive its doc → commit code+doc together → run the closure test |
| `doc-mirror-prompts`  | need an agent to *do* a task → search a reusable, reliability-scored prompt library, or author one |

Transitions are each state's reasoning chain plus the cursor; a hook keeps the moves sensical; the loop
prompt + an always-on rule keep the machine in front of the agent every turn, even after a compaction.

---

## The Law (what every doc file must be)

For a codebase `C`, **every file in its documentation layer is exactly one of:**

- **`doc(m)`** — the *impl* doc: a 1:1 explanation of what one module's code **actually is**, at
  `docs/mirror/<relpath>.md`. Written first, always. Records only what exists.
- **`vision(m)`** — the *vision* doc: every idea/decision about a module **not yet built**, at
  `docs/vision/<relpath>.md`. The gap between vision and impl **is** the backlog.
- a **named synthesis**, one of the **6 `context/` index files**, a **repo-local rule/skill**, or the
  dated **journal** (`context/journal/`).

Nothing else is legal. The **closure test** is the gate: the doc set must biject 1:1 with the module
set, and every file must classify under the kinds above. A run is "done" only when it passes.

---

## What's in this plugin

```
plugin/
├── .claude-plugin/plugin.json   the plugin manifest (name, version, description)
├── skills/                      the STATE MACHINE — one skill per state, plus the entry + the law
│   ├── doc-mirror-boot/           entry point: core-loop prime + router (use first, every session)
│   ├── doc-mirror-init/           state: first-mirror a codebase
│   ├── doc-mirror-seework/        state: read the backlog, pick the next gap, route
│   ├── doc-mirror-change/         state: re-derive a doc + commit code+doc + closure
│   ├── doc-mirror-prompts/        state: the reusable prompt-skill library (search / author / score)
│   ├── doc-mirror-install/        the host-setup WIZARD: agent places the bins + records the plugin root (run once)
│   ├── doc-mirror/                THE LAW: the invariant all states operate under
│   └── make-ai-operating-system/  the architect — design a NEW system of this class
├── hooks/                       the loop + the guards
│   ├── docmirror_brainhook.py       Stop hook: re-injects the loop prompt each turn (the work loop)
│   ├── docmirror_session_start.py   SessionStart hook: re-boots the context cascade after a compact
│   ├── docmirror_transition_guard.py PreToolUse(Skill): blocks a nonsensical state jump once
│   ├── docmirror_readonly_guard.py  PreToolUse: makes the managed doc files CLI-only (no hand-edits)
│   └── hooks.json                   registers the four hooks (plugin-relative)
├── bin/                         the CLIs (the "you are here" pin + the managed-file actuators)
│   ├── docmirror                    search the prompt-skill store + the doc-mirror graph (FTS5)
│   ├── docmirror-cursor             read/advance the cursor (your state pointer)
│   ├── journal                      append to the dated thinklog (and project it into vision)
│   ├── doc-mirror-commit            commit a code change together with its re-derived doc (fork-on-change)
│   ├── vision                       read the backlog / closure-check / migrate / graduate the vision layer
│   ├── tracker                      write the prioritized plan (pointers into the backlog)
│   ├── plan / projects              orientation: what's open, which repos are mirrored
│   ├── docmirror-layers / -system   derive the architecture stack + render the SYSTEM diagram
│   └── docmirror-sleep / -brainhook idle mechanic + the loop on/off toggle
├── rules/                       the behavior rules (the law + verification/honesty/code-reading discipline)
├── docmirror_loop_prompt.txt    the per-turn loop prompt the brainhook re-injects
├── docmirror_harvest_reminder.txt the periodic "capture a reusable rule/skill" reminder
└── install.sh                   the WIZARD's script: places ONLY the host-level pieces a plugin can't
                                 (bin/* onto PATH + records the plugin root); non-destructive — see Install
```

**Why it's organized this way:** `skills/ hooks/ rules/ .claude-plugin/` is the standard Claude Code
plugin layout — the skills *are* the state machine, the hooks *are* the loop and the guards, the rules
*are* the behaviors. The `bin/` CLIs and the two loose `.txt` runtime files are the parts a plugin
manifest alone cannot place on the host (a CLI has to be invocable; the loop prompt has to be
re-injectable), which is what the setup step handles.

---

## The concepts (glossary)

- **doc(m)** — a module's impl doc (what the code *is*).
- **vision(m)** — a module's vision doc (what's wanted but *not yet built*); the gap is the backlog.
- **the cursor** — your persisted "you are here" pin; which state you're in. Survives compaction.
- **the journal** — your dated thinklog of what you *thought/decided* (distinct from git log = what *changed*).
- **fork-on-change** — on any code change, re-derive that module's `doc(m)` and commit them together.
- **the closure test** — the doc set bijects 1:1 with the module set; the gate for "done".
- **the core loop** — the resident attention chain that primes every turn (boot → cursor → state → loop).

---

## Install

This is a standard Claude Code plugin. Installing it adds the doc-mirror skills, hooks, and rules to
your Claude Code and places the CLI tools — and changes nothing else. After install, start any
doc-mirror session by using the **`doc-mirror-boot`** skill; everything else cascades from there.

(The `install.sh` setup step exists to place the host-level pieces a manifest can't: the `bin/` CLIs so
they're invocable, and the loop-prompt / reminder runtime files the hooks re-inject.)

---

## Use

1. **Mirror a codebase** — point doc-mirror at a repo with no docs; `doc-mirror-init` enumerates its
   modules, writes a `doc(m)` for each, synthesizes the 6 context files, and runs the closure test.
2. **Develop it** — as code changes, `doc-mirror-change` re-derives the affected `doc(m)` and
   `doc-mirror-commit`s code + doc together; the closure test keeps the mirror honest.
3. **Think out loud** — `journal` everything you decide; it projects into the vision layer (the backlog)
   automatically. You never hand-edit the managed files — the CLIs write them, and a guard enforces it.
4. **Find what's left** — `doc-mirror-seework` reads the backlog (`vision` gaps) and routes you to the
   next thing; `doc-mirror-prompts` dispatches an agent against a reusable prompt when a task needs one.

---

## Two levels

- **Level 1 (this plugin):** make doc-mirror — a claude system — into a proper Claude Code plugin that
  gives these skills to your existing Claude Code, changing nothing else.
- **Level 2 (later):** those skills boot a **containerized, autonomous** doc-mirror that compiles its own
  parts and runs without you — so your main agent sends it tasks like any remote coding agent (and gets
  back a worktree branch / PR), and sends feedback through the plugin's skills. Not built yet.

---

## For developers of doc-mirror itself

The canonical source is `gnosys-plugin-v2/doc-mirror-system/` (this `plugin/` is the shippable unit).
The full operating state machine is `doc-mirror-system/STATE_GRAPH.md`; the four at-a-glance diagrams
are `doc-mirror-system/SYSTEM.md`; the deep spec is `DOC_MIRROR_SYSTEM.md`. When you change the state
machine, change every coupled piece in lockstep (the state skills, the cursor phases, the legal-transition
table + the transition hook, the loop prompt, the rules, the diagrams) — editing one in isolation is how
the machine desyncs.
