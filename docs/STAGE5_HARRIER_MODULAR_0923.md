# Stage 5 Chaos Harrier — modular laser pass, 2026-09-23

The miniboss now renders its clean hull and two independently pivoted gun modules
from the existing authored hull plates. The `ch_lance` attack reel is no longer
used by the encounter: it contains beam pixels inside its supposed charge frame.
Lasers, muzzle flashes, charge effects and warning fields are separate layers.
The wing muzzle positions use the same pivots as the gun hardware.

All four original attacks now use the shared green/yellow/red warning fields,
hazard sign and alert sound. Aim tracks during the first half of each warning,
then locks before release. Neither the main beam nor the wing lasers follows late
player movement. Beam rendering and damage stop together during recovery; death
also removes all warning and laser layers.

The existing three-teleport cycle remains. Its three subsequent laser attacks
finish with a three-emitter crossfire on Hard/Furious. Plasma volleys contain
4/4/6/8 shots on Easy/Normal/Hard/Furious. Shared warning durations are 0.72 seconds
for projectile volleys, 1 second for wing lasers and 1.2 seconds for the main beam
or crossfire; Hard uses 88% and Furious 75% of those durations. Each sustained
laser attack retains a recovery window.

No new generated art was required for this implementation. Automatic approval
review rejected uploading the private source image to SpriteCook because it
required specific authorization to export that payload. No upload or generation
completed, and no SpriteCook generation credits were spent.

## Verification

- `node --check assets/game.js` passes.
- `_BUILD_SOURCE/probe_harrier_modular_0923.py` passes in real Chromium with no
  page or console errors. Screenshots inspected for charge, warnings, paired fire
  and three-emitter crossfire. The probe observes the game context's `drawImage`
  calls, checks zero old lance frames, two independent hardware draws, no damage
  before release, fixed aim, recovery, death cleanup, translated muzzle anchors,
  all difficulty variants and complete teleport/attack cycles.
- Evidence: `_shots/harrier_modular_0923/`, including `results.json`.
- Full regression suite completed: 4,898 passing assertions, 81 failures, exit 1.
  Failure names match the earlier 81-failure sound-pass baseline. Compared with
  the immediately preceding 80-failure hammer run, the sole extra name is the
  documented intermittent Stage 1 sand-tank spawn check. Log:
  `_shots/harrier_modular_suite_0923.log`. The missile-flight fixture waits for its warning
  rather than expecting an immediate shot at 0.29 seconds.

This is scripted encounter verification; a complete human balance playthrough is
not claimed. Existing unrelated working-tree changes were preserved. No commit
or push was requested for this change.
