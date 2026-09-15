# Frost Cruiser Retina spiral volley — 2026-09-15

## Result

The Stage-3 Frost Cruiser now replaces its opening missile burst on Hard and Furious with one readable charged Retina sequence.

The attack:

1. Opens one player Retina and queues all six releases on that shared lock.
2. Charges both physical missile pods for 1.35 seconds with authored lightning while keeping the black/royal-blue difficulty hull readable.
3. Launches six independent rockets at 0.18-second intervals, alternating left/right/left/right/left/right from the actual pod mounts.
4. Gives each rocket its own phase on the existing frame-time-independent corkscrew path, producing two braided approach lanes rather than a stacked projectile.
5. Keeps every rocket shootable. A real player machine round was verified destroying one incoming rocket.
6. Binds all six rockets to the one Retina: the shared lock grants steering until the player's evasion breaks it or a rocket reaches its commitment radius.
7. Returns to the existing side-gun sequence after the bounded volley. Normal retains its established missile phase without the added Retina.

No new projectile sprite was added. The move uses the established missile plate, authored missile muzzle flashes, Retina family and chain-lightning charge art.

## Verification

- `node --check assets/game.js` and `git diff --check -- assets/game.js` pass.
- Focused suite section 317: **15/15** assertions pass for difficulty gating, one-Retina queueing, charge timing, six releases, alternating mounts, shootability, distinct spiral phases, shared lock ownership, speed, recovery and Normal isolation.
- Full suite: **4,086 passing / 57 failing**, exit 1. All failure names match the established baseline, including the intermittent Stage-1 sand-tank timing assertion on this run.
- Real Chromium: **14/14**, zero page or console errors.
- The browser run uses real `updatePlay`, the real player-lock scheduler, authored rendering and the actual player-bullet interception path.
- Browser evidence: `docs/qa/frost_cruiser_spiral_0915.json`.
- Screenshots: `_shots/frost_cruiser_spiral_0915/frost_spiral_charge.png`, `frost_spiral_first_release.png`, `frost_spiral_full_volley.png`, and `frost_spiral_intercept.png`.
