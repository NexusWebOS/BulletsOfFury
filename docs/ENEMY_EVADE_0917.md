# 0917 — incoming-fire evasion for ordinary air units

Mike, overnight brief: *"continue improving my boss and enemy AI"*.

## What changed

Two unit classes already read the player's rounds and rolled out of the lane: the droids
(`droidTick`, `DROID_EVADE_R`) and the Elite X aces (*"incoming-fire rolls"*, 0915). Every other air
unit flew straight into the first burst. `enemyEvadeTick` gives the plain jets, drones, strafers and
bombers the same read, gated by difficulty:

    EVADE_DIFF = {easy:0, normal:0, hard:0.30, furious:0.55, insanity:0.80}

The number is the share of **threat reads** a unit commits to. A read is a rising player round
(not the beam, not a shard) inside the unit's lane within 96px below it; a read costs the unit a
0.5–0.9s beat whether it commits or not, so a unit under steady fire does not twitch on every
round. A commit is a 0.30s sidestep at 150px/s away from the round's side (inward at a world
edge), then a 1.1–2.0s cooldown. **EASY and NORMAL never evade** — the stages Mike has tuned play
exactly as they did. Tanks, droids, aces, in-place units and set pieces are excluded; every key of
`DIFFS` has a row, and section 366 now checks this table with the other four.

## Measured

⚠ **The thing that could have made this a jitter instead of a manoeuvre is a pattern that
re-asserts x every frame.** `jetTick` writes `e.x` in five places; if a route owned x, the
sidestep would be undone the next frame and net to zero while `_evN` said the unit had evaded.
So the probe measures the displacement THROUGH the live loop, a frame at a time, and demands it be
monotonic. Measured across the unit classes, on INSANITY with every read committing:

    s1jetdelta / s1jetbomber (stage 1, routed)   -27.9px over 14 frames, monotonic
    strafer / topgun (stage 1)                   -22.2 / -20.4, monotonic
    s1jetDelta / mdrone (stage 4)                -27.9 / -32.5
    s1jetDeltaB (stage 6)                        -27.8
    drone (stage 2, the probe's subject)         -27.5

`probe_evade_0917.py` — **11 ok / 0 fail**, 0 errors: EASY/NORMAL 0.00px; INSANITY one commit
that sticks; away from the round's side; the cooldown holds; the edge rolls inward; a tank never.
Suite section 369.

## The boss side: DENIAL

The ship-boss denial patterns pick on a fixed beat - the ember wall's doorway `(step*3)%9`, the
lance's safe lane `step%3`, the siege broadside's first half `step%2` - so a player who learns the
beat can stand still. `BOSS_DENY_DIFF = {easy:0, normal:0, hard:0.50, furious:0.75, insanity:1.0}`
is the share of picks made AGAINST where the player is sitting: the doorway opens on the far side
(`playerLane(9)+4`), the safe lane is never the player's, the bank falls on the player's half
first. **The shape of every pattern is untouched** (0811s: what the player learned still applies)
- only which beat comes next. EASY and NORMAL keep the authored beat.

`probe_bossdeny_0917.py` - **8 ok / 0 fail**: the Blacksteel Raptor's lance (its SECOND phase -
`pats:['stormbolts','lance']`, so the probe drops it to 30% hp first) through the real
`shipBossAttack` with the player parked in each lane: on NORMAL the safe lane follows `step%3`
blind to the player; on INSANITY the safe lane is never the player's across 12 beat x lane
combinations, still one safe lane and six rounds. The Siege Ember's bank falls on the player's
half on both halves and both beats; on NORMAL beat 2 fires the left bank whatever the player does.
⚠ **The probe's rounds are identified AT THE MUZZLE.** A velocity/width filter on `eBullets`
matched nothing - `_shipShot` scales by `DIFF.ebSpeed` before the round lands - so `_shipShot` is
wrapped and the pattern's own calls are counted with the numbers the pattern asked for; the other
mounts fire on their own beats and are counted as `other`.

## Not done, on purpose

The rigged bosses (Razorback, Furnace Tyrant, Tempest, the Carrier, the Warden, Vile) keep their
authored attack books - the denial touches only the three generic ship-boss lane patterns, where a
beat is a beat. Their manoeuvre books are the next AI pass. The evade speed and window are one pair
of constants (`EVADE_SPD`, `EVADE_T`) if a stage reads too slippery on FURIOUS.
