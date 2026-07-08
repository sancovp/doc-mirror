---
name: check-sophia-progress
description: "WHAT: check the live status of the Sophia rollup / cohere worker — is the daemon running, how far BEHIND it is (how many journals not yet cohered / the lag between newest journal and newest momentum), and how many issues meta-Sophia has flagged. WHEN: when you want to know if Sophia is running + caught up, when a rehydration or decided-logic query looks stale, when you suspect the rollup died, or when the user asks 'is sophia running / caught up / how far behind / how many meta issues' (any of)."
---

# check-sophia-progress

Sophia = the chronological rollup worker (`doc-mirror-system/sophia/sophia_worker.py`) that reads the
journal oldest-first and writes one `{journal}_Momentum` node (`Doc_Mirror_Momentum_Observation`) per entry
(continues/diverges/reverses + canonical_intent). Meta-Sophia is the corrector that flags likely
misclassifications (`Doc_Mirror_Meta_Observation`). This skill answers: **running? how far behind? how many
issues?** — in three checks.

## 1. Is the daemon running?
```bash
ps aux | grep "[s]ophia_worker.py" | grep -v grep
```
Expect: `sophia_worker.py --daemon --interval 20 --cap 1 --model MiniMax-M2.7-highspeed`. Empty = DOWN
(restart it: `python3 doc-mirror-system/sophia/sophia_worker.py --daemon --interval 20 --cap 1 ... &`).

## 2. How far BEHIND is it? (the lag = the real health signal)
Run via `query_wiki_graph` (or `_get_module_connection().execute_query` in-process). The load-bearing number
is **journals with no `_Momentum` yet** — 0 = fully caught up.
```cypher
// backlog: journals Sophia has NOT cohered yet (0 = caught up)
MATCH (e:Wiki)-[:INSTANTIATES]->(:Wiki {n:'Doc_Mirror_Journal_Entry'})
WHERE NOT EXISTS { MATCH (m:Wiki {n: e.n + '_Momentum'}) }
RETURN count(e) AS behind
// freshness: newest journal vs newest momentum (the time-lag)
MATCH (e:Wiki)-[:INSTANTIATES]->(:Wiki {n:'Doc_Mirror_Journal_Entry'}) WHERE e.t IS NOT NULL
RETURN toString(max(e.t)) AS newest_journal
MATCH (m:Wiki)-[:INSTANTIATES]->(:Wiki {n:'Doc_Mirror_Momentum_Observation'}) WHERE m.t IS NOT NULL
RETURN toString(max(m.t)) AS newest_momentum
```
Interpret: `behind = 0` and `newest_momentum >= newest_journal` (or within a few min) = healthy. `behind`
growing over successive checks = the worker is dead or wedged. (Verified 2026-07-01: 1635 journals, behind=0,
Sophia cohered the newest entry within ~3 min.)

## 3. How many issues has meta-Sophia flagged?
```cypher
MATCH (f:Wiki)-[:INSTANTIATES]->(:Wiki {n:'Doc_Mirror_Meta_Observation'}) RETURN count(f) AS meta_flags
// to SEE them: RETURN f.n, f.current_class, f.suggested_class, f.thing, f.reason
```
These are the decided-logic misclassifications meta-Sophia caught (reversals Sophia missed, drift). A rising
count with no reconciliation = drift accumulating in the record.

## The one-line status (paste-ready)
`Sophia: <running|DOWN> · behind <N> journals · newest_momentum <ts> (journal <ts>) · meta-flags <N>`

## UPGRADE (not built — the better version Isaac wants)
Isaac's preference: this status should AUTO-UPDATE and be surfaced without invoking a skill (so it's live, not
a thing you must remember to check — see `status-phase-info-lives-in-carton-not-frozen-prose` +
`caching-provenance-zombie`). The build: a small tick/hook computes the three numbers above, writes them to a
CartON `Status_Phase_Table` concept (`set_properties`) + a status line, and a rule/`UserPromptSubmit` hook
surfaces the live line each turn. Until built, run this skill.
