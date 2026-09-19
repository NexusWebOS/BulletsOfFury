# Razorback recorded tread and dual-tank audio ownership — 2026-09-19

The Razorback movement loop now blends a CC0 metallic rolling recording into its existing low motor bed. The source is [“Tank Tread” by 77Pacer](https://freesound.org/people/77Pacer/sounds/425271/), a recorded sliding garage door offered as a tread effect under CC0. The public HQ preview is stored beside the output; the earlier synthesized loop is retained under `assets/game/sounds/unused_x/`. `_BUILD_SOURCE/rebuild_razorback_recorded_tread.py` recreates the 2-second mono WAV byte-for-byte. Its waveform has a zero-amplitude seam difference and 0.233 RMS at the WAV sample scale.

The Hard duo previously had both actors independently switching off the same loop. Its pair controller now owns the channel and uses the fastest live actor's movement: one stationary or destroyed tank cannot mute the moving one. A stationary pair stops the loop.

Focused Chromium checks verified moving/stopped/part-destroyed pair ownership, decoded the WAV as 2-second mono audio, and reported no page errors. `node --check assets/game.js` passed. The full legacy suite returned 76 existing assertions versus the prior 75-failure run; the only difference was the already-intermittent Stage 1 sand-tank spawn assertion.
