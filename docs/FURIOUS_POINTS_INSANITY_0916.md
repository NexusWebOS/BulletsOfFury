# 0916 — Furious Points, and INSANITY (ACH-14 / the fifth difficulty)

Mike, in the ACH brief: *"We also should have an Achievement Pts currency system as "Furious" pts
that unlock secret behind the scenes development stuff ... Also be able to unlock fun and cute stuff
like Bunny mode for Falva, "Bombshell" mode for Lizzie, Insanity - a 5th difficulty and 5th
difficulty button you should generate. it will not show up unless you unlock it via achievement
points, so its an invisible button you cant even select until this condition is met, then it becomes
visible and selectable."*

This drop lands **the spend side of the currency** and **INSANITY**. Bunny and Bombshell have their
shop rows and prices; their art and the vault of dev media are still to come.

---

## 1. What you have spent is derived from what you own — never stored

`furiousSpent()` sums the cost recorded on each owned row; `furiousBalance()` is
`achievementPoints() - furiousSpent()`. There is deliberately **no stored counter**.

Two numbers describing one fact drift apart the moment anything writes one without the other — a
save interrupted between the two, an item removed from the shop later, a hand-edited profile — and
then the balance is wrong for ever with nothing to compare it against. Summing the owned rows means
the balance **cannot** disagree with the list of things it paid for.

⚠ **AND EACH PURCHASE RECORDS THE PRICE IT ACTUALLY PAID**, so re-pricing an item later cannot
retroactively change what an existing player has left.

`furiousBuy(id)` returns a **word** — `ok` / `owned` / `poor` / `unknown` — not a boolean, because
the screen has to say which of the three happened and a `false` cannot carry that.

⚠ **`owned` WAS ADDED WITHOUT BUMPING `ACHIEVEMENT_STORE_VERSION`, AND THAT IS THE WHOLE POINT.**
`achievementNormalize` returns an **empty store** whenever the version does not match, so bumping it
to make room for a new field would have silently **deleted every achievement every existing player
has earned**. An absent `owned` reads as `{}`.

---

## 2. INSANITY is absent, not disabled

⚠ **"YOU CANNOT SELECT IT" IS THREE CLAIMS, NOT ONE.** A row can be missing from the screen and
still be reachable by the cursor, by the mouse hit test, or by the function that turns the cursor
index into a difficulty key — this repo has already shipped a menu where **four** separate places
knew the row count and one of them was missed. So INSANITY is simply **not in the list the screen
walks**: `diffList()` filters it out until it is owned, and the draw loop, the cursor, the mouse test
and `pickDiff` all read that one list. One fact closes three doors instead of three guards that each
have to remember.

The probe drives all three: it walks the cursor right round the menu, forces the index past the last
row and reads what `pickDiff` assigns, and checks the hit test walks the same list.

---

## 3. Three per-difficulty tables would have made INSANITY the EASIEST setting

This is the find of the drop, and nothing failed to reveal it — the grep for `DIFF` did.

    FODDER_DIFF   = { easy, normal, hard, furious }     read as FODDER_DIFF[k] || 1
    DRONE_TELL    = { easy, normal, hard, furious }     falls back to .normal BY NAME
    DRONE_RECOVER = { easy, normal, hard, furious }     falls back to .normal BY NAME

A difficulty with no row gets **NORMAL's numbers**. On the hardest setting in the game that means
**softer fodder than HARD** (1.0 against 1.15, and against FURIOUS's 1.60) and **longer warnings than
HARD** (0.55s tell against 0.46s). None of the three throws, none logs, and the run simply plays
wrong. `achievementNormalOrHigher()` had the same shape as a hand-written list of "the hard ones" —
INSANITY would have earned **no stage-clear or no-death award at all**.

⚠ **AND THE BOSS GRANT WAS AN EQUALITY LADDER**, `diffKey==='hard'` / `=== 'furious'`, so an INSANITY
boss kill granted **nothing** — harder than Furious and worth less than Easy. It is ranked now
(`difficultyRank`), so a difficulty added above the top earns at least what the one below it does.
*Granting the FURIOUS row rather than inventing new awards is my call and the conservative half of
it; whether INSANITY gets awards of its own is Mike's.*

**The durable fix is not that I remembered.** Suite section 366 asserts that **every key in `DIFFS`
has a row in every per-difficulty table** — `FODDER_DIFF`, `DRONE_TELL`, `DRONE_RECOVER`,
`ARCADE_STOCK`, `DIFF_META` — so the next difficulty cannot be half-added.

`DIFF_KEYS` / `DIFF_IMG` / `DIFF_DESC` were three parallel arrays; they are one keyed `DIFF_META`
table now, for the reason the title menu taught: three arrays that must stay the same length are
three chances to be wrong.

---

## 4. The buttons — all five, one face escalating

Mike, seeing the INSANITY plate: *"I LOVE that Insanity Logo. Can you also remake our other
difficulty options please, this is awesome. I would like each to feature Faces that go from Normal
to Under Pressure to Furious to Insanity's Death ... use this one for Insanity btw."*

And, on seeing the first cut: *"Cool, but they should all be different styling in representation
off their difficulty much like Insanity is. Including faces. Insanity remains as is."*

⚠ **THE FIRST CUT WAS ONE PLATE RECOLOURED FOUR TIMES, AND THAT IS EXACTLY WHAT HE CAUGHT.** All
four shared a frame, a dark panel and a pose; only the hue and the eyebrows moved. INSANITY was the
only one whose MATERIAL said what it was. The four are rebuilt so each is made of something
different and reads at a glance:

And then, casting it: *"To make it funnier, use Falva for the Easy person, use Freezer for the
Normal Person, Use Axel for the Hard Person and Use Cole in the Furious way ... based on our pilots
faces you should snippet and use as references."*

| | pilot | frame | panel | lamps |
|---|---|---|---|---|
| EASY | **Falva**, laughing, glasses, red curls | polished chrome, undamaged | sunlit sky, clouds, green horizon | green |
| NORMAL | **Freezer**, stone-faced and unimpressed | olive drab, stencilled | steel grid, blue radar sweep, readouts | blue |
| HARD | **Axel**, rattled behind his aviators | battered gunmetal, hazard stripes | scorched gouged plating, sparks from a torn seam | amber |
| FURIOUS | **Cole**, roaring | half molten, glowing at the joins | splitting open over lava, embers rising | red-white |
| INSANITY | the skull | **untouched, as he asked** | violet electrical cracks | violet |

The faces are the pilots' **own authored portraits**, cut out of `port_<pilot>_<emotion>` and
uploaded as the generation reference, exactly as he asked.

Then four corrections, all from one look at the first cut: *"ensure all avatars face to the right,
and Cole should appear like a mix of this. We need an actual face view of Freezer not cut off, and
Axel should be grinning like this."*

| | fixed |
|---|---|
| all four | heads turned to a three-quarter view **facing right**, toward their own word |
| all four | the **whole head inside its panel** with margin on four sides - nothing clipped by the frame |
| FREEZER | his source changed to the portrait that shows his **entire face**, and the panel no longer crops it |
| AXEL | `crash` -> **`smile`**: a broad open grin with teeth, which is what he asked for |
| COLE | crossed with a **demonic berserker** - eyes burning as solid orange-white furnaces, skin scorched, smoke off him - still recognisably Cole |
| INSANITY | **untouched** |

⚠ **"NOT CUT OFF" WAS A PANEL PROBLEM, NOT A PORTRAIT ONE, AND BOTH HAD TO MOVE.** The reference
crop was taken at 62% of the portrait's height, which already lost Freezer's jaw, and the generation
then cropped what it was given. The new strip takes 70% from the very top, and the prompt asks for
the whole skull inside the panel with clear margin - so the fix is in the source AND in the frame.
Of three candidate sheets, the one that ships is the only one whose four heads are all complete and
centred; the other two clip at the right edge, which is exactly the fault being fixed.

Only the SKELETON is shared - a riveted frame, a square emblem panel at the left, a lamp slot at
each end, one word on a central panel. Everything else is per-difficulty.

⚠ **HIS PICK FOR INSANITY HAS MUCH BRIGHTER STEEL THAN THE OLD FAMILY** - grey median **0.824**
against the shipped plates' 0.208-0.263. I had darkened my own earlier pick to match the old family;
that was the right call while INSANITY was a fifth plate joining four. It is the wrong call now,
because he approved this one and asked for the other four to be remade in its image - so the family
moves to the new look rather than the new plate being pulled back to the old. His plate ships
**unmodified**.

⚠ **ALL FIVE SHIP AS LOOSE FILES UNDER `diff_<key>_0916`.** `diff_easy`..`diff_furious` are CELLS
on `ui_menu_1` and cells are checked BEFORE the loose-file cache, so registering the new art under
those names would have been silently ignored and the screen would have gone on drawing the old
plates with nothing failing.

Aspects: **4.40 / 4.48 / 4.53 / 4.45** for the four, and **3.43** for INSANITY - a **1.10** spread,
noticeably over what the shipped family had (3.49-4.32): INSANITY now draws about **32% taller**
than HARD at the same width. It draws chunkier than the rest,
which reads as the final tier rather than as an error; it is his chosen plate and the measurement is
here so he can overrule it.

## 4b. Generating them — the bar COUNT sets the aspect

⚠ **ASKED FOR ONE BAR, IT COMES BACK FAR TOO THIN.** The first INSANITY attempt returned
**7.7–8.2:1** against a family that runs 3.49–4.32, and the difficulty screen draws every row at
one *width* — so a thin plate is a thin button. Three bars dividing a square canvas land at
**3.40–3.55**; the four-bar face sheet lands at **4.17–4.27**. It is the bar COUNT that sets the
aspect, not the prompt — the same lever the OPTIONS title bar needed the same day.

⚠ **AND A FOUR-BAR REQUEST THAT SAYS "LEAVE MARGIN AT THE SIDES" COLLAPSES THE CROP.** That
phrasing returned 46×46 and 94×94 canvases — unusable at a 210px draw. Dropping it and reusing the
phrasing that had worked gave 196×196 and 200×200, with the bars near full width.

**On the first INSANITY pick, since the reasoning is worth keeping:** its steel measured grey median
**0.443** against the old family's 0.208–0.263, and I darkened only the low-saturation pixels
(×0.62 — the violet lamps, cracks and lettering carry saturation and were untouched) to land at
0.275. That was right while INSANITY was one new plate joining four old ones. Mike then chose a
different variation and asked for the other four to be remade in its image, which inverts the
argument: the family moves to the new look, so **his plate ships unmodified** and the darkening is
gone.

The screen's row pitch and start follow the row **count**, so a fifth row does not run into the
rules text.

---

## 5. Two faults the screenshot found after the probe was green

- ⚠ **THE RULES LINE RAN OFF THE SCREEN.** `NO CONTINUES / NOTHING HELD BACK` at the fixed 15px was
  wider than the viewport, so it rendered centred with its first six characters off the left edge:
  **`TINUES / NOTHING HELD BACK`**. The string is shorter now (the line above already says
  `0 CONTINUES`) **and** the line is fitted with `stageFitH`, so the next long one cannot do it
  again. 24 assertions were green while that was on screen.
- The plate's brightness above — also invisible to every assertion.

---

## 6. Verified

`probe_insanity_0916.py` — **24 ok / 0 fail**, 0 page or console errors.

    a clean profile starts at zero, and cannot buy INSANITY with nothing
    a refused purchase moves NOTHING - balance still 0, still not owned
    2,120 pts earned over 16 awards through the real unlock path
    LOCKED: the list holds four; no cursor position resolves to INSANITY;
            forcing the index past the last row still picks FURIOUS;
            the mouse walks the same list, so there is nothing to click
    buying it takes the points: 2120 - 2000 = 120
    buying it twice is refused, and costs nothing
    UNLOCKED: it appears last, and can be picked - 1 life, 0 continues
    every per-difficulty table carries an INSANITY row, and they make it HARDER
    plate aspects 3.49 / 3.58 / 3.58 / 4.32 / 3.40 - the same shape as the family
    the purchase and the balance survive a reload

⚠ **The ledger is asserted on the BALANCE, not on the return value.** `furiousBuy` returning `ok`
says what the function decided; it does not say the points left.

⚠ **AND THE PROBE'S OWN FIRST RUN REPORTED A BUG THAT DID NOT EXIST**: it read `DIFF` immediately
after `pickDiff` and printed *lives 4 / continues −1 / name NORMAL*, i.e. "picking INSANITY plays
Normal". `pickDiff` sets `diffKey`; `DIFF` is assigned when the **run** starts, at two other call
sites. It reads the key from the pick and the tuning from `difficultyForRun` now.

Suite: section 366, **failure set identical to the baseline**.

---

## 6b. The FURIOUS VAULT — the screen that makes any of this reachable

⚠ **UNTIL THIS SCREEN EXISTED, NOTHING COULD BE BOUGHT AT ALL.** The ledger, the prices and the
INSANITY unlock were built, measured and provably correct — and a real player could reach none of
them, because `furiousBuy` had no caller outside code. **A system with no surface is
indistinguishable from one that was never built**, which is the same hole ACH-02 found in the
achievement registry: 66 awards, full persistence, and nothing on screen.

Reached from the gallery on its own button (CHARGE / X), because CONFIRM already cycles the filter
there and one button doing two jobs is a shape this file has been bitten by more than once. It
lists every catalogue row — the three unlocks and four vault rows — with the balance in the
sub-header, the price only on rows that can actually be paid for, and FIRE to buy.

**The vault rows Mike asked for** — the making-of, the interview, the BOF2 sneak peek, the other
ColeForge games — are in the catalogue carrying `media:null`.

⚠ **AND A ROW THAT CANNOT DELIVER IS REFUSED BEFORE THE POINTS ARE CHECKED.** Selling a video that
does not exist is worse than not listing it: the player is out the points with nothing to show, and
the refund path is exactly the bookkeeping the derived balance exists to avoid. `furiousBuy` returns
`pending` and the screen prints what the row is waiting for. **When Mike drops a file in, the row
becomes buyable by filling one field.**

Every refusal has its own words, because "it did not work" is the least useful thing a shop can say:

    OWNED               ALREADY UNLOCKED
    too few points      NEED 2000 MORE FURIOUS PTS
    no content yet      THE COSTUME ART IS NOT DRAWN YET / AWAITING FOOTAGE FROM MIKE

⚠ **TWO FAULTS THE SCREENSHOT FOUND WITH THIRTY-SIX ASSERTIONS GREEN.** The status line was drawn
at `VH-34` and the **achievement toast** — a 200x54 card pinned to the lower-left corner since
ACH-02 — sat straight on top of it, so the words explaining a refusal were invisible. It takes the
sub-header now, where it can collide with neither the toast nor the hint row. And the vault rows
read `AWAITING MIKE'S FOOTAGE`, which hits the documented 0912b defect: **this face has no usable
apostrophe at UI size** (`LIZZIE'S` renders as `LIZZIE,S`). Reworded to `AWAITING FOOTAGE FROM MIKE`.

Probe: **36 ok / 0 fail**, including a purchase made entirely through the UI with a real key press —
buy refused while poor with the shortfall named, refused on a pending row with the balance untouched,
then bought, the points leaving, and INSANITY appearing on the difficulty screen as a result.

---

## 7. Still open on the ACH brief

**BUNNY MODE — FALVA** and **BOMBSHELL MODE — LIZZIE** are in the vault at 600 each and refuse to
sell until their costume art exists. The four **vault media rows** are listed and refuse the same
way until Mike supplies footage — each becomes buyable by filling one field. So what is actually
left is the **art and the media**, not the plumbing.
