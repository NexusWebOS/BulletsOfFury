# Quick mechanics tutorial — November 9, 2026

Mike requested a shorter tutorial with no boss, no BOB and only darkened water
beneath the aircraft. `assets/tutorial_showcase_1109.js` now owns the active
tutorial itinerary and scenery. It loads after the existing tutorial and live
repair owners in `index.html`.

## Active flight

Nine short objectives demonstrate movement, firing, one barrel roll, one
somersault, a single Retina missile, a two-target Multi-Retina volley, warning
colors/ground targeting, a weapon pickup and the selected pilot's special pickup.
Objectives advance after the actual native action, with a short confirmation.
There is no final exam, escort wave, BOB encounter, dossier, element lab or
graduation/debrief screen. BOB assets remain available to their separate credits
and dossier owners; the tutorial neither spawns nor draws him.

The existing authored 32-frame, 224×224 Stormglass water bank is tiled with its
own clock and continuous scrolling. Scenery alone receives 56% black darkening.
Academy architecture and clouds are absent. Aircraft, warnings and HUD retain
their native brightness. The compact pilot dialogue remains 84px high, uses the
correct dispatcher portrait and shows one concise objective at a time. The
training confirmation uses the existing avatar-free MW21 menu window.

Practice deltas remain south-facing, tethered native targets. They cannot join
campaign Galaga sorties or hidden attack clocks. Twin warnings, muzzle flashes
and rounds use the measured `s1aPlaneMuzzle` sockets. The warning demonstration
fires three paired, straight-south bursts using the shared enemy MG cue and one
native ground-strike warning. Ordinary rounds retain native non-interception.
Targets keep real damage, white hit flashes and native death ownership.

Native controls/remaps, life protection, pickups, save completion, decline,
pause-skip, co-op restoration and campaign/arcade handoff remain in effect.
Legacy lesson definitions remain source history but are replaced in the active
array; do not reintroduce the long academy itinerary through later wrappers.

## Verification

`python -u _BUILD_SOURCE/probe_tutorial_showcase_1109.py` ran in actual Edge
Chromium and passed 22/22 checks, with no page or console errors. Cole/Normal
Arcade and Juggernaut/Furious Campaign completed all nine objectives using native
inputs without enemy HP, phase or timer writes. The informed automated driver
spent about 20 seconds on objectives; player reading and practice time varies.
This is not a promise of a fixed 20-second first playthrough.

The probe verified no BOB/boss/foreign waves, actual water draw keys, both twin
muzzle coordinates, actual south-facing frame selection, protected ordinary
rounds, life protection, native completion/mode restoration, decline and co-op
skip. A separate native damage fixture measured additional white target pixels
and their expiry. Desktop warning/menu and 390×844 dialogue screenshots were
inspected. Evidence: `docs/qa/tutorial_showcase_1109.json`; screenshots/raw log:
`_shots/tutorial_showcase_1109/`.

`node --check` passes for game.js and both changed tutorial/menu scripts.
The required `_BUILD_SOURCE/test_fl.js` still exits 1 before its assertions or
final summary: the pre-existing local archive
`UNUSED_ASSETS/retired_art_1022/manifest.json` is missing. The before/after error
is identical. No full-suite pass is claimed.

This is a source-build update. The previously downloaded Rev F Windows installer
has not been rebuilt or modified. No commit or push was performed.
