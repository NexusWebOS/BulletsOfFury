# Stage 5 whirlwind, static stun and second-half attacks

Mike requested a longer accelerating whirlwind across the arena, a repeated-hit hammer disarm with visible electrical stun, and improved phases below 50% health.

The whirlwind now performs two full-arena crossings on Normal, three on Hard and four on Furious. Each pass travels and spins faster. World-space endpoints cover the arena even when the player pans the camera. A shared warning marks the next horizontal danger band before the initial pass and every reversal; each lane commits before motion. Normal/Hard then recover. Furious proceeds into the existing two orbital strikes with their lowered idle and wind-up poses intact.

Ordinary body or hammer hits during the spin/reversal count toward disarm: four on Normal, six on Hard, eight on Furious. Impacts are spaced by a 0.12-second guard so simultaneous pellets or beam ticks cannot instantly exhaust the count. Missiles contribute two, and exhausting the weapon's existing HP also disarms it. Disarm immediately cancels the whirlwind and knocks away the authored single-headed hammer. The boss recoils toward the upper arena, kneels for five seconds with twelve animated static frames, and takes double damage. Healthy recovery returns the hammer and resumes the existing strike sequence. Crossing 50% during stun preserves the reward window before transformation.

Below half health the boss completes the current committed action/recovery before transforming; it does not abruptly remove an earned stun. The intact cannon phase now alternates:

1. Warned horizontal cannon rakes, with regular gaps in the stream.
2. Exposed cooling windows.
3. Marked laser-column casts: three columns on Normal, four on Hard, five on Furious. They follow early, commit, then fire.
4. The charged chromium beam, retaining its side escape lanes.

This rotation advances deterministically, replacing the former repeated tracking-cannon loop and random Furious-only spell branch. The cannon remains separately targetable and breakable, including during its warning/cooling windows. Once broken, the existing core/enrage transition leads into warned twin-gun rakes, beam attacks, and marked columns. Twin-gun fire is confined to downward arcs and gets faster by difficulty; it no longer fires unannounced through a full-circle spin while snapping between sides.

Generated assets use the built-in image tool, copied with their RGBA unchanged:

- `assets/game/stage5_archmage_0916/combat_0926/stun_static.png`: twelve static-discharge frames. Exact prompts and source: `docs/hammer_static_art_0926.json`.
- `assets/game/stage5_archmage_0916/combat_0926/arsenal_cast.png`: eight casting poses matching the corrected blue-reactor armor. Exact prompt and source: `docs/hammer_cast_art_0926.json`.

The new cast reel replaces the mismatched old red spell plate in live casts. Spell/beam markers sit above the radar and bottom HUD; beam damage and its full-height visual remain aligned with the warned columns.

The focused Chromium probe is `_BUILD_SOURCE/probe_hammer_overdrive_0926.py`. It checks every difficulty's crossings, acceleration, all eight spin views, native player-bullet disarm collisions, double damage, stun visibility, threshold deferral, intact-cannon rotation, broken-cannon rotation, warnings before fire, difficulty-specific column counts/speeds, contact vs. safe space, all twelve static frames, and reticle clearance. Existing strike and orbital regression coverage is in `probe_hammer_consistency_0926.py`.

The review page is `_shots/hammer_overdrive_0926/review.html`, with recordings for crossings, disarm/static, below-half arsenal, and broken-cannon core. These use an invulnerable pilot, selected attack/health fixtures and muted audio. Disarm footage injects ordinary player bullets through the real collision path; it is a repeatable mechanic demonstration, not an unassisted campaign clear.

Verification completed on the final build:

- Syntax passed. Full suite completed with **4,957 passing assertions, zero failures, exit 0**, matching the incoming zero-failure baseline. Log: `_shots/test_fl_hammer_overdrive_0926_verified.log`.
- The new real Chromium probe passed every case on Normal, Hard and Furious, with **zero page/console errors**. Report: `_shots/hammer_overdrive_0926/report.json`; execution log: `_shots/hammer_overdrive_probe_0926_verified.log`.
- Existing hammer consistency/orbital probe passed again after the final changes: `_shots/hammer_consistency_after_overdrive_0926.log`.
- Inspected final screenshots and samples from all relevant recordings, including the live disarm with camera motion, full-arena whirlwind passes, new casting pose, visible column reticles, and cannon/beam rotation.
- `assets/game.js` remains LF; `_BUILD_SOURCE/test_fl.js` remains CRLF. Diff whitespace check passed. No unrelated test assertion was changed.

No commit or push.
