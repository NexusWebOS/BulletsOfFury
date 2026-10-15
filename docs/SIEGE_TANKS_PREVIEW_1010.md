# Modular siege tank candidates — October 10

Preview: `docs/previews/siege_tanks_1010/index.html`.

Three new Dune-inspired tanks and their effects were generated with the built-in
`image_gen.imagegen` tool. The initial delivery was **preview-only**. Mike then
approved playable Level 1 miniboss passwords: `sonic`, `ordos` and `hark`.
See [the playable encounter report](SIEGE_TANKS_PLAYABLE_1010.md) for that
integration. This page remains an isolated art-review tool. No new commit or
push was requested for either local pass.

## Designs and scale

| Candidate | Preview assembly width | Visual identity and attack demonstration |
| --- | ---: | --- |
| Sonic siege tank | 240 game pixels | Platinum/graphite, cyan tuning-fork emitter, pressure packets and charged concussive bloom |
| Devastator assault tank | 154.5 game pixels | Graphite/crimson, alternating twin heavy plasma cannons and auxiliary pods |
| Deviator missile tank | 200 game pixels | Bronze/graphite, six staggered emerald missiles, violet interference energy and sensor dish |

The current regular heavy tank has a configured 103-pixel size; the Furious
Razorback has a configured 186-pixel size. Devastator uses 1.5 × the regular
heavy tank's configured size. The comparison view renders those original units
through the game's own drawing functions beside the new assembly.

Sonic's maximum authored pressure-bloom footprint covers approximately 33% of
the active playfield. The preview sizes it from occupied raster pixels and
keeps the whole bloom inside the field, with a separate contact burst.
This demonstrates graphics and timing, not approved encounter balance.

## Delivered art

The candidate manifest owns **58 banks and 553 normalized cells**:

- Three 16-frame bare-hull reels.
- Six 16-frame independently animated track reels.
- Three 16-frame main weapon charge/release/recovery reels.
- Nine separate auxiliary pod, reactor and targeting-array plates.
- Twenty-one four-state module banks: light damage, critical damage, burning
  wreck and authored white plate.
- Twelve loose armor/debris pieces.
- Three 16-frame charge effects, three 16-frame projectiles, three 16-frame
  impact/muzzle effects and three 32-frame explosion/shock-ring sequences.
- Sixteen persistent pressure scars, plasma craters, missile/interference
  craters and tread/breach decals.

Each assembly has eight independently rendered modules: hull, left track,
right track, main weapon, left auxiliary pod, right auxiliary pod, reactor and
targeting array. The two pods use the same authored part. The preview can hit
or destroy each module separately. Detached burning modules spin physically
into explosions, while delayed pieces remain at their mounts until detachment.
No opacity fade removes a module. In-motion white hits use the native `xartTint`
mask of the currently visible frame so the silhouette never changes on a hit;
the separately generated white plates are available in the damage gallery.

## Sources and ownership

- `_ART_SOURCES/siege_tanks_1010/returned/`: 31 unmodified generated returns,
  including retained unused/rejected layouts.
- `_ART_SOURCES/siege_tanks_1010/reference/`: authored reference components
  and a native current-tank export.
- `_ART_SOURCES/siege_tanks_1010/normalized/`: registered game-scale PNG cells.
- `_ART_SOURCES/siege_tanks_1010/manifest.json`: complete cell keys, frame
  rectangles, fixed pivots, common scales, translations and file hashes.
- `_ART_SOURCES/siege_tanks_1010/provenance.json`: source and output SHA-256
  hashes, tool and normalization policy.
- The `*-prompts.json` files, `prompts.json` and `decal-prompt.txt` in that source
  directory contain the exact built-in generation prompts. Targeted repairs
  are recorded in `repair-addendum-prompts.json`.
- `_BUILD_SOURCE/build_siege_tanks_1010.py` owns normalization and the isolated
  `art.js` registry. Its explicit `--deploy` option now copies the approved
  cells into the owned production folder and generates the shipping registry.
  It does not modify an atlas.

Normalization only cuts authored pixels, removes alpha below 64, translates
against stationary fixtures, and applies one common scale and transparent
canvas crop per bank. No frames are duplicated to fill a count. Missing or
incorrectly mirrored Sonic tracks were regenerated. Unequal sheet spacing is
cut around whole components. Deviator guard/gimbal registration uses measured
native bronze fixtures, not the moving gray tread links; those translations
are recorded in `registration-corrections.json`.

The [standing frame resolution rules](FRAME_RESOLUTION_RULES.md) now apply to
this kit. Every exported PNG has an even width and height, with identical
canvas dimensions, pivot and proportional scale throughout its bank. Odd
shared crops receive transparent padding on the right or bottom. The existing
artwork pixels, anchors and scales are preserved. `framePolicy` in the manifest
and provenance records the enforced export contract.

## Review and verification

The page runs an isolated instance of the real game renderer. Tabs choose each
tank. Controls demonstrate attacks, pause/speed, white hits, independent damage,
module breakup and rebuild. Additional views show native size comparisons,
animated effects and damage/debris/crater plates.

`_BUILD_SOURCE/probe_siege_tanks_1010.py` verifies frame counts and unique
native renders, fixed fixtures, assembled dimensions, intact white-hit
silhouettes, southbound projectiles, independent physical breakup, persistent
decals, visible sonic footprint, production ownership, and page/console/asset
errors. Its final report is `_shots/siege_tanks_1010/verification.json`.

`_BUILD_SOURCE/record_siege_tanks_1010.py` exercises the actual page controls and
records an 18-second native demonstration of all three tanks, including
attacks and staggered module destruction. Its video and separate control
report stay under ignored `_shots/siege_tanks_1010/`.

The initial art review was approved. Encounter HP, collision targets,
damage, attack scheduling, difficulty scaling and audio are now wired through
the separately owned playable runtime.

Initial preview verification: **96 native renderer checks and 13 control/video checks
passed**, with no page, console or asset errors. The measured visible sonic
footprint was **32.9975%** of the active playfield. JavaScript syntax checks
passed, and the complete existing game assertion suite reached its final
summary: **7,952 passing checks, 0 errors, exit 0**.

The even-resolution rebuild padded 419 cells across 41 banks. All 553 files
have even dimensions; byte comparisons of the original raster regions confirm
that artwork pixels, registered bounds, pivots and scales were preserved.
