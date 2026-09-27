# Stage 5: interruptible Chromium empowerment and recovery

After the chaingun breaks, the boss raises his approved single-headed hammer. Lightning charges it and the entire held weapon shakes and pulses. His chest reactor then brightens and sends a pixel-stepped glow outward through his armor, arms and legs. This supersedes the earlier bottom-to-top reveal. Armor, held hammer and health gauge share a cyan, silver and green color cycle. Existing authored plates supply the silhouettes; no replacement boss or procedural sprite was introduced.

## Recovery and counterplay

- Lightning arrives 1.25 seconds into the raise and follows the shaking hammer tip. The hammer charges first; 0.35 seconds later, a two-second reveal spreads outward from the chest reactor.
- Actual HP restores **25% of maximum HP over six seconds**, capped by available missing health. A pulsating **red segment without text** shows the remaining amount ahead of the current HP. Body damage still counts during charging.
- The raised hammer is a Retina target and accepts ordinary bullets, space bullets and Retina missile damage. Its core has `ceil(24 * DIFF.eHp)` health.
- Breaking that core immediately removes the pending segment and revokes **all HP already granted by this charge**, preserving unrelated body damage. The weapon erupts using the shared engine explosion, tinted specifically for this Chromium burst, with authored burst/static art.
- The boss loses empowerment and enters a **four-second stun** with doubled body damage. His hammer cannot be targeted while absent.
- A **2.4-second recovery animation** stands him up, reforms the hammer from its grip, repeats the chest-origin armor glow, and lowers the restored weapon. The cancelled heal does not restart. He resumes the charged slam/spike and counterable throw sequence.
- If charging succeeds, he lowers the hammer and resumes attacks after the heal. A heal never runs again during the same empowerment transition.

Revoking temporary healing can finish the boss if damage during the charge already consumed his original remaining HP. Recovery bookkeeping tracks HP actually granted, so cancellation does not undo player damage or remove more healing than was received.

## Rendering and integration

`hammerStormStart`, `hammerRecoveryTick`, `hammerRecoveryBreak` and the storm state machine own the transition. The existing missile/Retina and direct head-hit paths damage the same core. `hammerHeadPoint` follows the visible hammer jitter.

`hammerChromiumPoseDraw` reuses the authored charge, strike and throw reels. Cached palette variants preserve alpha, dark outlines and luminance. Following Mike's handle correction, the raised head, complete shaft/hilt and gripping hands move as one assembly, including the portion in front of the helmet. A 32-source-pixel flex band joins that motion to the anchored torso instead of leaving the lower handle stationary. The hammer's pulsing glow follows the complete shaft. During rebuilding, its authored pixels reveal upward from the grip. Hit flashes render above the empowerment layers and remain visible. Source PNGs and atlases are unchanged.

`hammerRecoveryBarDraw` fills only the pending recovery interval in the existing boss gauge. Its pulse shares the boss's clock, while its fill and glow stay red (`#ff3030`); no label is drawn. It clears on interruption or completion. The core's explosion is tagged individually for a matching Chromium palette; other engine explosions retain their existing rendering.

The full-width round warnings, framed signs, world-wide Retina row, faster Hard/Furious spikes, fixed-world eased return and warning-free hammer throws from the previous passes remain.

## Verification

- Syntax passed: `node --check assets/game.js`.
- Final full suite: **5,083 passing assertions / 0 failures**, exit 0 and final success banner. Previous baseline: **5,048 / 0**; no new failing names. All three full-suite runs during this pass exited 0. Final log: `_shots/test_fl_chromium_recovery_0926_verified.log`.
- Added 35 assertions for all three difficulties, gradual healing, interruption accounting with simultaneous body damage, core targeting, stun damage, rebuilding without a second heal, capped recovery and lethal cancellation.
- Real Chromium verified **nine interruption routes** (three difficulties × ordinary/space/Retina damage) and three completed heals, each granting exactly 25% of maximum HP in the no-damage fixture. It also checked palette differences, hammer jitter, hit-flash pixels, recovery-segment bounds, changing pulse opacity and complete segment removal after cancellation.
- Existing storm regression checks passed on all difficulties: counter routes, full world row, both camera edges, escape/collision coverage, spike warnings and recovery paths. No page or console errors in either probe.
- Durable evidence: [recovery results](qa/hammer_chromium_recovery_0926.json) and [storm regressions](qa/hammer_chromium_regression_0926.json).
- Inspected screenshots and contact sheets from two approximately 20-second real game-canvas recordings at `_shots/hammer_chromium_recovery_0926/review.html`. Chromium confirmed both video files, all preview images and zero preview page/console errors.

These recordings use controlled, invulnerable, muted fixtures with unrelated asteroid spawns suppressed. The interruption clip inserts a decisive hit through the native Retina missile damage route; it is not a demonstration of a manually fired missile's full flight. Separate native checks cover ordinary and space bullets. These are focused encounter checks, not unassisted full campaign balance runs. Still images clear unrelated pickups for visibility.

Gameplay source retains LF and the main test harness retains CRLF. Existing work preserved; no commit or push.

## Follow-up: full handle and hilt shake

The earlier horizontal crop stopped partway down the handle. The corrected held assembly now extends to the bottom of the hilt, with the hands following it and a short upper-body flex keeping the torso anchored. The change is limited to the raised charge motion and its glow; healing, targeting, stun and rebuilding retain their behavior.

Native Chromium compared head, shaft, hilt and torso pixels in all three raised poses in both shake directions: **24 comparisons, 100% matching expected translations**, with no page or console errors. The existing recovery probe also passed all nine damage routes and three completed heals. The full suite again finished at **5,083 pass / 0 fail**, exit 0, versus the same 5,083/0 baseline. Logs: `_shots/probe_full_handle_0926.log`, `_shots/probe_full_handle_regression_0926.log`, `_shots/test_fl_full_handle_0926.log`.

Updated real-canvas recording and enlarged crop: `_shots/hammer_full_handle_0926/review.html`. Both clips load and the page has no browser errors. Durable motion evidence: [qa/hammer_full_handle_0926.json](qa/hammer_full_handle_0926.json).

## Follow-up: chest core spreads energy outward

Mike changed the empowerment direction. `hammerChromiumCoreClip` now reveals the authored palette through expanding six-pixel steps centered on the measured chest anchor. A brighter advancing ring and a brief reactor pulse remain clipped to the authored sprite. The same mask handles post-stun rebuilding. The initial charge gives the hammer a 0.35-second head start after lightning; HP recovery and the hammer-core counter keep their existing timing. The lightning endpoint now follows the visible hammer jitter.

Native Chromium verified the lightning-before-armor order on Normal, Hard and Furious. Pixel samples show only the core changing early, then both arms while the boots remain unchanged, and finally the boots. All nine damage routes, three completed heals, hit flashes and recovery bar checks still pass. Page and console errors: zero. Recording/contact sheet inspected at `_shots/hammer_core_wave_0926/review.html`; durable results: [qa/hammer_core_wave_0926.json](qa/hammer_core_wave_0926.json) and [qa/hammer_core_wave_regression_0926.json](qa/hammer_core_wave_regression_0926.json).

Syntax passed. Both full-suite runs reached the final summary with **5,082 passes / 1 failure**, exit 1: `a second lance may destroy the wounded 3-drone column`. Previous immediate baseline was 5,083/0. This exact intermittent assertion is already recorded in `HAMMER_STORM_0926.md`; no other failure names appeared, and all hammer checks passed. Logs retained at `_shots/test_fl_core_wave_0926.log` and `_shots/test_fl_core_wave_0926_final.log`. The unrelated drone test was not changed in this visual pass.


## Follow-up: red recovery segment, no text

Pending healing now uses a red fill and red pulse glow, with no RECOVERY label. Native Chromium screenshots and the preview recording were refreshed and visually inspected; no browser errors. Syntax passed. Full suite: **5,083 pass / 0 fail**, exit 0 and final success banner, versus the previous 5,082/1 run. The known intermittent drone assertion passed this time. Log: `_shots/test_fl_red_recovery_0926.log`; durable native report: [qa/hammer_red_recovery_0926.json](qa/hammer_red_recovery_0926.json). Healing/cancellation behavior is unchanged.
