# Stage 2 Hard encounter HP and fire absorption — September 15, 2026

## Corrected encounter floor

Hard now gives the Stage-2 miniboss and boss exactly 25% more final encounter health than Normal. The raw difficulty table already appeared to encode that ratio, but the encounter-floor clamp converted Normal's 0.88 to 1.00 while leaving Hard at 1.10. Because the Stage-2 floor dominates these builds, the live fights only gained about 10%.

`encounterFloorDifficultyMul` now owns the exception at the shared boss/miniboss floor boundary: Stage 2 Hard returns 1.25. Other stages retain their current multiplier, and Stage 2 Furious remains 1.30. Internal part pools continue to scale through `enforceEncounterHp` with the public gauge.

The existing elemental boundary already identifies every Stage-2 boss and miniboss as fire-aligned. Same-element fire attacks retain exactly half damage and show the throttled `FIRE DMG ABSORBED!` popup. Opposing ice damage keeps its existing 2x rule.

## Verification

- Focused VM section 304h: 6/6 checks pass for the exact floor, live Furnace Tyrant and Magma Ward ratios, 50% fire retention on both roles and preserved Furious scaling.
- Real Chromium through `_BUILD_SOURCE/shoot.py`: the authored Furnace Tyrant and flame shield render at Hard 3,236 HP versus Normal 2,589 HP; the actual fire-absorption popup is visible. No enemy bullets, boss bullets, page errors or console errors.
- Full suite: 3,916 checks pass and 56 recorded assertions fail; exit code 1. There are no new failure names against the preceding 57-name baseline; the intermittent Stage-1 sand-tank assertion passed in this run.
- Proof frame: `_shots/stage2_hard_encounters_0915/native/shot_0001.png`.

