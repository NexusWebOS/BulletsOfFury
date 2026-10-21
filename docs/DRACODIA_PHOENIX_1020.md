# Corrupted Fire Phoenix — Dracodia's volcano replacement

Mike rejected the angled volcano robot. Slot2 now becomes a completely new,
strictly forward-facing corrupted alien fire phoenix made in PixelLab. The
Stage2 Furnace boss retains its native identity and controller.

## Art and anatomy

PixelLab Pro master `a3ed4f8a-edd3-49c0-8ba3-479f887a287f` supplies every
body pixel. Seventeen lossless components reconstruct the original exactly;
the256-square source is padded to320-square modules without rescaling.
The renderer uses one proportional world scale and fixed physical pivots.

Ten damage owners remain within the original total HP budget: two wing-root
armor sections, two furnace cannons, two blade-feather wings, two talon/tail
assemblies, the furnace heart and phoenix skull. Each breaks independently,
flashes through native owner/part feedback, emits its actual component debris
and stays destroyed through copy changes. A broken emitter cancels its beam
immediately. Targets, alpha masks, warnings and ordnance use the moving rig.

Live anatomy uses nine coordinated PixelLab wing/charge poses, partitioned into
seven modular banks with common canvases and pivots. Metal wings beat and tuck,
cannons aim/recoil, the heart charges, and talons/tails fold for rolling attacks.
The new skull has16 confined eye-charge states and32 fixed-scale turn poses;
the eye positions rotate with its artwork and own both warning and beam roots.

## PixelLab attack art

- Wing/furnace animation: `40f92480-fd27-4286-b87e-db372e4e0298`.
- Phoenix muzzle bloom: source `6b1ca499-cabc-492f-9ba3-006b3c6cc2d5`,
  sixteen animated frames `8fae5f5b-d5fd-4b27-b977-789be6c7420b`.
- Molten chromium feather: `ac817c6c-04a2-4b0d-9731-b259ed949e24`.
- Infernal beam: refined continuous-column PixelLab edit
  `76edd3fb-baae-4a18-a4f0-34131edbd8ea`, sixteen flowing heat-pulse frames
  from exact PixelLab drawing `344bdb15-4628-4260-8190-438a67737b3f`.
  The first arrow/spike-shaped beam was rejected after native visual review.
- Skull eye charge: `01ab246b-e121-4006-9ef4-238e0d34d4d9`; changes are
  confined to the two apertures to preserve stable armor and mounting points.
- Matching wireframe: `f56bc2ca-fccf-496c-98e7-a817c63444af`, exact PixelLab
  sixteen-frame scan drawing `5519d03c-45cc-43fc-b5fd-2586fe76d6af`.

Native Furnace timing, difficulty tuning, sounds and damage still own cannon
volleys, flame sweep,900-degree spin, heart rings/lance, fire rotor, committed
roll passes and the surviving skull's eye sweep. New attack visuals are PixelLab
art attached to those physical origins. Wide volleys use a seven-feather wall;
beam textures tile proportionally with one common scale across the entire bank.
Warnings remain authored FOVs. The source boss receives no phoenix tags/art.

## Integration and retained sources

New runtime: `assets/dracodia_phoenix_1020.js`, following the existing modular
volcano owner. Generated registry: `assets/dracodia_phoenix_art_1020.js`.
Readable shipping folder:
`assets/game/levels/stage_08/boss/corrupted_phoenix_1020/`.
Owner: `_BUILD_SOURCE/build_dracodia_phoenix_1020.py`.
Sources/provenance: `_ART_SOURCES/dracodia_phoenix_1020/`.
The existing wireframe builder now supports a source cacheTag, preserving all
old source files while replacing only its volcano entry with the phoenix.

Native reference capture forwards canvas properties as well as drawing methods.
The older generic export forwarded save/restore to its transparent canvas but
left globalAlpha on the original context, incorrectly dropping later modules
after additive passes. `_BUILD_SOURCE/export_phoenix_1020.py` corrects this for
the new actual-renderer reference. The incomplete wireframe candidate was rejected.

The full-loop arms fire test caught a genuine anatomy partition error: a few
lower cannon pixels were assigned to the protected talon and intercepted shots.
The thigh mask now begins inside the body, leaving every cannon-edge pixel with
its actual cannon. The final fixture fires from a legal station below it;
collision masks and weapon/player stats were not relaxed. Each wing's inner and
outer sections share its vent damage owner, preventing orphan feather sections
after a cannon breaks.

Review: `_shots/dracodia_phoenix_1020/review.html`.
Verification reports and logs: `_shots/phoenix-*.log` and the review folder.
No commit/push requested. All unrelated dirty game and Overdrive work retained.

## Final verification

235 native checks pass:114 module/attack checks across Easy, Normal, Hard
and Furious;16 complete-loop, ordinary-fire and decoded-audio checks;28 skull
pose/eye/hit checks;70 preserved wireframe/escape checks;7 actual PixelLab frame,
break and source-delegation checks. Nine review previews load with no browser
errors or narrow-layout overflow. Full regression suite:8854 printed passing
assertions, BUILD OK0errors, process exit0. Game/runtime syntax checks pass.

The final164 new PNGs total647,082bytes. All delivered dimensions are even;
modules320-square, skull128-square, plume128-square, beam64x128, feather64-square.
