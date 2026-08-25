# Fury Forge — AI Entity & Level Builder

Open `index.html` directly, or serve the Bullets of Fury folder and visit:

`/tools/fury-builder/`

Fury Forge is a data-first editor for the existing 480×720 game runtime. It includes:

- the integrated `CF_AIBuilderUI-Vol.1` 16-bit interface system with chrome window frames, stateful controls, editor icons, and mode-aware pixel cursors;
- portable bundled runtime art for every default roster preview, so the editor works when copied into another Bullets of Fury checkout;
- every enemy archetype and boss from both `game.js` runtimes, plus every pilot ship;
- unwired extracted ice-enemy, tank, and turret drafts;
- a generated vault of every image under `assets/`, all 1,090 extracted reference-library images, and every extracted atlas frame;
- a 1:1 live movement/fire preview;
- cursor-centered mouse-wheel preview zoom from 100% to 800% (`0` or the zoom badge resets it);
- per-frame muzzle, anchor, and damage-region authoring;
- reusable recommended AI patterns and freehand normalized paths;
- stage spawn placement, drag editing, timing, playback, and removal;
- project, selected-level, and image-reference JSON export;
- JSON import, browser-local autosave, and undo.

The default roster contains 41 selectable units: 17 enemy/ground units, 8 mini-bosses, 10 bosses, and 6 pilot ships. Classic-runtime entries are marked `CLASSIC`; unwired art remains marked `DRAFT`.

The export contract is documented by `data/fury-forge.schema.json`. Frame annotations and custom paths use normalized coordinates, so image resizing and runtime scaling do not invalidate authored points.

Rebuild the asset inventory after adding or removing art. The generator combines the repository's current `assets/` tree with the bundled unwired reference library:

```powershell
node .\tools\fury-builder\scripts\build-catalog.js
```

The builder never rewrites `game.js`. Its exports are designed to become the data source for a later runtime adapter without risking the playable build.
