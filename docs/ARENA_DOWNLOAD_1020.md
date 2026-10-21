# Downloaded corrupted arenas and Stage2 lava — October20

Mike requested that the approved PixelLab water become lava for Stage2, and that final Dracodia download corrupted versions of the copied bosses' home environments.

## Result

| Native Stage8 copy | Downloaded arena | Origin |
|---|---|---|
|Helicopter,form1|Corrupted jungle, dam cables and infected vegetation|Stage1|
|Phoenix/volcano,form2|Corrupted basalt/machinery over original animated cracked lava|Stage2|
|Harrier,form6|Corrupted blue storm sky and fortress debris|Stage6|
|Hammer,form8|Corrupted orbital space, nebula and infected station fragments|Stage5|

Main Dracodia returns to his existing void arena. Phase1/2 and the invasion ending retain their owners. Native copied-form budgets and the current exactly-four-copy roster are unchanged.

The arena erases into the incoming PixelLab wireframe during the native1.45s form-out, then a top-to-bottom scan materializes terrain during the native1.6s form-in. The actor's existing wireframe download continues above it. A new32-phase PixelLab curtain stitches the scan front across the field, behind pilots and HUD. No new combat delay, warning boxes, reticles, hitboxes, stat tuning or enemy spawns. Native transition protection and combat/audio clocks remain owners. Charge/teleport/materialization cues use decoded shared mixer voices; no new delayed audio queue.

## Native scene/layer ownership

Solid arena architecture is anchored to world coordinates, never to the pilot. Far and near data filaments have distinct rates/depths; sky has separately moving cloud banks. Lava's512-square terrain/wire overlays both preserve the same72.2588percent transparent area, exposing actual untouched nlq3_lava_0..7 pixels. The lava structure uses one shared proportional scene scale for both textured and mesh states, so it is visible from the centered camera. No snapshot crossfade, pixel readback, per-frame canvas allocation or extra animation loop. Pause freezes the scene's simulation clock.

Stage2 gets a separate offline molten-red/orange/gold palette of the accepted32 actual ocean poses:12fps,224-square cells,112-square pivot,2px extrusion and identical alpha/phase order. Existing land/volcano master and gameplay remain unchanged. Original lava is retained for the Phoenix. Stage1 bright blue and tutorial teal remain with their current owners. The palette export spends no generation credits.

## Art and reproducibility

- Stage2 builder/owner: `_BUILD_SOURCE/build_stage2_lava_1020.py`, `assets/stage2_lava_1020.js`.
- Arena builder/owner: `_BUILD_SOURCE/build_arena_download_1020.py`, `assets/arena_download_1020.js`.
- Readable delivery: `assets/game/levels/stage_02/terrain/lava_pixellab_1020/` and `assets/game/levels/stage_08/boss/arena_download_1020/{jungle,lava,space,sky}/`.
- Atlas, cell metadata and registries are generated together. Arena plates512-square, fixed256pivot. Curtain256-square, fixed128pivot,32 real phases/20fps on one1560-square atlas. No per-frame fitting, invented poses, temporal interpolation or duplicated holds.
- Arena assets/registry576,513bytes; lava atlas/registry350,205bytes. All new runtime files together remain below1MiB. Largest new dimension1824px. Arena plates/curtain account for about17.3MiB decoded RGBA; native reused floor/cloud assets remain under the existing cache owner. This is not a sustained hardware benchmark.
- Actual stage environments were exported from the native renderer as identity references. Sources, exact prompts, job IDs, references, seed, generated phases, rejected/unsupported requests and completion receipts are in `_ART_SOURCES/arena_download_1020`. Four PixelLab Pro terrain plates, four matching mesh edits, one Pro effect seed and one PixMiniMax animation. Confirmed generation charges total$1.3326; displayed credit balance$2.63→$1.30. The initial Pro Flash seed failed under service load; unsupported edit attempts submitted no job. The temporary still scan export is archived outside runtime assets.

## Verification

Native Edge21/21,0page/console/failed-asset errors.32 lava phases;32 curtain phases with exact lossless native atlas pixel matches; all16 arena×difficulty native transitions; Stage8 gate and Stage2 isolation; original cracked floor; stable camera pivot; no per-frame arena canvas allocations; main-void return; destroyed Phoenix cannon remains destroyed; actual hit-flash pixel difference; pause; decoded charge/teleport/phase audio.

The first matrix fixture initially tried to skip the existing main body's full attack book; corrected to complete its existing prerequisite before requesting a morph. The cell observer initializes its native roster collector before sampling. Neither repair changed gameplay. Final captures use the actual current side HUD, without the older test fixture's extra top HUD. Native reports and source evidence are not human survival-rate or laptop FPS certification.

Syntax checks pass; complete suite8940passing/0errors/exit0. Core game.js, test_fl.js, Command UI, tutorial and Stage1 water owner remain unchanged. No commit/push requested. Current review:`_shots/arena_download_1020/review.html`, server8794. Portable report:`docs/qa/arena_download_1020.json`.
