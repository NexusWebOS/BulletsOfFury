# Base33 — Dead Signal slide and side-scroller base

Build: `overdrive1015-base33-r1`. Local expansion update; no commit or push.

## Delivered

72 separate PNG assets generated with the built-in image generation tool:

- 4 front-elevation wall panels and 8 independent floor, ceiling, chute and service strips.
- 16 props: cargo, stacked cargo, armored cover and wreck, barrel, pillar, slide pipe,
  crawl canopy, closed/open doors, three vent states, ceiling drone hatch, siren and ammo locker.
- 4 background cover recesses with 8 separate foreground pier layers.
- 16 arcade signs/icons and 4 effects with 4 frames each: metal impact, vent rupture, steam, blast.

Source sheets and prompts: `expansion/topdown/art/base33/source/`.
Individual exports: `expansion/topdown/art/base33/frames/`.
Manifest: `expansion/topdown/art/base33/manifest.json`.
Owner: `expansion/topdown/_research/build_base33.py`.
Eight generated source images retained; the first softer pipe/canopy drawings remain
in the original props source sheet. The sharper replacements are `pipe_v2` and `duct_v2`.
All delivered canvases have even dimensions. Crops use measured source boundaries,
proportional nearest-neighbor scales and transparent padding. No independent axis stretching.
Effects share fixed 96×96 canvases and a stable anchor within each bank.

## Live route

Gosfer → existing elevator/hatch → 45° drone slide → service corridor →
self-destruct barrel/door escape → Prism Bastion, displayed as level 4.

The chute uses separate moving diagonal track, rear wall, overhead strip and drone hatches.
The corridor uses modular wall/floor/ceiling pieces with depth-separated recesses, cover,
low passages, a floor vent cache, red alarms and the final barrel door.
Foreground objects retain visible damage flashes. Existing Yuri30/31/32 and enemy art is reused.

The runtime is `js/base33.js` with scoped hooks in `js/escape29.js`.
The pre-pass Escape29 file is retained in `source/escape29_before.js`.
`assets/game.js` is untouched. Existing original art is preserved.

## Controls and interactions

- Hold cover while stationary inside a wall recess to tuck behind its actual foreground pier.
  Fire to lean out through the existing Yuri32 animation; release to return. Exposed Yuri is
  still vulnerable to one hit. Protection comes from the cover state and physical bullet block.
- Down + Roll performs the existing flat slide. The five-second roll cooldown remains.
- The M30 Mode + X chord toggles prone. Walk upright into a low passage and it blocks you;
  slide or crawl through. Yuri cannot stand up inside the canopy and can stand once clear.
- Shoot the vent grille three times with the assault rifle. The damaged and open artwork follows
  actual HP. Crawl into the open cache for 36 spread-shotgun rounds, two grenades and 2,000 points,
  once per corridor attempt. Existing weapon/Retina controls are unchanged.
- The final barrels blow the exit open; slide through to continue into Prism Bastion.

## Preview

`http://127.0.0.1:8781/expansion/topdown/art/base33/preview.html`

Six explicitly labeled section starting points use the real game renderer and controls.
They are preview shortcuts, not changes to normal campaign progression. Play/pause and restart
are available. The gallery shows the separate PNGs and four animated effect banks.

## Verification

Native Chromium, actual ART/AssaultArt draws and simulated raw 8BitDo M30 input:
22 focused art, cover, passage, vent and projectile checks pass; 14 preview/gallery checks pass.
Rendered chute, wall tuck/pop-out, slide/crawl and vent cache views were inspected.
The baseline of 820 original artwork hashes is unchanged.
Required `node --check assets/game.js` and full `_BUILD_SOURCE/test_fl.js` pass;
the final suite summary is **BUILD OK, 0 ERRORS**, exit 0.

The continuous ordinary-input corridor/self-destruct run reaches internal mission 7 (visible level 4) with zero deaths; all four route/cover checks pass.
Continuous route results are stored separately in `docs/qa/overdrive_base33_route_1015.json`.
The route probe uses only ordinary input after setting its corridor starting point.
The physical controller was not available for a hands-on test.
