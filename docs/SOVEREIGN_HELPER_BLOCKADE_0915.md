# Sovereign Hard/Furious helper blockade — September 15, 2026

## Result

S4-11 is complete. The Storm Sovereign's two authored chaingun helpers now receive a difficulty profile on Hard and Furious:

- Each helper shield has exactly 50 percent more capacity. Hull health and Normal behavior are unchanged.
- Windup, turret turning, straight-stream cadence, diagonal-burst cadence, and projectile speed increase on Hard and increase again on Furious.
- Once both helpers have materialized, they periodically advance from their generator positions into a forward horizontal row.
- The row tracks the active player across the safe camera range, holds long enough to deny a static firing lane, then withdraws to the generators.
- The formation keeps a center gap and camera-edge clearance. It uses the existing authored helper hull, rotating barrel, projectile, shield, and generator art.

The row is difficulty-only. Normal helpers stay at their original positions and keep their existing shield and attack values. The later generator-hit enrage and side-stream behavior remains tracked separately as S4-12 and S4-13.

## Verification

- `node --check assets/game.js` and the CRLF suite file pass.
- Focused suite section 325: **14/14** assertions pass for Normal isolation, shield scaling, advance/hold/retreat states, player tracking, row spacing, and progressive Hard/Furious attack speed.
- The complete suite reaches its final summary with the exact established **57 failure names** and no new failures.
- Real Chromium through `_BUILD_SOURCE/sovereign_helper_blockade_0915/probe.py`: **17 passed / 0 failed**, with zero page or console errors.
- Three native gameplay frames were pixel-reviewed: Normal home positions, the Hard forward row, and the row tracking toward the right edge.

Machine-readable Chromium evidence: [qa/sovereign_helper_blockade_0915.json](qa/sovereign_helper_blockade_0915.json).
