# November14 — physical kit, code-only satellite and consistent metal dialogue

Implemented in the original BOF checkout at `D:/BOF-Downloads/2026-11-14/RevG-source`.

Cole now follows the same twelve separate mounting pieces as every other pilot. The old Cole-only AP10 baked-strip interception is removed; SF14 applies the shared hardware effects to him too. Native kit size, flight/orbit positions, entry/audio, assembly timing, conversion and gameplay handoff remain owned by the existing system.

Satellite corruption is **only purple alien code**. Mike explicitly retired the physical tentacled/eyed parasite image on November14; this supersedes the earlier request for the two-eyed creature in orbital footage. Do not use that retired satellite creature again. A new generated sixteen-frame bank shows the recognizable clean satellite, propagating code and a pulsing code downlink. All three legacy satellite keys resolve to the new code bank, including small context inserts. Old source files are retained as historical work, outside active rendering.

Departure uses each selected pilot's actual normal aircraft. Both hull exhaust pixels and extended nozzle plumes now follow the cinematic time, with an eight-step burn pulse. Combat ship controls and space-conversion timing are unchanged.

Metal dialogue uses one460x84 authored frame, scaled proportionally to the native viewport. Box dimensions no longer grow with speaker, text length or requested old width/height. Long dialogue pages within the fixed aperture using the native character budget. Crew always use their framed `pav_<pilot>` selection avatars, including the correct Cole. Full comic/cockpit talking art remains in its existing scenes. Rebels use rust-red metal, Dracodia purple chrome, and CHRONOS metallic blue; all share the same geometry. Enemy portraits retain their authored frames. Native letter sounds, input, radio and combat continuation remain owners.

Late owner: `assets/kit_dialogue_1114.js`. Earlier assembly owners minimally corrected: `assets/audio_extra_1010.js`, `assets/ship_forming_1104.js`. Assets: `assets/game/shared/cinematics/kit_dialogue_1114/satellite-code.webp`. Sources, reference and full built-in imagegen prompt: `_ART_SOURCES/kit_dialogue_1114` and `docs/KIT_DIALOGUE_ART_1114.json`. No SpriteCook used.

Verification:

- Core regression:8969 passed,0 failures, exit0; failing-name list remains empty. Syntax checks passed. Core game.js and test_fl.js are unchanged; LF/CRLF preserved.
- Native Chromium:53/53 checks across all nine pilots, actual12-part blits, all sixteen distinct rendered satellite frames, animated exhaust with an idle combat clock, all crew/enemy avatars/materials and no page/console/HTTP errors.
- Final native verification:16/16, including exact original avatar compositing pixels for all nine pilots and proportional/centered/bounded metal caption geometry at480 and912 widths. The first comparison fixture incorrectly required fully opaque source pixels; older selection avatars have authored partial alpha. It was corrected to compare the complete avatar over the captured native underlay, with **zero tolerance** per channel and no game change. The initial failed receipt is preserved under `_shots`.
- Full95.63s H264/AAC recording decodes with zero errors. Native game audio mean-14.6dB, peak-2.0dB. All8 chapter playbacks, byte-range seeking and browser checks pass11/11. Full post4 continuation once, Stage5 assembly/countdown and live gameplay with gravityShipReady=true.
- These are cinematic checkpoints and focused renderer checks, not full campaign clears or balance validation. Original Stage5 death/rage/combat owners were untouched. No commit/push.

Review: http://127.0.0.1:8766/_shots/kit_dialogue_1114/review.html
Video: `_shots/kit_dialogue_1114/stage4-to-5-code-and-kit.mp4`.
Receipts: `docs/qa/kit_dialogue_1114.json`; repro: `_BUILD_SOURCE/kit_dialogue_1114_*.py`.
