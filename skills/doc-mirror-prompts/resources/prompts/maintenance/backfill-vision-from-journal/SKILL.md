---
name: backfill-vision-from-journal
description: Project an existing doc-mirror journal month-file's accumulated DECISION/FINDING entries into the vision(m) layer (catch the durable layer up to the thinklog). Use when the journal->vision projection was added after a session's thinking already piled up untagged in the journal.
---

# Prompt: backfill vision(m) from a journal month-file

You are catching the **durable vision layer up to the thinklog**. A doc-mirror journal month-file
has accumulated DECISION/FINDING/INTENT entries that were written BEFORE the journal→vision
projection existed (so they sit only in the journal, not in any `vision(m)`). Project the
substantive ones into the right `vision(m)` files so the geometry coheres.

## Inputs (the dispatcher fills these)
- **JOURNAL_FILE**: the month-file to backfill (e.g. `<repo-root>/context/journal/2026-05.md`).
- **MONOREPO**: repo root for routing (default `<repo-root>`; export `DOCMIRROR_MONOREPO`).
- **SINCE** (optional): only entries on/after this date (e.g. `2026-05-31`).

## How projection works (use the journal CLI — it does the routing)
`journal -t <FLAVOR> --tags <tag1>,<tag2>,... "<concise one-line restatement>"`
- A tag that is a **module** (its `doc(m)` exists at `<repo>/docs/mirror/<tag>.md`) → the entry is
  appended as a `tags:[...]` line to the paired `<repo>/docs/vision/<tag>.md`.
- Other tags (concepts, repos) ride along in the `tags:[...]` clause so `vision <tag>` resolves the
  hyperedge.
- A tag with no `doc(m)` does nothing (no projection) — that's fine.

## Procedure
1. **Read JOURNAL_FILE fully.** (Filter to SINCE if given.) Skip pure-noise lines; keep substantive
   DECISION / FINDING / INTENT / OPEN entries.
2. **Classify each kept entry by what it is ABOUT:**
   - **Module-specific** (about code that HAS a `doc(m)`): find the module path(s) — verify
     `<MONOREPO>/**/docs/mirror/<relpath>.md` exists. Project with
     `journal -t <FLAVOR> --tags <relpath>,<concept...> "<restatement>"`.
   - **Cross-cutting** (system architecture / strategy / a thing with no single `doc(m)`): append it
     to a cross-cutting vision file `<repo>/docs/vision/_<topic>.md` as a `- <restatement>  tags:[...]`
     line (create the file if absent; this is a legal vision kind). Pick the repo it most belongs to
     (e.g. doc-mirror-system architecture → the doc-mirror-system repo).
   - **Module with NO `doc(m)` yet** (un-booted repo): do NOT force-project. Add it to a
     `needs-doc(m)-first` list in your report.
3. **Restatements must be ONE concise line** — the durable vision entry, not the verbose journal text.
   **Preserve the user's exact terms** (do not paraphrase load-bearing words); compress, don't reword.
4. **De-dup:** before projecting, `grep` the target `vision(m)` for an entry already covering it; skip if present.
5. **Verify (E2E):** after projecting, run `vision <key-concept>` for 3–5 of the concepts you used and
   confirm they resolve to the expected files. Paste the output.

## Output (your final message)
- Count of entries projected, grouped by target `vision(m)` / `_<topic>.md` file.
- The `needs-doc(m)-first` list (entries that couldn't project because their module isn't booted).
- The `vision <concept>` verification output for the concepts you projected.
- Do NOT claim done until the `vision` CLI resolves the projected entries.

## RELIABILITY
- score: 1.00               # verified-good runs / total runs (the dispatcher's E2E checks, not the agent's report)
- runs: 1  verified-good: 1  last-verified: 2026-05-31
- check-level: FULL_E2E     # still verify E2E until ≥3 clean runs
- log (newest first):
  - 2026-05-31 PASS — backfilled the 2026-05-31 session (48 entries → 8 module-specific SOMA vision(m) + 40 cross-cutting across 5 doc-mirror-system/_topic files). Dispatcher re-ran `vision strong_compression/observation-chain/EAA/dumb-versions/MSC` + read samples: concise one-liners, user terms preserved, hyperedges stitch module↔cross-cutting correctly, cat_gate de-duped (2 not 3). No prompt fix needed.
