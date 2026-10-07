# Hard Corps combat transfer — October 7, 2026

This implements the cause → commitment → attack → crossing → recovery rhythm recorded in `_STAGING/contra_study_1005/BOSS_FIGHT_ATLAS.md`. The timings and attacks are original BOF designs; they are not measurements of Contra's hidden collision rules.

## Active encounters

- Stage 4 Storm Sovereign: committed left/right lightning-gun relay with staggered short bursts; the central destroyable lightning weapon produces a full rotating cross. Core revival interrupts custom attacks and retains its previous four-node lifecycle.
- Stage 5 Tempest Eclipse: intact modular space bomber relocates, settles, issues paired committed lances, performs a pulsed cross, then a short gun pass. Engine losses lengthen relocation, cannon losses cancel their own warnings, rays and released shots. Both cannons lost selects a bay flak pattern.
- Stage 6 Eclipse Siege Bomber: fixed flak gates with one open column, committed moving gun passes and staggered paired lances. Its full authored chassis remains attached to its surviving modules. Every attack is separated by recovery and relocation.
- Stage 8 Herald: first three taught cannon/lance/salvo patterns remain; each fourth attack introduces a wing-driven eclipse cross. Each wing owns two opposite rays. Broken pieces remain opaque while physically falling; the hot discharge effect may dissipate.

## Rotating cross

Six pulses complete exactly one 360-degree rotation, clockwise from a diagonal. Easy takes 15.30 seconds, Normal 13.80, Hard 12.48, Furious 11.64, following a 1.45–1.70-second initial warning. Each pulse damages only during the first 44% of its sector. A .20-second harmless dissolution is followed by complete absence and a .42-second preview of the continuing rotor. There is over .88 seconds without damaging beams per Furious sector. A pilot can move through a former beam during that interval. The beams do not chase the player. No simultaneous custom projectile rain occurs during the cross.

Warning geometry, native authored beam geometry and collision share the same origins, angles and width. Stage 4 uses the live central lightning socket. Space uses its visible central reactor, powered by the two destroyable cannons. Herald uses its skull socket, powered by the wings. All rays clear on death or owning part loss.

## Files and integration

`assets/hardcorps_bosses_1007.js` loads after `herald_1003f.js`, `combat_1003i.js`, `feedback_1002.js`, and `s4_core_revival_1006.js`. A later warning renderer may override `combatWarningDraw` without changing the controller API. `laneShape:'line'` requests constant-width lane art when available.

No new media, atlas repack, manifest, art resampling, core HP, reward or final-boss form pool change. All visible beams, muzzles, warnings and ship pieces use existing authored pixels. Public diagnostic state is `HC1007` and each owned encounter's `_hc1007`.

`_BUILD_SOURCE/test_hardcorps_bosses_1007.cjs` supplies 38 behavior checks for the main suite. `_BUILD_SOURCE/probe_hardcorps_bosses_1007.py` runs native Chromium fixtures and injects the runtime only if the index does not load it yet. Native screenshots and JSON go to `_shots/hardcorps_bosses_1007/`.

The native checks include each of four difficulties, correct warning lead, positive damage control, fully harmless gaps, complete revolution and cleanup, cannon/wing disarm, opaque physical debris, ordinary keyboard crossing, and natural full bomber attack books. These are focused fixtures, not unassisted campaign clears or complete balance certification. Root integration must run the full main suite after all October 7 layers are loaded.
