# Skills Reference Canonical Things, Never Random Ones — global rule about making skills

A skill may cross-reference and reference things it makes, and things that ought to exist when it is
being used right. A skill may NOT just be like "oh yeah that was in this dir we made randomly over
here."

## The distinction (this is the whole rule)

- **LEGITIMATE reference** — the referenced thing exists *by the system's design*, so it is guaranteed
  to be there whenever the skill is used:
  - things the skill itself MAKES/produces during its own run;
  - system-canonical anchors that ought to exist when the skill is invoked correctly (e.g. "read the
    repo's `context/progress-tracker.md`", "equip the `doc-mirror` skill", "the `doc(m)` at its computed
    mirror path", another skill by name);
  - the skill's OWN files — its lean `SKILL.md` body + its `resources/` dir.
- **ILLEGITIMATE reference** — the referenced thing exists *by accident*: an arbitrary file dropped in
  some random directory that the skill points at instead of containing the knowledge itself. The tell is
  a `SKILL.md` that is just "go read `<some/path/that/file.md>`" where that file was really the skill's
  DRAFT and should have BECOME the `SKILL.md` content (+ `resources/`).

The test before shipping any skill: **does each reference resolve by the system's DESIGN (canonical,
guaranteed) or by ACCIDENT (a file someone happened to leave there)?** Canonical references are fine.
Accidental ones must be pulled INTO the skill (promote the draft into `SKILL.md` + `resources/`) or
repointed at a canonical location.

## Why

A skill that points at a random external file is half-built — the draft never got promoted into the
skill body. It breaks in two ways that matter:
1. **It cannot be packaged.** When a skill is bundled into a plugin (`skills/<name>/` + its files), an
   external pointer to a repo file dangles — that file is not in the plugin. Every pointer-skill is a
   broken plugin. Skills must be portable: their knowledge travels with them.
2. **It is fragile to normal cleanup.** The random file it points at can be moved, renamed, or deleted
   (e.g. an illegal doc dissolved during a doc-mirror reconciliation) — and the skill silently breaks.
   A canonical anchor (the progress-tracker, a doc(m) path, another skill) does not have this problem
   because the system keeps it in place.

## How to apply

When authoring or reviewing a skill: a lean `SKILL.md` that carries the trigger + the procedure, with
depth in its own `resources/`, and references ONLY canonical/guaranteed things or what it makes. If you
find a skill pointing at a loose draft file, promote that draft into the skill (body + `resources/`),
then delete or repoint the loose file.
