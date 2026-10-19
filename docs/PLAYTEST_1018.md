# Levels 1–5 playtest — 18 October 2026

No reproducible runtime or progression blocker was found in the sampled encounters. All five levels reached their native stage-clear screens in assisted Normal runs. This is not a claim of unassisted clears or certified difficulty balance.

## Method and limits

Ran native Microsoft Edge/Chromium using `_BUILD_SOURCE/shoot.py` and the actual game loop. Each level began through normal initialization and proceeded through its natural waves, miniboss, boss, ending and results. No encounter was force-killed; enemy HP, damage, wave clocks and spawns were unchanged. Runs used Cole, single player, with fresh temporary browser saves.

Five stock Normal runs used ordinary damage and default gear. The input bot exhausted its lives in every run: Levels 1–4 at their minibosses, Level 5 at Hammer. These are losses, not clears, and are insufficient evidence to change the game's balance.

The five assisted Normal runs refreshed player invulnerability and began with primary MG level `min(5, stage+1)` and space levels `[3,3,3]`. Weapons acquired and switched during play remained native. These runs test encounter progression and rendering. Additional Hard and Furious runs sampled 95 simulated PLAY seconds per level; these were not full clears. Three assisted replays examined Furnace's head and Hammer's ending.

Frames were stepped in accelerated 60-update-per-second simulation with frequent yields for lazy assets. Screenshots use the regular playfield and full side HUD. Page errors, console/draw errors and failed asset responses were monitored. Actual `XART.get` keys blitted through the game context were logged; cached canvas identity was not used as an asset test.

## Assisted Normal results

Times include PLAY-state encounter transitions; they are simulated times, not real-time performance measurements.

| Level | Result | PLAY time | Enemy projectiles observed | Peak live enemy bullets |
|---|---|---:|---:|---:|
| 1 | Stage clear | 198 s | 519 | 42 |
| 2 | Stage clear | 177 s | 482 | 52 |
| 3 | Stage clear | 211 s | 705 | 24 |
| 4 | Stage clear | 347 s | 1027 | 32 |
| 5 | Stage clear | 278 s | 319 | 64 |

## Observations

- **Level 1:** Razorback and Damkeeper both progressed to defeat in the assisted run. A separate fresh run recorded the opening special crate arriving, opening and granting Cole's Level 1 special. The pickup was not stuck or missing.
- **Level 2:** Magmaward cycled its hunt, strafe, rain and mortar attacks. Furnace progressed through arms, core and head to defeat. The native renderer used all 30 head spin poses; head charge and laser graphics rendered. The full-view screenshot set includes the head eye-burst phase.
- **Level 3:** Frostcruiser remained the ice encounter and completed its core phase. Cryospear exercised machine-gun, missile and ice-volley states before defeat. The sampled main-boss modes contained no laser state.
- **Level 4:** Warden and its wing completed; Sovereign progressed through regular attacks, then panic, ram, departure, overhead pass and permanent north-facing rear attack before defeat. The lengthy generator/shield section eventually resolved normally; this run did not reproduce a shield progression lock.
- **Level 5:** Siege Bomber completed its bombing/flak encounter. Hammer exercised leap, shield, side-hammer, whirlwind, ball, nova, throw, chaingun, storm and recharge states across the main run/replays. The ending traversed drain, pulse, lock, missile, engulf, burst and aftermath. Mid-animation screenshots confirm the initial final-hit flash expires; armor fragments scatter outward with explosions during breakup.
- **Hard/Furious:** Native waves and miniboss attacks ran in all ten short samples with no runtime or asset errors. Stage 4 used the larger difficulty-dependent helper roster. These samples do not establish whether the full difficulty curve is fair.

Cole's fusion-overcharge self-kills occurred in some assisted Level 5 samples/replays. Logged hit sources were `fusionOvercharge`; these are not evidence of helper entry collisions bypassing invulnerability. The primary five assisted Normal clears had zero player hit events.

## UI and regression checks

All **12 native UI checks passed**: ordinary death to Continue; real-keyboard Continue restoring ship/lives/spawn protection; pause freezing combat time; resume; regular 480×512 combat canvas and side HUD at 1280×720, 1024×768 and 1920×1080; natural Level 1 results; traversal through unlocks, Forge, loadout and supplies; map unlock of Level 2; and deployment with the same pilot. Results and map screens use their authored wider presentation. No page, console, draw or missing-asset errors were recorded in these cases.

`node --check assets/game.js` passed. `node _BUILD_SOURCE/test_fl.js` reached its final `FALVA/LIZZIE BUILD OK, 0 ERRORS` summary: **8,754 passed, 0 failed, exit 0**, matching the recorded baseline.

No gameplay or art files were edited for this playtest. Starting hashes of `assets/game.js`, `_BUILD_SOURCE/test_fl.js`, `index.html`, `assets/stage4_panic_1017.js`, `HANDOFF_CODEX.md` and `CLAUDE.md` were unchanged. Existing local work was preserved; nothing was committed or pushed.

## Evidence

- [Full-view screenshot browser](../_shots/playtest_1018/review.html) — one full-window capture at a time, with mode and result labels.
- [Machine-readable QA report](qa/playtest_1018.json).
- Detailed raw reports, input driver and logs: ignored `_shots/playtest_1018/`.

Human balance, other pilots, coop, password encounters, all weapon combinations, audio mixing and real-time performance remain outside this pass.
