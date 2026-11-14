# Chronos / Dracodia: rigid hammers and authored rage — November 10, 2026

Mike's correction: the hammer head must remain joined to the side/middle of the cylinder. It must never become an axial club, swap heads, or slide along the handle between poses.

## Shipped source changes

- One immutable blue weapon master and Mike's exact approved HC23 spiked purple master. Every attack pose rotates the whole head/handle assembly together offline. Fixed head-to-grip distances: 100 px Chronos, 105 px Dracodia. 80 whole attack poses, with regular, chromium, red rage, white hit and red hit materials. The new clean body layers avoid destructive erasing of a flattened hammer/body image.
- Stage 5 detached hammer: 32 authored headings from the same first canonical master view. Replaces the inconsistent old eight-view sheet. Stage 8 keeps its existing rigid approved-master detached weapon.
- Native choreography retained: one jump to the target, then planted strikes. Normal: one downward contact. Hard: two downward contacts. Furious: two downward contacts, recovery, left sweep and right sweep. Both versions have chromium attack frames.
- GPT-generated whole-body charge and alternating/dual palm gesture banks, registered at a common root. Established helmet/head pixels retained. Charge uses 16 poses; palm gestures use 24 poses at authored foreground and background sizes. 128 prepared poses total. Shots and warning lanes originate at the actual current palm sockets.
- Stage 5 keeps native rage timing, permanent hammer discard, HP and collision. Stage 8 copied Chronos now uses the same empty-handed charge, background wave opener and foreground/background palm/wave cycles, with purple laser artwork. It retains RD74's native body/HP owner rather than acquiring a fake Stage 5 state. Red lightning, red rage materials and authored hot smoke rings remain shared.
- Prepared hit materials eliminate repeated runtime body masks. Charge lightning is driven once by simulation (26 strikes), instead of repeatedly rebuilding glow/lightning canvases in rendering. Images, throw cells and first raster preparation load behind the stage-loading gate.
- No core game.js changes. Rewards, foreground-only damage, real white hit flashes, native audio mixer, destruction and later form progression remain under their existing owners.

## Runtime owners / order

`rigid_hammer_art_1110.js` overrides BA119 attack metadata before `boss_animation_1109.js` initializes its frames. `rage_palm_art_1110.js` / `rage_palm_1110.js` follow the existing boss and ball owners. `rigid_hammer_1110.js` supplies the detached Stage 5 prop. `boss_preview_loading_1109.js` stays last. Do not load the unused interim rigid_hammer_flight_art_1110.js alongside the final rigid_hammer_art_1110.js.

Do not rerun older strike/frontal installers over these final bank overrides.

## Verification

- 38/38 native hammer checks pass: Normal/Hard/Furious, regular/chromium/rage where applicable, planted root, contact counts, real white hit feedback, frame use and no browser errors.
- 9/9 native rage checks pass: 16 charge poses, 26 once-only strikes, permanent discard, actual palm emission sockets, both depth cycles, purple shots, HP preservation, protected background and damageable foreground core. No browser errors.
- All 80 assembled attack cells remain within their fixed 576×576 cells. Source head/handle geometry is invariant; masters, authored Aseprite files and metadata are retained under `_ART_SOURCES`.
- Syntax checks pass. Full `test_fl.js` still stops before completing at the pre-existing `difficultyHealthBaseline15 is not defined` in `assets/combat_polish_0927b.js:151` (runner line 4537). This pass does not claim that full suite is green.

## Performance evidence and limits

Real Chromium RAF, same god-mode observer fixture, new browser run. Raw measurements are retained in docs/qa. The recurring canvas creation and typical frame cost improved substantially. Cold outlier stalls remain, so this is not a claim of a locked 60 FPS on every frame.

| Phase | Mean FPS before → after | 95th percentile frame ms before → after | Temporary canvases before → after | Worst frame ms before → after |
|---|---:|---:|---:|---:|
| charge | 23.44 → 39.9 | 116.7 → 17 | 3563 → 75 | 666.5 → 1483.2 |
| volley | 51.11 → 57.02 | 33.3 → 16.8 | 535 → 355 | 166.6 → 133.3 |

The worst cold-charge gap increased in this sample despite the much lower recurring effect cost. Further whole-game cold-load profiling is warranted; no false claim of eliminating all engine stalls is made. Small save/restore of the loading preparation area and Stage 8 ring parity were added after this sample; final visual/mechanics checks cover those changes.

## Native recordings

- `_shots/rigid_hammer_1110/chronos-hammer.mp4`
- `_shots/rigid_hammer_1110/dracodia-hammer.mp4`
- `_shots/rage_palm_1110/chronos-rage.mp4`
- `_shots/rage_palm_1110/dracodia-rage.mp4`

These are actual live engine recordings with the native audio mixer, an invulnerable observer and firing disabled. No animated mock-up replaces the fight. GIF excerpts are in each review folder. The separate rigid-hammer-rotation GIF is an asset inspection preview, not gameplay.

## Sources / rebuild

- `_ART_SOURCES/rigid_hammer_1110`: four accepted GPT body sheets, immutable weapon masters, production Aseprite source, body-build.py, body-author.lua and flight-author.lua. Old head-erasure prototypes are excluded.
- `_ART_SOURCES/rage_palm_1110`: four accepted GPT gesture sheets, approved head references, six Aseprite banks, source jobs/manifests, author.lua, build.py and projectiles.lua.
- `_BUILD_SOURCE/rage_palm_1110`: self-contained native test, profiling and recording fixtures, seed119.js and capture.json.
- `_BUILD_SOURCE/rigid_hammer_1110`: native combat checks and recorder. Its recorder shares the rage fixture seed/capture files.

Builders use Aseprite in batch mode; set their W/output paths to the intended working directory before rebuilding. They author final raster poses offline. There is no new runtime weapon rotation, silhouette construction, recoloring or shader glow.

Current source build only. No installer rebuild, Git commit or GitHub upload was requested in this turn.

Core game.js SHA256: `b46bb789b6344f31d0ecba126169447d491152670c09decc6da624bc4b5d2215`
