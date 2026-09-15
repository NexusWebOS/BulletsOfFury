# Chrome Hammer shared leap warning — September 15, 2026

## Result

ENG-02 advances with the Chrome Hammer leap/slam moved onto the shared non-laser boss warning rule.

- The 1.2-second windup now projects the authored green, yellow and red FOV field from the Hammer to its committed impact point, with the matching overhead alert above the boss.
- The original landing reticle remains at the exact impact point and changes through the same three phases.
- The target is sampled once when the warning begins. Player movement during yellow or red cannot redirect the leap.
- The warning and reticle disappear when the leap releases, leaving the impact path readable without hiding the active attack.
- The completed one-hand boomerang remains unchanged: 1.55-second accelerating spin, 0.70-second outbound throw and 315-pixel-per-second magnetic return.

ENG-02 remains partial because additional dangerous non-laser boss and miniboss families still require review.

## Verification

- Focused suite section 334: **7/7** contracts pass for green/yellow/red timing, committed targeting, release, shared helper ownership, retained reticle and boomerang preservation.
- The complete suite reaches its final summary with **56 existing failure names**, all a subset of the established 57-name baseline, and no new failures.
- Real Chromium through `_BUILD_SOURCE/hammer_shared_leap_warning_0915/probe.py`: **16 passed / 0 failed**, with zero page, console or game-loop errors.
- Four pixel-reviewed frames confirm the full Hammer, unobscured matching alerts, the committed landing reticle, readable green/yellow/red corridor progression and warning removal on release.

Machine-readable Chromium evidence: [qa/hammer_shared_leap_warning_0915.json](qa/hammer_shared_leap_warning_0915.json).
