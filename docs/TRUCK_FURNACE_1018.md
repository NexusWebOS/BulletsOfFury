# Missile truck and Furnace changes — October 18, 2026

Mike requested a generated modular Level 1 missile truck, travelling fire walls
and warned side geysers during the Level 2 boss, and faster head rotation on
Hard and Furious.

The actual `s1truckmissile` and black `s1truckmissile_b` now use a generated
chassis with two separately aimed, destructible launcher racks. Their warning,
three-round release, recoil and reload have distinct generated poses. Destroying
one rack silences that rack; the other continues. Retina exposes both racks and
the cab hull. Primary rounds, lasers, missiles and ice orbs damage the truck;
its committed missiles can be shot down. Existing tank ground motion and enemy
death/reward owners remain authoritative. Owner and module `markHit` flashes
render through the actual current animation frames and expire normally.

Eight chassis poses and sixteen launcher poses have olive and paint-only black
variants:48 loose192×256 PNGs, fixed96,128 pivots, common proportional source
scale0.625. Source bounds and fixture registration are recorded in
`_ART_SOURCES/missile_truck_1018/registration.json`. No shared atlas edits.
`build_missile_truck_1018.py` owns both pixels and `missile_truck_art_1018.js`.
The bank onions were inspected before native rendering.

The Stage 2 Furnace no longer spawns the hostile quarter-screen red zone
columns. Its arms/core phases regain the existing three-alert travelling fire
walls. The mountain-side vents also operate during those phases, alternating
sides, with1.25s warnings. Authored impact asterisks and arrows align with the
actual horizontal eruption direction and remain inside the visible field.
Walls and side vents queue independently so their warning sequences do not
overlap. The final head sweep owns its lanes. Native left-arm flamethrower,
right-arm magma/fire-wave alternation, core lasers, armor pools, shields and
ice advantage remain. Friendly geysers and the separate copied Stage 8 Furnace
retain their own behavior.

The approved PixelLab head bank is unchanged. A full360° eye-laser sweep takes:

| Difficulty | Before | Now | Charge warning |
|---|---:|---:|---:|
| Normal |5.8s |5.8s |1.85s |
| Hard |5.1s |4.0s |1.65s |
| Furious |4.5s |3.0s |1.45s |

The charge, rumble, recovery and actual eye sockets remain in place.

Validation: `node --check` passed for all three changed gameplay scripts.
`node _BUILD_SOURCE/test_fl.js` reached its final BUILD OK summary, exit0:
8,791 passed /0 failed, matching the baseline. Real Edge/Chromium probes passed
91 checks total:33 truck/hazard checks,54 existing Furnace encounter checks,
and4 interactive review controls. No page, console, draw or asset errors.
All three difficulties were checked at the regular full field of view.

The connected physical controller initially moved the automated pilot; native
test pages now isolate hardware input while retaining keyboard and combat
code. The map-jump fixture also settles scroll before inserting the truck.
Native death checks wait for the authored delayed removal and verify its
reward. Missile checks use emitted totals, observed live flags and actual J
gunfire interception; a projectile removed within its spawn frame is not
required to survive until the QA sampler.

Review: `docs/previews/truck_furnace_1018/index.html`.
Evidence: `docs/qa/truck_furnace_1018.json` and ignored
`_shots/truck_furnace_1018/`. No commit or push was requested or performed.
