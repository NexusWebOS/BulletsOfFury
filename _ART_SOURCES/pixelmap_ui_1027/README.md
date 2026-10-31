# Approved Pixelmap UI assets

`build_art.py` rebuilds the fixed-size font and selector banks from the approved original font PNGs/metrics under `assets/game/shared/ui/pixelmap_fonts_1027` and the actual BOF arrow exports in `source/`.

Requires Python, Pillow and NumPy. Run it in this directory; outputs are `compiled/` and `pixelmap_ui_art_1027.js`. Copy the generated PNGs/manifest to `assets/game/shared/ui/pixelmap_ui_1027` and the JavaScript manifest to `assets/`. The renderer is `assets/pixelmap_ui_1027.js`.

Font masters and editable Aseprite files remain in `_ART_SOURCES/pixelmap_fonts_1027`. The narrow speaker-name bank is baked offline. No runtime glyph scale/tint/filter/rotation/glow is required. See `docs/PIXELMAP_UI_CONCEPT_1027.md` for flags and validation.
