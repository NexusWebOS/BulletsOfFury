# Lizzie combat pattern laboratory — 2026-09-01

This is an isolated gameplay prototype based on the twelve-recording reference study. It loads the
shipped Stage 1 runtime, Stage 1 field, Lizzie ship, Lizzie level-1 machine gun, and existing enemy
and Jungle Overlord-X art. Experimental movement, projectiles, and encounter scheduling live only
in `_BUILD_SOURCE/qa_pattern_lab_0901_lab.js`; `assets/game.js` was not changed for this demo.

The point of this pass is to test the *combat grammar* before production integration: formation
spacing, committed aim, projectile speed bands, readable boss movement, safe-lane promises,
independent hardpoints, and damage states that alter attacks.

## Captured sequence

| Beat | Prototype behavior | Tuned values | Why it belongs in Bullets of Fury |
| --- | --- | --- | --- |
| Reserved formation pass | Four camo jets enter as one authored unit, swerve through their own slots, sample Lizzie once, fire, and leave. | 111 px slot spacing; six-round bursts; 0.10 s intra-burst gap; 305 px/s tracers. | Fast run-and-gun pressure without plane stacking, random wobble, or permanent tracking. |
| Durable anchor + support | A jungle tank rolls south, pauses, fires, then recovers while two bombers provide short side pressure. | Tank cannon 188 px/s; support tracers 325 px/s. | A heavy ground unit owns one lane while aircraft create a temporary second question. |
| Boss reveal tell | Stage shutters open, the boss silhouette resolves, and every weapon stays cold during the recognition beat. | 1.38 s reveal; 0.75 s recognition hold. | The entrance becomes the first fair telegraph instead of a decorative cut immediately covered by fire. |
| Independent hardpoints | Jungle Overlord-X keeps a slow, predictable hull slide while its pods emit separate twin-MG, missile, and wind attacks. | MG 318 px/s; missile 118→215 px/s; missile turn 1.15 rad/s; curved wind 165 px/s. | The boss looks aggressive without making its full collision body dart unpredictably. |
| Shootable homing missiles | Large jungle missiles accelerate and steer, but Lizzie's real player rounds can destroy them before impact. | Two missiles fired from separate pods; two successful live-fire intercepts in the recorded run. | The large silhouette correctly promises an object the player can counter, not an invulnerable homing bullet. |
| Moving safe door | Six warned beam lanes commit after a readable delay. Exactly two adjacent lanes remain open; the second door walks only one lane. | 0.90 s warning; 1.25 s commitment; two-lane opening; one-lane maximum door movement. | Dense spectacle has an answer the player can read, execute, and predict on the next wave. |
| Local damage state | At critical health, one pod breaks, smokes, and stops firing while the surviving gun increases cadence. | One disabled hardpoint; critical hull plate; localized smoke; faster remaining MG. | Damage changes the encounter mechanically and visually instead of only palette-swapping or fading the boss. |

## What the reference footage says Mike is asking for

- Fast projectile play, but attacks fire in coherent bursts and shapes rather than unrelated noise.
- Aircraft fly deliberate curves and swerves; they never wobble or occupy the same unit-sized slot.
- Tanks remain south-facing, roll deliberately, pause to fire, and recover before the next commitment.
- Giant bosses slide slowly enough to read while pods, turrets, missiles, and arena dividers carry the complexity.
- Fast aimed fire samples a position and commits. The player can dodge after release.
- Large set-pieces promise a safe lane before becoming lethal and provide a real recovery beat.
- Boss reveals, transformed armor, disabled sections, smoke, and oversized destruction are gameplay communication.

## Automated capture result

- Pilot/runtime identity: `lizzie`, production game state `play`.
- Laboratory sequence: completed all six readability contracts.
- Prototype launches: 77; peak simultaneous laboratory threats: 24.
- Shootable missile intercepts by Lizzie's live bullets: 2.
- Beam openings: 2 lanes in both waves.
- Browser/runtime errors: 0.
- Missing asset requests: 0.
- Capture: 600×640 H.264 MP4, approximately 36 seconds after trimming browser startup.

Lizzie is invulnerable in this capture so one recording can show every phase; the autopilot performs
only local projectile dodges and the two authored beam-door moves. This proves sequencing,
presentation, asset loading, and counterplay hooks. It is not a final hitbox or difficulty-balance
certification.

## Files

- Demo page: `_BUILD_SOURCE/qa_pattern_lab_0901.html`
- Prototype controller: `_BUILD_SOURCE/qa_pattern_lab_0901_lab.js`
- Deterministic Playwright capture: `_BUILD_SOURCE/qa_pattern_lab_0901.js`
- Video: `docs/proofs/pattern_lab_0901/lizzie_pattern_lab.mp4`
- Contact sheet: `docs/proofs/pattern_lab_0901/lizzie_pattern_lab_contact.jpg`
- Machine-readable result: `docs/proofs/pattern_lab_0901/report.json`

These values are candidates for the production Stage 1 AI pass. None have been merged into the
shipping runtime yet.
