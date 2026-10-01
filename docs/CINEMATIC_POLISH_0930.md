# Cinematic polish — September 30, 2026

This pass repairs internal presentation before another trailer shoot. Changes remain local and uncommitted. Preserve the earlier repair, art, and cinematic-director work. No full trailer was rendered and nothing was pushed.

## Changes

- **Stage 7 portal entrance:** the live modular Warden now springs from the original toxic doorway with tucked legs, a 1.12-second arc, an 88-pixel apex, then an impact and brief landing compression. Portal and actor share their starting position, removing the first-frame pop. Existing intro protection remains. The tank miniboss entrance is unchanged. The legacy `walkIn` phase identifier is retained for compatibility; it no longer means a walking animation.
- **Stage 6 storm:** apply one shared dark-blue grade after the completed sky/city/cloud composite. Launch transition and gameplay share the grade. Rain and Yuri's storm darkness cover the whole camera field, including horizontal pan and zoom-out reveals, instead of leaving a bright rectangle.
- **Harrier beams:** use the existing Tempest blue beam core and four-frame lightning reel, connected to each deployed cannon. Remove the floating spherical nozzle effect. The beam's opening ramp, rounded flare, origin, and collision use shared geometry. Warning, expired, destroyed-cannon, and twin-beam safe-lane cases are checked. Attack durations and final widths remain unchanged.
- **Stage 1 review/capture:** the boss debug bookmark now resolves from the current terrain range, placing the fight at the dam. Natural campaign timing and boss balance were not changed.
- **Capture controls:** the local City in the Sky capture controller holds Yuri still and waits for both stealth missiles to curl back close before firing. It destroyed both at approximately 68 game pixels without taking a hit. Boss/miniboss capture setup now retains the encounter stage clock instead of resetting it to the opening sky. These capture files live in `C:/Users/Mike/Documents/New project/trailer-city/`, outside the game repository.

## Verification

- Syntax checks passed for all three changed runtime files.
- `node _BUILD_SOURCE/test_fl.js` reached its final **BUILD OK, 0 ERRORS** banner, exit 0. The pre-change baseline also had zero errors.
- Native Chromium: all nine focused portal, weather, beam animation/collision, dam, and browser-error checks passed. Screenshots were inspected. Portable probe: `_BUILD_SOURCE/probe_cinematic_polish_0930.py` (requires the existing Playwright/shoot.py setup).
- Native helicopter sequence passed on Normal, Hard, and Furious: 2/3/6 sonic volleys, 2/4/5 missiles per side, four full-red warning zones, and 4/4/12 rush legs. Its old probe incorrectly expected the retired eight-missile barrage and cone warnings; the probe now checks current behavior. This pass did not rebalance it.
- Separate live Furious sewer run naturally reached chaingun fire, mortar targets, all leg swipes, jumps and stomps with no browser errors. It took six hits and eventually exhausted lives: this validates attack coverage, not clean trailer play.
- Local render-only readback timings: no beam median 10.3 ms, single 11.3 ms, twin 12.5 ms. This is not a guarantee of full-game frame rate.

Tracked evidence summary: [qa/cinematic_polish_0930.json](qa/cinematic_polish_0930.json). Raw logs and screenshots: ignored `_shots/cinematic_polish_0930/`. The visual isolation probe initializes boss state and protects the player; the separate live-flow and stealth-input checks use normal damage.

## Next trailer shoot

1. Keep the Bullets of Fury logo and dialogue-led stealth opening. Wait until the incoming missiles have curved back close to the pilot; preserve both explosion effects. Do not cut to early continuous gunfire.
2. Film the helicopter at the dam on all three implemented encounter difficulties. Keep the full six-volley Furious sequence and a readable dodge through it. Do not substitute the opening jungle arena.
3. For Stage 7, show the portal leap and impact, then actual chaingun bullets, mortar launches/impacts, jumps and leg swipes. Select frames after the attack fires, not only the warning or entry into an attack state.
4. Use the unified storm grade and cannon-connected animated beams for Stage 6. Keep the correctly timed Harrier flyover and sky encounter clock.
5. Rehearse and review clean native gameplay captures before editing. The sewer coverage test is not suitable as a skillful-play trailer clip. Do not include Stage 8. Preserve the user's City in the Sky music, nine-pilot special-ability coverage, and HAMA ending requirements.

Runtime owners: `assets/game.js`, `assets/stage7_modular_0927.js`, `assets/stage67_review_0929.js`. Existing authored art was reused; no new external art or audio was added. No other gameplay backlog is claimed complete by this pass.
