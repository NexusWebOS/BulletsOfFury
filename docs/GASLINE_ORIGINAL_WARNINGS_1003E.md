# Gasline Stage X score and original warning visuals — October 3

Mike supplied `C:/Users/Mdogg/Desktop/Gasline.wav` for Stage X and requested the original warning and Retina system visuals instead of the newly generated Stage 8 warning art.

## Music

`_BUILD_SOURCE/build_gasline_1003.py` converts the complete 88.36-second, 48 kHz stereo recording to 256 kbps MP3 with libmp3lame. No trimming, gain change, time stretch or normalization. Original WAV remains on the Desktop. Runtime file: `assets/game/music/stagex_gasline_1003.mp3` (2,829,412 bytes). Decode validation, SHA-256 hashes and encoding details are in `docs/qa/gasline_1003.json`.

`assets/rival_fight_0924.js` registers a separate `stagex` key in both BOFA and the already-created Snd music bank. Actual Stage X deployment starts that track once, with normal looping, volume and stop behavior. The normal Stage 6 `boss6` mapping is unchanged. Stage X restart redeploys with its usual fresh music flag.

## Original warnings

`assets/original_warnings_1003e.js` loads after the latest finale and code-wall layers. Stage 8 warning calls now use the original `combatWarningDraw` and `groundTargetReticleDraw` functions:

- Boss warning cones and one green/yellow/red alert sign use existing `bmfx_fov_*` / `bmfx_alert_*` art. The sign clears the shield HUD.
- Original Hammer/ground Retina art marks committed target positions and progresses through its original colors.
- Ordinary aliens use the shared system's straight lane bands, without floating boss triangles. Their real owner is passed by `assets/stage8_1003.js`.
- Attack geometry, timings, damage and locks stay with their existing owners. New shield art, hit flashes, reconstruction, alien beams and actual projectiles remain separate from warning graphics.

## Verification

The focused native Chromium probe (`_BUILD_SOURCE/probe_original_warnings_1003e.py`) passes 13 checks with zero page/console errors. It observes native drawing for all three boss FOV colors, ground Retina, the knight warning and ordinary enemy lanes; screenshots were inspected. It deploys Stage X through the real campaign-map and wingman-selection path, confirms the actual Snd player is playing the MP3, verifies 88.36-second duration and looping, captures non-silent waveform samples from the playing media stream, checks clock advance, and verifies leaving Stage X stops Gasline while normal boss6 playback remains separate.

Initial native verification found the new music key needed an entry in the already-created Snd bank, not just BOFA; fixed. A probe assertion initially expected the boss cone renderer on an ordinary enemy; inspection confirmed the original straight-lane policy was working correctly, and instrumentation was corrected to observe that renderer. Final native run exits 0.

Full suite exits 0 with 6,917 passing assertions and its final success banner. Syntax checks for game.js and the three edited/new runtime files pass. Results are recorded in `docs/qa/original_warnings_1003e.json`. Preview/audio download: `_shots/original_warnings_1003e/review.html`. No commit, push, source deletion, or Git integration in this pass.
