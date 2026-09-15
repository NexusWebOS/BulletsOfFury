# Razorback shared ram warning — September 15, 2026

## Result

ENG-02 advances with the Razorback body ram moved onto the shared non-laser boss warning rule.

- The former yellow guide line is replaced by the authored green, yellow and red FOV field and matching overhead alert.
- The tank samples the player during the green third, commits when yellow begins and retains that lane through red and release. A late dodge cannot pull the ram back onto the player.
- Normal, each independent Hard Razorback and the 150% Furious hyper tank use the same timing rule while preserving their own camera-safe movement limits and speed multipliers.
- Starting another attack clears the committed-ram latch. Hard actors continue to keep their own target lanes.
- The existing one-second windup, ram launch sound, southbound thrust and recovery timing remain intact.

ENG-02 remains partial because additional dangerous non-laser boss and miniboss families still require review.

## Verification

- Focused suite section 333: **9/9** contracts pass for green/yellow/red timing, lane commitment, release, reset, Hard pair limits, Furious support and shared helper ownership.
- The complete suite reaches its final summary with the exact established **57 failure names** and no new failures.
- Real Chromium through `_BUILD_SOURCE/razorback_shared_ram_warning_0915/probe.py`: **15 passed / 0 failed**, with zero page, console or game-loop errors.
- Four pixel-reviewed Furious frames confirm the full giant tank, unobscured matching alerts, green/yellow/red field progression and warning removal on release.

Machine-readable Chromium evidence: [qa/razorback_shared_ram_warning_0915.json](qa/razorback_shared_ram_warning_0915.json).
