# Late-stage airborne attack patterns â€” October 13, 2026

`assets/enemy_patterns_1013.js` introduces six attacks across 19 stage/type slots
(18 distinct enemy types) in stages 5, 7, 8 and 9. Existing stage wave counts,
enemy HP, body art, destructible parts, death behavior and background fire remain
owned by their native controllers. The module is included after air motion.

## Attacks

- **Traveling laser:** the ship holds a readable firing pocket, warns the entire
  corridor it will traverse, then moves horizontally with a continuous laser
  attached to its actual muzzle. Both outside edges remain available. The beam
  grows and dissipates without damage during its dim opening/closing frames.
- **Charged beam:** a native energy orb grows at the gun, a lane announces the
  committed aim, then the heavy animated beam fires. Moving after the tell starts
  defeats the aim; it does not follow the pilot after release.
- **Gap rings:** successive radial volleys leave a shared, clearly open escape
  wedge. Later pulses travel slightly slower and have offset pellet positions,
  producing separated arcs rather than merging into a single wall. The wedge
  is chosen again on the next fully announced attack.
- **Missile fan:** three or five shootable missiles leave on fixed angles in
  one to three announced volleys. There is no post-release homing. The native
  missile interception and player Retina code recognizes the missiles.

- **Twin rifle burst:** Rifle Locust alternates real `mg` rounds from both articulated gun tips. Aim is committed separately for each barrel, recoil follows each shot, and an authored rotary muzzle flash follows the moving gun. Destroying one barrel removes that barrel's fire; the survivor continues. Destroying both ends the attack.
- **Crystal pulses:** the Stage 9 Beacon emits purple `warpprismshard_*` projectiles in separated gap rings. The matching violet `warpcrystalimpact_*` release stays attached to its emitter. Its original queued attacks also fire these physical crystal shards. Neither this unit nor Rifle Locust uses a beam.

All effects use existing authored BOF `laserbeam_*`, `nchg_orb_*`, biome
projectile art, charge sounds, heavy laser audio and missile reports. No new
textures, procedural enemy sprites or particle generators are introduced.

## Roster

| Stage | Existing enemies | Attack roles |
|---|---|---|
| 5 | Beam Frigate, Twin Station, Gravity Orb, Missile Satellite | Moving/charged beams, rings, missile fans |
| 7 | Toxic Skimmer, Hexpyre, Imp Harrow, Rifle Locust | Moving laser, gap rings, missile fan, alternating modular rifle burst |
| 8 | Solar Corvette, Death Orb, Hunter, Hexpyre, Furnace Maw | Moving/charged beams, rings and missiles |
| 9 | Dimensional Gunship, Hyperspace Prism, Ring, Beacon, Horizon, Dread | Moving/charged beams, gap rings and crystal shards |

Only one upgraded field attacker can charge/fire/recover at a time. A controller
must finish its current native attack before becoming eligible. The enemy stays
damageable throughout; destroying the emitting gun interrupts the attack rather
than moving its beam to another gun. The twin-rifle role intentionally keeps a surviving gun operational. Shield-break stun, freeze, mercury lock,
death, removal, boss/miniboss transition and stage changes cancel owned beams.

Native firing flags and separation flags are restored at recovery. Each unit
gets at most two upgraded attacks, separated by at least eight seconds. Native
shots between these attacks and the original finite engagement/exit remain.

## Difficulty settings

| Setting | Easy | Normal | Hard | Furious |
|---|---:|---:|---:|---:|
| Warning seconds | 1.30 | 1.12 | 1.00 | 0.90 |
| Recovery seconds | 1.25 | 1.10 | 1.00 | 0.90 |
| Laser travel speed (world pixels/s) | 45 | 55 | 65 | 74 |
| Nominal beam damage width | 16 | 18 | 20 | 22 |
| Ring candidate pellets | 12 | 16 | 20 | 24 |
| Ring pulses | 1 | 2 | 2 | 3 |
| Open wedge (radians) | 1.52 | 1.38 | 1.24 | 1.12 |
| Missiles per fan | 3 | 3 | 5 | 5 |
| Missile fans | 1 | 2 | 2 | 3 |
| Alternating rifle rounds | 6 | 8 | 10 | 12 |
| Rifle beat spacing (seconds) | 0.18 | 0.16 | 0.15 | 0.14 |
| Existing + new projectile budget at release | 68 | 82 | 98 | 112 |

Ring counts decrease after removing pellets in the escape wedge. New attacks
wait until existing projectile pressure is below their start threshold; complete
volleys are skipped if they would exceed the budget. Native difficulty bullet
speed scaling still applies. `insanity` uses the Furious pattern profile.

## Verification

Native fixtures use the shipping renderer and input/collision code. The test
files are `_BUILD_SOURCE/probe_enemy_patterns_1013.py`,
`probe_enemy_patterns_live_1013.py`, `probe_enemy_patterns_safety_1013.py`, and
`probe_enemy_patterns_coop_1013.py`.
Machine-readable results are combined in `docs/qa/enemy_patterns_1013.json`.

The visual fixtures cover all four difficulties, the four attack families and
all 19 configured stage/type ownership slots. Reviewed captures show native hulls,
modular weapon mounts, real charge/beam art, distinct ring arcs, missile fans and
the matching warning lanes. Captures are under `_shots/enemy_patterns_1013/`.

Scheduled-wave probes keep the real stage plans and verify activation in 30
seconds of Stage 5/7/8/9 Normal and Furious play. These captures use invulnerability
to keep the observation camera alive. They are not measured player survival rates.

The separate escape fixtures use native movement at base speed, no shield, no
roll/somersault and no firing. Ordinary waves and unrelated Stage 5 asteroids are
removed for these isolated attacks; the pilot either holds the ring opening or
moves left after a 0.2-second reaction delay. They demonstrate an accessible
response to each attack, not a guarantee about every campaign overlap or a
population-level survival percentage. Browser timings are harness measurements
on this machine and are not a universal FPS guarantee.

Co-op checks use real seat swapping and damage: a beam can hit P2 independently,
invulnerability prevents repeat damage and the active seat restores to P1.
The stun test calls `enemyShieldStunStart` to exercise the actual object-valued
`_eshStun` path, including its skipped native enemy tick.

Final verification: 16 native difficulty fixtures, 19 ownership slots, eight
scheduled-wave scenarios and 24 unshielded escape fixtures passed. Edge covers
all four difficulties; Chrome and Firefox repeat the Furious escape fixtures.
All three browsers passed the real shield-break stun checks with no page errors.
P1 death with P2 alive still permits attack start and continuation; both pilots
down cancels the attack. The module adds 14,737 bytes of JavaScript and no raster
assets. Full-game regression is owned by the combined Contra encounter pass.


## Weapon identity correction (October 13)

The initial recorded Stage 7 charged-beam fixture and Stage 9 Beacon missile
fixture predate Mike's weapon identity correction. They are superseded by
`_BUILD_SOURCE/probe_enemy_weapon_identity_1013.py` and
`_BUILD_SOURCE/probe_enemy_weapon_escape_1013.py`. The earlier general probes
now select rifle/shards for these same units, including the preview API.

The correction passed 12 native pattern runs, six runs through the original
controllers after recovery, and 15 interruption cases across Edge, Chrome and
Firefox. Edge covers Easy/Normal/Hard/Furious; Chrome and Firefox cover Furious
plus the normal native controllers. Each rifle round originates exactly at a
live barrel; both guns produce authored muzzle frames. Tests independently
destroy each barrel, destroy both, and break shields during firing. The actual
object-valued shield stun cancels release and hides attached muzzle effects.

Eight additional native Edge movement fixtures passed without shields, firing,
rolls or somersaults, at base speed: move left after a 0.2-second reaction delay
for the rifles, or hold the announced opening for the shard rings. Regular wave
spawns are isolated, so these remain attack-response checks, not campaign
survival percentages. Actual screenshots are in
`_shots/enemy_weapon_identity_1013/`. No page errors occurred.
