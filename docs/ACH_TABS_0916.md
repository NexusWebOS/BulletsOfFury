# 0916 — the achievement tabs and filters (ACH-09)

Mike, in the ACH-02 brief: *"allow me to have a tab system and filter system to view our
achievements by type, enemy, player, completion etc."*

Five tabs across the gallery, LEFT/RIGHT to move between them, FIRE to cycle the value inside one:

| tab | values | what it answers |
|---|---|---|
| ALL | — | the whole 66 |
| TYPE | the 8 families | campaign clear, stage clear, no death, missile discipline, boss difficulty, boss speed, weapon max, no continue |
| ENEMY | stages 1–9 | the awards won **against a unit** |
| PILOT | the 9 | who earned it |
| STATUS | unlocked / locked | completion |

---

## 1. Every value is derived from the rows, never hand-listed

`awardsTabValues(tab, rows)` walks the achievement list and collects what it finds. This repo's own
history is the argument: `_selfPat`, the edge-pin exemption list and the enemy-separation list were
each a hand-written list that went stale the moment something new arrived, and each cost a drop.
Deriving means **a family added later appears in TYPE on its own**, and a family with no rows cannot
appear at all. The suite asserts the stronger direction too — no family present in the list may be
missing from the tab.

---

## 2. "ENEMY" is the encounter axis, not every row that carries a stage

Beating stage 4 without dying is an achievement about the **stage**. Beating its boss on Furious is
one about the **boss**. Offering every row with a `stage` field would have made ENEMY a second copy
of STAGE CLEAR, answering a question Mike did not ask. Only `boss_difficulty` and `boss_speed` are
offered here.

⚠ **AND THE FOUR STAGE-1 SPEED AWARDS HAD NO `stage` FIELD AT ALL.** Their ids and titles say
"Stage 1" — `stage1_boss_under_60` and friends — and their definitions carried only
`{family, role, seconds}`. So the ENEMY tab showed stage 1 its **two** boss-difficulty rows and none
of its four speed rows. The filter was right; the data was short a field. With `stage:1` added,
stage 1 shows all six. Found by reading the probe's own numbers, not by a failing assertion — the
tab was working exactly as written.

---

## 3. "PILOT" needed a fix in the grant path, not in the filter

⚠ **THE ONLY PILOT ANYWHERE IN THIS SYSTEM WAS A FIELD ON NINE DEFINITIONS.**
`campaign_clear_<pilot>` carries `pilot`; the other 57 do not. `achievementRunComplete` already put
`pilot` in its unlock meta, but `achievementStageComplete`, `achievementEncounterDefeat` and
`achievementWeaponMax` — which award **60 of the 66** — built their meta inline and recorded only
mode, difficulty and stage. A PILOT tab over that data could only ever have shown one row per pilot.

`achievementMeta(extra)` is now the single funnel: it records the pilot, the second seat in co-op,
the mode and the difficulty, and the three grant sites go through it. A grant added later carries it
for free, and the suite asserts all three call it.

⚠ **IT CANNOT REWRITE HISTORY, AND THE TAB DOES NOT PRETEND IT CAN.** Unlocks already sitting in a
player's `localStorage` have no pilot in them, so on a pre-0916 save the PILOT tab shows the
campaign-clear rows and nothing else. That is a limitation of the stored data, not of the filter.

---

## 4. Verified

`probe_awards_0916.py` — **38 ok / 0 fail**, 0 page or console errors, driving real key taps.

⚠ **ONE PRESS MUST MOVE EXACTLY ONE TAB**, and that is the assertion that matters here.
`Input.menuLeft`/`menuRight` **consume** their tap, and CLAUDE.md records the worked example of
getting it wrong — `d = menuLeft() ? -1 : 1` is always +1, because the second call has already been
eaten by the first. A probe that only checked "the tab changed" would pass on that bug. So it checks
`start + 1` exactly, then that LEFT comes straight back to `start`.

    the gallery carries a tab per axis Mike named: ALL TYPE ENEMY PILOT STATUS
    RIGHT moves exactly ONE tab (0 -> 1), not two and not back
    and LEFT comes straight back (0)
    TYPE offers a value per family, derived from the rows (8)
    and every row it shows belongs to that family (BOSS DIFFICULTY, 18 rows)
    FIRE cycles to the next value (BOSS DIFFICULTY -> BOSS SPEED)
    the list length and the header agree (4)
    ENEMY shows only rows won against a unit (boss_difficulty, boss_speed) - 6 rows on stage 1
    STATUS splits the gallery exactly in two (UNLOCKED 0 + LOCKED 66 = 66)
    a filter CAN come back empty, and the screen says so
    changing tab resets the scroll

Two things the design had to get right and the probe pins:

- **The header counts the filtered set.** "0 OF 66" over four rows is a lie about the thing on
  screen. The points stay the profile total, because that is a score and not a count.
- **An empty filter is a legitimate answer** and says `NOTHING HERE YET` rather than drawing an
  empty panel, which reads as broken.

Suite section 364 carries eleven more assertions (**4,669 ok / 56 fail**, failure set identical to a
clean worktree at `9f64e731`). Proofs: `docs/proofs/awards_0916/05_tabs.png`, `06_tab_type.png`.

---

## 5. Still open on the ACH brief

The Furious Points **vault** (dev videos, interviews, BOF2 sneak peeks), **Bunny mode** for Falva,
**Bombshell mode** for Lizzie, and **INSANITY** — the fifth difficulty, invisible and unselectable
until it is bought with points, with its own generated button.
