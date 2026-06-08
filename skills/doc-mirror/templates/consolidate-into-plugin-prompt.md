# PROMPT: Consolidate doc-mirror into ONE plugin source dir + an installer

You are an agent on a metacog team. Your job: make doc-mirror exist as ONE canonical source dir,
plugin-structured, from which it installs out to its runtime locations. Today it is SCATTERED across
6 places with no single source and no plugin manifest — fix that. Read this whole prompt, apply the
SPECIFICS your dispatch gave you, then DO IT and report what you built + the install verification.

## The canonical source dir (build it here)
`SPECIFIC: <PLUGIN_DIR>` (dispatch gives the path; default `<repo-root>/doc-mirror-system/plugin`).
Structure it as a Claude Code plugin (per https://code.claude.com/docs/en/plugins.md):
```
<PLUGIN_DIR>/
  .claude-plugin/plugin.json     # manifest: name "doc-mirror", version, description
  skills/doc-mirror/             # the SKILL.md + scripts/ + templates/ (THE LAW + prompt-files)
  skills/doc-mirror-boot/  # entry + core-loop prime + router
  skills/doc-mirror-init/        # @boot state-skill (subsumed the old boot-doc-mirror-system)
  skills/doc-mirror-seework/     # @seework state-skill
  skills/doc-mirror-change/      # @change state-skill
  skills/doc-mirror-prompts/     # @prompt state-skill
  skills/make-ai-operating-system/     # (and the architect skill)
  hooks/hooks.json + hooks/*.py  # docmirror_brainhook.py, docmirror_session_start.py
  bin/                           # journal, projects, vision, plan, doc-mirror-commit, docmirror-sleep,
                                 #   docmirror-layers, docmirror-system, docmirror-brainhook
  rules/*.md                     # the doc-mirror law + behavior rules (see list below)
  DOC_MIRROR_SYSTEM.md           # the spec
  install.sh                     # idempotent installer (see below)
```

## What to GATHER (the scattered sources — these are the truth to consolidate, read each first)
- `~/.claude/skills/doc-mirror/` — SKILL.md, scripts/{doc-mirror-commit,docmirror-sleep,docmirror-layers,docmirror-system}, templates/{team_doc_prompt.md,journal_reminder.txt,brainhook_prompt.txt,docmirror_harvest_reminder.txt}, hooks/{docmirror_brainhook,docmirror_session_start}.py
- `~/.claude/skills/doc-mirror-boot/`, `~/.claude/skills/doc-mirror-{boot,seework,change,prompts}/`, `~/.claude/skills/make-ai-operating-system/`
- `~/.local/bin/`: journal, projects, vision, plan, doc-mirror-commit, docmirror-sleep, docmirror-layers, docmirror-system, docmirror-brainhook
- `~/.claude/hooks/`: docmirror_brainhook.py, docmirror_session_start.py
- `~/.claude/`: docmirror_loop_prompt.txt, docmirror_harvest_reminder.txt
- `~/.claude/rules/`: doc-mirror-is-the-only-system, doc-mirror-flow-diagram, doc-mirror-normalize-doc-filenames-before-closure, use-the-journal, skills-reference-canonical-not-random, corrections-state-what-is-not-what-isnt, commander-not-hands-dispatch-everything
- `<repo-root>/DOC_MIRROR_SYSTEM.md`

DE-DUPLICATE on the way in: several files exist in 2+ places (e.g. the brainhook in both hooks/ and the
skill; the loop prompt loose AND as templates/brainhook_prompt.txt). The PLUGIN DIR is the ONE canon;
pick the newest/correct copy of each (diff them; flag any real divergence), put it in the plugin dir.

## install.sh (the install-out direction — plugin dir is source, runtime is a copy)
Idempotent bash that copies/symlinks from `<PLUGIN_DIR>` to the runtime locations the live system reads:
- `bin/*` → `~/.local/bin/` (chmod +x)
- `hooks/*.py` → `~/.claude/hooks/`
- `skills/*` → `~/.claude/skills/`
- `rules/*.md` → `~/.claude/rules/`
- loop prompt → `~/.claude/docmirror_loop_prompt.txt`
Print what it installed. Re-runnable. (Symlink vs copy: your call, but installing must make the LIVE
system identical to the plugin source.)

## CONSTRAINTS
- Read-only on the SCATTERED sources except to MOVE/copy them into the plugin dir; do NOT delete the
  live runtime copies until install.sh is proven to reproduce them.
- Do NOT change the CONTENT of any script/rule/skill — this is consolidation, not a rewrite. (If you find a
  genuine divergence between two copies, journal it and keep the newer; don't silently merge logic.)
- Work reversibly (git; the monorepo is a git repo).

## VERIFY E2E (the observer leg must confirm)
1. `<PLUGIN_DIR>/.claude-plugin/plugin.json` is valid JSON with name/version/description.
2. Every scattered artifact above has a home in the plugin dir (nothing missed) — list them.
3. `bash <PLUGIN_DIR>/install.sh` runs clean and re-runnable; after it, the live `~/.local/bin/journal`,
   the hooks, the rules, the skill all match the plugin-dir source (diff = empty).
4. Smoke: `journal --where`, `projects list`, `vision --tags`, `docmirror-brainhook` toggle still work
   post-install (they resolve to the installed copies).

## REPORT
The plugin tree, the de-dupe decisions (which copy won, any divergences flagged), the install.sh output,
and the 4 verification results. Do NOT commit (team lead commits).
