# Overdrive — Miami coastline art

## Current revision: Miami sections 03–05 and fortress rise

`preview.html` loads revision 8. Three independent floating map icons and the existing flag states now mark **03 Bridge to Miami**, **04 Center of Miami**, and **05 The Plateau**. The bridge icon sits over the city causeway; the Miami icon hovers over downtown; the plateau icon shows its intact summit and a G.O.D Burst energy corona. The first two sections, animated sludge water, stormy weather, boats, drones, bridges and portal remain.

Use the **Campaign map state** controls to compare the intact plateau, play the post-level-5 lightning transition, and inspect the new above-cloud map. The storm replaces the central plateau with a shattered mesa and giant alien fortress; the sky vista follows from that ascent. These are visual campaign-map states, not implemented save/progression rules. Sky-stage nodes are intentionally unspecified until those levels are designed.

Selected masters are `source/level_03_bridge_v8.png`, `level_04_miami_v8.png`, `level_05_plateau_v8.png`, and `plateau_fortress_v8.png`. Exported icons and the fortress live under `assets/v8/`, with `poststorm_terrain_overlay.png`, `poststorm_world_review.png`, and `sky_map_base.png`. `story_v8.json` records the five location beats and the level-5 G.O.D Burst/storm transition. Rebuild with `node expansion/tools/build_overdrive_coastline_v8.cjs` (Sharp required); `verification_v8.json` checks section markers and asset references. Revision 7 is preserved in `preview_v7.html`.

## Revision 7: six-frame sludge water

The preserved `preview_v7.html` loads revision 7. The sludge ocean plays a six-frame, 256×256 tile loop at 8 FPS beneath a transparent terrain overlay. Islands, shores, bridges, and the portal remain fixed; rain, clouds, boats, drones, and the shield keep their existing motion. **Water motion** has its own toggle, and the preview includes an animated tile sample.

The independent frames are `assets/v7/water_frame_00.png` through `water_frame_05.png`; `sludge_water_6f.png` is the horizontal spritesheet. `water_frame_contact.png` displays all frames, `water_tiling_review.png` checks repetition, and `terrain_overlay.png` preserves the map’s static terrain. `water_animation_v7.json` gives the frame order, rate, dimensions, and loop settings. The revision 6 preview remains in `preview_v6.html`.

Rebuild with `node expansion/tools/build_overdrive_coastline_v7.cjs` (Sharp required). `verification_v7.json` records six distinct frames, exact matching tile edges, consistent adjacent-frame changes including frame 6 to frame 1, unchanged terrain alpha, and complete asset references. These are map art and browser preview assets; the game engine has not yet loaded this animation.

## Revision 6: sludge water and rain

The preserved `preview_v6.html` loads revision 6 and opens on the portal bridge in a rainstorm. The sea texture and cyan shoreline water are palette-swapped to dark, low-saturation moss and toxic olive. The original ocean wave texture stays intact. Existing land, original campaign islands and the portal art retain their character; the prior blue-water map is preserved in `preview_v5.html`.

`assets/v6/sludge_ocean.png` is the independent palette-swapped water tile. `assets/v6/world_terrain.png` is the assembled sludge map without moving objects; `assets/v6/world_review.png` and `sludge_portal_review.png` show the full map and portal area with rain. `map_weather_v6.js` defines deterministic diagonal rain streaks, and `preview_v6.js` animates them over all map regions with a **Rain** toggle. The existing shield pulse remains independently controllable.

Rebuild with `node expansion/tools/build_overdrive_coastline_v6.cjs` (Sharp required). `verification_v6.json` records 6.24 million palette-swapped map pixels, unchanged terrain alpha, complete asset references and 1,250 rain drops. This remains map art and an animated preview; weather and polluted-water gameplay effects are not yet integrated into the game engine.

## Revision 5: shielded void portal bridge

The preserved `preview_v5.html` loads `manifest_v5.json`, `manifest_v5.js`, `map_motion_v3.js`, and `preview_v5.js`. It opens on **Void portal**, a new bridge between the northern city and the comet-struck island at the user-indicated water gap. The bridge carries a giant black-violet void portal at its midpoint. A separately exported cyan-violet shield layer pulses over the portal in the browser preview; the bridge source includes a static halo so it remains legible in still exports. The previous revision is preserved as `preview_v4.html`.

The independent masters are `source/portal_bridge_v5.png` and `source/portal_shield_v5.png`; exports are `assets/v5/portal_bridge.png` and `portal_shield.png`. `assets/v5/portal_bridge_review.png` shows the crossing in place, and `world_review.png` shows all regions. The road-and-portal sprite is placed at `[210, 390, 400, 500]`, with the shield overlay at `[375, 540, 100, 150]`. The cargo boat patrol and two ambient placements were moved clear of the portal to keep the crossing visible. The original city-to-Miami bridge and the separate collapsed comet-to-Miami crossing remain.

Rebuild with `node expansion/tools/build_overdrive_coastline_v5.cjs` (Sharp required). `verification_v5.json` records 360 orbit samples per boat and 17 conservative footprint points per sample against the full terrain alpha, including both added bridges; all routes pass. Sources, prompts and placement references are recorded in `prompts_v5.json` and `reference/`. This is map art and animated preview data; portal or shield gameplay behavior is not yet wired into the engine.

## Revision 4: collapsed island crossing

The preserved `preview_v4.html` loads `manifest_v4.json`, `manifest_v4.js`, `map_motion_v3.js`, and `preview_v4.js`. It opens on the **Collapsed crossing** focus between the comet-struck western island and green Miami coast. Revision 3 remains in `preview_v3.html`.

`source/collapsed_bridge_v4.png` is the transparent generated master. `assets/v4/collapsed_bridge.png` is the independently exported map sprite; `assets/v4/world_terrain.png` composes it at `[800, 1105, 560, 215]`. The surviving left approach has violet corruption, the right approach meets jungle, and the road is visibly impassable at its wide missing middle span. `assets/v4/collapsed_crossing_review.png` is a close map review; `assets/v4/world_review.png` shows the full map. The separate northern bridge to the city remains intact, and sections 1 and 2 retain their hovering icons and original flags.

The channel boat's short patrol was moved south of the new bridge. `verification_v4.json` records 360 full-orbit samples for each of the three boats, with 17 conservative footprint points per sample against all terrain alpha; no collisions remain. Rebuild with `node expansion/tools/build_overdrive_coastline_v4.cjs` (Sharp required). The prompt and style/placement references are recorded in `prompts_v4.json` and `reference/bridge_gap_review.png`. This is map art and preview data; bridge collision or pathfinding has not been wired into game runtime.

## Revision 3: comet-struck western island

The preserved `preview_v3.html` loads `manifest_v3.json`, `manifest_v3.js`, `map_motion_v3.js`, and `preview_v3.js`. It opens on the comet island beside Miami. **New expansion** frames the western regions; **Full connection** includes the original campaign islands. Revision 2 is preserved as `preview_v2.html`.

The giant dead coastal island occupies the open water in Mike's placement screenshot: **west of the green Miami coast, below the northwest bridge, and north of the southern islands**. A huge fractured alien comet is half buried in the crater, spreading violet-black growth through ruined settlements, dead palms, cracked roads and the shoreline. No new stage number or boss assignment is implied.

The new source masters are `source/comet_island_v3.png` and `source/comet_surrounds_v3.png`. The latter supplies three separate cloud overlays (storm, ash and spores), a comet-shard reef, a corrupted shipwreck and a dead palm islet. Selected exports are under `assets/v3/`; earlier sprites are reused from `assets/v2/`. Built-in **image_gen** prompts are in `prompts_v3.json` and `prompts_v3_spacing.json`. The original placement screenshot is preserved as `reference/comet_placement_request.png`.

- All **three boats** have moved to western-water patrols: north of the impact island, through the channel toward Miami, and through the southern open water.
- **Six drones** patrol the new expansion, covering the comet island, northwest city/bridge, Miami coast and southern archipelago.
- **Eleven cloud placements** combine the existing clouds with new storm, ash and spore layers. Their bounded drift stays independent of the land and leaves the central comet readable.
- The two floating level icons and original flag system are preserved. Other existing land pieces retain their previous coordinates.
- `assets/v3/world_review.png` is the complete map review; `western_expansion_review.png` is the new-side detail. `world_terrain.png` excludes moving clouds, boats, drones and level icons. Reefs and wreckage remain separate assets and are also included in that assembled terrain composite.

Rebuild with `node expansion/tools/build_overdrive_coastline_v3.cjs` (Sharp required). It uses revision 2's manifest and assets, adds ten PNG exports, and writes the combined 75-asset manifest. `verification_v3.json` records checks, including 360 samples around each full boat orbit against terrain alpha with a conservative boat footprint. All three routes pass without terrain intersections. The shared motion helper drives both static review placement and browser animation. This remains an asset/animated-map preview, with no game engine changes.

## Revision 2: separate icons and expanded world

The preserved `preview_v2.html` uses `manifest_v2.json`, `manifest_v2.js`, `preview_v2.js`, and the separate PNG assets in `assets/v2/`. The first composition remains available as `preview_v1.html` and the original assets below.

- Sections **1 and 2** each have an independent floating landmark sprite above the grass, with a ground shadow and gentle hover. The corresponding buildings have been removed from the underlying terrain. Their existing transparent 380×380 icons are reused.
- The original game's numbered flag art is reused, including available, highlighted, locked and completed states. Preview controls demonstrate both available, section 2 locked, and section 1 cleared. Highlighted flags animate. This preview does not change game saves or unlock progression.
- **Three cloud sprites, three boats, and three alien drones** are individually exported with alpha. Five placed clouds drift; three boats patrol water; three drones orbit the coast. Toggle motion, clouds, and boats/drones independently.
- **Four separate southern islands** surround a fifth island with a tall open grassy **central plateau**. Every island is its own PNG, with open ocean between placements.
- A **separate northwest causeway bridge** joins the coastal road to a **large city region**. These are geography pieces; no extra mission numbers or story claims have been assigned.
- `assets/v2/world_terrain.png` (3328×2304) contains terrain only. `world_review.png` adds a static illustration of the independently positioned objects and flags. `coast_detail_review.png` is a close view of the hovering icons. Runtime positions, sizes, orbit parameters and flag states are in `manifest_v2.json`.

Generated with built-in **image_gen**. The five new selected source masters are `coast_terrain_v2.png`, `southern_islands_v2.png`, `map_objects_v2.png`, `major_city_v2.png`, and `city_bridge_v2.png` under `source/`. Prompts are in `prompts_v2.json` and `prompts_v2_cleanup.json`. Raw generated PNGs can contain color in fully transparent pixels; alpha is preserved in the exports.

Rebuild this revision with `node expansion/tools/build_overdrive_coastline_v2.cjs` (Sharp required). It also reads the existing game atlas and manifest to extract the original flags. The builder produced 68 PNG exports: new terrain/object sprites, existing flag/cursor sprites, and review composites. `verification_v2.json` records dimension, transparency and file-reference checks. The browser preview is art presentation, not a playable campaign or a change to the game engine.

## First revision

Generated September 30, 2026. Five new image masters, nine packaged PNG exports, and a separate route overlay. This is an art package for review and later integration; the game does not load it yet.

Open `preview.html` for the interactive connecting map, both level icons, mission beats, draft radio dialogue and background plates. Drag the map, scroll to zoom, or select **Miami coast**. The HTML also works directly from disk.

## Deliverables

| Asset | Export | Use |
| --- | --- | --- |
| Connecting map | `assets/connecting_map_clean.png` — 2560×1280 | New coast far left, existing campaign island cluster right, long open-water gap. Existing island art and ocean are reused references. |
| Map with route | `assets/connecting_map_route.png` — 2560×1280 | Review composite with flight route and first two expansion nodes. Separate editable overlay: `assets/connecting_route.svg`. |
| Miami coast region | `assets/miami_coast_region.png` — 768×1024 RGBA | Independent land plate with compound, north gate, beaches, highway, palms, inland space and Miami district. |
| Level 1 compound icon | `assets/level_01_compound.png` — 380×380 RGBA | Matches the existing campaign icon canvas / 190 logical pixel display convention. Also supplied at 128×128. |
| Level 2 gate / highway icon | `assets/level_02_gate_highway.png` — 380×380 RGBA | Open military exit gate and road toward Miami. Also supplied at 128×128. |
| Flight arrival plate | `assets/level_01_ocean_approach.png` — 480×720 | Ocean-to-compound transition section. Full 1024×1536 source retained. |
| Tank departure plate | `assets/level_02_coastal_highway.png` — 480×720 | North gate, coast road, sand, palms, ocean and Miami architecture. Full 1024×1536 source retained. |

## Story continuity

Hotwire and Phoenix are independent fighters caught in the conflict. Their abandoned military compound is a refuge with working repair bays, not a rogue or rebel stronghold.

Level 1 flies across the water into an ambush by symbiotic alien ships. The symbiote has spread globally. The two allies greet the player and open the approach. A hostile shot downs the player's ship into the base immediately before entry. They rescue the pilot, attempt repairs on the ship, and bring a tank online.

Level 2 begins at the outbound gate. The player drives up the coast, fights both air and ground units, and proceeds inland toward Miami.

`story.json` preserves these beats, with working mission names and draft dialogue. The later tank explosion, on-foot base infiltration and jet recovery remain a separate mission sequence.

## Production boundaries

- No playable level, enemies, collision map, progression unlock or engine code was added. The old-campaign route endpoint is a proposed placement, not a chosen stage unlock.
- Background plates are finite illustrative transition sections, not seamless scrolling tiles. Their buildings retain some elevated architectural perspective. The arrival includes a decorative tank in a side bay and fixed defense guns; treat these as scenery pending production separation.
- The highway carriageway is narrow in the source. A playable bullet-dodging layout needs wider road/shoulder modules and authored collision bounds. Do not equate the image edges with gameplay collision.
- No UI, labels, markers or dotted route are baked into the standalone generated art. The review map adds its route as a separate SVG overlay. The overview geography is fictionalized for the game.
- The map source places a few parked aircraft at the compound. They are environmental aircraft, not a claim that the player's damaged ship is already repaired.
- Existing reference art was copied from `assets/game/campaign_map_v2/` in the BulletsOfFury checkout. The composite preserves the current game's island positions and relative sizes. It does not use the obsolete atlas map renderer.

## Files and rebuild

`source/` holds untouched generated masters. `prompts.json` records the coast/icon prompts and `background_prompts.json` the two backdrop prompts, all generated with built-in image_gen. Reference PNGs are in `reference/`. `manifest.json` records dimensions, transparency, hashes and review map coordinates. `verification.json` records export checks.

Rebuild the exports from the workspace root with Node and Sharp available:

```powershell
node expansion/tools/build_overdrive_coastline.cjs
```

The builder only normalizes/copies/composes the authored art; it does not replace it with procedural scenery. All nine PNG exports passed dimension, transparency and referenced-file checks. The original game checkout is unchanged.
