# Missile truck generation — October 18, 2026

Built-in image generation; actual live XART `nef_s1_rocket_buggy_intact`
was exported and inspected as the identity reference. The two source sheets
remain unchanged here. The first contains the eight accepted chassis poses;
its experimental launcher row was rejected for inconsistent tube layout.
The second generates the sixteen accepted launch/reload poses together.
A PixelLab animation request returned no remaining credits; no PixelLab output
is claimed or used for this truck.

Generation frame header:192x256 cells, common proportional scale and fixed
center96,128; transparent background, same high top-down south-facing camera,
Neo Geo / BOF detailed metal, olive paint, blue armored windshield, red/white
ordnance. Chassis bank animates tires, engine fan and amber lamps with a
stationary cab. Launcher bank animates three staggered launches, recoil,
smoke, opening reload shutters, insertion and closure. Entire banks generated
together, no runtime warping or independently fitted cells.

The generator's sheet spacing was approximate. The builder measures connected
sprite bounds, uses the bottom bumper/latch as the physical registration
reference, and translates each pose before one shared0.625 proportional scale.
Exports are uniform192x256, pivot96,128. It does not stretch or fit frames.
`registration.json` retains exact source rectangles, physical pivots and hashes.
Olive-to-black processing changes paint only, retaining ordnance, lamps,
outlines and alpha. Both bank onions are in `_shots/truck_furnace_1018/`.

Runtime: `assets/missile_truck_1018.js`; builder:
`_BUILD_SOURCE/build_missile_truck_1018.py`. No atlas repack.
