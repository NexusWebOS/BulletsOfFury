# PASSOVER 0813C — stage 5 is space, and the signs were scrolling backwards

Working Mike's list in his stated order, 1–9. Items 1 and 2 are done; item 3 is blocked on
identifying an asset and is written up below rather than guessed at.

---

## 1. "your using a skybackground level 5 when its space the whole time"

**The name was the trap, and one render nearly confirmed the wrong answer.** Stage 5's master was
`storm800_rc2_master`. Sampled at 45% of its height it shows Earth's horizon and a nebula — space,
apparently fine. Walked end to end it is **storm cloud, rain and lightning for essentially all
5120px**, with that orbital band the single exception. Mean luminance at three points: 75.6 / 70.1 /
80.9. That one band is the only reason it ever passed as space.

Stage 5 now loops its own authored orbital plate, **`norb5_arena`** (`norb5` = orbital, stage 5),
which was previously used only for the boss arena. Measured before switching:

- **dark** — edge luminance 11 (top) / 7 (bottom)
- **tiles** — first row against last row differs by 12.5/765, so looping shows no join

### `loopMaster`

`norb5_arena` is 1000px, and the windowing path maps the whole level across `rangeSrc = H - winH`,
which for a short plate would crawl through 488px and read as nearly static. A new `loopMaster` flag
routes it through `_loopDraw` instead — the right mapping for a starfield.

Verified across the whole scroll (`probe_stage5space.py`), stage 8 as a control:

| scroll | 0 | 400 | 900 | 1500 | 2200 | 3000 | 3900 | 4800 |
|---|---|---|---|---|---|---|---|---|
| stage 5 luminance | 6.6 | 6.6 | 9.3 | 9.9 | 10.2 | 12.5 | 10.5 | 10.7 |

All well under the sky threshold; stage 8 also reads space, so the metric is not simply calling
everything dark.

## 2. "the signs are scrolling"

**They were, and in the wrong direction.** The terrain shows master rows `[srcY, srcY+VH]` where

```
srcY = rangeSrc - (mapScroll/range)*rangeSrc
```

`srcY` **decreases** as the level runs, so a feature at master row R sits at screen `R - srcY` and
travels **down**. `drawRoadSigns` used `sn.y - mapScroll`, which travels **up**.

Measured on stage 4 between mapScroll 900 and 1020 — a crater at x≈185 moved **down 105px** while
the RESTRICTED AREA sign moved **up 105px**. The signs slide across the ground at twice the scroll
rate, in the opposite direction.

> ⚠ The 0810h note at game.js:2936 claimed they "already stay put ... that part was never wrong",
> because signs and props both use `y - mapScroll`. That compared the two props to **each other** and
> never to the terrain. Both were consistently wrong together.

`drawLevelMaster` now publishes `_masterSrcY` (both the windowed and the looping path) and
`drawRoadSigns` + `drawStageProps` read it, so a prop and the ground it stands on share **one**
mapping. After: chevrons down ~115px, COMMAND sign down ~110px — together.

### ⚠ Three failed measurements before this one, all the probe's fault

Each reported "nothing here" about a real bug:

1. **Signs undecoded.** `XART.rdy()` STARTS the decode and returns false on that first call, so a
   single synchronous render drew no sign at all.
2. **Master undecoded.** The first `drawWorld` started the master's decode, so frame one came back
   blank and the two frames were not comparable.
3. **A false green.** The summary printed *"signs ride with the terrain"* having measured **zero**
   stages. Same class as a suite that never ran. It now prints "NOTHING WAS MEASURED" instead.

## 3. "no additions to the highway scene liek that ugly upscaled bridge" — NOT DONE

Found the highway scene: **`nst4_crash_overlay`**, an 800x600 multi-vehicle pileup (trucks, buses,
ambulance, police car) drawn **1:1** at x=0, y=3100 on stage 4. See `docs/proofs/stage4_prop.png`.
That is the "car crash object" Mike approved in 0810h, and it is not upscaled.

**There is no bridge.** Searched the manifest for bridge/overpass/viaduct/span/highway/road/ramp/deck
— nothing (DECKER is a pilot, Rampart is a boss). `cfg.props` defines exactly **one** prop in the
entire game, the pileup above. So either the bridge is baked into a master plate (in which case it
cannot be deleted in code) or it is something not yet located.

**Worth re-checking before hunting further:** 0813b fixed a global bilinear filter that was
doubling every 800-wide master under `imageSmoothingQuality='high'`. Anything baked into a master —
a bridge included — looked soft and upscaled before that fix and should look crisp now. "Ugly
upscaled" may already be resolved.

Not guessing at a deletion here. That is the same call as the stage-6 overlay in 0813b, where the
obvious key turned out to be a flat blue noise field.

## Still open — items 4-9

4. Tanks go sideways and should not.
5. Bosses and minibosses not replaced on the other levels.
6. Purple halos still on level 7 (rule: converted to a black edge, never deleted).
7. Wrong region highlighted for level 5 — `CMAP_REGIONS.stage05`, game.js:32813.
8. Square boxes around background objects on space/sky. **Clean repro now exists** —
   `docs/proofs/stage5_scrollwalk.png` shows every satellite and debris chunk inside a rectangle.
9. Old chain-lightning graphic in the scrolling terrain, stage 8 especially.

## Suite

**2,636 assertions / 234 sections / 5 failures** — the same long-standing five (preload count, the
two `_superseded` ledger ones, volley round count, flash families). Full output captured this run,
so the counts are measured rather than inferred.

## Probes

`probe_stage5space.py` (walks the scroll, control stage), `probe_signdrift.py` (terrain vs sign
displacement off the canvas).
