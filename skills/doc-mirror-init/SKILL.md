---
name: doc-mirror-init
description: "WHAT: first-time mirror a codebase that has none (enumerate modules -> write doc(m)=IMPL + vision(m)=VISION -> the 6 context files -> closure test). WHEN: the active repo has NO docs/mirror/ and NO progress-tracker yet (a fresh repo to mirror); reached from seework or boot when the active repo is unmirrored."
---

# doc-mirror-init — the INIT state (first-mirror an unmirrored codebase)

You are in the **init** state of the doc-mirror state machine. This initializes the doc-mirror mirror into a
target dir `<C>`. It is NOT the compiler — to design a *different* system of the doc-mirror class, use
`make-ai-operating-system`. You operate under **THE LAW** (the `doc-mirror` skill: the 4 legal file
kinds, deterministic addressing, the doc(m) template, the closure test). Deep ref:
`doc-mirror-system/{SYSTEM.md, context/architecture.md}` + `DOC_MIRROR_SYSTEM.md`.

## The subgraph (this state's shape)

```mermaid
stateDiagram-v2
    [*] --> S_guard: R — GUARD (already mirrored? docs/mirror + tracker exist -> stop, resume seework/change)
    S_guard --> S_register: `tracker register <C>` (+ `tracker active <C>`) → ROOT REPO ORDER
    S_register --> S_sixfile: create <C>/context/ 6 files
    S_sixfile --> S_enumerate: enumerate modules -> docs/mirror/_MANIFEST.txt
    S_enumerate --> S_docm: team writes doc(m)=IMPL then vision(m)=VISION (templated prompt; via doc-mirror-prompts)
    S_docm --> S_synth: synthesizer writes the 6 context files (navigation, point DOWN)
    S_synth --> S_layers: docmirror-layers + docmirror-system (derive _LAYERS.json + docs/SYSTEM.md)
    S_layers --> CHECK
    state CHECK <<choice>>
    CHECK --> S_done: [closure prints nothing: manifest<->doc(m) biject; every doc(m) has vision(m); 6 ctx; no illegal files]
    CHECK --> S_fix:  [comm -3 prints / a file fails to classify]
    S_fix --> S_docm
    S_done --> [*]: advance cursor -> seework ; journal
```

## What this state is (the procedure)

**GUARD FIRST (idempotent — never double-init).** Check the target dir `<C>`:
```bash
C="<target-dir>"
if [ -f "$C/context/progress-tracker.md" ] && [ -d "$C/docs/mirror" ]; then
  echo "ALREADY MIRRORED at $C — stop. (mirror + tracker exist.)"; exit 0
fi
```
If a partial init exists (tracker but no mirror, or vice-versa), REPORT what's present and resume only
the missing part — do not overwrite existing doc(m) or context files.

**Two altitudes.** The ENVIRONMENT (`~/.claude` strip, the doc-mirror skills+rule, the loop hooks) is
initialized ONCE per machine — guard on the skills + hooks existing; if present, skip (that's one-time machine
setup, see `make-ai-operating-system`). A CODEBASE `<C>` is initialized PER-DIR — the common case:

1. **Guard** (above). If already initialized, stop and resume `seework`/`change`.
2. **Register in the ROOT order** via the CLI (never hand-edit the tracker): `tracker register <C>
   --status NEXT --note "<one-line>"` then `tracker active <C>` — adds/sets `<C>` in the ROOT REPO ORDER
   router table (root = cross-repo order; this lets the machine route to `<C>`).
3. **Six-file context:** create `<C>/context/` with the 6 files (six_file_methodology templates as
   scaffolds; progress-tracker = the queue). Leaf gets its own; root already has one.
4. **Run the doc-mirror procedure** (THE LAW — the `doc-mirror` skill):
   - enumerate modules → `<C>/docs/mirror/_MANIFEST.txt` (the fixed enumerator; record the command).
   - one `doc(m)` per module at `<C>/docs/mirror/<relpath>.md`, then `vision(m)` at
     `<C>/docs/vision/<relpath>.md` — dispatched as a TEAM via `doc-mirror-prompts` (one templated
     prompt, never improvised; imitate any existing hand-written doc(m) as the shape).
   - if a DESIGN mega-vision already exists for this codebase (a `docs/vision/_<topic>.md` written before
     the code), GRADUATE its entries into the new module `vision(m)` BY TAG as each module lands:
     `vision tag <topic> vN +<component>` to label, then `vision graduate <relpath> --from <topic>
     --by-tags <component>` (the design becomes modular as modules are born; lossless, refuses w/o doc(m)).
   - synthesizer writes the 6 context files from the doc(m) set (navigation; point DOWN).
   - `docmirror-layers <C>` then `docmirror-system <C>` → `_LAYERS.json` + `docs/SYSTEM.md`.
   - **closure test** (THE LAW step 6): `comm -3` manifest↔doc-set prints NOTHING; every file classifies.
   - commit as you go with `doc-mirror-commit`.
5. **SYSTEM.md** is for a *system* (the class), not a plain codebase — a leaf codebase does not need one;
   only systems-of-the-class get one.
6. **Done when** the closure test passes and `<C>` is in the ROOT order table.

(Writing the doc(m) team is itself a `prompt` task — when you reach S_docm you transition to
`doc-mirror-prompts` to dispatch the templated team, then return here to synthesize + close.)

## CoR (this state's binding + transition)

Now that I've read `doc-mirror-init`, I will run the init procedure on `{{C}}` — GUARD first (stop if
already initialized), then register → 6 files → enumerate → (transition to `doc-mirror-prompts` to dispatch
the templated doc(m)+vision(m) team, verifying the artifacts myself) → synthesize → layers → **closure
test must print nothing**. When closure passes I `docmirror-cursor set --phase seework`, `journal` the
init, and call `doc-mirror-seework`. If I cannot resolve a fork (which modules count, an irreversible
restructure, anything needing Isaac): I `journal -t OPEN "<fork + why>"`, `docmirror-cursor set --phase
open`, and `docmirror-sleep` — I call no next; I wait.
