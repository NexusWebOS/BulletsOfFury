# Stage 7 Warden toxic machine round — 2026-09-20

The Warden's 20-round hyper chaingun previously scaled the large toxic pressure shell to 30% and drew it smoothed. That left the attack visually soft and unlike a machine gun. The round now uses a dedicated 87×44 RGBA plate extracted without repainting or resampling from the first authored small-slug cell of `assets/game/combat_upgrade_0901/stage7_toxic_projectiles_atlas.png`. Its gold casing and green toxic tip match the existing Stage 7 projectile roster. The source remains unchanged; `_BUILD_SOURCE/extract_stage7_machine_round_0920.py` records the exact crop.

Only rounds marked `_s7Chain` use the new plate. The renderer keeps its native pixels, rotates the plate toward the round's actual velocity, and displays it at 34×17 world pixels. Other Warden pressure shells, mines, rails, collision sizes and attack timing remain as before.

`node --check assets/game.js` passed. `_BUILD_SOURCE/shoot.py` ran the real Stage 7 fight in Chromium with the hyper chaingun forced and captured 12 canvas frames in `_shots/stage7_chain_0920/`. The rounds visibly leave both cannon mouths with clear casings and green tips. No page or console errors were recorded. The full assertion-suite result is recorded in `_shots/stage7_chain_suite_0920.log`.
