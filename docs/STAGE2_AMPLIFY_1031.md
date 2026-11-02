# Stage2 volcanic enemy refit â€” October31

Current gameplay owner: `assets/stage2_amplify_1031.js`. Registered art:
`assets/stage2_amplify_art_1031.js`. Rebuild through
`_BUILD_SOURCE/build_stage2_amplify_1031.py`; `--basalt-only` rebuilds the steel
palette without re-encoding unrelated banks. No production atlas was repacked.

## Current lineup

| Enemy | Current behavior |
| --- | --- |
| Ash Fighter | Existing approved Magma Dart identity, animated flame thrusters, aimed fire bullets, tightening flown spiral, committed kamikaze and finite exit. |
| Lava Skimmer | New larger twin-boom fighter; banking curved passes and paired forward fire guns. |
| Cinderwasp | New distinct four-wing amber/black craft; curved stinging gun sorties. |
| Thunderlance | New large black/red/cobalt jet, matched fire-electric slugs and physical missiles. Retina/beep lock precedes missile releases. Both lance and reinforced firejet1002 retain their original native HP. |
| Fire Interceptor | New large red jet with exactly four visible gun mounts, two forward and two outer. Each emits a fire slug and attached flash. |
| Basalt Bomber | Gray/black steel palette variant of the approved Forge banks. Original fire cores, highlights, seams and source luminance retained; visible shootable magma arcs and committed ground Retinas. |
| Crucible Gunship | New black twin-fire-core medium gunship; large paired magma orbs, curved repositioning and a native one-way damageable fire shield. Shield energy must be exhausted before hull damage. |
| Magma Minelayer | Distinct magazine-and-booster hull, animated pulsing air mines, then boost escape.80% select the short two-second laying window;20% linger five seconds. This is an escape bias, not a forced immunity or guaranteed survival rate. |
| Lava Mechanical Serpent | Replaces crawl. Lower-edge eruption, three snaking jumps across the field, committed south bite warning, rapid open-jaw lunge and edge recovery. Actual mouth contact owns the bite. |
| Lavamaw | New mechanically braced mini volcano. Orbs leave its top crater and arc onto a circular set of ground Retinas; higher difficulty shortens tell, impact flight and recovery. |
| Magma Pod | Distinct six-petal mechanical eruption pod; visible opening, eight-position eruption and closing recovery. |
| Magma Carrier | New large volcanic Harrier hangar. Side arrival, sliding door opening, four staggered elite deployments, closing and retreat. |
| Furnace Wing | New carrier-jet family with four native roles: twin flamethrowers, paired magma fireballs, twin turbo fire guns and moving fire walls. Each has its own published preview and catalogue row. |
| Magma Disc | New source-derived nine-spike disc.32 registered spin poses and nine actual tip sockets. Commits nine authored green/yellow/red FOV lanes, releases nine red/white fire lasers simultaneously, then recovers. Beam directions use288 exported orientations aligned with the disc's9Ã—32 geometry. |
| Ground weapons | Stage2 full visible turret footprint is checked against the authored ground mask. Prefer a small right shift for the laser; search an upstream clear row if needed. Unplaceable fixtures do not appear in mountains. Twin missiles use Retina locks; laser bursts rotate on Hard/Furious and fire progressively faster. |

Magma Eye/eye and the Magma Orb enemy/magmaorb are removed from active wave and
drone selection, rejected through legacy spawn routes, and removed from both
current catalogues. Existing historical source files and archived films remain.
Magma orb **ammunition** remains, including its native offensive interception.

## Artwork and ownership

- 14 model registries,85 fixed banks,8240 exported cells. Runtime cells are even
  64/128/160/192/256 dimensions with shared padding, proportional scale and stable
  pivots. Generated whole sheets are normalized by connected hulls so loose source
  grids cannot cut off wings or include neighboring frames.
- New hulls and effect kit were generated with built-in `image_gen`. Original
  images and the prompt set are retained under `_BUILD_SOURCE/stage2_amplify_1031`.
  Current approved BF22 Ash and Forge banks supply the two source variants.
- Aircraft have idle, attack, drift, roll, somersault, charge and heading banks.
  Authored cardinal views and baked intermediate headings replace live sprite
  rotation. The V31 hull, projectile, muzzle and thruster renderer has no
  `ctx.rotate`, CSS transform, blur or opacity-based hull transition.
- Source pixels supply the disc's central body and exactly nine assembled blade
  modules. This corrects the image generator's seven-spike source. No placeholder
  hull or drawn geometric weapon substitutes are active.
- Native difficulty/thermal HP is applied once before the refit. Native damage,
  first-impact pool protection, shield deploy/break/stun/frenzy, hit flashes,
  destruction, rewards, locks and defensive clears retain their owners.
- Ordinary fire slugs and fire walls reject offensive interception immediately.
  Physical missiles, air mines and magma orbs retain native interception. Arcing
  magma uses real native eBullets; destroying one also cancels its landing Retina.
- Native cues use the shared mixer: machine-gun heavy, magmaOrb/bombDrop,
  enemyHeavyLaser, flameThrowerStart/enemyFlameBolt, jetDash and lock beeps.
  Launcher destruction clears pending heavy attacks, live beams and muzzle FX.

The native catalogue migration belongs to
`tools/enemy_atlas_1013/apply_stage2_amplify_1031.py` and is called by its owning
catalogue builder. Unrelated entries compare unchanged. 397 catalogue entries now
include the replacement and four elite roles. Stage1 changes remain active.

The interactive adapter now waits for complete document/runtime loading as well
as boot assets. Previously it could spawn a legacy actor while late refit scripts
were still loading, which caused the initial generic-jet identity. It reports
V31 phases and beam counts and hides the old EP13 attack buttons for these units.

## Verification and previews

- `node --check assets/game.js`, the V31 owner and its art registry pass.
- 86 native Chromium checks pass, including actual damaged pixels and flash
  expiry on every hull, no runtime hull/engine rotation, shield/hull routing,
  interception at birth, real player-shot arc cancellation, all four carrier
  roles and clear full-footprint turret placement.
- 15 cleanup/source checks pass: six native lethal-damage sequences cancel their
  attacks and complete, all85 files match even registered geometry, and retired
  entries are absent. Crucible tests use distinct native damage events for both
  pools; they preserve the engine's first-lethal-event reservation.
- 26 preview checks pass: guide selection, all other current cards preserved,
  retired entries removed, seeking and playback, all20 films with decoded audio,
  and no page/console/asset errors.
- Three interactive catalogue checks pass: the first actor is the native V31
  disc, all nine live beams/current phase are reported, and the page/console has
  no errors. `atlas-checks.json` and `native-atlas-disc.png` retain this evidence.
- 20 native Furious films total282.84 seconds,58.4â€“59.6 native fps. The observer
  uses normal movement and native God protection; no enemy HP, phase or timer is
  written during recording. Carrier footage retains its actual child squadron.
  These are isolated demonstrations, not a campaign balance certification.
- `node _BUILD_SOURCE/test_fl.js` still exits1 **before assertions and final
  summary**, because the pre-existing ignored
  `UNUSED_ASSETS/retired_art_1022/manifest.json` is absent. No fake archive,
  bypass or passing full-suite claim was introduced.

Native evidence: `_shots/stage2_amplify_1031/smoke-checks.json`,
`cleanup-checks.json`, `guide-checks.json`, native screenshots and video reports.
The affected bomb/disc/turret films were replaced after the final arc and laser
corrections. A later destruction-cleanup guard does not change the movement-only
previews. Full movies decode through FFmpeg and Chromium.

Local preview gallery:
`http://127.0.0.1:8805/current/stage2-amplify-1031.html`

Current enemy guide:
`http://127.0.0.1:8805/enemy-showcase-1031.html?revision=stage2-amplify-1031#enemy=stage2-disc`

`publish_stage2_amplify_local_1031.py --install` updates only scoped current routes
in the existing local review server. 164 guide cards preserve all other current
films. The old complete reel is explicitly archived. No commit or push occurred.
The separate dark-weapon pass remains deferred until Mike commands it.
