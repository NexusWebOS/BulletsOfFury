# Independent front-end audit of the November 1 refits (Claude Code)

Scope: Stages 4-8 regular-enemy refits (`stage4_amplify_1101`, `stage5_amplify_1101`, `stage6_airframe_1101`,
`cloud_carrier_1101`/`carrier_assault_1101`, `stage7_amplify_1101`, `stage8_amplify_1101`). Read-only: no game file was
edited. Real Chromium, TRAP_RAF stepping, invulnerable pilot (playerHit stubbed, never invuln-pinned), DBG.verbose on.

Two harnesses, both new:
- `_BUILD_SOURCE/audit_roster_1101.py` plays each stage's real wave plan for 80 s, passive and firing arms, and per type
  records spawned / on-screen frames / rounds / first-shot latency / kills / off-screen kills / jumps / stuck units.
- `_BUILD_SOURCE/audit_spawn_1101.py` empties the plan and spawns each type alone with the plan's own `spawnEnemy`
  call (stage clock held so the miniboss never arrives). It records speed, sideways drift, each round's angle vs straight
  down and vs the pilot, shot gaps, owner events (`S411/S511/S611/S811.events`), art keys drawn and a crop sheet.
- `_BUILD_SOURCE/probe_stage8_plan_1101.py` logs every `spawnEnemy` call of a real Stage-8 run.
Evidence: `_shots/audit_1101/` (JSON per stage/arm, `spawn_stage*.png` crop sheets, `stage*_sheet_*.jpg`).

## Result: zero console/page/draw errors in every run (Stages 4-8, Normal and Hard, both arms).

## Doc claims that hold (measured)
| Stage | Claim | Measured |
|---|---|---|
| 4 | Highway tank: no side motion | sum abs(dx) = 0 over 12 s |
| 4 | Fuel tanker unarmed, 114 px/s | 0 rounds, 114 px/s, dx 0 |
| 4 | Tractor fires south only | every round 0 deg from straight down |
| 4 | SAM 3 missiles 0.18 s apart | gaps 0.18, 0.18 every salvo |
| 4 | Heavy jet fires along heading | paired missiles 0.18 apart, spread 0-45 deg off the pilot bearing (not aimed) |
| 4 | Command fighter twin MG bursts | 2-round pairs at 0.12 s |
| 5 | Frigate beam | `beam-release` every 4.4 s, red beam visible, shield bubble drawn |
| 5 | Satellite 2 missiles (Normal) | pairs 0.17 s apart |
| 5 | Portal mine 6-way / gravity ring | 6 directions; gravity ring wide fan with a gap under itself on Normal |
| 5 | Repair drone / leech: no ranged fire | 0 rounds |
| 5 | Station shield + spread/beam alternation | hex shield drawn; 6-shot spread then beam |
| 6 | Carrier guns are lasers, hull gated | `laser` events; 10 wells + 2 hulls spawn at the 18 s beat on Hard |
| 7 | Heavy Relay accelerating bursts | gaps 0.23 -> 0.12 s |
| 7 | Toxic tank paired MG | 0.15 s pairs |
| 8 | Blue Hybrid 585 HP on Hard | 585 |
| 8 | Hunter beams, Tentacle no gunfire | `beam-release` x2; tentacle only tell/strike events |
| 8 | Leech/Razor/Solar removed | `spawnEnemy` creates nothing for them |
Art: every refit renders its authored cells (crop sheets inspected); warning cones precede fire on all Stage-8 roles.

## Findings for Codex / Mike
1. **Stage 8 starves its own wave queue for a player who is not killing fast.** game.js dispatch reserves 3 slots on
   Stage 8 (`_nextPressure = run.stage===8?3:1`). Several refits now station-hold (scout, needlejet, Death Orb, Blue
   Hybrid, Carrier, Gunship drift ~20 px/s = scroll only, 12+ s in isolation). Hard, passive pilot: after the two scouts at
   5.6 s no plan beat dispatches until 34.4 s; then razor/voidjet/spread release on the same frame the miniboss
   triggers and the miniboss intro clears them. The scouts sit at y~170 for ~24 s. With a firing pilot the queue
   flows and every refit role appears. Same trap game.js's 0809n comment records for Stage-1 naval units (which the
   dispatcher now excludes). Decide whether parked Stage-8 roles should count against the cap.
2. **Dead plan beats on Stage 8.** The removed types' beats still run: 4.0 leech, 7.0 razor x2, 25.2 solar, 43.0 razor
   spawn nothing, and both 11.5 s `s8spread` log a single `cancel` (consolidated). ~7 of 25 authored units are gone from
   the opening; the first 10 s field only 2 interceptors, a needlejet and 2 scouts.
3. **Stage-6 route jets (`l6v_*`, stage6_airframe_1101) open fire on their first visible frame** (first shot 0.0 s for
   all nine variants; everything else in Stages 4-8 waits 0.8-3 s). `l6v_s0` fires 8 rounds while still at the left edge.
   Twin-MG ~8 rounds/s on Hard. No warning window before the first burst.
4. **Stage-7 Heavy Relay (`cp22relay`) fires from off-screen** - 5 rounds while entering past the left edge (x -1..-30).
5. **Stage-4 refits are on the fodder HP cap.** SAM/tractor/tanker/missile truck spawn at 9 HP, command/heavy jet 10
   (authored 28-44). Not a regression (EHP() is global; the doc's "native HP" is the capped value), but with the pilot
   firing, a missile truck and a bomber died before their first shot - the same pattern fixed on Stage 5 in 1019.
6. Plan names are remapped at spawn: `s4minitank` and `s4airfield` -> `sandtank`; `s7sampler`/`s7mine` -> `cp22drone`,
   `s7skimmer`/`s7serpent` -> `cp22slime`, `s7lamprey`/`s7canister` -> `cp22relay`. Intended per the docs, noted so
   probes don't search for the plan names.

## Harness traps (for whoever reruns this)
- **Normal blocks Stages 6-8**: `normal_finale_1031.js` makes `beginStage(6..8)` open the Normal-complete screen. Forcing
  GS.PLAY afterwards gives an empty stage. Audit 6-8 on Hard.
- Every stage's later cast sits behind its miniboss (stage clock freezes at 26-34 s). A timed playthrough with a pilot
  that can't kill the miniboss never reaches them; spawn them directly.
- Carrier/frigate/hunter beams are not eBullets; read the owner's `.events` log.
- Big hulls (Blue Hybrid) fire from sockets > 90 px from centre; nearest-unit bullet attribution misses them.
