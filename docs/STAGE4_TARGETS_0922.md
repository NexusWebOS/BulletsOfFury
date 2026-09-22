# Level 4 target size and warship projectile repair — September 22

- [x] Olive Warden enlarged from 210×216 to 262×270 (about 25%). Its patrol, warning lane and glide use the visible arena; its resting altitude leaves the full hull visible. Its authored ram and offscreen return remain intact.
- [x] Warden gunner/rocket escorts enlarged by 50%, from 88/80 to 132/120 pixels. Damage bounds, missile targets, muzzle offsets and health-bar positions follow their size. Movement keeps the enlarged hulls within the visible arena.
- [x] Warship helpers doubled from 52.8 to 105.6 pixels. Their barrel sockets, overlays, point/beam/flame hit extents and Retina targets scale together. Rotated extents and larger formation/edge margins keep diagonal helpers hittable and visible.
- [x] Fixed missing beam and flamethrower collision routes for Warden escorts away from the central miniboss hull. Avoided duplicate beam hits where an escort overlaps that hull.
- [x] Warship-fired projectiles cannot be destroyed by player bullets, beams or orb projectiles. Chromium reflection and rolling-ball cancellation also respect the projectile protection. Other encounters retain their interception mechanics; defensive screen-clearing specials retain their existing behavior.

## Verification

`_BUILD_SOURCE/probe_stage4_targets_0922.py` uses real Chromium with empty temporary storage. All 16 native weapon-damage cases passed: machine gun, spread, travelling laser, passive missile, Retina missile, beam, flame and orb against both escort families. Warship rounds survived bullet/beam/orb overlap; the Warden control rounds remained interceptable. Chromium reflection also left warship rounds intact. Guided missiles were followed through actual impact on moving targets.

Thirty seconds of Furious miniboss simulation reached burst, center, rockets, circle, glide, warning, ram and return, including two rams. Non-ram patrol samples stayed within the visible arena. Inspected real screenshots of the miniboss/escorts, warship helpers and enraged diagonal helpers. Page and console errors: zero. Evidence is under `_shots/stage4_targets_0922/`.

The existing helper-blockade assertion now checks actual movement and screen-edge clearance instead of requiring the old 105-pixel formation margin. No new art or sound generation. No commit or push.

Final syntax and targeted whitespace checks pass. Full suite reaches its summary and exits **1 with 76 failing assertion names**, all in the recorded 76-failure baseline. No new failures. Gameplay LF and test harness CRLF line endings preserved.
