# Stage 6 Tempest brothers

Mike approved integrating the black and gray Tempest ships into the current
Stage 6 miniboss encounter and keeping lasers clear of the MINI BOSS gauge.

`SUBBOSS[6]` now selects `tempestbrothers`. Blacksteel remains stored as
`ALTBOSS[6]`, and the original single black Tempest can still be spawned for
regression checks. Other stage assignments are unchanged by this integration.

The reviewed AI and authored gray hulls came from GitHub main
`f936f106d85d935aaf518fbac5ab34756bc26724`, under
`_STAGING/tempest_leviathan_0912u/encounter/`. Source and its original tests are
preserved in `_BUILD_SOURCE/tempest_source_0913/`. The native adapter is authored
separately there and embedded in the self-contained runtime by
`_BUILD_SOURCE/integrate_tempest_duo_0913.py`.

Each brother has its own 8,000-unit source hull pool, four 300-unit apertures and
75/50/25% phase gates. Pools map proportionally onto the game's final encounter
HP, including difficulty, threat, stage floor and co-op adjustments. The gauge
sums both ships. Hits and flashes affect the ship actually struck; the space
between ships has no collision geometry. Killing an aperture disables only that
aperture and deducts its reviewed 90-unit hull cost.

The original source black ship flies on one axis. Gray crosses diagonally, horizontally and vertically,
warns its inbound passes, makes pincers below black's rear laser lanes, and waits
offscreen during black's busy maneuvers. Native coordination also counts gray's
return/counterattack and its visible regroup as crossings; black waits until
gray actually clears the screen before warning a side ram. Native camera insets
keep black's full hull inside the view during its ram setup.

Mike subsequently approved south-facing hulls, rapid turns/slides, red-to-green
charge flashes and aimed afterburner passes for both active duo ships. This
supersedes the earlier fixed orientation and axis constraint for this encounter.
See `docs/TEMPEST_FIGHTER_0913.md` for the current movement and verification.

The survivor keeps fighting, with gray receiving its approved 15% speed increase.
Each defeated ship plays its falling reactor. Only after both are gone does the
normal miniboss slot release run once. Standalone `step` methods, including their
player input, collision and escape cinematics, are excluded from the embedded AI.
The adapter copies the pilot's position into an AI targeting object and never
writes the campaign pilot's position.

The game owns bullets, one retina per ship, delayed one-by-one shootable needles,
authored sprites, hit sounds and explosion sounds. Forward lasers end below the
77px gauge band. Duo drawing is clipped below that band under the real camera
and zoom transform, and the gauge draws after both ships in screen coordinates.

Verification is driven by `_BUILD_SOURCE/probe_tempest_duo_0913.py`. It launches
the real game through Boss Mode's warning/spawn route, checks motion, part pools,
ram coordination, the unit retina and actual gauge pixels, and captures the
renderer rather than the standalone preview. The compact demonstration uses an
invincible pilot and accelerated damage through `hitSubBoss` to show the entire
encounter. Its game sounds come from the existing frame-stamped capture and
OfflineAudioContext replay workflow. No trailer recordings are deleted or copied.

Artifacts and the complete suite log are under `_shots/tempest_duo_0913/`.
Final validation results are recorded in `docs/qa/tempest_brothers_0913.json`.
