# Stage6 giant cloud-side carriers / November1

**Later revision:** Mike expanded and polished this design. The current implementation uses two enlarged staggered pairs, all-ten-turret hull gates, no HP bars, safe aircraft overflight/shadows and two additional strategic-carrier waves. The historical first-pass notes below are superseded where they differ from `docs/CARRIER_ASSAULT_1101.md`.

Mike requested giant airborne carriers rising up the cloud sides, each carrying five circular doors that split open, extend cannons and release lasers, using his Fire Shark screenshots as the mechanical reference. This is a new regular Stage6 elite, separate from the existing Carrier boss and protected entrance stealth bombers.

## Art and ownership

`assets/cloud_carrier_1101.js` owns the encounter. `CC111` and `CC111_ART` deliberately avoid the existing Siege Console's `SC12` registries. The `sc12_` XART keys and `_sc12` actor field belong only to this new carrier.

Two built-in image_gen outputs are preserved verbatim in `_BUILD_SOURCE/cloud_carrier_1101/`, with original generated filenames, source hashes and dimensions in the generated manifest. The generation brief specified a single north-facing navy/graphite carrier, silver rims, teal/blue circuits, five empty circular wells and four rear engine outlets; the second image uses the supplied hatch references for twelve fixed-pivot circular door/cannon poses. No whole-hull action strip is used.

Rebuild with `python _BUILD_SOURCE/build_cloud_carrier_1101.py`. Outputs live in `assets/game/levels/stage_06/enemies/cloud_carrier_1101/`; the builder also writes `assets/cloud_carrier_art_1101.js` and inspection plates under `_shots/cloud_carrier_1101/`.

- Hull:512x1024 fixed transparent canvas,340 world-pixel height, one proportional scale. Five measured deck wells, bridge and four exhaust sockets share that transform.
- Modules:192x192 cells, twelve authored poses,32 source-preserving direction exports and one shared rim scale/pivot. Disconnected grid-edge debris is removed from the normalized cells while original sources remain intact. Live rendering selects cells; it does not rotate the static sprite through canvas/CSS.
- Pose sequence: closed, split shutters, open well, rising cannon, extension, full extension, internal blue-white charge, recoil, return and authored destroyed well. The common circle pivot remains fixed through barrel extension.
- Own-pixel blue/teal1015 companions follow the actual vent/circuit masks. The whole hull stays solid. Four independent authored thruster effects animate from measured outlets. Existing rolling cloud plates appear behind the lower hull at the screen sides.
- Beam and release flash reuse the authored blue-white Stage3/lvl2 laser/muzzle banks. Registered bore anchors follow the selected recoil/extension pose and heading, so cannon, FOV, beam and contact ray agree.

## Gameplay contract

The controller is not an invisible collision body. Six actual native enemy actors occupy the visible bridge and five circular wells. Their complete health sum is retained; no extra full-health parent target duplicates that budget. Each well has its native Retina target, physical contact, hit/damage routing and visible white flash. Breaking a well immediately cancels that gun's warning/beam and leaves its destroyed hatch on the hull. A destroyed bridge stops exposing a live target while surviving cannons continue fighting.

The bridge uses `EHP(110)*5`; each of the five bays uses `EHP(38)*4`. The verified Furious total is475. On complete exhaustion, one separate native corpse owns kill feedback,8000 score, drops, breakup and death cleanup. There is exactly one kill/reward, rather than six component rewards. The solid corpse is rendered through the native death interval without HTML fading.

The carrier enters from below on the left or right cloud edge, travelling north into a broadside station. Its world lane is captured on entry, rather than being dragged with the camera. Bays cycle through0.76s opening, committed green/yellow/red warnings,0.58s laser/recoil and0.65s retraction, followed by a finite rest. Global release reservations stagger the battery. Normal/Hard/Furious minimum committed warning times are1.65/1.45/1.30s, with minimum release gaps0.72/0.64/0.58s. Each gun snapshots a quantized aim ray before its warning; it does not follow a dodge after committing.

Native campaign arrivals are left at18s and right at54s. After23s of station time the carrier closes its guns and departs north. Story/boss/miniboss warning interlocks cancel live attacks and initiate departure. New stages clear all old controllers and warnings. StageX is excluded.

`assets/game.js` has one explicit early native-update branch for `_sc12` actors, adjacent to the existing Warden-wing owner branch. It preserves the component actors through the offscreen fly-in, ticks native hit flash and handles health exhaustion while the carrier controller owns their position. The native collision and Retina loops still see them. This is required: the generic offscreen cull otherwise removed the lower bays during entrance.

Audio uses the existing approved shared mixer routes and simulation-time retrigger gates: `combatServo0927`, `bossWeaponCharge`, `enemyHeavyLaser`, `combatModule0927`, plus native warning beeps and complete-death sounds. There are no detached audio timers or delayed launcher callbacks. Ordinary enemy bullet and physical missile interception contracts are untouched; the laser is a native continuous hazard tested against the same visible ray.

## Evidence and preview

`python _BUILD_SOURCE/probe_cloud_carrier_1101.py`:21/21 real Chromium checks pass. Evidence includes all five complete attack cycles, ready FOV/cloud assets, a travelling player round hitting a visible well, six native Retina targets, actual damaged white pixels and expiry for bridge and every bay, surviving bays after core break, complete native reward ownership, stage cleanup and native player death on the visible laser ray. Screenshots and results are under `_shots/cloud_carrier_1101/`.

The preserved-aircraft regression `python _BUILD_SOURCE/probe_stage6_airframe_1101.py` also passes66/66, including existing hull identity, wind/helper flight, exhausts, native damaged pixels, sky turret exclusion and entrance stealth preservation. No page or console errors were reported.

`node --check assets/game.js`, `assets/cloud_carrier_1101.js` and its art registry pass. The required full `node _BUILD_SOURCE/test_fl.js` still exits1 before assertions/final summary because ignored `UNUSED_ASSETS/retired_art_1022/manifest.json` is absent. This is the previously recorded baseline blocker, not a passing suite.

`python _BUILD_SOURCE/record_cloud_carrier_1101.py` records23.24s of actual Stage6 gameplay, native health and attack clocks, movement input and an explicitly labelled invulnerable observer. The second carrier is spawned eight seconds into this demonstration so both screen sides are visible; campaign arrivals remain separate. All ten cannons fire. Native allies later damage and break two left-side bays. The final H264/AAC movie fully decodes; shared-mixer playback includes servo, charge, laser, warning and break cues without tap/bot errors. The capture gain is0.26; the measured pre-gain peak1.686 remains below full scale after the capture gain.

`python _BUILD_SOURCE/publish_cloud_carrier_1101.py --install` adds one new enemy card and a focused player to the local review hub. All160 existing cards/clips remain byte-for-byte unchanged, for161 cards total. Current local route: `/current/stage6-cloud-carriers-1101.html`. No commit or push was requested or performed.
