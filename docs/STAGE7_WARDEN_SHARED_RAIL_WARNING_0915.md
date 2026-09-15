# Toxic Portal Warden shared rail warning — September 15, 2026

## Result

ENG-02 advances with the Stage 7 Toxic Portal Warden rail fan moved onto the shared non-laser boss warning rule.

- The Warden commits its aim and safe-side gap when the 0.86-second rail charge begins. It no longer samples the player on the release frame.
- Five shared FOV fields preview the five spear paths that will actually fire. The omitted outer pair remains a readable escape gap on the committed side.
- All five fields progress together through green, yellow and red, with one matching overhead alert.
- The lane fields render behind the authored boss plate while the alert renders in front. This keeps the giant hull readable and prevents it from covering the warning symbol.
- Player movement during yellow or red cannot rotate the fan or move its safe gap.

ENG-02 remains partial because additional dangerous non-laser boss and miniboss families still require review.

## Verification

- Focused suite section 335: **7/7** contracts pass for committed aim/gap, green/yellow/red timing, five-projectile release, exact launch angles and split shared-warning layers.
- The complete confirmation suite reaches its final summary with the exact established **57 failure names** and no new failures.
- Real Chromium through `_BUILD_SOURCE/stage7_warden_shared_rail_warning_0915/probe.py`: **15 passed / 0 failed**, with zero page, console or game-loop errors.
- Four native frames were pixel-reviewed. The first capture exposed an occluded alert; the renderer was split into behind-hull fields and an in-front alert, then the corrected green/yellow/red/release sequence was recaptured and reviewed.

Machine-readable Chromium evidence: [qa/stage7_warden_shared_rail_warning_0915.json](qa/stage7_warden_shared_rail_warning_0915.json).
