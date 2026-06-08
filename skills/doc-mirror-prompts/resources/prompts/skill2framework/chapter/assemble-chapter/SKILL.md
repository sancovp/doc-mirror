---
name: assemble-chapter
domain: skill2framework   subdomain: chapter
description: "WHAT: assembles a framework CHAPTER from the two already-rendered blog posts — combines Blog 1 (narrative) and Blog 2 (deep dive) into a chapter directory, wires the cross-links (Blog1<->Blog2, and both -> the plugin on the monorepo + the framework's skills) and litters in CTAs, producing the chapter as the publishable unit (Blog1 + Blog2 = one chapter). It does NOT rewrite the blogs' prose — only wires links + CTAs + a chapter manifest. WHEN: when you have Blog 1 + Blog 2 for a framework and need to combine them into a chapter, when wiring the cross-links/CTAs of a framework package, or when the user mentions assembling a chapter / skill2framework (any of)."
golden: false
score: 1.00   runs: 1   verified_good: 1
check_level: FULL_E2E   last_verified: 2026-06-03
log:
  - "2026-06-03 PASS — dogfood on doc-mirror. Subagent combined blog1+blog2 into /home/GOD/tmp/framework_recon/doc-mirror_chapter/ (blog1.md, blog2.md, chapter.md). I verified E2E myself: cross-links relative + resolve (blog1<->blog2), prose bodies UNCHANGED (diff = pure additions only; the one blog2 change was normalizing the backlink to ./blog1.md), plugin link + all 8 skill links present in all three files, CTAs injected, chapter.md manifest clean. Self-contained chapter dir. Agent sensibly rendered skill_links as full URLs (plugin_url/skills/<name>)."
---
## PROMPT

You assemble a **framework CHAPTER** from two already-rendered blog posts. A chapter = Blog 1 (the narrative opener) + Blog 2 (the mechanical deep dive), WIRED together with cross-links and CTAs. You do NOT rewrite the blogs' prose (voice/structure is out of scope) — you only inject the link sections, the CTAs, and a chapter manifest.

### Specifics (provided at dispatch)
- Framework name: `{framework_name}`
- Blog 1 source (narrative): `{blog1_path}`
- Blog 2 source (deep dive): `{blog2_path}`
- Plugin URL (the operational face on the monorepo): `{plugin_url}`
- Skill links (the rung face — the skills this framework decomposes into; name -> path/url each): `{skill_links}`
- Output chapter dir: `{chapter_dir}`

### STEP 1 — COPY the two posts into `{chapter_dir}` as `blog1.md` and `blog2.md` (verbatim — do not touch their prose).

### STEP 2 — WIRE THE CROSS-LINKS + CTAs (append/replace ONLY the links section + add CTA lines; never edit narrative body)
- In `blog1.md`: ensure a links block exists near the top AND at the end with:
  - "Deep dive — how it works: ./blog2.md"
  - "Get the plugin: {plugin_url}"
  - "The skills: {skill_links}" (list each)
  - A clear CTA line (e.g. "Install the plugin and run it yourself: {plugin_url}").
- In `blog2.md`: ensure it links back ("The story: ./blog1.md"), links the plugin ("{plugin_url}"), and ends with a CTA.
- "Litter CTAs" = a short call-to-action at each major section break is fine, but keep them short and do NOT alter the surrounding prose. CTAs point at the plugin (install/use) and the other blog.

### STEP 3 — WRITE THE CHAPTER MANIFEST `{chapter_dir}/chapter.md`
A short index: chapter title = `{framework_name}`, a 2-line abstract, then the ordered contents (1. Blog 1 narrative -> ./blog1.md, 2. Blog 2 deep dive -> ./blog2.md), the plugin link, and the skill links. This manifest is what the framework skill and the nomicon will point at.

### STEP 4 — REPORT (final message)
Return: the chapter dir tree, the FINAL blog1.md + blog2.md links/CTA sections (show what you injected), and the full chapter.md. Confirm: prose bodies unchanged (diff only in link/CTA lines), cross-links resolve (blog1<->blog2 relative paths exist), plugin + skill links present in all three files.

### Hard constraints
- Do NOT rewrite blog prose. Only inject link sections, CTA lines, and the manifest.
- Cross-links between blog1/blog2 are RELATIVE (`./blog1.md` / `./blog2.md`) so the chapter dir is self-contained.
- Touch ONLY files under `{chapter_dir}`. Read nothing under `/home/GOD/core`.
