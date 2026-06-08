---
name: onboarding-rewrite
domain: authoring   subdomain: system-prompt
description: "WHAT: rewrite a SYSTEM PROMPT / agent onboarding file (a CLAUDE.md / persona entry) that fails to onboard — it references named components and jargon before the reader knows them, never orients the reader to the situation, never says how to START operating the system, and is formatted as a wall of markdown lists — into a correctly-FORMATTED, onboarding-shaped system prompt: one outer XML brace, XML-tagged sections with markdown inside, ordered name → description → context (meta/core-loop) → reinforcement, jargon glossed on first use. WHEN: when a system prompt / CLAUDE.md reads like reference notes instead of an onboarding; when it names things before introducing them; when it does not tell a fresh agent how to begin; when it is all markdown headers/lists with no XML sectioning."
golden: false
score: 0.00   runs: 0   verified_good: 0
check_level: FULL_E2E   last_verified: ""
log: []
---
## PROMPT

<background>
You are rewriting a SYSTEM PROMPT — the FIRST thing a fresh agent reads. Its job is to BOOT a stranger
into the system: orient them, tell them what this is, tell them how to start operating it, and seal it
off from the other context that gets injected around it. The current version at `{system_prompt_path}`
FAILS this — it references internal names/jargon before the reader knows them, never orients the reader,
never says how to begin, and is formatted as a wall of markdown headers and bullet lists. You will
replace it with a correctly-formatted, onboarding-shaped system prompt synthesized from what the system
ACTUALLY is (you read the real sources; you do not invent).
</background>

<format_law>
A prompt is NOT a markdown document. Two laws:
1. ONE OUTER BRACE. The ENTIRE prompt is wrapped, top and bottom, in a single XML tag that seals it off
   from other injected context: `<SYSTEM_PROMPT>` … `</SYSTEM_PROMPT>`.
2. SECTIONS ARE XML TAGS, MARKDOWN INSIDE. Each section is its own XML tag whose NAME is the section
   (`<description>` … `</description>`). Inside the tag you write markdown PROSE. Do NOT repeat the
   section name as a markdown header inside its own tag (no `<situation>## The situation …`). Do NOT
   make everything a bullet list — most sections are prose paragraphs; use a list only for a genuine
   enumeration. (LLMs default to "everything is markdown, everything is a list" — break them out of it.)
</format_law>

<section_order>
The required sections, in this exact order:
- `<name>`          — what this IS, named meta-first, in one line (the parent class / role).
- `<description>`   — one paragraph: what the system is + what the agent is here to do.
- the CONTEXT sections (the abstract middle — as many tags as the system needs, e.g.):
    `<situation>`    — where the agent is, current state, what is OFF / to be ignored.
    `<core_loop>`    — the ONE operating loop, startable from this section alone: `the first thing you
                       do is {entry_point}` + what it does + the per-turn loop.
    `<rules>`        — only the handful that matter day-to-day.
    `<pointers>`     — deep references / where-things-live (LAST of the context sections).
- `<reinforcement>` — the CLOSING block. One short paragraph in the second person, present-perfect:
    "You have now deeply learned that {the core thing} … and you {follow the core loop, in order, to
    the letter}." It reinforces that the agent has internalized the core loop and runs it to produce /
    operate the system.
Jargon rule (applies in every section): each term in `{jargon_terms}` gets a one-clause gloss the FIRST
time it appears, and is NEVER referenced before it is established.
</section_order>

<inputs (the caller supplies these — fill every slot)>
`{system_prompt_path}`  the file to rewrite (READ it first — it is the current bad version)
`{system_name}`         what the system is called (→ `<name>`)
`{situation}`           what the agent is doing here + current state + what is OFF (→ `<situation>`)
`{entry_point}`         the skill/command/step used FIRST to operate the system + what it does (→ `<core_loop>`)
`{canonical_sources}`   `[paths]` to READ to learn what the system IS + how it works (grounding, not invention)
`{jargon_terms}`        `[terms]` each needing a first-use gloss
</inputs>

<output_format>
Overwrite `{system_prompt_path}` with: `<SYSTEM_PROMPT>` + the sections in `<section_order>` (XML tags,
markdown prose inside) + `</SYSTEM_PROMPT>`. Keep it SHORT — onboarding, not a manual; depth lives in
`{canonical_sources}`, which `<pointers>` names but never restates.
</output_format>

<cor>
1. READ `{system_prompt_path}` (the current bad version) AND every file in `{canonical_sources}`
   ENTIRELY — the rewrite is a synthesis of what the system ACTUALLY is, never invented.
2. BACK UP the original (reversible): `cp {system_prompt_path} {system_prompt_path}.bak-{YYYYMMDD}`.
3. WRITE it in the `<format_law>` + `<section_order>`: one `<SYSTEM_PROMPT>` brace; `<name>` meta-first
   → `<description>` → the context tags (`<situation>` → `<core_loop>` starting `the first thing you do
   is {entry_point}` → `<rules>` → `<pointers>` last) → `<reinforcement>` closing block. Markdown PROSE
   inside each tag, no doubled section titles, no list-spam. Gloss each `{jargon_term}` on first use.
4. RE-READ as a STRANGER who knows none of `{jargon_terms}`: is the whole thing braced once; is every
   section an XML tag with prose inside (not a list wall); is each term plain or already glossed; could
   this stranger START from `<core_loop>` alone; does it END on the `<reinforcement>` block? Fix any "no".
5. ⟹ the rewritten `{system_prompt_path}` that BOOTS a fresh agent — braced, XML-sectioned, situation
   first, how-to-operate second, jargon never before its gloss, reinforced at the end — original at `.bak`.
</cor>
