# Overlord rotor audio — 2026-09-14

S1-08: replaced the servo-whirr placeholder with a dedicated original helicopter loop. Six seconds of periodic blade pulses, low engine harmonics and turbulent air, authored as mono 44.1 kHz PCM16. No third-party recording or license dependency. Reproduce with `python _BUILD_SOURCE/build_overlord_rotor_0914.py` (NumPy required).

The existing Overlord refresh call, mixer gain, attack/fade, preload and stop handling remain in use. Runtime registration now resolves `assets/game/sounds/overlord_helicopter_rotor.wav`.

Native Chromium verified decoded audio, a running audio context, advancing playback through three loop wraps, and release fading through level 0.1667 to zero and paused. Console errors: zero. This confirms playback plumbing, not a subjective listening review; full encounter pause/death handling was not repeated.

Peak 0.78; loop seam jump 0.02068, below the maximum adjacent-sample jump 0.06775. JavaScript syntax passed. Full suite: 3,850 passed, 58 known failures, exit 1; no new failure names against the pilot-reveal baseline. Detailed measurements: [QA](qa/rotor_audio_0914.json).

Next: UI-10, onion-align pilot-select ship rotation frames. Investigation identified independent frame fitting in psBlitFit; no alignment change is included here.
