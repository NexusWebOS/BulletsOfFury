# Satellite discovery, workshop comic and escape — November 14

Mike requested an approaching fire wave and actual ground rumble during the volcanic departure, removal of the attached fire ring, moving water during Stage 3's fly-in, a rewritten alien-satellite discovery and a six-panel Cole/Decker workshop comic with a clearly top-down Photon Cannon test. He also requested the complete Stage 4-to-5 cutscene after these changes.

This pass targets the original BOF checkout on D:. The owner is `assets/cinematic_rework_1114.js`, loaded after `cockpit_talk_1114.js`, with its generated manifest `cinematic_rework_art_1114.js`. The prior native owners still handle dialogue reveal/input, rewards, upgrade UI, cinematic completion and Stage 5's space-kit assembly. The core game and test files were not edited.

## Escape and water

The ship-attached `fchg` fire ring has been removed from the post-Stage-2 cinematic. The existing actual aircraft and animated thrusters remain. A new eight-frame transparent volcanic wave moves across the ground behind the departing aircraft. It is drawn as one continuous full-width authored effect, with no tiled vertical joins. Bounded terrain-only camera offsets provide ground rumble while captions and gameplay player coordinates remain stable. Native ground impact and firewall cues accompany the escape. The earlier terrain-bounds repair is preserved with a seven-pixel source inset.

Stage 3's lake connector and incoming lake now share one moving tile phase based on native fly-in speed. Its water frames also animate during LAUNCH, where the normal gameplay effects clock is paused. The render-only water phase carries into PLAY, then continues from the gameplay clock. No player, map-distance, stage progression or world-camera state is changed to create this motion. Other stages delegate to their existing material owners.

## Story

After Stage 3, Decker explains the restored network at the frozen base, a distress-signal virus from a Fury satellite, and code he cannot understand. Cole questions whether the threat comes from outside Earth. The team discusses tracing the source in space and recovering Federation prototype attachment suits from an airbase 500 km east. All nine pilots participate. Cole decides the team will go.

The backup-power-cell objective is removed from the active post-Stage-3 and post-Stage-4 scripts and continuity metadata. The later scene instead confirms that the Federation aircraft attachments were recovered and adapted, shows the existing satellite feed, and prepares the trip to orbit. Decker/Cole's native remote support substitution remains. Maverick's homing lasers retain their original combat stats. The previously earned Stage 3 and Stage 4 upgrade events remain exactly once per scene; the Photon demonstration grants no weapon tier.

## Generated panels

The new workshop uses six complete illustrations on a three-column, two-row page. The camera moves east across the upper row, southwest to the lower-left panel, then east across the lower row. Current and neighboring panels fill the view; there is no unused black reaction panel. Full panel proportions and complete heads/hugging arms remain visible. Captions use the existing comic frame and letter reveal.

The sequence includes the prototype reveal, Cole reaching toward Decker, their hug, Decker's restraining-order joke, the unfinished cannon, and Cole's reassurance and departure line. The weapon demonstration is an eight-frame true overhead view of the prototype, with charge, muzzle flash, coherent white/violet beam, terminal impact and recovery. Its bank is turned a quarter-turn offline to fit the wide presentation, then displayed at one proportional camera scale. Native charge and Level 7 beam sounds own the demonstration.

Built-in image generation was used; SpriteCook was not used. The approved new Cole and Decker cockpit references supplied face/outfit identity. Three accepted banks contain 22 frame slots: six workshop panels, eight cannon frames and eight transparent fire-wave frames. A first side-view cannon candidate was rejected in favor of the actual overhead view. Exact prompts, references, accepted source sheets, hashes and export metadata are in `docs/CINEMATIC_REWORK_ART_1114.json` and `_ART_SOURCES/cinematic_rework_1114`.

## Verification and recordings

The native Chromium probe passes 35 checks, including actual effect-bank draws, absence of `fchg` draws, terrain framing, unchanged gameplay player coordinates, all six workshop panels, cannon animation poses, all nine pilot story/upgrade contracts, and Stage 3's moving/animated water through its complete native arrival into PLAY. Screenshots were inspected for the escape, hug, cannon and water.

Syntax checks pass. The full core suite reaches its final summary with 8,969 passing assertions, zero errors and exit 0. The prior failing-name set was empty and remains empty. Durable evidence is `docs/qa/cinematic_rework_1114.json`; raw logs and screenshots are under `_shots/cinematic_rework_1114`.

The review page contains two fresh complete cinematic reels: corrected Stage 3 (departure, arrival, HQ discussion and workshop) and Stage 4-to-5 (Federation kits, satellite feed, ascent and native aircraft attachment/assembly). They use real game canvas/audio capture and native dialogue timing. Gameplay between scenes is omitted; these are cinematic checkpoints, not campaign wins. Final media receipts and chapter playback checks are saved alongside the raw captures.

The corrected Stage 3 reel is 214.05 seconds; the Stage 4-to-5 reel is 92.36 seconds. Both H.264/AAC MP4s decode without errors, retain audible game audio, and peak below clipping (−2.0 and −2.1 dB). Nineteen browser movie checks pass: complete dimensions/durations, every chapter's actual decoded frame, byte-range delivery, and no page/console/HTTP errors. Stage 5's native assembly and countdown both appear, and its gameplay handoff retains `run.gravityShipReady=true`.

Preview: `http://127.0.0.1:8766/_shots/cinematic_rework_1114/review.html`. The Stage 4-to-5 player is first, with the corrected Stage 3 player and six-panel art below it. Earlier previews are retained.

No commit or push was performed. Previous recordings and artwork remain available. Reproduce native checks and films with `_BUILD_SOURCE/cinematic_rework_1114_probe.py`, `_BUILD_SOURCE/cinematic_rework_1114_record.py` and `_BUILD_SOURCE/cinematic_rework_1114_package_movies.py` while the game is served on port 8765. The chapter preview uses the existing byte-range-capable loopback server on port 8766.
