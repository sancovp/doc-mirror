# Corrections State What IS, Now — Not Just What It Isn't — NON-NEGOTIABLE

When you correct any document, rule, doc(m), comment, prompt, or concept, the corrected text must
state **what the thing IS now and how it works now**, positively and completely. A correction that
only negates the old claim ("it is NOT an xyz, it does NOT work like this") and stops there is
FORBIDDEN — it leaves the reader with nothing true to act on, only the absence of the old wrong thing.

## The failure mode (banned)

Old text: "The system is an xyz and works like this: ..."
You change your mind.
BANNED correction: "The system is NOT an xyz; it does not work like that." ← leaves a hole. The reader
now knows one false thing to avoid and zero true things to use. They cannot proceed.

## The required shape

Lead with the positive truth; the negation is at most a trailing footnote to stop the old claim
resurfacing:
REQUIRED: "The system is an ABC. It works like this: <the actual current mechanism, file:line-cited
if code>. (It is not the xyz an older note claimed.)"

The test before saving any correction: **if a reader read ONLY my corrected sentence and not the old
one, would they know what the thing actually is and how it works now?** If they'd only know what to
avoid, the correction is incomplete — rewrite it to assert the current truth first.

## Fix on sight — never defer

A discrepancy you can see is a discrepancy you fix NOW, in the file where it lives, before committing
or moving on. Do NOT note "fix this later / capture for the ledger" and commit the wrong text anyway:
that pushes known-wrong content into the record with no guarantee you (or anyone) will ever have the
context to recognize it again before it steers someone wrong. Two narrow exceptions, and only these:
(1) it is a CODE-GAP (the code doesn't do what's wanted) rather than a DOC-ERROR — that is real work
and its home is the progress-tracker queue, which is the backlog, not deferral; (2) fixing it correctly
requires reading code/state you do not yet have — then read it now, do not guess. Otherwise: see it,
fix it, then proceed.

## Why

Two anti-patterns destroy a documentation layer the same way: (a) committing a known discrepancy
"for later" — the later context may never come, and stale-wrong docs steer the next session wrong;
(b) correcting by negation only — the reader is left unable to act, and the real current truth never
gets written down, so it has to be re-derived from code every time. Both turn the doc layer from an
asset into a trap. A correction is only done when the current truth is stated positively, in place,
on sight.
