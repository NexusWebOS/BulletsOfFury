# Pixelmap readability correction — October 27, 2026

Mike reported clipped R/r strokes, difficult small letters and truncated numbers in the pilot/HUD review. This revision preserves the approved family and palette roles while correcting the raster glyphs and their layout.

- Deep chrome shading was removing the readable face of thin legs and bottom strokes. Glyph faces now stay bright through their entire contours; shadows are shorter. Lowercase r and numeral0/8 were redrawn for clearer silhouettes.
- Whole-cell shrinking dropped essential rows/columns in the smallest sizes. Fury below18px, Command6 and the8px narrow name bank now have individually hinted rasters built directly from the authored pixel masters. Every live bank preserves a connected R/r, one counter in0 and two in8.
- Compiled glyphs record exact visible-ink bounds. Measurement, wrapping, fitting and alignment use those complete bounds. Digit advances are fixed within each bank. HUD numeric values use larger solid Command sizes to retain complete strokes after display reduction.
- HUD pilot names are uppercase as in the native UI. The portrait name, Somersault heading, armor/speed labels and weapon-level text use safe apertures. Pilot biographies and stat labels have larger readable sizes while retaining the full text above the stats.

Production owners remain assets/pixelmap_ui_1027.js and pixelmap_ui_art_1027.js. Runtime27 banks are under assets/game/shared/ui/pixelmap_ui_1027; original32 family/palette fonts under pixelmap_fonts_1027. The original sources, refreshed Aseprite documents and reproducible builders are retained in _ART_SOURCES. Script/image versions were advanced to glyph-tops-1027c so a reload fetches the corrected glyphs.

Validation: all27 banks pass stroke/counter/bounds/fixed-digit checks; all palette alpha masks match.20/20 menu checks pass. Actual raster checks confirm45 long numeric runs and all5 tested speaker names stay inside their apertures, including the68x12 name plate. Nine-digit score,99 lives/missiles and 0/5..5/5 HUD cases were rendered; desktop1280x800, compact960x720 and portrait390x844 screenshots were inspected. Final captures report no page/console errors. Both JavaScript syntax checks pass. The required full game suite reached its389-case summary and exited1 with the same five failures as the preceding pass; details in docs/qa/pixelmap_legibility_1027.json.

Review: http://127.0.0.1:50240/_shots/pixelmap_fix_1027/index.html
The previously supplied menu-review page also has refreshed screenshots and a link to the font detail review. No gameplay balance, generated art credits, commit or push in this correction.
