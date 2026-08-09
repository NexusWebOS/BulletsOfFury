# PASSOVER — drop 0806v   (135.7 MB THAT DECODED BEFORE THE TITLE SCREEN)

Build: `BulletsOfFury_0806v`
Harness: **2,061 assertions / 187 sections / 0 failing**, twice, reaching the banner.

---

## 1. I WENT LOOKING TO SHRINK THE STAGE FONTS AND FOUND SOMETHING BETTER

The plan was to downscale them — 2688x1152 each, 12.4 MB, for 47 glyphs. **Measured first, and
downscaling would not have paid:** the glyphs are stored 254px tall and `stageText` is called
with a height of at most 150. At 2x-of-drawn that is 300, which is already above what they are.
No headroom. Good thing to check before resampling nine sheets.

**The real problem was one line in the loader.** It built an Image for EVERY stage font and EVERY
stage-art sheet up front, and `mk()` sets `.src` immediately — so fourteen sheets decoded before
the title screen ever appeared:

    9 stage fonts   2688x1152 each    111.6 MB
    5 stage art    ~1024x1100 each     24.1 MB
                                      --------
                                      135.7 MB resident at boot

For content the player sees **one stage of at a time**.

## 2. THE FIX IS A GETTER

`img` is now a lazy property: the Image is created and its `src` set the first time something
reads it, and cached from then on. Reaching stage 3 costs stage 3's sheet and nothing else.

Everything downstream is untouched — callers still just read `.img` and cannot tell the
difference. Verified: all 14 lazy, all nine fonts still carry their full 47-glyph set, reading
one produces a real image, and `stageText` still draws through it.

## 3. WHY THIS IS THE PATTERN TO LOOK FOR

Three of the last four wins were the same shape, and none of them was about the art:

    0805m   art stored 60-90x larger than it is drawn      141.6 MB
    0806u   8,192 frames referenced one at a time            205 MB on disk, 8,157 fewer files
    0806v   fourteen sheets decoded for content unseen      135.7 MB

**Nothing was wrong with any of the pictures.** The cost was in when and how they were loaded,
which is invisible unless you measure it. Downscaling the fonts — the obvious move — would have
resampled nine sheets for zero gain and left the 135.7 MB exactly where it was.

## 4. STILL OPEN

* Helix contact burst POSITION · flame / ice fade-on-release · miniboss slow/shield ·
  stats-screen alignment.
* The **ice-level freeze** retest, and a browser look at the 43 packed sheets from 0806u.
