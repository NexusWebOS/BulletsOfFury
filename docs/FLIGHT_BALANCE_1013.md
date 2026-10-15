# Small aircraft, depth entrances and continuous scrolling — October 13

Mike requested fragile small aircraft with quicker attacks, depth entrants that
have the same health as their normal family, and uninterrupted stage scrolling.
This update is in the GitHub coding checkout; no commit or push was requested.

## Health and attacks

`assets/combat_pressure_1012.js` no longer supplies the 50/90 HP override to its
Stage 1 Delta and Stage 2 Ash ambush constructors. Each uses the complete normal
family health calculation, including difficulty, pressure and co-op.

| Ambush family (solo) | Easy | Normal | Hard | Furious |
| --- | ---: | ---: | ---: | ---: |
| Stage 1 Delta | 4 | 6 | 6 | 11 |
| Stage 2 Ash | 2 | 4 | 6 | 9 |

`assets/flight_variants_1012.js` replaces the formation-wide 20/36/60/90 HP values.
Corner depth entrants derive health from their actual authored aircraft family:
Delta, desert interceptor, Storm Dart or void interceptor. Small formation craft
use half their family health, with per-difficulty caps of 6/8/10/12 HP.

| Small formation (solo) | Easy | Normal | Hard | Furious |
| --- | ---: | ---: | ---: | ---: |
| Stage 1 | 2 | 3 | 3 | 6 |
| Stage 4 | 4 | 6 | 7 | 8 |
| Stage 6 | 4 | 6 | 8 | 10 |
| Stage 8 | 6 | 8 | 10 | 12 |

The first formation missile release is scheduled at 1.90/1.75/1.60/1.50 seconds,
previously 2.30 seconds. Repeat-volley gaps are .48/.42/.36/.30 seconds, previously
.70. Barrel bomb passes start at 1.10 seconds instead of 1.50. Per-aircraft stagger
is .08 seconds instead of .12. The actual release still requires an aircraft in
the firing area. Missile warning duration remains 1.15 seconds; bomb warning
duration remains .75. Projectile speed, number of aircraft and volley counts
remain unchanged.

The drone shell had an invisible cannon controller that could fire outside the
formation's advertised attack schedule. Formation initialization removes that
controller; its normal collision, damage, rewards and death bookkeeping remain.

## Continuous scrolling

The Stage 1 ground-wave pressure flag was included in `drawLevelMaster`'s boss
hold condition. Nine formation craft could therefore stop the entire terrain
when a mapped tank wave became due. Ordinary pressure no longer owns a terrain
hold. The ground wave stays queued under the existing density and terrain checks,
then dispatches when space opens. Actual boss/miniboss hold behavior is retained.

## Native verification

- CP12: 202 checks, including 48 family-health fixtures across both stages, all
  four difficulties, solo/co-op and all three entrance directions; 24 actual
  arrival/firing fixtures; 32 death/dying interruption checks.
- VP12: 112 formation fixtures (seven patterns, four stages, four difficulties),
  plus 16 exact family-health and native-damage comparisons. Small craft take
  2–6 two-damage hits in those fixtures; the ordinary first-lethal-hit grace
  still applies. Destroyed craft do not emit later shots.
- Scrolling: 38 checks, including all five affected stages on every difficulty,
  geographically due ground waves, later tank dispatch and real encounter holds.
- Native Edge screenshots inspected; zero page/console errors in these probes.

These are focused engine and rendered-behavior checks, not a full human balance
study. Live player pressure and co-op can change family-derived health. Reusable
probes and detailed reports are in `_BUILD_SOURCE` and `docs/qa`; screenshots and
the required full-suite log are in `_shots/flight_balance_1013` and the individual
probe folders.

Required final checks: all three changed JavaScript files pass syntax;
_BUILD_SOURCE/test_fl.js completed with the final BUILD OK / 0 ERRORS banner
and exit code 0.
