# HAMA — hooks and OH chants only

Originally prepared October 1, 2026 after `3cf07043`; prepared for the October 2 GitHub upload.

Mike's latest direction supersedes both earlier full-vocal mixes: **use only his recorded “can't touch this” hooks and “ooooh / ohhh” chants**. The active song is `assets/game/hama_vocals_1001/hama_mike_robot_mix_1001_v3.mp3`. The new URL avoids the cached rejected songs.

The same deep, fully wet vocoder and hard pitch correction are applied to the selected extras. The lead verses, robot dialogue, jump gag and spoken STOP/Hammer/Time clips are excluded from the build. Captions contain only `CANT TOUCH THIS` and `OH! OH-OH!`; singing mouths follow those cues and remain idle during the removed verses. Original source recordings are preserved losslessly under `_ART_SOURCES/hama_vocals_1001/`.

The finished track has 14 vocal placements and 42 short captions, and retains the original 180.013-second music/choreography clock. Physical hammer slams and dance sequences continue against the instrumental. The single existing HAMA music element owns audio, pause, loop and exit. HAMMER retains its separate remix.

Rebuild: `python _BUILD_SOURCE/build_hama_vocals_1001.py`. Custom vocoder: `_BUILD_SOURCE/hama_robot_dsp_1001.py`. Generated cues and audio path: `assets/hama_vocals_art_1001.js` and `assets/game/hama_vocals_1001/cues.json`. Runtime integration: `assets/hama_vocals_1001.js`.

Verification: **6,203 assertions pass, zero errors**, full final summary reached and no new failing names versus the incoming 6,203/0 baseline. **14 real Chromium checks pass**, with no page/console errors. Both approved vocal sections render; removed verse captions remain clear. Playback, pause/resume, physical slam choreography, chant captions, looping and exit are verified. Decoded duration 180.012993s, peak 0.732, zero clipped samples; removed verse vocal stem peak is exactly zero. The native clip uses an invulnerable player for media review and is not a campaign clear.

Portable evidence: `docs/qa/hama_vocals_1001.json`. Latest preview and captured gameplay: `_shots/hama_hooks_1001/review.html`. Earlier previews are historical.
