# PASSOVER 0825A — Chaos Harrier Stage 5 Replacement

## Result

- Stage 5's miniboss slot now spawns `CHAOS HARRIER` as a full replacement encounter.
- The complete source delivery is preserved under `_ART_SOURCES/CF_ChaosHarrierMiniBoss-Lvl5/`.
- Runtime PNG and JSON assets live under `assets/game/chaosharrier/`.
- `CF_EnemyTeleportFX-Vol.1 (1).zip` was not imported. It remains reserved for later Stage 8 enemy work.

## Runtime contract

- Held hover hull plus the six-frame internal glow reel for idle motion; no fake hover-frame wobble.
- Authored left/right bank hulls follow smooth flight curves and remain inside the live camera frame.
- Open red bays are the only missile launch points.
- Missiles use the delivered four-frame body/exhaust animation, fixed non-homing fan vectors, no generic smoke stack, and no detached lower-orb artifact.
- Side pods fire the delivered four-frame side-laser travel reel.
- The giant nose laser charges, locks its lane once, fires the delivered beam/impact art, and never tracks after warning.
- The Harrier uses its own delivered eight-frame warp for encounter movement.
- The separate Level 8 enemy-teleport families are intentionally not registered here.

## Verification

- `node --check assets/game.js` — pass.
- All delivered runtime JSON parses — pass.
- `git diff --check` — pass.
- Real Chromium captures exercised idle/bank, open-bay missiles, fixed nose beam, and warp exit/re-entry.
- Regression section 236 verifies the Stage 5 slot, art registrations, clean non-homing missile flags, camera-safe warp anchors, and Level 8 teleport isolation.
- The full legacy regression run retains seven pre-existing unrelated failures: stale Stage 6 master/scroll expectations, its preload threshold, missing historical `_superseded` ledgers, and stale cloud-stage palette expectations. This import adds no new failure after its asset-directory expectation is updated.
