# STEP 1 — THE LEVEL 1 OPENING IS LIVE

Your passover doc's own recommended order, step 1: *"Flip DBG.transitions = true and check the
level 1 opening feels right. It's the template for everything else."*

Done, with one change to how the flag works.

## Why enabling it broke the game before

`DBG.transitions` gated **nine things at once**:

    the level-1 OPENING          built
    TRANS[1] .. TRANS[8] routes  none built

Turning it on turned all nine on. It was never one feature — it was one built feature and eight
empty ones sharing a switch. So the split:

    DBG.opening      = true      the level-1 start. Built, and now verified.
    DBG.transitions  = false     the end-of-stage routes. Still off, one at a time.

## The opening, driven headless

Not "it compiles" — the actual sequence, 1080 frames at 60fps:

    runs 1080 frames without throwing
    walks 5 distinct phases          RUNWAY -> TAKEOFF -> SKY -> COAST -> HANDOFF
    scroll ramps 41 -> 200           Genesis-style, scroll rate only, no blur or filters
    THE PLAYER IS NEVER MOVED        0 position changes across all 1080 frames

That last one is rule 1 from your doc, in your words: *"do not cut our position or move the pilot
or anything. simply start the game exactly where they are positioned, no sudden jerks movments or
cuts."* It is asserted, so it cannot quietly regress.

Two implementation details from the doc, both still intact and now asserted:

- the runway steps by **858px**, not H-128. The plate has fully transparent bands at rows 114-127
  and 986-999; stepping by H-128 lands one band on the other and puts a black stripe across the
  road. 858 puts each band over the other's solid content.
- the sky is the **authored** sky plate, not `tflat_sky` — that one is a crop of the ORBITAL
  stage, which is why it read as a starfield.

## Try it

    COLE1  drops you at the stage-1 boss on its last sliver
    start a normal run to see the opening

## Next, when you say so

Step 2 in your order is **1 -> 2 · WATER**, and it is the most fully specified:

> *"remember the dam swaps to a destroyed image at the end. Keep the player positioned where they
> were at the time of the cut, and after the cut position them where they should be. from there,
> they fly directly past the broken dam, use the water tile, and make us fly over water. follow
> the player. do not fly them off in the distance to some cut water. this should look fluid. then
> you transition fade as we follow them flying to the stage end stats screen."*

Beats: dam swaps to destroyed -> fly PAST it -> out over water on the water flat -> camera follows
-> fade -> stats. `TRANS[1] = {via:['water']}` already carries the route data.

It proves the END pattern the way the opening proved the START pattern. I will build only that,
and you check it with COLE1 before we go near 2 -> 3.
