# Frost Cruiser Furious volley-charge combo — 2026-09-15

## Result

The Stage-3 Frost Cruiser's first Furious enrage attack now joins its Retina rocket pressure to a committed body charge.

The combo:

1. Reuses the Hard/Furious six-rocket sequence: one Retina, six delayed releases, alternating physical launch pods and independent spiral paths.
2. Opens the shared green/yellow/red attack FOV after the last rocket release.
3. Tracks the player's lane through most of its 1.20-second warning, then commits at 0.86 seconds and leaves a final 0.34-second dodge window.
4. Rotates the complete authored cruiser into its committed travel vector and charges at 760 pixels per second.
5. Remains a dangerous physical hull during the dash. A player who stays in the lane takes a real sub-boss body hit; moving after commitment clears it.
6. Flies fully off screen, becomes collision-safe for its 260-pixel-per-second return from above, and restores the encounter through the existing recovery state.

The attack runs once on the first Furious below-25-percent enrage transition. Hard retains its established rage-missile route, and the later Furious cycle keeps the existing rage patterns.

## Verification

- `node --check assets/game.js` passes.
- Focused suite section 318: **10/10** assertions pass for enrage routing, combo ownership, late commitment, dash vector, collision, offscreen return, bounded recovery and difficulty isolation.
- Full suite: **4,096 passing / 57 failing**, exit 1. Every failure name matches the established baseline, including the intermittent Stage-1 sand-tank timing assertion on this run.
- Real Chromium: **16/16**, zero page or console errors.
- The browser proof runs the native Stage-3 miniboss route, shared Retina scheduler, real update loop, real hull collision, authored renderer and the existing recovery controller.
- Browser evidence: `docs/qa/frost_cruiser_furious_charge_0915.json`.
- Screenshots: `_shots/frost_cruiser_furious_charge_0915/frost_fury_spiral_combo.png`, `frost_fury_tracking_warning.png`, `frost_fury_late_lock.png`, `frost_fury_committed_dash.png`, and `frost_fury_offscreen_return.png`.

