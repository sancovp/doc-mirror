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
- score: 0.90   runs: 1   verified-good: 1   last-verified: 2026-07-10
- check-level: FULL_E2E required on first runs (read blog-aida.md + pack.md yourself)
- log (newest first):
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

INPUTS:
- Source blog/journey markdown: {blog_md_path}  (read it in full FIRST)
- Live URL of the published narrative post: {live_url}
- Output dir (create it): {out_dir}

STEP 1 — read the LIVE field contract (never guess field semantics):
    python3 -m cave_unicorn.journey_suite --contract
It prints every field of journey_core and journey_blog with its description
and whether it is REQUIRED.

STEP 2 — read the source markdown in full (cat {blog_md_path}).

STEP 3 — write {out_dir}/journey_core.json: fill EVERY REQUIRED journey_core
field exactly per its contract description, grounded ONLY in the source (no
invented facts). Also set: blog_url = {live_url}; hook (an AUTHORED hook
sentence); plugin_url / skill_urls / deep_dive_url if the source's links name
them; hashtags.

STEP 4 — write {out_dir}/journey_blog.json: fill EVERY REQUIRED journey_blog
field per its contract description. This is the AIDA-within-AIDA discipline:
each section (hook, topic, personal, main, demo, discuss, cta) is its OWN
Attention→Interest→Desire→Action cycle, and the whole piece is also one AIDA
arc. Voice: natural, personal, "quotidian but polished" — structure invisible,
never formula-sounding. journey_name must match the core's.

STEP 5 — write {out_dir}/image-prompts.md with three entries (HERO / SOCIAL
SHARE / THUMBNAIL), 2-4 sentences each, in DIAGRAM language (zones, shapes,
arrows, labels — the excalidraw pipeline renders these).

STEP 6 — render and self-correct:
    python3 -m cave_unicorn.journey_suite --core {out_dir}/journey_core.json \
      --blog {out_dir}/journey_blog.json --out {out_dir} \
      --image-prompts {out_dir}/image-prompts.md
A validation error means YOUR JSON is wrong — fix the fill and re-run until it
prints rendered. Then read {out_dir}/blog-aida.md once to confirm it reads as
a natural piece.

When rendered and read, print DONE and the artifact paths.
