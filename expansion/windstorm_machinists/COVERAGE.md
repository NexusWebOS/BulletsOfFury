# Expansion graphics coverage

Updated 7 October 2026. This index distinguishes delivered graphics and design notes from engine implementation. The current request continues the art package; none of these additions register gameplay systems.

| Request | Saved graphics / review | Coverage |
| --- | --- | --- |
| Niel / Windstorm | `identity/`, `ship/`, `fx/windstorm_*`; [current preview](preview.html) | Approved portrait design, expressions, front/full-body poses, ship variants, special icon/box, tornado volleys, charge and impact phases |
| Wren, Rolf, Chaz / The Machinists | `identity/`; [crew redesign](previews/machinists_v2.png) | Selected grounded v2 identities; canonical portrait frames, hex badges and vented ability boxes added; anime-influenced draft archived |
| Each Machinist's modular tank | `tanks/`, `tanks/layers/`, `fx/`; current preview | Separate hull, turret, tracks, rear module, damaged state, wreck; primary and special FX; six independent motion phases per left/right track |
| Phoenix and Hotwire ally modes | `allies/`; [new action contact sheet](previews/ally_completion.png) | Runs, stance candidates, wall/door interaction, cover, crawl, east/north/south fire, heal/signals, grenade throw, roll-to-prone/stand, duck-to-prone, hit/stun, recovery, death, revive, powerup and assist-heal; four-direction crouch/prone-fire and west runs |
| Four shared helmeted player bodies and palette swaps | `players/`, [ground package](../ground/preview.html), [on-foot package](../onfoot/preview.html) | Heavy, athletic, regular and female families; all requested action categories represented across the three manifests; four-direction crouch/prone-fire and west runs added |
| Stealth actions and objects | `players/`, `allies/`, `props/`; [notes](DESIGN_NOTES.md) | Wall taps, door operation, wall lean, crate peek, noise toss, sound rings, medkits; cover, hearing and ally coordination contracts |
| On-foot HUD and Miami infiltration stage | [on-foot preview](../onfoot/preview.html) | HUD overlay and slots; beach → palm park/pools → brick fortress gate background concept |
| Six handheld weapons, ammo, breakable boxes | `../onfoot/weapons/`, `../onfoot/fx/`, `../onfoot/props/` | Desert Eagle, Spread Shotgun, Minigun, Fusion Beam, Napalm Launcher, Rocket Launcher; closed/cracked/open crates, ammo, grenade and weapon effects |
| Alien ground enemies, turrets, tanks and air units | `../onfoot/enemies/`, `../onfoot/stealth/` | Enemy state candidates, FOV phases, awareness and targeting cues; scout/heavy four-direction patrol, east fire and hit/death strips now in `enemies/` |
| Original three tank families and G.O.D Burst | [ground preview](../ground/preview.html) | Siege, assault and panzer components, palette candidates, projectiles/explosions, atom/magnetic charge and burst effects |
| Connecting coast map, separate floating icons and flags | [coastline preview](../coastline/preview.html) | Sections 1–5, compound, coastal highway, bridge to Miami, downtown and plateau; clouds, boats, drones, southern islands |
| Comet-decayed island, collapsed bridge and shielded portal bridge | `../coastline/assets/v3/`, `v4/`, `v5/` | Individual terrain/bridge/portal/shield objects and assembled map reviews |
| Sludge water, rain, six-frame water animation | `../coastline/assets/v6/`, `v7/` | Six tile phases and weather preview; prior blue-water art preserved |
| Plateau destruction and fortress rise to sky map | `../coastline/assets/v8/`, `story_v8.json` | Intact/destroyed plateau, fortress and above-cloud map transition art |

## Earlier completion pass in this chat

Six new generated masters add 120 dedicated ally frames and 36 track frames. A further 36 calibrated transparent track layers fit the existing tank assembly pivots: **192 additional PNG exports**, bringing this package to **510 indexed PNGs and 102 sequence definitions**. The two superseded north-run drafts remain marked and hidden from normal action selection.

The review now includes earlier shared-body aim/run actions as well as the previous on-foot actions. Track playback supports forward, reverse and opposite-direction pivot previews. These are art playback controls, not vehicle simulation.

## Directional/enemy/UI continuation

Twelve further masters add 414 indexed frame IDs, bringing this package to **924 indexed PNGs, 168 sequences and 39 preserved masters**. Four-direction crouch/prone-fire covers all six player/ally bodies; west runs and two alien biped patrol/combat sets are included. Machinist portraits, hex icons and vented ability boxes now match the current game UI family. See [PASS_2.md](PASS_2.md) for exact selected phases, export contracts and limitations.

## Work reserved for engine integration / final art cleanup

- Generated motion is candidate art: stabilize body roots, gun grips, muzzle/hand sockets, track housings, loop seams, and missing directional coverage before registration. Directional firing uses a fixed cell anchor so muzzle-flash size does not recenter the body.
- West runs and crouch/prone-fire are now drawn directly. West-facing cover, door and other interaction art is still incomplete; mirroring would reverse handedness and asymmetric insignia. South/north interactions are not complete in every action family. These sheets are not an eight-direction production animation set.
- The stage remains a background concept. Tile construction, collision, occlusion, cover anchors, AI navigation, enemy AI, remaining vehicle/air-unit motion, ammo, pickups, HUD binding, revive/heal rules, and campaign progression still need implementation.
- The campaign expansion is planned for eight levels plus a bonus. The user has defined numbered locations 1–5 and the sky transition. Later stage layouts and bonus content remain undesigned; this pass does not invent their final missions.

Generation: built-in **image_gen**. [Initial prompt/provenance record](generation.json) and [six completion prompts](completion-generation.json). [Directional/enemy/UI prompts](passes-2-generation.json). Source masters remain intact in `source/`. Export checks are in [verification.json](verification.json).

The selected [Machinist appearance revision](ROSTER_V4.md) gives Rolf blue hair/blue clothing, Wren black/white armor, and blond Chaz a red outfit and forehead bandana. Selected portraits, avatars and full-body poses use versioned v4 exports.
