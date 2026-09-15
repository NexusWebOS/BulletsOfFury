# Frost Cruiser charged viewport sweep — 2026-09-15

## Result

The Stage-3 Frost Cruiser miniboss now owns a committed charged laser sweep built around a readable diagonal escape route.

The attack:

1. Samples which side of the arena the player occupies, then commits the sweep direction instead of tracking after the warning.
2. Charges for three seconds through the shared green/yellow/red field-of-view warning.
3. Darkens the arena progressively and draws the authored chain-lightning plates around the cruiser while eleven timed crackle cues build toward release.
4. Fires one dark-edged, white-cored beam from the nose and sweeps it monotonically across the complete viewport.
5. Uses a 52.5px visual and collision width, exactly 25% wider than the previous 42px beam.
6. Holds the sweep for a bounded 5.2 seconds, then disables the beam and returns to the normal recovery sequence.

The existing Jungle Cruiser timing and attack behavior remain unchanged.

## Verification

- `node --check assets/game.js` passes.
- Focused suite section 316: **11/11** assertions pass for the three-second warning, committed direction, one complete sweep, recovery, crackle cadence, audio, contact geometry, exact width and Jungle Cruiser isolation.
- Full suite: **4,071 passing / 57 failing**, exit 1. Every failure name matches the established baseline, including the intermittent Stage-1 sand-tank timing assertion on this run.
- Real Chromium: **16/16**, zero page or console errors.
- Browser measurements: start angle -0.780 radians, midpoint -0.008, end +0.752; collision width 52.5px; eleven crackle beats.
- Browser evidence: `docs/qa/frost_cruiser_sweep_0915.json`.
- Screenshots: `_shots/frost_cruiser_sweep_0915/frost_sweep_baseline.png`, `frost_sweep_charge.png`, `frost_sweep_red_warning.png`, `frost_sweep_start_right.png`, `frost_sweep_middle.png`, and `frost_sweep_end_left.png`.
