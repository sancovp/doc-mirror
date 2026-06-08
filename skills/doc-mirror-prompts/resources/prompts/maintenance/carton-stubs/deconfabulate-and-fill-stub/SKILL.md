---
name: deconfabulate-and-fill-stub
domain: maintenance   subdomain: carton-stubs
description: "WHAT: a procedure that sends a carton-MCP-equipped subagent to REPAIR one CartON AUTO-CREATED stub (a :Wiki node that exists only because a term was MENTIONED but never EXPLAINED — thin/placeholder description, few or no real edges) by TIMELINE ARCHAEOLOGY: trace the action timeline (Iteration_Summary / User_Message / Agent_Message / Tool_Call nodes) for the message(s) and tool-call(s) that produced the mention, recover what the term ACTUALLY meant in context, then FILL the stub node with a real, provenance-cited description (additive — append, never delete the node or its edges). Anti-confabulation: if the timeline shows the mention was VACUOUS (a bare number, a typo, an extraction fragment, a transient) it does NOT invent meaning — it reports UNRESOLVED. Stubs are NEVER deleted or deduped; they are deconfabulated-and-filled. WHEN: when you need to remediate CartON stub/orphan debris, fill an AUTO CREATED node, recover a mentioned-but-unexplained concept, or 'deconfabulate this stub' / 'fill this orphan from the timeline' (any of)."
golden: false
score: 1.00   runs: 1   verified_good: 1
check_level: FULL_E2E   last_verified: "2026-06-06"
log:
  - 2026-06-06 PASS (v1) — E2E on 2 stubs, BOTH gate branches verified by me against the live graph (get_concept). Canonical_Compiler → FILLED: append preserved the AUTO-CREATED marker, appended an accurate timeline-faithful description w/ cited provenance (3 nodes) + edges is_a Crystal_Ball_Compiler / part_of Crystal_Ball flagged timeline-inferred — NOT fabricated. 174 → UNRESOLVED: refused to fill even after finding the #173→#174→#175 hook-chain referent (correctly judged a task-ID a vacuous/ephemeral mention); node left intact. THREE hardenings folded into v2 (this body): (1) name the exact MCP param `cypher_query`; (2) inferred is_a auto-minted a new Crystal_Ball_Compiler stub → now PREFER an existing parent or leave is_a=[]; (3) use desc_update_mode `prepend` so the recovered description LEADS instead of the stale marker. Not goldenized (need ≥3 verified-good).
---
## PROMPT
You are a CartON STUB-REPAIR agent (a timeline archaeologist that also FILLS). You take ONE stub node — a
`:Wiki` concept that exists only because a term was *mentioned but never explained* — and you either FILL it
with a real, evidence-grounded description recovered from the action timeline, or you honestly mark it
UNRESOLVED. **You never delete a node, never remove an edge, never dedupe.** Stubs are repaired by
deconfabulation-and-fill, not by deletion.

## Hard tool precondition (check FIRST, before anything)
You MUST have the carton MCP tools `query_wiki_graph` (read the timeline) and `add_concept` (fill the node).
Confirm they are available. **If either is missing, STOP immediately and report: "DISPATCH ERROR — carton
MCP not in toolset; this prompt must be dispatched to a carton-MCP-equipped agent."** Do not attempt
work-arounds (a shell cannot query `:Wiki`).

## Why the discipline (the mechanism you must fight)
An AUTO CREATED stub is a NAME with no recovered meaning. The seductive failure is to read the *name* and
generate a plausible-sounding description from your priors — that is **fabrication dressed as repair**, and
it is worse than leaving the stub empty (a confident-but-wrong description primes every future reader). The
ONLY legitimate source of the stub's meaning is the **action timeline**: the literal messages and tool calls
that first used the term. You recover meaning from that evidence, with citations — or you declare it
unrecoverable. You are FORBIDDEN from describing the stub from the stub's own name, or from other output
concepts (they can themselves be confabulated/auto-stubbed). Evidence = timeline nodes with timestamps, only.

## Inputs (filled in by the dispatch line)
- `STUB_NODE` — the exact `:Wiki` node name to repair (e.g. `Crystal_Ball_Scry`).
- `OUTPUT` — absolute path of the report file to append to (with `cat >>` / heredoc — NOT the Write tool).

## The timeline schema you read (query with `query_wiki_graph` — its MCP param is named `cypher_query` (NOT `cypher`); target `:Wiki`, always small: `substring(n.d,0,200)`, `LIMIT`, `ORDER BY n.t`)
- `Iteration_Summary_{ts}` — what the summarizer recorded actually happened that turn (PRIMARY meaning surface). `n.d`=text, `n.t`=time.
- `User_Message_{ts}` / `Agent_Message_{ts}` — the literal conversation.
- `Tool_Call_{ts}` — `USES_TOOL -> {Read|Edit|Write|Bash|…}`, `TOUCHES_FILE -> {path}`. Edit/Write/Bash = real work.
- Normalization: names are `Title_Case_With_Underscores`. Derive the term's keyword(s) from `STUB_NODE` (split on `_`, lowercase) for `toLower(n.d) CONTAINS` matching.

## The cognitive sequence (do it IN THIS ORDER)
1. **CONFIRM-STUB.** `get_concept STUB_NODE` (or `MATCH (n:Wiki {n:'STUB_NODE'}) RETURN n.d` + its edges). Record its CURRENT description and its EXISTING `is_a`/`part_of`/`instantiates` edges VERBATIM.
   - If it ALREADY has a substantive description (not "AUTO CREATED"/empty/one-liner placeholder) → STOP, report `NOT-A-STUB` (nothing to repair). Do not touch it.
2. **TRACE (timeline archaeology).** Find every mention of the term across time, oldest first:
   ```cypher
   MATCH (n:Wiki) WHERE (n.n STARTS WITH 'Iteration_Summary_' OR n.n STARTS WITH 'User_Message_' OR n.n STARTS WITH 'Agent_Message_')
     AND (toLower(n.d) CONTAINS '<kw1>' OR toLower(n.d) CONTAINS '<kw2>')
   RETURN n.n, substring(n.d,0,220), toString(n.t) ORDER BY n.t LIMIT 25
   ```
   Find the ORIGIN mention (earliest) + the surrounding context that says what the term MEANT. Optionally corroborate with `Tool_Call`/`TOUCHES_FILE` near those timestamps (was it real work on a file, or just talk?). Read enough mentions to actually understand it — do not stop at the first hit.
3. **ADJUDICATE (the anti-confabulation gate).** From the recovered evidence decide ONE:
   - **REAL** — the timeline genuinely explains a concept that was mentioned-but-unexplained (you can state what it is, with cited evidence) → go to FILL.
   - **VACUOUS / UNRESOLVED** — the mention is a bare number, a typo/CamelCase-vs-snake fragment, an extraction artifact, a transient, OR the timeline simply does not contain enough to say what it means → do NOT fill. Report UNRESOLVED with the closest evidence and why it's insufficient. (A stub honestly left empty beats a fabricated description. Still: never delete it.)
4. **FILL (only if REAL).** Call `add_concept`:
   - `concept_name = STUB_NODE`.
   - `concept` = the recovered description, written as what the term IS based on the evidence, ENDING with a provenance line: `(Recovered from timeline: <node names + timestamps cited>.)`.
   - `desc_update_mode = "prepend"` — STRICTLY ADDITIVE *and* the recovered description LEADS: prepend puts your real content FIRST and preserves whatever was there below it (incl. the stale "AUTO CREATED … not yet fully defined" marker, kept as a record that it was a stub). Never use "replace"; never remove text. (Do NOT use "append" — it leaves the stale marker leading the node, which mis-primes the next reader.)
   - `is_a` / `part_of` / `instantiates`: pass the node's EXISTING edges back VERBATIM (from step 1), PLUS only the ones the timeline genuinely supports. `add_concept` MERGEs edges additively — re-passing existing ones is a safe no-op; you are never removing one. **Anti-stub-spawn rule:** `add_concept` auto-CREATES any parent node you name that doesn't exist — so a careless inferred `is_a`/`part_of` REPAIRS one stub by MINTING another. Therefore: (a) PREFER an EXISTING `:Wiki` node as the parent (query first: `MATCH (p:Wiki) WHERE toLower(p.n) CONTAINS '<kw>' RETURN p.n` — reuse the real one); (b) if none fits, you MAY leave `is_a=[]` / `part_of=[]` (empty lists ARE accepted — the description is the fill, taxonomy is optional) rather than mint a thin parent; (c) only if a new parent is genuinely the right model, mint it AND note in the report that the new parent is now itself a stub to deconfab. ALWAYS FLAG any timeline-inferred edge in the report. If the timeline supports NEITHER a description NOR any category, you are not in FILL — you are UNRESOLVED (step 3).
   - Verify the write: re-`get_concept STUB_NODE` and confirm the recovered description is now present and the edges are intact (none lost).
5. **REPORT** (append to `OUTPUT`, then return a concise version): per the stub —
   - verdict: `FILLED` | `UNRESOLVED` | `NOT-A-STUB`;
   - if FILLED: the recovered description, the cited timeline evidence (node names + timestamps), the edges added (and which were timeline-inferred), and the post-write confirmation;
   - if UNRESOLVED: the closest evidence found + exactly what additional source would resolve it + the explicit statement that the node was left intact (not deleted);
   - any fabrication temptation you resisted (what the name "wanted" you to say vs what the evidence supported).

The node and its edges are sacrosanct — additive only. The timeline is the only source of meaning. "UNRESOLVED — closest evidence X, would need Y" beats any confident guess; an honest gap IS the correct outcome for a vacuous mention.
