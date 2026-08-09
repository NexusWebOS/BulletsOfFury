# PASSOVER — drop 0808f   (THE THRUSTER NUDGES)

Build: `BulletsOfFury_0808f`
Harness: **2,258 assertions / 207 sections / 0 failing**, twice, reaching the banner.

---

## 1. THE NUDGES

Mike: *"move lizzies about 10 pixels down. move yuri's up 5 pixels, move axel and freezer and
falvas up 5 pixels. this way they contact the thruster they are coming out of and with lizzie
coming out of the tail fin of the plane."*

    lizzie   +10px   down, out of the tail fin
    yuri      -5px   up, into the nozzle
    axel      -5px
    freezer   -5px
    falva     -5px
    cole / decker / juggernaut / maverick   unmoved — he did not ask

## 2. ⚠ STORED AS A FRACTION, NOT AS PIXELS

He gave these against the 224px hull in the 0808e render. **The ship does not draw at 224px in
the game** — it is around 44px in play and up to 128px in the launch cinematic, and he
specifically asked to see the thruster in ALL of those. A raw pixel offset would put the flame in
three different places across the three scenes: a 10px nudge is 4% of the reference hull but 23%
of the in-play one.

Stored as a fraction of hull height, so the flame stays welded to its nozzle at any draw scale.
Asserted, including that each fraction still resolves back to the pixel value he asked for at the
reference size.

## 3. STILL OPEN

    the baked-in thruster frames — identify which hull frames carry flame, THEN delete
    mfx_ (252 cells) — the unconfirmed deletion
    the helix ball · stage 1 transition · menus backable by keyboard · fireorb icon on level 3
