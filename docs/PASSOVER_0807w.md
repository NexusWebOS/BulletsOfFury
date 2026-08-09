# PASSOVER — drop 0807w   ("OUT OF THIN AIR" — FOUND IT)

Build: `BulletsOfFury_0807w`
Harness: **2,209 assertions / 204 sections / 0 failing — three runs, identical.**

---

## 1. THE WAVE PLAN WAS NEVER SORTED

Mike: *"shit aint working right and enemies are appearing out of thin air."*

    const add=(t,fn)=>P.push({t,fn});

That is the whole of `add()`. It pushes. Nothing sorts. And the dispatch loop walks the array **in
order**, firing whenever `stageTimer >= plan[waveIdx].t` — so the plan only behaves if it happens
to have been WRITTEN in ascending time.

It was not:

    stage 1   2 entries out of order   worst backward jump 15s    (36 -> 21)
    stage 3   5 entries                worst 41.5s                (44 -> 2.5)
    stage 4   4 entries                worst 39s                  (50 -> 11)
    stage 6   6 entries                worst 51s                  (53 -> 2)

**At a backward jump the next wave's time is already in the past, so it fires on the same frame —
and so does the one after it, and the one after that, until the plan's times catch up with the
clock.** A burst of waves dumping simultaneously, with no approach and no spacing.

Stage 6 jumps back 51 seconds. That is why stage 6 was the worst, and it matches exactly where
Mike saw it.

## 2. THE FIX, AND WHAT IT PROVES

One stable sort applied at every return from `buildStagePlan`. Stable specifically because several
stages author two waves at the same `t` to spawn a pair together, and a naive sort would reorder
them.

    out-of-order entries   ALL EIGHT STAGES: 0
    biggest wave burst in play (stages 1,3,4,6): 0
    spawns in a single frame: 3-4, from ONE wave, as authored

## 3. ⚠ AND IT EXPLAINS MY OWN FAILURE LAST DROP

My stage 1 rewrite went non-deterministic across three suite runs and I could not see why. This
is why: I wrote the new waves in proper time order, which changed which entries collided with the
unsorted ones around them. **I was moving waves to fix a scheduler bug**, so every arrangement
gave a different result and none of them could be right.

Reverting that rewrite was the correct call, but for the wrong reason — I thought my placement was
bad. The placement was fine. The pump underneath it was not.

## 4. WHAT THIS MEANS FOR THE REBUILD

The order Mike wanted — recode the enemies one at a time — is now actually possible. A wave placed
at t=36 will fire at t=36, which was not true before. Stage 1 can be rewritten on top of a
scheduler that keeps its promises.

## 5. ONE ASSERTION NEEDED RE-POINTING

The stage-4 roster check sliced `buildStagePlan.toString()` at `'return P;'`, which no longer
appears now that it returns through `_planSorted(P)`. The slice ran past the stage-4 block into
the rest of the function, where `VW*` is legitimate. Re-pointed at the new marker.
