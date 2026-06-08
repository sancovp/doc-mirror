# Claude-System Diagram Set — the canonical first-read map

A **claude system** = the context-part of an agent program: the agent's operating program (session-start
/ turn / session-end / memory / skill+rule creation / work-tracking / run-mode) authored as markdown the
agent reads, in a directory environment. (doc-mirror is one instance; not all systems produce artifacts.)

Every NON-TRIVIAL claude system MUST carry a single `SYSTEM.md` in its root directory. It is the FIRST thing
the agent reads when working in that system — visual orientation before any prose.

**Non-trivial** = more than one directory level OR more than one legal file kind. A trivial system
(single directory, single file kind — e.g. one `CLAUDE.md`) inlines an abbreviated version of the
four diagrams in its `CLAUDE.md` instead of a separate file. The diagrams are still required; only
their housing differs.

## The file
- Path: `<system-root>/SYSTEM.md`
- Pure ASCII (no rendered images — it must read inline as context).
- Braced top and bottom with: `===ONLY EDIT IF SYSTEM CHANGES===`
  → It is fork-on-system-change: invariant unless the system's actual structure changes, exactly
  like a doc(m) is invariant unless its module changes. Do NOT edit it for session notes.

## The four canonical diagrams (all four, in this order, every system)
1. **LAYER** — the static structure: the layers/components and how they stack. "What it IS."
2. **FLOW** — the runtime cycle: the loop over time (e.g. turn → act → commit → compact → rehydrate).
   "How it RUNS."
3. **GEOMETRY** — the file tree + how navigation nests (root → leaf → leaf-of-leaf). "WHERE things
   live and how you descend."
4. **LIFECYCLE** — the state machine of the system's core artifact or the agent (states + transitions).
   "The states and how they change."

## How it's made / maintained
- Produced by the `make-ai-operating-system` skill when a new system is designed.
- Re-derived (forked) only when the system's structure changes — then re-render the affected diagram
  and bump nothing else.
- The work-loop prompt reads `SYSTEM.md` FIRST, then the root progress-tracker, then descends.

If a non-trivial claude system has no `SYSTEM.md` (and a trivial one has no inline diagram map), it is
not yet a well-formed system of this class — generate the diagrams.
