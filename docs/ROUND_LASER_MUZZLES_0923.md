# Circular laser muzzle animation — 2026-09-23

Mike requested generated rounded laser muzzle flashes for bosses and players.
SpriteCook GPT 2.5 generated eight transparent frames (14 credits). The source,
prompt, asset ID and normalized frames are in
`assets/game/laser_round_muzzle_0923/`. The builder retains one scale across the
reel and centers every frame at (64,64), preserving the authored pulse size.

The Harrier's active cannon uses the new circular reel at its live nozzle.
Shared boss laser flashes also use it, preserving moving-mount callbacks.
Player held lasers, including the fire/ice infusion branches, use the same reel
with cached palettes that retain the artwork's luminance and white core.
Spaceship lasers flash independently at both existing gun hardpoints. The legacy
traveling laser origin also uses the circular art. Ring pixels composite over
the beam so its white core cannot wash them out. No attack timing or damage
changed, and Harrier lasers remain sequential.

Verification:

- `node --check assets/game.js` passes.
- `_BUILD_SOURCE/probe_harrier_modular_0923.py` passes in real Chromium: one beam
  at a time; independent warnings; flash, beam and gun-tip origins agree within
  0.001 backing-store pixels; orbital motion and all difficulty checks pass.
- `_BUILD_SOURCE/probe_round_muzzle_0923.py` passes: all five held laser tiers,
  fire and ice beams, two spaceship muzzle locations and a moving boss mount.
- Both probes report no page or console errors. Screenshots inspected under
  `_shots/harrier_round_muzzle_0923/` and `_shots/round_muzzle_players_0923/`.
- Full suite completed with exit 1 and 80 existing failures. No new failure
  names compared with the preceding 81-failure baseline; the intermittent
  Stage 1 sand-tank spawn assertion passed this run. Full log:
  `_shots/round_muzzle_suite_final_0923.log`.

Existing uncommitted work was preserved. No commit or push performed.
