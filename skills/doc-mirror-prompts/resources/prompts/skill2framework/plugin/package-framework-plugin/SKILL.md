---
name: package-framework-plugin
domain: skill2framework   subdomain: plugin
description: "WHAT: packages a framework into a Claude Code PLUGIN — assembles a plugin dir (plugin.json manifest + skills/<framework-skill>/SKILL.md + the chapter bundled as resources) from a generated framework skill + its chapter, and repaths the framework skill's chapter links to the bundled location. A framework package is ALWAYS a plugin; this is its operational face. WHEN: when packaging a framework as a plugin, when you have a framework skill + chapter and need the installable plugin, or when the user mentions packaging the framework / the plugin / skill2framework (any of)."
golden: false
score: 1.00   runs: 1   verified_good: 1
check_level: FULL_E2E   last_verified: 2026-06-03
log:
  - "2026-06-03 PASS — dogfood on doc-mirror. Subagent built /home/GOD/tmp/framework_recon/plugins/sancovp-framework-doc-mirror/ (plugin.json + skills/sancovp-framework-doc-mirror/SKILL.md + resources/chapter/{blog1,blog2,chapter}.md). I verified E2E myself: plugin.json is valid JSON (json.load ok, name+version correct); chapter bundled; the repathed chapter links (./resources/chapter/blog{1,2}.md) RESOLVE to existing bundled files; ZERO leftover absolute /home/GOD chapter paths; the 10 AIOS routing URLs (into doc-mirror's own plugin) PRESERVED untouched (diff = only the 4 chapter link lines). Self-contained framework plugin."
---
## PROMPT

You package a framework as a **Claude Code plugin** — its operational face. A framework package is ALWAYS a plugin. You assemble a valid plugin dir from the already-generated framework skill + its chapter, and you repath the framework skill's chapter links to the bundled copy so the plugin is self-contained.

### Specifics (provided at dispatch)
- Framework name: `{framework_name}`
- User/author token: `{user}`
- Framework skill SKILL.md (generated): `{framework_skill_path}`
- Chapter dir (blog1.md, blog2.md, chapter.md): `{chapter_dir}`
- Published plugin URL (for the manifest + any absolute links): `{plugin_url}`
- Output plugin dir: `{output_plugin_dir}`

### STEP 1 — BUILD THE PLUGIN SKELETON at `{output_plugin_dir}`
```
{output_plugin_dir}/
  plugin.json
  skills/
    {framework_name}-nomicon/
      SKILL.md          # the framework skill (copied from {framework_skill_path})
      resources/
        chapter/
          blog1.md  blog2.md  chapter.md   # the chapter, bundled
```
`plugin.json` (Claude Code plugin manifest) minimal valid shape:
```json
{
  "name": "{framework_name}-nomicon",
  "version": "0.1.0",
  "description": "<the framework skill's WHAT, one line>",
  "author": "{user}"
}
```
(If you know the repo's existing plugin.json conventions from the marketplace, match them; otherwise this minimal shape is valid.)

### STEP 2 — COPY + REPATH
- Copy `{framework_skill_path}` → `skills/{framework_name}-nomicon/SKILL.md`.
- Copy the chapter files → `skills/{framework_name}-nomicon/resources/chapter/`.
- In the COPIED framework SKILL.md, REPATH the chapter links: any absolute local path to the chapter (e.g. `/home/GOD/.../chapter/blog1.md`) becomes the bundled relative `./resources/chapter/blog1.md` (and note the published URL `{plugin_url}` for the plugin itself). Do NOT change anything else in the skill body (no voice/structure edits) — only the chapter link paths.

### STEP 3 — VALIDATE + REPORT (final message)
- Print the plugin dir tree.
- Show `plugin.json` (valid JSON — verify with `python3 -c "import json;json.load(open('...'))"`).
- Confirm: the framework SKILL.md is present under skills/; the chapter is bundled under resources/chapter/; the repathed chapter links in the skill now resolve to the bundled files (check the relative paths EXIST); the skill body is otherwise unchanged (diff = only the chapter link lines).
- Report anything that did not validate.

### Hard constraints
- Only repath the chapter links in the framework skill — do NOT edit its prose/structure.
- `plugin.json` MUST be valid JSON.
- Touch ONLY files under `{output_plugin_dir}`. Read nothing under `/home/GOD/core`.
