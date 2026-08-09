# PASSOVER — drop 0809c   (FONTS, MENU BACK, PASSWORD TYPING)

Build: `BulletsOfFury_0809c`
Harness: **2,379 assertions / 215 sections / 0 failing**, twice, reaching the banner.

---

## 1. EVERY FONT, RENDERED

Ten families: nine stage fonts plus the gamefont fallback.

    sfont1  Rumble in the Jungle    stone, green moss      47 glyphs
    sfont2  It's Hot in Here        orange/red             47
    sfont3  Ice Still Can't See     pale blue ice          47
    sfont4  Crouching Missiles      olive/gold             47
    sfont5  All for One, None       violet/pink            47
    sfont6  Heavy Turbulence        sky blue               47
    sfont7  Not Another Sewer       yellow-green           47
    sfont8  Furious Death           red                    47
    sfont9  Bonus Stage / Space     purple                 47
    ncm_font  the fallback          monospace pixel        74

⚠ The stage fonts carry 47 glyphs each and the gamefont 74 — so punctuation the stage fonts lack
(`%` for instance) falls through to a face that does not match. That is why the stats screen mixed
two styles. Worth knowing before choosing fonts for the UI.

## 2. ⚠ THE BACK BUTTON ALREADY WORKED — NOBODY CALLED IT

`Input.menuBack()` existed and already covered **k, b, escape, backspace and two gamepad buttons.**
Only TWO of the seven menu screens ever called it. `drawPilot`, `drawPassword`, `drawCredits`,
`drawStageSelect` and `drawModeSel` had no back at all: once you were in, the only way out was to
complete the screen.

That is a different bug from a missing feature, and adding a new back handler would have hidden it.

Handled once in `drawScene` from a table:

    pilot     -> modesel        credits   -> title
    password  -> title          stagesel  -> modesel
    options   -> title          modesel   -> title
    diff      -> title

A table rather than five copies of the same three lines, so the next screen added inherits it
instead of being the sixth one somebody forgot. Leaving the password screen also clears a
half-typed code — a stray input following you back out is its own bug.

## 3. THE PASSWORD TYPES NOW

It had a full on-screen keypad and no keyboard path — six slots you had to click a character at a
time. Typing works alongside the keypad; both write the same `pwInput`.

    IRON typed        -> IRON
    backspace         -> IRO
    retyped           -> IRON
    six-char cap      -> holds at 6
    ENTER             -> submits through submitPassword()

A raw keydown listener rather than the Input map, because Input tracks BOUND ACTIONS (up, fire,
bomb) and a password needs arbitrary letters and digits. ⚠ It only buffers while the password
screen is up, so it can never swallow a key anywhere else in the game — asserted.

## 4. ALREADY WORKING, VERIFIED NOT CHANGED

Menu movement is already on `keybind.up/down/left/right` through `menuUp()`/`menuDown()`/etc, so
it follows whatever the player has bound — WASD or arrows. No change needed.

## 5. NEXT

Pilot card fonts, and the wider UI pass.
