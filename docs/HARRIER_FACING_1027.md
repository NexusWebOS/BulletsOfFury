# Harrier guns face south before modular handover — October 27

The large arrival/flyover renderer used the old whole carrier plates, whose built-in small gun housings did not match the current south-facing colored modules. The four stowed housings now use the exact current colored south-facing gun pose before the independent rotating modules take over.

## Art and runtime owners

assets/harrier_facing_1027.js selects pre-authored whole-hull variants for the Stage 6 closed, open and broken plates, both complete-fan and cut-well versions. All original hull alpha and all pixels outside the four gun apertures are unchanged. The four legacy pre-modular white hit masks now match the complete south-facing silhouette. Normal combat still uses ER28's clean substrate and the existing HT28 modular guns, with no doubled gun plates.

The opening flyover flips the complete carrier northbound. Three additional opposite-local-facing hulls compensate that existing orientation, so their guns still face screen-south. This selection applies only inside that opening draw and restores its flag immediately afterward. Other stages retain their original carrier images.

On each native depth-to-fight handover, surviving small guns begin at the same south-facing angle and then use their existing smooth aiming. Health, cooldowns, weapon timing, module targets, breakup, damage, movement, carrier-to-Nightwing transition and rewards remain native. No new art generation or runtime image transform is introduced. The current Nightwing whole-ship entrance remains in place.

Nine complete 512x288 hull variants and four 32x40 white masks are under assets/game/levels/stage_06/boss/harrier_facing_1027. Registry: assets/harrier_facing_art_1027.js. Editable PNGs, manifest, harrier-south.aseprite and portable build.py are retained in _ART_SOURCES/harrier_facing_1027. All 13 runtime PNGs plus registry rebuild byte-for-byte; original hulls and the earlier turret banks remain preserved. ASEPRITE_EXE selects the optional editor export. The portable native probe is _BUILD_SOURCE/probe_harrier_facing_1027.py, with --out for evidence.

## Verification

30 art/native Chromium checks pass: exact original hull pixels/alpha outside the four apertures for all nine hull variants; real arrival/flyover/opening selection; matching hit masks; exact south-facing first and repeated modular handovers; unchanged ten-part health budget; independent actual opaque module targets; scoped opening compensation and other-stage isolation. Actual native arrival, handover, flyover, opening and decoded film pixels were inspected. No final page, draw, console or asset HTTP errors.

Fresh native Furious Cole GOD/input-bot footage completes Harrier and Nightwing in 171.79 seconds. All 27 sampled depth poses select south-facing graphics, and 3 native handovers occur. A continuous 12-second opening excerpt is provided. Initial 20 seconds withhold player fire; normal allies, native HP, attacks, phase timing and defeat remain. Native rendering averages 54.22fps; encoded 30fps. Audio mean -18.2dB/peak -0.9dB. No game, bot, console or HTTP asset errors; three unrelated background loads abort on navigation/closure. The invulnerable observer takes 525 prevented hits, so this is visual/behavior evidence rather than human balance proof.

Syntax passes. The full required suite reaches its summary with the same five known failures: single-hit flash duration, two Chronos opening-jump expectations and two StageX right-route expectations. No game.js/test_fl.js changes, commit or push. QA: docs/qa/harrier_facing_1027.json. Review: http://127.0.0.1:49257/index.html. Existing Stage 6–9 and turret-review pages point to the refreshed film.

All 13 final Chromium playback, seeking and affected-source-hash checks pass across both videos.
