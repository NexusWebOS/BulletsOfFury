# Weapon muzzle feedback and Stage 5 music — September 26–27, 2026

Mike requested Hammerman Cometh for the Stage 5 main boss, the previous main-boss track for its miniboss, aligned Reaver/Warden barrels, and weapon-specific firing/charging effects for players and enemies.

## Music

| Encounter | Runtime music |
| --- | --- |
| Stage 5 miniboss | `assets/game/music/boss5_deadly_night.mp3` — previous boss theme |
| Stage 5 boss | `assets/game/music/boss5_hammerman_cometh_0926.mp3` |

The supplied WAV is preserved in `assets/game/music/originals_0926/Hammerman Cometh.wav`. The browser copy uses 44.1 kHz stereo, 112 kbps MP3, with 1 dB source attenuation. Native Chromium decoded both routes: 134 seconds and 101.96 seconds respectively. The Desktop original and other music files remain intact.

## Runtime

`assets/weapon_muzzles_0926.js`, loaded after `encounters_0926.js`, owns short release animations and Maverick/Falva charging effects. Narrow release hooks in `game.js` cover normal firing, early-return specials, manual/automatic missiles, space racks, charged releases and shared enemy shooting functions. Existing specialized beam emitters remain active. This pass reuses inspected authored art; it adds no procedural muzzle sprites or atlas modifications.

| Weapon | Authored reel / behavior |
| --- | --- |
| Machine gun | `weapon_muzzle_rotary_*`, level/element palette |
| Chaingun | `bpfx_muzzle_kinetic_*`; replaces the flat triangle |
| Spread / Decker shotgun | `ndk_muz_*`, directional fan with separate sizes |
| Missile / rocket | `weapon_muzzle_missile_*` ignition; existing specialized launch reels retained |
| Laser / Maverick | `weapon_muzzle_laser_*`; growing green charge becomes purple at full charge |
| Orb / Falva roller | `bpfx_muzzle_void_*`; Falva's pink charge grows at the release point |
| Fire / Freezer ice breath | `bfx_magma_m_*` / cyan emitter with the existing continuous breath |
| Yuri lightning | yellow or upgraded blue discharge at the chain origin |
| Sonic | existing circular sonic emitter reel |

Release flashes follow their owner or exact rotating hardpoint. Fan pellets share a flash per barrel, separate barrels keep separate flashes, and the fired palette persists during weapon changes. Dead emitters, expired flashes and stage changes clear the effects; hidden cinematic ships do not acquire floating firing effects. Moving projectiles are unaffected.

The Inferno Reaver's outer gun mounts now match its lower pods. Olive Warden gun and rocket mounts match the visible guns and upper launch pods. Storm Sovereign forward gun mounts are mirrored and centered on its authored barrels; rockets use separate rear launch pods. Stage 4 helpers use the same rotated tip equation as their shots. Stage 4 gun/orb/lightning flashes use detailed reels instead of the flat arrow plates. Shared naval flashes now draw above boss hulls, and accept cached canvases as well as image elements.

## Verification

- `node --check assets/game.js` and module syntax checks pass.
- Full suite reaches its final banner: **5,159 pass, 0 fail**, exit 0. Baseline was 5,142/0. Early runs exposed two stale source expectations and two asymmetric hardpoint assertions; the source expectations were updated and the geometry was made symmetric. Logs are retained under `_shots/muzzles_0926/`.
- Native Chromium: 55 valid pilot/weapon combinations, eight special/missile routes, all frames of 11 muzzle families with nonempty raster output, moving-owner tracking and expiry, and three boss firing-origin checks pass.
- Both reassigned music files decode in Chromium. Page and console errors: zero.
- Five focused recordings show keyboard movement, actual firing, charge/release and boss patterns. They use isolated invulnerable fixtures and do not establish campaign difficulty or balance.

Evidence: `docs/qa/weapon_muzzles_0926.json`; local review: `_shots/muzzles_0926/review.html`. Verification scripts are `_BUILD_SOURCE/verify_weapon_feedback_0926.py` and `_BUILD_SOURCE/record_weapon_feedback_0926.py`, both using `shoot.py`'s native Chromium workflow. The new suite checks live in `test_weapon_muzzles_0926.cjs`. Game LF and harness CRLF are preserved. Nothing committed or pushed.
