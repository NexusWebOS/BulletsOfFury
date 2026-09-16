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

## 5. The rows, over four passes

> "you can list 4 at once, but use square boxes plus rectangle text next to them."
> "should be 4 large boxes for th weapon icons, 4 rectangle boxes next to the large boxes. re-do"
> *(with a crop of the plate's rank box and word strip)* "I meant 4 of these like this. and stretch
> to fill icons inside the box"
> "Now make it to where you can scroll, show just 1, just 2, just 3, etc. make it a flexible
> scrollable section. this si perfect otherwise. and center all texts, make them fit about the
> stage 2 clear message."

### What it is now

**The row is the plate's OWN box and strip, blitted.** The RANK bay
(`0.5220,0.6466,0.1111,0.1579`) and its word strip (`0.6667,0.6880,0.2453,0.0677`) are cut straight
out of `statpanel_full_0916` and repeated, so the corners, the bronze rail, the bezel and the
shading are the art's. `UNLOCK_ART` names those fractions and the suite asserts they are the same
rects `SC_SLOTS_FULL` carries, so the rows and the debrief cannot disagree about where the art is.

**The section is flexible and scrolls.** Two numbers, meaning different things:

| | |
|---|---|
| `UNLOCK_VIEW = 4` | rows visible at once — the section scrolls past this |
| `UNLOCK_MAX = 8` | the most a single stage may announce at all |

One unlock is **one row**, two is two, and the block is **centred in the region**. ⚠ The pitch is
fixed rather than sized to the count: sizing rows to the list would draw a single unlock at four
times the size of one in a list of four — the same art at two scales on two runs of the same stage.
Past four rows, UP/DOWN scroll and two drawn triangles say there is more. ⚠ They are **drawn, not
lettered**: CLAUDE.md records that `25B2`/`25BC` are absent from this face and a missing glyph draws
a **space**, so an arrow written as text is an invisible affordance.

⚠ **UP and DOWN are each read exactly once, into locals, before either is acted on** — `menuUp`/
`menuDown` CONSUME their tap, the trap this file records as `menuLeft()||menuRight()` always
resolving to +1.

**Every text is centred**, and the name is centred on the **whole** string: centring the typed
prefix would walk the word sideways as it types, so the block is placed from the full string's
width and the letters fill it left to right.

**The stage-clear message fits its bay.** It wrapped to three rows and the third sat below the bay,
so `CRATES.` was clipped on every stage that has a page. ⚠ `stageFitH` only solves the **width** of
one line; `stageWrapCount` gives the row count at a size without drawing, which is the half that was
missing — the same pairing 0811q needed for the cutscene box. The size is stepped down until the
block fits, then centred in the bay. It now sets in two lines.

**The icon fills its box.** ⚠ `iconBlit` takes a HEIGHT and derives width from the art's aspect, and
three art stores make that unknowable at the call site — so the width is measured: one draw at
alpha 0 off-screen returns what the icon would take, and the real draw runs under a horizontal
scale. The strip is 3-sliced (6.5:1 source into a ~8:1 row would pull its caps into ovals); the box
keeps its authored 1.24 aspect rather than being forced square.

### What each rejected cut got wrong — all four found by RENDERING, none moved a number

1. **Borrowed the debrief's stat bays.** A bay is 0.0526 of the plate, so a square at its height is
   a text row tall and the "box" read as an icon with a border.
2. **Drew its own flat panels.** They read as holes punched in the art beside the authored bays.
3. **Dimmed the empty sockets** — twice, at 0.55 and 0.62. The plate's bays are BAKED underneath, so
   a part-alpha socket shows two columns of old rails through itself.
4. **Drew four sockets always.** Replaced: one unlock is one row.

### Three probe faults, also worth keeping

- **It awaited `requestAnimationFrame` on a page that TRAPS rAF** (`shoot.TRAP_RAF` parks the
  callback), so the evaluate hung for ever. Record during a manual `loop()` step.
- **It chunked the page-background plate blit as a panel.** The background is drawn from the same
  image as every panel cut out of it, so every row came out one slot off and it reported a constant
  **222px "off centre"** on text that is dead centre.
- **It counted "gold pixels below the bay" with no control** and reported 948 on a frame where the
  message plainly fits — that band contains the plate's own warm metal. It now measures the same
  band at t≈0, before the brief fades in, and compares.

And one **assertion was repointed rather than worked around**: it required `i<UNLOCK_MAX` — four
sockets drawn whether or not they held a weapon — which is exactly the behaviour Mike replaced.

Measured: `probe_unlocks_0916.py` **51 ok / 0 fail** in real Chromium, 0 page or console errors,
covering 1, 2, 3 and 4 rows, a 6-row list scrolling and clamping, the name's ink centre in every
strip, and the brief against its control. Proofs: `03_four_rows.png`, `04_one_row.png`,
`05_scrolled.png`, `02_stage9_lasermist.png`.
