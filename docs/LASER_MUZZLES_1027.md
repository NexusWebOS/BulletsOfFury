# Focused blue laser muzzle correction — October 27, 2026

Mike rejected the Harrier's oversized blue crown. The shared `av3Beam` blue/ice route was drawing a muzzle crop from the crystalline ice-beam reel, upright regardless of the beam bearing.

`assets/laser_muzzles_1027.js` now calls the existing beam body with its optional muzzle disabled and blits a focused cyan-white emission cap at the same physical firing socket. The new sixteen-frame PixelLab VFX Workbench source has a small excitation lip and axial beam throat; no ice spikes, gunfire petals, smoke or explosion. Its common source pivot is [16,32] on a64x64 canvas. Three proportionally baked sizes each contain64 directional poses per phase on fixed64x64 cells, pivot [32,32]. All poses have transparent clearance at the cell edges.

The new effect uses only fixed-size source-over blits, frame selection and positioning. Rotation, scaling and palette appearance are baked offline. The original beam path, dimensions, collision, warning window, sound, damage and attack clocks remain owners. Other elemental beams, Helix/Fusion and standalone charge effects retain their previous renderers. Effects are drawn only with a live beam; there is no detached pool to survive owner death, pause or scene changes.

Source and recipe: `_ART_SOURCES/laser_muzzles_1027/`. Rebuild with Python/Pillow using `build_art.py`; copy compiled PNG/manifest and generated JavaScript to their matching asset directories. Runtime assets: `assets/game/shared/combat/laser_muzzles_1027/`. This is a separate owned bank, so existing atlases remain unchanged. PixelLab effect ID: ba5669e0-cf0d-4acf-9de2-9a14830f7824. VFX Workbench charged no generation credits.

Verification: thirteen native browser checks passed, including a natural Furious Harrier twin-laser release, actual new socket pixels, suppression of the old crystal-crown path, direction agreement within the authored64-pose quantization, all3072 phase/direction/size draws at native cell dimensions, preserved beam arguments and special-effect routing, and stage reset. Before/after native screenshots were inspected. No page, console or asset errors. Both JavaScript syntax checks passed. The required suite reached its389-case final summary and exited1 with the same five existing assertion failures as the prior UI/encounter pass; see docs/qa/laser_muzzles_1027.json.

Review: http://127.0.0.1:50240/_shots/laser_muzzles_1027/index.html

No commit or push was requested.
