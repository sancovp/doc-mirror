---
name: generate-framework-skill
domain: skill2framework   subdomain: framework-skill
description: "WHAT: generates the FRAMEWORK SKILL for an already-built AIOS — a single skill that indexes the AIOS's skill-tree + rules + how they relate (as a diagram), gives a DECISION TREE telling the agent what to do, and ROUTES the agent into the AIOS dir for those skills/rules. It is the front-door index + decision-tree router that sits on top of an AIOS; named {aios}-nomicon (the AIOS's own local nomicon, held by the author's {user}-nomicon). WHEN: when producing the framework-skill face of a framework package, when you need the index/router skill that points into an AIOS, or when the user mentions the framework skill, generate-framework-skill, or skill2framework (any of)."
golden: false
score: 1.00   runs: 1   verified_good: 1
check_level: FULL_E2E   last_verified: 2026-06-03
log:
  - "2026-06-03 PASS — dogfood on doc-mirror. Subagent generated /home/GOD/tmp/framework_recon/sancovp-framework-doc-mirror/SKILL.md. I verified E2E myself: frontmatter name=sancovp-framework-doc-mirror + keyword-dense WHAT/WHEN; indexes ALL 10 skills (it CAUGHT 2 the chapter missed — doc-mirror-install + ship-a-plugin — by reading the dir); rules table mapping rule->governed-skill; the state-machine FLOW diagram + legal-transitions edge set + machine-part mapping; a copy-pasteable DECISION TREE (cursor-phase + SELECT-by-situation + cross-cutting + stuck-escape); ROUTING into the AIOS dir with real per-skill plugin URLs; links the chapter (blog1/blog2) + plugin. Exactly the Isaac framework-skill definition (index + decision-tree router on top of an AIOS). NOTE: chapter (S3) listed only 8 skills vs the real 10 — completeness gap to fix later (non-blocking)."
---
## PROMPT

You generate the **FRAMEWORK SKILL** for an already-built AIOS. Per the definition: a framework skill is a skill that **has the AIOS's skill-info indexed** — it shows the **tree of skills in the framework + the rules + how they all relate, as a diagram**; then it gives the **decision tree** (what to do / which skill to use when); you use it, it tells you what to do, and it **routes you into the AIOS dir** for those skills/rules. It is the front-door index + decision-tree router that sits on top of the AIOS. It also links the chapter (the two blogs) and the plugin.

### Specifics (provided at dispatch)
- AIOS name: `{aios_name}`
- Author/user token (author context; the generated skill is named `{aios_name}-nomicon`): `{user}`
- AIOS skills dir (read each skill's name + description + when-to-use): `{aios_skills_dir}`
- AIOS system doc (the diagrams + state machine): `{aios_system_doc}`
- AIOS rules dir (the rules that bind the skills, if any): `{aios_rules_dir}`
- Chapter dir (the two blogs to link): `{chapter_dir}`
- Plugin URL (operational face): `{plugin_url}`
- Output dir for the framework skill (write `SKILL.md` here): `{output_skill_dir}`

### STEP 1 — INDEX THE AIOS
Read every skill in `{aios_skills_dir}` (name + its description's WHAT/WHEN) and the rules in `{aios_rules_dir}`. Read `{aios_system_doc}` for the relationships/state-machine. Build:
- the **skill tree** (the skills, grouped/ordered as the AIOS uses them),
- the **rules** that bind them (which rule governs which skill/transition),
- **how they relate** — a DIAGRAM (reproduce or distill the AIOS's own state/relationship diagram from `{aios_system_doc}`; ASCII or mermaid).

### STEP 2 — WRITE THE DECISION TREE
A concrete "what do I do?" decision tree the agent follows: each branch = a situation -> the skill to use. (For a state-machine AIOS this IS the routing: session start -> the boot/entry skill; situation X -> skill X; stuck -> the defined escape.) Make it copy-pasteable guidance, not prose.

### STEP 3 — WRITE THE FRAMEWORK SKILL (`{output_skill_dir}/SKILL.md`)
Frontmatter:
- `name: {aios_name}-nomicon`  (the {aios}-nomicon — the AIOS's local nomicon)
- `description:` WHAT/WHEN per the skill-description discipline — WHAT = "the {aios_name}-nomicon: an index + decision-tree router into the {aios_name} AIOS (its skills/rules), with the chapter that explains it"; WHEN = the literal situations where an agent should reach for this AIOS (name them).
Body (this is the index + router):
1. One-paragraph "what this framework is" (point at the chapter: `{chapter_dir}` blog1 = story, blog2 = mechanics; and the plugin `{plugin_url}`).
2. The SKILL TREE + RULES + the relationship DIAGRAM (from STEP 1).
3. The DECISION TREE (from STEP 2).
4. ROUTING: explicit "to operate, read/equip these AIOS skills" with their paths under `{plugin_url}/skills/<name>` (and rules under the rules dir) — i.e. it sends the agent INTO the AIOS dir.
5. Links: the chapter (blog1/blog2), the plugin.

### STEP 4 — REPORT (final message)
Return the full generated `SKILL.md`, and confirm: it indexes EVERY skill found in `{aios_skills_dir}` (list them, none missed); it contains a diagram; it contains a decision tree; it routes into the AIOS dir with real paths; it links the chapter + plugin. Mark any skill you could not characterize from its files.

### Hard constraints
- The framework skill is an INDEX + ROUTER — it does NOT duplicate the AIOS skills' content; it points at them (canonical reference, per skills-reference-canonical-not-random).
- Ground the index in the actual skill files + system doc — do not invent skills or rules.
- Touch ONLY `{output_skill_dir}`. Read nothing under `/home/GOD/core`.
