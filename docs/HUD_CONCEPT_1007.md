# Top HUD concept — October 7, 2026

Mike supplied a layout sketch and requested inspection, comparison and generated art. The resulting package preserves its five groups, three lower tabs and separate boss lane, using the existing BOF pixel-metal style.

- [Comparison gallery](../_ART_SOURCES/hud_concept_1007/review.html)
- [Generated concept](../_ART_SOURCES/hud_concept_1007/hud-concept-v1.png)
- [Empty frame source](../_ART_SOURCES/hud_concept_1007/hud-frame-source-v1.png)
- [Design comparison and integration contract](../_ART_SOURCES/hud_concept_1007/README.md)
- [Exact built-in image generation prompts](../_ART_SOURCES/hud_concept_1007/prompts.json)
- [File hashes and alpha metadata](../_ART_SOURCES/hud_concept_1007/manifest.json)

The live HUD was captured in real Chromium, Stage 4 assets ready, with zero page or console errors. The local comparison gallery was checked at desktop, 480-pixel preview and 390-pixel mobile widths, including light/dark backing, with no recorded errors or mobile horizontal overflow.

This is concept/source artwork, not a runtime HUD replacement. No gameplay, atlas or runtime loading changes were made. Sample labels and counts are illustrative. Before integration, prepare compact clean frame slices, use live native bitmap text and the existing weapon icons, preserve all gameplay data, and reserve layout space at load time. The generated source proportions are taller than the sketch; follow the sketch's compact budget for final layout. Empty-frame segment counts are decorative, not gameplay capacities. The source remains outside assets/game so it adds no browser preload or decoded texture cost to the current game.