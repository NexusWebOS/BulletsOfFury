# Wind arsenal — October 11, 2026

Mike requested actual Wind projectiles for every upgrade family and Wind-green
icon borders. The live game now has nine independently generated 16-pose reels:
Gale Slugs, Gust Fan, Cyclone Rack, Wind Lance, Gust Torrent, Tornado Orb,
Storm Mist, Gale Gatling, and Cyclone Sphere. All 45 level I–V weapon badges have
emerald borders, silver projectile bodies, and white Roman level tags. The
separate Stage 6 Wind reward symbol retains its green hexagonal frame.

Review: `docs/previews/wind_projectiles_1011/index.html`. It contains all reels,
a frame slider, onion overlay, the shared combat painter, all 45 badges, nine
native Forge captures, and a Stage 6 combat capture. The five HUD concepts remain
available from the page; no HUD selection has been applied.

## Authored art and registration

- Built-in image_gen: nine whole animation sheets plus two localized border
  edits. Exact prompts, references, original paths and archive destinations:
  `_ART_SOURCES/wind_projectiles_1011/generation_outputs.json`.
- Originals are retained in the default generated-images directory. Archived
  projectile sources and registered inspection sheets:
  `_ART_SOURCES/wind_projectiles_1011/`.
- Both original silver-border sheets and new green-border sheets are retained
  in `_ART_SOURCES/wind_icons_1011/`.
- Shipping projectile cells: 256 × 256, 24 fps, 16 distinct authored drawings
  per family, 144 cells total. Shipping badges: 128 × 128. Both dimensions are
  even. Each reel has a fixed physical pivot and one common proportional scale.
- The returned sheets had uneven physical placement. Registration measures the
  metal body/nozzle and matches the unchanged orb/mist core against its first
  drawn texture. Translation corrects drift; no per-frame fitting, deformation,
  interpolated poses, or procedural replacement sprites.
- The gust's generated silver nozzle is an emitter reference. Its pressure
  plume above the nozzle is the portion painted in combat. Laser body, organic
  crown and root come from the same drawn pose and use the same uniform scale.
- The owning `build_audio_fx_1010.py` invokes `wind_projectile_art_1011.py` and
  `wind_icon_art_1011.py`, rebuilding loose pixels and `audio_fx_art_1010.js`
  together. No shared atlas edits. Source rectangles, translations, scales,
  pivots and source/output SHA256 hashes are recorded in each registration.

## Runtime

`wind_projectile_painter_1011.js` is shared by the review and game.
`wind_projectiles_1011.js` selects the reel from each round's own Wind stamp and
native kind, including heavy-round identity. Co-op shots do not consult the
currently selected pilot or weapon when drawing. All frames warm through the
stage loader; partially decoded reels select a ready pose and completely cold
reels keep the previous weapon renderer.

The update, damage, collisions, velocities, firing cadence, ammunition, range,
and weapon ownership remain with the original simulation. Held columns tile
authored pixels at uniform scale, overlap joins, and clip their endpoints.
Invalid/subpixel columns exit immediately; valid columns have a finite tile
budget. Wind player art does not recolor enemy ammunition.

## Verification

- `node --check assets/game.js`, both new runtime modules, and the review script:
  exit 0.
- Complete `node _BUILD_SOURCE/test_fl.js`: **8,503 passing assertions**, final
  `FALVA/LIZZIE BUILD OK, 0 ERRORS`, exit 0. Previous baseline was 8,468/0.
- Native Chromium projectile probe: **26/26**, zero page/console/asset errors.
  Checks all 144 images through XART and the actual game context, all nine
  native weapon previews at levels I and V, every distinct pose, the equipped
  Stage 6 Wind laser, review controls, and the narrow viewport.
- Existing Wind badge/reward probe: **10/10**, zero errors. Checks all 45 real
  menu keys, the Forge and upgrade menu, the actual Stage 6 reward handler,
  pickup drawing, and Powers Gained.
- Screenshots inspected; laser and gust tile joins corrected before the final
  verification. The game context is opaque (`alpha:false`), so native padding
  checks inspect visible RGB ink. The owning builder checks transparent alpha
  margins on the actual PNGs.
- `assets/game.js` retains LF and `_BUILD_SOURCE/test_fl.js` retains CRLF.
  Temporary logs and captures remain under ignored `_shots/`.

Persistent QA record: `docs/qa/wind_projectiles_1011.json`.
All changes are local; no commit or push was requested for this pass.
