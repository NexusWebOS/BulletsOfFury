# Nightwing — consistent wing planform, October28

Mike identified extra wings and changing aircraft identity in the teal wind Nightwing. The culprit was the earlier Part2 blue stealth roll/somersault/bank art, mixed with the regular sky_repair Nightwing plate. Those legacy attitudes had longer extra stabilizers and a different fuselage/cockpit; the earlier flight shadows also retained that geometry.

## Correction

The owning `_ART_SOURCES/nightwing_wind_1028/build.py` now uses the same native sky_repair aircraft for every whole pose. Its regular teal hull/royal cockpit is pixel-identical to the previous regular pose. Damaged metal remains. The underside uses the native belly texture clipped to the canonical hull footprint. Source-pixel roll/pitch cells are authored offline with bounded body/engine depth, fixed272px canvases and measured transformed nozzle anchors. No Part2 flight-image input remains. Rolls/banks share this aircraft, as do rotated headings, curved entry, large flyover, shrinking drift, approach and death. Native107-cell indices and all flight timings remain.

Matching white-hit banks and four depth-shadow banks are rebuilt from the same actual pose alpha. Previously absent shadow aliases now select the corrected geometry. Removal of old fins also removes their phantom collision. All runtime artwork is fixed even cells; no new runtime rendering transforms. Cache-distinct identity filenames and registry version prevent old artwork from being reused after reload.

Weapons, non-destructible recoil guns, native muzzle anchors, thruster/ring effects, wind charge, ordinary-bullet interception policy, health, one-target ownership, protection, AI, native destruction and rewards are unchanged. No game.js/test_fl.js edits. Sources, original legacy files and editable Aseprite whole-sheet source retained; no paid generation.

## Verification

-35 new identity/native-render checks pass: exact regular pixels, consistent bank/roll/pitch input, same underside planform, every rebuilt cell’s clear borders, even/4096 limits, all white-mask alpha, four matching shadow families/aliases, actual native one-hull draws and hit-art selection for8 flight attitudes, discarded-fin collision and single HP/target.
-20 existing native wind/weapon/flight checks pass, including true accepted damage/white pixels/expiry, both emitters, engine sizes, wind warnings and non-interceptable shots. Initial local preload backlog overflow was corrected by increasing only the development server's queue for the rerun; no game error remained.
-Fresh102.55s real Furious Nightwing life reaches native defeat with GOD/input bot and ordinary allies,56.53 nativefps average. Carrier fight skipped in setup through native ace spawn. First35s withhold player fire. No enemy HP/phase/timer writes. Native wind/gun turns, multiple complete dash/flyover/drift/approach cycles and clear/white damage frames are present.10 film checks pass, no game/browser/bot/HTTP errors; audio mean−17.8dB / peak−2.4dB. Decoded native frames inspected.
-14 review playback checks pass for both movies: actual moving1280×800 frames, audio, three seeks each, range206 and no browser errors.
-All31 PNG banks /2393 cells and registry rebuild byte-identically. Updated editable Aseprite sheet contains the corrected107 whole-aircraft cells with their existing fixed metadata.
-Syntax checks pass. Required full suite reaches its summary with the same five prior failures (exit1): single-hit flash duration, opening-jump dialogue warning, jump return before Chromium, opposite StageX route persistence, StageX right full encounter. No commit or push.

Review: http://127.0.0.1:61609/. Local evidence: `C:/Users/Mike/Documents/New project/BOF-Nightwing-Consistency-1028/`. Portable probe: `_BUILD_SOURCE/probe_nightwing_consistency_1028.py`; recording helper: `_BUILD_SOURCE/record_nightwing_consistency_1028.py`. Source recipe: `_ART_SOURCES/nightwing_wind_1028/locked_motion.py`; aggregate QA: `docs/qa/nightwing_consistency_1028.json`.
