# Enemy Combat Atlas — 13 October 2026

Open `OPEN_ENEMY_ATLAS.bat` from this checkout, or visit `enemy-atlas.html` on the
existing game server. Keep the server window open. The guide needs the game's
assets beside it; it is not a standalone single-file export.

The launcher uses `_BUILD_SOURCE/serve_bof_1013.py`: a loopback-only threaded
server with a larger connection queue and quiet successful-request logging.
This avoids rejected script downloads during simultaneous cold asset loads.

The guide contains 393 dossiers across BOF and Overdrive. Its default roster shows
185 current BOF entries and 31 current Overdrive entries. The optional archive
includes older constructors, replaced names and unverified historical encounters.
Those counts describe catalogue entries, including forms and password routes,
not 393 distinct campaign enemies. See `ENEMY_ATLAS_CATALOGUE_1013.md` for the census.

## Using the guide

- Search names, weapons or passwords, then filter by stage or category.
- The large viewport runs the real game update and drawing code. Watch native
  movement, weapon tells, muzzle effects, projectiles, transformation and recovery.
- Pause, advance one frame, replay, or select quarter/half speed and any of the
  four difficulty settings. Sound starts muted and can be enabled.
- Traveling shots observed in that scene appear as LIVE in the projectile cards.
  Continuous beams, contact attacks and private boss effects remain visible in
  the native viewport. Frame banks use the authored proportions and pivots.
- The observation target is invulnerable. Health adjustment is available for
  simple health owners; module-owned encounters label the control MODULES.
- Verified legacy constructors can be previewed. Unverified/replaced archival
  rows explicitly show their status and available art instead of claiming a
  working native scene.

The page reuses one live game iframe. Offscreen frame-bank/projectile cards are
not repainted, visible cards refresh at 10 Hz, and the native game keeps its own
frame cadence. Guide hooks load only for `?enemyAtlas=1`. Preview storage writes
are confined to the iframe's memory, leaving saved progress untouched. Musical
password bosses use the same cue tables and attack controllers with preview time
controlling both their cue clock and soundtrack position.

## Gameplay corrections delivered with this guide

- Rifle Locust fires alternating bullets from its surviving articulated barrels,
  with attached muzzle flashes, recoil and gun sounds. A destroyed barrel cannot
  fire; its pressure turn no longer substitutes a laser for the rifle weapon.
- Void Beacon fires its native eight-frame crystal shards, with matching crystal
  muzzle effects. Queued attacks also retain the crystal projectile identity.
- Warhive Siege Carrier uses wide burgundy/crimson beams, authored muzzle bursts,
  and front lenses/vents that animate through charge, fire, recovery and off.
  Destroyed guns stay dark. Its six-gun opening sequence and core access remain
  tied to the real weapon modules.

## Verification

- Required game syntax check and `_BUILD_SOURCE/test_fl.js`: completed with
  **0 errors**.
- Carrier: **219 checks** across Chrome, Edge and Firefox, including all four
  difficulty settings, weapon interruption and safe-lane measurements.
- Main-game roster: native render/spawn audits cover **256 retained ordinary
  entries**, including legacy-spawnable constructors, and **56 encounter/sample
  rows**. This is not exhaustive combat testing of the historical archive.
- Overdrive: **139 native checks plus 5 guide UI checks**, including its unit,
  boss, crew and convoy factories. See `ENEMY_ATLAS_OVERDRIVE_1013.md`.
- HAMMER/HAMA: pause, one-frame step, 2× clock, blocked autoplay and 40 seconds of
  native combat verified. Preview pausing freezes both pose and cue time.
- Parent page controls, switching between BOF/Overdrive, mobile width, and saved
  progress protection were checked in Chrome, Edge and Firefox.

QA reports live in `docs/qa`; reusable probes live in `_BUILD_SOURCE`.
Catalogue build tools live in `tools/enemy_atlas_1013`. Automated observation is
not a substitute for human difficulty or battery-powered laptop FPS testing.
