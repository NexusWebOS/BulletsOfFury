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

## Stage 8 Vile aimed-fan follow-up

RAVENOUS ASCENDANT now commits its five needle paths before a 0.62-second shared warning, and FURIOUS DEATH commits its seven gunship paths before a 0.58-second warning. The original projectiles, speeds, alternating hardpoints, muzzles and total cooldowns remain unchanged. The second form's paired homing missiles retain the shared Retina rule and begin their lock only when the warned fan releases. Chromium passes 23/23 and focused section 345 passes 10/10. See [STAGE8_VILE_AIMED_FAN_WARNING_0916.md](STAGE8_VILE_AIMED_FAN_WARNING_0916.md).

## Stage 8 ABYSSAL LEVIATHAN solar-wheel follow-up

The third Vile form now commits all nine original solar-wheel angles before a 0.62-second shared warning. It retains the original 0.19-radian rotation step, equal spoke spacing, center hardpoint, authored solar rounds, speed 2.45, muzzle and 0.95-second total cadence. Chromium passes 16/16 and focused section 346 passes 8/8. See [STAGE8_VILE_SOLAR_WHEEL_WARNING_0916.md](STAGE8_VILE_SOLAR_WHEEL_WARNING_0916.md).

## Stage 8 FURIOUS DEATH straight-missile follow-up

The final Vile form now commits all four original vertical missile lanes before a 0.58-second shared warning. Its missile budget, four hull offsets, armored-gunship muzzles and 0.78-second total cadence remain intact. The missiles remain shootable and straight, with no Retina or homing grant after Stage 1. Chromium passes 16/16 and focused section 347 passes 9/9. See [STAGE8_VILE_MISSILE_SALVO_WARNING_0916.md](STAGE8_VILE_MISSILE_SALVO_WARNING_0916.md).

## Stage 6 Doomsday Carrier twin-cyclone follow-up

The Doomsday Carrier Mk II now commits the exact six paths from its twin rotary batteries before a 0.62-second shared warning. The left and right hardpoints retain their mirrored three-lane offsets, authored cyclone rounds, base speed, muzzle reels and phase-specific total cadences. The warning origins follow the moving hull while the six aim angles cannot chase a late dodge. Chromium passes 16/16 and focused section 348 passes 10/10. See [STAGE6_CARRIER_CYCLONE_FAN_WARNING_0916.md](STAGE6_CARRIER_CYCLONE_FAN_WARNING_0916.md).

## Stage 6 Doomsday Carrier storm-node follow-up

Both shield-down Carrier phases now commit the alternating storm-node pair and all six or ten original fan paths before a 0.62-second shared warning. The paths stay anchored to moving nodes while their aim angles and parity remain committed. Destroying a warned node disarms only its lanes, and phase changes cancel stale fan warnings. Original speeds, offsets, cadences and the central prism-lance beat remain intact. Chromium passes 16/16 and focused section 349 passes 11/11. See [STAGE6_CARRIER_NODE_FAN_WARNING_0916.md](STAGE6_CARRIER_NODE_FAN_WARNING_0916.md).

## Stage 6 Doomsday Carrier prism-crossfire follow-up

The Carrier's Phase 5 four-barrel prism crossfire now commits all four upper-hardpoint paths before a 0.62-second shared warning. Origins follow the hull while the alternating outward/inward angles remain fixed. Authored prism rounds, speed, muzzles, sound and total cadence remain intact, and a phase transition cancels any pending crossfire. Chromium passes 16/16 and focused section 350 passes 12/12. See [STAGE6_CARRIER_PRISM_CROSSFIRE_WARNING_0916.md](STAGE6_CARRIER_PRISM_CROSSFIRE_WARNING_0916.md).

## Stage 6 Doomsday Carrier gravity-mine follow-up

The Carrier's Phase 5 paired gravity mines now commit their two crossing paths before a 0.72-second shared warning. Origins follow the left and right mounts while both angles remain fixed. Authored gravity mines, slow acceleration, capped speed, scale, muzzles, sound and total cadence remain intact, and phase transitions cancel a pending warning. Chromium passes 16/16 and focused section 351 passes 11/11. See [STAGE6_CARRIER_GRAVITY_MINE_WARNING_0916.md](STAGE6_CARRIER_GRAVITY_MINE_WARNING_0916.md).

## Stage 6 Doomsday Carrier omega-bomb follow-up

Both Last Run omega-bomb variants now commit their center corridor before a 0.66-second shared warning. The origin follows the moving center cannon while the downward angle remains fixed. Authored omega art, both base speeds, acceleration, speed cap, scale, muzzle, sound and total cadences remain intact, and phase transitions cancel a pending warning. Chromium passes 16/16 and focused section 353 passes 11/11. See [STAGE6_CARRIER_OMEGA_WARNING_0916.md](STAGE6_CARRIER_OMEGA_WARNING_0916.md).

## Stage 6 Doomsday Carrier mirrored cluster-fan follow-up

The Last Run cluster fan now commits all six mirrored paths before a 0.62-second shared warning. Origins follow the moving left and right mounts while the three angles on each side remain fixed and preserve the open center escape wedge. Authored cluster bomblets, speed, muzzles, one release sound and total cadence remain intact, and phase transitions cancel a pending warning. Chromium passes 16/16 and focused section 354 passes 11/11. See [STAGE6_CARRIER_CLUSTER_WARNING_0916.md](STAGE6_CARRIER_CLUSTER_WARNING_0916.md).

## Stage 6 Doomsday Carrier chrome-flak follow-up

The Last Run chrome-flak pair now commits both shell paths before a 0.62-second shared warning. Origins follow the moving lower-inner hardpoints while the angles remain fixed. The unreachable outer `-18°/+18°` pair is restored and alternates with the inner `+10°/-10°` pair. Authored shell and burst art, speed, 0.64-second fuse, five fragments per shell, muzzles and total cadence remain intact. Chromium passes 19/19 and focused section 355 passes 13/13. See [STAGE6_CARRIER_FLAK_WARNING_0916.md](STAGE6_CARRIER_FLAK_WARNING_0916.md).

## Stage 7 Toxic Portal Warden cripple-rail follow-up

The crippled Warden now commits a complete rail group before a 0.58-second shared warning. Four fields preview the alternating straight singles and paired offset finisher. Their origins follow the crawling hull while their angles remain fixed; the next group samples a new aim only after the prior group completes. Authored rail spears, cannon mounts, speeds, offsets, muzzles and sound remain intact. Chromium passes 18/18 and focused section 356 passes 13/13. See [STAGE7_WARDEN_CRIPPLE_RAIL_WARNING_0916.md](STAGE7_WARDEN_CRIPPLE_RAIL_WARNING_0916.md).

## Stage 5 Chrome Hammer Archmage spiked-ball follow-up

The Archmage now commits its spiked-ball launch direction and exact first wall impact before a 1.25-second shared green/yellow/red warning. The corridor and first bounce remain fixed through player-driven camera movement; later reflections retain the original dynamic screen bounds. Authored ball art, base velocity, duration, missile knockback and rage behavior remain intact. Chromium passes 18/18 and focused section 357 passes 10/10. See [ARCHMAGE_SPIKED_BALL_WARNING_0916.md](ARCHMAGE_SPIKED_BALL_WARNING_0916.md).

## Stage 5 Archmage fused mega-wave follow-up

The restored Easy/Normal post-chaingun form now previews the complete fused mega-wave damage corridor through the shared green/yellow/red system for 1.65 seconds. The beam remains harmless until red completes. The same batch repairs the missing `core_orbit` controller with authored blue core effects and prevents destroyed module targets from returning. Chromium passes 22/22 and focused section 358 passes 10/10. See [ARCHMAGE_CORE_RECOVERY_0916.md](ARCHMAGE_CORE_RECOVERY_0916.md).
