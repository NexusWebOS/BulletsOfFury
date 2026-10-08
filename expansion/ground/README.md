# Bullets of Fury — Overdrive ground art, pass 1

This package contains authored candidate art for the ground expansion. Open `preview.html` through a local web server to inspect the three tank families, all eleven pilot palettes, four infantry bodies, ammunition/crates, and animated effects. The game runtime, campaign map, and levels are not modified.

## Contents

| Folder/file | Contents |
| --- | --- |
| `source/` | Untouched built-in imagegen source sheets, including the superseded first G.O.D Burst draft |
| `tanks/` | 27 normalized PNGs: eight source parts/states plus an assembly made from the actual hull and turret for each family |
| `infantry/` | 112 PNGs: 28 poses/frames for each of four shared bodies |
| `pickups/` | 18 ground crates, ammunition, weapons and power-up sprites |
| `fx/` | 42 projectile, muzzle, impact, destruction, and atomic/magnetic sprites |
| `manifest.json` | Source rectangles, fixed canvases, pivots, scales, SHA-256 prefixes, pilot assignments, and sequences |
| `manifest.js` | The same data for the local review page |
| `design.json` | User requirements and proposed future engine contracts, explicitly separated from implementation |
| `prompts.json` | Full prompts used with the built-in image generator |
| `previews/` | Transparency and assembly review images |

All **199 normalized PNGs** are derivatives of generated raster art. Extraction resamples with nearest-neighbor and preserves transparency. No procedural substitute sprites were drawn. The original masters remain untouched. SpriteCook was only queried during discovery; this art was generated with built-in imagegen.

## Tank families

| Family | Pilots | Direction |
| --- | --- | --- |
| Heavy siege | Juggernaut, Phoenix | Broad low hull, twin cannons, thick segmented treads; Harkonnen Devastator influence |
| Assault | Axel, Cole, Decker, Freezer, Maverick, Yuri | Compact arcade main battle tank and single main cannon; BattleTanx influence |
| Panzer | Falva, Lizzie, Hotwire | Long angular hull, slab skirts, precision cannon |

The tank layer canvases are 192×192 with a common `(96,120)` turret/hull socket and a north-facing source orientation. The normalized hull footprints are approximately 104 pixels wide for siege, 92 for assault, and 72 for Panzer. Muzzle positions in the manifest are candidate sockets for later calibration. Rotate the hull and turret separately around that socket. In the review page, fire shifts the original turret back slightly and attaches a shared flash.

Each family includes assembled concept art, a turretless hull, a detached turret, damaged hull, wreck, individual left/right track source modules, and a recoil candidate. The displayed assembled result uses the separately extracted hull and turret, not the original assembled concept. **The hull already includes its tracks.** The isolated track sources are available for future damage/animation work, but do not yet form an exact three-piece chassis assembly. Treads are not animated.

The generated recoil candidates shorten barrels inconsistently and should not ship as animation. Retain them as source candidates; translate the normal turret for recoil until exact geometry is repaired. Final gameplay hitboxes, collision footprints, direction-dependent lighting, and sockets must be tested when integrating the vehicle controller.

## Pilot palettes

The nine existing primary colors and brightness factors come from the current `assets/game/furyship_0914/pack.json`. Hotwire's cyan and Phoenix's dark ember paint are candidates based on the existing expansion art; copper/gold mechanical trim remains authored. The preview changes only cobalt-blue paint/suit regions, retaining neutral steel, dark outlines, amber lamps, and weapon effect colors. Palette variants are produced by the review renderer, not eleven independently generated vehicles or bodies.

## Infantry

| Body | Pilots |
| --- | --- |
| Heavy | Juggernaut |
| Athletic male | Axel, Phoenix |
| Female | Falva, Lizzie, Hotwire |
| Regular male | Cole, Decker, Freezer, Maverick, Yuri |

All wear opaque helmets and covered suits. The 96×96 canvases use a `(48,48)` pivot and fixed scale per archetype. Bodies are intentionally smaller than the tanks. Each base provides four directional aim poses; four-frame north, east, and south runs; a four-frame east shoulder roll; four directional prone poses; and four death frames. West run/roll mirror east. Aim and prone rows are directional poses, **not** looping four-frame animations. Separate muzzle flashes supply the current aim/fire stance.

These are first-pass motion candidates. Source poses have anatomy/heading drift and require final temporal cleanup. North/south rolls, prone crawl and prone transitions, separate weapon overlays, reload/use/enter/exit actions, eight-direction aim if desired, and collision/weapon sockets remain future production work. Playback loops death and roll for inspection only; the game should play those once. No hurt/health system is implied: the requested on-foot damage model is one hit kills the player.

## Crates, ammo and effects

Weapon crates and ammo crates each have closed, open, and broken forms. Pickups include rifle ammo, shells, rockets, energy batteries, tank shells, grenades, three weapon sprites, and speed/sensor/magnetic power-ups. Their final gameplay behavior and ammunition quantities are not assigned. No healing pickup was added.

Shared effects include six projectiles/tracers, six muzzle frames, six impact frames and six tank-destruction frames. Effect canvases preserve a common anchor within each animation, rather than independently centering each visible shape. Sequence timing is an initial review suggestion.

G.O.D Burst means **Godly Over-Powered Destruction**, obtained from expansion level 5's boss. Its sheet contains six charge frames, six burst frames, atomic bolts, a split bolt, hit spark, magnetic ring, atom-wave crescent and core icon. Cyan/violet rings and white splitting nuclei distinguish it from conventional explosions. The first draft overlapped frames and is retained as `god_burst_sheet_v1.png`; extraction uses the cleaner `god_burst_sheet.png`.

## Expansion requirements retained

Eight new main levels plus a bonus level; two or three ground levels depending on route. In the showcase ground mission, the tank is destroyed, the helmeted pilot proceeds on foot through robotic alien opposition, breaks into the base, and recovers their jet. Crates supply weapons and finite ammo. Stealth-inspired detection and cover coexist with run-and-gun waves. Enemy HP can exceed one hit. No ground level, drone roster, boss encounter, AI, ammo system or vehicle/player controller was implemented by this art pass.

The design record proposes separate hull/aim headings, vehicle-to-infantry-to-jet transitions, noise and visibility detection, collision footprints independent of sprite bounds, and explicit prone/roll collision rules. These are implementation requirements, not claims of engine features already added.

## Rebuild and review

The extraction script is `../tools/build_overdrive_ground.cjs`. It requires Node.js and `sharp`; the Codex bundled Node dependencies include `sharp`. Set `NODE_PATH` to that package directory or use an environment where `sharp` is installed, then run the script from any directory. `inspect_ground_sheets.cjs` reports actual row and column content bounds for infantry sources; generated sheets do not have perfectly uniform cells.

Serve this directory locally, for example `python -m http.server 8769 --bind 127.0.0.1`, then open `http://127.0.0.1:8769/preview.html`. Serving is needed for canvas palette inspection. The preview loads only local files and makes no external requests.

## References

- [Dune 2000 original manual, Devastator entry](https://www.bestoldgames.net/download/games/dune-2000/dune-2000-win-manual.pdf): heavy Harkonnen tank role and visual reference.
- [BattleTanx: Global Assault manual](https://www.videogamemanual.com/ps1/BattleTanx%20-%20Global%20Assault%20%28USA%29.pdf): arcade M1A1 and heavy-tank reference.

The new art is original and uses the existing Overdrive ship/pilot designs as material and style references.
