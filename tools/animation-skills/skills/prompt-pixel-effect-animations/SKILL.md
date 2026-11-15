---
name: prompt-pixel-effect-animations
description: Prompt for anchored pixel-art effect animations such as explosions, lightning, beams, fire pillars and eruptions; use for GIF motion briefs and reusable effect prompts.
---

# Prompt pixel effect animations

Use the creator's exact prompts in [references/prompts.md](references/prompts.md), choosing the effect requested. These are effect animations, not a proven character walk/combat pipeline. Preserve the current project's art direction and approved identity.

Specify a static camera, a fixed point in every frame, frame count and durations, and an ordered action sequence. Ground effects touch bottom centre; beams start at left mid-height. Do not include the ground, mountain, caster or background scenery in the isolated effect. Leave room above and beside flames; a beam reaching the right edge is intentional only if its endpoint is hidden at a clash/contact point.

The demonstrated detail phrase asks for art pixels only 2–3 image pixels wide. Treat it as a generation request, not evidence of a real grid. Inspect the actual output: requested 512x512 may return about 300x300. Flat magenta #FF00FF supports warm effects; use green #00FF00 for violet lightning so keying preserves violet. No text or borders.

Check the available generation tool's actual capabilities before calling it. The video uses ChatGPT animated GIF generation; a still-image tool does not automatically support GIF output. If only still generation is available, offer an explicitly labelled sprite-sheet adaptation with the same ordered poses and fixed cells. Do not claim that one still is an animation or that copied example frames are newly generated. Do not invent undocumented model options.

Keep exact submitted prompts, raw files, output dimensions, frame durations and generation settings. Reject clipped flames, camera motion, wandering anchors and coarse blobs. Retry the specific defect; after two unsuccessful revisions show the best result and describe what needs changing.

For cleanup use the sibling `clean-pixel-effect-gifs` skill. One-shot explosions finish empty; eruptions need a separately tested sustained loop. The creator's eruption request loops frames 6–16 (one-based), but the shipped usable loop is frames 8–15 (zero-based); inspect the seam rather than assuming the prompt succeeded.

Source: Kasperzack Games, [chatgpt-pixel-effects](https://github.com/kasperzackgames/chatgpt-pixel-effects), MIT, revision d25ce128ac5f2487e8187d0f1c6f4ac27dced599. The 111-second user-supplied video demonstrates the explosion and relight excerpts. The linked kit supplies the complete prompts and four additional effect examples. See LICENSE.
