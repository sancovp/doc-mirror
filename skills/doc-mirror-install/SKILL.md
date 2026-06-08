---
name: doc-mirror-install
description: "WHAT: the install/setup WIZARD for the doc-mirror plugin — it places doc-mirror's command-line tools (journal, vision, cursor, commit, search) on your PATH and records where the plugin lives, performing the host setup itself and telling you exactly what to run if the environment blocks it; non-destructive. WHEN: right after installing or enabling the doc-mirror plugin (first-time setup), or when a doc-mirror command is 'command not found', or when 'docmirror search' cannot find its prompt store (any of)."
---

# doc-mirror-install — the install wizard (run once, right after enabling the plugin)

This is a **WIZARD**: *you (the agent) perform the host-level setup yourself*, verify it at the surface,
and — only if the environment blocks you — tell the **user** the exact command to run. It is
**non-destructive**: it places doc-mirror's CLI tools on PATH and records where the plugin lives. It
writes only those, and deletes nothing.

## Why this exists (what a plugin can and can't place for itself)

When the doc-mirror plugin is enabled, Claude Code **auto-discovers** its `skills/`, `hooks/hooks.json`,
and `rules/` straight from the plugin dir — those need no setup. Exactly two things a plugin manifest
cannot place, which this wizard handles:

1. the **`bin/` CLIs** (`journal`, `vision`, `docmirror-cursor`, `doc-mirror-commit`, `docmirror search`,
   `plan`, `projects`, `tracker`, `docmirror-sleep`, …) must be on your PATH to be invocable;
2. the **`docmirror` search bin** runs as a host CLI (it does **not** receive `CLAUDE_PLUGIN_ROOT` at
   call time), so it needs `~/.docmirror_plugin_root` written to find the plugin's prompt store.

## Do this

1. **Find the plugin root.** It is the grandparent of THIS skill's directory — this skill lives at
   `<plugin-root>/skills/doc-mirror-install/`. (If `$CLAUDE_PLUGIN_ROOT` is set in your shell, that is
   the plugin root.) Confirm `<plugin-root>/install.sh` exists.
2. **Run the setup script** (non-destructive + idempotent — safe to re-run):
   ```bash
   bash "<plugin-root>/install.sh"
   ```
   Read its output: it reports where it placed the bins, that it recorded the plugin root, and whether
   your PATH needs an edit.
3. **Verify at the surface** (do NOT trust step 2's report — check the artifacts):
   ```bash
   docmirror-cursor show                                       # a bin resolves on PATH
   docmirror search "doc-mirror" --corpus prompts --limit 3    # the search bin finds the plugin's prompts
   ```
   Both must succeed. "command not found" means PATH isn't updated in this shell yet.
4. **If the environment blocked you, TELL THE USER** (never silently fail — that is the whole point of a
   wizard):
   - PATH not updated → give them exactly:
     `echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc && source ~/.bashrc`, then re-verify.
   - `~/.local/bin` not writable → have them re-run with a writable dir and add it to PATH:
     `DOCMIRROR_BIN_DST=<dir> bash "<plugin-root>/install.sh"`.

## Done when

`docmirror-cursor show` and `docmirror search … --corpus prompts` both work in a fresh shell. doc-mirror
is now operable — start any session with the **`doc-mirror-boot`** skill, which cascades everything else.
