# Boss choreography for Bullets of Fury

October 6 production follow-through: the existing Stage 8 Herald now implements committed, staggered twin cannon releases, owner-specific disarm cleanup and longer disarmed recovery. Two generated signature clips (joint/breach) are registered and reviewed in the native game. The full game suite passes 7,445 assertions; 41 native checks pass with zero errors. See the repository’s `docs/CONTRA_HERALD_1006.md` and `docs/qa/contra_herald_1006.json`. The four original lab bosses / eleven forms remain candidates; this does not implement all 35 reference bosses.

The close replay covers all 35 numbered encounters in Shadowserg's [Contra: Hard Corps all-bosses run](https://www.youtube.com/watch?v=iooQeqdyB8E). Read **BOSS_FIGHT_ATLAS.md** for each fight's visible sequence, player response, art, ownership corrections, uncertainty and original BOF transfer. This kit implements four encounter candidates, with eleven forms, rather than pretending all 35 source bosses have been implemented.

## What was studied

Arrival and arena setup; silhouette anticipation; stance/height/depth relationships; committed travel paths; articulated reach; moving sockets; projectile ownership; spaced and alternating volleys; safe pockets; player aiming while moving; phase transformations; assembly/collapse/reassembly; surviving parts; damage palette flashes; contact weight; charge/release/recoil punctuation; death cascades; color separation and foreground/background depth. Audio was not analysed. This expert no-damage run often ends an encounter before every possible move appears. Sequential visual samples establish the moves shown, not exact hitboxes, targeting algorithms or source frame timings.

The recurring difficulty change is **a new spatial problem**. Blade leaves grounded legs behind a traveling torso. Wrecker becomes a low heap. Takedda builds different reach from recognizable pieces. Bahamut's mutation becomes a looped body, then a hollow ring of faces. Living Warhead turns its casing into a surface, reveals a serpent, then replaces that geometry with arms and a reaching maw. Those are the most valuable BOF lessons: change the route, height, footprint and opportunity to attack, with visible physical cause.

## Playable original designs

Open **encounters.html**. WASD/arrows or drag moves at 240 world px/s. Space fires auto-aimed shots; F deals nearby melee damage. Auto-fire supports hands-free inspection; Pause and Step 0.25s let you inspect each beat. Preview next form is an authoring shortcut. Normal play advances by killing the vulnerable core during recovery. Unlimited shots and hit feedback without a death penalty make this a design sandbox.

| Design / source lesson | Implemented forms | Movement and damage decision |
| --- | --- | --- |
| Split Coupler / Blade, Cyborg Bros | Alternating twin sockets → detached core with grounded pedestal | Bait a committed fan, remove its owner; change depth before the low crossing, route around the reserved leg footprint, punish the reconnect. |
| Spindle Bastion / Spike, Takedda, Spear Sphere | Four extending/raking spokes → compact crossing | Stay between the selected pair of chains or break a tip; after contraction read the compact body's announced lane. |
| Rupture Regent / mutation-route Bahamut | Crossing → coiled neck → eight-mask orbit | Sidestep a locked crossing; leave the loop's extending reach; use the ring's real gaps and hollow centre. Recovery lowers the core into gun/melee range. |
| Payload Cathedral / Living Warhead | Paired breach sockets → vertical column → articulated arms → reaching maw | Remove a socket; bait a vertical column then move sideways; space the extending arm; leave a committed mouth path. Every form resets outgoing attacks. |

These are deliberately schematic collision previews. They must be represented by approved authored boss plates/poses in the live game. The sandbox's circles, chains, freely moving depth plane and auto-aim are review tools, not production BOF art or controls. A core becomes vulnerable only in recovery; that is a BOF proposal, not a claim that every bright Contra flash exposes a weak point.

## Runtime contract

`bosses.js` has no game globals or dependencies. It exports CommonJS or `window.BOFBosses`.

```js
const { Boss } = require('./bosses.js');
const boss = new Boss('payload', 'Normal', arenaWidth, arenaHeight);
// Absolute local seconds, monotonically increasing. Internally steps at 120 Hz.
const events = boss.advance(localSeconds, targetAtSimulationTime);
const pose = boss.pose(playerWorldPosition);
// Render parts/segments from pose; convert local world pixels through camera once.
// Pose includes parts, warnings, hazards, bullets and cosmetic fx.
const damaging = boss.hit(playerWorldPosition, playerRadius);
const struckPart = boss.hitPart(weaponWorldPosition, weaponRadius);
if (struckPart) boss.damage(struckPart.id, weaponDamage);
// Encounter exit, owner removal or adapter abandonment:
boss.cancel('encounter-exit');
```

Identifiers: `coupler`, `spindle`, `regent`, `payload`. Presets: `Easy`, `Normal`, `Furious`. Arenas must be finite and at least 300×300 px. `targetAtSimulationTime(seconds)` returns `{x,y}` in the encounter's local world space. Supply historical target positions during catch-up; returning the current render-frame player for every old tick would distort locks. `pose()` is read-only. `advance()` returns new events; `boss.events` retains the full trace for lab inspection.

Each attack tracks through the first 65% of its tell, then freezes a target. Events include tell, lock, shot, fx, recovery, damage, disarm, phase, defeat and cancel. Part health and owners are independent. A destroyed owner loses its chain, existing shots and future releases while another surviving owner keeps functioning. Transition clears old parts, locks and bullets and has one second without attack collision. The final defeat clears damage before playing its cosmetic breach.

Use the very same part/socket transform for art attachment, shot origin and collision. Chain segments use world-pixel capsules; tips/masks use circles. The orbit has discrete masks and an empty interior, not a filled damage disk. Cosmetics never collide. The pedestal is a separate reserved footprint. Parts can be damaged outside recovery; the core cannot. Continuous swept collision for very fast native weapons remains the game's responsibility.

| Tuning proposal | Tell / lock at | Active | Recovery | Main socket shot speed |
| --- | --- | --- | --- | --- |
| Easy | 1.45 / 0.943 s | 1.30 s | 2.40 s | 180 px/s |
| Normal | 1.25 / 0.813 s | 1.30 s | 2.40 s | 180 px/s |
| Furious | 1.05 / 0.683 s | 1.30 s | 2.40 s | 220 px/s |

The main fan has three release slots spaced 0.22 s and three rays at −0.12/0/+0.12 rad. Column releases use 220 px/s, radius 12; coil/maw paired shots use 150 px/s, radius 10. Core health is 100 per form; sockets 30, spokes 22, mouth 36, masks 12. Sandbox shots deal 5 every 0.18 s, melee 10 every 0.4 s. These values make behaviour reviewable; they are not final boss balance. Amber chain guides identify anticipated reach but do not certify an exact swept danger footprint. Native tuning must validate a reachable escape from both edges with BOF's slowest pilot, body collision, scrolling and support fire present.

## Effects generated and effects still needed

**art/boss_signature_fx.png** is an original transparent 4×3 sheet with three four-frame clips. It is wired into the new lab. Its manifest records native 1448×1086 dimensions, 362×362 cells, per-cell bounds, pivots and hash. Playback uses four equal slots, once, with alpha fade.

| Clip | Event / visual purpose | Duration / anchor |
| --- | --- | --- |
| `joint` | Charge/discharge and disarmed socket: cool white/cyan arc, navy edge, broken residue | 0.65 s; pivot (0.50, 0.58) |
| `contact` | Heavy reconnect/core lowering: low amber dust, gray chips and diminishing grit | 0.65 s; ground pivot (0.50, 0.72) |
| `breach` | Form boundary/defeat: jagged silver casing around a warm rupture with cold edge sparks | 1.00 s; pivot (0.50, 0.50) |

The earlier **reactor_pressure_discharge.png** provides a twelve-frame cyan pressure ring. Neither sheet uses extracted Contra pixels. Both are exact copies of imagegen output; no raster manipulation was performed. Generation did not meet all requested dimensions/padding: the new sheet has 13 px minimum significant-alpha margin and visible joint-anchor drift; the older ring has 1 px minimum. They are sandbox art candidates requiring native art/blending review before registry admission. Do not stretch the joint clip between two sockets and call it a stable conduit strip; generate a fixed-endpoint strip if that attachment is needed.

| Reference family | BOF asset work justified by the observation | Status |
| --- | --- | --- |
| Jumbo/Blade/Spider/Wrecker/Walker | Lift/scrape/landing grit, hinge join, split/reconnect weight | New contact/joint clips are first candidates; biome variants and authored poses still needed. |
| Blimp/Big Magnum/Rail Cannon | Socket charge, compact leading pulse, recoil, damaged muzzle, electrode arc | Reuse inspected registered muzzle/beam families; fixed-endpoint arc still needed. |
| Zodiac/Ninja/Warp | Leading body + brief pose echoes, curved projectile trail, relocation punctuation | Use real authored poses; keep echoes cosmetic. No new full-body reel generated. |
| Mandrake/Mother Alien/Heart/Warhead | Ingredient/fusion, membrane opening, exposed organ, emergence/breach | New breach clip covers transition punctuation; anatomy and transformations still need original authored poses. |
| Builder/Takedda/Army/Yokozuna/Sphere | Recognizable assembly pieces, extension/retraction, debris breakup | Requires approved boss/hazard art; a generic ring cannot replace the mechanical motion. |
| Joe/final Bahamut | Flight exhaust, limb/landing contact, ceiling debris | Reuse registered flight/debris/impact assets after native review. |

Maintain dark cavities and firm outlines under bright weapons. Source machinery often separates cold links from warm fists/eyes; organic bosses use warm organs inside cool/dark structural silhouettes. Preserve BOF's registered biome and ordnance identities. A death cascade should move through actual structural locations after hazards are cleared, rather than cover the entire arena in an opaque flash. Limit a flash while other threats survive.

## Concrete production landing points

Use **INTEGRATION.md** for the inspected existing BOF family table. The first low-art integration is alternating committed releases and part cleanup on the approved `hd1003_` cannon arms or `av3_` modular miniboss. Attach warnings via `combatWarningDraw`/`groundTargetReticleDraw`; bind `av3Beam` and muzzle effects to actual sockets. Use `cwd_` reconstruction/overload for assembly punctuation, `rg4_` phase effects for a cleanup boundary, and `aa5_` anatomy for the finale only through approved authored poses. Preserve `cf1004_` weapon contrast. Actual filenames are not sufficient evidence of an asset's role; consult `ART_TAXONOMY.json`.

The additive package is staged under `_STAGING/contra_study_1005` in the BOF repository. It does not register the sandbox as a live game encounter. No game runtime or production atlas was edited. Before production registration: fit authored poses and collision, check ordinary movement escape and real DPS, verify gun and melee reach, check cooperative target ownership, inspect native effect playback, then run the required BOF syntax/regression suite and Chromium captures. The standalone tests prove cleanup/geometry/scheduling properties, not production balance or complete escape-path safety.

## Verification

Run `node bosses.test.cjs` and `node patterns.test.cjs`; both run in-process. Syntax: `node --check bosses.js`, `node --check boss-lab.js` and the two earlier files. The encounter tests cover every form/preset, lock immutability, independent emitter destruction, transition cancellation, matching chain/tip transforms, hollow mask geometry, 30/60/144 Hz releases and capsule boundaries. `verification.json` records actual check results and browser review, plus remaining limits.
