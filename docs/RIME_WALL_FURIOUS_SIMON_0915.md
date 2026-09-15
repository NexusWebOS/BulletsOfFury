# Rime Wall Furious Simon-Says cannon feints — 2026-09-15

## Result

The Furious Stage-3 Rime Wall now replaces its normal three-second green/yellow/red cannon warning with a fast five-beat Simon-Says sequence.

The attack:

1. Alternates the existing authored FOV cone between both physical side cannons.
2. Shows exactly yellow, red, yellow, red and a final rapidly flashing red commitment lane. Furious never shows green.
3. Removes the overhead warning/asterisk only for this Furious sequence. The side-cannon cones remain the complete readable tell.
4. Fires only the cannon identified by the final red flash.
5. Locks the committed angle before release. Moving after the final cue does not make the beam chase the player.
6. Uses the existing dark-edged blue Rime laser and its real player collision boundary.
7. Keeps Hard and Normal on their established three-color warning.

The same live-router correction wires the S3-11 Retina laser-ball pair into the actual below-half `s3wallhalo` and `s3walloverdrive` selector. Its earlier helper-level proof was valid, but the original calls were in historical phase blocks below the live beam router and could not run during natural combat. The new Chromium proof enters through `shipBossAttack`, sees one Retina with both delayed releases, and verifies that Hard receives the pair while Normal does not.

## Verification

- `node --check assets/game.js` and `git diff --check -- assets/game.js` pass.
- Focused suite section 320: **13/13** assertions pass for the live route, exact colors, timing, both-mount sequencing, final-lane release, fixed aim, overhead-symbol suppression and difficulty isolation.
- Full suite: **4,122 passing / 56 failing**, exit 1. Every failing assertion name belongs to the established baseline; the intermittent Stage-1 sand-tank timing assertion passed on this run.
- Real Chromium: **21/21**, zero page or console errors.
- Browser proof uses the native Stage-3 boss route, the real `shipBossAttack` selector, shared Retina scheduler, authored FOV/beam/orb art, real beam collision and Hard/Normal isolation.
- Browser evidence: `docs/qa/rime_furious_simon_0915.json`.
- Screenshots: `_shots/rime_furious_simon_0915/fury_simon_01_yellow.png` through `fury_simon_06_committed_beam.png`.
