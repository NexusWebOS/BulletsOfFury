# Sprite frame resolution rules

Mike's standing header rule, October 10, 2026: “No odd #'s please, even based
only first and evenly proportioned.” Apply this when generating, normalizing,
exporting or registering new and revised game art.

- **Every delivered frame has an even integer width and height.** Choose the
  intended resolution first. Examples: 64 × 64, 128 × 96, 256 × 192 and
  512 × 512. Rectangular frames are fine; powers of two are optional.
- **An animation bank uses one fixed canvas size throughout.** Every cell has
  the same width, height, aspect ratio and mounting pivot. Reserve space for
  the largest pose, recoil, flame or explosion before exporting the bank.
- **Keep the artwork evenly proportioned.** Use one common scale for both
  axes and all frames in a bank. Preserve the authored aspect ratio and the
  relative scale of modular parts. Independent width/height stretching and
  fitting each frame separately change the unit's shape and are prohibited.
- **Use transparent padding to meet the even-size rule.** If a shared crop
  measures 287 × 380, export 288 × 380. Keep its pixels and physical pivot in
  place. Apply the same padding to the whole bank. Existing source images and
  measured source crop rectangles stay available as provenance.
- **Keep the unit anchored.** Animate the moving parts around their authored
  mounts. Hulls, ships, pilots and modular sockets must remain registered
  across frames and damage states. Detached pieces have their own fixed bank
  and pivot. Different modules can have different even resolutions.
- **Sheets use equal cells and predictable spacing.** Pick an even cell width,
  height, gutter and outer padding. The grid must divide exactly; record the
  cell rectangles and pivots when exporting. Register image dimensions and
  manifest changes together through the owning build workflow.
- **Verify the actual PNGs and native rendering.** Check even dimensions,
  uniform bank geometry, proportional scale, stable mounts and unclipped
  effects. Preview every frame in Chromium before accepting the art.

These are raster frame and sheet rules. Game positions, timing, measured
source rectangles and the scale used to place a sprite in the world retain
their existing meanings. A resolution change uses padding and correct
registration rather than altering gameplay coordinates.

## Generation prompt header

Include this header in future sprite and effect requests, filling in the
approved resolution and physical mounting point first:

> FRAME FORMAT: Deliver [even width] × [even height] pixels per frame. Use
> identical cell dimensions, one common proportional scale and the same
> physical pivot in every frame. Reserve transparent margins for the entire
> animation. Keep stationary fixtures registered; animate the moving parts.
> Export an evenly spaced grid with even gutters and padding. Preserve the
> authored proportions and modular mounting points.

## Current kit

`_BUILD_SOURCE/build_siege_tanks_1010.py` enforces this rule for the new preview
tanks. It extends the shared transparent crop on the right or bottom when
necessary, preserving the existing pixel placement, scales and pivots. Its
58 banks and 553 cells are registered together in the candidate manifest and
preview registry. The production atlases remain under their existing owning
build workflows; future revisions apply this rule there too.
