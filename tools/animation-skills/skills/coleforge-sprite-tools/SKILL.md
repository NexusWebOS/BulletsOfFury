---
name: coleforge-sprite-tools
description: Choose ColeForge sprite editors, atlas tools and level editors; preserve source artwork and export contracts when preparing game assets.
---

# ColeForge Sprite Tool Workflow

## Standing sprite clarity rule

When this work creates, exports, integrates or reviews sprites or raster game art/animation, apply [the ColeForge sprite clarity standard](../coleforge-sprite-clarity/SKILL.md). Blurry or muddy finished frames are not acceptable; use direct master exports and verify the actual animation at its intended game/display size.


Choose the tool from the project's source files and requested result. Preserve an established editor and importer. For new sprite work, default to Aseprite unless Mike chooses another tool. Load only the selected tool skill.

| Task | Skill |
|---|---|
| Pixel art, layered animation, bitmap HUD, authored effects; .aseprite/.ase | `coleforge-aseprite` |
| Existing .pxo work or requested Pixelorama authoring | `coleforge-pixelorama` |
| Existing LibreSprite project or requested free editor workflow | `coleforge-libresprite` |
| Pack separate finished images for a compatible atlas importer | `coleforge-spritesheetpacker` |
| Existing .ldtk project or new LDtk level pipeline | `coleforge-ldtk` |
| Existing .tmx/.tmj/.tsx/.tsj project or Tiled pipeline | `coleforge-tiled` |

Read `portable-sprite-games` and the relevant ColeForge domain skill for the actual game. Editor selection does not change the engine, art direction or rendering policy. Use `coleforge-beat-em-up` for character animation and `coleforge-retro-assets` for native console conversion.

## Asset handoff

Keep the editable source authoritative and exports reproducible. Inspect the current importer before choosing grid versus packed output. Record source path, logical cell size, frame order and durations, animation tags, root/pivot, attachment points, hit/hurt boxes, palette/transparency convention and output paths in the existing project format. Do not invent missing metadata or replace gameplay collision with visible pixel bounds.

Export at native scale with nearest-neighbor pixels. Preserve empty timed frames. For fixed cells, do not trim, rotate, merge duplicate frames or resize individual frames. Packed assets require an importer that restores original dimensions and trim offsets around the original pivot; reject rotated entries for the authored-sprite renderer. Offline transformations may be baked into distinct authored frames under the project rules.

Review a representative animation, asymmetric facing frame and empty frame where present: source appearance, reconstructed exported pixels, timing, root alignment, and in-game native-scale playback. Menus need controller-focus states and bitmap lettering; effects need readable startup/impact/recovery frames. Actual game integration is required before claiming in-game verification.

For new pipelines, keep editable sources and generated runtime exports distinguishable using the project's folder conventions. For existing pipelines, preserve their paths. Record tool version and export options when reproducing assets matters. Preserve original sources during cross-editor conversion; PNG strips cannot retain all layers, tags or editable effects.

## Installed environment

Tools live under `C:/Users/Mike/Desktop/Retro Dev Tools/Graphics`; path details are in [references/tools.md](references/tools.md). Check availability and version rather than assuming the recorded install remains current. Use proven CLI/file operations first; GUI presence does not prove native app automation is available. Report exactly which export, source edit or visual review was performed. Never claim to have used a GUI that could not be controlled.

## Console and handheld handoff

When these assets are for a native console or handheld, route through `coleforge-retro-workflow` and the selected platform skill, then `coleforge-retro-assets`. Keep editable artwork, explicit root/timing/collision data and target-specific derivatives. Editor export success does not establish hardware palette, tile/texture, memory or scanline compliance. Game Boy Color and Game Gear need their own profiles; combined CD+32X needs a separate integrated graphics plan.
## Standing retro reference direction

For every 16-bit or retro game Mike creates, including retro-styled host games and native console/handheld work, apply the [standing retro art direction](../coleforge-art-direction/references/retro-art-direction.md) as a default visual reference. Mike adopted the selected art styles on November 6, 2026; he does not need to name those games again. Choose the family that fits the genre/camera, retrieve actual relevant images, preserve approved project identity and the current request, and retain authored-frame graphics. Adapt detail to the actual target rather than inventing a shared hardware limit. This adds art direction; it does not approve new mechanics, replace unrelated existing art or establish an unauditioned sound signature.
