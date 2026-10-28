# Nightwing whole ship and corner entrance — October 27

Mike requested a complete fighter rather than independently drawn wings/body, with a deliberate flight sequence after the Harrier falls. Nightwing now uses one complete authored ship plate for every pose and retains a single native health pool and one Retina target. The Harrier keeps all ten native modular components and the corrected solid gun modules.

## Entrance

The native carrier fall still launches the actual blue Nightwing from its hangar. The new protected sequence then flies south beyond the playfield in 1.1 seconds, waits .22 seconds fully offscreen, relocates to a lower corner away from the player's column, and flies vertically north at a fixed x over 1.45 seconds. After another .22-second fully offscreen turn, it returns from the top facing south over 1.25 seconds, settles .4 seconds, then begins the existing patterns in the upper half. The corner center is 105px inside the playfield so the 184px-wide hull stays readable. The offscreen reposition/turn never occurs while visible.

The entrance owns movement only. No guns, missiles, attack decisions, body collision or Retina damage begin before the return completes. It preserves the complete native stored Nightwing HP, native carrier cookoff and stage-wide clock. Pause holds the sequence. Initial attack cooldowns reset to the native values. The existing flight/roll/somersault, machine-gun/gate volleys, missiles, dash, inverted/desperation, death, rewards and eventual stage exit keep their native owners.

## Whole-frame rendering

assets/nightwing_entrance_1027.js replaces the blue Ace draw and point-hit routing. It draws exactly one complete body frame for idle, damage, banks, roll, somersault, inverted movement, north/south entrance and death. Full-body white hit frames expire on the native boss flash timer; the old wing/body flash flags are retired. A single live body target shares b.hp/maxhp and follows the same A.x/y. Alpha point hits use the actual complete frame. No wing detachments or independent wing HP are introduced.

The fixed 272x272/pivot136 bank contains 107 whole plates: native blue repaired top/damaged/belly views; the current 16-pose blue P2 rolls/somersaults; baked northbound and inverted turns; native blue D27 exhaust baked into the whole top plate; and 32 whole damaged-hull death-spin directions. Matching white frames preserve all alpha. No runtime rotation, scaling, color compositing or limb assembly is used by the new draw owner. Existing non-body weapons/FOV, smoke, orb and death effects retain their native presentation. No new paid art was required.

## Source ownership and evidence

- assets/nightwing_entrance_art_1027.js registers two complete banks plus groups; index loads both after the Harrier turret owner with cache version whole-corner-pass-1027.
- Runtime PNGs: assets/game/levels/stage_06/boss/nightwing_entrance_1027.
- _ART_SOURCES/nightwing_entrance_1027 retains PNGs, manifest, portable build.py, original references and nightwing-whole.aseprite. The builder finds the repository from its own path and reproduces both runtime banks/registry byte-for-byte. ASEPRITE_EXE selects the optional editor export.
- _BUILD_SOURCE/probe_nightwing_entrance_1027.py uses --out for native test evidence. Its deliberate native damage/state fixtures are separate from the real-time recording.

17 native Chromium checks pass: intact modular Harrier; complete ordered route; fixed-x north pass and correct return orientation; pause; full protected HP/no attacks or targets; one live body; one body blit through all maneuver types; real whole-body hit pixels and expiry; resumed native gate/fire; complete native death and final exit. Actual native and decoded video pixels were inspected. No final page/draw/console/HTTP errors.

The fresh 164.41-second Furious Cole film completes Harrier and Nightwing via native input, HP, damage and phase timing. An explicitly invulnerable input-only bot and normal allies fight; first 20 seconds withhold player fire. All sampled entrance health stays full and the recorded source events contain all seven beats, including the two short offscreen turns. An 18-second continuous excerpt shows the carrier fall, escape, north pass, south-facing return and opening fight. Native rendering averages 52.53fps; video 30fps. Decoded audio mean -18.2dB/peak -0.9dB. No game/bot/HTTP asset/console errors; 21 unrelated background loads abort on navigation/closure. God Mode prevented 573 hits, so this proves presentation/behavior, not human balance.

Syntax passes. Required full suite reaches its summary with the same five prior failures: single-hit flash hold, two Chronos opening-jump expectations and two StageX right-route expectations. No game.js/test_fl.js edits, commit or push. QA: docs/qa/nightwing_entrance_1027.json. Review: http://127.0.0.1:64044/index.html. The old Stage6–9 Harrier card now points to the latest full film.

All 13 final Chromium film playback/seek/source-hash checks pass across both videos.
