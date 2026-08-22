# 0821h — THE SHAPE ROTATION WAS DEAD, AND THAT IS WHAT "CHAOTIC" MEANT

Mike: *"Still chaotic/unsensual projectile patterns."*

0821a cut the RATES — peaks down 18-48% — and he was still seeing it. So this pass looked at the
SHAPES, and the shapes turned out to be broken rather than merely busy.

---

## ⚠ MEASURED FIRST, AND THE MEASUREMENT WAS THE WHOLE ANSWER

Thirty seconds of stage 6, before changing anything:

    e._volN is 0 for EVERY unit of EVERY type, for the entire run

`_step` — which picks the shape out of a unit's `alt:[...]` list — is derived from `_volN`. And
`_volN` is only incremented on `enemyVolley`'s `!force` path, while **`enemyVolleyTick`, which is
what actually fires all of these, always passes `force=true`**.

So `_step` was permanently 0. `alt` never rotated once. Each unit picked ONE shape at spawn from
`_volSeed` — a hash of where it happened to spawn — and fired only that shape for its whole life.

**That is the worst of both ends, and it is exactly what "chaotic" describes:**

- no rotation over time, so a unit is monotonous
- a per-unit spawn seed, so two talons alive together were firing two DIFFERENT shapes at once

Measured: **up to 6 distinct type+shape combinations live simultaneously, averaging 3.8.** Nothing
on screen was a formation, so there was nothing to read. 0811s intended rotation between clean
learnable shapes; what shipped was the opposite of it.

## THE FIX: THE SHAPE BELONGS TO THE TYPE AND THE CLOCK, NOT TO A SPAWN POSITION

    _step = (stageTimer / VOLLEY_SHAPE_HOLD) + per-type offset

- Every unit of a type alive at a given moment fires the **same** shape, so a wave reads as **one
  pattern**.
- It rotates every `VOLLEY_SHAPE_HOLD` (4s), so the variety 0811s wanted finally happens.
- The per-type offset keeps two rosters from switching on the same beat.
- ⚠ **Still deterministic** — `stageTimer` drives the wave table, so the same replay is the same
  fight, which 0811s requires.
- ⚠ **The TIME stagger is untouched.** `_volCd` still starts at `rnd(0.25,0.8)`, so a row of four
  ripples rather than firing on one frame. What is now shared is the SHAPE, not the beat.

### Measured after

| | before | after |
|---|---|---|
| shapes from a single type at once | up to **2** | **1** |
| distinct type+shape combos live | max 6, avg 3.8 | max 5, avg **2.8** |
| `talon` shapes used over 30s | one per unit, forever | **fan and rake**, rotating |

`fang` (`pat:'pincer'`, no `alt`) correctly stays on pincer — fixed-shape units are unaffected.

---

## ⚠ THE ASSERTION WAS GREEN THE WHOLE TIME THE FEATURE WAS DEAD

`alt:[...] rotates a unit between shapes rather than repeating one` passed on every run for
months. It passed because it did this:

    for(var i=0;i<6;i++){ r._volN=i; enemyVolley(r,true); ... }

**It set `_volN` by hand — the variable the game never sets.** So it proved the rotation MECHANISM
worked if something drove it, while nothing ever did. A green suite proving a dead feature is the
sharpest version of this repo's standing rule, and it is worth remembering that the failing signal
here came from a 30-second measurement in the browser, not from the harness.

Repointed onto `stageTimer`, which is what the rotation is actually keyed to. And a second
assertion now pins the half that was broken on screen rather than in theory: **two units of one
type must fire the same shape at the same moment.**

---

## HOW TO VERIFY

    node --check assets/game.js
    node --max-old-space-size=3072 _BUILD_SOURCE/test_fl.js     2,702 ok / 3 fail

`VOLLEY_SHAPE_HOLD` is the dial — lower it for faster variety, raise it to hold a shape longer.

## STILL OPEN

If it still reads as busy, the next lever is the number of TYPES firing at once rather than the
shapes themselves — stage 6 runs 5-6 volley-capable rosters concurrently, and each now contributes
one clean pattern, so the remaining density is a wave-table question, not a pattern one.
