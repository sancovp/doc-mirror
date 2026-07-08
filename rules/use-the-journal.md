# Use The Journal — the dated thinklog (always-on; when to use each syntax)

The journal is the THINKLOG — the dated record of what you THOUGHT/DECIDED. It is DISTINCT from git log
(the changelog of what CHANGED) and from vision(m)/doc(m) (the durable layer it PROJECTS into). You write
to it continuously, with one command. This is always-on behavior, not a skill you equip.

## The command

The CANONICAL form of a queryable entry carries its TRIANGULATION COORDINATES:

`journal -t <TYPE> --domain <D> --subdomain <SD> --tags <a,b> [--repo <name|path>] "<msg>"`

- **`--domain` / `--subdomain` are REQUIRED on every queryable (vision-projecting) entry** — they are the
  CONCEPT axis (entry `PART_OF` subdomain `PART_OF` domain). Crossed with the repo (code axis) and the
  tags (hyperedge cross-links), they let a lookup TRIANGULATE what the entry IS. They are Title_Cased on
  write; **neither may equal the repo, and they may not equal each other.**
- It appends `{datetime.now()}  <TYPE>: <msg>` to the ACTIVE repo's `context/journal/YYYY-MM.md` AND a
  `[repo]`-tagged line to the GLOBAL index (`$DOCMIRROR_JOURNAL_DIR/YYYY-MM.md`); projects vision-types into
  the vision layer; and dual-writes TWO CartON nodes — a timestamped TIMELINE entry
  `{Repo}_{Domain}_{Subdomain}_{ts}` (per-event, append-only log) AND a LIVING COHERED NOTE
  `{Repo}_{Domain}_{Subdomain}` (no ts) that merge-appends every entry with a `⟐════` provenance
  separator, so the CURRENT DECIDED STATE of a topic is ONE node (`docmirror-read state <subdomain>`).
- `journal -g "<msg>"` — a pure cross-cutting thought: GLOBAL index only, tagged `[global]`. The ONLY form
  EXEMPT from domain/subdomain (it is not a triangulated entry). Use for system-level notes not about one repo.
- `journal --where` — print the target paths (don't guess where it writes).

## TYPES — two levels: PROJECTION type (where it goes) + VISION FLAVOR (what kind)

`-t TYPE` has two levels. The PROJECTION type is WHERE the line projects. VISION has FLAVORS under it.

**PROJECTION types (the mechanic — where it goes):**
- **`VISION`** → projects to `vision(m)` (`docs/vision/<relpath>.md`): any idea/decision about code not
  built. The dominant case — most lines are VISION, usually via a flavor below.
- **`COMMIT`** → the commit body. Usually you DON'T tag this — `doc-mirror-commit` rolls up your journal
  lines since the last commit automatically. Tag only to mark a line as commit-bound narration.
- (a bug is just a FINDING/VISION note — there is NO BUG→issue projector; we don't use one.)

Every VISION entry carries `tags:[modules, repos, concepts]` = the hyperedge. RESOLVE it with the
`vision` CLI: `vision <tag>` (every entry tagged X across all repos) or `vision --tags` (the index).

**VISION FLAVORS (sub-types of VISION — each implies projection → vision(m)):**
- **`-t INTENT`** — START of a session/chunk: what you're about to do + why. ("INTENT: build LINK 1 …")
- **`-t DECISION`** — the MOMENT you make/receive a decision: the choice + WHY + alternatives rejected.
- **`-t OPEN`** — a fork you CANNOT resolve (architecture / irreversible / needs Isaac). Write it, then IDLE
  (`docmirror-sleep`) — the sleep echoes the OPEN back to Isaac. NEVER auto-decide an OPEN. (a question you
  CAN answer is not an OPEN.)
- **`-t FINDING`** — a discovered fact (read code / ran a probe); especially a CORRECTION of a prior wrong claim.
- **`-t HYPOTHESIS`** — a guess you're testing; journal again when confirmed/rejected (rejected → its own line).
- **no `-t`** — a plain thinking note (still a VISION-layer thought, just unflavored).

## WHEN to journal (the triggers — do it the moment it happens, never batch)

Set an intent · make/receive a decision · hit an unclear fork · discover a fact or correct a wrong one ·
reject a hypothesis · update a vision file · finish a build step. If you thought it and didn't journal it,
it evaporates. The cost is one `>>` line — pay it every time.

## How it PROJECTS (the journal is not terminal)

- DECISION/idea about module m → its `vision(m)` (`docs/vision/<relpath>.md`); when BUILT → moves to `doc(m)`.
- On a code change: `doc-mirror-commit` ROLLS UP the journal lines since the last commit into the commit body
  (you write the why ONCE in the journal; it projects to the changelog). The commit must also cite its ORIGIN
  (a vision it realizes / a bug it fixes) or it is refused.
- (BUG → GitHub issue projection is designed but not built yet; for now a `journal -t FINDING`/note suffices.)

## The STATE MACHINE — status:open/done; tasks on CartON (doc-mirror IS a state machine, not a log)

Every journal node (timeline entry + cohered note) is born `status: 'open'` (a scratch-lane property the
system sets). The read layer (`docmirror-read` + the DMN skill) surfaces ONLY `status<>'done'` — so the
moment a thread's work LANDS, you retire its journals and they are NEVER rehydrated again. Information has
a state; the system tracks it; you control it. The two CLIs:

- **`docmirror-done --subdomain <SD> [--repo <R>]`** (also `--domain`/`--tag`/`--entry`) — the STRIKE-ON-BUILD
  actuator. Run it the moment a thread/subdomain's work is built + verified: it flips every matching entry +
  the cohered note to `status:'done'`. `--dry-run` previews; `--reopen` undoes. Re-journaling that coordinate
  re-opens it (new activity = live again). **Do this as you finish work** — a thread left un-done-marked is
  the bug that makes a future you re-pull settled work and re-ask "is X done?".
- **`docmirror-task add "<text>"` / `list` / `start <#>` / `done <#>`** — the per-session TASK LIST, on CartON,
  in the doc-mirror graph (`Doc_Mirror_Task` nodes PART_OF a session node + the repo). **We do NOT use Claude
  Code task lists (TaskCreate/TaskList) — ever.** Tasks live here so they are queryable, survive, and obey the
  same open/done state machine. `list` shows OPEN; `list --all` includes done.

## The hard distinction (never collapse these)
- **journal** = what you THOUGHT (thinklog). **git log** = what CHANGED (changelog). **vision(m)** = ideas not
  yet built. **doc(m)** = what the code IS. The journal feeds the others; it does not replace any of them.
