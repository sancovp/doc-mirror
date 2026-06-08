# How To Make A Harness (worked example: the Waypoint MCP)

A **harness** is the thing that **sequences typed outputs across a turn / across turns** — it runs a
*flow* (`cond / tool-use → CoR abc → CoR abc' → …`). A guy (see `how-to-make-a-persona-prompt.md`)
supplies the per-step cognition; a harness decides **what step comes next and feeds it**. This page
teaches the harness layer through a real one — **Waypoint** — read **in terms of the
`compiler → compiler-compiler → transition-map` shape** (the same symmetry that makes any of this boot
reliably), and then shows **how you put your own agent-harness on top of it** so you can run the agent
however/wherever you want.

> Layer map: `block → output → turn → HARNESS`. Personas live at block/output; harnesses live here.

---

## Part 1 — Waypoint: an MCP that *makes prompt-flows and executes them*

Waypoint (`starsystem/waypoint/payload_discovery`) is an MCP whose whole job is: take a **flow defined
as data**, and **walk an agent through it one step at a time**. It has three faces, and they line up
exactly with the reliable shape.

### The flow-as-data (the unit)
`core.py` — a `PayloadDiscoveryPiece` is one step:

```
PayloadDiscoveryPiece { sequence_number, filename, title, content, piece_type, dependencies: [int] }
```

A `PayloadDiscovery` is the whole flow: numbered pieces grouped into `directories` + `root_files`, an
`entry_point`, and — load-bearing — **`PayloadDiscovery(RenderablePiece)`**: the flow *is itself a
renderable piece*, so a flow can contain flows. It is plain data (`to_json`/`from_json`), so a maker
agent can author or edit it.

### The three faces = `compiler → compiler-compiler → transition-map`

```
COMPILER            a PayloadDiscovery compiles a spec → an executed flow:
                      .render_to_directory()  spec → a numbered directory on disk
                      MCP navigation          spec → pieces served one at a time
                    (definition → running thing)

COMPILER-COMPILER   the machinery that PRODUCES PayloadDiscoveries:
                      compiler.py  PayloadDiscoveryCompiler.compile_directory()
                                    ANY numbered-markdown directory → a PD spec
                                    (extracts seq#, title, piece_type; infers deps)
                      + to_json/from_json + maker agents author specs as data
                      + PayloadDiscovery IS a RenderablePiece → composes into bigger PDs (SELF-HOSTING)
                    (a system that makes flow-compilers — i.e. it makes the makers)

TRANSITION-MAP      dependencies:[int] (the DAG)  +  the MCP step-server:
                      _get_next_sequence_number()  reads completed-state, picks next
                      get_next_prompt / start_waypoint_journey / completion entry
                    (the edges + the executor that walks them, step by step)
```

So Waypoint is `compiler → compiler-compiler → transition-map` made concrete: a flow **is** a compiler
(spec→served sequence); the directory-compiler + JSON-editability + self-hosting **make** flows (the
compiler-compiler); the dependency-DAG + the next-step navigator **are** the transition-map the harness
executes.

### State lives outside the agent
`mcp_server_v2.py` header: *"No in-memory state — everything uses persistent JSON files."* Position is a
temp JSON; completed steps come from a diary registry; each `get_next_prompt` **reconstructs** "where am
I" and serves the next piece. That is what makes the harness **resumable and platform-agnostic** — the
flow + the cursor are data, not process memory.

**One-line read:** Waypoint = *flow-as-data* (`PayloadDiscovery`) + *a step-executor* (the MCP tools).
That pair — **a definition you can make/edit + a thing that walks it** — is the minimal harness.

---

## Part 2 — Coding your own agent-harness *on top of* the MCP harness

The MCP harness defines and **serves** the flow; it does not run an agent. To actually run an agent —
on the Claude Agent SDK, your own loop, any platform — you **stack a second harness on top** whose only
job is the loop:

```
# agent-harness (pseudocode) — a SECOND harness over the MCP harness
start_waypoint_journey(config_path=FLOW, starlog_path=PROJECT)     # arm the flow
while True:
    step = get_next_prompt(PROJECT)            # MCP serves the next piece (its content = the prompt)
    if step.is_END: break
    result = run_agent(step.content)           # YOUR runner: SDK / custom loop / whatever platform
    mark_complete(PROJECT, step, notes=result) # MCP advances the cursor (persisted)
```

Two harnesses, stacked:
- **MCP harness** = the flow-engine (makes/serves the transition-map; state in JSON).
- **agent harness** = the runner (consumes served steps, drives an agent, reports completion).

Because the MCP keeps all state in files, **the runner is swappable** — you can run the same flow under
a different agent platform by rewriting only the thin `run_agent` loop. That's the point of stacking:
the *what-comes-next* (flow) is fixed and reusable; the *how-it-runs* (platform) is a separate, replaceable
harness on top.

---

## Part 3 — Run an agent *via a tool* (worked example: the progenitor / Hermes system)

So far a harness *serves steps* and something *runs* against them. Now go one level up and ask a strange
question: **what if "set up an agent and run it" were itself just a tool — one another agent could call
mid-conversation?** If it is, then an agent can **create and run other agents** the same way it calls
any other tool. The legacy Heaven "progenitor" system is a real, clean example of it. Pulling it off
needs two capabilities — **a way to build the sub-agent's personality, and a way to run it** — so the
system comes in two halves.

### Half A — building the sub-agent's persona (the "progenitor" half)

Picture a **factory that stamps out agent personalities from inheritable blueprints**, like a class
hierarchy:

- a **deity** blueprint is the most general — the species-wide base personality;
- a **progenitor** blueprint specializes the deity for a domain;
- a **worker** is the concrete agent, built by filling in its progenitor's blueprint (which was itself
  built from its deity's).

In the code: `SystemPromptConfig(species, agent_type, name, domain, process)`, and calling `.build()`
finds the agent's **DNA** (a JSON file holding the values that fill the blueprint), composes
deity → progenitor → worker, and produces the finished **system prompt** — the guy. Two details matter:
it looks for an **evolved** DNA file *before* the original one (so an agent that's been improved over
time automatically gets its better version), and the deity → progenitor → worker chain is the same
**generator → generator → instance** ladder we keep seeing: *a deity makes progenitors, a progenitor
makes workers.* So Half A is a **persona generator** — the §G "meta-prompting system" from the persona
guide — built into the framework, over personalities that can evolve.

### Half B — running that agent, wrapped as a tool (the "Hermes" half)

Now you can build a guy; you need a way to run one. That's a recipe plus a runner:

- A **recipe** (`HermesConfig`, saved as JSON) says: *which* agent to run, *what goal* to give it — with
  blanks left in, like `"summarize {document}"` — how many iterations, and which tools. The blanks are
  declared up front in a `variable_inputs` schema.
- The **runner** (`use_hermes`) takes the recipe plus the **values for the blanks**, fills them in,
  builds the agent (its system prompt is the guy Half A made), runs it for N turns, and returns the
  result. Those fill-in values are exactly the **dovetailed input** from the persona guide (§F): the
  recipe is the bound persona, the values are the complementary input slotted under it.
- The whole runner is then exposed as **one tool** (`HermesTool`). So any agent, in the middle of its
  own turn, can call that tool and thereby **spin up a fresh agent, hand it a goal, and get its answer
  back** — without doing the work itself.

And you can wire runs together: a `DovetailModel` says "take *these* outputs from the run that just
finished and feed them as the inputs to the next run," so a chain of agent-runs passes data down the
line (the same data-passing as a flow's dependency edges, one tier up).

### Why this matters

A normal harness sequences *prompts or steps*. This one **builds a persona and runs a whole agent**, and
that entire act — build + run — is **packed inside a single tool call.** So instead of *you*
orchestrating agents, *an agent* orchestrates other agents just by calling a tool. Same
`compiler → compiler-compiler → transition-map` shape, one grain up:

```
compiler           a recipe + its filled-in values → a built, running agent
compiler-compiler  the deity→progenitor→worker factory that GENERATES the agents themselves
transition-map     the dovetail wiring (one run's outputs → the next run's inputs) + the chain that walks it
```

Set it beside Waypoint (Part 1): Waypoint sequences *prompt-pieces* and serves them one at a time; the
progenitor/Hermes system sequences *whole agent-runs* and packs the runner into a tool. And note it
already contains, under old names, two things the persona guide names: the **dovetailed input** (§F) is
Hermes's fill-in `variable_inputs`, and the **persona generator** (§G) is the deity → progenitor →
worker genealogy. Part 4 takes the last step: a tool that doesn't just *run* an agent but *manufactures*
agents and tools.

> Worked example only (the legacy Heaven framework) — you wouldn't depend on it; the lesson is the
> *shape*: wrap "build a guy and run it" in a tool, and you get agents that orchestrate agents.

---

## Part 4 — The factory: a tool that builds agents *and tools* (worked example: `construct_hermes_config`)

Part 3's tool *runs* an agent. The next tool *manufactures* them. `construct_hermes_config` (the legacy
`ConstructHermesConfigTool`) is a single tool an agent can call — and **one call can build a whole team
of agents, write a brand-new tool, and test all of it by running agents.** Here is what one call does
when you ask it to stand up a new capability (its own documented example: a "prompt engineering" agent +
tool). Each maker below is roughly one LLM call; the agent tests run for their configured iterations.

1. **Worker agent doesn't exist yet? Make it.** `evolutionary_intent(...)` **writes the worker's system
   prompt** (the persona, from the genealogy), then `agentmaker_func(... test_prompt, iterations=1)`
   **writes the agent's config and test-runs it** to confirm it works.
2. **Domain orchestrator doesn't exist? Make it.** Same two steps — and its test prompt is literally
   *"report the managers you can call, then call one with a dummy hello"*, so **the orchestrator's test
   run calls a manager agent.**
3. **Subdomain manager doesn't exist? Make it.** Same two steps again.
4. **Save the recipe** — a `HermesConfig` (the templated run-spec from Part 3).
5. **Code-generate a brand-new tool.** Derive the tool's name and argument schema from the recipe,
   `_generate_util_code(...)` **writes a `.py`** whose function calls the runner (`hermes_step`), then
   `toolmaker_func(... test_prompt)` **writes the tool and test-runs an agent against it**, and
   `register_tool(...)` **adds it to the system's tool registry.**

Tally one call: a worker, a manager, and an orchestrator **created** (persona written + each test-run),
those tests **calling each other**, a recipe **saved**, and a **new tool written, tested, and
registered.** So "how many agents" is never one — it's a **cascade**: *agents making agents making tools
that make agents.* And it is **self-extending** — the tool it writes becomes a new capability the system
can call forever after, and every later call of *that* tool runs an agent of its own.

That is the top of the harness ladder: not "run a flow," not even "run an agent via a tool," but **a
tool that grows the agent system itself** — it builds the workers, the management chain to coordinate
them, and the tool to invoke them, verifying each by running it. It's the same
`compiler → compiler-compiler → transition-map` shape turned on the *toolset*: a compiler whose output
is *more compilers* (agents and tools).

> Worked example only (legacy Heaven framework). The lesson is the *ceiling* of the pattern: when "build
> a guy and run it" is itself a callable, one call can **manufacture and wire up a whole sub-system of
> agents and tools, and test it by running it** — self-extending capability.

---

## Closure — the harness ladder

```
harness = flow-as-data  +  a step-executor that walks it

the ladder, each rung the same compiler→compiler-compiler→transition-map shape at a higher grain:
   1. MCP harness            defines + serves a prompt-flow            (Waypoint)        — sequence prompt-pieces
   2. agent harness on top   runs an agent against the served steps    (thin runner)     — run a flow on any platform
   3. runner-in-a-tool       build a guy + run it, packed as a tool     (progenitor/Hermes) — an agent runs an agent
   4. factory-in-a-tool      build agents AND tools + test them          (construct_hermes_config) — agents make agents+tools
```

A **guy** is the per-step cognition (built CoR-first); a **harness** sequences the steps; **packing a
harness into a tool** lets an agent invoke it; and at the top, **a tool that manufactures agents and
tools self-extends the whole system.** Make the flow data, make the executor thin, and the
transition-map is the only thing that has to be right.

> The named systems (Waypoint, progenitor/Hermes, `construct_hermes_config`) are *worked examples of the
> pattern*, not dependencies — the lesson is the shape: flow-as-data + step-executor, stacked and packed
> into tools, until a single call can build and test a sub-system of agents and tools.
