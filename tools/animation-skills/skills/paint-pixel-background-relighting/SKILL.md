---
name: paint-pixel-background-relighting
description: Create a registered warm-lit variant of a fixed pixel-art background from a marked source image, retaining unchanged pixels outside the lit surfaces.
---

# Paint a fixed background lighting variant

Use for a known effect location, such as the demonstrated explosion on a canyon floor. A relit copy is tied to that location and geometry; it is not a general moving-light solution.

Use [references/relight-prompt.md](references/relight-prompt.md) for the exact prompt. Scripts and sample images are MIT copies from [Kasperzack Games](https://github.com/kasperzackgames/chatgpt-pixel-effects), revision d25ce128ac5f2487e8187d0f1c6f4ac27dced599. Preserve LICENSE. Install requirements.txt in a workspace environment. Write outputs to the workspace, using absolute paths when running outside the skill directory.

1. Mark the intended light source in a 5x enlarged copy: `python scripts/make_marked_input.py assets/canyon.png 196 154 WORKSPACE/marked_x5.png`. The example's ground point is (196,159); its visible marker is five pixels above it. Replace these for the current scene.
2. Inspect and attach the marked image to an available image editing tool. Ask for exactly the same composition, grid, geometry and framing, changing only the lighting. The warm light source is implied: do not draw the blast or marker. Name the actual scene parts to preserve, especially dark sky and distant mist. Keep the original image separately.
3. Clean a candidate: `python scripts/make_lit.py assets/canyon.png WORKSPACE/relit.png WORKSPACE/lit.png`.
4. Compare: `python scripts/compare_lit.py assets/canyon.png WORKSPACE/lit.png --out WORKSPACE/compare.png`. A ready input is `assets/canyon_relit.png` when testing without generation.

The cleanup retains warmer pixels, rejects darkening and grey haze, removes tiny warm groups and restores original pixels elsewhere. Inspect the actual output for unwanted changed areas; a warmth test is not a semantic sky mask. Use a native-size explicit white-allowed/black-protected mask to lock protected areas. Require best_shift [0,0]; regenerate misregistered/cropped geometry rather than hiding it with lighting. Canyon-specific changed-pixel percentages (10.9% current cleanup, 12.8% earlier video copy) are examples, not universal thresholds.

For authored-sprite projects, bake accepted background variants and any graded transition frames offline; runtime selects authored frames. Keep original pixels bit-identical outside the accepted mask. The creator's radial blend/dither shader and synthetic tint fallback are reference techniques, not permission to introduce runtime tinting or shaders into a project with authored-only graphics. Preserve each project's rendering contract.

Inspect at native resolution and intended display size: no marker, added explosion, shifted rocks/stars, sky haze, seams or blurred pixels. Record the prompt, source image, accepted mask, registration and changed-pixel metrics. Use the sibling `stage-pixel-effect-impact` workflow to time the authored variants against the fire stage.
