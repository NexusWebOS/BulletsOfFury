# PASSOVER — drop 0807e   (ROOT-CAUSED THE COUNTDOWN AND THE MISSING STAGE CARD)

Build: `BulletsOfFury_0807e`
Harness: **2,113 assertions / 193 sections / 0 failing**, twice, reaching the banner.

Mike came back from a full playthrough with ELEVEN issues. This drop fixes the one that was
causing two of them, and it was mine.

---

## 1. ⚠ THE BARE ORANGE "3" WAS A REGRESSION I SHIPPED IN 0806v

Mike: *"the countdown now starting using my game over continue countdown instead of our 3-2-1"*
and *"I didnt see the stage card"*.

Both are the same bug, and it is not the countdown code — that code is correct and draws
GET READY plus a 3-2-1 in the stage font. **It was falling through to its fallback.**

`curFontArt()` and `uiFontArt()` gate on `img.complete`. In 0806v I made the nine stage fonts and
five stage-art sheets decode on FIRST USE instead of at boot — worth 135.7 MB off the boot cost —
but **reading `.img` is what CREATES the Image and starts its download.** So the first read hands
back an Image that has not decoded, the gate is false, and every caller silently drops to its
plain-font path. On a hotspot pulling a 12.4 MB font that gate stays false for seconds.

The fallback drew ONLY the number, in flat orange BOFmil. That is exactly the bare "3" in Mike's
screenshot, and it is why he read it as the continue counter — that is what it looks like.

**Two fixes, because either alone leaves a hole:**

* `warmStageSheets(n)` starts the decode at stage entry AND on the campaign map for the
  highlighted stage, so it has the whole selection plus the runway sequence to finish. Laziness
  is still right; nine fonts at boot was the original sin.
* The fallback now carries GET READY, the same pop, and an outlined number. A fallback that drops
  half the content is not a fallback.

## 2. ⚠ THE HARNESS COULD NOT HAVE CAUGHT THIS

The fake `Image` in the probe completes synchronously, so `img.complete` is never false headlessly
and the gate always passes. **That is precisely why it shipped clean.** Section 193 therefore
asserts STRUCTURE — that the decode is kicked off before the frame that needs it, and that the
fallback is worth falling back to — rather than trying to simulate a load delay it cannot model.

Worth remembering the next time something is gated on `complete`: this harness will always say yes.

## 3. THE OTHER NINE, TRIAGED AND NOT YET TOUCHED

Recorded so none of it is lost:

    ROOT-CAUSE CANDIDATES (likely one bug each, cheap once found)
      no music from liftoff until stage 1 proper   Audio.startMusic fires at LAUNCH; needs a
                                                   probe on what curStage.music resolves to there
      miniboss on L2 routes into the lava section  stage routing, not the miniboss
      the tank stays on the mountain (L3)          ground unit not clamped to its terrain band

    ART / PLACEMENT
      wrong runway graphic, should be over water   seqRunway(1,'run') is picking the wrong plate
      the tiled beach water — never use it         needs the key retired from the liquid set
      dialogue boxes not using our box art         drawCommWindow frameKey not resolving in-game

    LAYOUT
      stats screen still off; remove that window   flagged four times now, and still owed

    SET-PIECE
      L2/L3 boss parts combine too close           the assembly offsets differ from the concepts

    SYSTEMIC — the biggest of them
      enemies vanish instead of dying              Mike: "No enemy EVER dies or destroys like
                                                   this, you start anchoring animated smoke we
                                                   have to sections of the enemy unit to signal
                                                   damage, then small fires."

The last one is a damage-state system, not a bug fix: smoke anchored to sections of a unit as it
takes damage, then small fires, then the death chain from 0807c. It is the one that changes how
the whole game reads, and it is where I would go next.
