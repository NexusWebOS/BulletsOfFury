# Warden and Tidal Sovereign — October 25

[Watch the updated recordings](http://127.0.0.1:54219/docs/previews/warden_tidal_1025/index.html). The review includes a 45.2s Warden checkpoint, the complete 220.20s Furious Stage 9 fight, and six water attack jump points.

## Stage 7 corrections

| Problem | Cause and correction |
|---|---|
| Pilot retreats while the boss appears to slide | Chase mode moved the floor even after the chassis reached its screen target. Gait now measures body travel relative to that moving floor; stance feet ride its exact delta. Backward recovery also animates from its actual movement. Ground scroll stops with no usable legs or during a braced barrage. |
| Turrets shift while firing | The old battery pose converged their mounts inward, while chaingun poses stretched and extended the guns. Each complete gun now rotates around a fixed rear trunnion at local ±34,12. Its FOV and muzzle use the same resulting geometry. |
| Both live arms appear to disappear | Retired swipe and jump-crouch frames folded the forearms across the face, changing their silhouette and burying the return. The same connected walking claws and fixed hip pivots now perform the windup, strike, return, takeoff and landing. Native destroyed parts still break and lose their targets. |

## Stage 9 upgrade

The existing whole Tidal Sovereign keeps its three native damage states. Each now has 32 actual liquid poses on a fixed 320×256 canvas at 12 fps, common 160,128 pivot and one scale. Only the measured water apertures change: circles rotate and wing/core/nose water flows. Armor, seams, outlines and every alpha pixel stay byte-identical to each source damage state. The three banks total 392,646 bytes and reuse the approved blue water art.

| Furious attack | Behavior |
|---|---|
| Flood | Three water fronts, a 1.25 s first warning, 1.55 s between rows and a 150 px opening; the next gap shifts only after its tell starts. |
| Geysers | Six committed marks, a 1.35 s reaction window and 0.58 s stagger; tall water spires leave lateral escape space. |
| Laser mortars | Six arcing shots from the large circles, a 1.12 s charge plus 1 s flight; marked impacts erupt into water laser spires. Defensive clears cancel the pending eruption. |
| Mist lasers | The two lower cannon tips alternate four charged 0.48 s pressure beams, with water mist. A fifth pulse joins below half health. |
| Undertow | Five cutter-wave volleys from the circles and shootable physical torpedoes from the lower cannons. |
| Maelstrom | Six alternating circle barrages rotate around a committed opening. Water energy remains ordinary unshootable ordnance; defensive clears remain available. |

Normal and Hard use fewer flood rows and longer reaction windows. Attacks finish their hazards and recovery before the next turn; the old supplemental targeter is interlocked. Pending water hazards stop with their native boss owner. Measured cannon tips are (120,226) and (200,226); water circles are (96,87) and (224,87) on the 320×256 source canvas.

The complete water hull stays inside the visible camera bounds, keeping both circles and cannon tips readable as the pilot moves. The native sentinel fight, convergence, portal collapse,6,500 HP Furious water pool, vulnerability, death and rewards remain owned by the encounter. Pool initialization now occurs on the first live water frame, removing the old one-frame generic-health reset. No phase or health writes are used by the delivered full-fight bot.

## Current fight timestamps

These are absolute positions in the new full Stage 9 recording. The bot defeats the sentinels normally, withholds weapons for one water rotation, then resumes fire through native defeat at 210.42 s. GOD prevents player damage. This establishes runtime/visual coverage; human difficulty still needs player review.

| Water section | Full-fight timestamp |
|---|---|
| Tidal flood walls | 01:45–01:53 |
| Water geysers | 01:53–01:59 |
| Circle-launched laser mortars | 01:59–02:05 |
| Turret mist lasers | 02:05–02:10 |
| Cutter waves and torpedoes | 02:11–02:18 |
| Maelstrom bullet hell | 02:18–02:26 |

The Warden clip advances the native loop to its first chase, then captures 45 s at real time with an invulnerable input bot withholding weapons so all live arms remain visible. It is a checkpoint, not a full new Stage 7 kill. Earlier complete Stage 7/8 fights and all original [timestamped 7/8/9 findings](FURIOUS_789_REVIEW_1025.md) remain available in the older review.

## Verification and ownership

- 42 native Chromium checks pass, including actual visible claw pixels through every swipe, planted floor-relative feet, fixed turret pivots, all 96 water hull cells, actual animated/hit pixels and expiry, safe flood gaps, geyser collisions, mortar clears, camera edge visibility, audio decoding/playback, phase entry and cleanup.
- 34 browser review checks pass: both recordings and six chapters decode, play with audio, seek, frame-step and run in slow motion; byte-range requests and page/console/asset checks pass.
- The complete Stage 9 MP4 passes all 9 delivery checks; the Warden clip passes 7. Stage 9 has zero player deaths and no page, console or asset errors. Source render rate is 59.5 fps.
- Syntax passes for game.js and all updated modules. Required `node _BUILD_SOURCE/test_fl.js` exits 1 before any assertions or final summary because `_BUILD_SOURCE/retired_art_archive_1022.cjs` is missing. That existing blocker is retained and reported.

Runtime: `assets/stage78_review_1025.js` (gait, claws, gun pivots), `assets/bullethell_1025.js` (braced gait state), `assets/warden_tidal_1025.js` (water owner). Generated hull registry: `assets/warden_tidal_art_1025.js`, owned by `_BUILD_SOURCE/build_warden_tidal_1025.py`. Art taxonomy registers `wt25_`. No production atlas was repacked.

Evidence: `docs/qa/warden_tidal_1025.json`; `_shots/warden_tidal_1025/` contains native fixtures, visible-pixel proofs, source masks, raw audio/video, full-decode logs and browser screenshots. Pre-existing user changes remain in place. No commit or push.
