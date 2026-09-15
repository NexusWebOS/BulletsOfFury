# Sovereign helper spider walk — September 15, 2026

## Result

S4-13 is complete. During the Hard/Furious red side-stream phase, continued generator damage now makes the surviving helpers perform a bounded vertical response:

- The next live generator hit arms one synchronized walk without resetting on every damage tick.
- Hard rises at most 58 pixels; Furious rises at most 72 pixels.
- The pair moves upward slowly, reverses, and returns to its original side row. Another valid hit can restart the response after it finishes.
- Both helpers stay inside their edge stations throughout the motion, preserving the edge-hugging route.
- Their staggered projectile lanes and repeated pause windows continue while the row moves, so the player can follow upward and then back without the streams collapsing into one wall.
- Hitting a different live generator during the enrage is recognized correctly. Normal remains unchanged.

## Verification

- `node --check assets/game.js` and the CRLF suite file pass.
- Focused suite section 327: **9/9** assertions pass for new-node recognition, Hard/Furious bounds, edge retention, upward/reverse motion, baseline return, retriggering, stream-gap retention, and Normal isolation.
- The complete suite reached its final summary with **56 established failure names, no new failures**, and only the known timing-sensitive `stage 1: the sand tanks spawn (scroll never)` assertion absent from the 57-name reference run.
- Real Chromium through `_BUILD_SOURCE/sovereign_helper_spider_walk_0915/probe.py`: **13 passed / 0 failed**, with zero page or console errors.
- Two native frames were pixel-reviewed at the upward bound and on the return leg.

Machine-readable Chromium evidence: [qa/sovereign_helper_spider_walk_0915.json](qa/sovereign_helper_spider_walk_0915.json).
