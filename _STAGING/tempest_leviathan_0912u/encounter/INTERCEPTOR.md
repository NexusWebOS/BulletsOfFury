# Integrated-cannon interceptor

Run `node serve.cjs` and open http://127.0.0.1:8783/. This remains a separate encounter; no files in the BulletsOfFury game were modified.

The new ship has two built-in laser housings, each with front and rear apertures. Nose orientation is fixed upward throughout combat and destruction. Its 108×118 draw size is about twice the 48×59 player. Both ships cast offset silhouette shadows. White damage flashes, separate damaged art, and attached smoke/fire/explosion effects remain. Each of four apertures has 300 HP and independently loses its firing ability when destroyed.

All boss movement changes either X or Y in a simulation step, never both. It does not yaw, rotate, flip, or use diagonal approaches.

- 100–75%: fast horizontal strafes with rear plasma bolts, warned twin rear laser lanes, and vertical dive/climb attacks.
- 75–50%: the boss tracks beneath the player at 560 px/s, drives forward behind twin lasers, then makes three successive side rams. It positions at a random left/right edge, matches a captured player row vertically, warns for 0.4 seconds, and rams horizontally at 1,200 px/s. A short vertical recovery puts it above the player for a one-second counterattack opportunity; its rear lasers still threaten during that window.
- 50–25%: faster rear assault, shorter beam warnings, faster bolts, and generated needle missiles.
- 25–0%: false crash, then 660 px/s pursuit, 0.35-second beam warning, four consecutive 1,450 px/s rams, 0.28-second ram warning, and 0.72-second counterattack windows.
- 0%: the existing falling reactor explosion and bottom-to-top cinematic escape.

Normal flight speed is 480 px/s, pointer movement 540 px/s. Laser hits deal 20 armor, rams 32, plasma bolts 10. Post-hit immunity lasts 0.48 seconds. Beam telegraphs are harmless; active beam damage uses the visible vertical segment and its width. Attack warnings stop tracking before the damaging portion, so a committed dodge can clear the lane. Health thresholds cannot be skipped.

Practice prevents player damage. Showcase automates flight and eventually adds damage to show all phases; it is not evidence of human difficulty balance. Live play uses actual shot/collision damage. Fire continues throughout combat, including pursuit; get below the boss between passes to land upward shots.

## Generated assets

Built-in ImageGen produced the new intact/damaged ship atlas with integrated dual-ended laser housings, plus a separate laser beam, plasma bolt, charge corona, and needle missile atlas. Original outputs are retained in `sources/interceptor-v2.png` and `sources/interceptor-projectiles.png`; the prompt briefs are in `sources/interceptor-prompts.json`. Extraction is recorded in `interceptor-assets.ps1`; pivots and asset hashes are in `manifest.json`. Existing local BulletsOfFury laser/weapon/explosion sounds and explosion frames are reused.

The earlier standalone turret and ship files are retained as source history but are no longer rendered. `engine.js` is the live simulation; `game.js` renders it. `engine-v3.js` is the initial revision snapshot, not the live entry point. Run `node interceptor-test.cjs` (also available through `test.cjs`) for axis-only movement, fixed orientation, both flank choices, repeated high-speed rams, anchored beams, damage/telegraph separation, disabled apertures, health gates, and full victory runs.
