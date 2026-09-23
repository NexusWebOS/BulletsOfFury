# Firewhip laser muzzle — September 23, 2026

Firewhip's curved-laser branch skipped the beam renderer and its continuous muzzle. It now draws the existing generated circular laser muzzle reel in the fire palette at its live pivot after rendering the whip. The shared path serves gameplay and Forge previews. The player renderer suppresses its separate firing flash while Firewhip is active, just as it does for held beams.

The engine header now records the standing rule: player and ordinary enemy/boss lasers use palette-matched authored circular muzzle flashes at the attacker hardpoint; held and curved lasers keep the flash throughout firing. Specialized authored exceptions remain explicit.

Verification: syntax check passed. Real Chromium `probe_firewhip_muzzle_0923.py` passed moving-pivot attachment, exactly one muzzle, stop behavior and actual Forge rendering, with no page or console errors. Screenshots inspected in `_shots/firewhip_muzzle_0923`. Existing `probe_muzzle_variants_0923.py` also passed player laser tiers, nine pilots, nine elements, eleven enemy families, space hardpoints and moving boss mounts. Full suite completed with exit 1 and the same 81 failing assertion names as `_shots/forge_modular_suite_0923.log`; no new failures.
