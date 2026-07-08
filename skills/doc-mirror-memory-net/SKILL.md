---
name: doc-mirror-memory-net
description: "WHAT: REHYDRATE by querying the CartON journal/vision graph (ready-to-run Cypher) instead of re-reading flat files -- where-am-i, what-was-decided-about-X, what-spans-repos, concept-neighborhood. WHEN: rehydrating at session start or post-compact (run right AFTER doc-mirror-boot); recalling what was decided/found about a repo/domain/subdomain/tag; any 'where am I / what is related to X' lookup."
---

# doc-mirror-memory-net (DMN) — rehydrate by QUERYING the graph, not re-reading files

**The journal/vision is already a live, self-describing graph in CartON.** Every `journal` entry is a node;
its kind, repo, domain/subdomain, and tags are typed edges. So you do NOT rehydrate by scanning flat
`context/journal/*.md` files (the "re-read everything" context-blast the system prompt warns against) —
you **query the net for exactly the slice you need** (progressive disclosure). DMN is the *agent-facing*
front of the read layer; the *system-facing* twin is the `docmirror-read` CLI (same lookups, same Cypher).

Engine: the **`query_wiki_graph` MCP tool** (`mcp__carton__query_wiki_graph`) — read-only, must target
`:Wiki`. An agent CAN call it (a shell CLI cannot — that's why `docmirror-read` exists for the system side).

## ⛔ STEP 0 — NEVER START FROM THE COMPACTION SUMMARY. REHYDRATE FIRST, ALWAYS.

The compaction summary, a `<system-reminder>`, the cursor `pathway`, or "the last task said X" is a
**LOSSY POINTER, never the rehydration.** It exists ONLY to give you the SEED — the active
`<Repo_Title_Case>` + subdomain to feed the queries below. You may **NOT** start a task, write a prompt,
design anything, or touch a file from it. **Trusting the summary IS the cardinal failure** — it makes you
"continue" work you never actually rehydrated, building on a decohered picture (this exact failure: a
summary said "next: fix mereo-C", the agent fixed it without reading the store/JIT sprint it depended on,
and spiralled). The summary tells you WHERE to start querying; the JOURNAL tells you WHAT IS TRUE.
Re-derive everything below before acting — every session, every post-compact, no exceptions.

## ⛔ THE REHYDRATION ALGORITHM — run these steps EXACTLY, in order, before ANY work

This is MECHANICAL, not a judgment call. Do not improvise it. Do not sample. Do it every time.

### STEP 1 — pull THE LAST CONVERSATION'S complete journal set (conversation 0), via the convo_start marker
The boundary is **EXPLICITLY MARKED**, not guessed: the first journal of every conversation carries a
`convo_start: true` property (set by `journal --convo-start`). Pull **THE LAST conversation (conversation 0
— the most recent one)**: every entry since the most recent `convo_start` marker, **COMPLETE, NO
TRUNCATION, NO `status`/done FILTER** (you read DONE entries too — done work is part of what happened in
THIS conversation):

```cypher
// pass {"n": 0} — the LAST (current) conversation. (n=1 is the prior one, only if a term forces you back.)
MATCH (b:Wiki)-[:INSTANTIATES]->(:Wiki {n:'Doc_Mirror_Journal_Entry'})
WHERE b.convo_start = true
WITH b.t AS bt ORDER BY b.t DESC
WITH collect(bt) AS bounds
WITH bounds,
     CASE WHEN size(bounds) > $n THEN bounds[$n] ELSE datetime('1970-01-01T00:00:00') END AS lo,
     CASE WHEN $n = 0 THEN datetime('9999-12-31T00:00:00')
          WHEN size(bounds) >= $n THEN bounds[$n-1]
          ELSE datetime('9999-12-31T00:00:00') END AS hi
MATCH (e:Wiki)-[:INSTANTIATES]->(:Wiki {n:'Doc_Mirror_Journal_Entry'})
WHERE e.t >= lo AND e.t < hi
RETURN e.n AS entry, e.d AS full_text, toString(e.t) AS ts ORDER BY e.t
```
Or the CLI twin (prints each entry in full): **`docmirror-read conversation 0`**. **COUNT** the entries; read
EVERY one IN FULL. This is the LAST conversation — the **ENTRY POINT**. The last journal NAMES what to
continue. **You do NOT then read conversation 1, 2, 3 in full** — that is a circular whole-history read that
never converges. To understand the ORIGIN of a TERM the last conversation uses, you go to STEP 3 and
**QUERY/SEARCH the journals for that specific term, backward to its first mention** — recursive *per term*,
not per *conversation*.

> **If conversation 0 returns the WHOLE history (no `convo_start` markers exist yet):** the markers are
> new — mark the most recent conversation's first entry by hand
> (`set_properties <first-entry> {convo_start:true}`), and ALWAYS `journal --convo-start` your first entry
> each conversation from now on (the self_compact prompt + STEP 5 instruct it).

### STEP 2 — READ all of STEP 1's entries IN FULL (the merged cohered state of every subdomain they touch)
For each DISTINCT subdomain appearing in STEP 1, pull its LIVING COHERED NOTE in FULL — `RETURN c.d`,
NEVER `substring`:
```cypher
MATCH (c:Wiki)-[:IS_A]->(:Wiki {n:'Doc_Mirror_Cohered_Note'})
WHERE c.n CONTAINS '<Subdomain_Title_Case>'  RETURN c.n, c.d
```
Large results OVERFLOW to a file — **READ THE ENTIRE OVERFLOW FILE, every line.** No skipping, no "this
one looks less relevant," no stopping at the names you recognize.

### STEP 3 — RECURSIVELY RESOLVE every OPEN reference you do not FULLY understand (this reaches BACKWARD)
The last conversation is the ENTRY POINT; the RECURSION is what makes the rehydration COMPLETE. For EVERY
item still OPEN/undone, and EVERY reference inside STEP-1/STEP-2 text you cannot explain EXACTLY, pull it
and read it IN FULL:
- a **concept** → `get_concept` / its cohered note;
- a **PRIOR subdomain/domain** the entry points back to (e.g. the last convo builds on the
  conversation-before-last) → that subdomain's cohered note (`#8 state`) + its STEP-1-style entry list.
  **THIS is how you correctly reach earlier conversations** — by following the open references, not by
  querying 4 days of everything blindly;
- a **claim about WHAT CODE DOES** → go **READ THE CODE** (`check-code-not-markdown`). A journal/doc/skill
  line ("X rejects Y", "Z is disabled", "the store loads N facts") is a POINTER to VERIFY against source,
  NEVER a fact to propagate. Resolve it to `file:line` or do not rely on it.

Repeat — each resolved item exposes new references — UNTIL nothing open is unresolved. A vision/decision =
the recursive grouping of everything ever said about that thing; make your understanding REFLECT the
DECIDED state.

### STEP 4 — COUNT-CHECK, then act
State how many entries STEP 1 returned and confirm you read THAT EXACT NUMBER in full, plus every cohered
note and every recursively-resolved reference. Read fewer than exist → you are NOT rehydrated → go back.

**It does not matter if this fills the ENTIRE context window — it is supposed to.** You CANNOT "jump in."
Partial rehydration silently DECOHERES everything the prior session decided and **wastes the entire prior
session's work** — the single worst, most expensive failure there is. Reading 18 of 30 notes is a FAILURE
identical to reading 0. PREVENT YOURSELF from ever starting work on a partial read.

### STEP 5 — UNLOCK: run `docmirror-rehydrated` (only after STEP 1–4 are genuinely complete) to write the
rehydration flag and re-enable all tools. Do NOT run it early — it is the gate. A NEW conversation starts
LOCKED: the SessionStart boundary hook (`docmirror_session_boundary.py`) marks rehydration required, and
the PreToolUse rehydration gate (`docmirror_rehydration_gate.py`) BLOCKS every work-tool (Edit/Write/Task/
non-read Bash) until you unlock — only carton queries + Read + rehydration-read Bash are allowed while
locked. So the ONLY way out is to actually do STEP 1–4 and then run `docmirror-rehydrated` (optionally
`docmirror-rehydrated <N>` to record the entry count from STEP 4). Running it before you have genuinely
rehydrated is lying to the gate and defeats the entire system.

**THEN MARK THIS CONVERSATION'S BOUNDARY (mandatory, do it once, right after unlocking):** your VERY FIRST
journal entry of this conversation MUST be written with `journal --convo-start` — it stamps
`convo_start: true` on that entry, marking where THIS post-compaction conversation begins so the NEXT
rehydration's STEP 1 can pull it in one query. If you have already journaled this conversation without the
flag, mark that first entry by hand: `set_properties <that-entry-node> {convo_start: true}` (merge). Without
this marker the graph cannot delimit your conversation and the next lifetime falls back to a whole-history
read. One marker per conversation — never mark more than the first entry.

## ⛔ THE STATE MACHINE — every entry has a `status` (open/done); DONE work is NEVER surfaced again

Information has a STATE and doc-mirror TRACKS it. Every journal node (timeline entry + cohered note) is
born `status: 'open'` (a scratch-lane property the system sets, per `journal`). **EVERY query in this skill
carries `WHERE coalesce(<node>.status,'open') <> 'done'`** — so the moment a thread's work LANDS and you
mark it done, it disappears from rehydration permanently. This is why you no longer re-pull finished work
and re-ask "is X done?" — the graph knows X is done.

- **Marking a finished thread done (the actuator):** when a subdomain/domain/tag's work is BUILT + verified,
  run `docmirror-done --subdomain <Subdomain> [--repo <R>]` (or `--domain` / `--tag` / `--entry`). It flips
  every matching entry + the cohered note to `status:'done'` (synchronous). They are now retired from
  STEP 1, #1/#3/#4/#7/#8 — never rehydrated again. `--dry-run` previews; `--reopen` undoes.
- **Re-opening is automatic on new activity:** journaling again at that coordinate stamps `status:'open'`,
  so a topic with genuinely-new undone work comes back into the current-state view.
- **DO THIS as you finish work** (the seework/change leg): close out the thread you completed BEFORE you
  rehydrate the next one, so the next rehydration shows only what is truly still open. A thread left
  un-done-marked is the bug that makes a future you re-pull settled work — close it.
- **The ONLY way to see done work** (audit / history) is to query WITHOUT the filter, or read the literal
  journal file. Rehydration deliberately hides it.

### SOPHIA does the bulk done/open classification automatically — you do the POST-REHYDRATION reconciliation
**SOPHIA** (the chronological rollup worker) reads the journal oldest-first and classifies each thread:
DONE → a Sophia node + entries `status:done` (auto-retired); OUTSTANDING → entries `sophia_checked` (she
saw them; genuinely open). She auto-closes a thread later only when **connected NEW work lands on its
coordinate** (you journal more there → re-classified). That leaves a TAIL: a thread that is actually-done
but was never re-journaled stays falsely `sophia_checked`-open forever. **The cure is a required step right
after you rehydrate, BEFORE you pick the next work:**

1. **Surface the reconcilable backlog:** `docmirror-read outstanding` (or DMN **#9** below) = the
   `sophia_checked`-and-open threads SOPHIA confirmed outstanding.
2. **Reconcile it:** for each, decide *is this actually still outstanding, or done-but-never-closed?* Close
   the actually-done with `docmirror-done --subdomain <S>` (or `--domain`/`--tag` for a whole shipped
   family — the safe manual family-close). Keep the genuinely-open.
3. **THEN pick the next gap** from the (now honest) outstanding set.

This is `keep-the-rollup-current`'s "mark off the done ones" made an explicit reconciliation step: SOPHIA
automates the chronological pass; you curate the tail at the post-rehydration moment so false-opens die on
sight instead of accumulating.

## REHYDRATION IS RECURSIVE — the mechanics of the mandate above

**DMN is NOT "locate the single latest entry."** That is the failure that destroys work — a thin peek
then freestyling a design from it. To rehydrate you **recursively retrieve everything about your thing,
read it in full, and prove to yourself you have it all BEFORE you act**:

1. **Figure out WHAT you are working on** (the feature / goal — a goal is *multiple visions* to implement).
2. **CHECK what exists** about it: `tree` → its domain; `tree --domain D` → its subdomains; then for the
   relevant subdomain(s) use #3 (by subdomain/tag) and #6 (neighborhood) to see the full set.
3. **RETRIEVE THE ENTIRE SET, FULL TEXT.** Return `e.d` in FULL (not `substring(...)`), oldest→newest. A
   large result is written to an overflow file — **READ THE ENTIRE OVERFLOW FILE.** Read every entry.
4. **KEEP GOING — call it again and again**, following `related_to` / `part_of` to adjacent
   subdomains/tags, retrieving more, **UNTIL the entries STOP being about the thing you are working on.**
   Call it a hundred times if that is what it takes. You do not stop at the first slice.
5. **PROVE to yourself you have contextualized everything** about the feature. Only then act.

**A VISION = everything you have ever said about updating that exact feature = the RECURSIVE GROUPING of
every entry related to it** (its subdomain + the related_to web). The decisions were ALREADY MADE on the
journal. Your job: retrieve that whole grouping → make the vision **REFLECT the decisions made** → and
ONLY ONCE the vision reflects only the decided state, **implement**. **NEVER freestyle from a partial
read** — if you do not know the decision EXACTLY/verbatim, you have not retrieved enough; retrieve more.

(The lookups below are the TOOLS for steps 2–4. `locate` (#1) only tells you the latest single entry —
it is a starting pointer, NEVER the rehydration itself.)

## The schema (what the net is made of)
Each journal entry node is a COORDINATE ADDRESS, written by `journal`:
- name = `{Repo}_{Domain}_{Subdomain}_{ts}` ; `INSTANTIATES Doc_Mirror_Journal_Entry`
- `IS_A Doc_Mirror_Journal_{Type}` — the KIND (Finding / Decision / Intent / Vision / Open / Hypothesis / Note)
- `PART_OF [{Repo}, {Subdomain}]` ; `{Subdomain} PART_OF {Domain}` — the triangulation axes
- `RELATED_TO {Tag}` — the hyperedge cross-links
- **typed axis nodes**: `{Repo} IS_A Doc_Mirror_Repo` · `{Domain} IS_A Doc_Mirror_Domain` ·
  `{Subdomain} IS_A Doc_Mirror_Subdomain` (these make the boundaries STRUCTURAL — lookups key on them)

**TWO LAYERS per event (minimal-A 2026-06-09):** besides the timestamped TIMELINE entry above (per-event,
append-only, the thread), `journal` ALSO maintains a **LIVING COHERED NOTE** per topic: a node named
`{Repo}_{Domain}_{Subdomain}` (NO timestamp) `IS_A Doc_Mirror_Cohered_Note`, `PART_OF [{Repo},{Subdomain}]`,
that **merge-appends every entry** with a pure-glyph `⟐════ ts · KIND ════⟐` provenance separator. So the
**current decided state of a topic is ONE node read** (`#8 state`) instead of synthesizing the flat thread —
this is the anti-thin-rehydration / anti-double-up fix. (The append note is additive; SOPHIA — LIVE — writes
a separate `Doc_Mirror_Sophia_Note` for a DONE thread that `#8 state` JIT-prefers.) **Rehydrate via `#8
state` FIRST** (one query), drill the timeline only if needed.

**Normalization (critical):** every name is `Title_Case_With_Underscores`. A tag `read-layer` is the node
`Read_Layer`; `step-a` → `Step_A`. Title_Case your selector or the query silently returns nothing.

## The lookups (paste the Cypher into `mcp__carton__query_wiki_graph`)

**#1 locate — where am I? (graph-derived; replaces eyeballing a flat cursor)**
```cypher
MATCH (e:Wiki)-[:INSTANTIATES]->(:Wiki {n:'Doc_Mirror_Journal_Entry'})
WHERE coalesce(e.status,'open') <> 'done'
WITH e ORDER BY e.t DESC LIMIT 1
OPTIONAL MATCH (e)-[:PART_OF]->(r:Wiki)-[:IS_A]->(:Wiki {n:'Doc_Mirror_Repo'})
OPTIONAL MATCH (e)-[:PART_OF]->(sd:Wiki)-[:IS_A]->(:Wiki {n:'Doc_Mirror_Subdomain'})
OPTIONAL MATCH (sd)-[:PART_OF]->(d:Wiki)-[:IS_A]->(:Wiki {n:'Doc_Mirror_Domain'})
RETURN e.n AS latest_entry, toString(e.t) AS ts, r.n AS repo, d.n AS domain, sd.n AS subdomain
```

**#3 vision-by-coordinate — what was said about X?** (by tag; swap the predicate for subdomain/domain)
```cypher
// by TAG (Title_Cased!).  The `WHERE coalesce(e.status,'open') <> 'done'` is the STATE-MACHINE filter —
// keep it on EVERY rehydration query so DONE threads are never pulled (the cure for serving done-as-live):
MATCH (e:Wiki)-[:RELATED_TO]->(:Wiki {n:'Read_Layer'})
WHERE coalesce(e.status,'open') <> 'done'
RETURN e.n AS entry, substring(e.d,0,180) AS preview, toString(e.t) AS ts ORDER BY e.t DESC LIMIT 15
// by SUBDOMAIN:  MATCH (e:Wiki)-[:PART_OF]->(:Wiki {n:'Read_Layer_Build'})-[:IS_A]->(:Wiki {n:'Doc_Mirror_Subdomain'}) WHERE coalesce(e.status,'open')<>'done' ...
// by DOMAIN:     MATCH (e:Wiki)-[:PART_OF]->(:Wiki)-[:PART_OF]->(:Wiki {n:'Doc_Mirror_Read_Layer'})-[:IS_A]->(:Wiki {n:'Doc_Mirror_Domain'}) ...
```

**#4 cross-pollination — what ideas span ≥2 repos?** (the emergent hyperedges flat files can't find)
```cypher
MATCH (e:Wiki)-[:PART_OF|RELATED_TO*1..3]->(r:Wiki)-[:IS_A]->(:Wiki {n:'Doc_Mirror_Repo'})
WHERE coalesce(e.status,'open') <> 'done'
WITH e, collect(DISTINCT r.n) AS repos WHERE size(repos) >= 2
RETURN e.n AS entry, repos, substring(e.d,0,120) AS preview ORDER BY size(repos) DESC LIMIT 25
```

**#6 fuzzy-mereo — the neighborhood of a concept** (pass `{"c": "Doc_Mirror_Read_Layer"}` as parameters)
```cypher
MATCH p=(c:Wiki {n:$c})-[*1..2]-(m:Wiki)
RETURN DISTINCT m.n AS node, min(length(p)) AS hops ORDER BY hops, node LIMIT 40
```

**#7 tree — the HIERARCHY (use THIS to see "everything we know, organized"; NEVER `ls` the flat
`docs/vision/_*.md` files — the graph IS the tree). System-facing twin: `docmirror-read tree`.**
```cypher
// the whole hierarchy: domain → subdomain → entry-count
MATCH (e:Wiki)-[:INSTANTIATES]->(:Wiki {n:'Doc_Mirror_Journal_Entry'})
WHERE coalesce(e.status,'open') <> 'done'
MATCH (e)-[:PART_OF]->(sd:Wiki)-[:IS_A]->(:Wiki {n:'Doc_Mirror_Subdomain'})
MATCH (sd)-[:PART_OF]->(d:Wiki)-[:IS_A]->(:Wiki {n:'Doc_Mirror_Domain'})
RETURN d.n AS domain, sd.n AS subdomain, count(DISTINCT e) AS entries ORDER BY domain, subdomain
// scope to a repo (code axis): add  MATCH (e)-[:PART_OF]->(:Wiki {n:'Scalable_Publishing'})  after line 1
// drill a domain → its entries:
//   MATCH (e:Wiki)-[:PART_OF]->(sd:Wiki)-[:PART_OF]->(:Wiki {n:'Gnosys'})-[:IS_A]->(:Wiki {n:'Doc_Mirror_Domain'})
//   RETURN sd.n AS subdomain, e.n AS entry, toString(e.t) AS ts ORDER BY sd.n, e.t DESC
```

**#8 state — the LIVING COHERED NOTE = current decided state of a topic in ONE query (rehydrate with THIS
first).** System-facing twin: `docmirror-read state <subdomain>`.
```cypher
// JIT-prefers SOPHIA's cohered current-state node (Doc_Mirror_Sophia_Note) if she made one, else the
// append cohered note. Done topics are retired (state machine). The type is the signal — you just ask
// for the topic state and transparently get SOPHIA's coherence when it exists:
MATCH (c:Wiki)-[:PART_OF]->(:Wiki {n:'Journal_Merge_By_Coordinate'})   // <- the topic subdomain (Title_Cased)
MATCH (c)-[:IS_A]->(t:Wiki)
WHERE t.n IN ['Doc_Mirror_Sophia_Note','Doc_Mirror_Cohered_Note'] AND coalesce(c.status,'open') <> 'done'
WITH c, t.n AS kind, CASE t.n WHEN 'Doc_Mirror_Sophia_Note' THEN 0 ELSE 1 END AS pref
RETURN c.n AS node, kind, c.d AS state ORDER BY pref LIMIT 1
```

**#9 outstanding — the SOPHIA-confirmed RECONCILABLE BACKLOG (run this right after rehydrating, then
reconcile per the post-rehydration step above).** System-facing twin: `docmirror-read outstanding`.
```cypher
MATCH (e:Wiki)-[:INSTANTIATES]->(:Wiki {n:'Doc_Mirror_Journal_Entry'})
WHERE coalesce(e.status,'open') <> 'done' AND e.sophia_checked = true
MATCH (e)-[:PART_OF]->(sd:Wiki)-[:IS_A]->(:Wiki {n:'Doc_Mirror_Subdomain'})
OPTIONAL MATCH (sd)-[:PART_OF]->(d:Wiki)-[:IS_A]->(:Wiki {n:'Doc_Mirror_Domain'})
RETURN d.n AS domain, sd.n AS subdomain, count(e) AS open_entries, toString(max(e.t)) AS newest
ORDER BY newest DESC LIMIT 60
```
For each row, decide done-vs-still-open; `docmirror-done` the actually-done (or `--domain`/`--tag` a shipped
family); the rest is your true live backlog.

**#2 active-leaf** (what's the next ACTIVE thing to work on) and **#5 closure** (file↔doc(m) bijection) are
NOT yet wired: #2 awaits the tracker-as-derived-view rebuild (status in the graph); #5 awaits CA `:File`/
`doc(m)` nodes. For "what exists / where is everything" use **#7 tree**; for "the current decided state of a
topic" use **#8 state**; for "what am I on" use `locate` (#1).

## Self-describing introspection (so this skill never goes stale — ask the graph what exists)
```cypher
// kinds + counts (verified via query_wiki_graph: Finding/Decision/Intent/Vision/Hypothesis):
MATCH (e:Wiki)-[:INSTANTIATES]->(:Wiki {n:'Doc_Mirror_Journal_Entry'})
MATCH (e)-[:IS_A]->(k:Wiki) WHERE k.n STARTS WITH 'Doc_Mirror_Journal_'
RETURN k.n AS kind, count(e) AS n ORDER BY n DESC
// repos:     MATCH (r:Wiki)-[:IS_A]->(:Wiki {n:'Doc_Mirror_Repo'})      RETURN r.n ORDER BY r.n
// domains:   MATCH (d:Wiki)-[:IS_A]->(:Wiki {n:'Doc_Mirror_Domain'})    RETURN d.n ORDER BY d.n
// subdomains:MATCH (s:Wiki)-[:IS_A]->(:Wiki {n:'Doc_Mirror_Subdomain'}) RETURN s.n ORDER BY s.n
```

## How to use it
- **Rehydrating / post-compact:** run `locate` (#1) → then `vision-by-coordinate` (#3) on the active
  subdomain to pull the recent decisions/findings for THIS thread — instead of reading the whole journal.
  Composes with `verify-rehydration-before-compact` (rehydrate by querying the net, not scanning files).
- **"What did we decide about X?"** → #3 by tag/subdomain. **"What touches two repos?"** → #4. **"What's
  near this concept?"** → #6. **"What kinds/domains exist?"** → introspection.
- Coverage note: typed-axis lookups (#1/#3-subdomain/#4) cover entries journaled SINCE the typed-axis-node
  emission landed (read-layer step a). Older entries have untyped axis nodes — `--tag`/`related_to` (#3)
  and `#6` still reach them; a historical backfill of axis-node types would extend #1/#4 to them.
