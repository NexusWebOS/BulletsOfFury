# Fresh regular-wave films / layered stages — November 2, 2026

All nine regular stages and both Stage6 routes were re-recorded from the current local game after LS112 scenery integration. These are new real-time in-engine films, not replacement backgrounds composited into old videos.

Local review: http://127.0.0.1:63094/review/current/all-waves-1101.html?layers=1102 . The1102 alias opens the same new set. Familiar level/wave hash routes remain available.

## Coverage

Ten H.264/AAC films retain260 unique authored schedule entries and313 selectable wave chapters, native warnings/AI/health/audio and18s combat tails. Chapters overlap when original formations overlap. Both Stage6 route choices complete all four native carrier assaults. Bosses/minibosses and endless adaptive reinforcements remain suppressed only by the established QA fixture; StageX is boss-only and excluded.

The observer is visibly labelled invulnerable and supplies native movement/fire/Retina/missile inputs. No enemy HP, phase, attack timer or callback is synthesized. Native simulation and scenery share the same delta. All retained films have zero sampled pilot deaths or active bosses/minibosses.

Stages2–9 render their actual new terrain and separate animated material beds. Stage4 includes the powered Tesla overlay. Stage1 retains its approved original scenery. Runtime and asset hashes accompany each take, with real LS112 blit counters and material-frame samples.

| Film | Chapters | Seconds | Native render FPS |
| --- | ---: | ---: | ---: |
| stage-1 | 36 | 100.8 | 46.49 |
| stage-2 | 25 | 63.77 | 57.46 |
| stage-3 | 20 | 65.71 | 58.64 |
| stage-4 | 22 | 68.0 | 57.58 |
| stage-5 | 14 | 72.79 | 55.67 |
| stage-6 | 53 | 209.83 | 47.71 |
| stage-6-right | 53 | 211.93 | 45.55 |
| stage-7 | 22 | 214.63 | 13.54 |
| stage-8 | 30 | 80.47 | 43.51 |
| stage-9 | 38 | 77.34 | 37.41 |

Total duration: 1165.27 seconds. All movies fully decode; audio has nonzero RMS and unclipped peaks. Chromium verifies30 decoded first/middle/last chapter seeks across ten films, previous/full controls, rapid route switching,390px layout and zero browser errors. Native captures and decoded page views were visually inspected. Render FPS measures this capture host, not a console target or general performance guarantee.

## Reproduction and preservation

- _BUILD_SOURCE/record_layered_waves_1102.py reuses wave_review_1101.js and the established audio/canvas recorder. Explicit stage arguments (including6r) permit scoped retries; verified same-source takes are preserved. Persistent local HTTP connections and a large accept queue avoid Windows preload connection refusals. Expected aborted media-pool requests are separate from actual loading errors. Later captures disable only optional leaderboard configuration and use a lighter VP8 recording encoder; native gameplay/art/audio remain unchanged.
- _BUILD_SOURCE/publish_layered_waves_1102.py decodes films/audio, rebuilds thumbnails and timestamps, checks all scheduled indices and live layer evidence, then installs the complete collection.
- _BUILD_SOURCE/probe_layered_waves_1102.py checks actual browser playback and decoded pixels.
- Raw footage, reports, exact fixture copies, previews and receipts remain under ignored _shots/waves_layers_1102/. Failed setup takes are preserved and excluded.
- Downloaded original movies remain untouched; prior page/data are backed up in the task folder. New movies/posters live under the existing server's review/current/waves-layers-1102/. Data installs atomically after every movie verifies.

No production gameplay or scenery script changed for recording. Core game.js, full-suite fixture and every prior local status entry are preserved. The last required full-suite run retains its known difficultyHealthBaseline15 harness load-order blocker; this media-only task does not change it. No commit or GitHub upload was requested or performed. Machine-readable receipt: docs/qa/waves_layered_1102.json.
