# Generated Wind projectile reels

Nine original 16-pose sheets generated with built-in image_gen from the approved
Wind weapon badge identity/material reference. Two additional built-in edits
apply emerald borders to the 45 existing weapon icons. Full exact prompts,
input paths and archived output paths: `generation_outputs.json`.

Shipping pixels live in `assets/game/shared/player_weapons/wind_1011/`. Each
family has 16 independent 256 × 256 transparent cells, a fixed pivot, one shared
proportional scale, and 24 fps playback. The *_registered.png sheets are 1024 ×
1024 technical inspection exports, each a 4 × 4 bank of equal 256-pixel cells.

Rebuild pixels and their owning manifest together:

    python _BUILD_SOURCE/build_audio_fx_1010.py
    python _BUILD_SOURCE/build_wind_projectile_review_1011.py

The raw PNGs and default generated-image originals are preserved. Normalization
only cuts, removes negligible alpha noise, translates, proportionally scales
with nearest-neighbor sampling, and pads the generated pixels. Registration
records source/output hashes, source bounds, physical anchors and scale.

The game and review share `assets/wind_projectile_painter_1011.js`. The preview
has a frame slider, onion overlay, combat painter and native captures. Final
verification is in `docs/feedback/WIND_PROJECTILES_1011.md` and
`docs/qa/wind_projectiles_1011.json`.
