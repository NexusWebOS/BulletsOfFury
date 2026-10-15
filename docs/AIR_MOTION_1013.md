# Airborne motion roster — October 13, 2026

## Delivered scope

87 distinct airborne designs, 2,088 usable frames: eight clockwise turning views and sixteen axial roll poses per design. Includes Voss, Nyx, Rook, Kaia and Jace; all live stage aircraft/airborne creatures; the four maneuver-flight hulls; four stealth palettes; boss-deployed Ash-wing and Hell Wing escorts; Hivewings; Twin Splitter's Prism Needles; Horizon and Dread drones. Ground/naval units and standalone boss hulls are outside the user's clarified scope. The retired generic `drone` hull has no live scheduled spawn; the active maneuver formations use their four dedicated hulls.

The inventory sampled every wave callback twelve times, then explicitly exercised reinforcement paths. Shared artwork is registered once with logical aliases. Ash-wing is a separate aircraft, rather than a palette alias of the larger Lava Fire Jet. `assets/data/AIR_MOTION_1013.json` lists every physical design, logical alias, stage, sheet, cell, pivot, heading convention and hash. Each readable aircraft folder contains `manifest.json`.

## Art and geometry

170 new lossless WebP sheets add 18,746,544 bytes (17.88 MiB). Four existing approved sixteen-frame stealth roll banks are reused without duplicating their files. Original normalized PNG cells and generated sources are retained in the workspace's `output/air_roster_1013`, rather than shipped in the game. Every WebP was checked pixel-for-pixel against its normalized PNG.

Regular frame canvases are 128 × 128; rebels are 192 × 192; reused stealth rolls retain 256 × 256. A bank has a fixed center pivot and one uniform scale. Source islands were extracted independently of grid gutters to prevent neighboring wing tips leaking into a cell. The return poses of the airbase and void maneuver fighters were repaired after the first outputs reversed direction. The Comet bank starts north; maneuver-bank headings start east; other banks start south. The catalogue records these conventions explicitly.

New frames were generated from the current game's actual hulls using the built-in image generator. SpriteCook was inspected but its two-credit balance could not cover this roster; no SpriteCook job or credit expenditure was made. Generated dorsal/edge/ventral views represent axial rolls; they are not flattened canvas yaw rotations. Pose timing is sampled by the game controller rather than treated as a uniform engineering-angle simulation.

## Runtime owners

- Fury jets use their new sixteen-pose bank during the existing evasive roll.
- The stage 1/4/6/8 maneuver formations use their new authored headings and rightward roll banks, retaining their warning lanes, bombs, volleys, collision sizes and cadence. Their controller measures from north, so the new selector converts that angle to the catalogue convention.
- Rebels use new heading/roll bodies, retain independently destroyed wing masks, and keep native pitch somersaults. Rook's separate hook/winch/chain drawing remains outside the body hook. Nyx's back/front cloak spirals remain outside it. Death still owns the existing pilot-matched spin/crash timing and opaque burning hull.
- Intact stealth aircraft use their palette's new cardinal/diagonal views; existing damaged, true sixteen-pose roll and pitch banks retain ownership of those states.
- Other aircraft retain their native effects, modules and attack controllers. During existing turns/barrels the renderer replaces only the matching primary hull and its related tint/shadow images. Native damaged artwork remains in use below half health. Stationary artwork and specialist articulated attack frames remain owned by their original renderer.

This adds usable banks for every covered aircraft; it does not make every enemy perform new barrel-roll attacks automatically. Movement/attack balance was not changed by this pass.

## Loading and performance

Catalogue registration creates no images at boot. Only current-stage headings and that stage's active roll owners are warmed; other rolls load on demand. Original rendering is the fallback while a new image decodes. Stage-scoped paths remain compatible with the existing asset-memory ownership. All 87 designs are not decoded together during normal play. Hit-tinted cell canvases are cached with a 64-entry bound and cleared on stage transitions; normal pose rendering performs no pixel readback or glow processing.

The public `window.BOF_AIR_MOTION` exposes `catalogue`, `pose(id, 'heading', angleRadians)`, `pose(id, 'roll', normalizedProgress)` and `draw(pose, x, y, visibleHullSpan, alpha, optionalFlashColor)`. Angles use east = 0 and south = π/2. Rolls loop in [0,1). For native generic flight controllers, `_air13Motion={kind:'heading',angle}` or `{kind:'roll',t,dur}` supplies an explicit render request; specialist flight owners keep their own pose selection.

## Validation

Every normalized cell was visually inspected. All 2,088 actual delivered frames decoded and rendered in Edge, Chrome and Firefox, with nonempty alpha, even dimensions and no pixels touching the two-pixel frame margin. Each browser passed 20 live stage/difficulty fixtures (stages 1/4/6/8/9 × Easy/Normal/Hard/Furious), plus 120 rebel heading/roll poses, broken-module and opaque-wreck checks. No page errors were recorded.

The full existing game integrity/behavior harness completed with zero errors. The native rebel regression passed all 33 checks: Rookhook movement/interception/co-op, Nyx layered cloak/contact flash, modular hardware, pilot-timed death and blue-ace warning/recovery. Its older cycle assertion was updated to consume the already-existing opening signature before testing the normal Rook supply cycle; combat code was not changed to satisfy that assertion.

These are animation and rendering checks, not a claim of universal 60 FPS or a complete campaign balance certification on physical laptop hardware.

Review: `_shots/air_motion_1013/review.html` contains stage/pilot filters, animation playback, frame scrubbing and every pose strip. The preview animates only the selected design and stops updating while hidden.
