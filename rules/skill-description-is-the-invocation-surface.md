# A Skill's Description IS Its Invocation Surface — WHAT + WHEN, keyword-dense, no jargon

A skill's `description:` is the ONLY thing seen when deciding whether to invoke it. It is not a summary —
it is the trigger. If the trigger words aren't in it, the skill never fires (this is why correctly-built
skills get ignored). Every skill description is EXACTLY two parts:

## WHAT — what this is, generally, in plain words (every word a keyword/tag)
- State exactly what the skill IS, in the most general plain terms someone would actually SAY.
- NO internal jargon, NO project-coined names, NO codenames that aren't themselves the trigger word
  (e.g. don't say "Metacog Shell" / "World of Skillcraft" — say "agent team", "self-improving team of
  agents"). If a reader wouldn't type the word to ask for this, it doesn't belong in WHAT.
- Treat every word as a keyword/tag — the WHAT is a bag of the terms that should match a request.

## WHEN — the literal trigger condition (any-of)
- Say exactly when to invoke it, as: **"When the user mentions X, Y, or Z; or the situation is <S>"** —
  any of which fires it.
- Name the actual phrases the user says ("when the user says 'metacog team' / 'team' / 'spawn agents'")
  and the situations ("when about to do multi-agent parallel work").
- WHEN is matched against what's happening RIGHT NOW — make it concrete enough to match on sight.

## Format
`description: "WHAT: <plain what-it-is, keyword-dense, no jargon>. WHEN: when the user mentions <a/b/c>, or <situation> (any of)."`
One clean line. No escaped unicode, no doubled "WHAT: WHAT:", no duplicate WHEN clauses, no empty description.

## The test
1. Would the user's actual word for this appear in WHAT? (if not, it won't match — fix WHAT)
2. Does WHEN name the literal phrase/situation that should trigger it? (if vague, it won't fire — fix WHEN)
3. Is there ANY word in the description the user would never say? (delete it — it's noise, not a tag)

## Why
The agent fires skills by matching the request against descriptions. A description full of internal
jargon or vague summary text is invisible to the matcher — so a perfectly good skill sits unused while
the agent improvises (the exact failure: user says "metacog team", skill `soma-metacog-team` exists, but
its description didn't name the trigger, so it never fired). The description is the door; keyword-dense
WHAT + literal WHEN is the only thing that opens it.
