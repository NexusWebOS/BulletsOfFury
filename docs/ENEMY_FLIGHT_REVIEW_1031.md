# Stage 4–9 regular enemy animation and firing review

Mike requested the Stage1–3 flight, firing, muzzle and projectile rules be applied to the remaining regular enemies. This pass covers the authored Stage4–9 enemy roster and its guide cards. It does not replace the separate boss/miniboss encounter owners or activate the queued dark-weapon pass.

## Findings and changes

- The baseline exercised 116 authored wave variants. Several Stage6/9 renderers changed hull identity between idle and attack. R46 uses one complete existing source model through idle, attack, drift, roll and somersault, with a shared pivot, proportional scale and even heading cells.
- Stage4 interceptor/rocket flights could leave before the attack controller had a useful window. Their bounded curved sorties now bank toward their route, preserve native AIR17 attack phases and recovery, then visibly leave. Rocket attacks use the native rocketeer role.
- Direct canonical Sewer Drone/Slime/Relay spawns fell through to generic construction. They now reach the same native factories as their campaign aliases, preserving the real sewer controllers, HP and attacks.
- Physical muzzle sockets follow the rendered heading. Independent modular gun pools, targeting and broken-module cancellation remain native. Directly appended legacy rounds also use their owner's measured mouths.
- Physical missile launches use the native flashing Retina/beep owner and launch queue. The original round is kept outside the live projectile list until release, with its native shootability/acceleration modifiers retained. Release uses the current launcher position; native defeat cancels pending rounds and locks. Ground missile turrets keep their existing lock owner.
- Native ordinary projectile art is exported through the actual renderer into fixed directional cells. Explicit spinning orb art has a continuous full-turn reel. Stage palettes, alpha and hitboxes remain native; a small visual-only increase helps small rounds read. Ordinary rounds remain unshootable from birth, while missiles and explicitly shootable balls retain their exceptions.
- `assets/enemy_module_contact_1031.js` classifies bullet contacts against the displayed independent gun's authored alpha, replacing world-left/right classification on refitted aircraft. It preserves native part pools, attaches break effects to the real mount and cancels a destroyed module's queued missiles without disabling the surviving gun. The Stage7 Brood escort uses the same complete Crescent bank as Stage8.
- Matching existing stage muzzle/exhaust art replaces the shared gold muzzle on refitted hulls. Five remaining rotated native hull/module plates have explicit fixed-cell banks. Native hit feedback, shields, HP/parts, attack books, defensive clears and defeat/reward ownership remain intact.

## Owners and rebuilding

`assets/enemy_flight_1031.js` loads after the Stage1–3 pass. The art registries are `enemy_flight_art_1031.js`, `enemy_static_art_1031.js`, `enemy_ordnance_art_1031.js` and `enemy_feedback_art_1031.js`.

Build the complete body/module source banks with `_BUILD_SOURCE/build_enemy_flight_1031.py`, then preserve the Royal/Blackice material variants using `build_enemy_palette_1031.py`. Static native plates belong to `build_enemy_static_1031.py`. Native projectile capture belongs to `build_enemy_ordnance_1031.py`; `--repack-only` uses its retained original native captures. Matching feedback belongs to `build_enemy_feedback_1031.py`. Each builder writes its runtime registry and manifest together. `update_enemy_flight_metadata_1031.py` registers the taxonomy/atlas review without replacing native attack books.

All new runtime sheets and their owning manifests live under `assets/game/shared/combat/enemy_flight_1031/`. Native capture/reference PNGs are retained under `_BUILD_SOURCE/enemy_flight_1031/`. No original atlas was repacked and no new paid image generation was used.

## Verification and review

`audit_enemy_flight_1031.py` replays the real authored wave specifications and attack controllers in Edge. It saves per-stage evidence under ignored `_shots/enemy_flight_1031/after/`. `probe_enemy_flight_1031.py` checks actual native damaged pixels/expiry, prelaunch Retina timing, release of the original physical round and launcher cancellation. State changes used to center isolated QA crops are not part of the recording fixtures.

`record_enemy_flight_1031.py` records actual native sorties, normal movement input and the shared mixer. It uses an invulnerable observer; it does not write enemy HP, attack clocks, phases or live projectiles during a filmed case. Native Brood deployment and the special Tempest/flyby factories have separate guide cases. The clips demonstrate individual enemies, rather than certify full-campaign difficulty.

The final combat pixel/lock probe passes119 assertions. One temporary-server boot reported connection-refused/foundation-script errors; the subsequent stable-origin recheck passes all six stage boots, six heading-dependent native module-damage checks, destroyed-module missile cancellation, surviving-gun muzzle ownership and a real twin-gun release with two separate muzzle flashes (15 checks). `verify_enemy_flight_assets_1031.py` passes464 registered-asset, original-source and byte-identical complete-motion rebuild checks before the supplemental captures; all178 final registrations pass afterward. Final clip playback is checked after publication.

The capture fixture excludes unrelated reinforcement factories while preserving each selected enemy's native deployment owner, including LL18's deliberately cleared AI context. Brood deployment takes include actual spawned Crescent aircraft. Supplemental escort/rain projectile art is captured from the native renderers using `build_enemy_ordnance_1031.py --prepare-escort` / `--prepare-rain` and installed with the corresponding `--install-escort` / `--install-rain`; existing glyph banks are retained.

## Current local guide

All114 Stage4–9 cards are refreshed in the164-card guide at `http://127.0.0.1:8805/enemy-showcase-1031.html?revision=stage4-9-flight-1031#enemy=stage4-s4interceptor`. Stage1–3 and archived originals are preserved. The new films total1216.6 seconds, encoded as1280×800 H.264/AAC at30fps; measured native game speed averages59.7fps (56.2–60.1). Every current clip passes full video/audio decode, poster/route checks and actual Chromium seeking/frame/audio decode with no page or console errors.

Publisher: `_BUILD_SOURCE/publish_enemy_flight_local_1031.py`; installed routes remain scoped to `D:/BOF-Downloads/2026-10-31/current-overrides.json`. Complete media receipts, native source hashes, per-case timelines, full decode checks and browser playback evidence are under ignored `_shots/enemy_flight_1031/`. No Git commit or push was performed.

The required `node --check assets/game.js` passes. The full `node _BUILD_SOURCE/test_fl.js` exits **1 before assertions or its final summary**, because this checkout is missing ignored `UNUSED_ASSETS/retired_art_1022/manifest.json`. This pre-existing archive dependency is not replaced with invented data. Browser verification is reported separately from that blocked suite.
