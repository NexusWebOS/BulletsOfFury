# Sovereign Furious giant lightning strike — September 15, 2026

## Result

S4-15 is complete. After the Furious chain-lightning volley, the Storm Sovereign now holds center and charges a giant vertical lightning field for exactly five seconds of real time.

- The warning uses the shared authored FOV system in yellow, then red. It never shows the safe green state because this is one continuous committed attack.
- The matching authored alert emblem flashes visibly on the boss's upper hull, clear of the two Stage 4 boss gauges.
- The arena darkens while the core grows through the authored lightning-ball and chain-lightning frames. The final charge beat flashes red rather than using the engine's white flash.
- Release fills the center 66% of the camera with seven animated authored lightning columns and a reinforced core column.
- The outer 17% on both sides remains safe through release. Collision follows those same measured camera bounds and can hit each co-op seat only once.
- Helper turrets and final chainguns pause for the five-second warning and strike, preserving the announced escape lanes.
- Normal and Hard retain their existing transition from chain lightning back to burst fire.

## Verification

- `node --check assets/game.js`, Python probe compilation, and the CRLF-aware diff check pass.
- Focused suite section 329: **13/13** assertions pass for difficulty isolation, start/finish routing, exact charge time, yellow/red phases, corner safety, central collision, gun suspension, authored art, and red-only screen treatment.
- The complete suite reaches its final summary with the exact established **57 failure names** and no new failures.
- Real Chromium through `_BUILD_SOURCE/sovereign_giant_strike_0915/probe.py`: **15 passed / 0 failed**, with zero page or console errors.
- Pixel-reviewed native frames confirm the yellow and red warnings, full visible alert emblem, darkened charge, crackling core, central lightning wall, and two clear bottom-corner lanes.

Machine-readable Chromium evidence: [qa/sovereign_giant_strike_0915.json](qa/sovereign_giant_strike_0915.json).
