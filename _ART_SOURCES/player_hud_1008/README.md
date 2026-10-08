# Live player HUD extraction — October 8, 2026

The generated stage themes are now installed in the live game. Original concept
sheets remain unchanged in `../hud_themes_1007/`. The builder crops only their
player assembly, preserving native RGBA pixels, alpha and complete frame borders.
`manifest.json` records the source hashes, crop rectangles and deployed hashes.

Run `python _BUILD_SOURCE/build_player_hud_1008.py` from the repository root to
reproduce the ten registered compact rows. Runtime rows live beside their stage's
enemy HUD in `assets/game/levels/stage_NN/ui/`. The Stage X row belongs to Stage 6
because both optional encounters use that stage's runtime ownership.

`assets/player_hud_1008.js` caches the static assembly, replaces concept sample
labels/icons/counts with existing native fonts and authored game icons, and clips
authored green and red strip samples to actual fractions. It does not generate
new sprites or repaint the stored source images. No shared atlas was repacked.

See [runtime and verification](../../docs/PLAYER_HUD_1008.md).
