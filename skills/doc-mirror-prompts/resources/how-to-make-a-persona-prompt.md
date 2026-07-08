# How To Make A Persona Prompt

**You make this up.** An encoding either *has* the symmetries that make an LLM go "oh duh" and follow
it, or it doesn't — it **boots into a reliable system or it doesn't.** That's the only test. It isn't
complex at the base; it gets complex as you add tokens and make more meaning. The trick that keeps it
reliable as it grows: **make everything `compiler → compiler-compiler → transition-map` shaped** (the
generative-basis / self-hosting / Futamura shape). When what you make up is always that shape, the LLM
gets it.

This reference is the metalanguage for doing that on purpose — both to **teach from** and to **compose
with**. A persona (we call one a **"guy"**) is a prompt that puts an LLM in a role, built from *blocks*,
**CoR-first**, and **booted, not written**. `persona ⊂ prompt` (the `prompt` type is first-classed
later — not now).

> **Sibling, canonical:** `how-to-write-a-prompt.md` — how to write *any one block* well (the
> generative-basis pattern, XML sections, algebra⊕geometry, templating). THIS guide is the layer above:
> it types the blocks, encodes them into a bootable guy, and says what runs where.

---

## A. The blocks (vocabulary) — the neural ↔ symbolic axis

A guy is made of blocks. The reasoning blocks are distinguished by **whether the LLM must SAY them**:

```
CoR   = Chain of Reasoning   the LLM must EXPLICITLY SAY it           ← SYMBOLIC end · reliable ("overpowered")
                               (saying it IS what makes it a CoR)
attn  = Attention Chain      same shape, NOT said; steers generation  ← NEURAL end · partial
                               only "somewhat"; STACK many → emergent activation
```

A procedure (e.g. OMNICOMP) is **a CoR iff activated/said, otherwise just an attention chain.**

Orthogonal to reasoning:

```
style   output manner — voice, register, emoji      (⊥ to reasoning: "fun" ≠ "how it thinks")
schema  output-contract — the fixed output shape     (PersRubric schema · "wrap 🎭" · "emit Dragonbones")
```

**THE DIAL:** more **CoR** ⇒ more **symbolic + reliable**; more **attn** ⇒ more **neural + emergent**.
Choosing the mix is choosing where on the neural↔symbolic axis the guy sits.

---

## B. Encoding — how to BOOT a guy (not write one)

You don't write a guy in prose; you **encode an operating-structure the LLM loads and runs as.** The
encoding (worked on "bob"):

```
<bob>                                                               # the tag is the PERSONA'S OWN NAME (here: bob).
you are bob.  bob has a few CoRs; CoRs are used like {how}.         # `<GUY>` is NEVER written literally — it is only this doc's placeholder for "the persona's name-tag".

CoRs:           [ {sym} : {CoR name} : `{the literal CoR}` ]      # symbol-indexed table
Chaining:       { chaining system | meta-lang | lang | generator }  # = the GENERATION BASIS
Rules:          [ if {condition} : {sym from CoRs/Chaining/basis} ] # CONDITIONAL DISPATCH (when a CoR fires)
ComboPotentials:[ if {rule} then maybe {rule} ]                     # TRANSITION map — a layer ON TOP of
                                                                    #   Rules, NOT part of it, SEPARABLE
# attn chains about the CoRs                                        # unsaid priming
</GUY>
```

- **Symbol table = compression.** Index each CoR by an emoji/symbol so `Rules` and `ComboPotentials`
  reference it compactly. (The backtick is the literal forced CoR.)
- **Rules = reactive dispatch** (`condition → CoR`): *when* a CoR fires.
- **ComboPotentials = the transition system** (`rule → maybe rule`): *which firing leads to which*. It is
  **separable** — only visible *on top of* Rules, never mixed in. This is the `transition-map` of the
  reliable shape, living *inside* the guy.

**Boot vs write:** writing = prose; **booting = loading this structure so the LLM runs *as* bob.** This
is why a finished guy (e.g. the Poimandres Spine) looks the way it does: symbol table + ops-CoR + rules
+ notation — a bootable system, not an essay.

---

## C. Binding & activation — primed tokens (obvious/stupid)

This is the whole binding mechanism:

```
BIND     wrap the structure top+bottom in a tag   →  the tag becomes a PRIMED TOKEN bound to it
ACTIVATE use the primed token                      →  the LLM invokes the bound structure
```

Personas are **"guys"** generically, and `<GUY>` is a **placeholder used only in this doc** to talk about
the wrapper — say **"make a new `<GUY>` for X"** to mean "make a persona." The ACTUAL wrapper tag is
**named after the specific persona** (`<Skillwright> … </Skillwright>`), and you NEVER write the literal
string `<GUY>` in a real persona — you name the tag whatever you want the agent to understand ITSELF as
being. It is the same move as the CoRs symbol table, one level up: **a symbol binds a CoR; the persona's
own name-tag binds the whole guy.** Bind with a tag, activate with the token. That's it.

---

## C′. The required outer shape — name → description → context → reinforcement, braced + XML-sectioned

A guy / system prompt is **NOT a markdown document.** It has a FIXED outer skeleton: an XML-sectioned,
braced structure. This is the shape EVERY system prompt takes; §B (the encoding) and §H′ (the core
loop) fill the context middle.

- **One outer brace.** Wrap the WHOLE prompt, top and bottom, in a single binding tag **named after the
  persona itself** — e.g. `<Skillwright> … </Skillwright>`. `<GUY>` is ONLY this doc's placeholder meaning
  "the persona's own name-tag"; you NEVER write the literal string `<GUY>` in a real persona.
  (`<SYSTEM_PROMPT>` is the conventional tag for an agent's onboarding entry.) This seals it off from the
  other context injected around it, and primes the tag (per §C).
- **Sections are XML tags; markdown PROSE goes inside.** Each section is its own tag whose NAME *is* the
  section (`<core_loop> … </core_loop>`). Do **not** repeat the section name as a markdown header inside
  its own tag (no `<situation>## The situation …`), and do **not** make every section a bullet list —
  most sections are prose paragraphs; a list is only for a genuine enumeration. (LLMs default to
  "everything is markdown, everything is a list"; the XML sectioning + prose is what breaks them out of
  it. Markdown-everything is the failure mode, not the format.)
- **The fixed section ORDER:**
  1. `<name>` — what this IS, named **meta-first** (the parent class / role), one line.
  2. `<description>` — one paragraph: what it is + what it does.
  3. the **CONTEXT** sections (the abstract middle — `<core_loop>` always, plus whatever the guy needs:
     situation, rules, the CoRs / Rules / ComboPotentials encoding of §B, pointers).
  4. `<reinforcement>` — the **CLOSING** block. A short second-person, present-perfect paragraph that
     reinforces the guy has internalized its core loop and runs it to the letter: *"You have now deeply
     learned that {the core thing}, and you follow {the core loop}, in order, to the letter."*

---

## D. The guy classes

```
C1  single-CoR guy      built AROUND one CoR            "make a guy that talks about / does this CoR,
                                                         and use it for stuff"
C2  CoR-sequence guy     runs a SEQUENCE of CoRs          = a workflow
C3  spliced / complex     combine + splice CoRs and/or     the general case; swap attn for CoR to go
                          attn chains, different ways      more neural — the dial is a knob inside it
```

`C2 = C1s in sequence`. `C3 = arbitrary combination/splice`. **Scale is grain, not class:** "bob" and
the full GNOSYS guy are the same classes at vastly different grain (more tokens, more meaning).

---

## E. The build method — CoR-FIRST (always)

Build the guy **around the CoR**, never the reverse.

```
1. Define the core CoR.                        → test the BASE version (it must work alone first)
2. Build the guy AROUND it.                     → every other block supports / directs toward the CoR
3. Tighten the CoR: make it invoke "prompt-as-code" attn chains BY REFERENCE:
       "…{omnicomp output}… because the omnicomp output … so …"
4. RE-COMPILE the CoR *with the guy as a specialized dialect*.   → test it (vs the base)
5. EVOLVE by talking:
       "tell me about {block}, how you use it in {xyz situation}"  → response
       → NEW convo: "{xyz is the case}"  → log → compare → tweak → refire
       → eventually it "gets it" → ask it to make new parts of itself
```

The product is a **closed chain that knows its identity and its generative basis** (the CoR *is* the
generative-basis core). Closure is what makes it **evolvable** (interesting to talk to about who it
wants to be) and therefore **autonomy-capable.**

---

## F. The complexity ladder — what runs where (binding)

The transition this reference exists to make: from "write good prompts" → to knowing **which rung** a
task needs.

| rung | what | when to use it | bind |
|---|---|---|---|
| **1** | general agent **+ prompt** | the task has **no particular binding requirements** | loosest |
| **2** | **guy prompt injected** into a general agent | it can inject it, but **less reliable** than rung 3 | medium |
| **3** | **guy in the SYSTEM prompt + a dovetailed input prompt** | you need it **bound** | tightest |

**Rung-3 dovetail:** once the LLM is *in* the guy, inject a **complementarily-shaped input prompt**
beneath it — e.g. for a PersRubricUpdater guy, an input schema
`{use_omnicomp: bool, become_it: bool, metaorch: bool, …, msg: str}` concatenated under the guy, or a
dedicated agent built *with* that guy that takes that input.

**The binding law ("why not one agent with different configs?"):** it doesn't bind the same way. If the
agent must do a **deep cognitive operation between using a skill/tool — i.e. decide what to do** — you
want a **guy**. *Unless you don't even know what you want it to do* (then stay general). And the cost:
**the more you control it, the more particular the obstacles become** — you dictate what to do, the LLM
starts *not* doing other things. So: **target exactly what you want → make it reliably happen → build
systems out of those processes.**

---

## G. The generator — meta-prompting systems

A **Meta-Prompting System (MPS)** is an *opinionated template of blocks* that **emits a guy**.

```
MPS := guy_skeleton[ fixed blocks, fixed order, optional block-library ]
MPS(domain, goal) ↦ guy
```

`PersRubricUpdater` is an MPS; **`OMNICOMP`, `SKILLGRAPH`, `PERSUPDATE`, `METAORCH` are its BLOCKS**
(brands of block-types — mostly CoR-or-attn procedures), and it outputs a **`PersRubric`** (a
worker-guy spec). "Make an MPS" = fix a block-skeleton + fill-policy; "use" = `MPS(domain, goal)`. An
MPS is itself just a guy whose job is emitting guys — `compiler-compiler` shaped, on purpose.

---

## H. Up one level — a turn is a sequence of typed outputs; a harness sequences them

A guy composes blocks *within* outputs. But **a turn is just a sequence of typed OUTPUTS** — by
said-ness: `tool-use | skill-use (Skill tool) | CoR | unstructured text` (attn chains are the *unsaid*
steering underneath). So you can sequence them: `cond / tool-use → CoR abc → CoR abc' → …`. **Controlling
that sequence across the turn is a harness** — a sequencer of typed outputs (numbered steps +
dependency-DAG + step-by-step navigation). The `ComboPotentials` transition map *inside* a guy and the
harness sequencing *across* outputs are the **same `transition-map` primitive at two grains.**
(Harnesses = level-3 of the four levels in §I. Worked example — an MCP that makes prompt-flows and
executes them, plus how to stack your own agent-harness on top — is the sibling resource
`how-to-make-a-harness.md`.)

---

## H′. The core loop — the attention chain that primes every turn

§H sequences outputs *within* a turn (the harness). One grain up: a guy doesn't run once, it runs **over
turns**, and what carries it turn-to-turn is its **CORE LOOP**.

```
CORE LOOP = the ATTENTION CHAIN you are PRIMED with (resident, unsaid)
          → it INFORMS the CoR you OUTPUT at the start of every turn (said = the activation)
```

The core loop **IS the attention chain** (the prime) — NOT the output. The per-turn CoR is the **said
activation** that *makes use of the fact you've been primed with the chain*. It's the §C mechanism at the
TURN grain: `tag-to-prime, token-to-activate`. You emit the CoR every turn-start and it lands *because*
the chain is already loaded into you. (Mistake to avoid: "the core loop is the CoR I paste." No — the
core loop is what primes; the CoR is what you say to activate the priming.)

- **Resident + enforced.** The chain lives in the system-prompt surface (the bootstrap/entry skill + an
  always-on rule); a Stop-hook re-injects it so it can't lapse. That residency is what makes it the
  *baseline* — what the agent does **every** turn, before anything else.
- **It can be minimal.** "Check for relevant skills before acting each turn" is a core loop. "Think about
  domain X each turn" is a core loop. It is simply *the way the agent is told to understand its turns.*
- **Required component of any claude-system / AI OS.** An AI OS = `folder the AI lives in + frontend +
  CORE LOOP + apps on top`. The core loop is the **"loop that makes the place hold together"** — what makes
  a folder *govern* (it runs, not just sits there): it is why a folder is an OS and not just a folder.
  `make-ai-operating-system` always defines it.
- **Example (doc-mirror's core loop):** `bootstrap first when the convo starts · journal as you go · while
  there's work: be in the right flow-stage · use the prompts skill when you need an agent · sleep if idle
  · nothing else` — and you **emit a CoR every turn** that says where in this you are.

**Same primitive, three grains:** `ComboPotentials` (transitions *within a guy*) · harness (sequences
*outputs within a turn*) · **core loop** (primes *across turns*). All the same `transition-map` /
attention-chain primitive, at different grain.

---

## I. Why it terminates in a logic engine (the guarantee stack)

**LLMs ALWAYS flatten the syntaxes and the complexity when you ask them to self-modify.** That
flattening is the **16×** cost and it is **undirectable by LLMs** — you can't prompt your way out of it
— *unless* the structure is built into the guy (the persona layer) **and** guarded externally. So the
levels of AI-agent engineering are a ladder of stronger guarantees:

```
(1) prompt        → make the LLM output structure          (weakest — flattens)
(2) hook          → FORCE the LLM to use the structure
(3) harness        → run / sequence the forced agents
(4) context-eng    → keep context straight + self-organizing  ("how it self-organizes = context engineering")
    guy / persona layer → build the structure IN (CoR-first, booted, closed chain)
    + harnesses / skills / validators → guarantee it externally
    logic ontology engine (SOMA) → the ONLY full guarantee
```

**Why the engine is terminal:** *arbitrary string can never be constrained by anything except abstract
meaning graphs* — "**AMR for everything**" is the right mental image — *plus an actual **mereological
validator that rejects composition from meaning.*** Not only decomposing meaning (AMR breaks it down)
but **rejecting invalid compositions** by meaning. Everything above is partial because the string is
still free underneath; only meaning-graph + mereo-rejection closes it. **This is why Dragonbones means
"pass this to SOMA."**

---

## J. Closure (what a guy IS)

A guy = a **role-putting composition of blocks** `{ CoR (said/symbolic), attn (unsaid/neural), style,
schema }`, **encoded to boot** (symbol table + generation basis + Rules + ComboPotentials + attn),
**bound by a primed tag** (`<GUY>`), **built CoR-first**, of class **C1 / C2 / C3**, run at the **ladder
rung** its binding needs, optionally generated by an **MPS**, sequenced across outputs by a **harness**,
its turns primed by a **core loop** (the resident attention chain its per-turn CoR activates), and
**guaranteed by the stack down to the ontology engine**. Every grain is the same
`compiler → compiler-compiler → transition-map` symmetry; primed tokens are the binding handle at every
grain. `persona ⊂ prompt`.

---

*(Deeper layer, flagged for later: when `prompt` is a first-class type in the engine, each block-type,
the closed-chain condition, and the `<GUY>` boot become **admissibility checks SOMA validates on emit**
— the guy's composition proven role-configured the same way an EWS is proven to close. Base = this typed
block algebra + encoding + classes + ladder; engine-validation is the future addition on top.)*
