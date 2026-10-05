# October 3 music organization

Mike assigned unused3 to the Level 8 second boss form, unused4 to the Level 9 miniboss, unused7 to the Level 6 miniboss, unused9 to the Level 4 miniboss, and unused13 to the Level 7 miniboss.

All 51 game music files now live in assets/game/music, named LevelN, LevelNmb, LevelNb, Level8b2/Level8b3, or descriptive menu/special/archive names. Three HAMA vocal revisions were moved from the vocal asset directory; cue data stays there. Original audio bytes and historical provenance are preserved. catalog.json retains SHA-256 hashes, former paths and runtime routes; README.md is the readable file index.

organize_music_1003.py owns the music-only manifest regeneration and updates executable runtime/build/probe paths while preserving source line endings. The former 0925 music owner delegates to it. HAMA builders now write into the shared music folder. Newly assigned tracks no longer have unused aliases.

Native Chromium verifies all 51 files exist, the four actual miniboss warning gates select their new tracks, the actual second-form transition selects boss8p2, and the third form selects boss8p3. Five assigned MP3s decode; no page or console errors. Reproduction: python _BUILD_SOURCE/probe_music_1003.py. Portable evidence: docs/qa/music_1003.json.

Herald continues sharing Level8b, and finale forms 3Ã¢â‚¬â€œ8 continue sharing Level8b3. Other assignments remain intact. This is local work without a commit or push.

The first full-suite run exited 1 with nine failures: seven exposed two legacy non-music manifest aliases pointing to the renamed MP3 paths; the other two expected old Opening/HAMA filenames. The owning workflow updates those aliases and the filename checks now match the organized files. Final suite outcome is recorded below.

Final validation: node syntax check passed; full suite completed with 6952 passing assertions, final BUILD OK banner and exit 0. Final native probe passed with no browser errors. Whitespace and LF/CRLF checks pass.
