# 0916 — the marquee lights, the lettering, and a new Options scene

*(Credits was first built as "Neon Black" to Mike's original list, then changed on his follow-up:
"make credits neon brown instead with the star, text and light." Section 2b covers what that
changed; the black build and what it taught are kept below because the traps are the same.)*

Mike: *"in each marquee, the lights should be palette swapped to different colors on the left and
right sides of the button. New Game - Neon Green, Enter Password - Neon Orange, Options - Neon
Blue. Help - Neon pink - Achievements - Neon Red - Credits - Neon Black, also palette swap Star to
Black. Exit Game - White Light. You also palette swap the text in each button to match the color of
the lights. Options may need another generation as Ice has nothing to do with Options."*

| button | lights | lettering | extra |
|---|---|---|---|
| NEW GAME | Neon Green | green | |
| ENTER PASSWORD | Neon Orange | orange | |
| OPTIONS | Neon Blue | blue | **scene regenerated** |
| HELP | Neon Pink | pink | |
| ACHIEVEMENTS | Neon Red | red | |
| CREDITS | Neon Brown | brown | the emblem **star** browned too |
| EXIT GAME | White Light | white | |

---

## 1. Two masks, and neither is a threshold I picked

**The lamps are bounded geometrically.** The saturation histogram of the bezel zone has **no empty
band** between the metal and the tube — measured on every plate, bin 0 holds 716–986 px of grey
metal, bin 9 holds 575–748 px of lit tube, and every bin between holds 150–270 px of spill and
warm-tinted metal. Threshold-hunting there is the 0907u trap, where five colour detectors each broke
the ship the last one fixed. The tube is found as the **lit bounding box inside each end's bezel**
instead, and rotated with a weight, so grey metal is spared and the white-hot core stays white —
which is what a neon tube of any colour does.

**The letters are found by their shared baseline.** A gold colour mask alone is not enough, and the
render said so immediately — it swallowed the sunset **sky** on NEW GAME (1,692 px), the trophy and
the medals on ACHIEVEMENTS, the star on CREDITS and the fire on EXIT GAME:

    letters      y0 22-23   y1 44-45      <- every glyph, every plate
    the sky      y11-48       the medal   y32-52
    the trophy   y20-39       the star    y14-48      the fire   y34-51

A line of text has one property nothing in a painted scene has: **every glyph sits on the same two
rows.** The band is taken as the median of the letter-sized components and anything off it is
dropped. Nothing is hand-listed, so a regenerated plate classifies itself — which is exactly what
the new OPTIONS plate then did. Glyph counts came out 7 / 13 / 7 / 4 / 12 / 7 / 8, matching the
words letter for letter.

*(Boundary darkness was the first discriminator and is the weaker one: letters run 0.41–0.95 against
0.30 for the sky and 0.19 for the medal, but CREDITS' star reads 0.24 against its own dimmest letter
at 0.41 — one bad plate away from failing. Kept only as a tie-break.)*

---

## 2. Rotate the hue, don't set it — and two of the seven can't be a rotation at all

The tube runs white-hot core → bright body → deep rim, and that gradient is most of what makes it
read as a lamp. Each plate's **own** lit hue is measured (0.099–0.105 on the six amber plates) and
the rotation is `target − measured`, so the whole gradient travels.

⚠ **A LINEAR SATURATION WEIGHT GIVES A MID-TONE THE WRONG HUE, AND THE RENDER CAUGHT IT.** Rotating
by `dh × s` means a pale gold highlight at s=0.30 travels only 30% of the way: aiming HELP at pink
(+0.79) landed those pixels on **0.36, which is green**, and the word came out violet. ACHIEVEMENTS
came out magenta the same way. **A partial hue rotation is not a paler target — it is a different
colour**, which is the one thing a weight must never do. Text now rotates whole; the lamp uses a
sharpened ramp so the tube and its lit bezel rotate fully and near-grey metal is spared.

**CREDITS "Neon Brown"** — see 2b. It was first built as "Neon Black", which curved value and
saturation in opposite directions (the 0810s `ice_black` lesson) so the body crushed to black while
a rim survived.
⚠ **AND A LAMP THAT HAS GONE BLACK TAKES ITS HOUSING WITH IT.** Crushing only the coloured pixels
left the socket's lit metal at full brightness — the brightest pixel in the bezel measured **0.47
against 0.78**, a dim tube in a bright socket, which does not read as "off" at all. Dimming the
whole box takes it to **0.31 against 0.71**.
⚠ **AND THE +0.72 COLD CAST IS THE LAMP'S ONLY.** Applied to the star and the lettering it turned
gold into **plum**, and a violet star is not "Star to Black". A tube needs some colour left or it
stops reading as a lamp; a black star wants none. Cast 0 for those.

**EXIT GAME "White Light"** strips the cast and lifts the value — `'color'` compositing cannot make
white, because white has no saturation to donate (the same reason `xartPalette` carries its own
white path).

Palette counts: **0.84–1.05** of the original on every plate. The two below 1.0 are CREDITS and EXIT
GAME, which collapse chroma by definition — that is a desaturation, not the range-exchange shredder
0906o warns about.

---

## 2b. Neon Brown, and why the hue is the least of it

Mike, on the second pass: *"make credits neon brown instead with the star, text and light."*

⚠ **BROWN IS NOT ITS OWN HUE — IT IS DARK ORANGE — AND THESE LAMPS WERE ALREADY AMBER.** The
plates' own lit hue measures **0.100** against a brown target of **0.072**: a rotation of 0.028,
which is nothing. Hue alone would have left the bar essentially as generated and every number would
still have gone green. What makes a warm colour read as brown is the **luminance**, so the mode
carries a `val` factor alongside the rotation.

⚠ **AND A WEIGHTED LUMINANCE DROP ALONE LEFT THE TUBE LOOKING GOLD.** The saturation weight
spares low-saturation pixels on purpose — that is exactly what keeps the grey bezel grey — but a
neon tube's **white-hot core is low-saturation too**, so it kept nearly all its brightness:
measured, the brightest lamp pixels went 1.00 → only **0.58–0.74**, and at a glance the lamp still
read amber while the medians said it had moved. A brown lamp has no white-hot core to protect —
brown *is* dark — so an unconditional `dim` brings the whole tube down together. Brightest lamp
pixel now **0.33, was 0.73**; the lettering **0.46 against the gold's 0.79**.

The star and the lettering take the same rotation and `val` at full weight, so all three match.
Palette count **0.99** — brown costs nothing, where the black build collapsed chroma to 0.84.

---

## 3. The star was half black, because it is two components

Taking "the tall gold component" gave 174 px and the render showed a star **black down the left and
gold down the right**: its own bevel cuts it in two (n=174 at x27–45, n=51 at x46–61). All the
components in the emblem panel are unioned now, and the third one — n=88 at x6–11, which is the
**lamp**, gold like everything else — is excluded by geometry rather than by a size rule that would
need retuning. 602 px, the whole star.

---

## 4. OPTIONS: he was right, and the fix was not the obvious one

The ice plate had nothing to do with Options. A single-bar generation returned three good console
scenes — sliders, dials, an equaliser, a wrench, gold lettering, no ice — and **every one was the
wrong shape**:

    o1  362x79   aspect 4.58        the family is 5.74 - 5.93
    o2  367x88   aspect 4.17
    o3  502x43   aspect 11.67

⚠ **AND SHIPPING ANY OF THEM WOULD HAVE REINTRODUCED THE EXACT BUG MIKE REPORTED.**
`titleMenuLayout` draws every row at one width and takes height from the plate, so a 4.58 bar draws
**27% taller** than its neighbours — which is `btn_help` all over again, one drop later.

⚠ **THE LEVER IS THE BAR COUNT, NOT THE PROMPT.** Three bars in a square canvas came back at
3.56–4.46; seven bars in the same canvas is what produces ~5.8, because the canvas is square and the
bars divide it. Regenerating the **seven-bar sheet** with only OPTIONS' scene changed returned bars
at 396x69 / 397x69 / 397x68 / 397x67 — **the shipped family's dimensions exactly** — and its OPTIONS
bar at 397x70, aspect 5.671. Only that bar was taken; the other six on that sheet were discarded.

Family spread is now **5.671–5.925 = 0.254**, still inside the probe's 0.30 bound. The ice plate is
kept as `btn_options.ice.png`.

---

## 5. Verified

`probe_title_0916.py` — **38 ok / 0 fail**, 0 page or console errors.

⚠ **THE PLATE ON DISK IS NOT EVIDENCE**, so every colour is read off the canvas XART actually hands
the title — cells are checked before the loose-file cache, and this family ships under keys chosen
to dodge exactly that.

⚠ **AND IT MEASURES THE PIXELS THAT CHANGED, NOT THE PIXELS THAT LOOK LIT.** The first cut sampled
"saturated bright pixels in the bezel" and **failed four assertions on a build that is correct**:
CREDITS and EXIT GAME have no saturated lamp pixels *by definition*, so the sample came back empty
and the probe printed value `-1.000`, which reads as "the lamp is gone" rather than "I asked the
wrong question"; and the 431 and 553 "letter" pixels it did find on those two were the **city
lights** and the **runway fire**, which sit in the same band and were never meant to change.
Diffing the live plate against the un-recoloured source on disk gives the exact mask the builder
touched, so the scene cannot contaminate it and a colourless lamp is still findable.

    newgame       lamps hue 0.293   lettering 0.313      1103 / 2236 px changed
    password      lamps hue 0.047   lettering 0.056       552 / 3706
    options       lamps hue 0.560   lettering 0.576      1557 / 1980
    help          lamps hue 0.877   lettering 0.907      1280 /  931
    achievements  lamps hue 0.956   lettering 0.986      1169 / 3367
    credits       brightest lamp px 0.31, was 0.71       2360 / 2437   lettering value 0.18
    exit          lamp saturation 0.06, was 0.66         1714 / 2072   lettering sat 0.04, value 1.00

    and the recolour did not move a single plate size (spread 0.254)

Proofs: `19_lights.png` (all seven, before over after), `20_credits_black.png`,
`22_options_new.png` (ice vs console), `23_black_and_white.png`, `15_title_seven.png` (live).

---

## 5b. The suite

Against a clean `git worktree` at HEAD (`9f64e731`), names compared with the numbers masked:

    mine       4,658 ok / 56 fail        <- +10 assertions, section 365 at 10/10
    baseline   4,647 ok / 56 fail

**Best run against best baseline run, the failure sets are identical.**

The observed band is **56-57 on both trees**, and across eight full runs this session the extra name
was always one of two order-dependent fixtures, never both: the stage-1 sand tanks (which record
only `enemies.slice(-4)[0]` per wave increment off an unseeded plan) and "a second lance may destroy
the wounded 3-drone column" (which runs 200 frames of live `updatePlay`, so whether the second lance
connects in time moves with the run). The baseline reproduces the first with zero code changes.
`git diff assets/game.js` matches **zero** lines against
`random|spawnEnemy|waveIdx|updatePlay|pShoot|drone|lance|enemies`.

---

## 6. Registration

The recoloured plates are `btn_<name>_lit.png` and the registration points at those; the sheet's own
cuts stay on disk un-recoloured. That keeps the swap one path away from a revert **and** lets
`title_lights_0916.py` always re-run from a clean source — a script that consumes its own output is
not idempotent, which is how 0907u made a plate worse on every run.

---

## 7. Flagged, not changed

**CREDITS is the least legible row on the screen**, which is inherent in the instruction: its
lettering is black, on a night-city scene, and the plate's own keyline is dark too, so the glyph has
only its bevel to separate it from the background. It reads at 4x and it reads in the live frame,
but it is dimmer than its six neighbours by design rather than by accident. If Mike wants it to pop,
the cheapest fix is a light outline on that one word — one number in the builder, not a regeneration.
