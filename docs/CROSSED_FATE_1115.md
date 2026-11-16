> Presentation and progression superseded by CITY16 later November15: StageX is mandatory before Stage7; new rural split, generated pursuit plates,16-phase registered exhaust, eight post6 beats and city debrief/chibi travel. Earlier optional-choice/movie descriptions below are historical evidence. Route outcomes, actual encounters, messages and awards remain. See [CITY_RESCUE_1115.md](CITY_RESCUE_1115.md).

# Stage6 — Crossed Fate branches, November 15, 2026

Original BOF in D:/BOF-Downloads/2026-11-14/RevG-source. Mike requested difficulty-dependent split flyovers, remaining city opponents, Harrier crash/Storm Cannon escape, two map achievements and alternate-route password messages.

## Routes

| Stage6 difficulty and victory | Remaining city encounter | Map aftermath |
| --- | --- | --- |
| Hard: Harrier defeated | Rebel Fighters | Fury wing and remaining Rebels head toward the city. |
| Hard: Rebels defeated | Harrier | Fury wing and Harrier head toward the city. |
| Furious: Storm Cannon defeated | Rebel Fighters | Harrier and Fury wing reach the city; native explosions/scorches/smoke damage the city, Fury fire brings the Harrier into a48-frame720-degree burning crash. Crossed Fate unlocks. |
| Furious: Rebels defeated | Actual Harrier, on Furious | Storm Cannon flies west off the map while the Harrier reaches the city. Road Not Taken unlocks. |

The existing internal Thunderhead/FB112/TM115/TC119 boss is displayed as STORM CANNON; native modular combat remains. Furious's large Harrier passes first, faster, followed by Storm Cannon on the leftward/northwest path with independent authored shadows. Storm's native exhaust is16 frames. The native split clock runs1.35x during the flyby; its existing Rebel conversation remains. The left pursuit card is STORM CANNON on Furious and HARRIER on Hard; right remains ROUGH RIDERS. Native input and actual encounter dispatch own both choices. The new card uses the existing MW21 authored menu frame, current aircraft and five real Rebel ships.

All11 post6 beats remain readable and use current talking-cockpit identities. They discuss clearing the sky, actual remaining city contacts and an optional underground contact. The last beat stays in the sky, regrouping to choose the next move. No stopped-orders plot or forced sewer travel. After native settlement/cutscene continuation, the map event runs8.4s for the crash or4.8s for the escape. Navigation is held only for that transit; a normal frame still renders. Programmatic unlock-cursor movement cannot accidentally release its camera. City pursuit and Stage7 remain the player's choices afterward.

## Messages and awards

Both messages type in the existing bottom briefing frame at34 characters/s, hold3.5s, then fade. They match Mike's requested text:

- `Play Stage 6 via password STRM on hard to face the harrier!`
- `You let the storm cannon get away! use password STRM on furious for a second chance at redemption!`

STRM now submits Stage6 through the real difficulty picker; BASE4 preserves access to Stage4. The password catalog labels STRM as Stage6 sky pursuit. The old monolith's color-only stage-font hint remains untouched.

Generated gold/laurel/navy medals appear on a compact map achievement card above the navigation/briefing, then in the achievement gallery. Crossed Fate: “Defeated the Storm Cannon Boss on Furious Difficulty.” Road Not Taken: “Defeated the Rebel Fighters on Furious Difficulty.” Each grants200 Furious points once. Route award/persistence follows the existing extensible achievement-bank pattern; local storage key bof_stage6_fates_1115. The profile snapshot and reload include it.

## Native ownership and saves

Only the terminal native achievementEncounterDefeat callback verifies a Stage6 victory. Storm's six actual module pools must fall before its core opens. Rebels require all five real pools, Nyx's native Retina reveal, then their complete burning-spin/crash owners before verification. A prepared preview receipt cannot grant an award. scLeaveStage remains the native bonus/rank/cutscene/autosave owner; repeated settlement is still once-only. A city encounter never rewrites the original Stage6 result, and Furious's city Harrier is excluded from Storm replacement.

campaign.stage6Fate version1 records the actual defeat, difficulty, pilot/wing, target and map progress. Rival24.save/load extends its existing optional story schema. campSuspend remains native. Only the existing completed-stage autosave's rival24 field receives map-progress updates; native stock, ranks, next-stage metadata and explicit slots remain untouched. Loading or revisiting the map preserves the outcome and avoids duplicate points.

## Evidence

native: 34/34 checks, integration: 17/17 checks, rebels: 9/9 checks, routeInput: 19/19 checks, sourceReproduction: 255/255 checks, moviesBrowser: 35/35 checks.

No page/console/HTTP errors in native probes or final media review. Full suite8,969 passes/0 failures/exit0; failing-name comparison remains empty against the preceding HQ build. New route behavior is covered by the live-browser probes; the old VM suite is retained unchanged. game.js remains byte-identical LF and test_fl.js byte-identical CRLF. No commits, pushes, installers or releases.

Three1824x1024/30fps H264/AAC recordings with native game audio:

- split.mp4 —111.24s, actual flyovers, retained Rebel conversation, pursuit choice and full Storm Cannon briefing.
- storm.mp4 —77.77s, all post6 dialogue, city destruction/Harrier crash, password, Crossed Fate and map choice.
- rebels.mp4 —73.56s, all post6 dialogue, Storm west escape, password, Road Not Taken and map choice.

These are prepared native Chromium cinematic checkpoints, with scripted terminal damage through actual combat/death owners, not unassisted campaign wins or balance validation. No dialogue skip is injected. The split checkpoint selects the left route automatically after displaying the choice, then plays all four current Storm Cannon briefing lines and its native continuation. The recorder composites the visible playfield and separate HUD canvases proportionally; it does not change game resolution. The prior Stage7 prepared-entry player-visibility concern remains outside this feature; correcting a capture omission is not a gameplay fix.

Runtime: assets/crossed_fate_1115.js, loaded after current HQ/kit cinematic owners. Registry: assets/crossed_fate_art_1115.js. All approved HQ22 evacuation/swarm, kit, Chronos death, doors, Earth and pilot art work remains. Normal/Easy completion at Stage5 remains native.

Sources/provenance: _ART_SOURCES/crossed_fate_1115. Reproduce exact atlas/medal/registry bytes with python _BUILD_SOURCE/crossed_fate_1115_pack_saved.py. Other scripts with that prefix cover native inventory, build, route input, outcome matrix, actual Storm/Rebel defeats, recording, packaging and movie/browser playback. All temporary evidence is under _shots/crossed_fate_1115; durable receipt docs/qa/crossed_fate_1115.json.

Review: http://127.0.0.1:8766/_shots/crossed_fate_1115/review.html
