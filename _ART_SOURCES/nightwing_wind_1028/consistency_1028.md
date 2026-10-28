# Nightwing — consistent wing planform, October28

Mike identified extra wings and changing aircraft identity in the teal wind Nightwing. The culprit was the earlier Part2 blue stealth roll/somersault/bank art, mixed with the regular sky_repair Nightwing plate. Those legacy attitudes had longer extra stabilizers and a different fuselage/cockpit; the earlier flight shadows also retained that geometry.

## Correction

The owning `_ART_SOURCES/nightwing_wind_1028/build.py` now uses the same native sky_repair aircraft for every whole pose. Its regular teal hull/royal cockpit is pixel-identical to the previous regular pose. Damaged metal remains. The underside uses the native belly texture clipped to the canonical hull footprint. Source-pixel roll/pitch cells are authored offline with bounded body/engine depth, fixed272px canvases and measured transformed nozzle anchors. No Part2 flight-image input remains. Rolls/banks share this aircraft, as do rotated headings, curved entry, large flyover, shrinking drift, approach and death. Native107-cell indices and all flight timings remain.

Matching white-hit banks and four depth-shadow banks are rebuilt from the same actual pose alpha. Previously absent shadow aliases now select the corrected geometry. Removal of old fins also removes their phantom collision. All runtime artwork is fixed even cells; no new runtime rendering transforms. Cache-distinct identity filenames and registry version prevent old artwork from being reused after reload.

Weapons, non-destructible recoil guns, native muzzle anchors, thruster/ring effects, wind charge, ordinary-bullet interception policy, health, one-target ownership, protection, AI, native destruction and rewards are unchanged. No game.js/test_fl.js edits. Sources, original legacy files and editable Aseprite whole-sheet source retained; no paid generation.

