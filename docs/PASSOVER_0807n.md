# PASSOVER — drop 0807n   (SCALED TO FIT THE WINDOW)

Build: `BulletsOfFury_0807n`
Harness: **2,156 assertions / 198 sections / 0 failing**, twice, reaching the banner.

---

## 1. I MEASURED THE PANEL INSTEAD OF EYEBALLING IT

Mike: *"You gotta scale some stuff down to make it all fit in that window."*

Scanning outward from the centre of the `statscreen` art until it hits the bright bevel gives the
usable interior exactly:

    x 0.046 .. 0.951      y 0.086 .. 0.907

My first pass ran **0.075 to 0.945** — the header sat ON the top moulding and PRESS FIRE on the
bottom one. Both ends were outside the window, which is precisely the complaint this screen has
now collected five times.

## 2. WHAT WAS SCALED, AND WHY THAT AND NOT SOMETHING ELSE

The rows are the content; they should not be the thing that gets squeezed. The room came from
the furniture around them:

    portrait      0.215 -> 0.180 of panel width      the biggest single saving
    header type   0.062 -> 0.054
    rank letter   0.115 -> 0.098
    row labels    0.030 -> 0.026     values 0.032 -> 0.028
    row pitch     0.098 -> 0.083     start 0.165 -> 0.212

    header      0.075 -> 0.132       now inside the top moulding
    score       0.775 -> 0.762
    password    0.900 -> 0.838
    PRESS FIRE  0.945 -> 0.893       now clears the bottom moulding

The bars themselves got very slightly TALLER (0.44 -> 0.46 of the row) — with a tighter pitch
there was room, and the bar is the thing you actually read.

## 3. THE FIT IS ASSERTED, NOT LEFT TO THE EYE

Section 198 pulls every `py+ph*<frac>` anchor out of the drawing code and fails if any sits above
0.086 or below 0.907. It also checks the six rows finish above the score line, computed from the
start and pitch rather than hardcoded.

Five reports of this same class of collision is enough. The next person to move a number here
will be told immediately.

## 4. TWO SELF-INFLICTED SNAGS WORTH NOTING

The assertion originally bounded its slice with `indexOf('function mechDraw')` — a function that
no longer follows this screen, so the slice came back nearly empty and the check silently passed
on almost nothing. Bounded by "the next top-level function", whatever it happens to be.

And writing that fix, a literal newline went into a JS string and took the whole suite down —
**0 assertions, 0 failures, which reads exactly like a pass.** Same trap as always: the count is
the tell, not the failure number.

## 5. STILL OPEN FROM THE PLAYTHROUGH

Seven: dialogue box art · liftoff music · L2 miniboss routing into lava · the tank on the
mountain · the runway plate · retiring the beach water · L2/L3 boss assembly spacing.
