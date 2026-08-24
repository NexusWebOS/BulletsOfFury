# BulletsOfFury Generated Cinematic Pack

This folder contains standalone, review-ready art. The live legacy atlas files
and `assets/manifest.js` were intentionally left unchanged.

## Explosions

- `airburst`: center-anchored spherical blast -> rolling fireball -> ember ring.
- `ground_blast`: bottom-center-anchored impact dome -> tall combustion column -> soot.
- Both types include orange, blue, green, and purple palettes. Variant folders use
  names such as `airburst_blue` and `ground_blast_purple`.
- Each animation has 32 RGBA frames with no whole-sprite opacity fade.
- Frame 31 remains a visible authored ember/smoke breakup. The game should hide
  or destroy the effect after playback instead of relying on a transparent tail.
- There are eight animation families and 1,280 individual runtime PNGs across
  the five canvas sizes, plus strips and animated previews.
- Recommended playback: 30 fps (about 1.07 seconds per effect).
- Every animation is exported as individual PNG frames and a horizontal PNG strip.
- Canvas sizes: 128x128, 192x192, 256x256, 320x256, and 320x320.
- `previews/` contains an animated lossless WebP and a 32-frame contact sheet.

Frame naming is zero-based: `frame_00.png` through `frame_31.png`.

## Backgrounds

The three 4:3 scene plates are:

- `storm_bridge`
- `toxic_reactor`
- `ruined_hangar`

Each has a 1448x1086 master plus 1360x1020 and project-standard 680x510 exports.

## Metadata and rebuild

- `manifest.json` lists every output, frame count, anchor, and recommended fps.
- Rebuild all derived frames, strips, previews, and game plates with:

  `python _BUILD_SOURCE/build_generated_cinematic_pack.py`

The build uses one shared scale and anchor per animation. Six generated hero
poses are expanded across all 32 frames with premultiplied-alpha, eased
in-betweens. There is no fade-to-transparent branch: expansion, turbulence,
smoke and ember breakup carry the motion through frame 31 at full sprite
visibility.

Generated palette artwork is retained in
`_BUILD_SOURCE/generated_cinematic_palette_inputs/`. ImageGen supplied the RGB
color variants but repeatedly baked its checker preview into the files, so the
builder applies the validated alpha geometry from the matching transparent
orange master. This keeps silhouettes and anchors identical across palettes.

## Generation prompt set

Built-in ImageGen was used with the supplied `nca_5`, `nca_6`, `nca_17`, and
`nca_40` sheets as style references only.

- Airburst: six-frame horizontal production strip; white-hot ignition, layered
  orange plasma lobes, rolling red combustion, ember-ring dissipation; crisp
  high-resolution retro pixel art; transparent background; no UI or scenery.
- Ground blast: six-frame horizontal production strip; compact ground flash,
  fire dome, tall triangular combustion column, dark smoke and embers; stable
  bottom-center anchor; transparent background; no UI or scenery.
- Color variants: change color only while preserving the exact six-pose geometry,
  timing, scale and anchor. Blue uses white/cyan/electric-blue/navy; green uses
  white/lime/emerald/deep-green; purple uses white/magenta/violet/indigo.
- Storm bridge: empty armored command bridge facing a lightning-torn alien
  coastline; cold storm blue plus amber emergency lamps; full-bleed cinematic
  4:3 retro pixel-art environment; no text, characters, or UI.
- Toxic reactor: empty corroded underground reactor arena with a suspended
  chartreuse plasma core; olive/bronze industrial palette, steam haze and strong
  green rim light; full-bleed cinematic 4:3 environment; no text or UI.
- Ruined hangar: battle-damaged orbital hangar with a broken launch iris,
  burning moon, drifting smoke and orange/blue lighting; open central path;
  full-bleed cinematic 4:3 environment; no text, characters, ships, or UI.

All eight source strips are final RGBA PNGs with zero-alpha corners, preserved
fire/smoke edges, stable palette-matched alpha masks, and no matte.
