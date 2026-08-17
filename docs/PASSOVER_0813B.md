# PASSOVER 0813B — the levels were being bilinear-doubled every frame

Mike: *"Its likke you've upscaled my levels in-game and they dont look as clear ... the stages were
already graphic at 800 wide my man, hwat are you doing?"*

He was right, and the cause was one line running on the frame setup.

---

## The bug

`assets/game.js:37729`, in the per-frame render setup:

```js
ctx.setTransform(SS,0,0,SS,0,0); ctx.imageSmoothingEnabled=true;
```

`SS = 2`, so the backing canvas is `VW*2 x VH*2` = **960x1024**. The stage masters are 800 wide and
`drawLevelMaster` draws them **1:1 in virtual space** (`drawW -> drawW`, `winH = VH`, verified) — the
geometry was never the problem. But every one of those 800 authored columns then landed on a 1600px
backing under `imageSmoothingQuality='high'`. A high-quality bilinear double **invents a blended
pixel between every authored pair**, which is exactly "they dont look as clear".

Then it happened again on the way out: `#screen-area canvas` carried `image-rendering:auto`, so the
browser bilinear-scaled the 960x1024 backing to the display size. **Two filters stacked on top of
hand-authored pixel art.**

### Why this hid for so long

This file already states the pack contract as nearest-neighbour and sets it at a dozen individual
draws — `drawCutscene`, the mech pieces, the arcade plates, the boss rigs, the ship blit at 18342.
Every one of those is a site that had to opt **out** of this per-frame line, and several carry
comments explaining the blur they were fixing locally (see 18330: *"the canvas default set once at
init, `imageSmoothingEnabled=true` with `imageSmoothingQuality='high'`"*).

So the SPRITES were crisp and the BACKDROPS were not, because backdrops never opted out. That split
is what made it read as "the levels look upscaled" rather than "the renderer is filtering".

## The fix

- `assets/game.js:37729` — `imageSmoothingEnabled=false` on the frame setup, so it holds for
  everything downstream instead of per-draw.
- `assets/game.js:4176` — the init default set to `false` too, matching the stated contract.
- `index.html:36` — `image-rendering:pixelated` on the game canvas. The equip-box canvas already had
  it; the canvas the player actually looks at did not.

The local `=false` lines are now redundant rather than load-bearing, and the save/restore pairs
(`_sm = ctx.imageSmoothingEnabled` ... restore) now restore to false.

## Measured — `probe_flamebox`-style A/B, not by eye

`_BUILD_SOURCE/probe_sharp.py` renders the same frame with smoothing forced ON and OFF and counts
distinct colours in a backdrop crop. Nearest-neighbour **copies** source pixels, so the palette is
unchanged; bilinear **invents** values between them, so the count multiplies. Stage 1:

| | colours in one crop | uniform 2px pairs |
|---|---|---|
| bilinear | 21,423 | — |
| nearest | **13,927** | **192/192 (100%)** |

~7,500 invented colours removed from a single crop. The 192/192 is the stronger claim: under a clean
integer 2x, every pair of backing columns must be *identical*, and all 192 sampled pairs are. That is
a property, not an impression — a non-integer or filtered scale cannot produce it.

Boot state now reads `imageSmoothingEnabled: False` and CSS `image-rendering: pixelated`.

> ⚠ **The first run of this probe reported the fix as not working, and it was right.** Setting the
> flag at init showed `True` at boot, because line 37729 overwrote it on the very first frame. Had I
> only changed the init line and trusted it, the blur would have shipped unchanged. Measuring the
> flag at runtime rather than assuming the edit took is what caught it.

> ⚠ **Stages 5 and 8 are NOT measured.** Their crops came back with 2 colours — an unrendered
> backdrop at that scroll, i.e. blank canvas. The probe originally called that "no blur here", which
> is the same error class as the reaver probe measuring the lava background. It now says
> "not measured" instead of claiming a result.

## NOT done — Mike's list from this message

Nine items untouched, listed so none of them quietly disappears:

1. Stage 5 runs a **sky** background when it should be space throughout. The `STAGES` table already
   says `bg:'space'` for stage 5 — so it is coming from the kit/master, not this config.
2. The **signs scroll**.
3. The **upscaled bridge** added to the highway scene — remove.
4. **Tanks go sideways** and should not.
5. **Bosses and minibosses not replaced** on the other levels, as previously asked.
6. **Purple halos still on level 7.** Standing rule: converted to a black edge, never deleted.
7. **Wrong region highlighted** on the campaign map when selecting level 5 (`CMAP_REGIONS.stage05`
   poly, game.js:32813, is the place to check).
8. **Square boxes around background objects** on the space and sky levels.
9. **Old chain-lightning graphic** appearing in the scrolling terrain, stage 8 especially.

### ⚠ The stage-6 overlay was NOT deleted, deliberately

Mike: *"I told you not to use that door or side sky area overlay for stage 6, delete it now."*

The obvious candidate was `nl6sky_stage06_sky_scroll_640x960` (game.js:733, 17416, 33126). **Rendered
it first per rule 1 — it is a flat blue noise field**, a plain sky texture, not a door or a
side-area overlay. See `docs/proofs/stage6_sky_plate.png`. Deleting it would have removed the wrong
asset and dropped stage 6 onto its procedural gradient fallback.

The door/side overlay is something else and still needs identifying. **Filenames lie — this is the
third time in this repo that rule has stopped a wrong deletion.**

## Suite

**5 failures**, the same long-standing set (preload count, the two `_superseded` ledger ones, volley
round count, flash families). The run reaches section 229's last assertion and the summary, so it
completed. Assertion count not re-measured this run — the background invocation was piped through
`tail`, so only the final lines were captured.
