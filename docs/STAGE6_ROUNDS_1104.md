# Stage 6 fighter rounds (November 4)

Mike: "enhance the stage 6 new fighters bullets, I can barely see em".

**Cause.** The new Stage 6 fighters (`stage6_airframe_1101.js`, S611) mark their gun rounds
`_s611Ammo='slug'` and drew them from `airframe_1101/slug.webp`. That bank had recoloured its source
(the amber `mgcf_1_2` flame slug, 16x20, in `bof_player_ordnance_projectiles.png`) to pale cyan and shrunk
it to ~13x5 px in a 64 px cell, drawn at 28 px: about 6x2 game px, the same colour as the Stage 6 rain,
the jets' paint and the storm sky.

**Fix.** New last-loaded layer `assets/stage6_rounds_1104.js` (S6R14; `window.S6R14_OFF=1` disables it).
It draws `_s611Ammo` rounds from a new bank built from the SAME source pixels in their own amber,
unscaled (1 source px = 1 game px, ~6x14 px body), with a 1 px dark seat outline added after rotation.
- Builder: `_BUILD_SOURCE/build_s6_rounds_1104.py` writes
  `assets/game/levels/stage_06/enemies/airframe_1101/slug_amber_1104.webp` (32 dirs x 4 frames, 32 px
  cells, pivot 16,16, lossless) and `assets/stage6_rounds_art_1104.js` together. Cell d faces
  pi/2 + d*TAU/32 (`s1aDir`), so the hot head leads in every direction. Frames 1/3 cool the white core
  and drop the tail tip for a one-pixel flicker.
- Draw only: kind, speed, hitbox, owner and S611 socket routing are untouched. The sprite is larger
  than the hitbox, which errs in the player's favour. PFX13 glow/rim/trail and RD13 pips still apply.
- Falls back to the S611 draw until the sheet decodes; preloaded with the Stage 6 load.

**Verification.** `_BUILD_SOURCE/shots_s6_rounds_1104.py before|after|off` films Stage 6 Hard natural
pacing: after = 341 rounds drawn by S6R14, off = S611's cyan slug, zero page errors. Comparison:
`_shots/s6_rounds_1104/compare_crops.png` (top before, bottom after), full frames in `before/`, `after/`.
