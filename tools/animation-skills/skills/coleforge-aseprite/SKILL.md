---
name: coleforge-aseprite
description: Author and export ColeForge pixel art, sprite animations, bitmap UI and effects with Aseprite; use for .aseprite sources and new sprite production.
---

# ColeForge Aseprite

## Standing sprite clarity rule

When this work creates, exports, integrates or reviews sprites or raster game art/animation, apply [the ColeForge sprite clarity standard](../coleforge-sprite-clarity/SKILL.md). Blurry or muddy finished frames are not acceptable; use direct master exports and verify the actual animation at its intended game/display size.


Use `coleforge-sprite-tools` for the shared handoff and `coleforge-art-direction` for identity. Preserve source layers, tags, slices and palette. Inspect existing frames at native size before editing. Use onion skinning to check body mass, silhouette, root stability and action spacing; project animation dimensions take precedence over defaults.

Aseprite is the default for new sprite sources. Keep visual direction and gameplay timings explicit. Produce distinct authored poses for turns, impacts, glow and destruction when required by `portable-sprite-games`; editor transforms are offline authoring operations, not permission to add renderer transformations.

## Reproducible export

The installed build supports batch export. Read the current executable's `--help` before adding options. A typical fixed-cell export is:

```text
aseprite.exe --batch character.aseprite --list-tags --list-slices --data character.json --format json-array --sheet character.png --sheet-type rows --sheet-columns 8
```

Choose columns to fit the actual project. Use explicit paths and a separate staging destination; inspect JSON and importer compatibility before replacing runtime assets. Omit `--trim`, `--trim-sprite`, `--ignore-empty`, deduplication and scaling for fixed-cell exports. Do not add `--all-layers`: it reveals intentionally hidden construction/reference layers. Export only intended visible content. Preserve durations in milliseconds from JSON and the project's simulation-tick mapping. Tags and slices are export metadata, not automatically usable gameplay events or pivots; map them explicitly.

Lua scripting can automate repetitive source changes when supported by this build. Inspect the official API for the operation, work on a copy, and compare source/export before integrating. Do not assume LibreSprite accepts Aseprite Lua scripts.

Check original dimensions, frame count/order, empty timed frames, transparency, palette constraints, and untrimmed rectangles. Check an asymmetric frame to expose accidental flips. For character integration, preserve baseline/root and attack extents through `coleforge-beat-em-up`. For hardware output, hand assets to `coleforge-retro-assets`; an indexed PNG alone is not console-ready.

Official references: [CLI](https://www.aseprite.org/docs/cli/), [Lua API](https://www.aseprite.org/api/). This computer has a personal source-built Aseprite installation; do not bundle its executable with game releases or redistribute it as part of a skills pack.
