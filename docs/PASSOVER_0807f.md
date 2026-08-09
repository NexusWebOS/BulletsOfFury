# PASSOVER — drop 0807f   (ENEMIES SMOKE, THEN BURN, BEFORE THEY DIE)

Build: `BulletsOfFury_0807f`
Harness: **2,122 assertions / 194 sections / 0 failing**, twice, reaching the banner.
Full verification: **PASS — playable, every graphic resolves.**

---

## 1. WHY A UNIT LOOKED LIKE IT WAS "DISAPPEARING"

Mike: *"why is the tank disappearing like that when i start destroying it? No enemy EVER dies or
destroys like this, you start anchoring animated smoke we have to sections of the enemy unit to
signal damage, then small fires."*

I probed the stage-3 miniboss expecting a fade or a part-removal bug. **There was neither** — it
takes damage cleanly, hp counts down, no parts, no fade, then it dies.

**That IS the bug.** There was nothing between full health and dead. A unit took hits, flashed
white for 0.12s, and then was simply gone. With no state that says "this thing is nearly
finished", a big unit going from untouched to absent reads exactly as vanishing. The fix is not
to stop something from happening — it is to add the middle that was never there.

## 2. THE ART WAS ALREADY IN THE GAME, AND IT IS THE RIGHT SHAPE

Rendered every smoke and fire candidate before choosing anything:

    ntr_smkL   8 frames   a thin VERTICAL smoke trail rising from a point
    ntr_smkH   8 frames   the same, heavier
    ntr_fire   8 frames   the same, with fire along it
    nx_smoke   8 frames   round puffs — wrong shape for a hull vent
    nxp_smoke  8 frames   ⚠ not smoke at all. A red explosion cluster wearing the wrong name.

The `ntr_` set rises from a point rather than blooming outward, which is precisely what
"anchored to sections of the unit" needs. Nothing procedural, nothing new drawn.

## 3. THE PROGRESSION

    above 65% hp    nothing            a scratch should not smoke
    65% -> 35%      ntr_smkL, 1 vent   light
    35% -> 15%      ntr_smkH, 2 vents  heavy
    below 15%       ntr_fire, 3 vents  burning

**Vents are bolted to the hull, not scattered per frame.** Each is a fixed offset in the unit's
own space derived from the unit's own identity, so the smoke rides the unit as it moves instead
of jittering around it — asserted, because a wandering vent would undo the whole effect. Each
vent also runs the reel at its own offset so two vents on one hull are not in lockstep.

## 4. ⚠ HOOKED AT THE LOOP, NOT INSIDE drawEnemy

`drawEnemy` has a dozen early returns — sandtanks, arsenal drones, L6 fighters, the zap flash —
and any unit taking one of those paths would silently never smoke. The damage draw sits in the
enemy loop after `drawEnemy` returns, so it covers every unit regardless of which branch drew it.
That is the same class of mistake as the helix ball in 0806m, caught this time before shipping.

## 5. STILL OPEN FROM MIKE'S PLAYTHROUGH LIST

Eight of the eleven remain. In the order I would take them:

    stats screen — remove the window, make it pop      owed four times over now
    dialogue boxes not using our frame art            drawCommWindow frameKey not resolving
    no music from liftoff until stage 1 proper        needs a probe on what curStage.music is there
    L2 miniboss routes into the lava section          stage routing
    the tank stays on the mountain (L3)               ground unit not clamped to its terrain band
    wrong runway plate, should be over water          seqRunway(1,'run')
    retire the tiled beach water for good             needs the key pulled from the liquid set
    L2/L3 boss parts assemble closer than the concepts
