# PASSOVER — drop 0806s   (THE ENEMY SHEETS: MECHANISM FOUND, NOT INSTALLED)

Build: `BulletsOfFury_0806s`
Harness: **2,055 assertions / 186 sections / 0 failing**, twice, reaching the banner.
Tree unchanged from 0806r — 9 folders, 0 broken paths.

---

## 1. I FOUND WHY 0806a BROKE THE GAME, AND IT IS ONE WORD

0806a shipped per-stage enemy sheets by handing back a descriptor and expanding it in a wrapper
installed on **`ctx`** — one context instance. This file creates **twenty-six** 2d contexts, and
a descriptor reaching any of the other twenty-five is not a `CanvasImageSource`, so the browser
threw mid-frame and everything queued behind it stopped drawing. That is the "I shoot and
everything vanishes".

**Every 2d context in a document shares `CanvasRenderingContext2D.prototype`.** Patching the
PROTOTYPE covers all twenty-six at once — present and future, including contexts created later.
One word different, and it addresses the actual cause rather than the symptom.

**And it is safe here specifically**, which I checked rather than assumed: this file has **zero
non-drawImage consumers of an image**. No `createPattern`, no `texImage2D`, no assigning an image
to `.src`. Every image in the game goes through `drawImage`, so nothing else can ever be handed a
descriptor.

## 2. AND I STILL DID NOT SHIP IT

The sheets rebuilt cleanly against the new tree — 459 cells, nine sheets, all inside the 4096px
mobile texture limit:

    common  3.6 MB · s1 9.8 · s2 31.7 · s3 36.1 · s4 9.1 · s5 5.3 · s6 16.4 · s7 10.7 · s8 12.4

**The probe cannot verify the patch.** Three fidelity layers deep:

1. Fake contexts were plain object literals, so the prototype patch could not reach them.
   Re-parented them with `Object.setPrototypeOf` — still threw.
2. Because the fake ctx defines `drawImage` as an **own property**, which shadows the prototype
   entirely. A browser's does not.
3. Fixing that means rewriting the probe's context model, and at that point the probe is
   testing itself rather than the game.

On a feature that has already broken Mike's game once, "it should work by the rules of
JavaScript prototypes" is not evidence. **The wiring is removed and the finding is written into
the source where the next attempt will read it.** The sheets are built, the packer is
reproducible, and it is a fifteen-minute job to install once a real browser has confirmed it.

## 3. WHAT WOULD ACTUALLY SETTLE IT

Mike can test now. The check is one line in the browser console after the game loads:

    CanvasRenderingContext2D.prototype.__bofCellPatch

If a build with the patch installed returns `true` and stage 1 draws enemies normally, it works
and the 1,322 MB enemy set can move behind sheets. That single observation is worth more than
anything more I can do headlessly.

## 4. STILL OPEN

* The enemy sheets above — mechanism known, needs one browser confirmation.
* Helix contact burst POSITION · flame / ice fade-on-release · miniboss slow/shield ·
  stats-screen alignment.
* The **ice-level freeze** retest.
