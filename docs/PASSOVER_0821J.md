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

## 3. ORB DAMAGE ON STAGES 2/3 — HISTORICAL, SUPERSEDED 0825C

The table below records the old 0814a behavior; it is retained only as historical evidence of the
rule Mike corrected on 0825c. It is no longer the runtime behavior.

    stage element:   2 = fire,  3 = ice,  all others = none

| old behavior | orb element | multiplier | damage dealt |
|---|---|---|---|
| stages **2 and 3** | opposite the stage | **x2** | **4** |
| stages 1, 4, 5, 6, 7, 8 | n/a | x1 | 2 |

⚠ **SUPERSEDED 0825c BY MIKE'S EXACT KIT RULE.** Cole has no elemental damage addition and no
special orb; his authored specials are Sonic Boom and nuclear missiles. Generic orbs stay at x1
for Cole and every other pilot. The two approved bonuses are Freezer-only and attack-specific:
Stage 2 ICE BREATH x2, and Stage 3 FIRE-ICE / thermoshock ball x2. `elementMultiplier` now requires
the pilot, stage, element, and attack identity to match, so a generic orb can never inherit either.

---

## HOW TO VERIFY

    node --check assets/game.js
    node --max-old-space-size=3072 _BUILD_SOURCE/test_fl.js     2,702 ok / 3 fail

No code changed in this drop. Measurement and decision-support only.
