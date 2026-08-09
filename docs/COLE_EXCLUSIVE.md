# COLE — LOCKED PILOT + EXCLUSIVE TIERS 6-8 (drop 0801k)

    verify 121 passed / 0 failed

## He really had been unlocked the whole time

    let coleUnlocked=false;
    try{ coleUnlocked = localStorage.getItem('bof_cole')==='1'; }catch(e){}   <- read on boot
    ...
    coleUnlocked=true; localStorage.setItem('bof_cole','1');                  <- written on unlock

Typing COLE4U once unlocked him permanently on that machine. Mike: *"never save his unlocked
status to gamedata or anything. this is a pure password developer feature."*

Both the read and the write are gone. Every session starts locked; the code has to be typed again.
Asserted both ways — the source is checked for `localStorage.getItem('bof_cole')` as well, because
removing only the write would have left him unlocked from an existing save.

The LOCKED card is registered and draws in place of his card, with the reveal suppressed — there
is nothing to type out.

## NOBODY ELSE, EVER

One gate, `coleTier()`, applied INSIDE `pShoot`. Driven with a real pilot in the harness:

    falva -> coleTier(6,7,8) = 5,5,5     capped, whatever is passed in
    cole  -> coleTier(6,7,8) = 6,7,8

Because the cap is inside the fire function rather than at the pickup, no path that reaches
pShoot can route around it. **VS mode works** — the pilot is still Cole there, and the gate asks
the pilot, not the mode.

## The tiers

    LV6  GOLD TRIDENT    the level-3 gold triple, plus 3 homing rounds
    LV7  BLACK TRIDENT   4 rounds abreast, black shell with a white core, plus 4 homing rounds
    LV8  FUSION CANNON   hold to charge 1.15s, release TWO piercing purple lances

**The arch is the point.** The trident rounds leave SIDEWAYS (`side*TRI_ARCH`) and do not steer
for the first 0.16s. That gap is what makes them read as a separate weapon that then hooks, rather
than as bullets that were always homing.

**The black tier's glow moves.** Two passes: the sprite crushed to near-silhouette, then a small
bright core drawn INSIDE it that drifts on its own clock. A highlight painted on would sit still;
this reads as something travelling within the round.

**The fusion lances PIERCE.** No per-hit removal — that is the whole character of the weapon. You
line the shot up and it goes through the row instead of trading with the first thing it meets.
Drawn from the real green-laser art hue-rotated to purple, so it keeps the beam's own shading.

## The charge, and why that art

Mike: *"there was a charge animation not the circle orbs, but the one that surrounds the ship."*

`fchg_0..3`, and the measurement confirms the choice:

    fchg_0        ink 0.044   centre 0.011   HOLLOW — built to sit AROUND a hull
    nchgF_0       ink 0.841   centre 0.688   filled
    nchg_orb_0    ink 0.683   centre 0.975   filled

The orbs are solid at the centre, which is exactly why they always read as pasted on top of the
ship instead of wrapped round it.

Frames 0-2 step with the charge. **Frame 3 animates itself** at full charge — a scale breathe plus
a slow counter-rotation, driven by sprite manipulation rather than more drawn frames. That is
Mike's *"make the 4th charge frame animate on it's own"*, and it costs nothing.

Cole gets it green/grey; **Falva now uses it too, in its default colour, replacing the circle orbs**.

## Icons

Recoloured from `micon_mg_5` so they read as the same family, with the numeral stamped and
outlined so it survives on any tier colour. Measured after: gold hue 30, black at value 0.15,
purple hue 270.
