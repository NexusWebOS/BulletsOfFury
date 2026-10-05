# Stage 8 code knight and alien effects — October 3, 2026

Local, uncommitted implementation of Mike's October 3 sprite and encounter request, including the subsequent all-direction shield impact/shatter request. No commit or push in this pass. Prior campaign work and unrelated local files are preserved.

## What plays in the game

- The existing Stage 8 knight identity now has generated shield guard, sword wind-up/strike, airborne heavy slash, horizontal follow-up and recovery poses. The heavy landing and follow-up have separate warnings and a recovery window. A generated upright code portal handles disappearance and return.
- The active Stage 8 controller's former little code-wall attacks now raise one full-body binary wall. It grows upward, then loops downward-flowing digits. Its rectangular damage bounds follow the same position and size as the art; the larger colossus gets a correspondingly larger wall.
- Shield hits play an eight-frame impact reel. Breaking the shield launches a sixteen-frame radial shatter animation and sixteen independently moving, spinning crystal/code fragments, covering every direction. The effect captures the wall's current location, fires once per break, keeps the existing break sound, and does not damage the player. The shield stops absorbing damage immediately.
- Generated code-chrysalis transformation frames accompany form changes without adding another health reset. The original three-form encounter and rewards remain.
- Three new alien silhouettes replace existing Stage 8 leech, hunter and solar wave slots: a gravity gyroscope, paired-laser Retina stalker and code prism. Their hulls stay upright while positions orbit. Existing spawn beats are reused rather than increasing wave density.
- New generated FOV corridors and circular Retinas progress green/amber/red, with the asterisk inside its warning sign. Laser aim commits before firing; moving after the lock avoids the beam. Gravity warning spokes match the actual outgoing orb directions and preserve a safe sector.
- Alien and code beams originate at their emitters, use native player-hit handling, and disappear when their emitter dies. The possessed host also uses paired generated code beams. Charge/fire concurrency is capped by difficulty.

## Authored assets and ownership

All new raster art was made with the built-in image generation tool. Source originals and exact prompts are retained under `_ART_SOURCES/stage8_1003/`; `prompts.json` covers the original batch and `shield_break_prompts.json` covers impact/shatter. No SpriteCook or shared atlas was used.

`_BUILD_SOURCE/build_stage8_1003.py` owns extraction and registration. It preserves source alpha, uses measured cells and stable knight pivots, and produces `assets/stage8_art_1003.js` plus `assets/game/stage8_1003/manifest.json`. These must be regenerated together when source/crop metadata changes.

| Family | Frames | Use |
| --- | ---: | --- |
| Knight | 12 | Guard, strike, jump, follow-up and recovery poses |
| Binary wall | 12 | Growth, looping flow, impact/break states |
| Code portal | 8 | Upright teleport |
| Transformation | 12 | Code/symbiote chrysalis |
| Gravity unit | 4 | Alien gyroscope animation |
| Retina stalker | 4 | Twin emitter alien |
| Code prism | 4 | Code laser alien |
| Beams | 8 | Four alien and four code beam frames |
| FOV/Retina/orbs | 12 | Directional warnings, framed sign and ordnance |
| Shield impact | 8 | Local hit flash and cracking energy |
| Shield shatter | 16 | Radial code-crystal explosion |
| Independent shards | 4 | Crops from the generated shatter sheet |

Total: 100 generated animation frames, plus 4 reusable shard crops (104 registered cells). The runtime is `assets/stage8_1003.js`, loaded after `feedback_1002.js`. `assets/game.js` was not edited.

## Verification and reproduction

Completed checks:

- `node --check assets/game.js` and syntax checks of the new runtime/registration/test scripts.
- `node _BUILD_SOURCE/test_fl.js`: final summary reached, exit 0, **6,392 passing assertions, zero failing names**. Previous baseline: 6,287 passes, zero failures.
- `python _BUILD_SOURCE/probe_stage8_1003.py`: exit 0, **42 real Chromium checks**, no page or console errors. Uses `_BUILD_SOURCE/shoot.py`, polls lazy XART readiness, draws through the game's own context and yields between frame batches.
- Native checks cover Normal/Hard/Furious knight phase completion, alien movement limits, real warning safety and beam collision, escape after aim lock, emitter destruction, wall sizing, actual shield-break routing and shards spreading beyond all four wall edges.
- Final rendered screenshots were inspected for wall coverage, emitter alignment, horizontal slash, shield impact, shatter and outward fragments.
- `python _BUILD_SOURCE/review_stage8_1003.py` builds the review from completed evidence and writes portable results to `docs/qa/stage8_1003.json`.

Local review: `http://127.0.0.1:8794/_shots/stage8_1003/review.html`.

Temporary evidence remains under ignored `_shots/stage8_1003/`: full-suite log, verification JSON, screenshots and `knight-combo.webm`. The video is a silent capture of the actual game canvas using controlled Hard encounter/alien fixtures with player protection for inspection. Shield shatter has dedicated native screenshots. These are not full campaign wins or final balance certification; Easy has suite coverage but was not separately played through in the native probe.
