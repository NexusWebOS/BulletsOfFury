# Stage9 water roster and front-facing Current Breaker / November1

Current review: http://127.0.0.1:8805/current/stage9-water-refit-1101.html#enemy=stage9-cbreak

Live owner: `assets/stage9_amplify_1101.js` (S911). Art registry:
`assets/stage9_amplify_art_1101.js`. Rebuild with
`python _BUILD_SOURCE/build_stage9_amplify_1101.py`. Campaign timing belongs to
`assets/stage9_schedule_1101.js`; the isolated attack/graphics films use the same
S911 source, with no enemy HP/phase/attack-clock writes.

Mike corrected Current Breaker's initial angled art while this pass was active:
**he faces directly toward us**. The selected canonical body, transformation and
action sheets use square shoulders/chest and two eyes directed at the player.
The humanoid renderer always selects front0. Physical flight can aim toward the
player without rotating/flipping that front-facing body. The flying pose uses
foreshortened hands in front, then open palms firing toward the player.

| Role | Current design and arsenal |
| --- | --- |
| Comet / Slider | Existing canonical plate palette-swapped pink; preserved metal luminance/outlines, forward fire and curved pass |
| Beacon / Orb | One solid plate, bright flashing internal core, exact nine-way teal laser-orb volleys, spinning hull and real energy shield with authored animated serpent channels |
| Ring / Spinner | New open torus with six independent radial weapon pods and real source heading cells |
| Interceptor / Jumper | New four-blade jet with twin articulated laser cannons and committed jump/run; separate from retained Kamikaze |
| Gunship / Beam | One original solid hull, two giant water beams at its measured actual barrel mouths, independent exhaust/shield/muzzle effects |
| Water Skimmer | New hydrojet/racing fighter with water styling, curved flight and twin weapons |
| Ring / Laser | Separate elliptical hull and two suspended articulated beam cannons |
| Gate Turret | New flying gate frame with four independently directed corner guns; no ground base |
| Gravity Leech | New mechanical squid/feeler silhouette with two obvious heavy independent cannons |
| Prism / Beam | New triangular crystal vessel, separate twin beam projectors and native absorbing shield |
| Echo Fighter | New needle/canard aircraft, distinct resonance guns and fast warned runs |
| Singularity / Orb | Distinct vortex sphere with crystal petals and stabilization fins |
| Prism / Orb | Distinct prismatic crystal/satellite vessel and radial energy book |
| Prism Mine | Actual mine-dispensing alien jet; stationary animated mechanical mines arm by proximity, warn and detonate, and can be shot down |
| Gunship / Laser | New giant water harrier with four actual Stage6 iris/extension/charge/recoil gun mechanisms and water lasers |
| Void Manta | New pink/blue modular manta hull, no shield |
| Tidal Splitter | Actual wave-wing fighter with water guns and authored moving tidal crests |
| Current Breaker | Orb-to-front-facing liquid human, summoned tidal waves, physical water grenades, flying palm laser/mist fire; one real HP pool through the transformation |

All19 guide roles are distinct where requested. Current Breaker's29 exported
transformation cells use eight authored shapes plus baked source-pixel liquid
dissolves, one measured chest pivot and one scale. The final cell is pixel-identical
to the actual idle plate. Eight front-facing action poses use registered hand
positions; no HTML alpha or runtime static-sprite rotation replaces animation.
Disconnected neighboring-cell edge bits were removed before export.

22 selected transparent generated sources and171 even banks are registered in the
owning manifest. Source briefs, output IDs, original references and hashes are
under `_BUILD_SOURCE/stage9_amplify_1101/`. Canonical retained reference cells have
transparent160-cell padding; they are cropped back to the original128-unit socket
basis, fixing the gunship's formerly offset emitters. Harrier keeps all12 actual
Stage6 gun poses and their measured per-frame bores on a new water hull.

Regular actors retain their native pools; the new giant Harrier and Current use
explicit larger pools with native difficulty/co-op scaling. Weapons share the
unit's real hull HP/flash, without hidden extra budgets. Native shields absorb,
flash and break; their visual layer follows actual body/module pixels. Manta has
none. All primary shots use actual current alpha so empty modular gaps pass shots.
White hit pixels and expiry remain visible, including through shield absorption.

Ordinary water slugs, laser orbs, mist and tidal waves reject offensive interception
from birth. Physical grenades/mines keep interception and native defensive clears.
Water energy does not accidentally inherit missile acceleration/trails; mines
remain still after deployment. Intercepted mines/grenades use the generated water
burst, not a fire explosion. Hand/weapon/muzzle points move with their actual part.
All added attacks use approved shared-mixer cues and retrigger gates; recordings
verify real `cfComboWater`, charge, beam and jet cues, with silent volley partners.

Large beam vessels share a finite heavy-attack interlock. Waiting entrances hold
position rather than drifting into the pilot; committed FOV lanes agree with the
guns and giant beams. Normal fighters retain turning flight, animated source
exhaust and facing fire. Boss entry/launcher defeat cancel warnings, beams and
attached flashes. Existing Event Horizon, Tidal pools/arsenal/fusion/portal and
StageX have their own unchanged owners.

The original Current Breaker wave was at38.85 in a42-second regular section, too
late for the new reveal/book. Its entrance is now12.05 at the camera center; the
38.85 beamship and Singularity remain. The native42-second length, miniboss gate
(`at:.45`, `afterScroll:1201`) and boss owners are retained. A native-input campaign
probe gets through the ordinary dispatch cap, sees the front-facing human and its
actual attack within the regular-wave window. No enemy HP/phase/timer writes are
used to make that happen.

Verification and local publication:

- `_BUILD_SOURCE/probe_stage9_amplify_1101.py`:156 live difficulty, attack,
  actual damaged-pixel/expiry, shield and birth-interception checks.
- `_BUILD_SOURCE/probe_stage9_edges_1101.py`:28 real muzzle-pixel, alpha-gap,
  shield, mine-motion, handoff, crowded-heavy and other-stage checks.
- `_BUILD_SOURCE/probe_stage9_schedule_1101.py`:4 actual campaign dispatch,
  front-facing reveal, attack-window and native-gate checks.
- `_BUILD_SOURCE/record_stage9_amplify_1101.py`:19 fresh isolated native sorties
  with game audio, input-driven movement and a labeled invulnerable observer.
- `_BUILD_SOURCE/publish_stage9_amplify_1101.py` and
  `_BUILD_SOURCE/verify_stage9_preview_1101.py`:23 browser playback/seek/pixel,
  responsive layout and guide checks plus full H264/AAC and PCM decode.

211 focused checks pass.19 films total327.12s at59.5–60 native fps. Decoded peaks
are0.294–0.357, with audible nonzero PCM and no clipping. The guide has154 cards;
all135 other-stage cards and their films are unchanged. Evidence is under
`_shots/stage9_amplify_1101/`.

Syntax checks pass. The required full `_BUILD_SOURCE/test_fl.js` exits1 before
assertions or its final summary because the existing ignored
`UNUSED_ASSETS/retired_art_1022/manifest.json` is missing. This is not a green
full-suite run. No commit/push is part of this pass.


Latest flight follow-up: Mike requested true overhead flying sprites separately
from the frontal transformation/casts. Eight new authored overhead directions and
source-pixel launch/return transitions now ship in177 banks from23 selected
sources. Current alone has a new recorded preview. See CURRENT_FLIGHT_1101.md
for source ownership,38 focused checks and the unchanged full-suite limitation.


Latest material pass: ten hulls now use distinct black/blue, violet/pink and
black/pink families; nine other models and every ordnance/exhaust bank are
unchanged. Rebuild through the same owner using palettes.json. Partial fresh
film publication retains Current overhead flight. See STAGE9_PALETTES_1101.md.
