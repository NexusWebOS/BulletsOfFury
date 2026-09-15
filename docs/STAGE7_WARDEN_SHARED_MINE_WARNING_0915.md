# Toxic Portal Warden shared minefield warning — September 15, 2026

## Result

ENG-02 advances with the Stage 7 Toxic Portal Warden minefield moved onto the shared non-laser boss warning rule.

- The Warden commits one safe column when the 0.72-second charge begins. It no longer samples the player's position on the mine-release frame.
- Six shared FOV fields preview the six columns that will receive mines, leaving the committed seventh column visibly open.
- All six fields progress together through green, yellow and red, with one matching overhead alert.
- The lane fields render behind the authored boss plate while the alert renders in front, so the warning remains readable across the giant hull.
- Player movement during the warning cannot move the safe column. The six released mines inherit the exact previewed anchors.

ENG-02 remains partial because additional dangerous non-laser boss and miniboss families still require review.

## Verification

- Focused suite section 336: **7/7** contracts pass for safe-column commitment, green/yellow/red timing, six-mine release, exact preview/release anchors and split shared-warning layers.
- `node --check assets/game.js` and the focused test syntax check pass.
- The complete confirmation suite reaches its final summary with the exact established **57 failure names** and no new failures.
- Real Chromium through `_BUILD_SOURCE/stage7_warden_shared_mine_warning_0915/probe.py`: **16 passed / 0 failed**, with zero page, console or game-loop errors.
- Four native green/yellow/red/release frames were pixel-reviewed. The open lane remains readable while the warning changes phase, and all fields clear before the mines release.

Machine-readable Chromium evidence: [qa/stage7_warden_shared_mine_warning_0915.json](qa/stage7_warden_shared_mine_warning_0915.json).
