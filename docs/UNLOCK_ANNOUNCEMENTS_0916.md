# 0916 — the unlock page announces where the engine GRANTS

Mike, answering the open question `docs/RESUME_0916.md` left at the top of its list:

> "announcement should be after stage 4 victory yes. The same should apply if you unlock the laser
> mist on stage 9 if you beat the level."

## 1. What was wrong

`SC_UNLOCKS` had been written from Mike's stage-2 brief verbatim, which named the LIGHTNING ORB
among Yuri's stage-2 rewards. The engine does not grant it there. Both grants live in `bossDie`:

```
if(run.stage===9 && typeof laserMistUnlock==='function') laserMistUnlock();
if(run.stage===5 && boss && boss._hammer && typeof chaingunUnlock==='function') chaingunUnlock();
if(run.stage===4 && typeof yuriLightningOrbGrantStage4==='function') yuriLightningOrbGrantStage4();
```

So the page promised Yuri a weapon two stages before he receives one, and the weapon that IS
granted on the last stage — LASER MIST — was announced by nothing but a one-line arcade banner
fired during the boss's death cook-off, where nobody reads it.

**The rule now is: the page announces where the engine grants.** Suite section 361 reads both
sides — `bossDie.toString()` for the grant, `unlockRowsFor` for the announcement — so the two
cannot drift apart again without a red.

## 2. The change

| stage | who | announced | granted by |
|---|---|---|---|
| 2 | all | FIRE ORB | the stage's own crate pool |
| 2 | freezer | ICE BREATH, THERMOSHOCK BALL | unchanged |
| 2 | yuri | FIRE ORB **(the lightning orb was removed)** | — |
| 4 | yuri | LIGHTNING ORB | `yuriLightningOrbGrantStage4` |
| 5 | all | CHAINGUN | `chaingunUnlock` |
| **9** | all | **LASER MIST** *(new)* | `laserMistUnlock` |

Stage 3 still has no row, so no page appears after it — Mike has not said what it should announce.

⚠ **STAGE 9 IS THE BONUS STAGE, NOT THE CAMPAIGN END.** `CAMPAIGN_STAGES` counts the entries
without `bonus:true`, so the campaign finishes at stage 8 and stage 9 (THE VELOCITY VOID, reached
through the stage-5 gate) exits through `scLeaveStage`'s own `curStage.bonus` branch back to the
map. The unlock page sits in front of that exit exactly like every other — measured: its CONTINUE
lands on `stagesel`.

⚠ **THE LASER MIST ICON IS NOT ON THE ICON SHEET, AND AN UNWARMED PAGE FAILS SILENTLY.** `iconBlit`
routes `micon_lasermist_*` to `laserMistAtlasBlit`, which reads `bof_laser_mist_weapon_atlas` —
and `XART.rdy` is false on its FIRST call, which is the call that starts the load. `unlocksStart`
touches each row's icon key to start its decode; for this family that touch starts nothing at all,
so the row would have drawn its name beside a hole with no error anywhere. `unlocksStart` calls
`laserMistWarm()` when a row needs it. **Any future row whose art lives off `nia_icons` needs the
same**, and the probe's busted arm is exactly this: with the warm suppressed the icon never blits.

## 3. Measured

`_BUILD_SOURCE/probe_unlocks_0916.py` — **25 ok / 0 fail**, real Chromium, 0 page or console
errors. It drives the REAL debrief (`GS.STAGECLEAR` for the cleared stage) and presses its
CONTINUE with a real key tap, so the page is reached the way a player reaches it, and it
identifies the icon by the KEY `iconBlit` was asked for **and** by the dimensions of the sheet the
blit came from — `XART.get` returns a fresh canvas, so identity and `.src` catch nothing.

- stage 9 → the debrief → NEW WEAPONS UNLOCKED carrying `LASER MIST`;
- `micon_lasermist_3` asked for on 18 of 18 recorded frames, and **18 of 18 blitted from the laser
  mist atlas**, not from `nia_icons`;
- busted arm (warm suppressed): **0** blits;
- CONTINUE leaves through `scLeaveStage` to the map;
- stage 4 as Yuri → `LIGHTNING ORB`, its icon blitting; stage 4 as anyone else → no page;
- stage 2 as Yuri → `FIRE ORB` alone.

Proof frames: `docs/proofs/unlocks_0916/01_stage4_lightningorb.png`,
`docs/proofs/unlocks_0916/02_stage9_lasermist.png`.

Suite: **4,568 ok / 57 fail**, final summary reached, exit 1 — the established 56 names plus the
intermittent stage-1 sand-tank fixture, compared NAME by NAME against a clean `git worktree` at
`97265703`. Section 361 is 16/16.

## 4. Seen while proving it, NOT changed

The briefing line — `STAGE n CLEARED. YOUR ARSENAL GROWS - THE FOLLOWING WILL NOW DROP FROM SUPPLY
CRATES.` — wraps to three rows and its **third row sits below the brief bay**, so `CRATES.` is
clipped by the panel edge. It is the same on every stage that has a page (2, 4, 5 and now 9), it
predates this drop, and it is the debrief plate's own layout, so it is Mike's call: either the
sentence gets shorter or `stageWrapCen` gets the row count `stageWrapCount` can already give it.

## 5. The layout (Mike, three passes)

> "you can list 4 at once, but use square boxes plus rectangle text next to them."

then, on the first cut:

> "should be 4 large boxes for th weapon icons, 4 rectangle boxes next to the large boxes. re-do"

then, with a crop of the plate's own rank box and word strip:

> "I meant 4 of these like this. and stretch to fill icons inside the box"

**The row is the plate's OWN box and strip, blitted four times.** Not drawn, not approximated: the
RANK bay (`0.5220,0.6466,0.1111,0.1579`) and its word strip (`0.6667,0.6880,0.2453,0.0677`) are cut
straight out of `statpanel_full_0916` and repeated down the page, so the rounded corners, the bronze
rail, the grey bezel and the panel's own shading are the art's and cannot drift from it. Same idea
as 0912e building the boss tab out of the bar's own bands. `UNLOCK_ART` names those two fractions
beside `SC_SLOTS_FULL`'s, so the row layout and the debrief cannot disagree about where the art is.

⚠ **THE STRIP IS 3-SLICED AND THE BOX IS NOT.** The strip's source is 6.5:1 and a row's rectangle is
nearer 8:1, so a straight stretch pulls its rounded end caps into ovals — the caps are blitted at
their own scale and only the middle stretches. The box is drawn at its **source aspect (1.24)**
rather than forced square: distorting a bevel is what this repo's art rules exist to prevent, and a
box at the row's full height is large either way.

⚠ **THE ICON IS STRETCHED TO FILL THE BOX, AND `iconBlit` CANNOT DO THAT ON ITS OWN.** It takes a
HEIGHT and derives the width from the art's aspect, and with three art stores behind it that aspect
is not knowable from the call site. It is **measured**: one draw at alpha 0 off-screen returns the
width the icon *would* take at this height, and the real draw runs under a horizontal scale that
turns that into the box's width.

⚠ **EVERY SOCKET IS OPAQUE, FILLED OR NOT — and this took two goes.** The plate's thin stat bays are
BAKED underneath these rows. At 0.55 alpha, and again at 0.62, an unused socket showed two columns
of old rails straight through itself: worse than either layout alone. An empty slot is the same
panel with nothing in it. The gaps between rows are small for the same reason.

### What each pass got wrong, since all three were found by rendering

1. **Borrowed the debrief's stat bays.** A stat bay is 0.0526 of the plate — a thin strip — so a
   square at its height is the height of a text row, and the "box" read as an icon with a border.
2. **Drew its own panels.** Flat fill and a stroked rail: it read as a hole punched in the art next
   to the authored bays it sat between.
3. **Dimmed the empty sockets.** Twice, at two different alphas, with the baked bays showing through
   both times.

The rows cover the score bay, so **LOOK FOR THEM IN THE FIELD moved to the sign-off strip and the
CONTINUE prompt to the footer** — 0814b's lesson that two strings at one y read as garbage rather
than as two lines.

Proofs: `docs/proofs/unlocks_0916/03_four_rows.png` (four rows) and `02_stage9_lasermist.png` (one
weapon in four sockets).
