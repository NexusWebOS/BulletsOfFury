# Shared non-laser warning repair — September 15, 2026

The shared green/yellow/red field now owns the Stage-1 Jungle Overlord-X charge.
The cone tracks the player while green, commits its lane during yellow, flashes red
before release, and carries the matching authored warning sign above the helicopter.
The charge then travels down that fixed lane and cannot steer into a late dodge.
Overlord-X now layers its encounter-specific eight-beat red beacon over this shared
color progression; other shared warning users retain their one-shot alert behavior.

This pass also removed an engine naming collision. A later mech drawing function had
the same `bossTelegraph` name as the old generic warning setter, so JavaScript hoisting
made that setter unreachable. The mech renderer is now `mechBossTelegraph`; the dead
procedural ring and its render-time simulation tick are retired. Dangerous attacks use
`combatWarningTick` and `combatWarningDraw`, whose warning lifetime now warms the
authored art once and explicitly closes at release. Field and alert layers can be drawn
separately so the lane stays below the hull while the sign remains visible above it.

The wider ENG-02 migration remains partial. Chrome Hammer, Xeno Regent, Furnace eyes and
the accelerating Furnace rollerball, Stage-3 central pulse and Jungle Overlord-X use the shared rule; remaining dangerous
non-laser boss and miniboss attacks still need encounter-by-encounter review.

## Verification

- `node --check assets/game.js` and `node --check _BUILD_SOURCE/test_fl.js` pass.
- The latest dependent full suite reached its summary with **4,042 passed / 57 known failures**, exit 1.
  No new failure name appeared; the randomized Stage-1 sand-tank timing assertion
  failed on this run.
- Real Chromium proof is **12 / 0** with zero page, console or controlled-loop errors.
  It opens the native Stage-1 boss route, decodes the authored plates, captures all
  three field phases and the committed dash, and checks the warning clock and lane.
- The four 960×1024 captures were visually inspected. Green and yellow warning signs
  remain over the hull, the cone is unobscured below it, red shows the final committed
  lane, and the release frame shows the helicopter descending along that lane.
- Runtime remains LF-only; the suite remains CRLF-only.

Proof: `docs/qa/shared_nonlaser_warning_0915.json` and
`_shots/shared_nonlaser_warning_0915/`.

The dependent Furnace rollerball pass adds a committed horizontal corridor through the
same warning renderer. See `docs/FURNACE_ROLLERBALL_0915.md` and
`docs/qa/furnace_rollerball_0915.json`; its native Chromium proof is 14/14 with zero errors.

No atlas, source-art, balance, Git, or save-data operation was performed.
