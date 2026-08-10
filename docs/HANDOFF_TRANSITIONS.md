# Handoff — the transition rebuild

**Read `CLAUDE.md` first, then this.** `PASSOVER_0809t.md` is the facing/campaign-pause drop and
stops short of everything since — do not use it as the state doc.

Suite at HEAD: **2,395 assertions / 215 sections / 5 failures**, all five pre-existing (boss limb
pool, preload count, two `_superseded`, naval flash families). ⚠ Section 202 is **flaky** — re-run
before blaming a change for it.

---

## ⚠ Correction to the previous version of this doc

The last version said the jerk was probably a **terrain scroll offset** handed over wrong by the
level-1 opening, and told you to diff frames across `t=14.6s`. **That was wrong, and following it
would have cost you a day.** Measured, in the real browser:

- the level-1 **opening's** handoff is already clean — ship, camera and `mapScroll` are all
  continuous across it. Nothing about it jerks.
- the jerk is in a **completely different system**: the `GS.LAUNCH` sequence that stages 2–9 use.
- and it was never the terrain. It was the **ship and the camera**.

This is rule 1 from CLAUDE.md wearing another hat: the previous hypothesis was reasoned from
reading the code, not from measuring the running game.

---

## There are TWO intro systems. This is the thing to know.

| | stage 1 | stages 2–9 |
|---|---|---|
| state | `GS.OPENING` → `drawOpening` | `GS.INTRO` → `GS.LAUNCH` |
| what it is | the runway cinematic: RUNWAY/TAKEOFF/SKY/COAST/HANDOFF | stage card drops in, then `drawLaunch`: run → brake → settle → cd |
| gate | `DBG.opening && num===1 && XART.rdy('nst4b_exit')` | none, it is the default |
| status | smooth handoff, **wrong picture** | **was jerking**, now fixed |

`beginStage` line ~10824 is where it forks. Note the gate's third term: `XART.rdy` **returns false
on its first call** (that call starts the lazy load), so a cold boot can silently take the LAUNCH
path on stage 1 instead of the runway.

**"Stage 2's intro is the model" means `drawLaunch`.** That is what Mike is pointing at.

---

## Done in this drop

**The jerk, killed.** `probe_seam.py` on stage 2, at the frame GO hands over:

```
intro drew    x= 240.00  y= 307.20  h= 62.00      (phase cd)
play draws    x= 400.00  y= 399.36  h= 76.10
DELTA         x=+160.00  y= +92.16  h=+14.10      <-- THE JERK
camX          0.00 -> 159.04 over the next 41 frames
```

Three quantities and a camera, none of which anything forced to agree:

- **x** — the launch drew at `VW/2`; PLAY draws at `player.x - camX`, and `beginStage` left `camX`
  at 0. So the ship appeared 160px right of where it had been and the camera eased back over
  two-thirds of a second. That is "knocks the ship back".
- **y** — the launch held `VH*ANCHORY` (0.60); `player.reset()` starts play at `VH*0.78`.
- **h** — the launch passed a **canvas** height to `drawShipSprite`; PLAY scales to a **content**
  height and divides by the pilot's content fraction, so 62 landed as 76.1. That is "clips it in
  and out".

Fixed with one shared pose rather than three coincidences:

- `playShipPose()` — the single pose both sides read.
- `drawLaunch`'s **settle** phase eases onto it over the 0.45s it already had. Its comment already
  claimed the ship "holds the exact spot it will start play from"; that was true of the intent and
  false of the numbers.
- `snapCamToPlayer()` — called from `beginStage` after `player.reset()`, and reused by
  `openingStart`, which had been the only place that knew to do this.
- `_drawLevelRegion` now draws through the same `translate(-camX)` `drawWorld` uses. Without it
  the terrain slid 160px the *other* way at the same instant.

All three deltas are now **0** and the camera does not slide. Requirements 3 and 4 are done for
stages 2–9.

**The two camX assertions** pinned `camX===0` — a value PLAY abandons within 41 frames. Exactly
the "assertion defends a bug" shape. They now test the intent they were written for (stage 1's
camera must not leak into stage 2) instead of the old literal, which would have passed for a leak
that happened to be zero.

---

## Still open, in order

**1. Requirement 2 for stage 1 — "no more fake transitions".**
The opening's COAST phase draws a **generated** coastline (`openingCoastY`, two sine terms, tiled
from the 64×64 `tflat_water`/`tflat_sand` flats). PLAY then draws the **jungle master**. `mapScroll`
is 0 on both sides — measured, it does not move — so nothing *jumps*, but the entire picture is
replaced. That is the fake transition.

The mechanism to build: during COAST, draw the **real stage master** descending into view from the
top over water, converging so the final cinematic frame is the frame PLAY starts on. Concretely,
PLAY at `mapScroll=0` draws source rows `[H-VH, H]` to screen `[0, VH]`. Draw that same window at
`dest y = -dy` with water below it and drive `dy: VH → 0`. At `dy=0` the frame is byte-identical to
PLAY's first frame, because it is the same draw. Reuse `drawBG`/`drawLevelMaster` under a translate
rather than reimplementing — that makes the identity structural instead of something to re-verify.

**2. The six themed joins, 2→3 … 7→8.** Only 1→2 is built; the rest sit behind `DBG.transitions`
and were never made. Six new builds, not six repairs. `o.con` is forced null — Mike rejected the
connector plates, so terrain comes from `TRANS[]` flats. No runways from 2→3 onward.

| join | transition |
|---|---|
| 2→3 | lava into ice |
| 3→4 | ice into urban warfare |
| 4→5 | the airbase into space |
| 5→6 | space back down to the sky |
| 6→7 | sky to the sewer |
| 7→8 | sewer to a portal into Furious Death |

---

## Tools, and two traps that will cost you a run each

**`_BUILD_SOURCE/probe_seam.py`** — drives the real entry path in real Chromium and prints the
ship/camera/terrain deltas across the seam. This is what turned a wrong hypothesis into three
numbers.

```bash
python3 _BUILD_SOURCE/probe_seam.py --stage 2
```

⚠ **It runs the whole sequence inside ONE `evaluate`.** That is deliberate — the game takes `dt`
from `performance.now()`, so stepping one frame per `evaluate` gives every frame a `dt` of about
1.6 *seconds* and a 14.6s cinematic "completes" in nine frames. But it means it hits the `--warm`
trap: **lazily-loaded art never arrives**, so `mapScroll` reads 0 and the master is never decoded.
**Trust it for the ship and the camera, which are art-independent. Do not trust it for terrain.**

⚠ **`shoot.py` captures inflate `dt` between shots.** Each screenshot is a separate `evaluate`, so
the next frame sees the real wall-clock gap (100–300ms) as its `dt`. A 6.3s launch therefore
finishes in far fewer captures than `--seconds`/`--fps` implies — my first seam capture put the
countdown before frame 0 and every shot landed in PLAY. Aim early and check where the countdown
actually is before concluding the sequence did not run.

`_BUILD_SOURCE/scenario_seam.js` drops shoot.py into `GS.LAUNCH` at the brake, since `--state PLAY`
calls `beginStage` and then `setState(GS.PLAY)` — which skips the launch entirely, so the one
sequence Mike is complaining about is the one the capture tool cannot normally see.

⚠ **The boss is being wired in another chat, in this same working tree.** Check `git log` before
assuming a change is yours, and coordinate before touching boss code.

---

## Appendix — the bridge rescale, four attempts deep

`jungle800_rc2_master.png` is **untouched**; all work went to scratchpad. Mike: "Scale it as best
as possible."

**Settled:** band is **y 2290–2880**, full width. **0.65 is the right scale** — confirmed visually.
**The approach that works** is: mask the stone, heal the band with jungle, scale *only* the masked
structure, composite it back. Do **not** scale a rectangular crop — attempt 2 proved the jungle
inside the crop ends up at 65% while the jungle around it is native scale, and the rectangle's edge
is visible however much you feather it.

**Calibrated stone gate** (measured, don't re-derive):

```
sat < 32  and  50 < lum < 210        -> 29.4% of the band   ✅ correct shape
```

Traps already hit, each cost an attempt:

1. Adding a dark clause (`sat<46 and lum<=45`) to catch tower interiors floods the mask — the
   canopy is full of low-saturation shadow. It went ~100% white. Don't.
2. `MaxFilter(9)` then dilates that flood over everything. Keep morphology gentle (5/5).
3. Tiling the fill with an alternating vertical flip makes the two halves near-mirrors and
   duplicates a river. Sample each patch at the **same x**, never flipped.

**What is still wrong, and it is the only thing left:** the mask has interior speckle holes and I
Gaussian-blurred it, so the structure composites *semi-transparent* and reads as a ghost with
jungle showing through. Fix: fill holes properly (flood-fill the mask's interior, or a much larger
close) and use **hard alpha** in the interior — feather only the outer boundary.

Then cover Mike's seam at **y 2760–2875** *after* the rescale, since scaling moves where the span
lands. WIP script: `_BUILD_SOURCE/bridge_rescale_wip.py`.
