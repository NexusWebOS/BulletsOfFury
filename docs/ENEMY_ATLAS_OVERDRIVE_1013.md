# Overdrive native enemy atlas adapter — 2026-10-13

The enemy guide runs the actual Overdrive mission renderer, unit controllers, modular bosses, and projectile renderer in its reused preview iframe. Its 32 Overdrive dossiers cover 21 units, five boss controllers, three Exhibit forms, and three individual Machinists.

`expansion/topdown/index.html` loads the shared save/clock guard before game code and `assets/enemy_atlas_overdrive_1013.js` after game code only for the exact `enemyAtlas=1` query. Normal play loads neither adapter nor guard. The native mission is reset for each selection; unrelated combatants and automatic reinforcements are suppressed. The camera frames the current opponent and protected observation target. Convoy specimens use their exclusive chase owner rather than generic ground-unit behavior.

The public `BOF_ENEMY_ATLAS` bridge supports start, snapshot, pause, speed, single-frame step, mute, health adjustment, target repositioning, real projectile drawings, and actual registered artwork. Boss phases evolve through their native state machines. Exhibit form previews use native module destruction to enter their selected form. Preview progress and achievements are ephemeral through the shared storage guard.

## Validation

- 139/139 native checks passed in Chrome: all 32 spawns and animations; actual firing from every armed unit; native modular forms; isolated, protected target; all four difficulties; playback and health controls; pixel output; storage guard; and the absence of guide hooks on the normal game page.
- 5/5 parent-guide UI smoke checks passed: native Overdrive iframe, pause, playback speed, difficulty control, and no browser errors.
- Zero JavaScript page or console errors in both runs. Parent task owns the separate Edge/Firefox/Chrome full-guide compatibility audit.
- Visual review covered Warrior, Gosfer, Machinists, Exhibit form 3, Jackal, the elite assault robot, and convoy jet. The full-guide screenshot is `_shots/enemy_atlas_1013/overdrive/guide-warrior.png`.

Reproducible exhaustive probe: `_BUILD_SOURCE/probe_enemy_atlas_overdrive_1013.py`. Machine-readable record: `docs/qa/enemy_atlas_overdrive_1013.json`.
