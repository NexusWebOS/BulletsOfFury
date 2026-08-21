# DROP 0821B — THE SPAWN TRAP WAS A CLAMP, AND THE SPAWN SAFETY IT NEEDED

> "Enemies do not scroll past the bottom of the screen. They reach the bottom and stay there. This
> is a problem and causes the player to be spawn trapped. Enemies should be scrolling down and off
> the screen. Lets also create a spawn safety. If the player spawns on top of an enemy, kill that
> enemy unless it's a miniboss or boss."

## 1. IT IS ONE LINE, AND IT IS `navalTick`'s FLOOR

`probe_bottomstick_0821b.html` spawns one of every type, runs **60 simulated seconds**, and reports
anything still alive at or below the player's own row. Before:

    player spawns at VH*0.78 = 399   (hull top 384)

    s1boatGun     @453   naval      <- 54px under the spawn point
    s1boatPatrol  @453   naval
    s1boatgun     @453   naval

`navalTick` ends on `clamp(e.y, 40, VH-60)`. **`VH-60` is 452** — exactly where the probe found them
parked, and they were still there after a minute with the scroll held. Three boats permanently
camped in the one band the player cannot leave.

⚠ **THE CATCH-ALL EXIT PUSH COULD NEVER WIN.** The enemy loop's "ensure everyone eventually exits"
adds `0.7`/frame after `t>9` — and the clamp undid it on the same frame, every frame. The cull
(`y > VH+80`) was therefore *unreachable* for anything naval: not a slow exit, no exit at all.
**A unit that re-asserts its own position after the exit push is exempt from it by construction**,
and that is invisible to any check that reads the push rather than where the unit ends up.

**Fix:** the floor becomes a HOLD, not a cage. `NAVAL_HOLD_T = 9.0` — deliberately the same 9s the
catch-all starts at, so release and push begin together — after which the bottom cap lifts and the
boat rides its drift plus the scroll off screen. The top guard stays (released is not licence to
float back up), and the 0812k entry approach is untouched.

    after:  INTHE_PLAYER_ROW []      survivors sit at y 115..136, all far above the spawn

"They move, not scroll" (0808k) still holds for the boat's whole combat window. What changed is
that the window now ends.

⚠ **`gunboat` IS STILL EXEMPT AND WAS LEFT ALONE** — `e.pattern!=='gunboat'` in the catch-all, its
own note calling it "a STATION - it holds its patrol line for its whole life". It measures at y≈136,
nowhere near the spawn, so it is not part of this report. If Mike wants *everything* to leave, that
exemption is the other half and it is a design call.

## 2. TWO WRONG MODELS, BOTH KILLED BY MEASUREMENT

⚠ **"Enemies stick at `VH+80` because the clamp equals the cull threshold."** `tankTick` really does
`clamp(e.y, -80, VH+80)` while the cull tests `> VH+80`, so a tank pinned there can never satisfy a
strict `>`. Plausible, tidy, and **not what was happening** — the 60s sweep found nothing pinned at
592, and the units the 12s run showed low were on `stationgun`, not `tankTick`. Left recorded as a
latent hazard, not fixed as if it were the report.

⚠ **"Things linger below the screen forever."** The 12-second run showed five units below the
playfield and looked conclusive. At 60 seconds every one of them had culled. **A window too short to
reach the mechanism reports a stall that does not exist** — the naval boats were the only permanent
case, and only the longer run separated them from the slow-but-leaving.

## 3. SPAWN SAFETY

`clearSpawnZone()` in `reset()` — the ONE funnel every spawn and respawn passes through (fresh
stage, lost life, continue), rather than the three call sites.

⚠ **`reset(keepPos)` RESPAWNS YOU WHERE YOU DIED**, which is exactly where the thing that killed you
still is. That path needs this more than the centre-spawn does.

The zone is the player's own box grown by `SPAWN_CLEAR_PAD` (26px) per side — derived from the hull,
so a future ship of another size is covered without anyone remembering this.

⚠ **BOSSES AND MINIBOSSES ARE NOT IN `enemies`.** `boss` and `subBoss` are their own globals and
only `spawnEnemy` pushes to the array, so iterating it excludes them *structurally* — measured, not
assumed (`minibossOnTop.inEnemiesArray: false`). The predicate is for what IS in the array and still
must not be swept: the arsenal mini tier (`_mini`), modular set pieces, anything `sub`.

⚠ **`isSetPiece` IS NOW ONE FUNCTION, READ BY BOTH CALLERS.** `dkIgnite` already carried this exact
list hand-written under the same quoted rule ("except for mini bosses and bosses"). A second copy is
a second thing to forget — this file's own `_selfPat` lesson.

Measured, four cases:

| case | result |
|---|---|
| ordinary enemy exactly on the spawn point | **cleared** — cannot shoot, cannot move, collision skipped |
| ordinary enemy 260px away | survives, untouched |
| arsenal mini (`_mini`) on the spawn point | **survives** |
| real miniboss on the spawn point | **survives** |

## 4. ⚠ `e.dead` IS THE WRONG PREDICATE AND IT REPORTED A WORKING FIX AS BROKEN

The first run said `killedBySpawn: false` while `clearSpawnZone` returned `1`. Both were true.
`killEnemy` starts a *death*: `_dyingT=0, shoots=false, vx=vy=0, _frozen=true` ("stop dead the
instant it dies"), and the collision pass skips `_dyingT!=null` ("dying wrecks don't collide").
`dead` only flips ~0.35s later when the animation finishes.

**What the player needs is NEUTRALISED — cannot shoot, cannot move, cannot collide — and that is
true on the same frame.** Asserting the flag that was easiest to read would have sent me rewriting a
correct fix. Killing via `killEnemy` also means a cleared spawn plays its authored death (shock ring,
debris, white flash, smoke) instead of the enemy blinking out.

⚠ **IT CREDITS A KILL.** `killEnemy` increments `stageStats.kills`, so a safety clear scores like a
shot-down enemy and feeds the stage-clear KILLS row. Defensible (the wave still fielded it) but it is
Mike's call — suppressing it is one flag on the call.

## 5. NOT DONE

- **`tankTick`'s `clamp(e.y, -80, VH+80)` against a `> VH+80` cull** — latent, unreproduced, one
  character from being a permanent stick. Worth its own measured pass.
- **`gunboat`'s catch-all exemption** — a deliberate permanent station; see §1.
- The suite has not run (no node here). Parse-checked only.
