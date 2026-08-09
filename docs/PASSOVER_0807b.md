# PASSOVER — drop 0807b   (MINIBOSS 1: TURRETS EXPLODE, HULL SHIELDS)

Build: `BulletsOfFury_0807b`
Harness: **2,080 assertions / 190 sections / 0 failing**, twice, reaching the banner.

---

## 1. A DEAD TURRET IS GONE

> "when we break its turrets make them explode not swap to that green plasma static image.
> They explode and disappear each."

Two things were drawing it after death: `nql_cannon_<id>_damaged`, a static ruptured plate held
for the rest of the fight, and a four-frame `nql_rupture_0N` overlay on top. That is the green
plasma smear.

Neither is drawn now. The turret detonates on the frame it dies and its plate stops existing —
a layered burst at the turret's own position (two explosions, a dense FX burst, ten thrown
sparks) instead of the single 46px pop it had. `c.rupt` is set to **-1** rather than 0, so
nothing can put a plate back.

## 2. THE HULL SHIELDS INSTEAD OF FLASHING

> "do not let the hull flash white until you break all the turrets, until then, just make it
> flash the shield color"

⚠ **The white was not `b.flash`.** Drop 0801kf had already replaced the full-sprite white tint
with an armour trace, and `b.flash` measures **0** on a blocked shot. The white you were seeing
came from the BURST FAMILY — `fxBurst(..., 'nxp_white', 0.35)` — a white explosion sprite fired
at the impact. That is why the earlier fix did not fix it.

The blocked burst is the blue-white `nxp_clus` family now, at 0.22 instead of 0.35 — a block
should feel like nothing gave. And the armour trace, which already existed, now has a STATE:

    a turret still alive   ->  shield blue  #7fd1ff
    every turret dead      ->  amber        #ffd27a

The colour change IS the signal that the hull became vulnerable. No HUD text needed.

## 3. THE BLOCKED SOUND

> "make a different sound that sounds like it blocked the shot, like a pitched version of one of
> our sounds."

Built from `hit()` rather than as a new asset: same square wave, but pitched from 1400 to 2350Hz
and given a **rising** sweep where `hit()` falls. A falling sweep reads as something giving way;
a rising one reads as something refusing to. Shorter and quieter, so a wall of blocked pellets
does not drown the fight.

## 4. VERIFIED IN A REAL FIGHT

Driven to the miniboss and shot:

    turrets fielded                    4
    hull damaged while a turret lives  false
    b.flash on a block                 0
    shield pulse fires                 yes
    hull damaged once all are dead     true
    dead turrets carrying a plate      none

## 5. WAITING ON YOU

The explosions — you said you were going to describe the pattern and I have not started them.
Nothing else in this drop touches explosion behaviour.
