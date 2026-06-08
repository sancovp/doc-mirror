# Archive Done Plans Out Of The Active Dir — They Hijack Compaction — NON-NEGOTIABLE

`~/.claude/plans/` is AUTO-INJECTED into every session and every compaction. The harness reads each
`.md` in that directory and injects it with the standing instruction: *"If this plan is relevant to
the current work and not already complete, continue working on it."* A plan that is DONE but still
sitting in that dir does NOT go quiet — it keeps getting injected as live work, and at compaction the
summarizer indexes the whole session around it (a detailed, authoritative-looking plan outweighs the
actual recent work). One stale plan becomes the loudest voice in the room, every time.

## The law

The active plans dir (`~/.claude/plans/`) contains ONLY plans that are still being worked. The moment a
plan is verified DONE (its work landed + verified through the user surface), MOVE IT OUT of the active
dir — do not leave it, do not just delete it.

- Archive (reversible — never just `rm`): `mv ~/.claude/plans/<name>.md ~/.claude/plans_done/<name>.DONE-<commit>.md`
  (put the landing commit SHA in the filename so the corpse is traceable to what realized it).
- After archiving, the active dir should be EMPTY unless a plan is genuinely in-flight. Verify:
  `ls ~/.claude/plans/` → only live plans.

## When to apply

- A plan's outcome landed and you verified it E2E → archive it NOW, on sight, same as any fix-on-sight.
- You rehydrate after a compact and discover the injected plan is already complete (the artifact/tracker
  says it landed) → archive it immediately, then proceed with the REAL recorded next step. Do not work
  the done plan just because it was injected.
- Before a deliberate `self_compact` at a seam → check `~/.claude/plans/`; archive any done plan FIRST so
  the compaction summarizes the real work, not a corpse.

## Why

The compaction-hijack is silent and expensive: the summary comes back "all about" a finished plan, the
next session tries to redo merged work, and you lose the thread of what's actually next. The tell that
this bit you: the rehydrated "next step" is something `git log`/the tracker says already landed. The dir
is a live work-queue, not an archive — keep it that way.
