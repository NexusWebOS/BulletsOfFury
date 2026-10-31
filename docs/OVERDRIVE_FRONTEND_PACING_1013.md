# Overdrive menus and frame pacing — October 13, 2026

The combat overhaul keeps the original menu artwork and password format. All
six current operations now fit in the Password menu: Iron Infiltration,
Fortress / Dead Signal, Machinists, Desert Breaker, Night Run and Prism Bastion.
Both the full keypad and the six level cards remain available on one screen.
Controller navigation can cross between the last card and bottom keypad row.
Existing codes still decode; Level 5's code now enters Desert Breaker.

| Level | Yuri / Normal / Hotwire password |
|---|---|
| 2 | OD-237A-5JXL |
| 3 | OD-237B-5JXM |
| 4 | OD-237C-5JXN |
| 5 — Desert Breaker | OD-237D-5JXP |
| 6 | OD-237E-5JXQ |
| 7 — Prism Bastion | OD-237F-5JXR |

Help now prominently teaches **F / Mode+X to toggle prone**, repeating the
button to stand, and moving while prone to crawl. The cover pages explain
peek fire and blindfire. A fourth page covers Prism Bastion's sidestep, duck
and free-aim controls, with separate standard and six-button assignments.
Opening Help from the paused base stage selects this page automatically.
Campaign completion rewards now check every visible mission instead of a
fixed five-stage list. Existing earned rewards and save data are preserved.

## Fixed simulation, interpolated rendering

The previous refresh-rate heuristic rounded each display interval separately
and discarded fractional time. In a native Chromium fixture, a one-second
sequence alternating 25 ms and 8.33 ms advanced 72 simulation ticks after a
refresh-rate transition. The game now retains the fractional remainder in a
fixed 60 Hz accumulator; the same fixture advances exactly 60 ticks.

Rendering interpolates between the last two simulation positions, including
tank/infantry movement, enemy units, boss bodies and independent Machinist
tanks, camera movement, shot positions and angles. Prism Bastion also
interpolates its reticle, projectiles, hazards, cover rise and depth scale.
Angles take the shortest path across the wrap boundary. Teleports and mission
changes snap to their new position. A `finally` block restores every temporary
render value, so collision, damage, targeting and the next tick always read
the exact simulation state.

Stalls are capped at six catch-up ticks. Hidden-tab time and freeze/resume do
not create a backlog. `TDGAME.step(n)` and `TDGAME.render()` draw exact current
state for the existing deterministic probes. `TDGAME.advanceFrame(seconds)`
exercises the actual accumulator/interpolation path while automatic RAF is
frozen. Achievement toast time now follows elapsed display time rather than
assuming every render takes 1/60 second.

Level 5 and Level 7 use the same close 640 by 480 viewport as the other large
stages. Mission initialization clears prior desert/Bastion state. Generic
alarm reinforcements can enter only from gates above the screen.

## Verification

- Native Chromium frontend probe: **41/41 passed**, including real mouse and
  controller pin selection, all six briefing launches, typed legacy code,
  invalid-code and Insanity gates, both controller Help schemes, narrow-window
  fit and completion rewards waiting for Level 7.
- Native Chromium pacing probe: **24/24 passed**, including 60/120/144/240 Hz,
  alternating frame intervals, 240 Hz quarter-step tank and camera movement,
  120 Hz boss/enemy/shot/Bastion interpolation, angle wrapping, state restoration
  after a render exception, freeze/pause, viewport and mission reset checks.
- Both probes completed with zero page, console or missing-asset errors.
  Menu, Help and native tank screenshots were visually inspected.
- Syntax and whitespace checks pass for the edited frontend and main modules.

These are simulated refresh intervals in real Chromium, not a hardware frame
rate or physical-controller claim. Full-game regression and the new combat
encounter probes are reported in the overall combat-overhaul verification.

Owners: `expansion/topdown/js/frontend_1011.js` and `js/main.js`.
Reproduce with `_research/probe_frontend_overhaul_1013.py` and
`_research/probe_pacing_1013.py` under `expansion/topdown`.
Portable results: `docs/qa/overdrive_frontend_overhaul_1013.json` and
`docs/qa/overdrive_pacing_1013.json`. Screenshots remain under ignored `_shots`.
