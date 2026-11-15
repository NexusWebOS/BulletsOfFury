---
name: coleforge-sprite-clarity
description: Enforce Mike's standing ColeForge sprite and animation clarity rule when generating, resizing, exporting, integrating or reviewing raster game art. Use for blurry sprites, resolution planning, frame pipelines and visual acceptance across ColeForge projects.
---

# ColeForge Sprite and Animation Clarity

Mike established this as a standing ColeForge production rule on November 9, 2026:
**blurry, muddy or softened sprites and animation frames are not acceptable finished artwork.**
Apply it to characters, enemies, vehicles, pre-rendered 3D sprites, scenery, effects,
portraits, bitmap fonts, icons and raster UI in every ColeForge project. It applies
through generation, cleanup, export, integration and review. Current explicit user
instructions take precedence. It does not impose pixel-art shading on ordinary
real-time 3D meshes or authorize unrelated changes to an existing game.

## Standing even pixel dimensions rule

Mike clarified on November14,2026 that every in-game frame in every ColeForge game, including Bullets of Fury, must have **even pixel width and height**. Apply [even frame dimensions](../coleforge-even-frame-dimensions/SKILL.md) during generation, crop normalization, export and import. Use transparent padding and preserve the artwork/pivot. This is not an animation-count rule; odd counts are allowed. Validate cells, not just atlas totals.

## Choose the real detail budget first

Before producing an asset family, establish its intended nearest/largest view,
logical game resolution, renderer/backing resolution, pixel-density mapping and
intended display scaling. Record the native frame dimensions, visible body/content
bounds, padding, pivot/baseline and required distance/size variants in the existing
project brief or asset metadata. A large transparent cell does not mean the body
contains that much detail.

Choose dimensions that retain readable faces, hands, clothing, equipment and poses
at the actual view size. There is no universal 128, 256 or 320-pixel ColeForge frame
size. Preserve approved project proportions and real target hardware budgets. If a
target needs smaller sprites, simplify and re-author deliberate pixel clusters;
do not squeeze dense artwork into an unreadable miniature and enlarge it later.

## Protect the master and export directly

- Keep the highest-quality editable or lossless approved master. Generate or author
  enough genuine detail for the largest required view. Larger file dimensions or
  an upscaled low-resolution frame do not constitute new detail.
- Derive each production size directly from that master. **Never shrink a frame
  and enlarge the reduced derivative to manufacture a near-view frame.** For
  example, `160 -> 128 -> 160` loses detail and is not an acceptable 160-pixel export.
  Export the 128 and 160 variants independently from the approved master instead.
- Offline resizing may prepare a target derivative, but it must be reviewed and
  pixel-cleaned at that target size. For pixel-art derivatives, use nearest-neighbor
  sampling where resampling is necessary. Do not use bilinear/bicubic smoothing,
  blur, a generic pixelation pass or a sharpening filter as a substitute for
  authored outlines, readable clusters and coherent material shading.
- If generated artwork contains painterly softness, mixed edge pixels, halos,
  excessive microtexture or unstable detail, clean it in the sprite editor or
  regenerate it. A nearest-neighbor setting alone does not make it finished pixel art.
- Use lossless production frames and preserve palette/material separation and clean
  alpha. Compressed trailers, recordings, screenshots or video-converted sprites
  are not production masters. Video references may inform poses and style. Proper
  pre-rendered animation should export lossless frames from its original source.

Preserve whole authored poses, fixed cells, complete extents, timings, origins and
foot/weapon registration. Atlas packing must not silently resize frames, resample
them again, introduce edge bleed or discard the metadata needed to reconstruct them.

## Keep the renderer honest

Follow `portable-sprite-games` and `coleforge-portability`. Preserve the intended
native detail through the frame-to-logical-to-backing-to-display mapping. Use the
pixel-art renderer's nearest-neighbor sampling and integer-aligned placement, with
consistent pixel density and integer whole-viewport display scaling/letterboxing.
Do not introduce fractional sprite transforms, CSS scaling effects, smoothing,
filters or arbitrary runtime sprite enlargement to hide undersized assets.
Authored distance/size frames remain the approved sprite-mode approach.

Check source rectangles, texture/atlas sampling, camera positions, backing-canvas
configuration, display scaling and atlas borders when softness appears. Do not
blame source art without checking the renderer, or declare the art sharp merely
because image smoothing is disabled. Keep requested authored transparency and
intentional effects distinct from accidental blur; preserve a readable body and
do not remove approved effects without cause.

## Clarity is a completion requirement

Compare the lossless master and actual exported frames at 1:1 and nearest-neighbor
integer enlargement, then view the integrated animation at native game scale and
the intended player display size over real backgrounds. Check the nearest/largest
view and the smallest required variant; inspect faces, hands, weapon edges,
outlines, lettering, palette edges and alpha contamination.

Review the full animation family, not just its best still. Use onion/overlay review
in the editor and playback to catch soft or inconsistent frames, shimmering pixels,
changing body mass, drifting pivots, unstable equipment and accidental detail loss.
Scale the work to the changed assets; do not force unrelated projects through a
new audit. Compressed preview video is supplementary and cannot establish pixel
clarity in place of lossless frames and the running game.

If softness remains, repair the source, export or rendering path responsible and
review it again. Do not mark the asset family visually complete or describe it as
sharp/production-ready while known blurry frames remain. A palette-only correction
does not also prove that resolution, edge quality or animation clarity was fixed.
State unavailable in-game verification or remaining problems accurately.
