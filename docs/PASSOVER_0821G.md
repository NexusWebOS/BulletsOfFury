# 0821g — THE CHARGE IS ANNOUNCED THREE SECONDS OUT

Mike: *"give enemies who charge at you some indicator to the player that they are going to 3
seconds before to get out of the way."*

`loopcharge` is the only pattern in the game whose airframe IS the weapon — it flies in, carves
one circle, then commits at the player with no projectile to dodge. It now announces itself.

    measured warning delivered, six runs:  3.03  3.28  3.63  3.78  3.33  3.60 s

---

## THE PLACEMENT CAME FROM MEASURING, NOT GUESSING

Timed the pattern before designing anything:

    run-in   1.80 - 2.60s   (varies with spawn height)
    circle   1.17s          (flat — it is one revolution)

So the charge lands **3.0-3.7s after the unit appears**. That is why the tell starts at SPAWN
rather than when the circle begins: it is the only placement that buys three seconds *without
touching the choreography*. Hanging it off the loop would have meant circling ~2.6 times to fill
3s, and 0819 is explicit that it is **ONE full circle**.

A floor holds the commit until 3.0s has actually elapsed — on the shortest run-in measured the
circle finished at 2.97s. It fires rarely and by a few frames, which is the point: the common case
is unchanged.

## ⚠ MY FIRST CUT DREW A WARNING YOU COULD MISS

Rendered in play, the ring was a dark maroon smudge. The cause was mine: the pulse
`0.55+0.45*sin(...)` **bottoms out at 0.10**, so the alpha at the sampled instant was **0.11** —
less than a fifth of a second before the jet committed. A warning that periodically disappears is
not a warning.

It pulses between BRIGHT and BRIGHTER now (`0.76+0.24*sin`), never between invisible and bright.
The pulse still quickens as the commit nears, because a static ring reads as decoration and a
quickening one reads as a countdown.

The tell also draws a lead line toward the player, so it says WHERE as well as WHEN — which is the
whole content of "get out of the way".

## ⚠ AND THE HARNESS HID IT FROM ME FOR FOUR ATTEMPTS

Worth recording, because none of it was the game's fault:

1. **Cropping by world coordinates.** The enemy was at world x=161 with **camX=141** — its screen
   position was x=14. Every crop I took was looking 140px away from the thing I was checking.
2. **Diffing two draws.** `drawWorld` advances on a wall clock internally, so two consecutive
   draws differ across the WHOLE canvas — the diff bbox came back as the entire frame even with
   `dt=0`. Frame-diffing cannot isolate anything in this engine.
3. **Drawing the tell onto a cleared canvas** to isolate it — the engine's own redraw wiped it.

What finally worked was the plain one: let the game run, ask the page for `e.x`, `e.y` and
`camX`, and crop `(e.x - camX)`. *If a visual check keeps failing, suspect the ruler before the
thing being measured.*

---

## HOW TO VERIFY

    node --check assets/game.js
    node --max-old-space-size=3072 _BUILD_SOURCE/test_fl.js     2,701 ok / 3 fail

`CHARGE_TELL` is the dial (3.0s). `CHARGE_TELL_COL` is the amber-to-red ramp.

## STILL OPEN FROM MIKE'S TWO LISTS

- **"Still chaotic/unsensual projectile patterns."** 0821a cut the rates (peaks down 18-48%) but
  he is still seeing it, so the next pass has to look at the SHAPES and their overlap rather than
  the volume. Not started.
- **Stage 6** — his.
