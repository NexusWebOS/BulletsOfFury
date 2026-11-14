# Bullets of Fury — cinematic direction, November 10

The continuation adds authored comic dividers across the mission bridges and nine current-reference space-ship finishing reels. Its later owner is `cinema_comic_1110.js`; details are in `COMIC_TRANSITIONS_1110.md` beside this document. The satellite remains the symbiote-code correction described below.

Mike requested authored comic-style cinematics using the actual pilots and aircraft. The new late presentation owner is `assets/cinema_direction_1110.js`; its asset registry is `assets/cinema_direction_art_1110.js`. Both load after the existing November 10 runtime layers.

### Satellite correction, revision 2

Mike replaced the creature/dragon interpretation with symbiote code. The six-frame `satellite-takeover` bank now uses a completely new titanium/gold communications relay with articulated blue solar arrays, antenna hardware and a parabolic dish. Incoming violet packets infect the receiver, spread as rectilinear circuit corruption through the core and arrays, seize control, and broadcast hostile commands toward Earth. There is no creature in the corrected archive. B403's readings follow the actual infection stage; B404 uses electrical crackle instead of the creature shriek. Decker identifies the symbiote code and the satellite downlink. The new sheet was generated with the built-in image tool; its complete production prompt is recorded in `source-art/generation-prompts.json`. Script and image cache versions were advanced so a refreshed review loads the corrected scene.

## Delivered behavior

- New 96-second opening: a peaceful city, the secret global pilot program, Cole and Decker working together, the crew's relationships, the machine takeover, local-control isolation, the selected pilot's launch, and the lost squad channel.
- New mission bridges after Stages 1–7 and the bonus mission: evidence, readings, travel, return, maintenance, the base alarm, and the reason for the next sortie. Stage 8 retains its existing battle/finale ownership and enters the new true ending.
- New 72-second true ending, crew roll, separate final transmission, and final score card. Easy/Normal completion choices and Arcade retain their existing owners.
- 132 newly generated animation frames in 22 six-frame banks, plus one overhead hangar background. Actions include typing/pointing, harness checks, the sisters repairing equipment, Juggernaut catching a case and playing guitar, radar escalation, the satellite takeover, homecoming, service connection, and all nine aircraft's landing/gear/canopy states.
- Live flight and legacy friendly-flight call sites use exact current native aircraft exports. Generated gear/canopy banks use fresh top/front/rear exports as identity references. No generic replacement jet bank is used for the nine pilots.
- Sliding comic panels, readable bitmap dialogue, radar readings, native sound cues, confirm-to-reveal/advance, and Start-to-skip. Panel motion and scale changes are scoped to cinematic presentation.

The animation is authored comic key poses with held reading beats, not continuous full-frame film. Older compact headset frames remain for some dialogue-only panels. Existing boss combat animation and Stage X battle scenes remain native; friendly aircraft in those scenes use actual ship views.

## Progression contract

`campaignIntroStart` retains the native completion callback. The new story supplies presentation rows to `BOFCinematicDirector`; native settlement, rank, bonus, Forge, save, completion-menu and mission-launch functions continue to own progression. No new reward grant is introduced. Hard/Furious Stage 5 continues to Stage 6; Easy/Normal keeps its completion menu. Both Stage 6 routes retain the correct remaining-threat report and earned Stage X offer. Active co-op pilots are excluded from base guards; Cole/Decker co-op analysis stays with the deployed pair.

Current connected Stage 2/4 landing owner is `pr118S2Exit`, with landing at 10.4 seconds and stats at 11.7 seconds. Do not restore the older November 3 timing fixtures. The live Warden escape calls `cf4PortalHandoff` directly rather than ordinary debrief hooks; the new wrapper plays the portal beat once, then calls the captured native handoff for its score, save and Stage 8 arrival. A cancelled scene can be entered again without leaving a stale handoff latch.

## Sources and rebuild

The complete durable source pack is:

`C:\Users\Mike\Documents\Codex\2026-11-10\you-are-a-cinematic-director-for-3\outputs\BOF-Cinema-1110`

It contains 23 full-size generated masters, fresh native identity exports, generation prompts, 196 fixed-cell PNG exports, and 59 editable Aseprite timelines. The latter include reused native face/ship cells as well as the new artwork. Every Aseprite file was reopened in Aseprite 1.3.18.6-dev and all 196 frames compared without a changed pixel.

`source/build_assets.py` builds the lossless WebP banks, registry, art checks and Aseprite job list. `source/build_timeline.py` combines `source/cinematic-shot-plan.json` with the production overrides and `source/cinema_direction_1110.js`. The compiled timeline has 74 shots in 14 sequences. Fixed cells are even-sized, use one common bank pivot, and are exported directly from masters. Chroma removal removes only connected background pixels so Falva's pink hull is preserved.

Open `Start Review.vbs` in the pack for a native-game scene/pilot/route/co-op review. The review server uses its own browser origin and overlays these exact installed asset names. It does not grant or alter progression in the user's ordinary game origin.

## Verification and scope

Before installation: 86/86 native rendering/identity/clock checks and 50/50 native campaign continuation/input checks passed, with no page exceptions, missing local assets or error console messages. The natural intro clock played all 15 shots and invoked its completion once. Stage 1, the bonus return and the live Warden portal were also entered through their native continuation owners. All 196 exported frames drew through native XART. Screenshots were inspected at game scale. The separate replay interface passed 10/10 control checks.

After-install results and file hashes are recorded in the pack's `verification/` folder and `installation-report.json`. Tests use native continuations and controlled battle-clear fixtures; this is not a full combat campaign playthrough. Sound cues use the game's shared mixer; no new voice performance or music was generated.

The required full game suite already exits 1 on `ReferenceError: difficultyHealthBaseline15 is not defined` in `assets/combat_polish_0927b.js:151`. This is recorded separately from the cinematic checks. `assets/game.js` and `_BUILD_SOURCE/test_fl.js` are not edited by this change. The published Windows installer is not rebuilt. No commit or push is made.
