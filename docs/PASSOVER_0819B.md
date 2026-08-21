# 0819b — LEVEL 2'S CAST, AND THE CAMERA THAT WAS HIDING 40% OF THE WORLD

Mike's second 0819 message, both halves:

| # | item | state |
|---|------|-------|
| 1 | level 2: fast planes that **don't shoot** and go at the player | **DONE** |
| 2 | lava enemies firing the **magma ball we already have** | **DONE** |
| 3 | **spin**, **dodge**, and **fly off if they miss** | **DONE** |
| 4 | the reavers keep doing what they do | **UNTOUCHED, deliberately** |
| 5 | Raiden/Fire Shark don't lose the action when scrolling — zoom out | **DONE** |

---

## THE CAMERA: 40% OF EVERY STAGE HAS BEEN OFF SCREEN

⚠ **MEASURED: EVERY STAGE IS 800 WIDE AGAINST A 480 VIEWPORT.** The player has been seeing 60% of
the world, with the camera sliding **320px** to chase them. Anything on the far side is simply not
on the screen. That is exactly what Mike noticed against Raiden and Fire Shark — and those games
have **no horizontal camera at all**: the playfield *is* the screen, which is why they never lose
the action.

So the world is now **scaled to fit the viewport**, and at fit the camera stops sliding entirely —
`camX` collapses to 0 because the visible width *is* the world width. `VIEW_FIT` is the one dial;
`0` restores the 0818 camera line for line.

**Not one gameplay coordinate changed.** Units, spawns, hitboxes, wave scripts and every tuned
constant go on working in the same 800-wide world space. Only the draw transform moved.

⚠ **THE ZOOM IS ANCHORED AT THE BOTTOM, AND THAT IS THE WHOLE DESIGN.** The player flies in a band
at the foot of the screen and *every* constant in the file is written against it — culling at
`y>VH`, the fire gates at `VH*0.85`, the arena floor. Anchoring the bottom keeps world `y=VH` on
the bottom edge, so that band is pixel-identical and the extra rows appear **above**: you see
further up the level, which is more warning, not less. A centred zoom would have moved the
player's own band and quietly changed all of it.

### Four things the zoom broke, each found in a rendered frame

1. ⚠ **NOTHING IN THIS ENGINE CLEARS THE PLAY CANVAS.** `drawBG` painting rows 0..VH *is* the
   clear, and that was sufficient for exactly as long as those rows were the whole screen. The new
   band held the **previous frame** — torn stripes across the top third. One `fillRect` over the
   visible band, and the guarantee is explicit instead of incidental.
2. ⚠ **THE LIQUID BED STOPPED AT y=0.** Water and lava are *keyed holes* in the master with an
   animated bed painted underneath, so a bed ending at the old top edge left every river as a
   **black void** in the new band. Walked up in whole tiles, so the phase — and the seam — is
   where it was.
3. ⚠ **THE MASTER WINDOW WAS FIXED AT VH**, so the terrain ended in a hard line across the screen.
   `winH` is the view height now. `rangeSrc` shrinks with it and that is correct: it maps the
   plate onto the window, and a taller window has fewer legal top rows. The level's **pacing** is
   `range`, a different number, so no stage got shorter in time.
4. ⚠ **SPAWN CLEARANCE WAS MEASURED FROM THE OLD TOP EDGE.** With the visible top at `y=-341`, every
   wave authored "just above the screen" at `y=-40` would have **materialised in full view** —
   Mike's "enemies appearing out of thin air", the complaint this file records him making about
   twenty times, re-created by the fix for a different one. `viewTopY()` at the single chokepoint.

### And a fifth that predates the zoom by drops

⚠ **`drawWarning` HAS NO CAMERA COMPENSATION AND NEVER HAS.** It draws at `VW/2` *inside*
`translate(-camX)`, so on an 800-wide stage the WARNING banner slid up to **320px off-centre** and
hung off the edge of the screen. **I have a picture of it from this session's own stage-3 probe** —
the miniboss alert reading `PPROACHING!` with its left third past the edge — and I first read that
frame as normal.

This is the world-vs-screen family CLAUDE.md already records **four** times (the launch seam, the
outbound routes, the level-1 ship, the laser probe). It is the fifth. The zoom did not cause it; it
made it impossible to keep ignoring, because a scaled context shrinks these as well as displacing
them.

Fixed by **moving** them below `ctx.restore()` rather than by adding a compensation to each —
outside the transform there is no camera and no zoom to compensate for, so a panel added there
later cannot inherit the bug. `worldXformEscape()` covers the few that legitimately draw screen-space
from *inside* (the in-play dialogue box). ⚠ **AND IT IS NOT `setTransform`** — 0814b records
`freezerL3Draw` escaping that way and throwing away the SS=2 backing, rendering at half size. It
applies the exact inverse, in reverse order, and nothing else.

---

## LEVEL 2'S NEW CAST

Three new behaviours on art families that already ship. No placeholder art, and the reavers, the
mantis and every original wave are untouched.

| kind | answers | how you beat it |
|---|---|---|
| `lance` on `loopcharge` | "fast planes that dont shoot but go towards the player" | shoot it before it lands |
| `magmagun` | the magma ball, shelled down a lane | cross the lane during the reload |
| `spinner` | "spin" — winds up, rings the screen, leaves | read the wind-up, be off the ring |
| `dodger` | "dodge attacks, and fly off if they dont hit" | lead it, or wait out the pass |

The silent charger is stage 2's **own** elite interceptor rather than a jet imported from stage 1,
so the Fire Shark mechanic arrives on art that already reads as an interceptor. The fly-off is the
**shared** rule, not a per-unit quirk: all of them commit to one pass and leave, because a unit
that lingers turns the stage back into the wall of noise Mike has objected to since 0810q.

### The magma ball was already in the game, and the obvious name was the wrong one

⚠ **`bfx_magma_p` / `_m` / `_i` IS A COMPLETE AUTHORED WEAPON WITH ZERO REFERENCES** — a 6-frame
molten round trailing a crown of fire, a 6-frame starburst muzzle, and a 6-frame impact that
scatters into cooling debris. Same family as the 45-key thermoshock 0814a found: authored,
registered, never fired.

⚠ **AND RULE 1 EARNED ITS PLACE AGAIN.** `nqm_shmagma` reads like "magma shot" and is a **275×335
armoured hull with a lava core** — a structure piece. Rendered before it was trusted; using it
would have put a boss-sized machine on screen as a bullet.

⚠ **`PROJ.type` IS THE BASE FAMILY, NOT THE ART.** `type:'magma'` failed §157, which enforces
Mike's own rule that every round reduces to one of his nine masters. The magma ball *is* a
comet-family round; the authored art still reaches the screen because the draw resolves `FIRETYPES`
by the **kind name**. Exactly how `eshot` is wired.

⚠ **THE MUZZLE REEL IS SIX FRAMES AND THE FLASH PLAYER WAS HARDWIRED TO FOUR** — it would have
played 0..3 of 6, the same silent truncation CLAUDE.md records for the 12-frame thermoshock under
`%8`. The reel length travels with the flash now.

---

## THE DISPATCHER IS A QUEUE, NOT A CLOCK

⚠ **TEN NEW WAVES PUSHED `skim` OFF THE END OF LEVEL 2.** A wave only fires when the live count is
under the cap, so inserting ten shoved the tail of stage 2's own timeline past the end of the run:
the 110s soak measured the cast at **6 of 7**. Trimmed to six; all four new behaviours are still
represented and the duplicates are what went.

**This is 0809n's failure exactly** — five prop waves once shoved stage 1's sand tanks and its
miniboss off the end. Adding waves to a full plan costs something, and the thing it costs is the
waves already at the back.

---

## ASSERTIONS REPOINTED

- **`stage 1 camera pans right`** — **inverted**. With the world fitted there is nothing to pan to,
  and a `camX>250` there would mean the zoom had stopped working. The **leak** check under it is
  kept alive by driving the old camera explicitly at `VIEW_FIT=0`, so the pan machinery is still
  covered and the leak still has a real non-zero value to catch.
- **the entry runway** — the claim is unchanged (a side entry clears the visible edge, by the same
  margin wherever the camera is); it now measures against `camRightX()`/`camLeftX()`, the helpers
  the **spawn itself** asked, instead of a hand-built `camX+VW` that no longer describes the window.
- **VOLC counts** 12→15 and 8→10 ships — a behaviour roster, not new art, so the 72-key art check
  above them is untouched.

---

## HOW TO VERIFY

    node --check assets/game.js
    node _BUILD_SOURCE/test_fl.js
    python _BUILD_SOURCE/shoot.py --state PLAY --stage 1 --seconds 14 --fps 2
    python _BUILD_SOURCE/shoot.py --state PLAY --stage 2 --seconds 30 --fps 3

Pixels: stage 1 now shows islands **edge to edge** across the full 800, three jets and two boats on
screen at once, the water bed filling the whole band, and the player at the bottom — with the
camera no longer sliding. Stage 2 renders the full canyon width and its MAGMA WARD miniboss
cleanly.

---

## ⚠ ONE OPEN REGRESSION, NOT DIAGNOSED

**`skim` no longer appears in the stage-2 110s soak — the cast measures 6 of 7.** It passed before
this drop, so it is mine. Trimming the added waves from ten to six did NOT fix it, which rules out
the dispatcher-starvation theory the trim was based on.

What is already ruled out, so the next person does not repeat it:
- **not the dispatcher.** The soak splices the field down to two units every 0.5s, so dispatch is
  never gated; every wave gets its turn inside 110s.
- **not the plan.** Stage 2 still authors three `skim` waves (t=4.5, 11.5, 34.5).
- **not the x-bounds.** `volcTick` kills a skim at `x < -40 || x > W+40`; at either the old
  `offRightX` (510) or the new one (830) it survives its first tick and travels inward.

**Where to look next:** the soak only records a unit if it is alive at a 0.5s sample boundary, so
the question to ask is whether skim is *spawning at all* — wrap `spawnEnemy` and count `skim`
calls over the run before looking at any behaviour. If it spawns and vanishes inside 30 frames,
the suspects are the spawn-time x remap and `offRightX` under the zoom; if it never spawns, the
wave is being refused and the plan is the place to look.

## STILL OPEN

- `VIEW_Z_MIN` is 0.55 and the fit for an 800-wide stage is **0.60**, so sprites are 60% of their
  previous on-screen size. That is the trade for seeing the whole world, and **it is a creative
  call Mike owns** — one number if he wants it tighter, or `VIEW_FIT=0` to put it back.
- The `laser` fire mode from 0819a is still fielded only by stage 3.
- Stage 2's `el_lr` reavers still fly `s1jet` with guns, deliberately: Mike said they are great.
