# Audio, weapon decals, and stage-exit pass — 2026-09-20

This is local working-tree work; no commit or push was requested in this turn.

## Done

- The ColeForge offline sample pipeline now builds 20 new, short MP3 cues from authored game recordings: nine element-combination hits, Thermoshock, fire wave/burst/geyser, shield destruction, three boss attack voices, and fire/ice/electric enemy projectiles. The originals remain untouched. Recipe and source layers: `_BUILD_SOURCE/sfx_coleforge_0920.py`; per-cue measurements: `qa/coleforge_sfx_0920.json`. All cues have an explicit gain and retrigger gate. The new files live in `assets/game/sounds/cf_*_0920.mp3`.
- Fire wave arrival, Stage-2 geyser eruption, player shield destruction, Thermoshock and Fire Orb impacts, Razorback pressure, Overlord lance, Warden laser, and the three enemy elemental bullet families now use the new cues. Elemental Forge impacts combine the underlying weapon's own shot voice with the new element hit; they do not all collapse to a single generic effect.
- All nine primary weapon slots now resolve to authored impact art through `weaponDecalKey` at the shared enemy-hit point. The impact tracks a live target briefly. Fire, ice, and lightning attacks without an infusion also emit their existing eight-frame authored element burst. No new placeholder or procedural sprite was added.
- Stage 2 and 4 boss tracks were the quietest pair relative to their stage music. New mastered copies, keeping the original songs, raise the first-20-second RMS from -15.7 to -13.7 dBFS and -15.5 to -13.0 dBFS respectively; decoded peaks remain below 0.95. The boss music player remains at the full user music level (1.0 in the probe). The pre-existing 0.28 pause reduction is preserved because Mike previously requested quiet paused music.
- The pilot can steer after a boss dies and during the stage-clear hover. The fly-off takes control at the first climb frame, using the pilot's final position.

## Verification

- `node --check assets/game.js` and `git diff --check` passed.
- `_BUILD_SOURCE/test_fl.js` reached its final summary and exited nonzero with the exact incoming 76 failing assertion names. A repeat briefly had 75 because the known intermittent Stage-1 sand-tank spawn fixture passed. No new failing name was added.
- Real Chromium probe: `_BUILD_SOURCE/probe_audio_exit_0920.py`, report and inspected screenshots in `_shots/qa_0920_audio/`. It checked all 20 audio handles and TAME rows, six actual sample playbacks reaching decoded playing time, nine weapon decal mappings and pixels, live movement after boss defeat, hover steering, frozen X during climb, full boss-track volume, and zero page/console errors.

## Still open

The project's ElevenLabs generator is `_BUILD_SOURCE/sfx_gen.py`, and `_BUILD_SOURCE/sfx/boss_cues_0919.json` already queues three additional boss sounds. `_BUILD_SOURCE/.secrets.json` is absent, so no ElevenLabs request could run in this pass. Its instructions require `elevenlabs_api_key` in that ignored local file. The authored source-remix cues above are playable now; a separate ElevenLabs pass and listening review of the full miniboss/boss roster remain open. All nine original boss signature sounds still exist for the attacks not replaced here.
