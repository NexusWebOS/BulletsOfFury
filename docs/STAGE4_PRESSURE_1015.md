# Stage 4 combat pressure repair — October 15, 2026

The Warden miniboss now attacks independently of its south-entry jets. Starting,
flying, firing and retiring an escort wave never resets the miniboss attack clock.
Its guns and missile boxes keep their own warnings, committed targets and releases.
This supersedes the separate-turn tuning recorded in WARDEN_READABILITY_1014.md.

| Difficulty | Main warning | MG rounds / cadence | Missile waves | Recovery | Jet entry / warning | Jet rounds / cadence |
| --- | --- | --- | --- | --- | --- | --- |
| Easy | 1.45 s | 8 / .16 s | 1 | .95 s | 1.25 / .80 s | 6 / .18 s |
| Normal | 1.25 s | 12 / .12 s | 2 | .80 s | 1.15 / .70 s | 8 / .15 s |
| Hard | 1.10 s | 16 / .09 s | 3 | .65 s | 1.05 / .60 s | 10 / .12 s |
| Furious | .95 s | 20 / .07 s | 4 | .50 s | .95 / .50 s | 12 / .10 s |

Jets use the existing camo heading bank at the approved 96px combat size, family
health, enlarged shadowed entry, and native hit flashes. They turn at 10 radians
per second, strafe while firing at a committed point, and peel out on their own
continuous exit path. Entry remains harmless while above the combat plane.
Camera-hidden or destroyed jets cannot emit unseen shots. Escort waves remain
bounded to one aircraft on Easy and two otherwise; they can overlap main fire.

The Sovereign's four detached shield generators follow its position and depth
scale while retaining upright positions and plate orientation through hull turns.
Their independent internal energy animation remains. Mounted guns, missile boxes
and the central reactor still rotate with their actual hull hardpoints. Existing
collision, generator damage and Retina targets use the same node coordinates.

The Sovereign helpers previously received an unconditional overheat state every
frame, preventing their guns from running. They now own independent warning,
firing and cooling clocks, emit from their visible rotating barrel sockets, and
play native enemy gun audio and authored muzzle effects. Their warning lanes
also render while the main hull recovers. Pressure increases through all four
difficulties. Each helper retains its shield, hull, destructible gun and hit
feedback. Destroyed guns stop firing. Rearming, materialization, overhead depth
and camera-hidden placement suspend fire and require a fresh warning on return.
The legacy helper enrage controller is retired while this controller owns them.

Runtime owner: assets/stage34_assault_1014.js. No art, atlas or game.js edits.
The shipping index updates this module's cache version. Unrelated local tutorial
and project work remain outside this release.

Verification uses _BUILD_SOURCE/probe_stage4_pressure_1015.py plus the existing
Stage 3–4 combat/visual probes and required full test_fl suite. Native fixtures
inspect rendered warnings, moving projectiles, muzzle flashes, hit feedback and
sound output, as well as attack timing. This is targeted combat verification,
not a complete human campaign-clear claim. See docs/qa/stage4_pressure_1015.json.

Final verification: 50/50 focused native checks, 60/60 existing Stage 3–4 combat
checks and 13/13 existing visual checks, with no browser errors. The final full
suite reaches 8,700 passing assertions and BUILD OK / 0 ERRORS, exit 0. Native
screenshots of concurrent fire, active helper barrels and upright cores were
inspected. Runtime SHA-256 is recorded with the focused QA evidence.
