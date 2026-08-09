# PASSOVER — drop 0807q   (SHIP ATLAS ANSWERED, RANK UNTINTED)

Build: `BulletsOfFury_0807q`
Harness: **2,180 assertions / 201 sections / 0 failing**, twice, reaching the banner.

Mike came back with SIXTEEN items. This drop closes two of them — including the one he asked as a
direct question, because the answer determines whether he has to go looking for files.

---

## 1. THE SHIP ATLAS — ANSWERED, WITH THE EXACT LIST

Mike: *"you have an atlas of my ships with cut off frames. is that that the master sheet or do you
need those sheets?"*

**The atlas is not the problem. It faithfully contains what the individual ship files contain,
and two pilots' source frames are damaged.**

Measured by connected-component analysis on every barrel-roll cell — a clean roll frame is ONE
blob, a broken one has the wing floating as a second:

    pilot        br frames with DETACHED chunks    stray px
    axel              0/8                                9
    decker            0/8                                5
    freezer           0/8                                4
    juggernaut        0/8                                6
    maverick          0/8                                6
    yuri              0/8                               18
    falva             1/8                            1,219    (minor)
    cole              4/8                            1,230    <-- SOURCE SHEET NEEDED
    lizzie            2/8                            2,095    <-- SOURCE SHEET NEEDED

Six of nine pilots are perfectly clean, which is what proves the atlas mechanism is sound — if
the packer were cutting frames it would cut all of them equally.

**So yes: I need the sheets `ship_cole_br0..7` and `ship_lizzie_br0..7` were sliced from.** Nothing
else. The contact sheet shows it plainly — Cole's frames 2 and 3 have a wing floating clear of the
fuselage, Lizzie's frame 1 is missing a wing outright, and Yuri's eight are flawless.

This is almost certainly the "Cole looks clipped" report from earlier in the week: it only shows
MID-ROLL, which is why it looked intermittent.

## 2. THE RANK IS NO LONGER COLOUR-OVERLAID

Mike: *"Dont color overlay the rank please. just use the variant of that color for the passwords
and letters we have."*

Tinting a stage-font glyph washes its stone texture flat — the letter stops looking like the
game's font and becomes a coloured shape. The rank and the score draw untinted now. The password
keeps its two-colour flash, which is where he asked for the colour to live.

## 3. THE OTHER FOURTEEN, RECORDED

Nothing here is started. Grouped by what they actually are:

    SEQUENCE / ROUTING
      stage 1 intro should match stage 2's — runway, liquid flyover, centred start
      L2 miniboss spawns in a lava section AND the game switches sections to reach it.
        Mike's fix: no section swap. At the END of the level, tile an 800x480 lava frame,
        loop the vertical scroll, and run the boss there.
      no longer pulling up to the dam on the helicopter boss

    ENEMY BEHAVIOUR — the biggest of them
      stage 1 enemies are very broken
      jets still appear in thin air
      stage 2 enemies underwhelming in projectiles and behaviour
      "half like a shmup, half like high speed action"

    WEAPONS
      helix: STOP drawing the lance on top of the ball while charging and on release.
        It must detonate on IMPACT only, and the lances fire in volleys FROM the burst.
        ⚠ He has told me this more than once and it is still wrong.
      level 3 shows the iceorb icon when fireorb is what fires

    AUDIO
      an annoying noise every time a jet flies
      the flamethrower is silent

    MINIBOSS 1
      still no body glow / shield aura
      killing the inner turrets while the outer ones live looks wrong

    SET-PIECE
      the magma boss formation is right in the GIF and wrong in game

The helix is the one I would take next: it is a repeat request, it is specific, and I have twice
now believed it fixed when it was not.
