# Pixelmap typography and menu concept — October 27, 2026

User approved the original font experiment for HUD, dialogue, speaker names, pilot select and detailed text, and requested a playable text-menu concept.

- `index.html?pixelmap=1`: text-only title, modes, Campaign hub, Arcade/NG+, Co-op and difficulty choices. Native arrow design, inputs, confirmation timing, unlocks and mode routing remain the owners.
- Normal `index.html`: approved typography enabled; graphical front-end menu buttons remain for comparison.
- `index.html?classicfont=1`: original font rendering for comparison.
- Review: `http://127.0.0.1:50240/_shots/pixelmap_ui_1027/index.html` (local review server).

Fury Strike supplies larger labels and fitted speaker names. Command supplies dense details and dialogue. An offline-baked narrow 8px Command bank keeps JUGGERNAUT readable in the existing 68px name aperture. Names and text fit the existing 84px portrait chat plate. Pilot bios fit above the actual three- or five-stat region; the full roster text was checked.

The assets contain 21 fixed-size banks, eight authored palette rows with baked dim states, 95 printable ASCII glyphs per bank, and four banks of the original selector with baked mirrored/white-sweep frames. Every atlas has even dimensions. New font rendering only positions and blits pixels; it does not tint, filter, rotate, add shadows, or rescale individual glyphs at runtime. Existing panel and background drawing remains owned by the game.

Files: `assets/pixelmap_ui_art_1027.js`, `assets/pixelmap_ui_1027.js`, `assets/game/shared/ui/pixelmap_ui_1027/`; reproducible source and the original arrow exports in `_ART_SOURCES/pixelmap_ui_1027/`. The original editable glyph masters remain in `_ART_SOURCES/pixelmap_fonts_1027/`.

Validation: both JavaScript syntax checks passed; 20/20 browser menu/text-fit checks passed. Keyboard wrap/confirm, Campaign -> difficulty -> pilot, Arcade, Local Co-op, B cancellation of its submenu, solo reset of co-op, locked Boss Rush, mouse activation and long speaker names were checked. Screenshots inspected at 1280x800 and 390x844. No browser/console errors in final capture. Controller hardware and the online service were not tested. Temporary browser profiles were used, preserving user saves.

The required `node _BUILD_SOURCE/test_fl.js` reached its final summary (389 cases) with exactly the same five failures as the previous encounter baseline:

1. and the flash is held long enough for a single hit to register
2. dialogue ends with the opening jump warning
3. opening jump lands and returns before chromium activation
4. unchosen right route persists as the opposite Stage X fight
5. Stage X right branch launches a full encounter

No commit or push was requested for this concept.
