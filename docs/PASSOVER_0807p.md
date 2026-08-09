# PASSOVER — drop 0807p   (THE PANEL FILLS THE WINDOW)

Build: `BulletsOfFury_0807p`
Harness: **2,177 assertions / 200 sections / 0 failing**, twice, reaching the banner.

---

## 1. NINE-SLICED, NOT STRETCHED

Mike: *"you may have to vertically stretch my window."*

The panel art is **1496x980 — a 1.53:1 landscape frame** — and the viewport is 480x512, which is
TALLER than it is wide. Fitting by aspect therefore left roughly forty percent of the screen
empty below the panel, which is what Mike was looking at.

Stretching it whole would need a **1.57x vertical scale** and would visibly deform the corner
brackets and the bevel rails — a decorated frame does not survive a non-uniform scale.

So it is nine-sliced. The corner decoration was MEASURED off the art rather than guessed at:
the complex block runs to x 264 and y 171, and the frame is symmetric. Corners are drawn at their
own scale, the four edge rails stretch along ONE axis each, and only the centre stretches both.

    panel   0.925 -> 0.950 of the screen height, and now genuinely fills it
    corners keep their proportions
    rails   stretch, which is what a rail is drawn to do

⚠ **One subtlety worth keeping:** the corners are scaled by the SMALLER of the two axis ratios.
Scale them by their own axis and a tall window gives you tall corner brackets on a wide frame —
the exact deformation nine-slicing exists to prevent. Asserted.

## 2. THE ASSERTION THAT HAD TO CHANGE

`fitted by aspect rather than stretched` was pinning the behaviour I had just been asked to
replace. Re-pointed at the slice margins and the corner-scale rule instead, plus a check that all
nine slices are actually drawn — a nine-slice that quietly draws eight looks fine until the one
missing edge is the one on screen.

## 3. STILL OPEN FROM THE PLAYTHROUGH

Seven: dialogue box art · liftoff music · L2 miniboss routing into lava · the tank on the
mountain · the runway plate · retiring the beach water · L2/L3 boss assembly spacing.
