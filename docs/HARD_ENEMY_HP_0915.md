# Hard enemy hull and shield health — September 15, 2026

## Implemented rule

Hard difficulty now applies the requested 15% ordinary-enemy hull bonus over Normal in both Campaign and Arcade. The older shared fodder value was 35%; it is now 1.15 at the single shots-to-kill scaling boundary.

Automatic enemy shield energy is calculated from the already-scaled hull. This gives shielded ordinary enemies the same Hard increase without a second multiplier or mode-specific branch. Bosses, minibosses and authored sectional encounters retain their existing `DIFF.eHp` and encounter-specific modifiers, including the separately tracked Stage-2 Hard boss request.

Easy, Normal and Furious ordinary-enemy multipliers are unchanged. Campaign and Arcade continue to share the same combat table; Arcade only clones it to apply its stock and continue rules.

## Verification

- Focused VM section 304f: 6/6 checks pass for the exact 1.15 multiplier, preserved Normal/Furious values, monotonic shots-to-kill, Campaign/Arcade parity, hull-derived shield energy and separate boss scaling.
- Real Chromium through `_BUILD_SOURCE/shoot.py`: three clean frames, zero enemy bullets, zero boss bullets, no page or console errors.
- Native pixel comparison uses the same authored Stage-5 frigate and void shield. Normal resolves to 12 hull / 4 shield; Hard resolves to 14 hull / 5 shield after integer combat quantization.
- Full suite: 3,904 checks pass and 56 recorded assertions fail; exit code 1. There are no new failure names compared with the preceding 57-name baseline. The intermittent Stage-1 sand-tank assertion passed in this run.
- Proof frame: `_shots/hard_enemy_hp_0915/native/shot_0001.png`.

