# Level 5 modular Space Blaster form — 2026-09-22

Generated with the built-in image generation tool; prompts are preserved in `assets/game/stage5_archmage_0916/blaster_0922/prompts.json`. Source PNGs remain alongside the normalized frames. Nothing was committed or pushed.

## Assets and integration

- Eight body frames: normal armor expands into a wide braced siege form, then firing recoil and enraged glow. Body is separate from the weapon and has no back-mounted gun.
- Eight weapon frames: four cold rotor attitudes, two hot barrel frames, damaged gun and destroyed gun/debris. Every frame faces vertical south. `manifest.json` records the receiver mount and muzzle anchors.
- Eight effect frames: four blue muzzle flashes, two downward energy rounds and two cooling steam frames. Effects are separate alpha assets.
- The existing chaingun phase now uses this body and separately drawn weapon. It triggers through the existing half-health/hammer-loss logic. Shots launch from the gun muzzle with zero horizontal velocity while the boss moves laterally to track the player.
- The independent gun hit region follows the same mount used to render it. Destroying it stops further chaingun shots and enters the existing enrage/core phase. No separate gun health bar. The retired invisible hammer hit region is disabled while in blaster mode.
- Heat accelerates the firing rate, changes barrel art, stalls into cooldown, then resumes. Cooling steam and muzzle effects use the new sprites rather than procedural placeholders.

## Verification

`node --check assets/game.js`: passed.

`python _BUILD_SOURCE/probe_blaster_0922.py`: passed. Real Chromium, no page/console errors. Checks: south-only velocity, exact emission point, overheat/cooldown cycle, independent module damage without hull damage, no invisible hammer target, destruction and no subsequent fire. Screenshots of transformation, assembled form, firing, hot barrels, steam and destruction were inspected under `_shots/blaster_0922/`.

The full `test_fl.js` run completed with 78 failures; the suite is not green. Comparison with the earlier downloaded-build failure set found two additional names: the second-lance/drone-column assertion (also failed before this change in `_shots/focus_suite_complete_0922.log`) and a randomized road-patrol heading assertion. The latter was not resolved in this art/chaingun pass and must not be presented as a confirmed inherited failure. The full run preceded the final invisible-hammer guard; syntax and the focused browser probe were rerun after that guard.

This is functional/visual verification, not a complete human difficulty playthrough.
