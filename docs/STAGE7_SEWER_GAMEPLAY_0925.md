# Stage 7 sewer gameplay and assets — 2026-09-25

Stage 7 already uses the authored `nst7_master_v3` sewer, animated sludge channels, fourteen armed enemy units, the Overflow Excavator miniboss, and the Toxic Portal Warden's pursuit fight. This pass keeps those encounters and adds environmental pressure outlets to the continuous sewer scroll.

## Pressure outlets

Two new transparent bitmap assets live under `assets/game/stage7_sewer_0925/`: an eight-frame left-facing outlet and a separate amber chevron lane warning. The same outlet is mirrored for right-side channels. Its idle grate stays attached to the moving sewer plate before activation, and its cooled frame remains afterward. Both assets are registered with `XART` and warmed on Stage 7 entry.

Outlets are anchored to seven fixed master rows rather than to screen coordinates. Four fire on Normal, five on Hard, and all seven on Furious. They wait until their pipe reaches the pilot's play area, then show an amber warning strip and charging outlet before the toxic stream extends across one side of the corridor. The opposite lane remains open. Hard and Furious shorten the warning from 1.08 seconds to 0.88 and 0.72 seconds respectively. Each outlet runs once and does not start during the miniboss or boss fight.

The stream's collision interval matches its active animation frames and uses the game's existing `playerHit` path, including shields, pilot invulnerability, and death. Both co-op seats are checked. Charge and release use existing game sounds. The art is rendered above terrain and below enemies and pilots, keeping the ship legible inside the stream.

## Verification

- The first left-side outlet and shield collision were inspected in Chromium at `_shots/s7_sluice_compact_0925/` and `_shots/s7_sluice_collision_0925/`. The live hit displayed `SHIELD DOWN` at the stream location.
- The right-side outlet, persistent idle grate, mirrored warning strip, and shorter Hard warning were inspected at `_shots/s7_sluice_right_0925/` and `_shots/s7_sluice_final_idle_0925/`.
- The outlet also appeared without a forced position during normal Stage 7 playback at `_shots/s7_sluice_natural_0925/`.
- The two generated assets load with HTTP 200; these probes recorded no page, console, or HTTP errors. The exact native image-generation prompts are in `docs/qa/stage7_sewer_asset_prompts_0925.md`.

The final `node --check assets/game.js` and `git diff --check -- assets/game.js` passed. The full `node _BUILD_SOURCE/test_fl.js` run reached its final summary and exited 1 with 82 failures; their assertion names exactly match the recorded 82-failure baseline in `_shots/test_fl_0925_airliner_repeat2.log` (including the intermittent Stage 1 sand-tank assertion). The current log is `_shots/test_fl_0925_s7_sluice_postidle.log`.

The existing sewer plate, enemy and boss sprites, and Stage 7→8 finale remain the authored versions. The outlet art is a new environmental layer; it does not replace or recolor those assets.
