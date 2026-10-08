# Asset folders and loading — 7 October 2026

Start with [the searchable asset library](../asset-library.html). It lists physical files and logical frame keys without decoding every image on opening. Each pilot and stage also has an `asset_index.json` and a README. The complete catalog is `assets/data/asset_catalog.json`.

```text
assets/game/
  pilots/
    axel/ cole/ decker/ falva/ freezer/ juggernaut/ lizzie/ maverick/ yuri/
      portraits/       Selection, dialogue and expression reels
      body_frames/     Character poses and animation atlas crops
      ship_frames/     This pilot's aircraft animation
      abilities/       Pilot-specific special effects
      asset_index.json
      README.md
  levels/
    stage_01/ ... stage_09/ stage_x/
      stage/           Backgrounds, highway, terrain and props
      enemies/         Ordinary enemies and their animation
      miniboss/        Miniboss rigs and frames
      boss/            Boss rigs, transformations and frames
      projectiles/     Stage-owned weapon animation
      effects/         Stage-owned impacts and attack effects
      cinematics/      Stage-owned story art
      audio/           This level�s music and stage-specific sounds
      asset_index.json
      README.md
  shared/
    fonts/ ui/ audio/ ships/ campaign/ cinematics/
    player_weapons/ effects/ combat/ atlases/
    asset_index.json
    README.md
```

Original pack names remain beneath the owner/category folder to identify provenance and prevent collisions. Empty categories are intentional. Common sounds, player weapons and the Furyship hull are stored once; pilot palettes are applied by the game. `shared/combat` contains legacy or multi-stage source packs that cannot honestly be assigned to one owner. The inventory identifies unregistered source/support files separately from registered runtime textures. Moving a file does not establish that it is unused, so this pass does not delete unique art.

## How a frame is loaded

The game asks for a stable logical key, such as a boss frame or portrait pose. XART resolves that key to its root texture and authored rectangle. All aliases for the same canonical URL share one `Image` object. Several frames inside an atlas are crops of that image; they are not separately stored copies.

`assets/asset_paths_1007.js` resolves old logical URLs to the owned physical file. `assets/data/asset_locations.json` provides exact file and uniform directory mappings to build tools. These compatibility tables contain strings, not duplicated artwork. Production loaders and current metadata use the new physical paths. They never request artwork from `UNUSED_ASSETS`.

Boot loads UI, fonts and idle portraits. Expensive stage art and portrait mouth reels are deferred. Deployment queues the selected pilot's expressions, player weapon textures and the stage's required roots. Stage 6 deliberately warms its cast. Stage 8 final copied forms retain donor-stage textures through the next encounter's explicit dependency queue.

At a stage boundary, `asset_memory_1007.js` retires previous-stage images and derived terrain/tint/rotation canvases. Shared ship and portrait animation caches remain usable. Reentering a stage loads its roots again. Retirement does not run during a live fight.

## Editing and rebuilding

Edit source frames in their owning folder. Preserve frame dimensions, order, transparency and authored pivots. Do not edit generated atlas rectangles by hand. Use the owning pack builder and inspect its output before publishing a changed reel.

The current combat builders are `tools/pack_stage_runtime_atlases.py` and `tools/pack_stage5_runtime_atlas.py`. They use `tools/art_sources_1006.py` to enumerate migrated and archived inputs in the original logical order and `output_path()` to write into owned folders. Older builders have migrated literal paths, but a historical builder that constructs a new output name must also use `output_path()`; do not recreate old live folders.

The one-time migration workflow is `_BUILD_SOURCE/organize_assets_1007.py`. Its verification mode checks 3,943 moved files and 400 repacked cells against recorded hashes. Seven mixed pilot/terrain sheets were split by owner without changing a cell's RGBA pixels. Originals are preserved under `UNUSED_ASSETS/asset_layout_2026-10-07`; they are excluded from production loading. The portable integrity journal lives in `docs/qa/asset_layout_1007_journal.json`. Archived originals are verified when present.

After adding or editing assets, register their stable keys in the owning manifest, capture the native registry with `_BUILD_SOURCE/asset_layout_probe_1007.py --phase snapshot`, and run `_BUILD_SOURCE/refresh_asset_catalog_1007.py --registry _shots/asset_layout_1007/snapshot/registry.json`. Refreshing inventories never moves art or changes coordinates. The initial migration is intentionally one-shot; do not run `--apply` again.

## Performance and browser scope

Directory organization makes ownership readable; canonical caching, deferred loading, stage retirement and reduced render fill improve the runtime's memory behavior. The opaque playfield uses a canvas context with `alpha:false`. Rendering stays nearest-neighbor.

Automatic quality starts at native resolution when the browser reports four or fewer GB of device memory or four or fewer CPU cores. Otherwise it starts with 2× supersampling. Sustained play frames slower than 19 ms trigger native resolution; gameplay timing and attack patterns are unchanged. `?quality=high` locks supersampling and `?quality=performance` starts native. Missing hardware hints are handled by measured frame timing.

The native boot image estimate fell from 908,601,856 to 168,469,988 RGBA bytes (81.5%). This is the estimate of unique retained decoded images, not process memory or GPU allocation. A single live Stage 8 encounter still has substantial texture residency; large source sheets remain a future optimization opportunity. Tight-loop draw submission measurements do not establish a higher frame rate.

See `docs/qa/asset_layout_1007_results.json` for measured browser checks and timings. Chromium, Firefox and WebKit fixtures cover menus, all pilot portrait/comm poses, production encounter routes and stage transitions. They are protected render fixtures, not completed campaign playthroughs or proof for every physical device. WebKit on Windows is an engine check, not a Safari-on-iPhone hardware test.

The rendering choices follow [MDN Canvas optimization guidance](https://developer.mozilla.org/en-US/docs/Web/API/Canvas_API/Tutorial/Optimizing_canvas). Frame cadence uses [requestAnimationFrame](https://developer.mozilla.org/en-US/docs/Web/API/Window/requestAnimationFrame); it is reported separately from synchronous CPU submission time.
