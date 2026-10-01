# Spreadfire animation source — October 1, 2026

Generated here with the built-in image generator, with native transparency. No SpriteCook. The original output is preserved as `spread.png` (793 × 1983 RGBA).

Generation brief: production pixel-art animation sheet for Bullets of Fury, four columns and ten rows; one isolated upward-travelling Spreadfire projectile per cell at a consistent pivot, four animated frames per row. Crisp shaded 16-bit pixels with dark contours and luminous cores, no text, ship, hands, borders or background. Rows: golden base slug, orange/red Fire comet, blue Ice crystal, yellow Lightning pellet, orange/steel Kinetic slug, silver/cyan Chromium shard, purple/black Dark pellet, green Toxic droplet, multicolor Prism crystal, turquoise Water droplet. Projectiles travel upward with trails below. These are projectile loops, not muzzle flares or multiple-shot fans.

The generator did not obey a uniform row grid. `_BUILD_SOURCE/build_spread_1001.py` uses measured transparent gutters for all ten rows and a common bounding box across each row's four cells, preserving native alpha and image pixels. The importer creates the ten separate runtime reels and their source-rectangle metadata together. Original PNG is unchanged. No generated atlas was edited.

Runtime registration: `assets/spread_art_1001.js`, `assets/spread_1001.js`, `assets/game/encounters_1001/manifest.json`. The manifest records the source hash and measured row bands. Native game-context draw evidence: `_shots/encounter_feedback_1001/spread-all.png`. Forty frames inspected for cross-cell bleed and clipped outlines; all ten reels decoded in Chromium.
