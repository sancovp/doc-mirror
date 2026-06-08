---
name: doc-mirror-memory-net
description: "WHAT: doc-mirror-memory-net (DMN) — the doc-mirror journal/vision IS a live, self-describing graph in CartON; this skill teaches its schema and gives ready-to-run query_wiki_graph Cypher so you REHYDRATE BY QUERYING the graph instead of re-reading flat journal files. The agent-facing front of the read layer (the system-facing twin is the docmirror-read CLI): 6 typed-traversal lookups — locate/where-am-i, vision-by-coordinate, cross-pollination, fuzzy-mereo network (+ active-leaf and closure when ungated) — plus a self-describing introspection query that keeps it from going stale. WHEN: when rehydrating/remembering at session start or post-compact; when you need to recall what was decided/found about a repo, domain, subdomain, or tag WITHOUT scanning files; when you want where-am-i / what's-related-to-X / what-spans-multiple-repos; or when the user mentions DMN, the memory net, rehydrate-by-query, or the doc-mirror read layer (any of)."
---

# doc-mirror-memory-net (DMN) — rehydrate by QUERYING the graph, not re-reading files

**The journal/vision is already a live, self-describing graph in CartON.** Every `journal` entry is a node;
its kind, repo, domain/subdomain, and tags are typed edges. So you do NOT rehydrate by scanning flat
`context/journal/*.md` files (the "re-read everything" context-blast the system prompt warns against) —
you **query the net for exactly the slice you need** (progressive disclosure). DMN is the *agent-facing*
front of the read layer; the *system-facing* twin is the `docmirror-read` CLI (same lookups, same Cypher).

Engine: the **`query_wiki_graph` MCP tool** (`mcp__carton__query_wiki_graph`) — read-only, must target
`:Wiki`. An agent CAN call it (a shell CLI cannot — that's why `docmirror-read` exists for the system side).

## The schema (what the net is made of)
Each journal entry node is a COORDINATE ADDRESS, written by `journal`:
- name = `{Repo}_{Domain}_{Subdomain}_{ts}` ; `INSTANTIATES Doc_Mirror_Journal_Entry`
- `IS_A Doc_Mirror_Journal_{Type}` — the KIND (Finding / Decision / Intent / Vision / Open / Hypothesis / Note)
- `PART_OF [{Repo}, {Subdomain}]` ; `{Subdomain} PART_OF {Domain}` — the triangulation axes
- `RELATED_TO {Tag}` — the hyperedge cross-links
- **typed axis nodes**: `{Repo} IS_A Doc_Mirror_Repo` · `{Domain} IS_A Doc_Mirror_Domain` ·
  `{Subdomain} IS_A Doc_Mirror_Subdomain` (these make the boundaries STRUCTURAL — lookups key on them)

**Normalization (critical):** every name is `Title_Case_With_Underscores`. A tag `read-layer` is the node
`Read_Layer`; `step-a` → `Step_A`. Title_Case your selector or the query silently returns nothing.

## The lookups (paste the Cypher into `mcp__carton__query_wiki_graph`)

**#1 locate — where am I? (graph-derived; replaces eyeballing a flat cursor)**
```cypher
MATCH (e:Wiki)-[:INSTANTIATES]->(:Wiki {n:'Doc_Mirror_Journal_Entry'})
WITH e ORDER BY e.t DESC LIMIT 1
OPTIONAL MATCH (e)-[:PART_OF]->(r:Wiki)-[:IS_A]->(:Wiki {n:'Doc_Mirror_Repo'})
OPTIONAL MATCH (e)-[:PART_OF]->(sd:Wiki)-[:IS_A]->(:Wiki {n:'Doc_Mirror_Subdomain'})
OPTIONAL MATCH (sd)-[:PART_OF]->(d:Wiki)-[:IS_A]->(:Wiki {n:'Doc_Mirror_Domain'})
RETURN e.n AS latest_entry, toString(e.t) AS ts, r.n AS repo, d.n AS domain, sd.n AS subdomain
```

**#3 vision-by-coordinate — what was said about X?** (by tag; swap the predicate for subdomain/domain)
```cypher
// by TAG (Title_Cased!):
MATCH (e:Wiki)-[:RELATED_TO]->(:Wiki {n:'Read_Layer'})
RETURN e.n AS entry, substring(e.d,0,180) AS preview, toString(e.t) AS ts ORDER BY e.t DESC LIMIT 15
// by SUBDOMAIN:  MATCH (e:Wiki)-[:PART_OF]->(:Wiki {n:'Read_Layer_Build'})-[:IS_A]->(:Wiki {n:'Doc_Mirror_Subdomain'}) ...
// by DOMAIN:     MATCH (e:Wiki)-[:PART_OF]->(:Wiki)-[:PART_OF]->(:Wiki {n:'Doc_Mirror_Read_Layer'})-[:IS_A]->(:Wiki {n:'Doc_Mirror_Domain'}) ...
```

**#4 cross-pollination — what ideas span ≥2 repos?** (the emergent hyperedges flat files can't find)
```cypher
MATCH (e:Wiki)-[:PART_OF|RELATED_TO*1..3]->(r:Wiki)-[:IS_A]->(:Wiki {n:'Doc_Mirror_Repo'})
WITH e, collect(DISTINCT r.n) AS repos WHERE size(repos) >= 2
RETURN e.n AS entry, repos, substring(e.d,0,120) AS preview ORDER BY size(repos) DESC LIMIT 25
```

**#6 fuzzy-mereo — the neighborhood of a concept** (pass `{"c": "Doc_Mirror_Read_Layer"}` as parameters)
```cypher
MATCH p=(c:Wiki {n:$c})-[*1..2]-(m:Wiki)
RETURN DISTINCT m.n AS node, min(length(p)) AS hops ORDER BY hops, node LIMIT 40
```

**#2 active-leaf** (what's the next ACTIVE thing to work on) and **#5 closure** (file↔doc(m) bijection) are
NOT yet wired: #2 awaits the tracker-as-derived-view rebuild (status in the graph); #5 awaits CA `:File`/
`doc(m)` nodes. Use `locate` (#1) for "what am I on" until #2 lands.

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
