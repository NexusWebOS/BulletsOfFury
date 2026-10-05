# Stage 6–8 white hit frames and stealth fighter paint — October 4

## What changed

- Restored the Stage 6 red and green stealth fighter sheets to the bomber renderer. A late gameplay override had been drawing recolored Harrier boss art instead. The four directional fighter cells now come from the authored blue fighter family, and the existing flight warnings and attacks remain in place.
- Made hit flashes use white copies of the exact authored cell or modular part being drawn. This covers Stage 6 ordinary enemies, the Siege Bomber, Warhive and Rebels; Stage 7 ordinary enemies and Warden; and Stage 8 ordinary enemies, new aliens, Herald and the finale forms. The shared Stage 8 fleet atlas had no flash draw at all, which explained most of the remaining misses.
- Increased the late boss hit duration from 0.045 to 0.12 seconds and removed the finale renderer's extra flash suppression. Damage throttling still prevents sustained allied fire from pinning a boss white. The Rebel direct-damage path now gives each ship a visible 0.12-second flash.
- Kept modular components independent: a damaged Siege Bomber body can flash while its weapon modules retain their own art; a directly hit module flashes at its own pose. White frames are cached tints of approved art, not new silhouettes or placeholder sprites.

## Verification

- `node --check assets/game.js` and all touched modules: pass. `assets/game.js` retains LF line endings.
- `node _BUILD_SOURCE/test_fl.js`: 7,053 assertions, zero errors, exit 0.
- `_BUILD_SOURCE/probe_flash_palette_1004.py`: 47/47 Chromium pixel checks pass across Stage 6–8, including real `hitEnemy` damage on one unit in each stage; zero page or console errors. The review page is `_shots/flash_palette_1004/review.html`.
- Existing `_BUILD_SOURCE/probe_stealth_1002.py`: pass for red, green, orange, all entry headings and direct bomber/strike conversion; zero page errors. The red Retina missiles, green atom bomb and orange machine-gun attacks still release.
- Pixel audit of the first three directional cells against `assets/game/mission_repair_0929/bluejets.png`: each red and green sheet changes exactly 3,624 blue-paint pixels; 8,441 opaque non-paint pixels and all alpha values stay identical. No paint-pixel mismatches against the original hue-rotation rule.

Evidence: `_shots/flash_palette_1004/flash_probe.json`, `palette_audit.json`, `stealth_probe.txt`, and `suite_final.txt`. These are controlled encounter and source-pixel checks, not a full campaign clear. The workspace remains local and uncommitted; prior work was preserved.
