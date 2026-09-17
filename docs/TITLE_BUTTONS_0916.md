# 0916 — the title buttons, regenerated as one sheet

Mike: *"Regenerate all my other buttons here to match the current style of Bullets of Fury and
proper reference of ships and pilots please. The help button also is too large compared to the
rest."*

---

## 1. "Too large" was an ASPECT problem, and no size change could have fixed it

`titleMenuLayout()` measures **one width** for the whole menu and takes each row's height from its
own plate (`h = w * naturalHeight/naturalWidth`). So a plate whose native aspect differs from the
family is drawn taller than every bar around it **at the same width**. Measured on the shipped
build:

| plate | size | aspect |
|---|---|---|
| the authored bars | 1090x222–233 | **4.68 – 4.91** |
| `btn_help` | 446x112 | **3.98** |
| `btn_achievements` (0916, generated alone) | — | **5.17** |

`btn_help` is 19% squatter than the family, so at the menu's common width it drew **~23% taller**
than its neighbours. Nothing about it was big. It was the wrong shape — which is why it could only
be fixed by regenerating the family, not by tuning a number.

⚠ **AND THE ACHIEVEMENTS BAR WAS ABOUT TO BE THE SAME BUG, ONE BUTTON OVER.** It was generated on
its own for ACH-02 at 5.17:1. A six-bar replacement sheet came back at 6.11–6.27, which would have
left the newest button as the odd one out. The sheet was regenerated with **seven** bars including
ACHIEVEMENTS; bars cut from one job share an aspect by construction.

**Result: 5.739 – 5.925, a 0.186 spread** (3% of the mean), measured on the live canvas. The
shipped family spanned 0.93.

---

## 2. Two sheets came back, and the better-looking one could not be cut

Both candidates were correctly lettered in the right order. The one with the richer scenes
(`b7a`) was the first choice on looking at it — and it is **unusable**:

    b7a   alpha 0 on 9,423 px of 262,144    -> 1 connected island
    b7b   alpha 0 on 82,024 px of 262,144   -> 7 islands, 7 clean row gutters

`b7a`'s background was never cut out, so the bars are joined by painted backdrop and no slicer can
separate them.

⚠ **AND MY OWN PROOF RENDER HID THAT**, because it composites each cut onto a dark card — the
0906v rule (`paste(img,(0,0),img)`, never `convert()`) in its other direction: compositing a proof
onto a background is correct for showing colour and **cannot show you that a plate has no alpha**.
The alpha histogram is one line and it answered immediately.

`b7b`'s scenes turned out to run the game's own stage order anyway — jungle river and hangar, the
volcano, the ice field, a circuit board, the trophy, the neon city, a burning runway — so the
"proper reference" half of the ask is met by the sheet that could actually be sliced.

---

## 3. They ship under NEW keys

`btn_newgame` and friends are **atlas cells**, and CLAUDE.md records (0912m) that cells are checked
**before** the loose-file cache. Registering a loose file under the same key would be silently
ignored and the title would go on drawing the old plates, with nothing failing.

So the plates are `btn_<name>_0916`, registered in the **code-owned** `XART._src` block
(`manifest.js` is generated), and `MENU_KEYS` points at them. The atlas rows stay untouched for the
pause menu (`CAMP_PAUSE_BTN`) and the campaign hub (`CAMPHUB_ITEMS`), which draw their own.

---

## 4. Two places still carried their own copy of the menu

0912a's note — *"FOUR places knew the title menu was five long"* — was one place short.

- **`drawMenuButtons`'s pre-decode gate** read `XART.rdy('btn_newgame')`, a written-out key. With
  the menu repointed, that tests a plate the title no longer draws: it is true for ever, so the
  fallback never runs and, had the new art failed to decode, nothing would have drawn. It reads
  `MENU_KEYS[0]` now.
- **the fallback icon list** was an inline six-entry array against a seven-row menu, so **EXIT GAME
  drew with `icon` undefined**. It is `TITLE_ICONS` now, asserted the same length as `TITLE_ITEMS`,
  with a new `medal` icon for ACHIEVEMENTS.

The pre-decode aspect default moved from `62/330` to `68/397`, the new sheet's own.

---

## 5. Verified

`probe_title_0916.py` — real Chromium, real decode wait, blits identified by **KEY** off the
context instance (`XART.get` wrapped; a size match cannot say whose art a blit is, 0906e):

    16 ok / 0 fail, 0 page or console errors

    all seven plates decoded
    aspects 5.739 5.739 5.754 5.754 5.838 5.838 5.925  (spread 0.186)
    all seven BLITTED, in MENU_KEYS order, top to bottom
    unselected row heights 42.62 .. 44.00  -> 1.38px, i.e. nothing is stretched
    row pitch 48.0 x6, exactly even; 0 rows overlapping the row beneath
    choosing ACHIEVEMENTS still opens the gallery

**And it carries a busted arm, because the fallback path has never once been exercised by a green
run - which is precisely where the seventh row drew with no icon.** `MENU_KEYS[0]` is repointed at
a key nothing registers, which is exactly what a failed decode looks like to the gate:

    BUSTED   7 fallback rows, icons ship / lock / gear / help / medal / star / door
    CONTROL  restoring the key puts the seven plates straight back (7 blits)

On the code this replaces that arm reports `EXIT GAME -> <undefined>`.

⚠ **AND THE ARM FAILED TWICE BEFORE IT PASSED, BOTH TIMES FOR REAL REASONS.** It was first
placed after the probe had already navigated to ACHIEVEMENTS, so `drawMenuButtons` no longer ran at
all - it reported 0 fallback rows, which is indistinguishable from "the fallback is broken". **The
CONTROL is what said otherwise**: 0 blits with the key restored means the title is not being drawn,
not that the menu is empty. An arm with no control would have sent me after a bug that was not there.

⚠ **THE PROBE'S FIRST RUN FAILED THREE ASSERTIONS AND THE GAME WAS RIGHT BOTH TIMES.**
It stepped **two** frames and then measured row pitch across the lot, so the gap between the last
row of frame 1 and the first row of frame 2 came out as **-288px** — a row apparently flying off
the top of a menu that is fine. And it asserted "every row draws at one measured box", which is not
what the layout claims: the layout fixes the **width** and gives each plate its own height, so the
honest assertion is *not stretched* (max-min <= 2px), which is exactly the quantity Mike was
looking at.

Proof frames: `docs/proofs/awards_0916/13_title_buttons.png` (the seven cuts at 2x with their
measured aspects), `15_title_seven.png` (the live title), `16_awards_from_title.png`.

---

## 5b. The suite, and a flake that took three baseline runs to settle

Against a clean `git worktree` at HEAD (`9f64e731`), names compared with the numbers masked:

    baseline   4,648 ok / 56 fail      sand-tank fixture: pass
    baseline   4,648 ok / 56 fail      sand-tank fixture: pass
    baseline   4,647 ok / 57 fail      sand-tank fixture: FAIL   <- zero code changes
    mine       4,656 ok / 57 fail      sand-tank fixture: FAIL
    mine       4,656 ok / 57 fail      sand-tank fixture: FAIL

**+9 ok, which is exactly section 365, and the run-3 pair has identical failure sets.**

⚠ **THE SAND-TANK FIXTURE WAS NOT WAVED AWAY AS "THE KNOWN FLAKE", BECAUSE THE EVIDENCE DID NOT
SUPPORT THAT AT FIRST.** It passed on the baseline and failed on my tree twice running, which is
what a real regression looks like. Two things settled it, in this order:

1. **No mechanism.** `git diff assets/game.js` touches **zero** lines matching
   `random|spawn|wave|enemies|mapScroll`; the whole diff is the title menu and the achievement
   plaques.
2. **The fixture is order-sensitive by construction.** It runs 6,000 frames of live stage-1 play
   and records only `enemies.slice(-4)[0]` each time `waveIdx` increments, off an **unseeded** wave
   plan - so whether `s1tankapc` is ever the unit it happens to record depends on spawn ordering.
   The baseline's own passes print different scrolls each run (2302, then 2296).
3. **A third baseline run, with nothing changed, failed it.**

Measured rate this session: baseline 2 pass / 1 fail, mine 0 pass / 3 fail, over five full runs.
A 2-2 split is not evidence either way, and the third run is what made it one.

---

## 6. Two assertions repointed, not worked around

- `probe_help_0912a.py` pinned the **whole six-row menu** — `['NEW GAME','PASSWORD','OPTIONS',
  'HELP','CREDITS','EXIT GAME']` — while its own message claims only *"HELP is the fourth title
  button"*. ACHIEVEMENTS landing in 0916 failed it on a build where HELP is exactly where it
  belongs. It now asserts the claim: `items.index('HELP')==3` under OPTIONS.
- `test_awards_0916.cjs` asserted the ACHIEVEMENTS key and registration path; both follow the
  repoint, and the path assertion now pins `title_0916/` so the family cannot drift back.

Suite section **365** covers the family: the three tables agreeing in length, every key ending
`_0916`, every key registered under `title_0916/`, **no cell shadowing any of them**, the atlas
buttons still present for the pause menu, the gate reading `MENU_KEYS[0]`, and `titleMenuLayout`
still deriving its row count.

---

## 7. Seen in the proof, NOT fixed (pre-existing, flagged for Mike)

The in-canvas control hint row draws the D-pad glyph **on top of** its own label, so "MENU" reads
as "MEWII". The strip below the canvas renders the same labels correctly. That is the 0914 control
hints work, not this drop, and it is his call whether the glyph or the word moves.

---

## Files

    _BUILD_SOURCE/title_buttons_0916.py          the slicer (seven names, refuses on any other count)
    assets/game/ui/title_0916/btn_*.png          the seven plates
    assets/game.js                               registration, MENU_KEYS, TITLE_ICONS, the gate
    _BUILD_SOURCE/test_title_buttons_0916.cjs    suite section 365
    _BUILD_SOURCE/probe_title_0916.py            the Chromium probe
    docs/qa/title_buttons_0916.json              the QA record
