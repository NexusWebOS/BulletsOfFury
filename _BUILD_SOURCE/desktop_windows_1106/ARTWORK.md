# Fury HQ desktop artwork

Generated with the built-in imagegen tool, then exported to fixed 1024x576 launcher plates. These are new sibling assets; game artwork was not replaced.

## Generation prompt set

1. **hangar-generated.png**: Production game background plate, 16:9, target1280x720. 1990s Neo-Geo/Sega-CD military science-fiction hangar deployment terminal; crisp HD16-bit pixel art. Gunmetal, weathered steel, silver bevels, amber lamps and sparse cyan accents. Straight-on orthographic interface. Left60% dark fighter hangar/runway with distant tiny aircraft; right35% empty black console for four menu choices. Bottom100px empty status strip. Outer45px mechanical armor with bolts/vents. No text, buttons, logo, people or product mockup. Full bleed.
2. **doors-generated.png**: Production 16:9 target1280x720, two rigid closed horizontally sliding armored hangar doors; straight-on flat view, exact central vertical seam, edge-to-edge surfaces. Symmetrical graphite armor and chrome bevels, broad recessed ribs, amber hazard strips below, small orange lamps/cyan latches. Upper middle flat/dark for existing game logo. No text, emblems or surrounding doorway. Crisp HD16-bit Neo-Geo/Sega-CD cutscene style. Rigid halves must slide without deforming.
3. **emblem-generated.png**: Original transparent square Windows app emblem. Heavy graphite hexagonal badge, chrome bevels, four amber lamps, cyan latches. Huge readable chrome/orange enamel F; tiny fighter-wing motif behind it. Bold silhouette at32px, 8% transparent margin, no other letters/backdrop/mockup. Crisp HD16-bit 1990s metal arcade style.
4. **briefing-generated.png**: Production 16:9 target1280x720, straight-on 1990s Neo-Geo briefing console. Outer graphite/silver armor, amber corner lamps, vents, cyan latches. One enormous empty dark navy-black text display x8%-92%,y15%-80%, second empty footer y84%-94%. Decoration at edges only. No illustrations, text, buttons, logos or mockup. Crisp HD16-bit full-bleed texture.

## Existing BOF material

- Main game logo: assets/game/shared/ui/ui/logo_0916/bof_logo.png. Its existing magenta key is exported to alpha; identity retained.
- Bitmap typography: original BOF pixelmap_ui_1027 Fury Strike banks at 8,10,12,14,16,18,20,22,24,26,28 and32 pixels, with original glyph metrics and palette planes. Every launcher/installer label uses these authored glyphs. Panel text is measured, centered, wrapped where appropriate, and fitted by selecting a native bank rather than resampling the letters.
- Sounds: cf_boot, select, selectpilot, furnace_servo_whirr and nsp_booster_ignite. Trimmed PCM copies at balanced launcher levels. The in-game mixer and its assets are unchanged.

## Export and animation contract

ExportArt.cs preserves source PNGs, exports even fixed-size plates and the Windows icon, and authors the status segment/selection sprite offline. The renderer blits these bitmaps and existing glyphs; no runtime gradient, tint, glow, alpha animation, rotating or scaling individual art. The two rigid door halves move through96 explicit position keys. Whole screens share one fixed logical canvas. The generated logo halves move with the doors. UI screens are cached so movement only requires a few image blits. Doors have cinematic and quick timing options.

Production artwork is saved in `art/` beside this file, including the four generated sources, fixed plates, logo-bearing door panels, icon, bitmap font atlases/metrics, motion keys and PCM cue exports.


## November 6 revision B: generated titlebar and real window controls

Built-in image_gen edited the inspected, approved art/hangar.png. The new
source is art/hangar-generated-v2.png; src/ExportArt.cs normalizes to1024x576,
stamps exact BOF Pixelmap Fury Strike glyphs into the titlebar offline and
exports four native window-control identities (normal/hover and restore).
The code only selects/blits these authored images at runtime. No original
logo, font bank, game sprite or sound was regenerated.

Generation prompt:
Regenerate this exact Bullets of Fury desktop launcher background as a refined
original 1990s 16-bit military arcade terminal. Wide16:9 layout. Preserve the
exact composition: outer gunmetal riveted chrome frame, dark aircraft hangar
left62%, enormous black menu aperture right34% from14% to77% height, black
footer aperture across bottom16%. Crisp deliberate pixel-art material and
amber/cyan lamps. Add an attractive thin TITLE BAR across the top, at most8%
height, containing a baked-in engraved custom chunky Sega-style pixelmap label
BULLETS OF FURY left and small engraved FURY HQ around the middle. At top right
create three actual separated recessed SQUARE metal window-control buttons:
amber minus, cyan outlined square, red X, within the top titlebar. No other
words in the menu aperture, footer or left logo area; keep these clear for the
exact custom bitmap typography. Main wordmark overlaid at assembly. Leave
left ceiling dark for logo. Preserve panels/gutters. No people, monitor mockup,
perspective distortion or overlapping ornaments.

Final lettering deliberately uses the game's exact glyph pixels rather than
AI-rendered letters. Generated letter pixels underneath were replaced offline.
