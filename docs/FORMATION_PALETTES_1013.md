# Mini-aircraft stage palettes — October 13, 2026

Requested liveries now apply to the small formation aircraft: silver for Stage 1,
camo green for Stage 4, and black/navy with blue highlights for Stage 6.

`assets/formation_palettes_1013.js` maps the existing authored heading and barrel
roll sheets when XART first returns them. This includes both modern AIR13 banks
and legacy VP12 fallback banks. It changes RGB only; frame dimensions, alpha,
pose spacing, pivots, collision, missiles and movement remain unchanged. Existing
panel shading supplies the camouflage contrast. Cockpit/engine highlights and
dark outlines remain readable.

The original files remain the source of truth. No duplicate shipping images or
generated artwork were added. The browser caches each finished palette canvas;
there is no per-frame pixel conversion. Stage readiness warms available banks,
and stage changes/memory retirement release the derived canvases.

Native Edge verification: all 12 heading/roll/fallback sheets retain byte-exact
alpha and even dimensions. Each changes hundreds or thousands of visible pixels.
120 repeated accesses per sheet reuse the same canvas with zero rebuilds.
Each stage uses 2,162,688 bytes (about 2.06 MiB) for these four cached sheets;
retirement returns the cache to zero entries/bytes. The test used actual game
updates and rendering on Stages 1, 4 and 6, with zero browser errors. Both native
gameplay captures and source/live-palette contact sheets were inspected.

Reproduce with `_BUILD_SOURCE/probe_formation_palettes_1013.py`.
Portable evidence: `docs/qa/formation_palettes_1013.json`.
Local captures: `_shots/formation_palettes_1013/`.
