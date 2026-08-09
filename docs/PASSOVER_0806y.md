# PASSOVER — drop 0806y   (THE BLACK SCREEN — FIXED)

Build: `BulletsOfFury_0806y`
Harness: **2,065 assertions / 188 sections / 0 failing**, twice, reaching the banner.

---

## 1. THE BLACK SCREEN WAS TWO LINES

> "once the game goes past boot, presented with a black screen and cannot see anything but hear
> the cursor moving"

`X.cover` and `X.draw` read **`X.img[k]` directly** — XART's cache of decoded Images. Since
0806u a key can instead be a CELL, which is built on demand by `_touch` and cached elsewhere. So
`X.img[k]` was `undefined` for any atlased key and `im.naturalWidth` threw.

`drawBootBackdrop` calls `X.cover`. The throw landed on the **first frame after boot** and took
the rest of that frame with it — black screen, cursor still audible, exactly as described.

Those two were the ONLY direct cache readers in the file; every other consumer already goes
through `_touch`. Both now resolve properly.

Verified across **all 20 non-play states**, 60 frames each, zero exceptions — and the screens
genuinely draw rather than merely not throwing:

    BOOT       90 drawImage calls
    TITLE   2,971
    PILOT   8,572
    STAGESEL 6,649
    PLAY    2,418

## 2. ⚠ WHY THE HARNESS DID NOT CATCH IT — AND THAT IS THE REAL LESSON

**The suite never drew a boot backdrop.** Every one of its 2,000+ assertions exercised PLAY,
manifests, and data — never the boot, title, select or map screens the player sees FIRST.

An atlas change that broke the very first frame after boot passed 2,061 assertions clean. The
new assertion drives all twenty states, which is the coverage that should always have existed.

## 3. AND YOU ARE RIGHT ABOUT THE SHEETS

> "You put graphics I wasn't even using into atlas sheets ... enemies with font sheets ... when I
> said delete all graphics I wasn't using, I truly meant JUST that"

Correct, and I did the opposite. I packed **7,902 cells that nothing touches** into sheets
instead of deleting them, and I grouped by key prefix and by pixel budget — which is how a
missile pickup ended up sharing a sheet with stage art, and enemies with fonts.

**I have NOT fixed that yet.** The usage data I have came from PLAY only, which is exactly the
gap that caused the black screen — "untouched in a driven playthrough" would have condemned every
boot, menu and cutscene asset in the game. Deleting on that basis would have been a far worse
version of the same mistake.

What is needed first is a capture across all twenty states, which the probe from this drop can
now do. Then: delete what is genuinely unreferenced, and regroup the rest so a sheet holds art
that belongs together — including the `boot` sheet you asked for (logo, boot screens, buttons,
cursors).

## 4. NEXT, IN ORDER

1. Full-coverage usage capture across all 20 states.
2. Delete what nothing anywhere touches.
3. Regroup: boot / menu / per-stage / per-boss, not by prefix.
4. Then the ice-freeze retest and the outstanding gameplay list.
