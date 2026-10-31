# Bullets of Fury expansion UI templates

Open browse.html directly to inspect all three designs and all nine pilots. Select a style and pilot; named dialogue/right-rail plates contain actual BOF portraits and native BOF lettering. Blank variants retain editable name/portrait wells. Left rails intentionally have no baked game values.

Each style folder contains neutral bases, a layout.json with rectangles and body nine-slice borders [left, top, right, bottom], extracted portrait/body components and one folder per pilot. Preserve authored corners with nine-slicing. Do not stretch portraits or character bodies. Fill bars continuously and draw live numbers/status separately.

B Cartridge Classic has pilot-colored interiors. A Command Armor is the selected main-game design. C Fury Broadcast is preserved for future use. Different designs have different source sizes; read layout.json rather than assuming A's coordinates apply to B/C.

cole/ contains complete 512x1024 head-to-boots neutral/report/worried/talk frames, a shared pivot/scale manifest and the corrected identity references. These replace the rejected cropped/cartoonish actors. portraits/ contains the actual pilot portrait references and the dedicated Dracodia portrait. fonts/ contains the existing game's Command Signal font for UI text. source-concepts/ preserves all six original full mockups.

Generated raster art: built-in image_gen. Pilot palettes, source rectangles, final filenames and original references are recorded. Main-game interface code remains in assets/command_ui_1020.js and is not a standalone engine dependency of this art kit.
