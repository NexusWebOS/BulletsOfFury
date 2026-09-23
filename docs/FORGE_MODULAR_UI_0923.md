# Forge selector correction — September 23, 2026

Regenerated the chamber with five fixed element apertures, a dedicated empty scrollbar lane and a much wider preview window. The old nine-bay overlay and its cropped scrollbar are no longer used by this screen.

SpriteCook kit `178f52c1-01e9-445e-916b-7fadb9233641` used `gpt-image-2.5-sunburst`: one concept and one component sheet, 23 credits total. Finalized eight separate transparent components: track top/middle/bottom, normal/hover/pressed thumbs and normal/hover button housings. The existing authored `nsel_arrow_y` is rotated up/down inside the housings. No new arrow glyphs were generated. Source IDs and reviewed component geometry are in `assets/game/ui/forge_modular_0923/manifest.json`.

The thumb tracks the first of five visible selections. Mouse drag, track clicks, arrow clicks, wheel and keyboard navigation all work. Arrows appear only when additional selections are outside the visible range. Bay clicks only select; they cannot spend a combine. The preview camera keeps the ship near the bottom of the enlarged viewport at a readable scale, preserving room above for the actual weapon effects. The forging/product sequence shares the new chamber geometry.

Verification: `node --check assets/game.js` passed. Real Chromium probes `probe_forge_modular_0923.py` and `probe_forge_megashield_0923.py` passed: actual pointer/wheel/key events, first/middle/last screenshots, all 90 level-one weapon previews, recipe restrictions and persistent shield regression. No page or console errors. Evidence is in `_shots/forge_modular_0923` and `_shots/forge_megashield_0923`.

Full suite log: `_shots/forge_modular_suite_0923.log`. Suite exits 1 with the same 81 failing assertion names as `_shots/forge_megashield_suite_final_surface_0923.log`; no newly failing assertions. Existing unrelated working-tree changes were preserved. No commit or push performed.
