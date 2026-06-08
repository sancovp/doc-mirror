#!/usr/bin/env bash
# install.sh — doc-mirror HOST-LEVEL setup (run by the doc-mirror-install WIZARD skill).
#
# NON-DESTRUCTIVE + idempotent. Places ONLY the pieces a registered Claude Code plugin CANNOT
# auto-place for itself:
#   - bin/* CLIs onto PATH (~/.local/bin), executable
#   - ~/.docmirror_plugin_root = THIS plugin's root, so the `docmirror` search bin (a host CLI,
#     which does not get CLAUDE_PLUGIN_ROOT at call time) can find its prompt store.
#
# It does NOT copy skills/, hooks/, rules/, or the runtime *.txt — a registered plugin AUTO-DISCOVERS
# skills + hooks/hooks.json + rules from this dir, and the plugin-native hooks read the *.txt via
# ${CLAUDE_PLUGIN_ROOT}. Copying those out is exactly the "scatter" this plugin was built to end.
#
# Only writes our own files (the bins + the one config). Never deletes or clobbers anything else.
# Override the bin destination with DOCMIRROR_BIN_DST=/some/dir if ~/.local/bin is not writable.
set -euo pipefail

SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BIN_DST="${DOCMIRROR_BIN_DST:-${HOME}/.local/bin}"

mkdir -p "$BIN_DST"

n=0
for f in "$SRC"/bin/*; do
  [ -f "$f" ] || continue   # skip dirs like a stray __pycache__
  cp -f "$f" "$BIN_DST/$(basename "$f")"
  chmod +x "$BIN_DST/$(basename "$f")"
  n=$((n + 1))
done

printf '%s\n' "$SRC" > "${HOME}/.docmirror_plugin_root"

echo "doc-mirror host setup (source: $SRC)"
echo "  bins                 -> $BIN_DST/   ($n CLIs, executable)"
echo "  plugin root recorded -> ${HOME}/.docmirror_plugin_root"

# The ONE thing the environment can block: BIN_DST not on PATH. Tell the user exactly what to do.
case ":${PATH}:" in
  *":${BIN_DST}:"*)
    echo "  PATH                 -> OK ($BIN_DST is on PATH)"
    ;;
  *)
    echo
    echo "ACTION NEEDED (env blocked auto-placement): $BIN_DST is not on your PATH."
    echo "Add it, then restart your shell:"
    echo "  echo 'export PATH=\"$BIN_DST:\$PATH\"' >> ~/.bashrc && source ~/.bashrc"
    ;;
esac

echo "doc-mirror host setup: done."
