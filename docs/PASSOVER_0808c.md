# PASSOVER — drop 0808c   (THE THRUSTERS, DRAWN AS AUTHORED)

Build: `BulletsOfFury_0808c`
Harness: **2,218 assertions / 205 sections / 0 failing**, twice, reaching the banner.

---

## 1. THE ART WAS ALWAYS THERE

Mike, at the start of this chat and several times since: *"stop overlaying fake thrusters and use
their sprites and make the thruster in their frames we have for each pilot appear to animate."*

`nthp_` is **nine complete reels — one per pilot, four frames each**, colour-matched: Axel blue,
Cole green, Decker gold, Falva pink, Freezer purple, Juggernaut orange, Lizzie a flame, Maverick
green, Yuri red. Nothing needed authoring. It has been in PRELOAD the whole time.

⚠ It read as "missing" in my own contact sheet because I looked up the FAMILY name with no frame
index — `nthp_cole` is nothing; `nthp_cole_0` is the art. That is the second time today my
sampler, not the art, produced a wrong answer. Written into the taxonomy as a standing rule.

## 2. THE BUG: THE FRAME SIZES ARE THE ANIMATION

The four frames are deliberately different sizes:

    81x102  ->  136x158  ->  170x192  ->  81x135
    aspect 0.79    0.86       0.89       0.60

A 2.1x linear swing. **That variation IS the flame pulse.** Both draw sites destroyed it, in
opposite ways:

* **in PLAY** — every frame was stretched into one fixed `_wid x _len` box, so each was distorted
  by a DIFFERENT amount. The flame squashed and stretched frame to frame, which is exactly why it
  read as a sprite pasted under the plane rather than the plane's own exhaust.
* **in the LAUNCH** — aspect was kept, but every frame was scaled to the same height, so the
  pulse was flattened and the thruster never changed at all.

Both now scale against the reel's **largest** frame and keep each frame's own aspect, anchored at
the nozzle so the flame grows downward out of the hull.

Measured after: aspects preserved to three decimals on every frame, and the drawn height cycles
**37 -> 58 -> 70 -> 49px** where it used to sit flat.

## 3. WHAT THIS DOES NOT DO

It does not light the exhaust pixels ON the hull. There is a note in the source from an earlier
drop claiming that is "the real fix" — but Mike's actual words are to use the sprite frames and
make them animate, which is what this does. If he wants the hull's own exhaust pixels glowing as
well, that is an additional pass, not a replacement for this one.

## 4. STILL OPEN

    mfx_ (252 cells) — the one deletion I have not confirmed, and 39% of the delete list
    the repack into named sheets, once the taxonomy is settled
    the helix ball · stage 1 transition · menus backable by keyboard · fireorb icon on level 3
