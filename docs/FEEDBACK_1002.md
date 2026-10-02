# October 2 — Campaign feedback and straight enemy hulls

Prepared on downloaded `d19c966693d8a5e73b5394f69207801725e163eb` and prepared for the October 2 GitHub upload. Existing work preserved. No atlas replacement or SpriteCook use.

## Implemented

| Area | Result |
|---|---|
| Level 1, Freezer | The stage clock advances in real time during Slowdown. Boss entry animations can advance during the slowed threat updates. Ice Breath keeps its own generated icon, without a numeral in the art, and its correct loadout name. Its form/element selection is locked through the Level 1 clear and opens after Level 2; the unlock survives campaign saves and replays. |
| Dam approach | Three green bombers per Normal wave, four on Hard, five on Furious; four waves precede the chopper. Easy has three shorter two-bomber waves. Aircraft enter vertically, drop warned Ground Retina bombs and leave the screen. The boss gate waits for both the aircraft and their pending impacts to clear. |
| Level 2 | Runtime golem names and the authored wave entry resolve to the newly generated fire jet. Destroyed encounter magma balls produce an authored explosion and impact/launch audio cues. Furious Magma Ward rain has three randomized spatial groups of nine Retinas, with staggered releases, early tracking and committed red warnings. Ordinary shots now open Ultra/Uber missile crates. |
| Level 3 miniboss | A new generated hull, independent twin guns, missile racks and central core replace the old Frost Cruiser plate. Its attack book includes balls, four charged beams, missiles and short strafing bursts. Furious Fire/Ice forms use their matching beams and balls. Other difficulties retain the Ice elite. Existing neutral arrival → nuclear impact → transformed actor remains continuous. |
| Level 3 boss | Rapid visible cold machine-gun tracers and crossfire join the existing paired charged beams. The weapon mounts follow the modular guns and their recoil. Loadout element pages use earned discoveries instead of every infusion type. |
| Level 4 boss | A fifth destroyable central lightning barrel has four generated charge poses and a generated beam reel. Helpers retain their shared materialization/positioning clocks during the new attack and fire committed rocket bursts. Incoming boss rockets are Retina targets. Losing at least two weapon modules adds warned rams and faster fire from surviving weapons; losing every weapon produces red damage flashes, smoke and weaponless charges. Removed miniboss helpers stay removed. |
| Level 5 Hammer | Spike Retinas anchor at the bottom edge and spike columns span the full vertical play area. Passive volleys and unguided manual missiles cannot damage the hammer; a real curved Retina missile deliberately locked to it can. Whirlwind windup cannot be disarmed. The ordinary attack book now naturally reaches spin/throw/catch, orbital jumps and the spiked ball. |
| Hammer dialogue and rage | After the ship unfolds, the boss uses its new portrait to reveal the Earth trap and taunt the pilot, then opens with a jump strike. Rage performs a fast second strike, returns smoothly, sends a short burst, then rests long enough for both evasion cooldowns. HAMA/HAMMER music and dance choreography remain separate. |
| Hammer chaingun and death | Eight generated standalone rotary-barrel poses replace the old gun attachment. A common pivot and muzzle registration keep the gun attached and shots aligned. The unique death sequence uses a generated body, independent bulging-eye/head-turn poses and a raised shaking arm, a hammer-core burst, mechanical scream, five smoke rings, sixteen-frame electrical explosions and the existing explosion system. |
| Enemy facing | Living ordinary hulls draw with fixed facing instead of banking, spinning or squashing through a roll. Independent turrets can still aim; authored cardinal bomber/bay headings, player evasions, boss choreography and death rotations keep their owners. Level 7 flyers commit a target, warn, release staggered toxic bursts, pause and depart. Level 8's four hull roles use bounded committed bursts, charging pockets, a gap in the radial attack and two attack cycles before departure. |

## Assets and ownership

`assets/feedback_1002.js` is the final gameplay layer after `feedback_1001b.js`. `assets/feedback_art_1002.js` registers fourteen loose asset families from `_ART_SOURCES/feedback_1002/manifest.json`. Source originals, including the rejected first chaingun candidate, are preserved there. `_BUILD_SOURCE/build_feedback_1002.py` repacks the saved originals; the original generated-image directory is only needed if an archived original is missing.

The builder scales crop coordinates to each actual source size, bounds alpha using a visibility threshold, and preserves alpha in the saved pixels. Shoulder and cannon attachment anchors are registered explicitly. No shared atlas or atlas manifest was edited. The small core hooks are documented in `_BUILD_SOURCE/patch_feedback_1002.py`; this patch is for the incoming build, not an idempotent repair command to rerun against the finished file.

`assets/game.js` remains LF. `_BUILD_SOURCE/test_fl.js`, the modified Hammer storm test and the new focused assertion module remain CRLF. Existing prior HAMA imports and tests were preserved.

## Verification

- Incoming baseline: 6,247 assertions, zero failures. Final full suite: **6,287 assertions, zero failures, exit 0**, with the final `FALVA/LIZZIE BUILD OK, 0 ERRORS` banner. Failing-name comparison: `[] → []`. Removed golem expectations and the former 75%-height spike expectation were updated to the requested behavior.
- Syntax: `node --check assets/game.js`, `assets/feedback_1002.js` and `assets/feedback_art_1002.js` pass.
- `_BUILD_SOURCE/probe_feedback_1002.py`: **118 native Chromium checks pass**, zero page and console errors. It uses the actual game canvas, waits for lazy assets on a timer after trapping RAF, and yields between frame batches. It checks real bullet/crate collisions, a real curved Retina missile, all four dam waves and the chopper warning, materialized helper rockets, Frost Cruiser/cryospear/Sovereign attacks on Normal/Hard/Furious, and the continuous Furious Stage 3 transformation.
- Straight hull rendering is measured through the game context's actual `drawImage` transforms for three sewer flyers and all four Stage 8 roles on Normal/Hard/Furious. Continuous motion samples show maximum per-frame steps under six pixels; real attacks release finite projectiles. A separate droid draw check verifies its rotating/squashing path is neutralized without deleting its other state.
- A naturally advancing Normal Hammer fixture reaches `spin → throw → hammer_catch`, orbital rise/dive/sweep/recovery, and the spiked ball without a password or forced move selection. The rage sample records two strikes followed by **7.67 seconds** in the recharge state; barrel-roll and somersault cooldowns are five and seven seconds. The generated gun fires a sustained live burst. Death events include the core burst, scream and all five rings.
- Screenshots were inspected for the new hull, central barrel/helper placement, straight sewer/alien ships, aligned gun and modular death poses. Evidence and the review page are under `_shots/feedback_1002/`; the final logs are `_shots/feedback_1002_suite.log` and `_shots/feedback_1002_probe.log`. Portable check results are saved in `docs/qa/feedback_1002.json`.

## Remaining playtest and design work

These are controlled native gameplay fixtures with invulnerability and chosen encounter starting points. They are not complete campaign wins or proof of final balance. Human playtests should cover the full dam approach, a full Furious Frost Cruiser form cycle, the Sovereign helper-to-ram progression, and Hammer's complete health/armor progression with missiles and evasions.

The new sewer modular-enemy roster is an optional follow-up design item from Mike's latest request. This pass keeps the existing authored sewer assets and fixes their facing/attacks; it does not claim to have generated a new sewer roster. Full nine-stage difficulty comparison and long-session performance measurements remain separate work.
