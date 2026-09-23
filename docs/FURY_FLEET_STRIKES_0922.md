# Fury fleet and ground missile runs — 2026-09-22

## Shipped behavior

Stage 1's four interceptor/bomber variants use newly generated olive and black/crimson hulls. Each has three bank attitudes, eight barrel-roll frames, eight somersault frames, and eight compass headings. Tracking-round evasion alternates a 0.58-second roll and loop, with a 2.8-second cooldown; firing pauses during the maneuver. This adds visible attitudes to the existing dodge movement, without granting invulnerability. Frames preload on spawn. The live renderer does not rotate the hull canvas and keeps one center anchor; shadows follow the selected frame.

The two Stage 1 boats use new intact, damaged (65% HP), and critical (35% HP) plates, alongside the existing anchored burning/explosion system. Dying hulls are not faded over the explosion.

Stage 6 adds south/north/east/west missile-strike passes at 9, 20, 31, 43, 54, 61 and 67 seconds in the authored wave plan. The shared scheduler may delay a pass under pressure. These use the new bomber's cardinal-heading frames and hold one movement axis through entry and exit. They do not slow the stage. The flight clock resets at spawn; generic entry spacing, edge pinning and enemy separation no longer interfere with these passes.

Missiles commit to fixed ground sites near the player, using the shared green/yellow/red perspective reticle and warning HUD. Easy/Normal/Hard/Furious fire 1/1/2/3 missiles per pass, with 1.65/1.45/1.25/1.25 seconds of warning. No more than five strike warnings are active together. An authored missile travels from the bomber to the site, then produces existing burst-explosion graphics, launch/impact sound triggers and screen shake. Collision is a 30-pixel radius, not a full vertical lane. Shooting down a bomber cancels unlaunched missiles; already launched rounds finish their flight.

Roll/pitch evasion is currently used by the Stage 1 fleet. Stage 6 strike runs use the authored heading frames and retain their committed cardinal route.

## Assets and reproducibility

- Runtime art and original sheets: `assets/game/fury_fleet_0922/`.
- 114 transparent 128×128 runtime PNGs: 108 jet frames + six boat damage frames, approximately 1.68 MiB.
- Frame/crop/anchor manifest: `assets/game/fury_fleet_0922/manifest.json`.
- Exact generation prompts: `assets/game/fury_fleet_0922/prompts.json`.
- Generated with the built-in image_gen tool. Separate correction passes preserve interceptor/bomber identity and correct northward diagonal headings.
- Normalizer: `_BUILD_SOURCE/build_fury_fleet_0922.py`. Committed source sheets are used directly when present. Alpha is preserved; connected-component extraction avoids the generated sheets' imperfect grid spacing. All frame edges are transparent.
- Assets register directly in the shared engine; no generated atlas manifests were edited.

## Verification

`node --check assets/game.js` and `git diff --check -- assets/game.js` pass.

Real Chromium probe: `_BUILD_SOURCE/probe_fury_fleet_0922.py`; evidence in `_shots/fury_fleet_0922/`, log `_shots/fury_fleet_probe_final_0922.log`. All 114 images decode; roll/loop progression and zero hull canvas rotations verified; four flight directions hold their axis until exiting; all three Furious missiles impact; all four difficulty volley sizes and warning durations verified; five-warning cap verified; no premature damage, no distant lane damage, one hit per blast; launch cancellation and stage cleanup verified. The actual Stage 6 wave callback also dispatches through the main game loop. No page or console errors. Screenshots of the rendered poses, damaged boats, missiles, warnings and explosions inspected.

These are focused automated gameplay checks, not a complete human campaign playthrough or listening pass. Existing unrelated suite failures remain tracked separately.


Full regression suite completed with exit 1: 75 failures, with exactly the same normalized failure names as the preceding stats/clock baseline. Final log: `_shots/fury_fleet_suite_verified_0922.log`. No commit or push performed during this pass.
