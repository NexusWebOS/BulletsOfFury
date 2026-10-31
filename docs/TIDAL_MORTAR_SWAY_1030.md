# Tidal Sovereign mortar weave — October 30

[Watch the live attack excerpt](http://127.0.0.1:51046/?tidal=mortar-sway-1030#clip=stage9-tidal-mortars)

The water mortar charge and active volley now weave left and right around the visible playfield centre, with a small fore/aft hover. Movement ramps in over 0.8 seconds, uses simulation time, is capped at 180 pixels/second and retains 168-pixel hull clearance. Native 480-pixel framing allows a 144-pixel full sweep. The attack does not add sprite rotation, scaling or new body art; current authored water/fan animation remains. Its established recovery eases back toward the home position.

The four alternating northbound fan launches still use the actual current hull sockets. Each shot retains its locked destination, offscreen handoff, ground Retina/beeps and returning geyser; warnings do not chase the moving boss. No change to attack count, speed, cadence, damage, HP, half-health protection, wave warnings/audio, or the separate paired fan-rain attack. Existing hit-flash/death/reset and native damage remain.

62 native Chromium checks pass, including smooth lateral reversals, more than 100 pixels of visible movement, entry from off-centre, actual socket agreement for all four launches, committed landing points, finite recovery, and previous weapon/HP/hit/death/Sentinel regressions. Actual native and decoded screenshots were inspected.

New short real-RAF Furious GOD-observer attack excerpt: no enemy HP/phase/timer writes, 237.29-pixel active mortar sweep, 58.03 FPS. It is a presentation excerpt, not a complete fight or human balance test. 10/10 video/playback checks pass. Recorded audio mean -23.0 dB, peak -9.2 dB, no engine/media/asset/audio/input exceptions. The gallery's mortar chapter now uses this recording; earlier full-fight footage and other chapters remain available.

Syntax checks pass. The required full suite completes and exits 1 with the same five existing failures: single-hit flash hold, opening-jump dialogue, jump/chromium order, opposite Stage X route persistence and Stage X right-branch encounter. Core game.js and test_fl.js unchanged. No commit or push.

Owner: assets/tidal_sovereign_1029.js / ts62MortarMove. Reusable native probe and recorder: _BUILD_SOURCE/probe_tidal_mortar_sway_1030.py and record_tidal_mortar_sway_1030.py. Full evidence: docs/qa/tidal_mortar_sway_1030.json.
