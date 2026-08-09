# PASSOVER — drop 0806o   (RESTRUCTURE: SECOND ATTEMPT, REVERTED, RECIPE NOW COMPLETE)

Build: `BulletsOfFury_0806o`
Harness: **2,063 assertions / 185 sections / 0 failing**. Tree identical to 0806m/0806n.

---

## 1. THE ATTEMPT GOT MUCH FURTHER, AND THEN STOPPED FOR A GOOD REASON

The move itself is now a solved problem:

    182 dirs -> 25          9,221 files relocated (art AND audio)
    player 687 · enemy 3,575 · game 4,959  (game/music 22 · game/sounds 91)
    filename collisions                     0
    broken paths across ALL namespaces      0
    protected folders re-created with .keep 3

**21 assertions still failed** — and every one of them asserts the OLD folder layout:
`enemies/boss`, `enemies/tanks`, `enemies/drones`, `music/stages`, per-stage font folders, a
`gamefont` folder. They are not breakage; they are expectations that the restructure
deliberately invalidates.

Re-pointing 21 assertions and verifying them properly is real work, and I did not have room to
do it and check it. Mike cannot test for another hour. **A red suite does not ship**, and I have
now been burned twice on this exact task — so it is reverted again rather than shipped on the
argument that the red is "only expectations". That argument is how 0724dq happened.

## 2. ⚠ THE FINDING THAT MATTERS: THERE ARE NINE NAMESPACES, NOT ONE

0806n failed because I rewrote `BOFX.img` and missed the audio. This attempt failed further in
because I rewrote `BOFX` and `BOFA` and missed **seven more**:

    BOF     BOFA    BOFFI   BOFPI   BOFQL   BOFRS   BOFTK   BOFTM   BOFX

`window.BOF` alone carries `logo`, `boot`, `mapJungle`, the main atlas, and a per-stage
`atlas` path for every stage font and stage card.

**The fix is generic and it works.** Do not rewrite namespaces one at a time. Treat
`manifest.js` as text, pull every `"assets/..."` string out of it, and repair by BASENAME
lookup against the moved tree:

    distinct asset paths in manifest   9,240
    broken after the move                  3
    repaired by basename                   3
    ambiguous (same basename twice)        0
    broken after repair                    0

That one pass fixed every namespace at once, including the seven I had not even identified.
Because the flatten produces zero basename collisions, basename lookup is unambiguous — which
is the property that makes this safe.

## 3. THE COMPLETE RECIPE, NOW THAT ALL THREE FAILURE MODES ARE KNOWN

1. **Bucket rules** — unchanged, they produce 0 collisions and 0 disagreements over 9,113 art
   files. Already solved.
2. **Move art AND audio together**, collision-checking the combined set before touching disk.
3. **Repair paths generically by basename across the whole manifest text.** Nine namespaces;
   never enumerate them by hand.
4. **Re-create every folder in `PROTECTED_ASSETS.json` after cleanup**, with a `.keep` marker.
   Never `find -empty -delete` without this — empty is not unneeded.
5. **Re-point the ~21 layout assertions in the same commit**, then verify green before shipping.

Steps 1-4 are done and proven. **Step 5 is the only thing left**, and it is the reason this is
not shipped.

## 4. AND THE THING WORTH REPEATING

Folder layout still buys **zero** runtime speed (0806n §1). This is a maintainability change.
The performance work that actually moved the needle was resolution and decode count:
**2,891 MB -> 2,555 MB decoded**, none of it from layout.

## 5. STILL OPEN

* Restructure step 5 above.
* Helix contact burst POSITION · flame / ice fade-on-release · miniboss slow/shield ·
  stats-screen alignment · the ice-level freeze retest.
