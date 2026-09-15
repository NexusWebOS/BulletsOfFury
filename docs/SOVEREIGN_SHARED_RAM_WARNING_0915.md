# Sovereign shared ram warning — September 15, 2026

## Result

ENG-02 advances with the Stage 4 Storm Sovereign’s unpowered body ram moved onto the shared non-laser boss warning rule.

- The live attack now uses `combatWarningTick` and `combatWarningDraw` for one continuous green, yellow and red field with the matching authored overhead alert.
- The field follows the player during the original 0.40-second aiming window, then holds one committed lane through yellow and red before the dive.
- Release remains at one second. The complete offscreen exit, overhead hull/shadow pass and opposite-edge return remain unchanged.
- The shared warning API now accepts an optional alert anchor. Stage 4 places its sign just below the encounter’s dual boss/shield gauges, preventing either gauge from hiding it.
- Other warning users retain their existing automatic above-unit placement.

ENG-02 remains partial because other dangerous non-laser boss and miniboss families still need review.

## Verification

- Focused suite section 332: **8/8** live and structural contracts pass for shield gating, attack start, green/yellow/red timing, lane commitment, release and shared helper ownership.
- The complete suite reaches its final summary with **56 established failure names** and no new failures; the known intermittent Stage 1 road-tank heading assertion passed on this run.
- Real Chromium through `_BUILD_SOURCE/sovereign_shared_ram_warning_0915/probe.py`: **14 passed / 0 failed**, with zero page or console errors.
- Four pixel-reviewed native frames confirm the unobscured green/yellow/red signs below the two gauges, the cone’s committed lane and the first dive frame after warning closure.

Machine-readable Chromium evidence: [qa/sovereign_shared_ram_warning_0915.json](qa/sovereign_shared_ram_warning_0915.json).
