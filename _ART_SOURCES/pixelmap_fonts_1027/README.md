# ColeForge Pixelmap Fonts / revised October 27, 2026

Original hand-authored Sega-era inspired bitmap fonts. Mike approved the family for BOF's HUD, dialogue/speaker names, pilot select and detailed text. No glyphs were extracted from the reference games.

Four families: Fury Strike, Afterburn, Sovereign and Command. Eight baked palettes; all95 printable ASCII characters. PNG, JSON and AngelCode .fnt exports, plus editable Aseprite source and glyph-masters.json.

The readability revision brightens complete glyph faces, redraws lowercase r and numeral0/8, shortens shadows, and uses a tighter readable Command advance. Deep metal colors stay outside the readable face. BOF's compiled runtime adds independently hinted small sizes, full visible-ink bounds, stable numeral advances, and larger solid numeric Command sizes; see docs/PIXELMAP_LEGIBILITY_1027.md in the game. These runtime-specific banks are rebuilt by _ART_SOURCES/pixelmap_ui_1027/build_art.py.

All palette variants are authored offline. Do not apply runtime tint, glow, arbitrary glyph scaling or filters. Align to a shared baseline and fit complete glyph bounds, including outlines. Native source cells remain even and fixed. No target-console binary is claimed.
