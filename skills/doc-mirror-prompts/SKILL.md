---
name: doc-mirror-prompts
description: "WHAT: the reliability-scored prompt-skill library for getting an AGENT to DO a task. WHEN: you need to dispatch an agent to do a task; or you say 'find / add / score / goldenize a prompt-skill for X' -- from change (dispatch the worker), seework (a gap that is an agent task), or init (the doc-gen team)."
---

# doc-mirror-prompts — the prompt-skill store (the one door)

This is the ONLY Claude-visible skill for a whole library of PROMPT-SKILLS. Each prompt-skill is a
DORMANT skill-package dir under `resources/prompts/<domain>/<subdomain>/<procedure>/` — a searchable
file costing ZERO context, found by SEARCH not the skill matcher. It becomes Claude-visible only if you
deliberately export its dir into a plugin. Search and trust are reliability-gated: GOLDEN (proven) ranks
above EXPERIMENTAL (unproven); GOLDEN is EARNED from logged checks, never asserted.

## THE SHAPE OF EVERY PROMPT (always — never a bare instruction)

Every prompt you author or dispatch = THREE sections, in this order:
1. **PERSONA** — a role wrapper named after the role (`<PersonaName>`, NEVER literal `<GUY>`); a role
   makes the LLM follow instructions more carefully.
2. **CHAINS** — reusable process-priming blocks, included BY PATH (not retyped), every one relevant to
   the task: a CoR to steer reasoning + named chains like `HOWTOCODE:[DRY,YAGNI,read-whole-file]`,
   `CLAUDE-CODE-ONLY:[no flight/waypoint/starsystem/mission]`, `PERSONA-TAG:[tag = role's own name]`.
3. **INPUT REQUEST** — the specific ask, ALWAYS as: *"READ <these lines> in <these modules>, UNDERSTAND
   <these features>, MAKE changes that accomplish <these features> with <these requirements>"* + a path
   to the per-change throwaway-specifics file.

**Compose by REFERENCE, not prose:** *"READ <persona path> + <chain paths> to assemble context, THEN
<input request>."* Let the LLM derive the phase decomposition emergently UNLESS you know the phases from
a previous success — then encode them into the persona/chain. A prompt-skill IS a skill; chains are the
material it is composed of; the store below is where personas + chains + procedures live and mature
(EXPERIMENTAL→GOLDEN). To make a stored prompt-skill auto-visible to a worker, symlink its dir into the
project-local `.claude/skills/` — then the dispatch is just "get X from context; also use this skill."

## To DO something, two moves:

### 1. SEARCH first (the only CLI step)
`docmirror search "<what you need to do>" --corpus prompts`
- A GOLDEN match → DISPATCH it: tell a subagent **"Go read <abs path to the package dir> and apply it
  with these specifics: [k=v, ...]"**. Then VERIFY THE ARTIFACT YOURSELF (the agent's report is a claim;
  the artifact is truth). Then record the trial (step 2.d).
- Only EXPERIMENTAL matches, or none → go to 2.

### 2. If no golden match, AUTHOR one (all LLM-native — no CLI for these)
a. **Scaffold**: create `resources/prompts/<domain>/<subdomain>/<procedure>/SKILL.md` in the FORMAT
   below (golden:false, zeros, empty log). Add `resources/` / `scripts/` subdirs only if the prompt needs them.
b. **Write the prompt — start from CoR upward, complexify only as needed.** Decide the prompt's
   complexity ON THE FLY by climbing only as far as the task forces you (stop at the lowest rung that
   boots reliably — *more control = more particular obstacles; don't over-bind*):
   1. **Floor: a single CoR.** Ask *"does one CoR prompt (one said reasoning chain) accomplish this
      task?"* If yes, write that and stop. (`resources/how-to-write-a-prompt.md` — how to write the block.)
   2. **If not, complexify one rung at a time:**
      - a **sequence of CoRs** (a workflow) or **splice** in attention chains — the C1→C2→C3 guy
        classes;
      - **bind it harder** when the LLM must reliably *decide what to do* mid-task: persona injected →
        persona in the **system prompt + a dovetailed input** — the complexity ladder + binding law in
        `resources/how-to-make-a-persona-prompt.md`;
      - **pack it into a harness** when you must sequence outputs/runs across turns (serve a flow → run
        an agent via a tool → a factory) — `resources/how-to-make-a-harness.md`.
   3. **Test each rung** — it boots reliably or it doesn't. Use the lowest complexity that works.

   Write the chosen prompt into the SKILL.md body under `## PROMPT` (the templated instruction the
   receiving agent reads & follows).
c. **Dispatch** it (same one-line form as above) and **verify the artifact yourself**, E2E.
d. **Record the trial — by editing THIS prompt's own SKILL.md frontmatter** (trials live in the prompt's
   dir; the score is kept current here): append a `log:` line `"<YYYY-MM-DD> PASS|FAIL — <what you
   checked>"`, `runs += 1`, `verified_good += 1` iff PASS, `score = round(verified_good/runs,2)`,
   set `last_verified`. On FAIL: fix the prompt body, keep check_level FULL_E2E.
e. **Goldenize — only when EARNED**: set `golden: true, check_level: SANITY` ONLY IF
   `score >= 0.9 AND verified_good >= 3 AND` no FAIL in the last 3 log lines. Never flip it on a claim.
   Once SANITY, a light sanity check of the artifact suffices instead of full E2E.

## prompt-skill SKILL.md FORMAT (the unit)
```
---
name: <procedure>
domain: <domain>   subdomain: <subdomain>
description: "WHAT: ... WHEN: ..."
golden: false
score: 0.00   runs: 0   verified_good: 0
check_level: FULL_E2E   last_verified: ""
log: []
---
## PROMPT
<the templated prompt the receiving agent reads & follows>
```

The agent's report is a CLAIM; the ARTIFACT is the only truth. Golden = the proven-prompt-system that
a light sanity check is enough for; everything else gets full E2E. (See rules: verify-agent-results-
yourself-not-their-report, prompt-skill-reliability-scoring, commander-not-hands.)

## CoR (this state's binding + transition)

Now that I've read `doc-mirror-prompts`, I will SEARCH the prompt-store for the task; dispatch a GOLDEN
prompt-skill if one exists (else author CoR-first, test E2E, reify + score), and VERIFY the artifact
myself (the report is a claim, not proof). When the artifact exists: if it is a change to a module that
must be re-derived + committed, I `docmirror-cursor set --phase change` and call `doc-mirror-change`;
otherwise (the task is complete, back to the backlog) I `docmirror-cursor set --phase seework` and call
`doc-mirror-seework`. I `journal` the dispatch + the trial result. If the prompt cannot be made to do the
thing and I cannot resolve why (needs Isaac / an irreducible fork): I `journal -t OPEN "<fork + why>"`,
`docmirror-cursor set --phase open`, and `docmirror-sleep` — I call no next; I wait.
