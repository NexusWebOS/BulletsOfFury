# Stage8 alien roster refit / November1

Owner: `assets/stage8_amplify_1101.js` (S811). Art registry:
`assets/stage8_amplify_art_1101.js`. Rebuild the source-derived exports with
`python _BUILD_SOURCE/build_stage8_amplify_1101.py`.

This pass is scoped to regular Stage8 enemies. Herald, Dracodia, their composite
HP budgets, first-host entrance, transformations, portal and final defeat keep
their existing owners. Stage7 Brood and the separately owned Stage6 Blacksteel
boss remain unchanged.

| Role | Current behavior |
| --- | --- |
| Interceptor | New actual jet with two independently turning laser cannons; bursts and committed beams |
| Imp Harrow | Original horned identity, eight authored front/profile/back depth poses, own-pixel glow and audible fire |
| Hexpyre | New modular fire platform; continuous flamethrowers, fireballs and fire lasers only |
| Dark Matter Dreadjet | New large modular jet; dark orbs, beams and physical Retina missiles;420/546/681 HP |
| Alien Laser Harrier | New flying hull with three independently articulated preserved laser heads |
| Hellwing Jet | New actual jet; hellfire slugs, missiles, own-pixel glow and committed turbo runs |
| Parasite | Distinct articulated claw/pincer body with independent weapon pods |
| Crescent | Distinct curved fighter with independent cannons |
| Hunter | Actual loved `S81003.stalker` identity, three blue eye/cannon beams, turning and committed tentacle lunges |
| Skull Jet | New skull fuselage, two bone cannons and new eight-frame rotating bone projectiles |
| Symbiote | New living alien jet with independent dark-energy pods |
| Warp Sentinel | Enlarged same referenced design, independent inner-glowing cannons, fire/void magma and fire beams |
| Alien Carrier | New four-gun hull; eight-pose bay door opens, launches actual Interceptors and closes |
| Death Orb | Actual round eye/core with four independently turning radial weapon pods |
| Blue Hybrid | Larger same blue/red/green identity, independent cannons and core volleys;450/585/729 HP |
| Furnace Maw | Distinct molten body with dual fireball/flame projectors, replacing the duplicate identity |
| Dark Matter Bomber | One actual bomber hull; new physical animated bombs, native ground Retinas and electric impacts |
| Tentacle | Six three-link source-pixel arms, committed melee grasp and real absorbing own-pixel energy shield; no gunfire |

Elite absolute HP values use Normal/Hard/Furious and retain native co-op scaling.
Other units retain native EHP/fodder tuning. Modules share the displayed native
hull pool and white hit flash; no hidden additional part budgets are introduced.
The Tentacle's separate medium energy shield deploys, absorbs, hits and breaks
through `enemyShieldEquip`; it is rendered along actual hull and limb pixels.

Stage8 Leech, Razor, Solar, Cryo Spear, Blacksteel Hunter and Brood Sentinel are
removed from direct/campaign spawns. Former ground missile/laser roles fly on
the new laser harrier; sonic ground fixtures are removed. Duplicate Spread,
Warp Alpha/Beta and Brood/Crescent guide identities are consolidated. Native
campaign beats10/13/27/41 now field Dreadjet/Hellwing/Tentacle/Carrier.

Leech removal intentionally creates **no graphics archive**. Its25 unique source,
runtime, shipping and animation images are deleted. Owning atlas/Stage8/AQ23
builders and registries exclude it on future rebuilds;16 packed cells are
cleared, with213 retained cells verified pixel-identical. Separate Stage5 and
Stage9 Leech identities and shared weapon art are outside this deletion.
Receipt: `_shots/stage8_amplify_1101/leech-deletion.json` and
`leech-atlas-removal.json`. Migration owner:
`_BUILD_SOURCE/retire_stage8_leech_1101.py`.

Art selection:22 generated transparent sources, original Hunter and original
front Imp identity. Source briefs/selected output IDs/hashes live under
`_BUILD_SOURCE/stage8_amplify_1101/`.301 fixed even source banks register common
body pivots, per-joint trunnions, measured muzzle mouths and one proportional
unit scale. Runtime draws authored/baked heading cells, never a rotated static
sprite. Carrier launches apply the same depth scale to hull, guns, sockets and
exhaust. Independent weapons recoil and hold the committed warning direction.

Primary weapon hits sample actual current body/module alpha, letting shots
pass through transparent modular gaps. Continuous flame uses a newly authored
eight-frame plume and its actual animated alpha for contact, rather than tiled
nozzles or a full-width invisible rectangular hit area. Hunter's warned lunges
turn and reach the player before returning to their starting point.

All attacks route through the shared mixer/retrigger gates. Missiles retain
native audible Retina association and physical interception. Ordinary slugs,
bone rounds and laser bullets reject offensive interception from birth; explicit
heavy orbs/bombs retain their physical shooting rules. Heavy attack interlocks,
finite departure, launcher cancellation and native boss handoff stop warnings,
pending launches, beams and attached flashes. Bomber drops use a real physical
projectile and ground Retina, with no asterisk or filled hazard disc.

Verification owners:

- `_BUILD_SOURCE/probe_stage8_amplify_1101.py`:151 live Normal/Hard/Furious
  attack, native pool, real hit-pixel/expiry, shield and retirement checks.
- `_BUILD_SOURCE/probe_stage8_edges_1101.py`: current directed muzzle pixels
  (1440 samples), actual alpha gaps in four headings, physical missile locks,
  cancellation, proportional bay launch, real flame contact, Hunter contact,
  campaign replacements and preserved Stage7 owners.
- `_BUILD_SOURCE/record_stage8_amplify_1101.py`:18 fresh native-input sorties
  with real shared-mixer audio and a labeled invulnerable observer. No enemy HP,
  phase or attack-clock writes; source SHA256 snapshots prevent stale films.
- `_BUILD_SOURCE/publish_stage8_amplify_1101.py`: full H264/AAC decode, PCM
  audio verification and local guide publication, preserving unrelated entries.

Final evidence:202/202 focused checks pass (151 broad live checks,29 edge checks,
22 playback checks).18 H264/AAC clips total327.29s at59.1–60 native fps.
Decoded audio peaks0.175–0.299 with nonzero PCM in every film.154 total guide
cards retain136 unrelated entries unchanged. Pixel contact sheets and receipts
are under `_shots/stage8_amplify_1101/`.

Local review: http://127.0.0.1:8805/current/stage8-alien-refit-1101.html .
The all-enemy player remains `/enemy-showcase-1031.html`.

Syntax checks pass. The mandatory `_BUILD_SOURCE/test_fl.js` still exits1
**before assertions or final summary** because the existing ignored
`UNUSED_ASSETS/retired_art_1022/manifest.json` is missing. This is not a green
full-suite run. No commit or push is part of this pass.
