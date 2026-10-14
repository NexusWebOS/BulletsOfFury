# Storm Sovereign core access and electrical ordnance — October 13

The four electrical generators now translate with the Sovereign's hull. The
October 11 layer had pinned them to the boss's first world position while its
attack stations continued following the camera; panning could move the hull and
its shield across a generator. Render, collision, and Retina now read the same
boss-relative sockets, finalized after the native attack controller moves.
Helpers stay between the upper and lower sockets without the old vertical bob.
Their separate health, guns, and damage routing remain intact.

The core-ball and final-pursuit attacks already assigned `lightning`, but the
shared projectile renderer interpreted every non-ice value as a magma ball.
All Sovereign orb constructors now identify their shots as electrical ordnance;
the renderer uses the existing sixteen-frame `s4w_lightning_ball_*` reel.
Interceptions use the authored lightning burst and electric sound, including
the large fusion shot's split balls and the final pursuit. Ordinary bullets and
missiles retain their own identities. No new artwork, HP, damage, attack timing,
or phase changes were introduced.

Runtime: `assets/s4_core_access_1013.js`, included after the older combat layers.
No shared `assets/game.js` edits are required.

## Native verification

`_BUILD_SOURCE/probe_s4_core_access_1013.py` runs the actual game in Edge. All
121 checks pass with zero page/console errors across Easy, Normal, Hard, and
Furious. Each difficulty checks:

- All four core positions, native point targeting, Retina validity, and real
  ordinary-bullet damage at left, middle, and right camera positions.
- A twelve-second continuous native camera sweep: clear approach lanes, stable
  locks, and smooth generator positions. Native curved missiles reach an upper
  core; held beams destroy only the selected core column.
- Helper hull/collider separation, stale target rejection after destruction,
  and the current 75%/50% reconstruction cycles with no premature locks.
- Real core-ball, fusion split, and final-pursuit controllers. Native draw calls
  select electrical frames, never fireball frames; ball positions remain finite
  and actual electrical interception dispatch remains active.

The initial held-beam fixture deliberately skipped boss entry but also marked
engagement complete, leaving the controller's old offscreen recovery origin.
This was a fixture error: running native `er26Tick(b,0)` after entry setup resets
that origin normally. Final results use that native engagement path.

Native screenshots were visually inspected, including the electrical reel,
both camera extremes, and the helper arrangement. These are protected combat
fixtures, not full human clears or a survival-rate claim. The parent task owns
the required complete game regression run and combined handoff.

Portable results: `docs/qa/s4_core_access_1013.json`.
Images: `_shots/s4_core_access_1013/msedge/`.
Reproduce: `python _BUILD_SOURCE/probe_s4_core_access_1013.py --browser msedge`.
Local work only; no commit or push.
