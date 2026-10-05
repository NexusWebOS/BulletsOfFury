# Overnight combat upgrade — October 5

Mike requested stronger independent finale encounters, persistent copy health,
proper symbiote emergence, a whole knight with an intact head, live Rebel Gang
defense, readable late-stage ammunition, the approved bomber palettes, musical
Hammer upgrades and direct boss passwords. He also reported that lasers were not
damaging Rebel fighters.

## Rebel laser collision

The sustained-beam and flame branches previously tested the squad controller's
single center instead of the five moving fighter hulls. They now intersect each
live hull and use an independent burn clock per fighter. Cole VI, VII and Fusion
projectiles still pass through the ordinary weapon collision path. Cole's homing
search now selects individual visible Rebel hulls instead of the empty squad
controller. Blind shots can hit cloaked Nyx; cloak continues to block missile and
homing acquisition. Entry, warp and protected dialogue remain protected.

Finale sustained beams also select an intersecting code projection before its
owner's whole-body rectangle, so shields actually absorb pulses and reach zero.
This is a physical collision repair, not a health reduction or invulnerability
bypass. The four base-game integration lines preserve the old paths for unrelated
bosses and ordinary enemies.

## Three outer finale fights

The original normal drone arrives, then mutates into the first boss. Its independent
attack book has aimed paired gun streams, committed claw lunges with flank fire,
warned paired lances and radial volleys with a dodge gap. The ghost has its own
volley, dive, lance and orbit cycles and a 4.8-second introduction.

The third encounter gathers loose black symbiote fragments into an animated void,
then reveals the giant authored fiend. Front/back sorting, foreshortening and
three sets of eight rotational views produce the swirl. No binary download effect
is used for the transformation. The introduction fills one health housing through
eight successive colors. Normal combat shows the active form's actual remaining
health.

Each third-encounter copy keeps its own remaining HP and destroyed parts. Returning
to Dracula uses his saved pool; switching forms never heals it. Defeated copies
cannot be selected again. Budgets derive from the existing source boss values,
with 1.30× for the drone, 1.65× for the knight and 1.50× for the other copies.

| Third-encounter pool | Furious maximum HP |
| --- | ---: |
| Dracula / drone pool | 5,330 |
| Helicopter | 3,567 |
| Furnace | 5,048 |
| Cryo | 7,020 |
| Storm | 8,580 |
| Knight | 10,148 |
| Ace | 8,754 |
| Warden | 9,225 |

Seven copies use their real campaign boss controllers; the drone retains its
authored finale book. All eight were advanced through attack and recovery cycles
in real Chromium. The knight keeps the Hammer controller, sword throws and gun /
targeting combos, plus committed shield smites and Dark Code salvos. Its body is
one generated plate per pose, with the complete head in all eight poses. Sword and
shield are independently mounted, hittable and breakable.

Code projections track exact remaining HP, flash on impact, exhaust at zero and
shatter into opaque ballistic digits followed by authored terminal explosions.
Form cleanup preserves ongoing shatter effects. A projection discharges after
6.5 seconds if left intact, then stays exposed before rearming. Finale support
capsules alternate usable Flash and Time Bombs: first after 11 combat seconds,
then every 22 seconds (18 on Easy).

## Late-stage and musical fights

Stage 6 bomber render paths use the approved genuine red/green stealth sheets,
including lateral and vertical passes and exact-alpha white hit silhouettes.
Arcade durability is six HP, owned by spawn/simulation; drawing never heals a
wounded bomber. No new jet silhouette or tint overlay is used.

Gang Mode now raises short live shields around surviving Rebels without clearing
hostile fire or starting a cinematic. Voss keeps 1,250 px/s through every visible
turbo demonstration pass. Jace's live full helix ball travels south at 380 px/s;
Rook's heavy special slugs also travel south. Their harmless introduction props
travel south at 520 / 640 px/s. Staggered personal specials remain active. Baseline
guns yield during their own firing specials, reducing overlapping volleys.

Ordinary Stage 6–8 gun/tracer rounds use brighter authored strips without changing
their collision dimensions or shootability. A concurrent ordinary-fire cap and
modest speed reduction preserve boss signature attacks. These are initial tuning
changes, not proof that every Furious campaign route is perfectly balanced.

Both HAMMER and HAMA add the real campaign Hammer machine-gun chain and targeting
spell initialization to their musical attack rotation. HAMA plays the retained
instrumental, with robot vocal/caption playback disabled. Original source audio
files remain preserved.

Live testing also found a renderer stall: an animated opening beam could have a
positive floating-point epsilon width. Its strip loop then attempted trillions of
draw calls. Subpixel or invalid beam geometry is now skipped at rendering only;
attack clocks and collision remain unchanged. Carrier/ace donor tests now run to
completion.

## Authored art and verification

The built-in image generator produced 12 symbiote animation cells, eight whole
knight poses and 24 loose fragment views. Originals, generation briefs and hashes
are preserved under `_ART_SOURCES/overnight_1005`. The owning builder
`_BUILD_SOURCE/build_overnight_1005.py` performs equal-cell slicing and registers
all 44 deployed keys in `assets/overnight_art_1005.js`. Native RGBA alpha is retained
unchanged. No shared packed atlas was edited.

Runtime layers: `assets/overnight_finale_1005.js`,
`assets/overnight_combat_1005.js`, `assets/overnight_routes_1005.js`.
Password reference: [all encounter routes](PASSWORD_ENCOUNTERS_1005.md).

Final verification totals are recorded in `docs/qa/overnight_1005.json`. Native
probes cover hull damage for all five Rebels and all three Cole laser modes, cloak
acquisition, shield exhaustion, actual donor controllers, intact knight rendering,
support capsules, bomber durability, Voss speed and musical Hammer attack state.
Keyboard tests exercise all new codes and representative complete difficulty /
pilot deployment flows. The playable review blocks campaign save writes.

Eight focused live-engine recordings cover Stage 6–8 waves, the Rebel dogfight,
all three outer finale fights and the knight. They include actual player deaths,
keyboard flight and firing. Recordings are silent canvas captures, not a complete
human campaign clear or full audio review. Every three-second sample across their
timelines is included in review contacts for visual inspection. Stage 7–8 wave
samples include intervals without firing so hostile attacks can complete instead
of being erased by Cole's upgraded primary.

Review: `_shots/overnight_1005/review.html`. Scratch recordings/screenshots/logs stay
under ignored `_shots/overnight_1005`. Mike authorized GitHub publication on October 5; scratch review evidence remains local.
