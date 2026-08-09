# PASSOVER — drop 0807d   (PILOT CARDS: TIMING, FIT, AND A LIVE EXCEPTION)

Build: `BulletsOfFury_0807d`
Harness: **2,106 assertions / 192 sections / 0 failing**, twice, reaching the banner.
Full verification: **PASS — playable, every graphic resolves.**

---

## 1. ⚠ A REAL EXCEPTION WAS FIRING ON EVERY STAT SEGMENT

Found while probing the card, not while looking for it:

    if(Audio.SFX.statTick) Audio.SFX.nsp_console_beep(...)

It **guards on `statTick`** — which exists — and then **calls `nsp_console_beep`**, which exists
nowhere in the file. So every segment of every stat bar raised a TypeError. At the old 46ms
segment pitch that is roughly 22 exceptions per second for the whole bar fill, on the select
screen. That is very likely a real part of the sluggishness.

It survived because the name it TESTS is real and the name it CALLS is not — a guard that cannot
protect the thing it guards.

## 2. THE TEXT: 9.93 SECONDS TO 2.48

Mike: *"the text loads in way too slow on all cards."* Measured before touching it:

    cole 9.93s · lizzie 8.58s · juggernaut 8.18s · falva 7.82s · decker 7.73s
    freezer 7.42s · axel 5.99s · maverick 5.49s · yuri 4.97s

Cole's 275 characters took 6.55s at 42 cps, and his stat bars added 3.38s. Retimed to 180 cps /
14ms segments / 0.04s gaps — the flourish still reads as a Mega Man X reveal, letters still land
one at a time, bars still fill segment by segment. Worst card is now **2.48s**, median ~1.9s.

## 3. THE EMBLEM WAS FITTED CORRECTLY INTO THE WRONG BOX

Mike: *"rescale and place their affiliation signs inside to scale to fit, not cut off."*

`PEMB_INK` and the aspect fit were both fine — I checked the ink rects against their atlas cells
first and all nine fit. The **socket rect** was wrong. Zooming the socket on the 1448x1086 shell
with a percentage grid shows the bevel interior ends at **x 0.947, y 0.902**. The code used
**0.9758 and 0.9659** — reaching 2.9% of the card width and 6.4% of its height past the bevel,
into the frame moulding. No amount of fit-tuning could fix a correct fit into a wrong rect.

## 4. THE TEXT COLUMN WAS USING A THIRD OF THE CARD

`RW_X1` was held to 0.845 to clear the emblem — but the emblem only occupies the BOTTOM of the
window, from y 0.776 down. Everything above it had the full bay free and was not using it.

The column runs to **0.945** now and steps back to 0.845 only where the socket is actually in the
way, via `bwAt(y)`. That is ~32% more line width for the bio and the ability row.

The SPECIAL ABILITY row is also pinned above the bottom bevel rather than drawn wherever the stat
block happened to end — with five stats it could already be past the card edge. If the stats run
long the row now rides up over them, because a special the player cannot see is worse than a
tight column.

## 5. ⚠ THE HOTSPOT PROBLEM IS NOT FIXED, AND HERE IS THE NUMBER

    the menus TOUCH        399 keys · 34 Mpx
    the menus DOWNLOAD     7 sheets · 46 MB

    weak hotspot (1.5 Mbit)   245 s
    ok hotspot   (5 Mbit)      74 s

**The grouping is the cause.** A sheet is bucketed `common` when its art is touched by two or
more STAGES — which sweeps gameplay art into the sheets the menus need. `nst8_master` (a stage-8
backdrop, 2.88 Mpx), the water sets and the quadlaser FX are all sitting in sheets the select
screen has to pull before it can draw.

I downscaled the pilot cards while I was in there — they were stored at 1448x1086 and drawn at
479x359, **9.1x the pixels needed** — which took the sheets from 315.8 MB to 303.0 MB. But only
one card was in a menu sheet, so the select-screen download barely moved: 46.9 -> 46.0 MB.

**The fix is a regroup, not a rescale:** bucket a key as `ui` if the menus touch it AT ALL, even
when stages use it too. Duplicating a few hundred shared cells is cheap next to making the menus
wait on stage backdrops. I have the capture data to do it and did not want to start a regroup
without saying so first — the last two both duplicated art in ways that took a while to find.

## 6. STILL OPEN

* The menu regroup above — the actual answer to the hotspot.
* Flame / ice fade-on-release · miniboss slow · stats-screen alignment · helix burst POSITION.
* `UNUSED_ART_CANDIDATES.txt` — 868 families awaiting your confirmation.
