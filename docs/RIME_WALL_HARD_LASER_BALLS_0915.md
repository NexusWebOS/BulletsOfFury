# Rime Wall Hard Retina laser balls — 2026-09-15

## Result

Below half health on Hard and Furious, the Stage-3 Rime Wall now adds a paired laser-ball attack to both of its late combat patterns.

The attack:

1. Opens one shared Retina and queues two releases 0.24 seconds apart.
2. Fires the first ball from the physical left cannon and the second from the physical right cannon.
3. Uses the existing authored dark-blue Rime orb plate with a fixed silhouette, rigid rotation and a four-step additive pixel pulse.
4. Keeps each ball independently shootable with two hit points.
5. Lets the shared Retina steer both balls until they enter the normal commitment radius. A barrel roll or somersault started after lock breaks both at once.
6. Preserves the last heading after a broken or committed lock, so a successful dodge sends the threat off screen instead of allowing it to reacquire.
7. Omits missile exhaust. The first visual pass exposed orange exhaust inherited through the generic shootable-round path; the final pass retains only the authored blue laser-ball read.

Normal and the Stage-3 miniboss do not receive this attack. The existing below-half Rime Wall beam, halo and overdrive geometry remains intact, with the two delayed laser balls adding the requested second layer of laser pressure.

The following S3-13 pass found that the pair's calls were trapped in historical phase blocks below the live Rime Wall beam router. That integration gap is repaired in `RIME_WALL_FURIOUS_SIMON_0915.md`: the native Chromium proof now enters through `shipBossAttack`, verifies the pair on Hard/Furious, and verifies its absence on Normal.

## Verification

- `node --check assets/game.js` and `git diff --check -- assets/game.js` pass.
- Focused suite section 319: **12/12** assertions pass for difficulty/health/role gating, one-Retina ownership, staggered left/right release, authored art, homing, evasion break, shoot-down and offscreen culling.
- Full suite: **4,108 passing / 57 failing**, exit 1. Every failure name matches the established baseline, including the intermittent Stage-1 sand-tank timing assertion on this run.
- Real Chromium: **17/17**, zero page or console errors.
- The browser proof uses the native Stage-3 boss route, real Retina scheduler, real barrel roll, real player machine round, enemy-projectile collision and ordinary offscreen culling.
- Browser evidence: `docs/qa/stage3_hard_laser_balls_0915.json`.
- Screenshots: `_shots/stage3_hard_laser_balls_0915/rime_hard_retina_charge.png`, `rime_hard_first_laser_ball.png`, `rime_hard_laser_pair.png`, `rime_hard_tracking_pair.png`, and `rime_hard_roll_break.png`.
