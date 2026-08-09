# PASSOVER — drop 0807v   (THE SHARED TAIL IS GONE; MY STAGE 1 REWRITE IS NOT READY)

Build: `BulletsOfFury_0807v`
Harness: **2,198 assertions / 203 sections / 0 failing — three runs, identical.**

---

## 1. WHAT SHIPPED: THE CONFLICT IS CUT

`buildStagePlan` ran each stage's own table and then fell through to a shared tail adding **31
waves across 12 enemy types to every stage 2-8**, gated only on `stageNum>=2` / `>=3`. Stage 6 got
assault, drone, gunship, frost, cryo, mine, octo, mech, scout, shieldd, turdrone and icegun on top
of its storm-front cast — Mike's "enemies from all levels", and the reason no stage played as
authored. Removed, preserved verbatim in `docs/removed/`, and ten assertions now stop any of it
returning to stage 6.

Stage 1 was the only stage that escaped it, via an early `return P`. Which is why stage 1 has
always felt closest to right.

## 2. ⚠ WHAT DID NOT SHIP: MY STAGE 1 REWRITE

I wrote stage 1 from scratch as asked — same five units, each with a defined job, air waves as the
high-speed half and ground waves as the shmup half. It played: miniboss and boss both reached,
16 of 20 waves firing.

**But it was non-deterministic.** Three consecutive suite runs gave 4 failures, then 2, then 0.
The failing assertions were the beach-tank ones — the same coastline behaviour Mike has reported
twice before.

The cause is not wave placement, and I moved waves three times before understanding that:

* Stage 1's ground waves can only fire inside a narrow terrain window — after LAND at scroll 1416
  (~t=35s) and before the halfway cutoff at 2144 (~t=54s).
* `_s1Ground` DEFERS a wave by decrementing `waveIdx`, which re-queues it into a TIME-ORDERED
  plan, so it then competes with whatever else is due at that moment and pushes everything behind
  it.
* The miniboss triggers at scroll ~2197 — only ~53px past the cutoff. The whole ground section
  rides that margin.

**That is a scheduler problem, not a placement problem.** A level that plays differently on every
run is worse than one I have not touched, so the original table is restored and verified green
three times. My rewrite is kept in `docs/removed/stage1_waves_rebuild_attempt.js` with those three
findings written at the top, because they are what the next attempt has to solve FIRST.

## 3. WHAT I LEARNED THE HARD WAY, RECORDED

Replacing the stage 1 block dropped two things declared inside it — `S1_HALF` and the three
`_s1Ground` / `_s1OnLand` / `_s1Past` helpers — and each took the stage down with a
ReferenceError until restored. The terrain gate in particular is hard-won: its own comment
explains that Mike reported the coastline twice before it existed, and that a ground wave must ask
the TERRAIN, not the clock. **It is not part of what "start from scratch" should throw away.**

## 4. NEXT

Fix the wave scheduler so a deferred wave cannot reorder the level, THEN rewrite stage 1 on top of
it. Rewriting the waves first is what I just tried, and it does not work.
