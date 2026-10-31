# Correct metal water-wall warning signs — October 30

[Watch the corrected water-wall preview](http://127.0.0.1:51046/?tidal=metal-warning-signs-1030#clip=stage9-tidal-walls)

Mike meant the actual metal-framed warning signs used by Stage 2. The preceding pass incorrectly used HH52's plain red impact stars. The three water-wall warnings now use the original nwarn_yield/nwarn_alert artwork: queued lanes are yellow; the next lane is red. Each sign remains above the hull/effects until its own wall launches. Ordered reveals, bobbing placement, three decoded beeps and dedicated aqua rushing/crashing wave sounds remain.

Source artwork was extracted through the native XART renderer and archived as wall_yield_master.png and wall_alert_master.png. Aseprite normalizes each proportionally to 52-pixel artwork height on fixed 64x64 cells with pivot 32,32. wall_warning.png/.aseprite contains two states. The existing owning author.lua/inputs.json, manifest and registry now include that bank; build_tidal_sovereign_1029.py rebuilds it with the rest. No new paid generation, runtime sprite scaling/tint/glow or new atlas was used. The bank adds 32 KiB decoded. Existing warning signs elsewhere remain unchanged.

64 native checks and 42 art checks pass: actual warning identity/order/preload, visible changed red pixels above the real hull, even cells/padding, source metal-border pixels, sound decoding, mortar weave/socket/landing commitments, HP/half/hit/death and prior Sentinel behavior. Native and decoded film frames were inspected. Existing attacks and water audio were retained.

The new short real-engine Furious GOD-observer water-wall excerpt runs at 58.19 FPS, preserves native HP and clocks, contains all three wall launches and their actual decoded beeps/water rushes, and reports no engine/asset/media/audio/input errors. 11/11 video checks pass. Encoded audio mean -22.7 dB, peak -8.8 dB; browser playback and HTTP 206 seek pass. This is an attack excerpt, not a complete defeat or human difficulty test. The water-wall chapter now points to this new media; older full fight and other chapters remain available.

Syntax passes. Required full suite completes and exits 1 with the same five existing failures: single-hit flash hold, opening-jump dialogue, jump/chromium order, opposite Stage X route persistence and Stage X right-branch encounter. game.js/test_fl.js unchanged. No commit or push.

Runtime owner: assets/tidal_sovereign_1029.js / ts61WaveWarnings. Art sources: assets/game/levels/stage_09/boss/tidal_sovereign_1029/. Verification helpers: _BUILD_SOURCE/probe_tidal_warning_signs_1030.py, record_tidal_warning_signs_1030.py and audit_tidal_warning_signs_1030.py. Evidence: docs/qa/tidal_warning_signs_1030.json.
