# Grid21 — separate gritty components and Three.js corridor

Local build `overdrive1014-grid21-r1`, October 14, 2026. Level 7 now uses a real
perspective Three.js corridor instead of the painted, downsampled room image.
The existing enemy, Yuri, Gosfer and Helios character PNGs are retained: all
779 recorded previous PNG hashes match. No new character generations.

## Separate artwork

Twelve independent original generations: repeating wall, floor, ceiling, rear
bulkhead, armored double door, protective cover wall, barrel, crate, bullet
turret, laser turret, door core, cylindrical containment reactor. The object
states stay with their component. 41 unique even-sized PNGs and 45 asset
keys, including four enemy-wall scale aliases. Original images, exact prompts,
source crops, alpha threshold, uniform bank scales, pivots and hashes remain in
`expansion/topdown/art/grid21/source` and the manifest. Owner:
`expansion/topdown/_research/build_grid21.py`; it can rebuild from the retained
sources without the generating chat. No photographic filter or full-scene resize.

## Rendering and gameplay

Three.js 0.186.1 is pinned locally with its MIT license and npm-package
provenance, unmodified official ES modules. The existing HTTP launcher remains
the entry point; no live CDN connection is needed. Module loading finishes
before the game's scripts initialize.

The corridor has 275 independent grid faces merged into material meshes for
efficient drawing. Floor, ceiling, left and right wall surfaces, rear wall
opening, door and black passage have separate geometry. The transition moves
the perspective camera from z=4 through the room into the passage. Fresh cover
appears in the next room; combat stays at the same camera distance, including
the boss encounter.

Each existing character animation frame is its own texture on a Three.js flat.
The sprite pass uses screen coordinates to retain existing aiming, gun sockets,
hitboxes and cover timing. Foreground cover uses a separate perspective pass
after Yuri and before near-side attackers. Legacy projectile/effect drawing
uses a transparent canvas texture layer. The GPU layers composite once into
the game canvas, followed by the existing graphic HUD. Textures use nearest
sampling, no mipmaps, no antialiasing and pixel ratio 1 at native 640x480.
Transparent flats render once, preserving invulnerability blinking and fades.

Only machinery artwork and its turret target width changed; all eight room
cores, elites, powerup collection, cover damage, roll/prone, M30 controls and
boss behavior remain. Small cores show damage only after destruction; turret
hit targets now match the new 40px fittings.

## Verification

- Real Chromium visual checks: 10 passed, zero page/console/asset errors.
- 47 native pixel comparisons: every new registered component plus Yuri and
  Helios matches the native ART draw at scale 1 (opaque RGB difference <=1,
  no alpha mismatch). Even PNG sizes and source pivots checked.
- Raw M30 input checks: 24 passed. These are synthetic HID/button inputs;
  physical controller button presses were not performed.
- Complete Normal mouse route: 137.717s, 1 damage,
  zero deaths, all eight cores and both boss forms; ordinary input only.
- Complete Normal D-pad Retina route: 145.433s,
  1 damage, zero deaths, all eight cores and both forms.
- All seven breach/hop/walk/black/emerge transitions completed; shotgun,
  laser and minigun capsules were collected and actually fired.
- Median renderer measurement: 10.28ms per frame in
  headless Chromium six-frame batches, including the actual GPU-to-canvas
  composite. This is a local measurement, not a hardware-wide FPS guarantee.
- Required base suite completed BUILD OK / 0 ERRORS / exit 0;
  `node --check assets/game.js` passed. That file was not edited.

Screenshots: `docs/qa/grid21_views`. Combined evidence:
`docs/qa/overdrive_grid21_1014.json`. Unrelated local work was preserved.
No commit or push was made. Preview:
http://127.0.0.1:8781/expansion/topdown/index.html?fullscreen=0&build=overdrive1014-grid21-r1
