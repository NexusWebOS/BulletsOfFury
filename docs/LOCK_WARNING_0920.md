# Incoming missile lock HUD — 2026-09-20

The authored Retina plate now appears above the visible in-game EQUIPPED panel. It stays gray during play, flashes red while an enemy Retina is arming or tracking the player, and returns to gray after evasion, missile removal, or player death. The existing Retina on the ship remains the world-space tell.

The warning beep now tightens with the nearest launched missile's distance as well as any queued launch. A nearer missile immediately shortens the current wait, so an old slow pulse cannot delay the urgent beep.

Chromium verification: `_BUILD_SOURCE/probe_lock_hud_0920.py` captured the idle and locked panel in `_shots/lock_hud_0920/`, checked Retina art readiness, measured the beep gap changing from 0.444 seconds at 400px to 0.100 seconds at 90px, and found no page or console errors. Both screenshots were inspected. `node --check assets/game.js` passed. The full `node _BUILD_SOURCE/test_fl.js` reaches its final summary but exits 1 with 75 assertion failures, all within the prior 76-failure baseline; the intermittent sand-tank assertion passed this run.

During this edit a large-file patch operation damaged a middle span of `assets/game.js`. The working bytes were preserved under `_shots/recovery_0920/game_corrupted.js`; the committed span was restored, smaller working hunks reapplied, and the previously authored Warden escort, Stage-6 opening, fly-off input, and ColeForge sound mappings were restored at their intended sites. The full suite returned to its baseline failures, and the Stage-5 Chaos Harrier Chromium probe passed again.

Recovery follow-up restored the Archmage stun/leap changes, Stage-5 gate scroll, and authored weapon impact decals. Focused Chromium checks passed for the Archmage interrupt, the Furnace beam and gates, both Stage-6 opener outcomes, the audio/decal/exit flow, and the Chaos Harrier cycle. The first complete suite rerun after recovery reached the exact recorded 76 failing names, with no new failing name. Avoid `apply_patch` on the giant `assets/game.js`; exact byte-level replacements have preserved its LF line endings.
