# Campaign world — September 30, 2026

Local implementation of Mike's expanded campaign-map request. No commit or push.

## What changed

- World expanded from 940×700 to 1400×1200 logical pixels. Stages are farther apart. The central battleground and Stage X node remain at (700,600), the world centre. Fury HQ sits north of Stage 1 at (385,185); the normal overview camera remains centred on the world when selecting missions.
- Stage 9's portal moved from the northeast corner to the far north at (735,90). Its existing unlock, deploy and return cinematics still use the map camera. Fixed `openStageSelect(9)` clamping its cursor to Stage 8 when the bonus portal is unlocked.
- A generated jungle HQ island and the Fury HQ marker sit directly north of the Stage 1 jungle. The existing central island is the battleground; Stage X rebel orbit, plaque and selection stay on that island.
- Generated ruined eastern city coast, mostly offscreen northern mainland, offshore island details, and a locked East Coast USA fire region to the west. Eight newly generated poses animate in place with flames blazing left; the western territory stays completely hidden (see the revision below). No expansion levels, unlocks or manifest were merged.
- Water stays on the existing animated ocean layer. New scenery retains genuine alpha.
- Map pilot uses two cached cardinal plates, left and right, from each pilot's approved hull. Horizontal direction changes switch plates; vertical travel retains its previous heading. No heading interpolation, bank frames or runtime sprite rotation during map movement. Gameplay ship controls are unchanged.
- Clicking the western fire barrier reports `EAST COAST USA - PASSAGE SEALED` without selecting or unlocking a stage.

## Ownership

`assets/campaign_world_0930.js` owns scenery registration, the overview camera, horizontal map plates and frontier feedback. It loads after Realm and before the widescreen HUD. `assets/game.js` contains the world positions, fixed horizontal movement state and the portal reopen fix.

Art: `assets/game/campaign_0930/`. Original generated images and exact prompts/provenance: `_ART_SOURCES/campaign_0930/`. Generator: built-in image_gen. `_BUILD_SOURCE/build_campaign_art_0930.py` reproduces crop/nearest-neighbour runtime sizing while preserving alpha. Three existing expansion scenery files were copied as decorative art only; the western coast is now retained unused.

## Verified

- `node --check assets/game.js` and `node --check assets/campaign_world_0930.js` passed.
- Full `_BUILD_SOURCE/test_fl.js` completed: **6,121 passing assertion lines; final FALVA/LIZZIE BUILD OK, 0 ERRORS; exit 0**.
- Real Chromium probe: `_BUILD_SOURCE/probe_campaign_0930.py`. All eight campaign islands selected through actual held mouse clicks. Keyboard Right selects Stage 2 from Stage 1. 1,080 movement updates retain exactly ±90° headings and zero bank. Both plate directions inspected for all nine pilots. Portal's screen point hits Stage 9. Frontier click preserves stage selection and locks expansion.
- Wide 1920×1080 and compact 1000×900 screenshots inspected; zero page/console errors. Images are in `docs/campaign_0930/`, evidence in `docs/qa/campaign_0930.json`.

The portal reveal still zooms north, while ordinary stage selection keeps the HQ-centred overview. The northern mainland intentionally continues beyond the view. The locked East Coast region now uses four generated alien binary-data poses at fixed coordinates; this is map geography, not a combat wall.


## Previous correction — regenerated fire, no scrolling (superseded visually by v4)

Mike rejected the moving fire texture. The live renderer now uses eight newly generated
16-bit poses of flames blazing left. Only the source cell changes at 12 fps. Destination
position, size and transform stay fixed at a fixed camera; there are no time-dependent
texture offsets, mirrored tiles, opacity pulses or old vertical ribbon overlays.

The canonical label remains **EAST COAST USA / LOCKED / PASSAGE SEALED**. The full region
is opaque in every frame, including before image decode; expansion terrain is never drawn.

- Runtime sheet: `assets/game/campaign_0930/east_coast_flames_v3.png` (1024 square, eight 256x512 cells).
- Cell manifest: `assets/game/campaign_0930/east_coast_flames_v3.json`.
- Exact prompt and generation provenance: `_ART_SOURCES/campaign_0930/east_coast_flames_v3.json`.
- Original: `_ART_SOURCES/campaign_0930/east_coast_flames_v3.png`; generated with built-in image_gen.
- Reproducible crop/nearest-neighbour sizing: `_BUILD_SOURCE/build_east_coast_fire_0930.py`.
- Live animation preview: `docs/campaign_0930/east_coast_usa.webp`.

Native Chromium checks passed: all eight distinct source cells are drawn, the ninth wraps
to the first, destination rectangles/transforms never change between poses, and the fallback
covers the region at alpha 1. Across the live capture there were 160 new flame draws and
zero old curtain, ribbon or hidden-island draws. Animated fire pixels change, with no page
or console errors. Evidence: `docs/qa/east_coast_0930.json`.

The existing native map probe also passed: all eight island clicks, keyboard selection,
1,080 horizontal-heading updates, sealed-region feedback, northern portal hit test, and
wide/compact layouts. Both game.js and campaign_world_0930.js syntax checks passed.
This art/render-only correction did not rerun the combat suite; the last completed full
suite remains the 6,121-assertion, zero-error run recorded above.

Earlier `solar_frontier.png` and `solar_curtain_v2.png` art and previous generation notes
are preserved as retired history. Neither is registered or drawn by the current map.
Their scrolling implementations and earlier SOLAR FRONTIER wording are superseded.

Compact layout follow-up: the frame keeps its original aspect ratio and is clipped at the locked boundary instead of squeezed. The final native animation and campaign probes were rerun successfully after this adjustment.


## Current map treatment — organic fire/smoke front

Mike asked for a less line-like effect that belongs on the map. The replacement v4
generation removes the bright straight seam and uses eight poses of left-blazing fire,
dark smoke, embers, and a strongly irregular transparent perimeter. Ocean animation
shows through the ragged fringe; the fire renderer no longer clips at a vertical line.
The backing ends well inside the dense part of the art. Hidden expansion geography is
still never rendered, and a solid fallback conceals it before the image loads.

Frame selection now runs at 6 fps (half its previous speed) at fixed destination coordinates: no scrolling, rotation,
mirrored strips or moving texture offsets. The East Coast USA lock and navigation are
unchanged. The smoke extends slightly across the old border to integrate with the ocean.

- Runtime: `assets/game/campaign_0930/east_coast_front_v4.png` and matching JSON cell manifest.
- Original and exact built-in image_gen prompt: `_ART_SOURCES/campaign_0930/east_coast_front_v4.png` / `.json`.
- Owner: `_BUILD_SOURCE/build_east_coast_front_0930.py`; measured 887x1774 source, 4x2 panels,
  normalized to eight 256x512 map poses; original RGBA/edge transparency preserved.
- Preview: `docs/campaign_0930/east_coast_usa.webp`.

Native animation checks: eight unique poses and a complete loop, fixed transforms and
destination rectangle, no hard edge clip, fringe overlapping ocean, hidden-island draws
zero. Each source frame has genuine transparency and at least 90 pixels of variation
in its perimeter. Browser page/console errors: zero. Existing wide/compact map selection,
horizontal travel, portal hit-test, and locked feedback checks also passed. Both script
syntax checks passed. This visual-only pass did not rerun the combat suite; the prior
6,121-assertion pass remains the full-suite baseline.

v3 is preserved as retired source/runtime history and is no longer loaded by the map.

Final edge cleanup: the owning builder trims three pixels at each source cell's right edge to exclude the neighboring panel. All eight rightmost frame columns have zero opaque rows, so no faint straight sprite seam survives. Both native probes passed again. Versioned preview: docs/campaign_0930/east_coast_organic_v4.webp.

September 30 timing adjustment: Mike requested slower fire. The eight authored poses now cycle at 6 fps, taking 1.33 seconds per loop. The source builder and runtime manifest use the same rate.


## Map geography correction — HQ north of jungle

The Fury HQ terrain plate is now at (385,185), directly north of Stage 1's jungle
island at (385,370). Its plaque sits on that plate. The map centre at (700,600)
is visibly labeled CENTRAL BATTLEGROUND; it retains the existing Stage X orbit,
five rival ships, Fractured Fury card and selection logic. No campaign node, stage
position, hit area or route was moved.

The new HQ art is generated 16-bit RGBA island terrain matched to Stage 1's map
plate and the approved HQ exterior. Runtime PNG and measured placement manifest:
`assets/game/campaign_0930/northern_hq_island.png/.json`. Original and exact
built-in image_gen prompt: `_ART_SOURCES/campaign_0930/northern_hq_island.png/.json`.
Owning crop and sizing script: `_BUILD_SOURCE/build_northern_hq_0930.py`.

Native Chromium verification passed all eight stage clicks, keyboard selection,
portal selection, sealed East Coast feedback, wide and compact map layouts, and
zero page/console errors. A second check enabled the Stage X rival state and
confirmed its card and orbit remain centered at the old battleground while HQ
appears north of Stage 1. Screenshots: `docs/campaign_0930/overview.png`,
`compact.png`, `hq_stagex.png`, `hq_stagex_compact.png`. Evidence:
`docs/qa/campaign_0930.json` and `docs/qa/hq_stagex_0930.json`.

This map-art correction did not rerun the combat suite; the prior 6,121-assertion,
zero-error pass remains the full-suite baseline.


## Current East Coast barrier — alien binary-data wall (v5)

The former fire and smoke art is retired. Four generated 16-bit alien-data poses
now conceal the locked western sector with an irregular transparent edge over
animated ocean. The wall stays fixed while the glyphs and code filaments flicker
at 4 fps. The label remains **EAST COAST USA / LOCKED / PASSAGE SEALED**, and
clicking the barrier still cannot select an expansion stage.

- Runtime sheet and cells: `assets/game/campaign_0930/east_coast_datawall_v5.png/.json`.
- Preserved master and exact built-in image_gen prompt: `_ART_SOURCES/campaign_0930/east_coast_datawall_v5.png/.json`.
- Rebuild: `_BUILD_SOURCE/build_east_coast_datawall_0930.py`. The fourth generated pose's authored alpha perimeter is shared across the four frames to remove neighboring-panel bleed while retaining each frame's different pixels.
- Current focused Chromium probe: `_BUILD_SOURCE/probe_east_coast_datawall_0930.py`. It checks all four distinct frames, alpha/perimeter variation, a stationary destination, locked label, and zero page/console errors. Visual screenshots are in `_shots/east_coast_datawall_0930/`.

The earlier fire-front notes in this document record the superseded v3/v4 work.


## Binary-row correction (v6, current)

The first alien wall had too much purple crystal structure and too few rows of
code. A new generated single-panel master places dense horizontal 0/1 strings
on dark navy data texture, with a ragged transparent right edge. The owning
builder makes four subtle palette poses from that master: no texture translation,
frame rotation or geometry change. The wall flickers slowly at 3 fps.

- Runtime: `assets/game/campaign_0930/east_coast_binary_rows_v6.png/.json`.
- Generated master and exact built-in image_gen prompt: `_ART_SOURCES/campaign_0930/east_coast_binary_rows_v6.png/.json`.
- Rebuild: `_BUILD_SOURCE/build_east_coast_binary_rows_0930.py`.
- Previous v5 crystal wall remains archived as source and is no longer registered.
