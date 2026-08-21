# 0819c — THE PLUME WAS MEASURED AGAINST A SHIP THAT IS NOT DRAWN

Mike's third 0819 message, all four items:

| # | item | state |
|---|------|-------|
| 1 | panning — "thats how fireshark and raiden did it" | **RESTORED** |
| 2 | enemies appearing mid-screen instead of scrolling in | **FIXED** |
| 3 | thrusters wrong for every pilot in-game | **FIXED** |
| 4 | the new dialogue font on dialogues and cutscenes | **DONE** |

---

## 1. PANNING, AND A PREMISE THAT WAS SIMPLY WRONG

⚠ **0819b's CENTRAL CLAIM WAS FALSE.** That passover states Raiden and Fire Shark have no
horizontal camera, and the whole zoom-to-fit decision was reasoned from it. Mike, with both games
in front of him: *"we still have screen panning left and right, thats how fireshark and raiden did
it."* The pan is the genre, not a defect.

`VIEW_FIT = 0` restores the 0818 camera exactly. The zoom survives as one dial and is **PARKED** —
the open question is not whether to pan but how to make panning FEEL better, and Mike is weighing
800-wide plates against 720. That is a one-number experiment now rather than a rebuild.

**The lesson is about method, not the camera.** The zoom was built, four follow-on bugs were fixed
to support it, and a suite assertion was inverted to match it — all downstream of a premise nobody
checked.

---

## 2. THE THRUSTERS — TWO DEFECTS, BOTH SYSTEMATIC

Which is why it read as *"wrong for every pilot"* rather than wrong for one.

### a) The plume was sized against a hull that is never drawn

⚠ **THE HULL BLIT DRAWS AT A HARDCODED 60px. THE THRUSTER DERIVED ITS OWN REFERENCE** —
`(player.h||34)*2.05` = 69.7px of content, which over the per-pilot content factor gives an **86px
canvas**. So the plume was sized, spaced and anchored against a hull **43% taller than the one on
screen**: mounts (fractions of canvas WIDTH) came out too wide, and the anchor — canvas top plus
`hb`, the measured hull bottom — landed well below the real tail.

`SHIP_DRAW_H` is that number now, and both the blit and the thruster read it. `drawShipThruster`
(the cinematic) never had this bug because it derives its reference from the height it is actually
drawing — which is the whole reason Mike sees the cinematic as correct.

### b) The flame was anchored by its plate edge, not by the flame

⚠ **THE PLATES HAVE NO TRANSPARENT MARGIN** — measured, every `nthp_` cell's bbox is the whole
cell — so "no margin" was read as "the plate edge IS the flame". It is not. The luminance core sits
at **0.58 of the plate height**, the same for all nine plumes (0.575–0.590 measured).

⚠ **A SINGLE PROPORTIONAL SEAT DOES NOT FIX IT, AND I SHIPPED THAT MISTAKE BRIEFLY.** Rendered:

    seat 0.58   every plume buried inside the hull
    seat 0.34   AXEL correct, COLE's twins buried, LIZZIE displaced onto her wing
    seat 0.00   COLE correct, AXEL and LIZZIE detached

Measured in play, core-below-hull-bottom in screen px, the ratio runs **0.33 to 0.51** — not a
constant, so no single fraction can work.

**Solved in closed form instead.** Put the CORE a fixed distance behind the nozzle and the plume's
own height cancels out:

    core  = tailY - dy + th*CORE_F        (derived; identical for both draw branches)
    want  = hullBottom + SEAT
    so      tailY = hullBottom + SEAT - th*CORE_F

`SEAT` is 4 world px because that is what **Cole** measures at, and Cole is the one pilot whose
plume already read as attached — the number is taken from the case that looks right rather than
picked. `dy` still nudges each pilot on top of it, which is what Mike tuned it for.

Measured before → after (screen px, core below the hull's content bottom):

| axel | freezer | decker | falva | cole | juggernaut |
|------|---------|--------|-------|------|------------|
| 22.8 → **10.7** | 22.1 → **11.1** | 16.2 → **8.0** | 14.3 → **10.7** | 7.9 → **8.0** | 7.7 → **8.0** |

A 3× spread collapses to a tight band, and **the two that were already right did not move** —
which is the check that matters: the fix corrected the error rather than shifting everything.
Confirmed in pixels on axel / cole / lizzie.

---

## 3. THE SIDE ENTRIES WERE LIVING ON THE CAMERA'S OFFSET

⚠ Waves author side spawns at `offLeftX(28)` — 28px beyond the visible edge. That was **always**
too small to hide a jet (stage 1's are 73 and 101 wide, so half a hull is 36–50), but while the
camera sat anywhere in 0..320 the spawn was genuinely far off to the side and nobody saw it. Fit
the world, pin the camera at 0, and a jet at x=-28 puts its right 8px on screen on its FIRST frame.

0813x fixed the other half of this — it anchored the helpers to the camera so the runway stopped
collapsing toward the player, and named `ENTRY_CLEAR` "the guaranteed screen runway". What it could
not do from there is account for the unit's own WIDTH. `spawnEnemy` can, so the guarantee is now
the one that note describes. Pushed outward only, and never for an `inPlace` beat.

---

## 4. THE DIALOGUE FONT REACHES THE CUTSCENES

`drawCommWindow` — the MODAL panel cutscenes and comms speak through — is on the Fury dialogue face,
joining `dlgBox` and the pickup banner from 0819b. 0814b's note is explicit that those are the two
legitimate dialogue renderers, so between them "dialogues and cutscenes" is covered.

⚠ **THE 1x FACE, NOT THE 2x CUTSCENE BUILD.** This panel draws its name at 20px and its body at
14px; `fury-cutscene-font` is an exact 2x of the same letterforms for full-screen cards, and asking
for it at 14px downscales a 2x plate to land softer than the 1x it was doubled from.

⚠ **SET AT THE TOP, CLEARED AT THE SINGLE EXIT** (checked: the function has no early returns).
Because the face flag gates `msgMeasure` as well as `msgTextLeft`, the wrap is solved in the metric
it is drawn in — 0814b's "the text ran off its rail" cannot recur.

---

## THE STAGE FONTS WERE ALREADY LIVE — AND I REPORTED OTHERWISE TWICE

I told Mike the eight `bof_font1..8.png` stage faces were unwired. They are not. **All eight are
registered with 46 frames and a 46-entry glyph map each**, named per stage, and `curFontArt()` /
`uiFontArt()` already prefer them over every older face.

Two separate measurement errors produced that wrong claim, and both are ones this file already
warns about:

⚠ **GREPPED THE DEFINITION, NOT THE CONSUMER.** `grep bof_font assets/game.js` returns nothing,
because the wiring goes through the manifest key `bofFont` and the game reads `BOF.bofFont`. The
handoff's own highest-value habit — *grep for the consumer* — is exactly what was skipped.

⚠ **THEN A READINESS CHECK INSIDE THE SYNCHRONOUS WARM BURST.** A probe reported
`decoded=false, curIsBof=false` for every stage and looked like proof. `shoot.py`'s warm is
synchronous, so **no network can progress inside it** — the frame counter ran to 150 while zero
real time passed. Measured against real elapsed time instead:

    t=9ms     frames=1     complete=false  natW=0    curIsBof=false
    t=576ms   frames=184   complete=false  natW=0    curIsBof=false
    t=1500ms  frames=488   complete=true   natW=832  curIsBof=true

**A frame count is not a clock.** Poll readiness against `performance.now()`, never against frames.

---

## ASSERTIONS REPOINTED (four, all pinning a line rather than a rule)

- **`stage 1 camera pans right`** — un-inverted. 0819b flipped it to match the zoom; the pan is the
  shipping behaviour again, so the original claim stands.
- **`the canvas height is derived from the target hull height`** pinned the expression
  `_dh=_targetContent/_cf`, the exact line the thruster fix had to change. The RULE — canvas and
  content related by the per-pilot fraction — is intact; it now asserts the canvas comes from
  `SHIP_DRAW_H`, plus that the hull blit draws at the same number.
- **`tucked just under the bottom tip`** asserted that a **COMMENT STRING** existed in the source.
  Repointed onto the seat geometry.
- **`msgTextLeft falls back to a real measure`** sliced 900 chars of the function; the bitmap-face
  branch pushed the fallback past it. The slice was the artefact, not the fallback.

---

## HOW TO VERIFY

    node --check assets/game.js
    node _BUILD_SOURCE/test_fl.js          2,697 ok / 3 fail
    python _BUILD_SOURCE/shoot.py --state PLAY --stage 1 --pilot axel --seconds 2 --fps 2

**The 3 failures are environmental**: the preload key count and two `_superseded/` ledger checks —
that folder is not committed, so they cannot pass on a fresh clone.

⚠ **One suite failure this session was FLAKY, not real** — "a corner run travels further sideways
than a curve" failed once and cleared on re-run with no change to that code. Re-run before chasing
it.

---

## STILL OPEN

- **the 720-wide plate experiment** — Mike's, pinned. `VIEW_FIT` is the dial.
- `laser` fire mode is still fielded only by stage 3.
- Stage 2's `el_lr` reavers keep their guns, deliberately — Mike: they are great as they are.
- **Lizzie has a residual LATERAL offset** — her flame sits slightly left of her spine. No vertical
  seat explains it; it points at the per-frame rig's tail centroid for her set.
