---
name: fold-into-nomicon
domain: skill2framework   subdomain: nomicon
description: "WHAT: folds a framework into the author's NOMICON — the top-level holder + search of all of {user}'s frameworks (its {aios}-nomicons). Creates the {user}-nomicon skill if it does not exist, then registers/updates the framework's entry (one-line + links to its framework skill, plugin, and chapter). The nomicon is the framework-of-frameworks index an agent equips to mesh with the author's way of thinking and find which framework fits a task. WHEN: when folding a finished framework package into the nomicon, when creating/updating the author's nomicon, or when the user mentions the nomicon / framework-of-frameworks / skill2framework fold (any of)."
golden: false
score: 1.00   runs: 1   verified_good: 1
check_level: FULL_E2E   last_verified: 2026-06-03
log:
  - "2026-06-03 PASS — dogfood on doc-mirror (TERMINAL stage). Subagent created /home/GOD/tmp/framework_recon/sancovpnomicon/SKILL.md (the sancovpnomicon holder/search skill) and registered the doc-mirror row. I verified the FULL framework->nomicon round-trip E2E myself: nomicon valid frontmatter (WHAT/WHEN); doc-mirror row present EXACTLY ONCE (idempotent); HOP1 nomicon->framework skill resolves (16592B); HOP2 framework skill->AIOS = 10 routing URLs into doc-mirror plugin skills; HOP3 plugin.json + bundled chapter (blog1/blog2/chapter) all resolve. The whole AIOS->framework->nomicon chain is hooked. Nomicon is a pure holder/search+router (canonical refs, no duplication)."
---
## PROMPT

You fold a finished framework into the author's **NOMICON** — the top-level **holder + search** of all of `{user}`'s frameworks. The nomicon is the framework-of-frameworks skill: an agent equips it to see the author's whole framework set, search "which of my frameworks fits this task?", and route into the chosen one. (It is JUST a holder/search — not a doer.) You CREATE the nomicon skill if it does not exist, then REGISTER (or update) this framework's entry. The op is idempotent — re-folding the same framework updates its row, never duplicates it.

### Specifics (provided at dispatch)
- User/author token: `{user}`
- Nomicon dir (the `{user}-nomicon` skill home — create `SKILL.md` here if absent): `{nomicon_dir}`
- Framework being folded in: `{framework_name}`
- Its one-line summary: `{framework_summary}`
- Its framework-skill name + path: `{framework_skill_name}` @ `{framework_skill_path}`
- Its packaged plugin dir/URL: `{framework_plugin_ref}`
- Its chapter dir/URL: `{chapter_ref}`

### STEP 1 — ENSURE THE NOMICON SKILL EXISTS (`{nomicon_dir}/SKILL.md`)
If absent, create it:
- Frontmatter `name: {user}-nomicon`; `description:` WHAT = "the {user} nomicon — the top-level holder + search of all of {user}'s frameworks (its {aios}-nomicons); given a task it tells you which of the author's frameworks fits and routes you into it (so an agent meshes with {user}'s way of thinking and uses {user}'s frameworks)"; WHEN = "when you want to use {user}'s frameworks, find which framework fits a task, mesh with {user}'s mental model, or the user mentions the nomicon / {user}'s frameworks (any of)".
- Body sections: a one-paragraph "what the nomicon is", then `## Frameworks` containing a TABLE (columns: Framework | What it's for | Framework skill | Plugin | Chapter), then `## How to use` = "scan the table / match your task to a framework's 'what it's for', then equip that framework skill — it routes you into its AIOS."

### STEP 2 — REGISTER THIS FRAMEWORK
Add (or update, if a row for `{framework_name}` already exists — never duplicate) a row in the `## Frameworks` table:
`| {framework_name} | {framework_summary} | {framework_skill_name} ({framework_skill_path}) | {framework_plugin_ref} | {chapter_ref} |`

### STEP 3 — VALIDATE + REPORT (final message)
- Show the full `{nomicon_dir}/SKILL.md`.
- Confirm: the nomicon frontmatter is valid; the `{framework_name}` row is present EXACTLY ONCE (idempotent); the links/paths in the row are correct.
- Demonstrate the E2E round-trip in words: nomicon → (search) → `{framework_skill_name}` → (routes into) → the AIOS. Confirm each hop's reference resolves.

### Hard constraints
- The nomicon is a HOLDER/SEARCH + ROUTER only — it does not duplicate framework content; it points (canonical reference).
- Idempotent: one row per framework; re-folding updates, never duplicates.
- Touch ONLY files under `{nomicon_dir}`. Read nothing under `/home/GOD/core`.
