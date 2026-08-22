# 0821j — TWO OF BRIAN'S STANDING CALLS, ANSWERED BY MEASUREMENT

Continuing the backlog while Mike is out. Both of these were on the
"⚠ YOUR CALLS" list in `HANDOFF_COLE_0814.md`; neither needed a decision once measured.

| item | answer |
|---|---|
| regression sweep after the 0821 pass | **all 8 stages clean** |
| **% glyph** in the BOF face | **ALREADY SOLVED — verified, close it** |
| **orb damage on stages 2/3** | **exactly 2x, and it is guaranteed rather than situational** |

---

## 1. REGRESSION SWEEP — NINE COMMITS IN ONE DAY, CHECKED TOGETHER

0821a-i changed boss AI, volley shapes, pickups, the camera and the thruster rig. A green suite
proves state, not pixels, so all 8 stages were run 35s each in the real renderer:

    stage  frames  maxEnemies  maxEBullets  maxPickups  result
    1..8   2100    7-14        38-97        3-4         OK, no throws, no console errors

⚠ **ONE NUMBER FOR THE PLAYTEST, NOT FOR ACTING ON:** peak enemy bullets is **38 on stage 1** —
Mike's readable baseline — against **96 on stage 3 and 97 on stage 7**. After 0821a (rates) and
0821h (shapes), the remaining gap is the WAVE TABLE: how many volley-capable rosters are alive at
once. That is a density question and it is parked until Mike has played 0821h.

## 2. THE % GLYPH IS NOT AN OPEN ITEM

Carried on the standing list as *"% glyph in the BOF face (stats screen borrows stage 2's molten
one)"*. Rendered the stage-clear screen with real stats and looked at it:

    ACCURACY     87%        MISSILE HITS   85%

**Both the digits and the borrowed glyph render, in the same khaki.** The existing handling is
correct and deliberate: `%` exists in EXACTLY ONE of the eighteen font sheets, `stageTextMixed`
borrows it per glyph, and `SC_PCT_TINT` (#bbb574) was sampled off a rendered value so the borrowed
character matches the digits beside it rather than arriving in stage 2's fire orange.

⚠ **AUTHORING A NEW % INTO THE BOF FACE WOULD BREAK THIS REPO'S OWN RULE** — the same one that
kept 0811m from inventing a Decker pickup icon. The borrow is the right answer, not a workaround
waiting to be replaced. **Recommend closing it.**

⚠ **AND MY FIRST READ OF THE SCREEN WAS WRONG.** I reported the % rows as showing no digits at
all. They were there — I had cropped too small and captured the reveal mid-animation. Two fixes:
step the REAL loop so the sequence's own timers advance, and zoom before concluding. *A value that
has not finished animating in is not a missing value.*

## 3. ORB DAMAGE ON STAGES 2/3 — THE NUMBERS

Brian: *"orb damage on stages 2/3 is higher since 0814a (the elemental bonus finally reaches it —
you have not seen the numbers)."* Measured as damage actually dealt to a dummy, weapon level 5:

    stage element:   2 = fire,  3 = ice,  all others = none

| | orb element | multiplier | damage dealt |
|---|---|---|---|
| stages **2 and 3** | opposite the stage | **x2** | **4** |
| stages 1, 4, 5, 6, 7, 8 | n/a | x1 | 2 |

⚠ **IT IS GUARANTEED, NOT SITUATIONAL — which is the part worth Mike's eye.** Cole's orb is ICE,
so it is the opposing element on fire stage 2; and 0814a made it correctly count as FIRE on ice
stage 3, so it is the opposing element there too. **The orb auto-matches whatever the stage is
weak to, so it can never NOT double on 2 or 3.** It is strictly the best weapon on both elemental
stages, by construction rather than by choice of loadout.

That is the intended "opposite element" rule working exactly as written — but the rule was designed
for a weapon that might be the wrong element, and this one never is. If Mike wants the orb to be a
choice rather than an answer on those two stages, the dial is `elementMultiplier` (one line).

Freezer's thermoshock reads `fireice` and takes the same x2 on 2/3 — and correctly x1 elsewhere,
because `elementMultiplier` returns 1 for any stage with no element before the `fireice` branch is
reached. No bug there.

---

## HOW TO VERIFY

    node --check assets/game.js
    node --max-old-space-size=3072 _BUILD_SOURCE/test_fl.js     2,702 ok / 3 fail

No code changed in this drop. Measurement and decision-support only.
