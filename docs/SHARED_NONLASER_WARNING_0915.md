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

## Stage 4 Sovereign follow-up

The unpowered Storm Sovereign ram now uses the same shared field and overhead alert. Its 0.40-second tracking window, committed lane and one-second release remain intact. An optional shared alert anchor places the sign below Stage 4's dual gauges so it is fully visible. Chromium 14/14 and focused section 332 8/8 pass. See [SOVEREIGN_SHARED_RAM_WARNING_0915.md](SOVEREIGN_SHARED_RAM_WARNING_0915.md).

## Razorback body-ram follow-up

The Razorback body ram now uses the shared green/yellow/red FOV and overhead alert. It tracks only during green, commits at yellow and holds through red and release on Normal, both independent Hard tanks and the Furious hyper tank. Chromium 15/15 and focused section 333 9/9 pass. See [RAZORBACK_SHARED_RAM_WARNING_0915.md](RAZORBACK_SHARED_RAM_WARNING_0915.md).

## Chrome Hammer leap/slam follow-up

The Chrome Hammer leap/slam now projects the shared green/yellow/red FOV and overhead alert down its committed travel corridor while retaining the authored landing reticle. The target is sampled once before the tell and cannot chase a late dodge. Its completed one-hand boomerang remains unchanged. Chromium 16/16 and focused section 334 7/7 pass. See [HAMMER_SHARED_LEAP_WARNING_0915.md](HAMMER_SHARED_LEAP_WARNING_0915.md).

## Toxic Portal Warden rail follow-up

The Stage-7 Toxic Portal Warden now commits its rail aim and safe-side gap when the 0.86-second charge begins. Five shared green/yellow/red fields preview the five spear paths and one matching alert renders in front of the giant hull. Chromium 15/15 and focused section 335 7/7 pass. See [STAGE7_WARDEN_SHARED_RAIL_WARNING_0915.md](STAGE7_WARDEN_SHARED_RAIL_WARNING_0915.md).

## Tidal Sovereign cascade follow-up

All four Tidal Cascade rows now commit a two-column opening, preview the other six exact release columns through a 0.62-second shared green/yellow/red warning, then move the opening by one column for the next warned row. Fields render behind the authored hull and the alert remains visible above it. Chromium 19/19 and focused section 340 9/9 pass. See [STAGE9_TIDAL_CASCADE_WARNING_0916.md](STAGE9_TIDAL_CASCADE_WARNING_0916.md).

## Stage 6 Thunderhead follow-up

All four live Doomsday Carrier Mk II Thunderhead rows now commit their two-column opening, preview the other six exact release columns through shared green/yellow/red fields, then move the opening one column for the next warned row. Chromium passes 19/19 and focused section 341 passes 12/12. See [STAGE6_THUNDERHEAD_WARNING_0916.md](STAGE6_THUNDERHEAD_WARNING_0916.md).

## Stage 5 Archmage boomerang follow-up

The active Chrome Hammer Archmage one-hand twirl now preserves the boomerang controller's committed vertical lane and floor reticle through the shared green/yellow/red warning. The alert is placed beside the boss to clear its destructible-module labels. Chromium passes 19/19 and focused active-render section 342 passes 6/6. See [ARCHMAGE_BOOMERANG_VISUAL_0916.md](ARCHMAGE_BOOMERANG_VISUAL_0916.md).

## Stage 7 DUAL SCOOP DREDGER minefield follow-up

The live Stage-7 miniboss now commits one safe column before its late-phase mine attack, previews the other five exact trajectories through a 0.86-second shared green/yellow/red warning, and releases the original five slow mines only after red. Late player movement cannot relocate the opening. Chromium passes 16/16 and focused section 343 passes 10/10. See [STAGE7_DREDGER_MINE_WARNING_0916.md](STAGE7_DREDGER_MINE_WARNING_0916.md).

## Stage 8 BLACK COCOON crescent-wall follow-up

The opening Vile form now commits its original wide center corridor and previews all eleven dangerous crescent columns through a 0.72-second shared green/yellow/red warning. Boss-clock changes and late player movement cannot move the opening; the original eleven authored crescents release only after red. Chromium passes 16/16 and focused section 344 passes 10/10. See [STAGE8_VILE_CRESCENT_WALL_WARNING_0916.md](STAGE8_VILE_CRESCENT_WALL_WARNING_0916.md).
