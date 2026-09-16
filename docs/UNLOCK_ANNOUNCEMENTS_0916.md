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

## 5. The layout (Mike, later the same day)

> "we dont need to have multiple listed weapon unlocks like that, at most we might unlock 3 at once
> like Freezer. you can list 4 at once, but use square boxes plus rectangle text next to them. the
> icons go in the boxes, text for the attack next to the box. I love this design."

`UNLOCK_MAX = 4` is the cap AND the layout, one number: `unlockRowsFor` slices to it and the page
lays out that many rows. The rows use the **left column only** (`stats` slots 0, 2, 4, 6) - the
right column stays empty, because a name that wrapped into it would read as a fifth unlock.

Each row is a **square box with the name beside it**, which is the shape of the RANK bay and its
word strip - the place he asked for it first. The box is drawn in the PLATE'S OWN socket colours
rather than invented ones: measured off `stat_panel_full.png` at both a stat bay and the rank bay,
a bronze rail at **rgb(112,88,72)** around a **rgb(22,22,32)** well, identical on the two. The icon
sits in the box at 74% of its height; the name starts one gap past its right edge and is fitted to
what is left.

Proof: `docs/proofs/unlocks_0916/03_four_rows.png` - the four-row case, which is the one that had to
be looked at, driven through the page's own entry point with real icon keys.
