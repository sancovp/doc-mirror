# Think In Braids — Solution Formation Is Staging Staged Processes — NON-NEGOTIABLE

## The principle (Isaac, verbatim)

ALWAYS think from a braiding nonlinear perspective of problem solving: **solution formation is
itself a staged process of staging staged processes.**

We will encounter a lot of situations where normal linear thinking cannot solve them and will
make them increasingly hard. The default move — "see the problem, do the obvious step, then the
next" — fails whenever the steps have hidden dependencies on each other, because doing an
"obvious" step first can destroy what a later step needs. **Proactively assume problems are
braided (steps depend on steps) until proven linear**, not the reverse. Assume the braid; earn
the line.

## What braiding means

A braid is a partial order of moves, not a line. Solving = FIRST discovering that order (which
move enables which, which move destroys what another needs), THEN walking it. And discovering the
order is itself a staged process — you stage the work of figuring out how to stage the work.
There is no single flat list; there is a **stage-DAG**, and producing the stage-DAG is the first
stage.

So three levels are always in play:
1. the moves that solve the problem,
2. the **staging** that orders those moves (the braid: what precedes what, what destroys what),
3. the **process that produces that staging** (read/classify/map the dependencies → emit the
   stage-DAG).

Going straight at level 1 in whatever order is convenient — skipping levels 2 and 3 — IS the
linear failure.

## The canonical instance (replace-before-remove)

Cleaning up disconnected/garbage artifacts in a system: the linear move is "delete the garbage."
But the garbage often ENCODES the spec of what is supposed to replace it — so deleting it first
destroys the only written statement of what you're about to build toward. The braided solution:
build the real replacement, THEN remove the now-redundant artifact. And figuring out
which-removal-waits-on-which-build is itself the audit's job — a staged process whose output is
the staging. "Clean up the garbage" is therefore not a step; it is a stage-DAG. The recurring
ordering rule that falls out: **replace before remove** (and its siblings: build-the-target
before the thing that targets it; ground before you build on).

## How to apply

- **The tell you're in a braided problem, not a linear one:** the obvious next step makes the
  whole thing HARDER; you keep "fixing" and the symptom moves rather than shrinks; each step seems
  to undo a previous gain. The moment you feel this — STOP attacking linearly.
- **When you see it:** do not prescribe the first move. First produce the braid — map which moves
  depend on / destroy which, emit the stage-DAG (the ordered partial order), and recognize
  explicitly that producing it is itself a staged process worth doing as its own stage.
- **Front-load the cheap work (mapping the order) before the expensive work (acting)** so every
  action lands in an order that cannot undo itself.
- Composes with `trace-bug-chain-to-exact-symptom`: tracing the exact chain IS the level-3 process
  that reveals the braid. Composes with the doc-mirror staging (TYPE before DO): typing the
  structure IS producing the stage-DAG before executing it.

## Why

Linear attack on a braided problem is the single most expensive failure mode: each "obvious" step
that violates a hidden dependency destroys a later step's ground, so you pay twice — to undo it
AND to rediscover why it broke — and the problem gets harder with every push. Treating solution
formation as staging staged processes front-loads the ordering work before any action, so nothing
you do undoes something you already did. The braid is not overhead; it is the solution's actual
shape.
