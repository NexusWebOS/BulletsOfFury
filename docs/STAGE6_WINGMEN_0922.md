# Stage 6 independent squadron — September 22

Latest request: wingmen must fly independently, think for themselves, match the player's size, and support a more active level with side-entry ground-Retina bombing runs.

- [x] Removed player-relative formation anchors from ordinary combat. Each pilot owns a destination, velocity and target; moving the player only causes short-range hull separation.
- [x] All eight allies use `SHIP_DRAW_H` (60), exactly the player's hull draw height. The short rally and route-choice formation use arena positions, never the player's position.
- [x] Target selection spreads allies across enemies. They approach firing lanes, collect assigned supplies, anticipate projectiles, avoid ground strikes and nearby enemy bodies, and use authored roll/somersault frames. Movement has acceleration instead of instant sideways teleporting.
- [x] Friendly rounds now have native MG art, dimensions, damage and firing sounds. The old generic ally objects lacked the normal projectile kind and hitbox fields. Allies can take hits and withdraw when damaged.
- [x] Added four alternating side-entry bomber waves. Easy/Normal drop one rack, Hard two, Furious three; each rack commits a separate landing marker and leaves room to escape. Added runs respect the existing wave scheduler and bomber cap; at most six jet-bomb warnings are live.
- [x] Bombs visibly descend and rotate into authored ground-reticle strikes and impact bursts. Landing markers never chase the player. Warning durations are 1.65/1.45/1.25 seconds for Easy/Normal/Hard–Furious. Nearby bomb warnings share the missile warning scheduler, preventing overlapping beep sources.
- [x] Shared jet movement respects entry staggering and the Stage 6 art's south-facing source orientation, so bombers and dashers point in their travel direction. Radio lines stay readable longer.

## Verification

`node --check assets/game.js` passes. The full `node _BUILD_SOURCE/test_fl.js` reaches its final summary and exits **1 with 76 failures**, exactly the same failing assertion names as `_shots/stage6_cinematic_final_test_fl.log`. No new failures. `git diff --check -- assets/game.js` passes; other previously modified CRLF documents still produce unrelated whole-worktree whitespace reports.

Real Chromium probe: `_BUILD_SOURCE/probe_stage6_wingmen_0922.py`. Empty temporary browser storage; no user saves changed. Evidence in `_shots/wing_0922/`:

- Moving the player between opposite sides produced identical remote ally paths.
- All eight ally hull draws measured 60 pixels, with screenshots inspected.
- Native ally bullets reduced a live enemy from 200 to 192 HP.
- An approaching projectile triggered a real authored dodge.
- All four difficulty rack counts passed; warned coordinates remained unchanged; no strike damage before warning expiry.
- A Furious late-stage wave run reached route choice with seven allies still fighting and one withdrawn. Actual arrow-key input selected the left route. This is a targeted encounter check, not a complete campaign balance certification.
- Bomb source, direction of bomber travel, landing warnings, impacts, independent formation and combat screenshots inspected. Page/console errors: **0**.

No new art-generation credits used. No commit or push. Earlier repair backlog remains in `REPAIR_0922.md`.
