# Passover 0812b — the last dead menu, six missing art files, and the stats screen the tester photographed

Continues 0812a. Two of the tester's items close here, and a third thing was found on the way that
neither of us was looking for.

---

## 1. ⚠ SIX TRACKED ART FILES WERE MISSING FROM THE WORKING TREE

Found by chasing a 404 on the stage-select screen, not by looking for it:

```
 D assets/game/logo.png      D assets/game/stage1.png     D assets/game/stage2.png
 D assets/game/stage3.png    D assets/game/stage4.png     D assets/game/stage5.png
```

Deleted from the working tree, never committed — `git checkout --` restored all six.

**What it cost while they were gone:**

- Two 404s on every boot/stage-select (`logo.png`, `stage1.png`), which is why `grep` found no such
  path in game.js: the paths are built at runtime from the manifest, and the manifest was right.
- **The suite went from 5 failures to 13** and the eight extra were all this — nine assertions
  across four sections exist specifically to catch a missing manifest path, and they did.
- **Every percent sign on the stats screen was invisible** (see §3). `%` exists in exactly one font
  sheet in the entire build: `stageArt[2]`, which *is* `stage2.png`.

**⚠ THE ZIP MIKE ALREADY SENT IS FINE.** Checked rather than assumed — all six are in
`BulletsOfFury_playable.zip`, so the deletion happened after 0811z packaged it. Nothing to re-send.

⚠ **CLAUDE.md's "two 404s at boot" is now fully closed**, but not the way 0811z recorded it: one
was the font path, and the other two were these — a missing file, not a wrong path. The only
request that still 404s is `assets/data/ui_layout.json`, which is optional and guarded.

---

## 2. Stage select takes the mouse — the last pointer-dead screen

0812a fixed mode select and left four. Campaign hub, campaign slots, credits and stage clear were
done with a shared `menuMouseList` helper; **stage select could not use it** because it is not a
vertical list — the flags sit at authored map coordinates.

The flag hit test is built from `SSEL_POS` and the same `S=0.75 / MX=0 / MY=64` transform the
draw loop uses, read from the same constants rather than re-derived, so the clickable spot cannot
drift from the art.

⚠ **TWO-STAGE, NOT INSTANT DEPLOY.** Clicking a flag you are not on **moves the cursor**; clicking
the one you are already on launches. One click doing both would send the player into a level they
were only pointing at, and deploy is irreversible once the stage card starts. Locked flags are not
clickable at all — same `_hi` bound the arrow keys respect.

Verified with real DOM MouseEvents, and the probe recomputes the map transform independently so a
wrong constant shows up as a miss instead of being hidden:

```
CAMPAIGN HUB   click row 2 / 0 / 1  -> campHubIndex 2 / 0 / 1        ok
STAGE SELECT   flag 5 map(497,390) -> screen(373,356)
               first click  -> sselCursor 5, committed False          ok
               click flag 3 -> sselCursor 3                           ok
               second click on flag 3 -> deployed True                ok
CREDITS        click anywhere leaves CREDITS                          ok
                                                        8 ok / 0 failed
```

Audit of all thirteen menu screens: **pointer-dead: NONE.**

---

## 3. The stats screen: three faults, one cause

> *"Stage-clear text centring — the label column and the value column disagree; the rank letter and
> portrait collide with the first rows."*

⚠ **`stageText`'s third parameter is named `cx` and IS the centre** — its last line is
`let x = cx - total/2`. Three call sites passed a column EDGE as that centre:

| what | passed | drawn at | effect |
|---|---|---|---|
| row labels | `rowsX` | `rowsX - width/2` | long labels reached 60px left, over the portrait column |
| SCORE + digits | `rowsX`, `rowsX+rowsW` | straddling both edges | digits ended **43px** right of every value above |
| PASSWORD | `rowsX` | `rowsX - width/2` | 50px left of SCORE directly above it |

So **nothing moved into the portrait — the long labels grew out over it.** COLE, RANK and the rank
letter were never misplaced. The row VALUES were already correct (`right - width/2`), which is
exactly why the two columns disagreed: they were positioned by two different rules.

All of them now measure the string and offset by half of it. Proof:
`docs/proofs/stageclear_{mid,rows,settled,longpw}_0812b.png`.

⚠ **AND EVERY PERCENT SIGN WAS INVISIBLE.** ACCURACY read "63", MISSILE HITS "85", SPECIAL HITS
"92" — the number, then a gap. `stageText` turns an unmapped character into a blank
(`items.push(null)`) and says nothing, so a missing glyph looks like a spacing quirk. Checked all
eighteen font sheets: `%` exists in **one**, `stageArt[2]`. `stageTextMixed` already exists to
borrow per glyph — the stage-1 font borrows `S` from the same sheet — so the face does not change.

⚠ **THE BORROWED `%` IS STAGE 2'S MOLTEN ONE.** Its cell is 110px against the digits' 56 because a
magma drip is baked into it, which is why it first rendered small, raised and fire-orange. Tinted
to `#bbb574` — **sampled off a rendered digit, not picked** — it reads as part of the number and
the drip is a faint tail at 12px. It is still not a BOF-face glyph: **if Mike wants a proper `%` in
the game font, that is authored art and his call.**

⚠ **THE PASSWORD CANNOT BE RIGHT-ALIGNED like every other value**, because it is typed: `shown` is
a growing prefix and pinning its right edge would make it appear to type backwards. Left-anchored,
with the anchor measured from the FULL password so the block does not creep as it types, and
clamped clear of the label. IRON is four characters and merely looked tight; an eight-character
password's left edge lands 30px *inside* "PASSWORD" at the authored 0.52 centre. Both rendered:
`stageclear_settled` and `stageclear_longpw`.

---

## 4. ⚠ An assertion pinned a literal, not the property it names

`test_fl.js` §201 checks "the score draws untinted" by matching the string
`"ph*0.040, null, 0, fl, 0.06)"`. Hoisting the size into a named constant — a change that touched
neither the tint nor the size — failed it. The assertion now checks the two tint arguments and,
separately, that the size is still `ph*0.040`. Third time this class has come up; the rule in
CLAUDE.md holds — **read the assertion before fixing the code.**

---

## 5. Probes that would have lied, and one bug that did not exist

- **`probe_stageclear` first reported `t=0.00` for all three timeline points.** `stateT` is advanced
  by the game loop, not by the draw call, so pumping `drawStageClear` alone rendered the same 0.18s
  early-out three times — an empty panel, three files, no warning. The probe now drives the clock.
- **And it seeded no stats**, so every row read `0` / `0%` / `0:00` — the shortest possible value
  string, the one case that *cannot* show a column disagreement. Seeded to real end-of-stage numbers.
- **The "broken preview card" in the stage-select screenshot was not a bug.** It is the stage banner
  mid-type-on: it scales in from 0.45 and wipes its label left-to-right, and the screenshot caught
  it 0.1s after a cursor change. Rendered at 90 and 400 frames to confirm it settles correctly
  before writing a line of code against it.

---

## 6. Suite

**2,507 assertions / 222 sections / 5 failures** — back to the documented baseline, from **13** with
the art missing. The five are the long-standing ones (`_superseded/` ledger ×3, volley round count,
flash families).

New **§217** asserts both of this drop's fixes as *properties*, not literals: all thirteen menu
screens carry a pointer handler, and every `stageText` call in `drawStageClear` that places from a
column edge offsets by a *measured* width.

⚠ **My first cut of §217 failed on correct code** — it scanned the call line alone and flagged two
calls that measure into a local (`_lW`, `_pwLW`) on the line above. It now collects those locals
first. Checked both directions before re-running the ten-minute suite: it passes on the current
code and **still flags both call sites when they are reverted to the 0812a form**.

---

## 7. Still owed from the tester's list

- **A miniboss is still the hitbox square.** Mike: *"never replaced it"* — stage not identified.
- **Stage 8 boss**: four forms, very high HP, same attack pattern throughout. Mike: *"filler shit"*.
- **Signs scroll when told not to**, and a waterfall sits in the middle of the road.
- **The barrel roll fires on micro-adjustments.** Tester wants hold/toggle **shift**; Mike wanted a
  cooldown. Feel change to core movement — **needs Mike's call on which**.

And found here, not on his list: **the pilot card uses the same edge-as-centre pattern** at three
call sites (`lx+cw*0.20`, `bx+ch*0.075`, `bx+ch*0.095`). The pilot card is already a known-open
item; whether those are the same fault or deliberate centres has not been rendered yet.
