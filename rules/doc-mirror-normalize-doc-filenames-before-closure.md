# doc-mirror: normalize doc(m) filenames before the closure test

When running the doc-mirror population engine (HUD `hud-writer` agents, one per module), the
**default-model (sonnet) writers drift** to the legacy HUD filename `<name>_<ext>_explained.md`
instead of the doc-mirror path `<relpath>.md` — even when the `hud-writer` agent definition says
to use `<relpath>.md` and "NEVER write `{file}_explained.md`". Opus writers comply; sonnet writers
regress to the old habit on a fraction of files.

**The fix (the team leader runs this, idempotent, BEFORE the closure test):**
```bash
cd <repo>/docs/mirror
for f in $(find . -name '*_py_explained.md'); do mv "$f" "${f%_py_explained.md}.py.md"; done
for f in $(find . -name '*_pl_explained.md'); do mv "$f" "${f%_pl_explained.md}.pl.md"; done
# (extend per language extension as needed)
```
Then run the closure test (`comm -3` manifest↔doc-set). Content is correct in the drifted files —
only the filename is wrong, so a rename fully repairs the bijection.

**Why:** the closure test is the gate; a filename-only drift shows up as 15 "missing" + 15 "orphan"
and looks alarming but is a 2-line rename. Normalize first, then closure. For high-fidelity source
modules prefer spawning the writers with `model: opus` (they don't drift); sonnet is fine for bulk
test-file docs as long as the leader normalizes filenames afterward.
