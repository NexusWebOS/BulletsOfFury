# October 9 — Hammer farewell and enemy/ship motion

Mike requested sequential electrical explosions, Hammer's final dialogue and
reactor-finishing missile, smoother enemies across Stages 2–8, better small
volcanic/arctic designs, correct incoming Stage 6 aircraft facing, and the start
of smoother framing for the current nine pilot ships and spaceship. He also
authorized publishing the completed game changes and their source art to GitHub.

## Shipped behavior

Hammer says **“This cannot be..”** and **“You were a worthy opponent, mortal.”**
The existing large dialogue box types those lines, holds each for two seconds,
whitens his authored portrait over 1.1 seconds, then fades the window out.
The original pilot Retina locks onto the measured chest reactor, and the current
Furyship fires an authored missile into it. Only its impact starts the existing
eight-second whole-body death. Nine electrical eruptions appear one after another,
with new expanding, cracking and scattering electric rings. His existing acted
two-arm/head reel, major explosions, cutaways, monochrome aftermath and Earth
return remain in that order. The prelude takes approximately 9.1 seconds.

Thirteen built-in imagegen RGBA sheets provide **208 normalized loose cells**:
112 enemy cells, 72 pilot cells, eight Furyship cells, eight Furyship palette
masks and eight electrical ring cells. New actors retain their encounter HP,
hitboxes, patterns, emitters and original warning/sound systems. Existing wear
effects and white hit flashes are preserved. The desert tank retains its original,
independently aimed turret over an animated hull.

The 24 current roster slots receiving new eight-frame loops are:

| Stage | Current slots | Motion/art |
| --- | --- | --- |
| 2 | `disc`, `eye`, `skim` | New radial heat drone and furnace sentry; current thermal jet |
| 3 | `s3mine`, `s3interceptor` | New shard sentry and ice patrol interceptor |
| 4 | `s4tractor`, `s4airfield`, `s4minitank` | Current tractor and modular tank hull; the last two spawn the existing `sandtank` |
| 5 | `s5frigate`, `s5rammer` | Current orbital frigate and rammer |
| 6 | `s6lancer`, `s6cyclone`, `s6skimmer`, `s6dart`, `s6thunder` | Their existing shared storm-jet chassis with rear exhaust above the south-facing nose |
| 7 | `s7pipe`, `s7walker` | Current pipe unit and toxic walker |
| 8 | `s8interceptor`, `s8parasite`, `s8skull`, `s8symbiote`, `s8spread`, `s8crescent`, `s8hunter` | Current shared alien fighter and separate stalker |

Incoming Stage 6 storm fighters ignore transient spin when drawing their
south-facing flight plate. Stealth/bomber direction comes from its actual flight
state. The original three-cell blue sheet uses its south cell rotated for a true
northbound unarmed gate, fixing the previous `3 % 3` selection of an east-facing
cell. The existing authored red/green/orange bomber palettes remain authoritative.

Axel, Cole, Decker, Falva, Freezer, Juggernaut, Lizzie, Maverick and Yuri each get
eight neutral-flight frames. Registration uses their original native canvas bounds
and existing nozzle/muzzle rigs. The Furyship gets eight neutral-flight frames and
the original nine pilot hull palettes; chrome, cyan windows, engine glow and
ordnance stay their authored colors. Original bank/roll poses still own those
actions. This is the requested beginning of smooth-framing those ships.

## Art ownership and rebuilding

- Runtime: `assets/smooth_motion_1009.js`, loaded after the current boss and Stage 1 motion owners.
- Builder: `_BUILD_SOURCE/build_smooth_motion_1009.py`.
- Registry: `assets/smooth_motion_art_1009.js`, written with its cells by that builder.
- Art: `assets/game/shared/combat/smooth_motion_1009/`.
- References, exact prompts, returned source sheets, crop/registration manifest and SHA256 provenance: `_ART_SOURCES/smooth_motion_1009/`.
- Taxonomy prefix: `sm10_` in `assets/data/ART_TAXONOMY.json`.

Rebuild with `python _BUILD_SOURCE/build_smooth_motion_1009.py`. It slices the
authored art, clears stray alpha below 64, registers fixed chassis by translation,
and applies a common scale to each reel. It does not paint procedural sprites or
fit every frame independently. The electrical reel has measured unequal cell
widths; expansion is preserved around measured common centers. Native ship sizes
are preserved. No shared atlas changes or repacks are involved.

The reference exporters are deliberately guarded against replacing the approved
source baseline. `--refresh-reference` is for an intentional later art pass;
normal rebuilding only reads those original references.

## Verification

Real Chromium ran the shipped `index.html`, lazy assets and the game's own
`drawImage`/update paths. Recorded farewell and Stage 6 flight clips and native
contact sheets were inspected under `_shots/smooth_motion_1009/`.

| Check | Result |
| --- | --- |
| `node --check assets/game.js` and both new runtime/registry scripts | Pass |
| `node _BUILD_SOURCE/test_fl.js` | 7,952 passes, zero failures, exit 0 and final success banner |
| `_BUILD_SOURCE/probe_smooth_motion_1009.py` | 16 passes, zero failures/errors |
| `_BUILD_SOURCE/probe_enemy_ship_motion_1009.py` | 71 passes, zero failures/errors |
| `_BUILD_SOURCE/probe_boss_motion_1009.py` | 18 passes, zero failures/errors |

Checks cover actual portrait whitening, prelude/death order, one reactor impact,
nine timed electrical pops, eight distinct rendered frames, unchanged enemy
HP/hitboxes, actual white hit pixels, independent tank aim, ship canvas/nozzle
rigs, distinct Furyship palettes, stale-spin facing and existing filmed boss
attack/head/claw regressions. The base suite reached its final summary; the
September takeover failure counts are historical and do not apply to this run.

Fixtures protect the player and select encounters; they prove rendering and
integration, not a complete campaign victory or final difficulty balance.
Stage 6's clip is a controlled flight fixture. Portable results are in
`docs/qa/smooth_motion_1009.json`; ignored recordings are local review artifacts.

## Further motion work

This pass covers the slots listed above, not every unique enemy in the 80-slot
reference export. Existing independent mutant parts, other enemy reels and
authored bank/roll actions remain with their owners. A later motion pass can add
those remaining distinct chassis and bank/roll in-betweens while keeping their
targetable weapons independent. Do not replace all of them with a shared plate
or describe the current neutral loops as a full bank/roll replacement.
