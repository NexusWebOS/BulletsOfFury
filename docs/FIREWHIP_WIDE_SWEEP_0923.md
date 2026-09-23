# Firewhip wide sweep — September 23, 2026

Mike requested the broad left/right sweep again, retaining the approved natural curls. GPT2.5 Sunburst generated 16 new wide-lash poses using the existing master as reference. Eight approved curl poses are interleaved for 24 complete frames across the existing 1.4-second cycle. Mike clarified with a reference screenshot that the flash must stay on the ship's nose while the entire flame, including its lower shaft, bends left and right. The animation now hinges at that fixed muzzle. No frames are mirrored or procedurally bent at runtime.

The whip and circular muzzle retain the sampled flamethrower/fire-orb palette. Collision masks are rebuilt from each displayed pose, including intervening frames during a fast update. Damage and one-hit-per-target-per-half-stroke behavior remain unchanged. Both extended sides reach more than 100 world pixels from the root at weapon level 1.

Assets: `assets/game/player_weapons/fire_whip_sweep_0923/`. The manifest retains source IDs, frame order, extents, and hashes. New asset: `bf2adfda-6b5c-4b59-b2e4-f30572fe2159`; GPT2.5 Sunburst, 2K/high, 55 credits. SpriteCook's pixel conversion incorrectly reduced the sheet to 33x33, so the full-resolution raw source from the same asset was recovered and normalized locally. Integration report: `dab046fb-266d-416d-8f6b-2b6ac03aa7b1`.

Rebuild with `python _BUILD_SOURCE/build_fire_whip_sweep_0923.py --install` to synchronize frames, collision masks, registrations, and runtime frame count. Previous generated sources are retained.

Verification artifacts: `_shots/firewhip_sweep_0923/`, `_shots/firewhip_wide_probe_0923.log`, and `_shots/firewhip_wide_suite_0923.log`.

The intermediate moving-flash version was superseded. Its checks and suite are retained in `_shots/firewhip_swing_*` only as history. The current real Chromium check confirms the flash at the ship nose on every frame, the lower shaft bending both ways, authored collision and the complete rendered animation, with no page or console errors. The full suite reached its summary with exit 1: 4,889 passing / 81 failing. The only additional failure name versus the preceding run was the known intermittent sand-tank spawn assertion; no new failures outside the recorded baseline. Current logs: `_shots/firewhip_fixed_muzzle_probe_0923.log` and `_shots/firewhip_fixed_muzzle_suite_0923.log`. Nothing committed or pushed.
