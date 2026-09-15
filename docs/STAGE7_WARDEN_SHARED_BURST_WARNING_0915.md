# Toxic Portal Warden shared cannon-burst warning — September 15, 2026

## Result

ENG-02 advances with the Stage 7 Toxic Portal Warden's ten-round cannon burst moved onto the shared non-laser boss warning rule.

- The Warden commits its aim when the 0.48-second cannon charge begins. Late movement cannot steer the burst.
- Five shared FOV fields preview the five narrow firing lanes used twice across the alternating left/right cannons.
- The fields progress through green, yellow and red with one matching overhead alert.
- The fields render behind the authored boss plate while the alert renders in front, preserving the giant hull and warning symbol.
- The original ten-round cadence, 0.105-second spacing, two physical cannon origins, toxic shell art and movement remain unchanged.
- Both direct cinematic entries into the burst now arm the same committed aim and warning, preventing the opening and post-stun volleys from bypassing the rule.

ENG-02 remains partial because additional dangerous non-laser boss and miniboss families still require review.

## Verification

- Focused suite section 337: **7/7** contracts pass for committed aim, green/yellow/red timing, first release after the tell, exact ten-round/five-angle pattern, and split shared-warning layers.
- `node --check assets/game.js` and the focused test syntax check pass.
- The complete suite reaches its final summary with the exact established **57 failure names** and no new failures.
- Real Chromium through `_BUILD_SOURCE/stage7_warden_shared_burst_warning_0915/probe.py`: **16 passed / 0 failed**, with zero page, console or game-loop errors.
- Four native frames were pixel-reviewed. Real `updatePlay` stepping separates the barrage in flight; the boss records all ten shots while the leading shell exits the arena normally and nine remain visible in the release frame.

Machine-readable Chromium evidence: [qa/stage7_warden_shared_burst_warning_0915.json](qa/stage7_warden_shared_burst_warning_0915.json).
