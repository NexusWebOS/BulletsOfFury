# Upgraded critical-enemy approach alert

Created with the built-in ImageGen tool. The first generation is emblem-source.png. Mike then requested the exact phrase "Warning: Critical Enemy Approaching!"; the selected second generation is critical-enemy-source.png. Full prompts: generation.json. Source alpha is preserved.

_BUILD_SOURCE/build_approach_alert_1024.py exports the selected source with one proportional nearest-neighbor scale onto768x640, pivot384,320. It writes assets/game/shared/ui/approach_alert_1024/critical_enemy.webp, its manifest and ART_TAXONOMY owner. No atlas repack or procedural replacement lettering. All displayed copy is generated into the matching metal plaque.

Live key alert_critical_1024 is preloaded by stageLoadBegin and used by drawApproachAlert for boss, miniboss and rival entrances. Existing alarm and countdown owners remain. Old generic warning title cards and radio overlays stay suppressed; latest user-requested copy is entirely inside this new art. Native QA: docs/qa/critical_enemy_alert_1024.json. Screenshots: _shots/critical_enemy_alert_1024. Required core suite still exits1 before assertions because retired_art_archive_1022.cjs is missing. No full-suite pass claimed.
