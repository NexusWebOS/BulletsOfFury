# Lost desert airbase — October 7, 2026

Mike requested a regenerated Stage 4 with a more interesting lost desert airbase and a looping highway. `assets/lost_airbase_1007.js` replaces the entire Stage 4 master renderer, including ordinary waves, the miniboss hold, the Sovereign pursuit and its death travel.

The generated native 1024×1536 RGB image contains cracked tarmac, broad clear central highway, ruined hangars, wrecked aircraft, fuel tanks, radar installations, desert sand and winding service roads. The source and deployed image are exact byte copies. SHA-256: `5f427c1778eee4c98cb684d8f914fa33e70656b7c7e7787262b93d940f5ec371`; 3,646,448 bytes. `_BUILD_SOURCE/build_lost_airbase_1007.py` imports/rebuilds the deployment without editing pixels. Exact generation prompt lives in the root-owned `_ART_SOURCES/hardcorps_1007/generation_manifest.json`.

The runtime draws the source at the existing 680px world width with nearest-neighbor sampling. Alternating vertical reflection produces a 2040-world-pixel repeating pair: both join orientations meet on the identical source edge. This retains the approved pursuit-loop technique while replacing the old empty road with the full airbase. There is no source crop, processed alternate image, atlas change, fabricated overlay or recoloring.

The original 3568px wave progression range and 40px/s ordinary scrolling remain. The miniboss holds the actual encounter position. Sovereign pursuit uses 480px/s, with the existing 560/620px/s swerve/flyaway modes, without consuming stage waves. Engagement and death keep the same continuous terrain phase instead of switching to a different road asset.

The terrain belongs to fixed world coordinates. Camera translation reveals other parts of it; the player's position is never used to position its sides. Ground movement is published from unwrapped visual travel rather than a modulo bitmap row, so ground decals do not jump at a loop edge. The source's measured clear paved spine, x=334..690, receives a 20px inset for tank movement, avoiding the old master's obsolete masks and the static wreckage on service aprons. The player's flying movement is unchanged.

## Verification

`_BUILD_SOURCE/probe_lost_airbase_1007.py`: **15/15 native Chromium checks**, zero page or console errors. Both rendered seam orientations had zero mean difference between the adjacent meeting pixel rows. Ordinary progression and visual terrain each moved 40px over one second; decals matched measured terrain displacement. Boss chase moved 480px while map progression stayed fixed. Camera movement changed the visible world scenery; player motion alone did not. Retry reset, miniboss hold, master registration, highway drivability and source/deploy hash also passed.

Screenshots inspected: `_shots/lost_airbase_1007/ordinary-stage.png`, `sovereign-chase.png`, `seam-0.png`, `seam-1.png`. Portable report: `docs/qa/lost_airbase_1007.json`. These are focused terrain fixtures, not a full campaign clear.

Load the new terrain layer after the existing Stage 4 layers. It owns wrappers for `_levelCfg`, `drawLevelMaster`, `beginStage`, `levelSrcY`, and `tankDrivable`. It does not edit `assets/game.js`.
