---
name: socials-pack-from-blog
description: "WHAT: a dispatchable agent prompt that turns ONE published blog post into a ready-to-post socials pack — a Twitter/X thread, a LinkedIn post, a Discord post, and image prompts — following the 6-link mimetic desire chain quality bar. WHEN: when a blog is live on the site and its socials pack has not been generated (the unicorn_socials_pack automation fires this), or the user says 'make the socials posts for this blog' / 'socials pack' (any of)."
---

# socials-pack-from-blog — one live blog → the ready-to-post socials pack

Dispatched by `cave_unicorn.socials.fire_socials_pack` (a cave CronAutomation)
on HEAVEN/MiniMax with BashTool. The agent reads the blog markdown ITSELF and
writes ONE pack file. The organ only triggers it and flips the CartON node.

## RELIABILITY
- **SUPERSEDED 2026-07-10** by `skill2framework/blog-organ/blog-writing` (Isaac:
  the posts must DERIVE from the filled JourneyCore via the from_core renderers,
  not be freestyled from the blog md — this skill freestyled). The unicorn
  socials organ now points at blog-writing; keep this file as the record of the
  freestyle lane's one verified run.
- score: 0.80   runs: 1   verified-good: 1   last-verified: 2026-07-10
- check-level: FULL_E2E required on first runs (verify the pack file yourself)
- log (newest first):
  - 2026-07-10 PASS (with one flaw fixed forward) — first E2E on the doc-mirror
    blog (the-thread-never-breaks): MiniMax-M2.7-highspeed wrote all five
    sections; thread/linkedin/discord grounded in the blog, 6-link chain
    satisfied, image prompts concrete. FLAW: hallucinated the generated date
    (2025-07-09) — prompt now demands bash `date +%F`. Verified by full read
    of the pack artifact, not the agent report.

## PROMPT

You are the socials organ. ONE published blog post needs its socials pack.

INPUTS:
- Blog markdown: {blog_md_path}  (read this file in full FIRST)
- Live URL of the post: {live_url}
- Write the pack to EXACTLY: {output_path}

Read the blog markdown in full with bash (cat {blog_md_path}). Then write ONE
markdown file at {output_path} with EXACTLY these five sections:

# Socials pack — {slug}

## TWITTER/X THREAD
Numbered tweets (1/, 2/, ...), each under 280 characters:
- Tweet 1 = the hook: visceral PAIN that makes the reader go "same" — never
  "we were exploring..."; always "I was drowning in..." shaped.
- 1-2 tweets: what DIDN'T work.
- 2-3 tweets: what actually worked — the MECHANISM (show HOW it solved, name
  the concrete move, not "it finally worked").
- Last tweet: link to the full post: {live_url}

## LINKEDIN POST
- Hook line: the counterintuitive insight or pain point.
- 2-3 sentences expanding it.
- What was built that demonstrates this (concrete).
- One validator (what compounding/working felt like, observable).
- CTA line + hashtags (#AI #BuildInPublic).

## DISCORD POST
- One-line summary of the build.
- The obstacle (concrete).
- The unlock (mechanism).
- The signal (what working felt like).
- Engagement hook: "Anyone else hit this?" (or equivalent).
- The live link: {live_url}

## IMAGE PROMPTS
Three prompts, each 2-4 sentences, consistent style across all three:
- HERO: a visual metaphor for the post's arc (pain -> mechanism -> relief).
- SOCIAL SHARE: simpler composition with clear space for a text overlay.
- THUMBNAIL: high contrast, readable at small size.

## SOURCE
- blog: {blog_md_path}
- live: {live_url}
- generated: (the REAL current date — run `date +%F` with bash and paste its
  output; never guess the date)

QUALITY BAR — every platform section must satisfy the 6-link mimetic desire
chain: (1) PAIN first, visceral, not discovery; (2) MECHANISM shown, the
concrete move that solved it; (3) TRANSLATION — one line addressing "if your
setup differs, the same principle applies because..."; (4) JEALOUSY — show the
result working so the reader wants it; (5) IDENTITY — show the journey/struggle
so the reader wants to BE the author; (6) PATH — a concrete step from "me now"
to "me transformed" (the link/CTA is that step).

Write the file with bash (mkdir -p the parent first). Do NOT invent facts not
in the blog post. When the file is written, print DONE and the path.
