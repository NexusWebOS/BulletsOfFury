# Music integration — 2026-09-25

Mike's six supplied WAVs are preserved byte-for-byte in `assets/game/music/originals_0925/`. Browser-ready 44.1 kHz stereo, 160 kb/s MP3 copies are in the parent music folder. The originals on the Desktop remain untouched.

| Supplied track | Live assignment | MP3 |
|---|---|---|
| Over The Horizon | Stage 7 field music | `stage7_over_the_horizon_0925.mp3` |
| final boss - phase 1 | Stage 8 final boss, first musical phase | `final_boss_phase1_0925.mp3` |
| The Final Confrontation | Stage 8 final boss, third and final musical phase | `final_boss_phase3_the_final_confrontation_0925.mp3` |
| Final Level | Campaign ending cinematic/victory | `cinematic_final_level_0925.mp3` |
| unknownbosstheme | Stored for boss assignment review | `unknownbosstheme_0925.mp3` |
| ratchetman | Stored for boss assignment review | `ratchetman_0925.mp3` |

Stage 8 remains the campaign finale; Stage 9 is the optional Velocity Void bonus stage in the current game. Stage 8 phase 2 currently retains its phase-1 track until a distinct phase-2 decision. The unassigned files are not presented as active tracks.

Retired files were renamed in-place with a numbered `unusedN - prior role.mp3` pattern; no audio was deleted. The archive includes the old Stage 7 field score, old Stage 8 phase tracks, prior Stage 1–5 boss scores, and alternate mixes. Runtime BOFA.music aliases are redirected to real files. `assets/manifest.js` is generated, so live remaps remain code-owned in `assets/game.js`.
