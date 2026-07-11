---
name: blog-writing
description: "WHAT: THE blog writing skill — a dispatchable agent prompt that fills ONE JourneyCore + ONE JourneyBlog (the AIDA-within-AIDA blog format) from a source blog/journey, so the deterministic suite renderer derives the AIDA blog + the twitter/linkedin/discord posts from the single filled core. WHEN: when a blog/journey needs its JourneyBlog AIDA write-up and platform posts (the unicorn socials organ fires this), or the user says 'write the blog' / 'use the blog writer' / 'fill the JourneyCore' (any of)."
---

# blog-writing — fill the Core once, derive everything

The 'fill once, render everywhere' doctrine executed: the agent fills TWO JSON
models against the LIVE field contract; `cave_unicorn.journey_suite` renders
blog-aida.md + pack.md (from_core socials) deterministically. The agent never
hand-writes the rendered output — only the fills.

## RELIABILITY
- score: 0.50   runs: 3   verified-good: 3-by-commander-checklist, 0-by-user-gate   last-verified: 2026-07-11
- (score moves only on the USER GATE — run 3 passed the full commander
  checklist below and is AWAITING Isaac's read; bump on his pass.)
- log (USER GATE, newest — the real gate): 2026-07-10 Isaac REJECTED both runs'
  outputs against the format bar, verbatim: "neither of these look like
  JourneyBlog AIDA fractals -- i dont see the links from the framework and the
  journeycore isnt really present correctly, the stories are not ABOUT the
  literal fucking stuff that happened to me/us... it needs to be
  ARCHIVAL/ARCHAEOLOGICAL -- LOOK AT WHAT FUCKING HAPPENED TO ME AND FUCKING DO
  YOU WANT TO DO THIS YOURSELF!? thats the whole idea." Three defects: framework
  links absent from the render; the core not correctly present; stories generic
  instead of ARCHIVAL. The ARCHIVAL LAW + links requirement are now in the
  prompt (below); renderer-level links section is a merge-time item. My own
  verified-good reads measured grounding, not HIS bar — the user gate outranks.
- check-level: FULL_E2E required on first runs (read blog-aida.md + pack.md yourself)
- log (newest first):
  - 2026-07-11 RUN 5 (cave-unicorn story, scan-lane release run) — HALT-TOOL
    MISFIRE, NO ARTIFACT: the agent worked passes 0-2 perfectly (contract,
    all sources read, canonical core COPIED faithfully) then called
    WriteBlockReportTool as a STATUS note ("blocked_reason: None — all
    sources read, no blockers") right before writing journey_blog.json — the
    block tool HALTS by design, so the run died with zero fills. The module's
    fill-verification caught the ok-report-no-artifact (socials_pack_error on
    the node; nightly-retry semantics intact). HARDENED: explicit
    never-call-a-halt-tool-as-a-status-report law added to FORBIDDEN below.
    Gate mechanics were all correct (hold pre-wire, release post-wire,
    dispatch).
    fills (Isaac, verbatim: "you dont publish the section title the hook
    lmao... its supposed to be in heros journey marketing format!!!" and
    "its not links its literally supposed to be *copy* with CTAs... Link to
    *funnel about that thing*"). The template's mechanic slot names (The
    Hook / Take Action / Links) were leaking into published copy. FIXED at
    the suite render (journey_suite._render_marketing_blog): structure
    invisible, bolded attention leads, closing = the CTA cycle as flowing
    copy ending in ONE funnel link (funnel_url arg; interim fallback
    deep_dive then plugin until funnel pages exist). The agent's FILLS were
    not faulted — this prompt is unchanged by the verdict; the re-rendered
    run-3 artifact goes back to the gate.
  - 2026-07-11 RUN 4 (skilltree deep-dive, the first SCAN-LANE run through the
    framework gate) — MECHANICS PASS, CONTENT DEFECT CAUGHT + STRUCTURALLY
    FIXED: the gate held the node live (framework_missing, zero dispatch),
    released on core-wiring, packed, flipped, and cleared the flag — the full
    hold->release cycle proven on the real graph. BUT the agent RETYPED the
    existing core from memory instead of copying it, corrupting nine fields
    (plah/IKZ/sancopv — a broken URL) despite PASS 2's copy-never-rewrite
    instruction. LESSON: a prompt cannot guarantee byte-fidelity — the module
    now ENFORCES the canonical core over whatever the agent writes
    (cave_unicorn.socials._enforce_canonical_core; only sanctioned change =
    blog_url from live_url when unset; regression-tested). Artifacts repaired
    by deterministic re-render from canonical. The agent's own-authored blog
    fills were clean — corruption only where it transcribed.
  - 2026-07-11 RUN 3 (skilltree, the first framework-backed + archival-law +
    voice-law run) — PASSED the full commander checklist, USER GATE PENDING:
    dispatched via cave-unicorn pack-socials direct mode with existing_core =
    chapters/skilltree/chapter/blog1.journey_core.json (core REUSED INTACT —
    zero fields changed, fill-once held) and 5 deep sources; journey_blog
    GROUNDED 28/28 (tally found in the heaven history, NOT process stdout —
    the run-2 capture nit was aimed at the wrong stream); the marker-skill
    verification claim spot-checked verbatim against
    research/ssri/ship/skilltree-paper.md line 61; cta_* carries all four real
    URLs in prose + the new rendered Links section present; ONE checklist
    fail found+fixed: demo_action said Links below instead of carrying a URL —
    fill patched (plugin + code URLs), deterministic re-render, no agent
    re-run (the two-phase payoff again). Voice law satisfied on read
    (Im-not-a-platform-engineer move, went-through-it-so-you-dont-have-to,
    genuine questions as CTA; no guru/hype). KNOWN renderer nits (merge-time,
    NOT fill defects): TwitterPostSet.from_core hook_tweet = whole boon (way
    over tweet length); reply truncates accomplishment mid-word at 100 chars.
  - 2026-07-11 HARDENING (pre-run-3, no run): THE VOICE LAW embedded from
    integration/cave-discord-fork/VOICE.md (the flagged run-3 item) — explorer
    not guru, look-what-works, invitation not pressure; voice never overrides
    the archival law. Run 3 (skilltree, framework-backed) is the scoring run.
  - 2026-07-10 PASS (run 2 — the MPE-hardened prompt + deep-source pipe): the
    fill provably REACHED into the deep record — blog-aida.md names the four
    enforcement layers, the two-hooks-twelve-rules environment strip,
    docmirror-init, the updated-vs-last_journal cursor split, and the
    written-by-the-dominant-activity actuator doctrine, ALL absent from the
    source blog (they live in SYSTEM.md + the June journal). Verified by full
    read. NITS for run 3: some em-dash punctuation dropped in JSON fills; the
    GROUNDED/INFERRED tally line was cut from the captured output (capture
    full stdout next dispatch, not a tail window).
  - 2026-07-10 PASS — first E2E on the doc-mirror journey: MiniMax filled all
    21 core + 31 blog fields against the live contract; blog-aida.md read in
    full = publishable (each section a real AIDA cycle, voice natural, zero
    invented facts); pack.md from_core renders correct AFTER two LEGACY
    RENDERER bugs the run exposed were fixed in the fork's renderers.py
    (LinkedIn hook interpolated a Python list repr — now uses the core's
    AUTHORED hook per core.py's own doctrine; '#'-carrying hashtag fills
    double-marked — now lstrip'd). The deterministic re-render needed NO agent
    re-run — the two-phase design's payoff. Verified by full artifact reads,
    not the agent report.
  - (created 2026-07-10 per Isaac: "give the agents the right instructions.
    and once you get the right output, make that a skill... thats the blog
    writing skill... then give it to that agent")

## PROMPT

You are the blog writer. ONE journey needs its JourneyCore + JourneyBlog fills.
You fill models; you never hand-write rendered output. Work the passes IN ORDER —
each pass is small and gated. Do not narrate your understanding of these
instructions; the fills and the render are your only output.

INPUTS:
- Source blog/journey markdown: {blog_md_path}
- DEEP journey source (the raw record the blog was derived from — journal/spec
  paths, comma-separated; may be empty): {journey_source}
- Existing filled core to REUSE (path, or the word none): {existing_core}
- Live URL of the published narrative post: {live_url}
- Output dir (create it): {out_dir}

PASS 0 — CONTRACT. Run:
    python3 -m cave_unicorn.journey_suite --contract
This prints every field of journey_core and journey_blog with its description.
The descriptions are the spec; never guess field semantics.

PASS 1 — SOURCE. Read {blog_md_path} in full. If {journey_source} is non-empty,
read EACH listed path in full too — the deep record is where the concrete
details live (real filenames, numbers, quoted moments, the actual struggle).
Your fills must reach INTO this material. A fill that could have been written
without reading the source is wrong by definition — rewrite it.

PASS 2 — CORE. If {existing_core} is a path: load it as journey_core.json,
copy it to {out_dir}/journey_core.json, and only ADD missing optional fields
(blog_url = {live_url} if unset; never rewrite existing values — the core is
filled ONCE upstream). If it is none: fill EVERY REQUIRED journey_core field
per its contract description, grounded only in the sources; set blog_url =
{live_url}; author the hook as one clean sentence (never derived by
string-splitting); set plugin_url / skill_urls / deep_dive_url if the sources
name them; set hashtags (no leading #). Write {out_dir}/journey_core.json.

PASS 3 — BLOG SECTIONS, one at a time, in this order, each derived from the
named core fields plus source specifics:
  1. hook_*      <- status_quo + the_boon (the recognition trigger)
  2. topic_*     <- the_boon + why_this_matters (what this is, why different)
  3. personal_*  <- status_quo + obstacle (the lived moment — use a CONCRETE
                    detail from the deep source: a filename, a timestamp, a
                    number, the actual failing thing)
  4. main_*      <- overcome + the_boon (the mechanism, named concretely)
  5. demo_*      <- demo_description + accomplishment (what seeing it proves)
  6. discuss_*   <- universal_application (the question that maps it onto the
                    reader's own domain)
  7. cta_*       <- accomplishment + the links (the one concrete next step)
Each section is its OWN Attention->Interest->Desire->Action cycle, and the
whole piece is one AIDA arc. Voice: natural, personal, quotidian-but-polished —
structure invisible, never formula-sounding. journey_name matches the core.

THE ARCHIVAL LAW (Isaac, verbatim — this is the whole idea): the story must be
ARCHIVAL/ARCHAEOLOGICAL — "LOOK AT WHAT FUCKING HAPPENED TO ME AND FUCKING DO
YOU WANT TO DO THIS YOURSELF!?" The sections are ABOUT the literal documented
events from the deep source: real dates, real filenames, real error messages,
the actual moment it broke and the actual moment it worked — receipts, not a
story ABOUT the kind of thing that happened. If a paragraph could describe
someone else's project, it is not archival — rewrite it from the record. The
JourneyCore must be PRESENT in the piece: the reader should be able to point at
where status_quo, obstacle, overcome, accomplishment, the_boon each literally
appear. The cta_* and demo_* sections MUST carry the ACTUAL LINKS from the core
(plugin_url, deep_dive_url, skill_urls, blog_url) written into the text — a
JourneyBlog with no framework links is invalid.

THE VOICE LAW (the canonical content voice; source of truth:
integration/cave-discord-fork/VOICE.md — "Every JourneyCore should be written
in this voice"): Position = enthusiastic explorer, never expert guru. Frame =
"look what works", never "here's my system". Energy = genuine excitement,
never hype. Accessible = "I'm not X but I can Y". CTA = invitation, never
pressure. The formula a section leans on: credit/appreciate what inspired it
-> "I'm not X but" -> "here, look" -> "isn't that nice?" -> concrete benefits
-> soft invitation. FORBIDDEN tones: guru mode ("I have the answers"),
technical flex ("here's my complex system"), humble brag ("I accidentally
built..."), hype ("THIS CHANGES EVERYTHING"). Never claim an example already
solves the reader's problem — frame it as an investigation that worked. The
voice never overrides the ARCHIVAL LAW: the excitement is ABOUT the literal
documented receipts.
Write {out_dir}/journey_blog.json.

PASS 4 — GROUNDING GATE. For EACH filled field, classify GROUNDED (you can
point at where in the sources it comes from) vs INFERRED. If any hook_*,
personal_*, main_*, or demo_* field is INFERRED, or any field reads like
generic marketing that fits any product, REWRITE it from the sources before
proceeding. Report the final GROUNDED/INFERRED tally per model in one line each.

PASS 5 — IMAGE PROMPTS. Write {out_dir}/image-prompts.md with three entries
(HERO / SOCIAL SHARE / THUMBNAIL), 2-4 sentences each, in DIAGRAM language
(zones, shapes, arrows, labels — the excalidraw pipeline renders these), each
depicting a mechanism from the core (never a generic tech illustration).

PASS 6 — RENDER + SELF-CORRECT. Run:
    python3 -m cave_unicorn.journey_suite --core {out_dir}/journey_core.json \
      --blog {out_dir}/journey_blog.json --out {out_dir} \
      --image-prompts {out_dir}/image-prompts.md
A validation error means YOUR JSON is wrong — fix the fill and re-run until it
prints rendered. Then read {out_dir}/blog-aida.md once end-to-end; if any
section fails the grounding gate on read-back, fix the fill and re-render.

FORBIDDEN: inventing facts absent from the sources; hand-editing blog-aida.md
or pack.md (fix the FILL and re-render); leaving a required field templated
("...", TBD, placeholder); summarizing these instructions back instead of
executing them.

NEVER CALL A BLOCK-REPORT / HALT TOOL AS A STATUS REPORT. If your loadout
carries WriteBlockReportTool (or any blocked/halt tool): calling it HALTS the
run permanently — it is NOT a progress note. Use it ONLY when a real external
blocker makes every remaining pass impossible (a source file missing, the
render command absent). "No blockers, about to write the fills" is NEVER a
block report — the next action is simply WRITING the fill files.

When rendered and read, print DONE, the GROUNDED/INFERRED tallies, and the
artifact paths.
