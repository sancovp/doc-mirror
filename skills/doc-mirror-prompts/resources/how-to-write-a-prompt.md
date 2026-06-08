# How To Write A Prompt

**The core idea: don't explain the thing — hand the LLM a *generative basis* it can collapse to the
invariant and re-expand from.** "Minimum explanation" = the minimal *sufficient basis*, NOT minimal
length. You give `{primitives} + {self-hosting closure} + {one generator→instance ladder} +
{few collapsible templated examples} + {grain hierarchy}`, and the model reconstructs the whole space.

A prompt is organized into **XML sections**; inside each you write in **markdown**. Below: the surface
conventions, then the generative-basis pattern that makes a prompt actually teach.

> **Canonical worked example:** `resources/examples/categorical-state-graph-notation.md` — it embodies
> every point below. Read it; this guide is the distilled pattern, that doc is the pattern realized.

---

## A. Surface conventions

### The canonical order (top → bottom)
```
{required background info}
  → {definitions} + {local shorthands}
  → {expected output format: [sections + def usages | meat]}
  → {graphs/diagrams}
  → {CoR}
```
Each stage is an XML section, markdown inside: `<background>`, `<definitions>`, `<output_format>`,
`<diagrams>`, `<cor>`. (Tag names are conventional — name them for the prompt.)

### Templating = masking / "madlibbing" (ALWAYS)
- `[]` = a **list**. `{}` = a **template** slot; `{{}}` usually works better.
- Inline backticks `` `{xyz}` `` whenever you want to **force the model to say something**:
  *"Your output should be: `{templated stuff}`"*.
- One line → single backticks. Multi-line → triple-fence.

### Speak algebraically; show geometries
LLMs natively grok — so use — **math operators**, `+`/`+=` for **string ops + templates**, and
**nested** parens/brackets/curlies/arrows. **It is always better to speak algebraically and to show
geometries (diagrams) whenever possible.** Algebra = the compressed basis; a diagram = the invariant
made visible.

---

## B. The generative-basis pattern (what makes a prompt *teach*)

A prompt that makes the model generalize hard has these parts, in order:

1. **Meta-first name + class properties** — open by naming what the thing IS at the most meta level
   (the parent class + its properties), before any detail. *(notation doc line 1: "CATEGORICAL STATE
   GRAPH NOTATION — Turing Complete + Category Theory Extension".)*

2. **Primitive basis = algebra ⊕ geometry, fused at the definition layer.** Define the basis set; each
   primitive is `symbol = NAME` + one line + a **templated micro-diagram** showing its use. The symbols
   ARE the local shorthands; every one carries its geometry. e.g.
   ```
   S = STATE     simple node, holds value     [*] --> S ; S --> [*]
   T = TRANS     conditional transition        S1 --> T ; T --> S2: [cond]
   ```

3. **Self-hosting / closure.** Write the thing **in its own notation**, show it operating on itself,
   and state the closure condition + prove it (*"✓ this document is written in its own notation"*). A
   self-hosting prompt meta-compiles on the reader — it teaches itself by being used.

4. **ONE type-ladder worked example — built generator → instance, with a diagram at EVERY rung,
   ending in a grounding collapse.** This is the highest-leverage move. Give it meta-first:
   > the parent class is the most meta, defined like `{parent_def}`. its generator `{parent}-gen`.
   > `{parent}-gen` produces `{some_class}`, which produces `{this_instance}`.
   ```
   {generator} ──produces──▶ {parent_class} ──is_a──▶ {some_class} ──is_a──▶ {this_instance}
   ```
   Build it down the tower with a diagram per level, terminating in a `COLLAPSE[quotient=0]` to
   concrete observables. *(notation doc: Arrhenius/Fick generators → THERMO/KINETICS/FLUID domains →
   L1→L2→L3→L4 tower → the brew instance `18g/288g/95°C/240s`, quotient=0.)* This makes LLMs go nuts
   in the good way — they learn the universal from the build, not from a snippet.

5. **N templated examples that collapse to the invariant.** Give 3–4 (or more), all variable-ized,
   each applying the **same operation to different content**, so the model collapses them to the shared
   universal. *(notation doc: 5 EXT examples, all `surface → EXT-expand → COLLAPSE[observable]`.)*

6. **Explicit grain/level hierarchy.** State the levels (`L0..Ln`) and the rules for which level to
   collapse to, and what "done" means (`quotient=0 ⟺ fully instantiated at that grain`).

7. **Usage + closure list.** When each operator/section fires; close with the property-list of what
   the system IS.

---

## Skeleton (copy this shape)
```
<background> {what the model must know first; name it meta-first} </background>

<definitions>
  `{Sym1}` = {NAME} — {1 line} — {templated micro-diagram}
  shorthand: `{X}` ≡ {longer thing}
</definitions>

<output_format> Your output should be: `[{section_1}, {section_2}, {meat}]` (each uses the defs) </output_format>

<diagrams> {the type ladder generator→instance + the grain hierarchy, as ASCII} </diagrams>

<examples> {3–4 templated examples, same operation / different content → collapse to invariant} </examples>

<cor>
1. {step using `{Sym1}`}
2. {step} → {step}
3. ⟹ {result, COLLAPSE[quotient=0]}
</cor>
```

---

*(Deeper layer, flagged for later: prompt-languages / English-as-Algebra — programming syntax into
LLMs via sparse priming representation, self-hosting on the model. This guide + the canonical example
are the BASE; that is a future addition on top.)*
