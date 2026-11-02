# Current Breaker overhead flight / November1

Mike added true top-down flying sprites after approving the frontal transformation
and casting identity. Standing, transformation, tidal waves and grenade casts stay
front-facing. Superman flight now uses eight separately authored overhead views:
S, SW, W, NW, N, NE, E, SE. Never rotate the frontal humanoid to substitute for
these views.

The selected generated source is `flight_topdown_source.png` in the existing
Stage9 source directory; exact successful prompt and output ID are in its source
ledger. The actual source has eight448px cells; the owning builder registers
common384px cells and one236px proportional body unit. Separate palms have
measured alpha-bearing sockets per direction. Six new banks bring the roster to
23 selected sources and177 even banks. The other18 models and canonical Current
frontal/morph banks retain their original metadata.

`_BUILD_SOURCE/build_stage9_amplify_1101.py` owns exports. Launch/recovery use
eight baked liquid source-pixel transition cells each, assembled from approved
crouch/front-flight/palms and the new overhead South pose. They are source-pixel
transfers, not newly generated intermediate3D poses. Endpoints match the actual
native poses. The optional generated intermediate-pose attempt returned no image
and is not an active source. No runtime opacity or static-sprite rotation is used.

`assets/current_flight_1101.js` loads after the native Stage9 owner. It selects
directional flight cells and live palm sockets, with launch/recovery transitions.
It retains the original attack book, native HP, path, cues, damage, hit feedback,
boss cancellation and frontal casts. No changes to game.js/test_fl.js this pass.

Verification:30/30 native Chromium checks cover all difficulties, eight actual
direction selections, alpha-bearing hand emitters, damaged pixels/flash expiry,
transition endpoints, attack book and boss cleanup.8/8 browser checks inspect
actual decoded front/transition/overhead frames, seeking, mobile layout and the
full guide, with no page/console errors. Evidence is under
`_shots/current_flight_1101/`.

One fresh29.14s H264/AAC native-input film replaces only Current's preview.
Native59.5fps, decoded PCM peak0.316/RMS0.079, unclipped; full decode succeeds.
The pilot is a labeled invulnerable observer; no enemy HP/phase/timer writes.
All153 other guide cards and18 other Stage9 films remain unchanged. Publishers:
`record_current_flight_1101.py`, `publish_current_flight_1101.py` and
`verify_current_flight_1101.py` under `_BUILD_SOURCE/`.

Review: http://127.0.0.1:8805/current/stage9-water-refit-1101.html#enemy=stage9-cbreak

Syntax passes. Required `node _BUILD_SOURCE/test_fl.js` exits1 before assertions
or final summary on the existing missing ignored
`UNUSED_ASSETS/retired_art_1022/manifest.json`; the full suite is not green.
No commit or push.
