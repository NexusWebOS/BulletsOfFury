# BOSS WIRING — drop 0731v

    1335 assertions + 30, node --check clean, 12 bosses composite to master at diff 0

## Done this pass

**Debug overlay off.** `DBG.probe` was drawing the input/state readout over the play area.
Set false. `verbose` stays on but logs to console only, so nothing is on screen.

**Firewave flipped.** It was rotated 90 degrees and nothing else, which sent it across the screen
BASE FIRST. Measured: `nwf_fire_*` is 420x421 with 96% of its ink in the bottom half, so it is a
flame drawn base-down, exactly like the flamethrower art. It now flips vertically so the tip
leads, then rotates to its direction of travel.

**Tanks move like tanks.** Three states, no idle motion at all:

    ROLL    advances at 26 px/s
    BRAKE   decelerates at 54 px/s to a dead stop and holds
    STRAFE  turns and translates sideways at 9 px/s, always toward open ground

Never two strafes in a row — that would read as swaying. Tanks are excluded from the hover, and
their thrusters are suppressed, because a tank that hovers reads as a hovercraft.

Applies to the four tracked bosses: Obsidian Drill Tank, Glacier Rail Fortress, MIRV Stalker,
Legion Command Tank.

**Heads wired.** There are two per mech and they are not interchangeable:

    mbg2_head_intact     5861 px    position-locked component. Has damage states AND a neck socket.
    mbg2_p_head         12525 px    socket-free head from CF_GenesisBossHeads. Clean silhouette.

The floating head uses the socket-free one — a levitating head trailing a neck plug looks like it
fell off rather than like it is held. Once the head takes damage the render falls back to the
component, because the socket-free head has no damage states. Sized from the component's bounds
rather than its own, so it sits at the scale the boss was designed around.

**More HP on 2 and 3.** The Colossus was trimmed to 1.35x when it was a static hull. It now
assembles itself, tracks with two cannons and sheds limbs, so 1.35 -> 1.75. Cryo 2.5 -> 2.9,
nudged rather than doubled so the pair keep their relative weight.

**Stages 4 and 6 get the high-speed run.** `BOSS_SCROLL_MUL` is per stage now: 5.6 for 4 and 6,
3.2 everywhere else. The looping terrain scroll it drives was already built in the earlier
session for the Iron Revenant fight.

## Standing rules now in code

    tanks           roll / brake / strafe. never bob, never sway.
    mechs           hover on thrusters, arms and cannons move, head levitates
    snake (L7)      Mike's to animate — left static
    spider          Mike's to animate — left static
    barrels, drills, heads, tracks, hulls, wings   never move
    no derived cuts anywhere — components are drawn as they shipped
