# Stage 5: charged hammer and counter-throw — September 26, 2026

Mike rejected the dual-gun/body-change continuation after the chaingun breaks. That live route now restores the approved single-headed hammer and the same black/chrome armor with its blue chest reactor on every difficulty. The earlier intact-cannon arsenal and whirlwind/stun work remain.

## Encounter

- Cannon destruction uses the engine explosion, then restores the hammer. He raises it, lightning strikes the cylindrical head, the energy charges, and he lowers it before his next attack. A 3.05-second transformation gives this beat time to read.
- Hammer energy changes between cyan, silver-white and emerald. The cached palette affects blue energy inside measured hammer-head regions; armor, outlines and the blue reactor remain authored. Brightness detail is preserved instead of flattening the cylinder into a solid color.
- Each slam commits its target, shows the shared warning and ground Retina, jumps, and lands the actual animated hammer head on that target. Wind-up lasts 1.15/1.0/0.9 seconds on Normal/Hard/Furious.
- Ground Retina markers split outward from the impact into 3/4/5 committed areas. They travel for 0.6 seconds, then warn for 1.15/0.95/0.8 seconds before the generated chromium spikes erupt. Spikes use a local 27-pixel ground footprint; travel, warning and fading frames do not damage the player. Markers are large enough to contain that footprint. This is a projected ground eruption, not the old full-height column attack.
- Two slam/split cycles lead to a hammer throw. The broken cannon never regenerates, and no akimbo body or weapon is drawn in this continuation.
- A damaging hit to a flying hammer sends it back without subtracting hull or hammer-module HP. This works through ordinary shots, space weapons and Retina missiles. The reflected return cannot hit the player; a generated electrical tether and the existing magnetic sound lead into the authored catch pose.
- He catches, recoils, pulls the hammer behind his head, and twirls it through eight authored overhead poses. The two-second retaliation wind-up spins faster than the first throw. Its starting side is randomly chosen and warned before release; subsequent player movement does not redirect it.
- The retaliation flies out to that side, then spirals inward toward a committed arena center: 1.35/1.65/2 turns on Normal/Hard/Furious, with 4.0/3.5/3.0 seconds of spiral travel. It returns magnetically afterward. It can also be shot back, but a second counter ends the exchange rather than creating an endless retaliation loop.

## Generated graphics

All six PNGs were generated with the built-in image tool, inspected, copied into the repository with RGBA preserved, and registered through XART and `ART_TAXONOMY.json`. Source paths and exact generation/edit prompts are in [hammer_storm_art_0926.json](hammer_storm_art_0926.json).

- `assets/game/stage5_archmage_0916/combat_0926/storm_charge.png` — 8 charging poses.
- `assets/game/stage5_archmage_0916/combat_0926/hammer_throw.png` — 8 catch, pullback, release and empty-hand poses.
- `assets/game/stage5_archmage_0916/combat_0926/hammer_overhead.png` — 8 overhead twirl poses with a stable torso.
- `assets/game/stage5_archmage_0916/combat_0926/hammer_flight.png` — 8 detached single-headed hammer orientations.
- `assets/game/stage5_archmage_0916/combat_0926/hammer_lightning.png` — 8 lightning frames, also used for magnetic recall.
- `assets/game/stage5_archmage_0916/combat_0926/chromium_spike.png` — 12 eruption/fade frames.

Explicit source rectangles handle uneven generated gutters. Chest/head anchors keep the weapon, damage target and Retina target attached to the drawn pose. The existing twelve-frame strike reel supplies the slam and recovery. No atlas repack or generated atlas-manifest edit was needed.

## Verification and limits

- Syntax check passed. Game LF and test-suite CRLF retained.
- Full suite before the final warning-size refinement: **4,981 passing assertions, zero failures, exit 0**, reaching `FALVA/LIZZIE BUILD OK`. Incoming baseline was 4,957/0. Three obsolete tests were replaced by tests of the requested design: cannon-loss behavior, the counter/spiral exchange, and authored throw rendering. Prior tests remain on disk as history.
- Final full-suite and browser logs: `_shots/test_fl_hammer_storm_0926_release.log` and `_shots/probe_hammer_storm_0926_release.log`; completion recorded below after the run.
- Real Chromium checks cover the entire new phase on Normal/Hard/Furious, native bullet cannon destruction, all nine difficulty/weapon-route counter combinations, restored weapon state, actual spike collision and safe areas, ground/head alignment, and source-cell clipping. Both page errors and console errors are inspected.
- `_BUILD_SOURCE/probe_hammer_consistency_0926.py` passed after the phase replacement: lowered-idle regular strike chains, Furious orbital sequence and missile counter remain functional.
- Review: `_shots/hammer_storm_0926/review.html`. Three real game-canvas recordings show 25 seconds of the charged phase and 14 seconds of each spiral direction. These are muted, invulnerable encounter-inspection fixtures, with a native player bullet inserted at the hammer to demonstrate the counter. The unrelated asteroid stream is disabled only in the final preview fixture; campaign asteroid behavior is unchanged. These are not complete unassisted campaign balance runs.

Previous failed development checks were retained: an incorrect weapon-owner reference was fixed, old design assertions were replaced, and a Chromium source-edge check caught two cropped throw frames whose gutters were then corrected. They are not represented as passing runs.

Nothing committed or pushed.

### Final results

The final Chromium probe (`probe_hammer_storm_0926_release.log`) exited **0**, with no page/console errors, all difficulty/counter/collision checks passing, and zero clipped edge pixels across the 24 charge/throw/twirl poses. The review page also passed: all six sheets and all three videos load. Final recording samples were visually inspected. A durable copy of the browser results is `docs/qa/hammer_storm_0926.json`.

The final full-suite runs **exited 1** and reached their final failure summaries:

- `_shots/test_fl_hammer_storm_0926_release.log`: **4,980 passed / 1 failed**, `road tank changes among the eight drive headings instead of sliding on one axis (0)`.
- Unchanged-code recheck, `_shots/test_fl_hammer_storm_0926_recheck.log`: **4,980 passed / 1 failed**, `a second lance may destroy the wounded 3-drone column`. The road-tank assertion passed this time.

Both failures are outside the hammer tests. The road patrol fixture itself documents its random start/direction instability; the drone failure also exists in prior logs such as `_shots/frost_furious_beams_0920/test_fl.log`, `_shots/sfx_test_0923.log` and `_shots/test_fl_0924_online.log`. Neither gameplay system nor assertion was changed here. Relative to the incoming zero-failure baseline, these failed runs are still nonzero and are reported rather than treated as green. All new hammer assertions passed. The earlier complete 4,981/0 runs are retained but do not replace these final results.
