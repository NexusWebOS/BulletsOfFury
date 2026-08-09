# PASSOVER — drop 0808s   (THE TANK TABLE, AND ENGINE RULES)

Build: `BulletsOfFury_0808s`
Harness: **2,300 assertions / 209 sections / 0 failing**, twice, reaching the banner.

---

## 1. TANKS ARE A TABLE NOW

Mike: *"Make that for the black and regular colored tanks, and this should be a class or array
for tanks."*

`S1_TANKS` — eight rows, four vehicles in two paints:

    s1tankheavy      mg       48x64  hp16  460     s1tankheavy_b      hp20  560
    s1tanklight      missile  38x52  hp10  340     s1tanklight_b      hp13  420
    s1tankapc        kick     42x62  hp13  400     s1tankapc_b        hp16  500
    s1truckmissile   homing   44x62  hp12  520     s1truckmissile_b   hp15  640

The black ones are the SAME vehicle in night paint — same hull, same gun, same tracked movement.
Tougher and worth more because they are the later-wave version of the same threat, not a new one.
Asserted: matching attack and hull size across paints, black strictly tougher.

Adding a tank to any stage is now a row of data, not another case in a 200-line switch.

## 2. TRACKED MOVEMENT

    drive -> brake -> shift -> drive

It decelerates, sits still for 0.45s changing gear, then rolls the other way. Mike: *"if they move
backward or want to move backward they have to brake, adjust and move backward."* Modelled as an
explicit state machine rather than a velocity sign flip, because the PAUSE is the character — it
is what makes a tank feel heavy next to a boat that can simply slide sideways.

Verified on all eight: every phase reached, both gears used, correct attack, correct flash.

## 3. ENGINE RULES

    explosions      COVER_TARGET 1.79 -> 2.69, BIG 2.19 -> 3.29   (+50%, as asked)
    smoke rings     grow 1.15x -> 1.85x over 1.45s -> 1.9s        (mid pace, readable swell)
    shock rings     unchanged — they are the impact, they snap
    smoke rings now fire for jets as well as tanks, boats and minis
    muzzle flash    boats nmz_2 / nmz_4   ·   tanks nmz_1 / nmz_8

Scale lives on COVER_TARGET rather than per-unit size, so +50% is one constant and every blast in
the game moves together.

## 4. ⚠ TWO PLACEMENT TRAPS, BOTH THE SHAPE OF THE BOAT BUG

**The applier first landed in the art-picking switch** inside the unclosed if-block, where `c`
does not exist yet — ReferenceError on every tank. Same lesson as the boats: find the branch that
OWNS the object, not the first one that can reach it.

**`_selfPat` was hand-listed** with the four regular tanks. I added four black rows to the table
and they silently reverted to pattern `sine`, because the list did not know about them. It is
driven from `S1_TANKS` now, so any row added is covered automatically — which is the entire point
of making it a table, and it would have bitten again on the next tank.

## 5. NEXT

The jets. Mike: *"The way second wave worked is for jets."*

Still open: the boats and tanks drift downscreen rather than holding station — the scroll
cancellation sign. And no capture has yet filmed a smoke ring, because nothing has killed a unit
in front of the camera.
