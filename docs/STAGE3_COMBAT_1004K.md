# Stage 3 recording pass â€” October 4

Mike's recording: `C:\Users\Mdogg\Videos\2026-10-04 19-56-14.mp4`
(13:15.30). The recording was sampled across its full timeline every twelve seconds,
then the Stage 3 miniboss and boss section from 9:50 onward was inspected every two
seconds. This is sampled visual review, not a claim of continuous playback or an
audio review. Contact sheets are retained under `_shots/stage3_combat_1004k/`.

## Changes

- Ordinary gun pellets, tank/boat ground shots, slugs, shards and laser lances are
  weapon-proof. Actual fire/ice balls and missiles remain interceptable. The separate
  `groundup` collision path now respects the same policy as the general bullet path.
  Bomb clears, Axel shield reflection and Chromium mirror reflection retain their
  original permissions; non-shootable gunfire still responds to those defenses.
- Both ordinary and large elemental balls can be intercepted. Impact uses existing
  authored fire/ice burst strips, ice debris, brief scattered residue, and the
  registered fire/ice impact sounds. Interception is idempotent and cancels pending
  targeted arrivals and legacy orb shard bursts. Making a ball shootable no longer
  replaces its authored velocity with generic missile steering/speed.
- Held flames use `flameHit`; sweeping fire whips use `fireWhipTouches` for ordnance
  interception. The visible authored weapon geometry owns the hit test.
- Frost Cruiser retains its ball, beam, missile and strafe attacks and adds a
  warned charge using Voss's `ra4DashSetup`. It tracks early, locks the target before
  release, charges once, then returns smoothly. No concurrent gun barrage during
  the charge.
- Rime Wall retains its battery, charged laser relay, crossfire and glacier press.
  It adds paired rocket-bank missile volleys and a deploying orbital-gun attack.
  `mr27Shape` owns the moving modules, so rendered turrets, muzzles, hit tests and
  missile targets share their position. Destroyed banks stop firing. Turrets return
  smoothly to the hull, including after a module-break interruption.
- Gun mounts aim at the pilot during warning acquisition. Charged lasers track
  during early warmup and lock at least 0.4 seconds before firing; they do not chase
  the pilot during the active beam.
- Spread Fire and shotgun releases follow the selected pilot's actual authored
  nose, including bank poses. The final renderer override measures each authored
  flare's base instead of relying on a fixed hull offset or stale reel padding.

Boss/miniboss HP, authored hulls, existing attack repertoire and the Furious
fire/ice transformation structure are preserved. No new art, atlas repack,
placeholder sprites or procedural effect plates were added.

## Implementation and verification

Runtime extension: `assets/stage3_combat_1004k.js`, loaded after the Rebel arsenal
extension. Shared bullet collision fixes are in `assets/game.js`; pilot nose
attachment helpers are in `assets/weapon_muzzles_0926.js`. Base game retains LF;
`_BUILD_SOURCE/test_fl.js` retains CRLF.

Syntax checks and the complete suite must reach the final summary. The initial
suite exited nonzero because its mock canvas lacked `createImageData`, now used by
the existing ship-frame compositor reached through the measured muzzle path.
Added that standard canvas API to the harness. This was a harness exception, not
a failed gameplay assertion; no recorded baseline failures were waived.

Native probe: `_BUILD_SOURCE/probe_stage3_combat_1004k.py`, using `shoot.py`, actual
Chromium, the game context, `XART.get` and real `drawImage`. It verifies six weapon
collision types, both elemental impacts, actual held-flame interception, preserved
ball velocity, actual damage against an orbiting gun, rocket banks, early laser
tracking/late commitment, charge movement, nine pilot muzzle attachments, and forty
seconds of live attacks for each encounter. Asset readiness is polled, frame batches
yield, and screenshots/page/console errors are captured. Initial probe issues were
an incorrect readiness key, incomplete fixture projectile fields, an intro state
left active, and premature timing assertions; corrected before final verification.

Playable review: `_shots/stage3_combat_1004k/review.html`, with Furious miniboss,
boss and full-stage buttons. Practice uses `map4hPreviewStorage` to isolate save
writes. Optional invulnerability is off by default. Stage 3's actual password remains
`DAM5`. Review buttons have their own native Chromium verification.

Final verification: 7,200 full-suite assertions, exit 0, final summary reached;
49 native combat checks and 4 playable-review checks passed, zero page or console
errors. Syntax checks passed for all three changed gameplay scripts.

Final results are stored in `docs/qa/stage3_combat_1004k.json`. Local and uncommitted;
no GitHub integration, commit or push performed in this pass.

Follow-up: Mike requested a 2-pixel rightward adjustment to the Spread Fire
muzzle. Both its initial and following player nose attachment now use that offset;
the nine-pilot Chromium comparison was refreshed.
