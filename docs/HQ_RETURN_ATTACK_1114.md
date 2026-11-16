# Stage 5 to 6: physical homecoming, radar alarm and evacuation

Implemented November14-15,2026 in the original BOF source at `D:/BOF-Downloads/2026-11-14/RevG-source`. This replaces the static post-Chronos orbital/dying plates and the old post5 workshop/chaingun conversation from the previous reel. Those historical files and recordings remain preserved.

## Sequence

Chronos's original native last words, core lock, final missile, ignition and armor breakup remain. At the end of the native destruction, the selected actual Furyship flies north offscreen against moving stars. Earth is absent for the first2.4 seconds of the new return, then scrolls in from above. The ship returns southbound and shrinks into Earth before fading. Native score/drop/StageClear settlement still happens once.

The returning selected pilot's actual normal aircraft approaches the new overhead Fury HQ, scales down and lands. Existing pilot-specific exit frames show disembarkation; actual walking frames carry the pilot through the opening doors. The doors close. A fade leads into one full comic frame of the actual pilot walking through the base, then one full crew reunion frame using the existing happy/ecstatic/cheering poses. This supports every pilot and both co-op pilots; Cole uses the current green-uniform likeness.

All nine actual crew members turn toward a new sixteen-frame radar display. Its authored sweep, contacts and red alarms animate with accelerating native beeps. The seven first-wave aircraft depart through the HQ doors, heading south, scaling up and leaving the frame. The doors close and the exterior stays quiet for five seconds. Enemy jets then arrive, fire, and multiply around the base. Decker and Axel leave last through reopening doors with their original framed roster avatars and the fixed-size metal dialogue box:

> Decker: Dammit! They made it to our base too!
>
> Axel: We gotta tell the others!

The following existing Stage6 radio is scoped to this new scramble so Decker and Axel are correctly reporting from the air. Its native stealth reveal/interception, controls and timing remain. Existing Easy/Normal Stage5 completion and difficulty-choice ownership remains: those modes get the return/landing/welcome, while the radar/evacuation/Stage6 continuation stays on the existing Hard/Furious branch.

## Ownership and artwork

Late owner: `assets/hq_return_attack_1114.js` (HQ19), with `assets/hq_return_attack_art_1114.js`. Original `assets/game.js`, `_BUILD_SOURCE/test_fl.js`, HF17's destruction and protected Stage5 C45/C46/C47/CF48/49/50 combat/rage owners are unchanged. The new after phase delegates back to native settlement. The post5 rows retain the one-time upgrade5 reward.

Built-in image_gen produced the HQ exterior/door bank, radar room/alarm bank and corridor. No SpriteCook used. Aircraft, enemies and all pilot performances reuse actual game assets; no substitute cast generated. Shared fixed backgrounds prevent frame-to-frame scene wobble. Exterior/radar cells418x236 (16 frames each), corridor1672x942, all even. Full sources, prompts and reference: `_ART_SOURCES/hq_return_attack_1114`; provenance/prompt set: `docs/HQ_RETURN_ATTACK_ART_1114.json`. Runtime exports: `assets/game/shared/cinematics/hq_return_attack_1114`.

Door, footsteps, radar beeps, thrusters, gunfire and impacts use the existing shared mixer. Guards keep KD18's consistent460x84 metal frame and original selection-avatar apertures. No standalone/mismatched portraits.

## Verification and recording

- Core regression:8,969 passed,0 failures,exit0. Failing-name comparison remains[] against the November14 green baseline; game.js LF and test_fl.js CRLF retained.
- Native Chromium:84/84 content/roster/scene checks,22/22 lifecycle/audio checks,7/7 final visual/co-op checks. All sixteen rendered radar frames are distinct. Direct draw inspection confirms old static plates never draw and Earth stays absent before the reveal. Seven first-wave ships plus the two guards; no ships/enemies during the quiet pause; enemies begin at least five seconds after departure.
- Actual shared-bus audio decodes were checked for doors, both footsteps, radar beep, thrust, enemy gun and impact. No page, console or HTTP errors in final checks/captures.
- Complete1:57.32 (117.32s) H264/AAC reel,1824x1024 at30fps, native game audio mean-14.3dB/peak-1.7dB, strict full decode with zero errors. Sixteen chapter seeks, geometry/duration, Range206 and browser error checks pass19/19.
- Real Chromium canvas/audio recording at native time: Cole on Hard. Two prepared cinematic checkpoints, no cinematic dialogue skipped. Result/equipment menus between checkpoints are omitted. HQ through the Stage6 card, flight-in and all five opening radio cues is continuous; ends at the first interactive missile interception. This is not a full campaign win, survival test or balance validation.

Video: `_shots/hq_return_attack_1114/stage5-to-6-hq-evacuation.mp4`.
Chaptered review: http://127.0.0.1:8766/_shots/hq_return_attack_1114/review.html
Receipts: `docs/qa/hq_return_attack_1114.json` and `_shots/hq_return_attack_1114/*qa.json`.
Reproducible scripts: `_BUILD_SOURCE/hq_return_attack_1114_{pack,probe,lifecycle,verify_views,record,package,verify_movie}.py`.

Changes are source-only. No commit, push, installer regeneration or release publication in this pass.
