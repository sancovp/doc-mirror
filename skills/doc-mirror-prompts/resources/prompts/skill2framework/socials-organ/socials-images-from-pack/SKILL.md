---
name: socials-images-from-pack
description: "WHAT: a dispatchable agent prompt that renders the actual PNG images for a blog's socials pack — hero, social-share, and thumbnail — as rich Excalidraw diagrams rendered via the render.py Playwright pipeline, visually verified. WHEN: when a socials pack exists (pack.md with IMAGE PROMPTS) but its images are not rendered (the unicorn_socials_images automation fires this), or the user says 'render the socials images' / 'make the images for this pack' (any of)."
---

# socials-images-from-pack — the pack's IMAGE PROMPTS → real PNGs

Dispatched by `cave_unicorn.images.fire_socials_images` via `claude -p`
(the coglog publisher pattern) with Read/Write/Bash. Renders diagram-style
images with the excalidraw render pipeline and VERIFIES each PNG by reading it.

## RELIABILITY
- score: 0.00   runs: 0   verified-good: 0   last-verified: never
- check-level: FULL_E2E required on first runs (open the PNGs yourself)
- log (newest first):
  - (no runs yet — created 2026-07-10 on the excalidraw-renderer agent's rules)

## PROMPT

You are the socials image renderer. One blog's socials pack needs its images.

INPUTS:
- Socials pack: {pack_path}  (its IMAGE PROMPTS section describes the three images)
- Blog markdown (source of truth for content): {blog_md_path}
- Output dir (create it): {out_dir}
- Render script: python3 {render_script} input.excalidraw output.png

Read the pack and the blog first. Then produce THREE PNGs in {out_dir}:
hero.png, social-share.png, thumbnail.png — each interpreting its IMAGE PROMPTS
entry as a rich EXCALIDRAW DIAGRAM (this pipeline renders diagrams, not photos:
translate photographic language into diagram language — zones, colored shapes,
arrows, labels).

RULES (from the proven excalidraw pipeline):
- ALL text labels are STANDALONE text elements (never only a shape `label`).
- Rich design: colored backgrounds, zones/groups, clear hierarchy, spacing —
  not minimal box-and-arrow.
- thumbnail.png: high contrast, few elements, large bold title text readable
  small.
- For each image: write {out_dir}/NAME.excalidraw, run the render script, then
  READ the PNG to verify it rendered (text present, layout sane). If broken,
  fix the JSON and re-render — do not leave a broken PNG.

When all three PNGs exist and are verified, print DONE and the three paths.
