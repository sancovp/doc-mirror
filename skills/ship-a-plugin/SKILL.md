---
name: ship-a-plugin
description: "WHAT: the development-flow for building AND distributing a Claude Code plugin — what a plugin is made of, how a marketplace actually works (ONE catalog that REFERENCES plugins, not a monorepo that houses their code), and the complete build → commit → install → dogfood → de-scatter flow with the gotchas that bite. WHEN: when you are about to create, package, publish, install, or distribute a Claude Code plugin or marketplace; when the user mentions a plugin, marketplace, 'ship a plugin', 'add it to the marketplace', or a one-off vs shared marketplace; or before touching .claude-plugin/plugin.json or marketplace.json (any of)."
---

# ship-a-plugin — build AND distribute a Claude Code plugin (the full flow)

This is a DEVELOPMENT-FLOW skill: it is the way you make a plugin, the complete set of things that must
be coherent for it to actually install + run, and how you verify it. Read it before any plugin/marketplace
work. Ground truth examples (READ them, don't guess): the canonical multi-plugin marketplace is
`~/.claude/plugins/marketplaces/claude-plugins-official/.claude-plugin/marketplace.json` (207 plugins,
ONE catalog); plugin structure depth is the `plugin-dev:plugin-structure` skill.

## 1. WHAT A PLUGIN IS (the structure — files Claude Code auto-discovers)

A plugin is ONE dir with `.claude-plugin/plugin.json` (the manifest: name = the skill namespace,
`doc-mirror:doc-mirror`). At the dir ROOT (NOT inside `.claude-plugin/`), Claude Code AUTO-DISCOVERS:
`skills/<name>/SKILL.md`, `hooks/hooks.json`, `agents/*.md`, `commands/*.md`, `rules/*.md`, `.mcp.json`.
- **Hooks** must reference scripts via `${CLAUDE_PLUGIN_ROOT}` (set by Claude Code at hook-run time),
  never a hardcoded `~/.claude` path.
- **`bin/` CLIs and loose runtime files are NOT auto-placed** — a manifest can't put a CLI on PATH. That
  is the ONE thing needing a setup step → ship an **install WIZARD skill** (see §3.2).

## 2. HOW A MARKETPLACE ACTUALLY WORKS (the load-bearing correction)

A marketplace is ONE repo with ONE `.claude-plugin/marketplace.json`. That file is a **CATALOG** — a
`plugins[]` list. Each entry has a `source`, and the source is EITHER:
- **in-repo:** `"./plugins/<name>"` — the plugin's files live as a subdir of the catalog repo; OR
- **another repo (reference):** `{"source":"git-subdir"|"url", "url":..., "path":..., "ref":..., "sha":...}`
  — the plugin lives in its OWN repo and the catalog just POINTS at it.

THEREFORE (the things that are NOT true, that cost us a session):
- You do **NOT** merge `marketplace.json`s; naming two the same does nothing. ONE catalog per marketplace.
- A marketplace does **NOT** have to house every plugin's code. Prefer a thin **catalog of references**
  (point at each plugin's own repo) over a fat monorepo that stores everyone's code.
- Do **NOT** make a one-off marketplace per plugin (the noob move). Grow ONE shared catalog; add plugins
  to its `plugins[]`. (Each plugin keeps its own `plugin.json`; only the catalog root has `marketplace.json`.)
- A catalog CAN reference a plugin in a PRIVATE repo — but then only people with access can install it.
  Public distribution ⇒ the plugin must live in a PUBLIC repo.

## 3. THE BUILD → SHIP FLOW (do these in order; each step has a coherence obligation)

1. **Build the plugin** (the §1 structure). De-hardcode EVERY path: resolve `env → ${CLAUDE_PLUGIN_ROOT}
   → a machine-config file the wizard writes → derive`. Zero absolute `/home/...` literals in shipped code.
2. **Ship the install WIZARD skill** for the host-level pieces a manifest can't place: an agent-run,
   NON-destructive skill that runs a slim `install.sh` to put `bin/*` on PATH + write a config recording
   the plugin root, and TELLS THE USER the exact command if the env blocks it. (Pattern: `doc-mirror-install`.)
3. **Commit + push the plugin to its OWN repo** — as you go, never batch. Uncommitted work is vapor; a
   plugin referenced by a catalog must be a real pushed repo (public for public distribution).
4. **Register in the shared CATALOG** — add a `plugins[]` entry whose `source` points at the plugin's repo
   (or `./plugins/<name>` if co-locating). Do NOT spawn a new marketplace.
5. **Install:** `claude plugin marketplace add|update <catalog>` then `claude plugin install <plugin>@<catalog>`.
   These are agent-runnable CLI subcommands (not REPL-only). **GOTCHA: a plugin activates only on RESTART.**
6. **Dogfood (the real test — see §4):** restart, run the wizard, confirm skills load FROM the plugin,
   hooks fire (via `${CLAUDE_PLUGIN_ROOT}`), bins work, search/CLIs resolve the plugin's own data.
7. **De-scatter (replace-before-remove, reversible `mv` to a backup, never `rm`):** remove any old
   hand-installed copies now that the plugin provides them. **GOTCHA: if a persona/skill-sync ALSO ships
   these skills** (e.g. this container's `sync_on_startup` from `/tmp/heaven_data/skills/_defaults.json`),
   you MUST remove them from the sync source too (the `add-to-defaults` mechanism, inverse), or they
   re-sync every boot and the de-scatter is futile.

## 4. HOW TO VERIFY (the only valid test)

Not "the code ran." A plugin is verified when a FRESH boot / a DIFFERENT agent **installs and USES** it,
observed: skills invoke, hooks fire from the plugin path, bins resolve, the wizard places host pieces and
user-falls-back when blocked. Watch it happen; don't trust the report.

## 5. THE GOTCHAS (the exact things that bit us — keep them in front of you)

- Plugin activates on **RESTART** only; you cannot verify the install mid-session.
- **directory-source** marketplace tracks the live source dir (great for DEV — edits show on update);
  **git-source** = a pushed repo (for distribution).
- **Persona/skill-sync collision:** if the skillset sync also delivers the plugin's skills, you get a
  double-load; the real de-scatter is removing it from the sync defaults + source, not just `~/.claude`.
- **Private-repo plugin** = only you can install it; publish needs a public repo.
- **Commit + push every chunk.** The single biggest failure is a day of work sitting uncommitted = vapor.

## CoR (this skill's binding)
When I touch any plugin or marketplace, I FIRST read this flow + the canonical `claude-plugins-official`
catalog. I build the structure, de-hardcode paths, ship the install wizard, commit+push to the plugin's
own repo, register it in the ONE shared CATALOG by reference (never a one-off marketplace, never a code
monorepo), install, RESTART, dogfood by a fresh boot/different agent, then de-scatter replace-before-remove
(including the persona sync source). I never trust "it ran"; I watch it install + run.
