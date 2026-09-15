# Olive Warden Hard/Furious assault cycle — 2026-09-15

## Result

The Stage-4 Olive Warden now gains a complete difficulty-gated assault cycle on Hard and Furious while Normal retains the established spread, center-gun and rocket sequence.

The Hard/Furious cycle:

1. Accelerates the two mounted-turret spread and the dual straight center-gun flurry.
2. Continues from the rocket phase into a smooth full circular flight path while firing alternating authored side guns.
3. Glides horizontally across the arena while both center barrels fire rapid straight machine rounds.
4. Tracks the player through a shared green/yellow/red FOV warning, shakes and pulses late in the tell, then locks the lane before release.
5. Commits the complete upright boss plate vertically south at an accelerating ram speed.
6. Leaves the playfield and follows a continuous cubic side-return path to its station. The return is collision-safe so an off-screen plate cannot deal a hidden hit.

The first circular frame initially exposed a nearly 63-pixel position snap in the focused continuity measurement. The final implementation starts at the Warden's exact live radius and expands into the full orbit, and its warning tracker reaches the committed lane without a one-frame pull.

## Verification

- `node --check assets/game.js` and `git diff --check -- assets/game.js` pass.
- Focused suite section 321: **13/13** assertions pass for cadence, complete state order, continuous motion, lane commitment, collision safety, upright presentation and difficulty isolation.
- Full suite: **57 recorded failures**, exit 1. The 56 established baseline names remain, plus the known intermittent Stage-1 sand-tank spawn fixture on this run. Section 321 adds no failure.
- Real Chromium: **28/28**, zero page or console errors.
- Browser proof uses the native Stage-4 miniboss route, authored Warden hull and mounted ammunition, shared warning art, real `updatePlay` body collision and Normal/Hard/Furious isolation.
- Browser evidence: `docs/qa/olive_warden_hard_assault_0915.json`.
- Screenshots: `_shots/olive_warden_hard_assault_0915/warden_01_rapid_spread.png` through `warden_09_safe_curved_return.png`.
