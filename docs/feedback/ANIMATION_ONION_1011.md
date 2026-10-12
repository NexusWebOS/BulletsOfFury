# Animation onion correction — October 11

Mike identified neighboring explosion fragments, a clipped late cloud, the
Furnace laser's flat origin, and the wrong red/green fighter silhouette.
These corrections are active in the game and the part-two preview.

- The original atomic image contains **28 poses in seven rows**, not32.
  Measured crops retain those28 poses. Built-in image generation supplied four
  real drawn intermediate poses, producing32 distinct shipping frames.
  Near-transparent gutter contamination at alpha20/255 or lower is removed;
  the remaining authored RGB is preserved. Every output has a384×576 canvas,
  ground pivot192,480 and proportional registration. The renderer uses both
  registered dimensions, avoiding the previous square stretch and clipping.
- The32 fire column textures are registered on384×384 canvases with their
  complete muzzle flare. Sixteen new drawn flared-root poses connect the
  Furnace core to the large column. A curved clip follows the authored flowing
  texture from the narrow nozzle into the existing full width. Attack timing,
  damage and the full column's draw width retain their prior parameters. Beam
  rendering remains finite and bounded at129 draws with its root and muzzle.
- The requested fighter is **whv_ace / skycarrier/ace_top.png**, used by the
  opening Stage6 interception, rather than mission29/bluejets.png. Red and green
  variants derive from that exact family, including its damaged and roll poses.
  Only blue paint changes: alpha, black outlines, non-paint pixels and RGB
  luminance are preserved. The native idle-frame comparison measures11544
  changed paint pixels per palette and a maximum luminance difference of0.459
  byte units from quantization. Flight direction determines south/north/east/
  west heading. The original opening pair is retained.
- The original fighter family has repeated pose aliases. Its30 registered
  blue/red/green cells contain21 distinct plates; these are preserved original
  poses and palette variants, not30 newly drawn animation frames.
- The preview has an **Onion** control, palette selection and one fixed camera,
  physical anchor and scale per bank. Its scale fits the union of all visible
  frame bounds; every pose has at least ten clear pixels on the preview border.
  Asset and screenshot hashes refresh the browser's old cached images.

Owners: `_BUILD_SOURCE/build_part2_art_1010.py`, its measured-crop and repair
helpers, `assets/part2_art_1010.js`, and `assets/part2_combat_1010.js`.
Original sources remain in `_ART_SOURCES/part2_1010`; accepted new sources,
exact prompts, source crops, hashes and audit metadata are preserved in
`_ART_SOURCES/part2_1011`. No shared atlas edits or deleted source art.

The interactive page is `docs/previews/part2_1010/index.html`.
Durable QA is `docs/qa/animation_onion_1011.json` and the refreshed
`docs/qa/playthrough_part2_1010.json`.

Verification: JavaScript syntax checks pass. The complete regression suite
reaches **FALVA/LIZZIE BUILD OK, 0 ERRORS**, with8394 passing assertions and
exit0. An initial run exited1 before the final summary because its canvas stub
lacked bezierCurveTo; the test-local stub is now complete and restored after
the check. Refreshed native Chromium runs pass45 checks: onion preview15,
exact source/live atomic/Furnace8, existing presentation16 and finishing6.
No page, console, renderer or missing-asset errors. Native shots inspect the
actual game context's XART pixels, flight headings, fire origin and all32
atomic draw keys. Protected fixtures establish presentation and continuity;
they do not establish a natural Furious campaign clear. No commit or push.
