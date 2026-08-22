# 0821i — THE SMALL BATCH, AND A THREE-PILOT BUG HIDING BEHIND A ONE-PILOT REPORT

| item | state |
|---|---|
| pickups scaled up | **DONE** — one dial, nine draw sites |
| cinematics too zoomed in | **DONE** — one dial, was written out five times |
| Lizzie's lateral thruster offset | **DONE — and it was FREEZER and MAVERICK too** |
| signs / waterfall | **CLOSED BY MIKE** — "the signs and waterfall are gone" |

---

## PICKUPS — FIVE DRAWERS, FIVE HARDCODED SIZES

`50 / 46 / 40 / 34 / 30` across `drawMcrate`, `drawScrate`, `drawCrate` (two branches) and the
four `drawPowerups` icon paths. Scaling them by hand would have been nine edits that drift apart
the moment one is retuned.

`PICKUP_SCALE = 1.22` multiplies all nine, so the pickups keep their proportions **to each other**
by construction and there is one number to change.

## CINEMATIC ZOOM — THE PEAK WAS WRITTEN OUT FIVE TIMES

The map unlock cinematic peaked at **2.15x**, and both the peak and its delta `1.15` appeared
across all four phases (`zoomin` / `ding` / `unfurl` / `zoomout`). Reframing meant changing five
numbers that had to agree or the zoom would jump between phases.

`CINE_ZOOM = 1.65` is the peak and every phase derives from it. It still reads as a deliberate
push-in onto the flag, but leaves the neighbouring stages visible — which is the point of the
shot: seeing WHERE on the map the thing you just unlocked sits.

---

## ⚠ THE THRUSTER OFFSET WAS NEVER JUST LIZZIE

0819c logged it as hers alone: *"her flame sits slightly left of her spine."* It is
`tailX = x + (cxF-0.5)*_dw`, where `cxF` is the neutral frame's tail centre.

Measured every pilot's own hull — alpha centroid of the bottom 30% of the plate, which is the
tail — against what the rig claimed:

| pilot | tail measured | rig said | plume error |
|---|---|---|---|
| axel / cole / decker / falva / juggernaut / yuri | .4942-.4982 | matches | **under 0.2px** |
| **freezer** | .4961 | **.2703** | **13.6px LEFT** |
| **lizzie** | .5031 | **.3686** | **8.1px LEFT** |
| **maverick** | .4945 | **.3717** | **7.4px LEFT** |

**Every hull's tail sits between 0.494 and 0.503.** So those three values were not compensating
for off-centre art — they were bad measurements, and *Freezer's was worse than the one Mike
actually reported*. A one-pilot report, a three-pilot bug.

Replaced with each ship's own measured tail, by the same method the six correct ones already
match. After: **worst remaining lateral error across all nine is 0.19px.**

⚠ **THE BARREL-ROLL FRAMES ARE UNTOUCHED.** A rolling aircraft's tail genuinely does swing off
the spine, which is exactly what those per-frame values are for. Only `nf` — level flight — was
wrong, and only for three pilots.

### ⚠ and the measurement took four tries, all of them my ruler

- `"ship_lizzie"` is an **8-element trimmed-atlas rect** `[x,y,w,h,offX,offY,origW,origH]`, not the
  5-element `[sheet,x,y,w,h]` form — so a reader written for the common case returned nothing for
  all nine pilots and looked like "the art is missing".
- The fix was to stop parsing the manifest myself and let the ENGINE resolve the plate, then do
  the pixel work in-page against the decoded image. The game already knows how to find its own art.

---

## HOW TO VERIFY

    node --check assets/game.js
    node --max-old-space-size=3072 _BUILD_SOURCE/test_fl.js     2,702 ok / 3 fail

Dials: `PICKUP_SCALE` (1.22), `CINE_ZOOM` (1.65). Both are single constants.
