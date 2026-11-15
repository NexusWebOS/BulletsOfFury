---
name: coleforge-walk-run-frames
description: Create or repair consistent whole-character walk and run sprites using proven SpriteCook movement as the pose guide and approved GPT artwork for identity. Use for ColeForge and Elementalist locomotion, body scale, pivots, palettes, Aseprite export and native integration; use a combat skill for attacks.
---

# ColeForge-Walk/Run Frames

## Standing sprite clarity rule

When this work creates, exports, integrates or reviews sprites or raster game art/animation, apply [the ColeForge sprite clarity standard](../coleforge-sprite-clarity/SKILL.md). Blurry or muddy finished frames are not acceptable; use direct master exports and verify the actual animation at its intended game/display size.


Preserve the process Mike accepted in Elementalist on 2026-11-05: **smooth SpriteCook motion + the character's own higher-quality GPT identity + complete drawn figures + calibrated native units**. The accepted set contains 18 fighters, 36 loops and 288 frames. Do not replace this with independent pose invention, assembled character parts, fixed head stamping, or credit-heavy reanimation when the working motion already exists.

## Establish the two references

Inspect the approved full-character identity and the existing working cycle at native size. Read [the accepted Elementalist recipe](references/accepted-elementalist-recipe.md) when working on that project or recovering the original implementation.

- Motion reference: a complete smooth SpriteCook cycle, retaining pose order, alternating contacts, loading, passing, opposite arms and loop closure. The bundled eight-frame guide is available in `assets/motion/` when a project lacks a suitable owned guide.
- Look reference: this character's approved full GPT image, fixing face, hair, outfit, build, head-to-body ratio and palette roles. Another character is only a rendering-quality example.

Use the established walk rendering as an additional appearance reference for the same character's run. For an enemy without its own good cycle, transfer the accepted guide's **motion only**; retain the enemy's original physique and costume.

## Generate coherent complete poses

Use the built-in image-generation tool for GPT raster work. Inspect local inputs first and preserve generated alpha. A coherent full-cycle edit with eight complete figures on a 4-by-2 grid is the proven method here; it supersedes Elementalist's earlier one-pose-per-generation convention for this workflow. These cells hold **whole people**, never interchangeable body tiles.

Assign explicit roles to every input image. Preserve mechanical poses and the same camera, facing and phase order. Keep the character's face readable, with natural head movement and one recognizable identity. Match anatomical limb lengths and torso/head proportions across the set. State which features belong only to the motion guide: remove a guide's coat tails, hair, weapons or footwear when absent from the identity reference. Preserve actual props and bare feet where present.

Use [the proven prompt patterns](references/prompt-patterns.md). Save exact prompts, reference provenance and raw outputs in the project. A nominal 1536-by-768 request may return 1774-by-887; inspect actual dimensions rather than assuming the requested canvas was honored. Reject malformed anatomy, extra garments, incorrect poses or identity drift and regenerate the affected cycle/frame. Do not disguise them with positional tweaks.

## Normalize without size pulsing

Measure the existing standing unit and root from the project's approved native idle. Preserve individual stature; do not make every roster member the same height.

Normalize the **whole source canvas uniformly**, then split fixed cells. Apply one calibration factor to every drawing in an action bank, calibrated to the same character body unit. Compare head, torso and limb lengths across walk and run. Never fit each pose independently to its alpha box. Running naturally projects shorter due to lean and bent legs; it must not enlarge the body to refill the cell.

The supplied guide's run/standing projection ratio is 116/126, and its flight gaps are 4 and 2 native pixels in frames 4 and 8. These are measurements of this guide, **not universal anatomy or timing rules**. Measure another guide rather than applying those numbers blindly. Registration may translate an entire valid figure to a stable pelvis axis and planted-foot baseline. Airborne poses retain their authored flight gaps.

Use generous untrimmed action cells. In the accepted OpenBOR pass, cells are 192-by-192, root (96,167), with standing units 105–130 pixels. Project dimensions override these example values.

## Preserve pixels through export

Read [export and verification](references/export-and-verification.md) for matte cleanup, native palette compatibility, exact milliseconds and runtime integration. Key lessons:

- A generated background may look transparent while retaining nonzero pale alpha. Clear boundary-connected exterior matte, preserving enclosed eyes, white shoe panels and hot flame cores. Inspect detached flames and weapon spikes before clearing debris.
- Reindex new OpenBOR frames to the **existing model palette**; an independent palette for the new action can corrupt colors when the engine uses the model's shared palette. Keep transparent index 0 and hard alpha.
- Keep fixed cells, origins, frame ordering, phases and explicit durations. Store Aseprite durations directly from integer milliseconds when available; conversion through floating simulation ticks previously truncated 120 ms to 119 ms.
- Keep native walk loop periods while distributing phases evenly. Keep established player run cadence; tune new enemy run cadence to movement. A 60 Hz game does not require 60 unique drawings per second.

## Review and integrate

Onion-review previous/current/next, frames two apart and last-to-first at native size and integer zoom. Compare idle, walk and run side by side. Inspect head size, shoulders, hips, hands, knees, soles, clothing, weapons, flame extent, palette and alpha. The provided `scripts/check_locomotion.py` checks export contracts; it cannot establish gait or visual identity.

For Elementalist, review `tools/onion_studio.html?native=fullframe&character=<id>&clip=walk`. Check the native engine at game scale before replacing a shipped action. Load and play every new frame, then verify movement, attacks, deaths and encounter progression. If adding enemy RUN support, verify an actual run-to-walk approach instead of only forcing an animation for a screenshot.

Update the final asset rebuild stage so older exports cannot overwrite the accepted cycles. Preserve a reversible backup and verify installed hashes. Report what was actually generated, integrated and tested; do not treat generation, frame-coverage logs or a height measurement as proof of animation quality.
## Standing retro reference direction

For Mike's 16-bit and retro work, apply the [standing retro art direction](../coleforge-art-direction/references/retro-art-direction.md) automatically alongside this skill. Choose a coherent source family and inspect/use actual images in generation. Preserve this skill's specific source requirements, current character identity, complete authored poses and project camera. The selected arcade styles now supplement the standing sheet libraries without needing to be named again; exact palettes, proportions and timings still come from the current brief/assets.
