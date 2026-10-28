# Solid Harrier gun modules — October 27

The four ghost turrets came from the October 27 encounter art builder treating HH21's white, brightness-only hit-highlight masks as complete colored gun plates. That preserved only scattered highlights and partial alpha. The files were intended for brief damage feedback over an existing hull, not for use as detached modules.

## Correction

The gun banks now use the actual dark-metal colors from the Harrier's original two central gun housings. Full hand-outlined silhouettes retain the dark body and barrel pixels at alpha 255. Four fixed 96x96 banks each contain 64 directions x 4 recoil cycles; matching white banks flash the complete opaque module. All four existing sockets and component IDs remain. Recoil retracts the barrel section while the mounting body stays fixed. The two native bore sockets are stored for every heading/recoil pose; the native gun alternates between them when emitting its existing rounds.

The existing encounter renderer owns drawing and smooth bearing/frame selection. The updated muzzle owner is shared by emission, warning and muzzle graphics. Projectile point hits use the actual authored opaque gun pixels. Each module retains its original health, Retina target, native flash, break effect and attack disable on destruction. Other component budgets, carrier movement/flight, beams, fan/rack weapons, Nightwing, stage progression, rewards and bullet interception rules remain native. This is an art/socket correction; the invulnerable recording does not establish player difficulty.

## Owners and reproducibility

- assets/harrier_turrets_art_1027.js registers the colored/hit banks and per-frame bore metadata.
- assets/harrier_turrets_1027.js replaces the four ER28 hull-gun definitions and attaches their opaque hits and emission sockets to the native gun owner.
- Runtime PNGs: assets/game/levels/stage_06/boss/harrier_turrets_1027.
- _ART_SOURCES/harrier_turrets_1027 retains the full colored sources, silhouettes in build.py, manifest, compiled banks and gun-colour.aseprite. The portable builder finds its repository from its own location; ASEPRITE_EXE selects an optional Aseprite editor export. Runtime PNGs and registry rebuild byte-identically.
- _BUILD_SOURCE/probe_harrier_turrets_1027.py runs the native fixtures; --out selects the evidence folder. These deliberate state/damage fixtures are separate from the real-time film.

The original HH21 masks and original hull atlases remain preserved. No paid generation was required. index.html loads the new owner after ER28 and the current bomber/HUD owners, with cache version solid-modules-1027a. No game.js or test_fl.js edits.

## Evidence

17 targeted art/native Chromium checks pass: opaque colored banks, fixed frame/bore data, five actual targetable headings per gun, attached moving sockets, native alternating-bore emission, real white damaged pixels and expiry, four independent Retina targets, isolated component death/fire cancellation, and unshootable ordinary bullets. Actual idle/firing/hit/destroyed screenshots and decoded film pixels were inspected. No final page, console or asset HTTP errors.

The fresh 161.83-second Furious Cole GOD/input-bot film completes Harrier and Nightwing normally. All four gun modules die through native damage; first 22 seconds withhold player fire. Native HP, damage, attack timing and phases are unchanged during capture. Average native rendering 55.16fps; encoded 30fps. Decoded audio mean -18dB, peak -1.5dB. No game/bot/console/HTTP asset errors; five background preloads were aborted on navigation/closure. God Mode prevented 672 hits; the film is explicitly behavior/art evidence.

Syntax passes. The full required suite reaches its summary with the same five baseline failures: one flash-duration expectation, two Chronos opening-jump expectations and two StageX right-branch expectations. See docs/qa/harrier_turrets_1027.json.

Current review: http://127.0.0.1:62986/index.html. The older Stage6–9 gallery's Harrier card now points to this film. No commit or push.

All nine final Chromium video playback, seek and current-build source-hash checks pass.
