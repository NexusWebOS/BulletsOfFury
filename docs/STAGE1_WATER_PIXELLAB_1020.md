# Stage1 bright-blue PixelLab ocean — October20

Stage1 now uses the accepted Stormglass PixelLab ocean animation in the brighter royal-blue/cyan-white palette of the previous Stage1 water. Tutorial water remains teal. This is a fixed offline palette export, with no new generation or credit charge.

## Art ownership

- Builder: `_BUILD_SOURCE/build_stage1_water_1020.py`.
- Source: approved `assets/game/levels/tutorial/stormglass_1020/water/ocean.webp`; original PixelLab job/provenance in `docs/STORMGLASS_WATER_PIXELLAB_1020.md`.
- Delivery: `assets/game/levels/stage_01/terrain/water_pixellab_1020/ocean.webp` and `ocean.json`.
- Registry: `assets/stage1_water_art_1020.js`, generated together with the atlas/cells.
- Runtime: `assets/stage1_water_1020.js`, loaded after the tutorial owner.

All32 genuine phases retain their order,224x224 cells,112x112 pivot,2px edge extrusion,1824x912 atlas,12fps and alpha. One fixed monotone brightness ramp preserves depth-to-crest ordering. No per-frame fitting, changing scale, temporal interpolation or duplicated poses. Atlas plus registry:350,032bytes. One lazy texture; stage retirement may reload it on return. No runtime recoloring or per-frame offscreen-canvas allocation.

The owner preserves the native liquid-array contract and intercepts only Stage1 water blits. The native animation clock freezes on pause and continues while map scrolling is held; drawing twice does not advance it. Stage1 loading includes the atlas before gameplay. Launch/entry connector uses the same palette. The existing terrain master, land-mask generation, coastline, ground routes, boats, pickups, weapons, collisions and combat stats retain their owners. Other stages and tutorial do not route through this water renderer. Shared legacy water remains for its other users.

## Verification

Native Edge checks14/14, zero page/console/asset-response errors: all32 native cells pixel-identical to the lossless export,32 distinct poses, fixed scale, world/config preservation, native coast/jungle/arena screenshots, held scrolling, repeated draws, pause, all4 difficulties, six other stage owners, Stage1 connector, tutorial teal isolation, lazy loading and texture retirement.

Syntax checks: game.js and both new scripts passed. Full regression suite reached BUILD OK,0ERRORS,exit0. game.js, test_fl.js, Command UI and tutorial owner remain unchanged. These are visual/engine checks, not human survival-rate or laptop FPS certification.

Review: `_shots/stage1_water_1020/review.html` (server8794). Evidence and JSON: `_shots/stage1_water_1020`, `docs/qa/stage1_water_1020.json`. Local only; no commit/push requested.
