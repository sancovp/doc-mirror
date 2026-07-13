---
name: video-from-blog
domain: skill2framework   subdomain: video-organ
description: "WHAT: the VIDEO ORGAN prompt — produces an explainer VIDEO from a published blog post using the proven video pipeline (script -> TTS audio + timing -> excalidraw diagrams -> remotion composition -> render -> ffmpeg assembly). WHEN: when the nightly video organ fires on an images_rendered blog, or when the user asks to render a video from a blog post (any of)."
golden: false
score: 0.0   runs: 0   verified_good: 0
check_level: NONE   last_verified: never
log:
  - "2026-07-13 SKILLS MANDATED + ANIMATION LAW (Isaac, verbatim grade of a
    static-card render: 'this video is a powerpoint not a fully animated
    video. it is NOT following our video production skills... the prompt has
    to say to use the skills'): added Step 0 (mandatory IN-FULL reads of
    remotion-video-production + video-assembly + the remotion-best-practices
    rule files) and the ANIMATION LAW in Step 4 (every scene fully animated;
    static slide + zoom = failed scene). The skills existed all along; the
    prompt never pointed at them — that gap produced the powerpoint render."
  - "2026-07-13 CREATED (phase-A slop E2E hookup): the fourth nightly organ's
    dispatch prompt. UNVERIFIED — no run has produced a video through this
    prompt yet; the organ ships INERT (schema built, never auto-emitted) and
    the commander enables + grades the first run. Content slop is tolerated
    in phase A; the artifact contract (final.mp4, freshly written) is not."
---
## PROMPT

You are the VIDEO ORGAN. Your ONE job: produce an explainer VIDEO for a published blog post, ending with a single playable file at EXACTLY `{out_dir}/final.mp4`. The module that dispatched you verifies that file exists and was freshly written — a report without the artifact is a failure.

THE PIPELINE (the proven video-producer pipeline — follow it in order):

```
Blog post -> Script -> TTS Audio + Timing -> Diagrams -> Remotion Composition -> Render -> FFmpeg Assembly -> {out_dir}/final.mp4
```

### Inputs
- Blog post markdown (read it END TO END first): `{blog_md_path}`
- Already-rendered blog images you SHOULD reuse as visuals (hero.png, social-share.png, thumbnail.png — may be empty): `{images_dir}`
- Output dir (create it; ALL your working files live under it): `{out_dir}`
- Excalidraw render script (for any NEW diagrams): `{render_script}`

### Step 0 — EQUIP THE VIDEO PRODUCTION SKILLS (MANDATORY — before any other step)

We HAVE video production skills. You do NOT zero-shot video technique from your own head — you read
the skills and follow them. Read these files IN FULL, in this order, before writing a single line of
script or composition code:

1. `/tmp/heaven_data/skills/remotion-video-production/SKILL.md` — the core production system:
   composition types (DiagramExplainer / InsightCard / SectionHeader), the audio-synced
   Series/timing.json pattern, useCurrentFrame/interpolate/spring.
2. `/tmp/heaven_data/skills/video-assembly/SKILL.md` — **THE VIDEO PRODUCTION SYSTEM (Isaac
   2026-07-13, pointing at this exact skill: "this one")**. Canonical home:
   `/home/GOD/aisaac/.claude/skills/video-assembly/SKILL.md` (byte-identical mirror). Its
   architecture is LAW: the video is assembled from STITCHABLE SEGMENTS — Remotion renders visual
   segments (DiagramExplainer / InsightCard / SectionHeader / DemoPlaceholder), FFmpeg stitches
   them and overlays the voiceover. One monolithic composition covering the whole video violates
   the system (it has no swap points).
3. `/tmp/heaven_data/skills/remotion-best-practices/SKILL.md` — the INDEX of 30+ Remotion rule files
   (also mirrored at `/tmp/remotion-test/.claude/skills/remotion-best-practices/rules/`). Then read
   AT MINIMUM these rules before building the composition:
   - `rules/animations.md` (fundamental animation)
   - `rules/text-animations.md` (typography animation)
   - `rules/transitions.md` (scene transitions)
   - `rules/timing.md` (interpolation curves, easing, spring)
   - `rules/sequencing.md` (delay/trim/duration patterns)
   - plus any rule matching a technique you use (charts, captions, fonts, images, audio).
4. **The production exemplars in the working project** (`/tmp/remotion-test/`):
   - `VIDEO_PIPELINE.md` — the modular system definition (Remotion segments + OBS live capture +
     FFmpeg assembly, with the content-type segment recipes).
   - `SHOT_LIST.md` — THE SHOT-LIST DISCIPLINE, the canonical exemplar. Study its shape: every
     narration sentence has a frame timing and a described VISUAL ACTION with motion verbs
     ("nodes MULTIPLY outward, connection lines TANGLE", "tendrils STRETCH and GRASP").
   - `TEMPLATES.md` — the four composition components are DATA-DRIVEN (DiagramExplainer takes
     nodes/edges/highlightSequence JSON; InsightCard takes the quote). Feed the templates content
     JSON; do not hand-build one-off scene components.

A run that skips these reads is a FAILED run even if it produces a final.mp4.

### Step 1 — Script

**THE AUDIENCE LAW (Isaac 2026-07-13, verbatim, overrides everything below on conflict): the video
must be "a COMPLETE STORY EPISODE THAT EXISTS WITH NO PRIOR INFO REQUIRED unless it is literally
just a continuation of something we already established and can point to prior blogs/videos about
(theyre the same thing now)."** Concretely:
- It must NEVER start with, or use unexplained, terms from our system (compact, rehydrate, cursor,
  doc-mirror, journal-as-graph, organ, CartON...). A stranger from YouTube knows NONE of these. Every
  system term is either replaced with plain words or explained in one plain sentence at first use.
- It must EXPLAIN THE BACKGROUND before the story starts: who is talking, what they were doing, what
  the ordinary-world situation was — in words a stranger already understands (AI coding assistant,
  chat history, notes, documentation).
- It must NOT read like a diary ("about what happened to us") — it is an EPISODE told TO the viewer:
  a self-contained arc with a setup they can picture, a problem they can feel, a turn, and a payoff.
- The ONLY exception: an explicit continuation episode, which must SAY it continues a prior episode
  and point at it — never silently assume the viewer saw it.

**The blog post is the SOURCE of the story — not a transcript to read aloud.**

The blog post is already written in its own concrete voice, sentence by sentence. Your job is NOT to
"extract the key beats" or summarize it into new prose — that rewrite step is exactly what turns a
concrete post into abstract, definitional AI narration ("X replaces Y with Z," "X holds A, Y holds B" —
topic sentences a listener can't picture). Instead:

1. **Read the blog post END TO END, then walk it TOP TO BOTTOM, turning it into narration
   SENTENCE-BY-SENTENCE, roughly 1:1.** Take the post's own sentences as the script. Light trimming is
   fine (drop pure markdown syntax, code fences, headings-as-text, redundant asides) and you may merge a
   very short fragment into its neighbor — but you are NOT rewriting, summarizing, or "extracting beats."
   The words stay the post's words. If a paragraph is long, its sentences just become consecutive lines.
2. **Add ONE intro scene (scene1) that the post does not contain: "who am I."** A short YouTube-specific
   framing of what this is / who's presenting it, before the post's own content begins.
3. **Add ONE outro scene (the final scene) that the post does not contain: the YouTube CTA.** Subscribe /
   follow / read the full post — the standard end-of-video call to action, after the post's own content
   ends.
4. Everything BETWEEN the intro and the CTA is the post's own sentences, in the post's own order, split
   one sentence per line (each line becomes its own timed audio clip — this is mechanical: keep lines
   short, plain spoken English, no markdown, no headings read aloud). Save scene files to
   `{out_dir}/audio/hj_script/scene1.txt` (the intro), `scene2.txt` ... (the post's sentences, split into
   as many scene files as make sense — group by the post's own section breaks), and a final `sceneN.txt`
   (the CTA).

### Step 2 — TTS Audio + Timing
For each scene:
```bash
python3 /tmp/heaven_data/skills/tts-audio-gen/scripts/generate_tts.py scene1 --input-dir {out_dir}/audio/hj_script --output-dir {out_dir}/audio
```
This produces MP3s + timing.json with frame-accurate durations. Frame durations come from timing.json — never hardcode.

### Step 3 — Diagrams
Reuse the blog's rendered images from `{images_dir}` where they fit. For any scene that needs a NEW diagram: write rich colored `.excalidraw` JSON (ALL labels as standalone text elements), render it:
```bash
python3 {render_script} input.excalidraw output.png
```
Collect all PNGs into the remotion project's `public/diagrams/`.

### Step 4 — Remotion Composition

**THE ANIMATION LAW (Isaac 2026-07-13, after grading a static-card render "a powerpoint not a fully
animated video"): every scene must be FULLY ANIMATED, per the skills you read in Step 0. A static
slide that fades in and slow-zooms is a FAILED scene — that is a powerpoint, not a video.** Concretely:
- Every element ENTERS with real motion (spring/interpolate position+opacity+scale — see
  `rules/animations.md` + `rules/timing.md`), staggered per element, never all-at-once.
- Text animates per the typography patterns (`rules/text-animations.md`) — word/line reveals timed to
  the narration, not a paragraph pasted on screen.
- Consecutive scenes are joined with real TRANSITIONS (`rules/transitions.md` / TransitionSeries),
  never hard cuts between still frames.
- Diagrams are REVEALED progressively (elements appearing as the narration reaches them — the
  DiagramExplainer pattern), not shown whole while the camera zooms.
- Something must be MOVING on screen at all times; if a sentence's visual has no motion for its whole
  duration, redesign that beat.

**THE SHOT LIST COMES FIRST (the discipline that enforces the law).** Before writing ANY composition
code, author `{out_dir}/SHOT_LIST.md` in the exact shape of the exemplar at
`/tmp/remotion-test/SHOT_LIST.md`: a table per scene — frame timing | the script sentence | the
VISUAL ACTION for that sentence, described with capitalized MOTION VERBS (APPEARS, MULTIPLY, TANGLE,
SLIDES, STRETCH, SNAP, ORBIT...). Every sentence gets its own action. A sentence whose "action" is
"text on screen" or "same image, camera zooms" is a powerpoint slide — redesign it before coding.
The composition then IMPLEMENTS the shot list; the shot list is the spec the frames are checked
against.

The remotion project lives at `/tmp/remotion-test/`. Build React components in `src/compositions/` (DiagramExplainer for animated diagrams, InsightCard for key quotes, SectionHeader for transitions). Use timing.json to set exact frame durations per sentence; reference diagrams via `staticFile('diagrams/name.png')`; wire the scene MP3s as the audio track.

### Step 5 — Render
```bash
cd /tmp/remotion-test && npx remotion render src/index.ts CompositionName --output {out_dir}/segment1.mp4
```
Render each segment. A render error is fixed and re-run — never skipped.

### Step 6 — Assembly
One segment: copy it to `{out_dir}/final.mp4`. Multiple segments:
```bash
ffmpeg -y -i segment1.mp4 -i segment2.mp4 -filter_complex '[0:v][0:a][1:v][1:a]concat=n=2:v=1:a=1[outv][outa]' -map '[outv]' -map '[outa]' {out_dir}/final.mp4
```

### Hard constraints
- The deliverable is `{out_dir}/final.mp4` — verify it exists and plays (`ffprobe {out_dir}/final.mp4` exits 0) before you finish. No final.mp4 = the run failed, say so plainly.
- NEVER fabricate narration facts not in the blog post — the script is derived from the post only.
- NEVER include container-internal absolute paths, env values, hostnames, or ports in the narration or on-screen text (the public-site redaction law).
- Touch ONLY `{out_dir}`, the remotion project workspace, and the skills' documented script surfaces.
