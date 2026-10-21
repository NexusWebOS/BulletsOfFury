# Boss FOV warnings and combat sound wiring — October 15, 2026

Local changes in the main Bullets of Fury checkout. No commit or push.

## Warning presentation

Bosses, minibosses, password encounters and rebel fighters use the existing authored green/yellow/red FOVs. Removed the muzzle-anchored polish warning box, the legacy tiled arrow fallback, shared floating hazard signs, direct rebel signs and the old Sovereign escape-arrow overlay. The Knight's edge attack keeps its directional FOV without the extra text arrows. Existing impact reticles, target locks, projectile collision alerts and the Hammer SHOOT! objective remain separate functional cues.

All three FOV colours are required stage-load assets. Unregistered future laser families use the regular FOV instead of falling back to arrows. Warning timing, committed trajectories, collision, hit flashes, HP, difficulty tuning and Stage 4 simultaneous pressure retain their existing owners.

## Sound coverage

New owner: assets/combat_audio_1015.js, loaded after encounter/audio extensions. Seventeen previously undefined names now resolve to approved recordings: shieldHitCombat, shieldRestore, turbo, boost, enemyMachineGun, hammerWhoosh, somersault, falvaRelease, playerHit, warp, sludge, lightning, flameIgnite, fireOrbLaunch, iceOrbLaunch, enemyOrbImpact and laserCharge. The static loaded-script audit now finds zero undefined literal sound references after excluding comments.

Typed ammunition now distinguishes toxic spit, crystal/electric shards, mechanical tracers, missiles, heavy/rail ordnance, fire/ice, wind/sonic and alien energy families. Targeted balls/lobs gain matching launch and impact reports when the event callback has not already requested one. Silent volley partners stay silent; destroyed launchers cancel pending audio; re-entering an impact cannot replay it. Five enemy/ally gun call sites now use enemy gun cues rather than Cole's suppressible player weapon cue.

Aliases reuse the existing recording pools, retrigger gates, mute/volume controls and voice budget. No new audio files, runtime projectile scan or extra audio bus. Explicit caller audio and mixer-throttled requests suppress fallback duplication.

## Verification and limits

- Required test_fl suite: 8,700 checks, zero errors, final BUILD OK, exit 0. Historical assertions requiring the deliberately removed arrows now assert FOV presentation and keep the bounded-warning-sound regressions.
- Eleven edited runtime scripts pass syntax checks. game.js remains LF; test_fl.js remains CRLF. Scoped whitespace check accepts their existing line-ending conventions.
- Native Edge: 372 checks pass, zero page/console/media errors. 329 short scene samples: all 185 current BOF catalogue entries on Normal, plus all 48 encounter/rebel/password entries on Easy, Hard and Furious.
- Stage 2's actual anchored-lane warning renders green/yellow/red FOVs on all four difficulties; screenshots inspected. Native Stage 4, Stage 6 and Stage 8 miniboss captures inspected too. Hammer chain warnings and actual shield-absorption audio requests explicitly exercised on all four difficulties.
- Eight new sound routes show advancing decoded playback, nonzero captured signal and positive volume. Silent partners, duplicate prevention, no audio from rendering, cancellation and Cole/enemy separation pass. Live SFX remain within the existing 64-voice budget.

These are bounded native encounter samples and focused fixtures, not exhaustive attack-cycle coverage, full campaign clears, hardware listening tests or new balance claims. Music/intro-only samples are not evidence of a complete combat cycle. No new gameplay difficulty changes are claimed.

Evidence: docs/qa/combat_fov_audio_1015.json (source hashes included). Reusable owner probe: _BUILD_SOURCE/probe_fov_audio_1015.py; set BOF_ALL_TIERS=1 for the complete roster pass. Captures and complete logs: _shots/fov_audio_1015 and _shots/fov_audio_1015_native.log / fov_audio_1015_suite.log.
