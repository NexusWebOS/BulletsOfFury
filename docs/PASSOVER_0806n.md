# PASSOVER — drop 0806n   (RESTRUCTURE ATTEMPTED, MEASURED, REVERTED)

Build: `BulletsOfFury_0806n`
Harness: **2,063 assertions / 185 sections / 0 failing** — identical to 0806m. Nothing shipped
from the restructure.

---

## 1. FIRST, THE PART THAT MATTERS MOST

> "This is how to get the game to process and run as fast as possible"

**Folder layout has no effect on runtime speed.** The manifest maps a key to a path; the browser
opens that path. Whether it reads `assets/game/foo.png` or `assets/ui/icons/foo.png` costs
exactly the same. Nothing in the frame loop touches the directory tree.

What actually governs speed, all of it already measured this session:

    decoded RGBA resident   2,891 MB -> 2,555 MB   (0805m/0805n, from RESOLUTION not layout)
    decode calls            the atlases, where the sheet is small enough to be worth it
    draw calls per frame    unchanged by folders

So the restructure is worth doing for **organisation and maintainability** — which is a real and
good reason, and Mike's own words include "cleanly structured" — but it should not be expected to
buy a single frame. I would rather say that than let an hour go into something sold as a speed
fix that cannot deliver one.

## 2. THE RESTRUCTURE ITSELF WORKED, AND THEN THE SUITE CAUGHT WHAT IT BROKE

The move ran clean on its own terms:

    182 dirs -> 40           9,113 files relocated
    player 687 · enemy 3,575 · game 4,851
    filename collisions when flattening      0
    files whose keys disagreed on a bucket   0
    manifest keys 9,555, broken paths        0

Only ONE hardcoded asset path exists in the whole codebase (`assets/ui_layout.json`), so a pure
path rewrite looked safe, and by every check I had run it was.

**Then the suite failed 21 assertions**, and two of them were real damage rather than stale
path-shape expectations:

* **115 registered sounds stopped resolving.** There IS a sound registry. I could not find its
  loader by grep — audio paths appear only in `manifest.js` and `PROTECTED_ASSETS.json`, never in
  `game.js` — so I had left the 650 loose audio files alone on purpose. That was correct but not
  sufficient: the five audio entries that DO live in `img` moved, and something else resolves the
  other 115 by a route I never located.
* **Protected folders were deleted.** `assets/levels/level9` and `assets/fonts/stages/9` are on
  `PROTECTED_ASSETS.json` for the unbuilt stage 9. My `find -type d -empty -delete` removed them
  because they are empty *right now*. Empty is not the same as unneeded.

## 3. REVERTED, NOT PATCHED

Mike cannot test for an hour. Shipping a tree with a broken sound registry and deleted protected
folders — on the strength of me patching 21 assertions I had just caused — is precisely how
0724dq went (green suite, 4,000+ browser errors). The assets were restored wholesale from the
0806m build and re-verified: **9,555 keys, 0 broken paths, suite back to 2,063 / 0 failures.**

## 4. WHAT A SAFE RESTRUCTURE NEEDS, WHEN IT IS DONE

Recorded so the next attempt starts from here rather than from scratch. All of it is cheap now
that the shape is known:

1. **Find the audio loader first.** 115 sounds resolve by some route that is not `BOFX.img` and
   not a literal in `game.js`. Nothing moves until that is identified.
2. **Never `find -empty -delete`.** Walk `PROTECTED_ASSETS.json` and re-create every listed
   folder after the move, empty or not.
3. Keep the bucket rules exactly as they were — they produced 0 collisions and 0 disagreements
   across 9,113 files, which is the hard part and it is already solved.
4. Re-point the path-shape assertions in the same commit as the move, not afterwards.

## 5. STILL OPEN

* The helix contact burst POSITION (0806m §40) · flame / ice fade-on-release · miniboss
  slow/shield · stats-screen alignment · the ice-level freeze retest.
