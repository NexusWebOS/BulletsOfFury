# Handoff — current state, and the transition rebuild

**Read `CLAUDE.md` first, then this.** `PASSOVER_0809t.md` is the facing/campaign-pause drop and
stops short of the last three changes — do not use it as the state doc.

---

## Where the build actually is

Suite: **2,395 assertions / 215 sections / 5 failures**, all five pre-existing at HEAD (boss limb
pool, preload count, two `_superseded`, naval flash families). Verified by stashing and re-running.
⚠ Section 202 is **flaky** — re-run before blaming a change for it.

Landed after `PASSOVER_0809t`, so it is in no passover doc:

- **Full-size pause menu**, palette-swapped black, red/white/blue save slots. New
  `xartPalette(key, mode)` — use it, never `xartTint` (that one is the `source-atop` flood that
  caused the E→B bug). `black` must be a *multiply*; `'color'` cannot darken.
- **Stage clear** — control is released the instant the boss dies, and the fly-off overlaps the
  death instead of queuing behind it. `drawFlyover` itself was always correct.
- **Two dams.** `ndam_*` exists but does NOT overlay the dam painted into the plate (match test:
  37.26, noise). Full note in CLAUDE.md. Don't re-run that test.

---

## The transition rebuild — Mike's spec, verbatim intent

> "Before anything though. stage intros and transitions. Thats a broken system that needs fixing
> badly."

1. **Stage 2's intro is the model.** Stage 1 should work that way but with the runway, its music,
   and flying over water.
2. **Connect the last transition tile to the level's first frame** — "so we truly fly into level 1,
   same with level 2 etc. No more fake transitions."
3. **Always start centered**, and keep play mainly to the centre of the screen.
4. **Kill the jerk after 3-2-1** that knocks the ship back and clips it in and out.
5. **Stage clear**: non-playable, fly off, fade. *(control release + overlap already done)*
6. **No runways from 2→3 onward.** Themed joins instead:

   | join | transition |
   |---|---|
   | 2→3 | lava into ice |
   | 3→4 | ice into urban warfare |
   | 4→5 | the airbase into space |
   | 5→6 | space back down to the sky |
   | 6→7 | sky to the sewer |
   | 7→8 | sewer to a portal into Furious Death |

---

## What the code actually looks like — measured, not assumed

**The opening** (`GS.OPENING`, `openingStart` ~line 28317):

```
OPEN_PH = {RUNWAY:0, TAKEOFF:1, SKY:2, COAST:3, HANDOFF:4}
OPEN_T  = [2.2, 4.2, 8.0, 11.4, 14.6]     // cumulative phase ends
```

- sets `player.x = worldWidth()/2` (not `VW/2` — stages 1/5/6 are 800-wide worlds) and snaps
  `camX` so it doesn't lerp in from the left.
- the coastline is **generated, not painted**: `openingCoastY()`, two sine terms, drawn from the
  64×64 `tflat_water` / `tflat_sand` flats.
- the handoff **deliberately does not touch the player** — not x, not y, not velocity — then
  `setState(GS.PLAY)` and starts the stage music.

**The outbound** (`GS.OUTBOUND`, `outboundStart` ~line 97):

- `via: (fromStage===1 || DBG.transitions) ? transVia(fromStage) : []`
  → **only 1→2 is built.** The other six sit behind the debug flag and were never made. This is
  six new builds, not six repairs.
- `o.con` is **forced null** — Mike rejected the connector plates outright. Terrain must come from
  `TRANS[]` flats, not from a plate belonging to neither stage.
- 1→2 water route beats: `W12_PAST 2.2 · W12_WATER 1.6 · W12_CRUISE 1.5 · W12_FADE 1.0`, and it
  never climbs — the player holds position and the world changes underneath.

**Watchdogs:** `OPEN_MAX = 22`, `OUT_MAX = 14` seconds. `cinematicEscape()` bails on
backspace/escape.

---

## The jerk — leading hypothesis, and how to test it

The handoff provably does not move the player, so the jerk is almost certainly **visual, not
positional**: the opening draws its own ship using `O.shipScale` and `O.panY` over a *generated*
coast, and `GS.PLAY` then draws `drawPlayer()` over the *stage master* starting from its own
`mapScroll`. If the opening's terrain doesn't hand its scroll offset to the stage, the world
jumps even though the player didn't.

That is the same root cause as requirement 2 — "no more fake transitions" *is* "make the
opening's last frame the level's first frame."

**Test it before changing anything:** capture across `t = 14.6s` with
`shoot.py --state PLAY --stage 1 --seconds 3 --fps 12` and diff consecutive frames for a
discontinuity in terrain offset vs player offset. Do not fix by nudging positions until you know
which of the two moved.

⚠ `--warm N` is one synchronous burst that never yields, so lazily-loaded art never arrives.
Use `--seconds/--fps` for anything needing art loaded on entry.

---

## Order of work

1. **Connect opening → level.** Fixes requirement 2 and very likely 4 at the same time, and every
   themed join afterwards inherits the mechanism. Do this first.
2. **Start-centered / keep-play-centered** — verify `worldWidth()/2` survives into PLAY.
3. **The six themed joins**, built on the mechanism from (1), using `TRANS[]` flats. No connector
   plates, no runways.

⚠ **The boss is being wired in another chat, in this same working tree.** Check `git log` before
assuming a change is yours, and coordinate before touching boss code.

---

## Appendix — the bridge rescale, four attempts deep

`jungle800_rc2_master.png` is **untouched**; all work went to scratchpad. Mike: "Scale it as best
as possible."

**Settled:** band is **y 2290–2880**, full width. **0.65 is the right scale** — confirmed visually,
the structure stops dominating and reads as part of the jungle.

**The approach that works** is: mask the stone, heal the band with jungle, scale *only* the masked
structure, composite it back. Do **not** scale a rectangular crop — attempt 2 proved the jungle
inside the crop ends up at 65% while the jungle around it is native scale, and the rectangle's edge
is plainly visible however much you feather it.

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
close) and use **hard alpha** in the interior — feather only the outer boundary, not the whole
mask.

Then cover Mike's seam at **y 2760–2875** *after* the rescale, since scaling moves where the span
lands.
