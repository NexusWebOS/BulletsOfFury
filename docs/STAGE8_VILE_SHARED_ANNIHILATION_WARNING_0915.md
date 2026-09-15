# Stage 8 Vile shared Annihilation warning — September 15, 2026

## Result

ENG-02 advances with Furious Death's Annihilation cross moved onto the shared non-laser boss warning rule.

- The final Vile Existence form commits the cross center when its 0.78-second Annihilation charge begins.
- Four shared FOV fields converge from the exact left, right, top and bottom release points onto the retained square target reticle.
- The four fields progress together through green, yellow and red with one matching overhead alert.
- The warning fields render behind the authored black-and-red boss plate while the alert renders in front.
- Late player movement cannot move the cross center. The first eight rounds launch from the four previewed sources on the exact committed paths.
- The existing three cross waves, radial follow-up, timing, projectile art and final-form silhouette remain unchanged.

ENG-02 remains partial because additional dangerous non-laser boss and miniboss families still require review.

## Verification

- Focused suite section 338: **7/7** contracts pass for target/source commitment, green/yellow/red timing, first-wave release, exact projectile paths and split shared-warning layers.
- `node --check assets/game.js` and the focused test syntax check pass.
- The complete suite reaches its final summary with **56 established failure names**, an exact subset of the 57-name baseline and no new failures.
- Real Chromium through `_BUILD_SOURCE/stage8_vile_shared_annihilation_warning_0915/probe.py`: **16 passed / 0 failed**, with zero page, console or game-loop errors.
- Four corrected native frames were pixel-reviewed. The first probe pass froze the startup hit flash; the corrected capture clears that expired flash and proves the authored final-form silhouette, converging fields, reticle, alert and eight-round release together.

Machine-readable Chromium evidence: [qa/stage8_vile_shared_annihilation_warning_0915.json](qa/stage8_vile_shared_annihilation_warning_0915.json).
