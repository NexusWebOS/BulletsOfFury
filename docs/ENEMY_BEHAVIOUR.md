# ENEMY BEHAVIOUR — the design

Drop 0810a. **The shared scaffold is built and asserted** (§0). The per-unit tuning in §4 is still
the proposal to argue with.

---

## 0. WHAT IS BUILT

`TELL -> COMMIT -> RECOVER` now runs for every arsenal drone, in `droneTick`.

    TELL      glow ramps from its idle throb into a hard flash; the hover stiffens
    COMMIT    the shot fires — locked, once the tell has played it is coming
    RECOVER   glow drops to 0.35x and the unit is passive. The punish window.

    easy 0.70 / 0.85      normal 0.55 / 0.68      hard 0.46 / 0.55      furious 0.40 / 0.45
    floors: tell 0.35s, recover 0.40s — asserted, so no future tuning can erase the telegraph

**ONE-HIT-DEATH IS CONFIRMED IN THE CODE, NOT ASSUMED.** `playerHit()` reads `// 1-shot kill`:
shields absorb a hit and are consumed, i-frames follow, and past that the ship is lost. So every
one of these numbers is a fairness constraint rather than a feel preference, and they are asserted
as such.

**⚠ THE REAL BUG THIS FOUND: aimed shots could not be dodged at all.** `droneFire` called `atan2`
on the player's LIVE position at the instant the bullet spawned — the shot tracked the player right
up to the muzzle, so no move beat it. In a one-hit game that is not difficulty, it is an
unavoidable death every time an aimed unit fires.

The aim now locks when the **tell begins**. Asserted with a probe that starts a `sharddart` tell,
moves the player 100px mid-tell, and measures where the shot crosses their plane: it misses by
100px. Player half-width is 9. If that assertion ever fails, aimed shots have gone back to
tracking and the game is unfair by construction.

    verify_0730a  272 passed / 17 failed   (the same 17 pre-existing art/backup failures)
    test_fl       2093 passed / 2 failed   (the missing _superseded folder)

---

## 1. THE CONSTRAINT THAT DECIDES EVERYTHING

Measured from the manifest: **every arsenal drone is a 4-frame idle loop and nothing else.**

    basaltbomber    idle:4f          cinderwasp      idle:4f
    caldera         idle:4f          magmaorb        idle:4f
    cryoeye         idle:4f          sharddart       idle:4f
    glaciercarrier  idle:4f          frostbite       idle:4f
    deathchoir      idle:4f          furymine        idle:4f
    ragetalon       idle:4f          nullprism       idle:4f
    fractureskimmer idle:4f          discordgunship  idle:4f

    dambreaker      idle:4f  rotor:8f  topthruster:4f  bottomthruster:4f   <- the only exception

No firing pose. No hit reaction. No wreck. The stock aircraft are worse — a single frame.

This matters because the design literature is unanimous that the wind-up **animation** is the
primary telegraph: *"Before the attack, we need a small delay"*, carried by a pre-attack pose,
charge particles, a bright flash. We cannot draw a pose. So the tell has to come from somewhere
else, and picking that channel is the whole design.

## 2. WHERE THE TELL COMES FROM INSTEAD

**Contra's answer: make the MOVEMENT the tell.** Its centipede robots fire a wide spread every
time they turn to change direction. The player does not read a wind-up frame — they read a change
in motion, and the change *is* the warning. That works with a static sprite.

**The shmup answer: make the PATTERN readable.** Group bullets into lines and clear shapes rather
than stray singles, which read as unfair; treat a dense pattern as a collection of lanes, each a
micro-challenge with its own risk and reward; mix aimed patterns (which pressure the player and
let them manipulate the enemy by moving) with fixed patterns (which the designer shapes).

Combining those gives three channels we already own, none needing new art:

    MOTION   a hover-stop, a bank, a turn, a recoil. The unit visibly commits before it fires.
    GLOW     DRONE_BEHAV already carries glowHz. Ramp it into the shot: slow pulse -> fast pulse
             -> flash on release. That is the "charge-up + bright flash" telegraph, in the one
             channel the art gives us for free.
    SOUND    a charge cue. Cheapest telegraph in the game and we are not using it on drones.

## 3. THE SHAPE EVERY ENEMY GETS

One loop, three phases, for every unit on the list:

    TELL      0.35-0.60s   motion changes AND glow ramps. No bullets. This is the contract.
    COMMIT    the attack fires. Locked — once the tell has played, the shot is coming.
    RECOVER   0.4-0.8s     the unit is passive and readable. This is the player's window.

The numbers matter more than the idea. A tell under ~0.3s is not a tell, it is a surprise. A
recover under ~0.35s means the enemy is never punishable and the fight is just attrition.

**Difficulty scales the TELL, not the damage.** Easy stretches the tell and the recover; furious
compresses both toward the floor and lets units overlap their windows. The attacks stay the same
shape at every difficulty, so learning transfers upward — which is the thing that makes a run-and-
gun feel fair while still being hard.

## 4. THE UNITS

Every one asks a different question. If two units ask the same question, one of them is filler.

### Level 2 — volcanic. Close, hot, aggressive.

**cinderwasp** — *"can you deal with something faster than you?"*
Darts in fast, stops dead at ~0.55 screen height (TELL: the stop, plus glow ramp), fires 2 aimed
shots, then peels off to a side. Aimed, so the player can bait the shot by moving first. Currently
hz 2.10 / cd 0.9 — keep the speed, add the stop. The stop is what makes it fair.

**basaltbomber** — *"can you read an arc?"*
Slow, high, lobs 3 shells on a fixed arc that lands where the player *was*, not where they are.
Static pattern: the same arc every time, so it is learnable. Telegraph is the bank before each
lob. The answer is to keep moving laterally — it punishes camping, which is what the level needs
underneath the faster units.

**magmaorb** — *"can you find the lane?"*
Hangs, spins up (TELL: spin rate climbs, glow brightens), releases a full 8-bullet ring. A ring is
the cleanest possible "collection of lanes" — eight gaps, all equal, all readable. Fires only
while stationary so the ring is never dragged into a smear.

**caldera** *(miniboss)* — *"can you do all three at once?"*
The level-2 exam. Alternates the three drone attacks above on a fixed rotation with a longer tell
between each, so it reads as a summary of what the level taught rather than a new vocabulary.

### Level 3 — ice. Precise, formation-minded, colder tempo.

**sharddart** — *"can you move before it commits?"*
Fast single aimed lance. Very short travel time, so the tell has to carry it: a hard bank onto the
firing line, held 0.4s, then the shard. Aim locks at the START of the tell, not at release —
without that it is unavoidable, which is exactly the "aggressive without telegraph feels cheap"
failure.

**cryoeye** — *"can you hold still under pressure?"*
Slow, opens into a 5-shot fixed ring-arc. Fixed, not aimed — so the safe spot exists regardless of
where the player is, and finding it beats fleeing. Pairs against sharddart deliberately: one
rewards moving, one rewards not moving. Fielding them together is the level-3 idea.

**glaciercarrier** — *"can you manage the board?"*
Heavy, slow, spawns 2 sub-shards on a cooldown. A priority target, not a threat — it makes the
player choose between killing the source and dodging what it already produced. The only unit on
the list whose answer is "shoot this one first".

**frostbite** *(miniboss)* — same exam role as caldera, on the ice vocabulary.

### Level 4

**dambreaker** *(miniboss)* — the one unit with real animation: 8-frame rotor and two thrusters.
It should be the only enemy whose tell is an actual animated wind-up — rotor spins up, thrusters
flare, then the attack. Everything else fakes the tell; this one earns it. Worth spending its
extra art on a genuinely different rhythm.

> ⚠ **This is a move.** `ARSENAL_MINIS` currently reads `{1:'dambreaker', 2:'caldera',
> 3:'frostbite'}`, and `LEVEL_ROSTERS.md` lists DAMBREAKER as level **1**'s miniboss. Putting it on
> level 4 leaves level 1 with no miniboss. Say the word and I will move it, but I am not doing that
> silently.

### Level 5 — chaos and fury.

**fractureskimmer** — fast erratic strafe. Skims across the top, tells with a hard bank, fires 2
on the way through. Never stops — the pressure unit.

**nullprism** — spins, releases a 6-bullet ring. The lane puzzle again, but with fewer, wider gaps
and a longer tell, so it reads as heavier rather than merely faster.

**ragetalon** — the sharddart question at higher tempo: aimed lance, 2 shots, short tell. This is
where compressing the tell is the difficulty, not adding bullets.

**deathchoir** — 7-shot wide burst on a 2.1 arc. The widest fixed pattern in the game; the answer
is to be somewhere specific before it fires, which means the tell has to be the longest of the set.

**furymine** — *"can you decide?"* Hangs motionless, glow accelerating, then detonates into a ring.
It never chases. The whole unit is a timer the player chooses to engage with or leave alone, and
its glow ramp IS its health bar as far as the player is concerned.

### Level 8 — the EsB series, per your note.

`esB_big1..6` are the six heavy craft, and they carry **3 states each** (idle / fire / hurt) —
more than anything else in the game. Restricting them to level 8 means the finale is the only
place enemies visibly react to being hit, which is a good reason for them to be there. Their
behaviour should lean on that: real hurt reactions, and a fire pose that IS the telegraph.

## 4b. WHAT THE WIDER READING CHANGES

Galaga, Raiden II, R-Type, 1942 and Einhänder, read against this codebase. Four of the five
already have a counterpart in the engine — the value is in what each says we are doing wrong with
the one we have.

### Galaga — the entrance IS the level, and it is scoreable

Galaga's aliens *"enter the formation gradually at the beginning of the stage, giving you an
opportunity to shoot them down before they even reach their position"*, and the entrance pattern
is **fixed per stage** — deterministic, therefore learnable. The stated payoff is that readable
patterns *"shift player thinking from reaction to prediction"*.

BOF spawns at `y=-30` and drives straight down. The entrance is dead time: nothing to read, nothing
to pre-empt, no reward for knowing the level. This is the single biggest gap on the thing you
picked, and it is bigger than the stacking fix.

**What it wants:** enemies fly an authored path INTO a held formation, killable the whole way, then
peel off to attack. `vKamikazePair` is already commented "GALAGA-style", so the idea has precedent
here — it just never reached the ordinary waves.

### Raiden — slow, readable bullets; scale SPEED, never count

Raiden's enemies *"shoot at consistent tempos with predictable bullet patterns that don't blend
into backgrounds"*, bullets stay *"fairly slow even on harder difficulties"*, and the higher loops
raise bullet **speed**. Memorising placement and holding a safe route is the intended skill.

The engine already agrees: `DIFFS.ebSpeed` runs 0.70 → 1.35 and `eShoot` applies it.

**⚠ Except it never reached the drones.** `droneFire` builds its own `push()` and did not multiply
by `ebSpeed`, so all fifteen arsenal drones fired at one flat speed from easy to furious. Fixed and
asserted — 4.34 / 5.46 / 6.94 / 8.37 — with a companion assertion that the bullet COUNT stays
constant (7 at every setting), because the pattern has to keep its shape for learning to transfer.

*"Don't blend into backgrounds"* — **measured, and it passes.** See §4f.

### R-Type — some enemies should occupy space, not shoot

The Force pod attaches front or back, *"working as a shield against regular bullets, damaging
everything it touches"*. R-Type is built on positional problem-solving rather than reflex.

BOF has nothing that asks a positional question. `glaciercarrier` is the nearest — it spawns
sub-shards, so it makes you choose between the source and its output. That is a board-management
question, not a routing one.

**What it wants:** at least one unit per level whose threat is *where it is*, not what it fires.

### 1942 — the evade is a finite resource

1942's Super Ace performs *"a limited number of rolls or loop-the-loops to evade"* — finite, and
purely defensive.

BOF has the roll (`BR_DUR` 0.46s, i-frames spanning it), but it is **cooldown-gated, not finite**:
`_rollCool` recharges. That is a rechargeable panic button rather than a resource you spend.

Not a bug — a design choice worth making deliberately. A finite roll only earns its keep if some
attack is designed to be beaten by rolling; otherwise limiting it just removes an out. Flagging it
rather than changing it.

### Einhänder — enemies as the weapon economy

Gunpods are stolen from enemies and carry **finite ammunition**, making the game *"a constant
struggle to replace and/or replenish"*. Some behave differently depending on where they are mounted.

BOF has weapon pickups and levels, and `dropMul` per difficulty. What it does not have is any
reason to prefer killing one enemy over another.

**What it wants:** make specific drones the *only* source of specific weapons. That converts a
wave from "clear it" into "clear it in the right order", which is the cheapest depth on this list —
it is a drop-table change, not new code.

### The through-line

Galaga, Raiden and R-Type are all won by **knowing**, not reacting. Every one of them is
deterministic: fixed entrances, consistent tempos, memorisable placement. That argues against the
`spray` attack's per-bullet `Math.random()` more strongly than the one-hit argument in §5 does —
a random bullet cannot be learned, so it can only ever be survived.

## 4c. THE RAMP — BUILT

> Mike: *"since bullets is more high speed action and has all these cool abilities, homing missiles
> etc, there should be an obvious ramp up in difficulty, enemy behaivor and action to it."*

Right, and it is the correction the Raiden reading needed. Raiden's answer is a slow deliberate
tempo you memorise. This game is fast and hands the player a lot of tools, so the tempo has to
CLIMB or the back half of a level plays exactly like the front half.

**`stageHeat()`** — 0 at the start of a stage, 1 at the end, smoothstepped so it is S-shaped rather
than linear: a quarter in it is 0.156, three quarters in it is 0.844. Gentle while the units are
still new, biting in the back third. It drives three things:

    TELL       0.55s -> 0.35s      less warning, never none
    COOLDOWN   up to 35% tighter   attacks arrive more often
    DOUBLE-TAP above heat 0.5      one tell, TWO volleys, 0.16s apart, same locked aim

The double-tap is the behaviour escalation rather than another number. It is more to dodge, but it
is still one tell and still one solution, so it stays learnable — which is the whole reason it
fires off the same locked aim rather than re-solving between volleys.

**What heat never touches:** the floors, the pattern shape, the bullet count. Asserted at the worst
case the game can produce — FURIOUS at the very end of a stage — where there is still a 0.35s tell
and a 0.40s recover. In a one-hit game that floor is the contract, and heat is not allowed to cross
it.

**The entrance sweep** — Galaga's read at this game's speed. `ENTRY_DUR 1.05s`, `ENTRY_SWEEP 96px`:
a drone arcs in from one side and straightens into its lane, banking into the curve and levelling
out. The side is seeded off spawn position, not `Math.random()`, so a wave lays out the same way
every attempt — Galaga's entrances are fixed per stage precisely so they can be learned.

It moves the **real** position, not a draw offset, so the hitbox comes with it. Being killable
during the entrance is the entire point of the Galaga model, and a draw-only sweep would have made
that a lie. The offset is applied as a delta against the previous frame and decays to exactly zero,
so whatever else moves the unit keeps working and it ends where its mover intended — asserted at
0.00px residual, because a sweep that strands a unit off-lane is worse than no sweep.

## 4d. LEVEL 2 — THE VOLCANIC SET, BUILT

Three units, three different questions. Movement runs from `droneMove`, called by `droneTick`
before the generic pattern mover integrates `e.vy` — so a drone has the last word on how it moves
and the existing mover still carries it.

**cinderwasp — "can you deal with something faster than you?"**
Dives at vy 2.9 (a stock drone is 0.9), brakes hard at 0.55 screen height, fires, peels off the
side it came in on. **The brake is the telegraph** — Contra's trick, and the only one available
when there is no wind-up frame to draw.

> A real bug on the way: it fires during the dive too, so it could reach the hold point already in
> `recover` from that earlier shot, peel on the very next frame, and never brake at all. Arriving
> now resets the phase machine — it arrives, *then* commits, fresh. Asserted at vy 0.029 in hold.

**basaltbomber — "can you read an arc?"** High and slow on purpose: the unit you have TIME to
answer, sitting underneath the fast ones. Three shells, fixed 1.32 spacing every time so the shape
is learnable, but the group is PLACED toward the locked aim — it lands where you were standing, not
on top of you. That is the difference between punishing camping and punishing existing.

**magmaorb — "can you find the lane?"** Brakes to a full stop through the tell and volley (vy 0.027
when the ring leaves) and drifts otherwise. A ring released while sliding is a smear, not a set of
equal lanes.

### ⚠ The ring was unlearnable, and that was the worst bug in the set

    a = (i/B.n)*Math.PI*2 + D.t*0.6         // D.t is seeded Math.random()*9

Where the gaps fell was **random per drone AND drifting while you watched**. In a one-hit game that
is the worst kind of pattern: it cannot be read, only survived — and the entire design here rests
on patterns being learnable.

It is anchored to the **locked aim** now. Bullet 0 goes exactly where the player was when the tell
began, so the gaps sit half a step either side. Stand still through the tell and you eat bullet 0;
move at all and you are in a gap. Same contract as every other attack — the tell is the warning,
moving is the answer — and now the ring teaches it too. Asserted identical for the same aim
regardless of the unit's time seed.

### caldera — see §4e, now built

## 4e. THE ARSENAL MINI TIER — BUILT

    stage 2  CALDERA     104px  46hp  cycles strafe -> lob -> ring     tell x1.35
    stage 3  FROSTBITE   104px  46hp  cycles lance -> burst -> spawn   tell x1.35
    stage 4  DAMBREAKER  120px  57hp  cycles four attacks             tell x1.60

Level 1 keeps its quadlaser. A mini arrives at 0.32-0.34 of the stage clock, ahead of the sub-boss
at 0.45, so a level escalates **mini -> sub-boss -> boss**.

A mini is a **drone that cycles** — built through `droneInit`, so it inherits the tell, the aim
lock, the glow ramp and the heat ramp rather than adding a second boss system beside the first. The
rotation is FIXED and never shuffled: two fresh calderas fire an identical sequence, so the order is
part of what the player learns. `tellMul` makes a mini warn for LONGER than a plain drone — bigger
and heavier should mean more readable, not less.

No warning banner and no scroll hold. That ceremony belongs to the heavier tiers, and a mini that
froze the stage would land in the same trap the sub-boss needed its `_sbLate` failsafe for.

### ⚠ WHY THE TABLE WAS DEAD — IT WAS NEVER A MISSING CONSUMER

`ARSENAL_MINIS` was declared at **brace depth 2, inside `spawnEnemy`**. So were `ARSENAL_DRONES`,
`arsenalDroneArt` and `arsenalDronesFor`. Every name in that block was function-scoped and could
not be referenced from anywhere else in the file. Nothing forgot to wire it up; nothing *could*.

This is the same bug `spawnEnemy` already carries a comment about thirty lines above it — `liveType`
and `DEAD_TYPES` were declared in a nested block and "do not resolve AT ALL from here". **That fix
inlined the one table it was looking at and left this second block sitting in the identical trap.**
The whole block is hoisted to top level now, with an assertion that the siblings are reachable too.

Worth a grep for other declarations inside that function before trusting anything else in it.

### The back-port took four attempts, and that is a finding

`sync_fn` only understands functions, so the `DRONE_BEHAV` entries, `aminiTriggered` and the trigger
block silently did not cross; then a span-sync INSERTED instead of replacing and declared `subBoss`
twice. Every one of those was caught by counting symbols in both files — never by the tool's own
"verify: identical", which it printed each time.

`gamecode.js` has genuinely diverged from `assets/game.js` in the stage-update region, which is what
the 0805a stale-source guard exists for. It wants a dedicated reconciliation pass rather than
per-change patching.

## 4f. BULLET READABILITY — MEASURED, AND IT PASSES

I raised Raiden's *"bullets don't blend into backgrounds"* as an open risk and said it needed
Mike's eyes. That was giving up too early: it is measurable. Every ordinary enemy shot is
`FIRETYPES.pellet` — `mfx_mg_2_0`/`mfx_mg_2_2`, h=16, glow `#ffd36b` — and the stage plates are
right there. Measured with WCAG relative-luminance contrast, sampling every master on a 7px stride.

**The pellet already solves this, and it solves it the way the literature says to.** Boghog's rule
is to put *"light & dark values side-by-side"* in the sprite so one end always separates. This one
does: **53% of its pixels are dark (<0.25), 24% are bright (>0.6)**.

Result — the fraction of each stage where NO part of the sprite reaches 2:1:

    stage 1 jungle 0.0%   stage 5 orbital 0.0%
    stage 2 lava   0.0%   stage 6 sky     0.0%
    stage 3 ice    0.0%   stage 7 sewer   0.0%
    stage 4 town   0.0%   stage 8 toxic   0.0%

**There is nowhere in the game the bullet disappears.** No change needed.

### The one nuance

On **stage 6** the bright end fails against 74.6% of the sky — bright gold on bright blue, and the
glow is useless there because it is brighter still. The bullet reads on its **dark rim instead**,
so it inverts: a dark dot on that stage rather than a gold one. The rim is 53% of the sprite so it
carries easily; this is a consistency note, not a fairness problem.

Stages 5 and 8 are the mirror image — their near-black grounds kill the DARK end (99.4% and 97.0%)
and the bright core carries. The sprite is doing exactly what a dual-value sprite is for.

### ⚠ How I nearly got this wrong twice

The verdict flips entirely on which statistic you pick, which is worth recording:

    median of ALL opaque pixels   0.232  ->  "BLENDS on 6 of 8 stages"   WRONG
    bright quartile only          0.827  ->  "BLENDS on stage 6"         WRONG
    full value range, best-of     both   ->  "reads everywhere"          correct

The first is dominated by the outline, which is most of a small sprite by pixel count and none of
what you look at. The second ignores that the outline is exactly what rescues it on a bright
background. Either one alone produces a confident, wrong answer — and the first one had me ready
to report a lava-readability problem that does not exist.

## 4g. LEVEL 3 — THE ICE SET, BUILT

### The mechanism that was missing: aimed vs FIXED

Every attack in the file centred on the player. That means every unit asks the same question —
*"can you move?"* — and it is exactly why level 3 had no shape: **cryoeye and sharddart were the
same problem at two different speeds.**

`aimed:false` centres a pattern straight DOWN instead of on the player. The consequence is the
whole point: a fixed pattern's safe gap sits at a fixed place on the SCREEN regardless of where
the player is standing. Running does not bring the gap with you. You have to find it and hold it.

Exactly one unit is fixed — cryoeye — and it is asserted that way, so "fixed" stays the exception
that makes it special rather than a thing that quietly spreads.

### The pair

**cryoeye** — *"can you hold still under pressure?"* Fixed 5-shot arc, widened to 2.1 because a
fixed pattern has to cover ground to be a question at all. Asserted: it fires an IDENTICAL pattern
whether the player is at x=60 or x=420.

**sharddart** — *"can you move before it commits?"* Aimed, and at spd 6.2 the fastest projectile
any drone fires — too fast to dodge on reaction. So **the bank is the telegraph**: it slows and
leans hard onto its firing line through the tell (bank 0.00 → 0.87, vy 1.90 → 0.39) and only then
releases. Same idea as cinderwasp's brake, but a lean rather than a stop, because this one never
stops moving.

**Fielding them together IS the level-3 idea.** The two correct responses are opposites, so the
player has to read WHICH one is telling before they react — and the wrong instinct is fatal. That
is a dilemma; two aimed units at different speeds is just a difficulty knob.

**glaciercarrier** — *"can you manage the board?"* Heavy, unhurried, never stops or flinches. It
is not trying to kill you; it manufactures the things that will, and the question is whether you
spend the time to go and shut it off. `hpMul: 4.5` — 18hp against a stock drone's 4 — because a
6hp carrier dies to a stray round and never poses the question. That needed a new hook: spawnEnemy
hands every drone the same `EHP(6)` before `droneInit` runs, so the multiplier is applied there.

### The measurement trap, again

The sharddart lean assertion failed on the first run reporting bank 0.87 → 0.85, i.e. no lean.
`droneMove` runs BEFORE the phase machine advances, so on the final frame of a tell it applies full
tell-bank and the phase then flips to 'commit' — sampling the phase AFTER the tick files that frame
under cruise and hides the effect entirely. Corrected to attribute by the phase droneMove actually
saw: 0.00 → 0.87.

That is the third time this drop a first-cut assertion measured the wrong thing (after the foam
grep and the magmaorb velocity probe). The pattern is always sampling on the wrong side of an
update.

## 4h. ⚠ THE ENTRANCE SWEEP ONLY REACHED THE ARSENAL — NOW FIXED

I built the Galaga entrance into `droneTick`, verified it, and reported the entrance work done.
`droneTick` runs **only for ARSENAL drones**, and `ARSENAL_DRONES` has no stage 1 entry.

So every unit on the level the complaint actually came from — racer, topgun, intcp, jungletank,
sandtank, drone, turdrone, stationship, gunboat — was **still dropping straight down**. The other
two level-1 fixes (the `warmStage` art preload for the pop-in, and the wave spacing for the
stacking) did land there. The entrances did not.

`enemyEntrySweep()` now runs for every stock enemy from the main loop, with the same rules:

    seeded from SPAWN POSITION, never Math.random()   a wave lays out identically every attempt
    moves the REAL x                                  killable throughout, per the Galaga model
    delta-applied and decayed to exactly zero         ends where its pattern intended

**Only top entries.** A unit spawned off the left or right edge already arrives on a heading, and
sweeping it would fight the entrance it was authored with. Units that start on screen, arsenal
drones, bosses and minis are all excluded — asserted, so nothing is swept twice.

### And a leak in it, caught by its own assertion

The cleanup was `else if(S.off)`, which never fired: the sweep eases to `want≈0` on its own final
in-range frame, so by the time `t` passes `ENTRY_DUR` the offset is already zero, the branch is
skipped, and the state object stays attached to the enemy being re-checked every frame for the
rest of its life. Correct residual, leaked bookkeeping. The `else` is unconditional now.

## 4i. LEVEL 5 — CHAOS AND FURY, BUILT

Mike's assignment: deathchoir, furymine, ragetalon, nullprism, fractureskimmer. Between them they
re-ask every question levels 2 and 3 taught, at a tempo that assumes you learned the answers.

    fractureskimmer  tell x0.85   never stops — fires on the way past. Pressure, not threat.
    ragetalon        tell x0.80   sharddart's lean at higher tempo. Same shape, less time.
    nullprism        tell x1.25   magmaorb's lanes made HEAVIER: fewer bullets, wider gaps.
    deathchoir       tell x1.45   the widest fan in the game, and therefore the longest warning.
    furymine         tell x1.80   a fuse. See below.

The five tell for five different lengths, and that is the design: **the widest fan warns longest
(0.80s) and the fast lance warns shortest (0.44s).** Wide and fast would be unfair; wide and slow
is a positioning problem — you have to read it early and walk out of the arc.

### ⚠ FURYMINE DID NOTHING AT ALL

Its whole attack was:

    case 'mine': e._mineArmed=1; break;

**One write, zero readers.** Grep the engine: nothing anywhere consults `_mineArmed`. So furymine
hung in the air, ran its cooldown, armed itself forever, and never fired, exploded or threatened
anything. `n:1, spd:0` was the tell — there was no ring to detonate into because the detonation was
never written.

It is a **timer the player chooses to engage with** now: it hangs (settled vy 0.099, it never
chases), its glow accelerates through the longest tell in the game, and then it detonates into a
full 10-round ring and dies. The fuse IS its health bar as far as the player is concerned, and the
question is not "can you dodge this" but "is it worth your time and your position to go and deal
with it".

### SPRAY was unlearnable, and that contradicted everything else here

`spray` rolled `Math.random()` per bullet for **both** angle and speed — a fresh dice throw every
time. In a one-hit game that is the one thing a pattern must never be: it cannot be learned, only
survived, and the shmup literature is explicit that random placement *"can create unfair
situations"*. Every other deterministic choice in this design — fixed entrances, aim-anchored
rings, the locked aim — exists so the player can learn. This quietly opted out of all of it.

It still reads as scatter, because the offsets are irregular. They are just the SAME irregular
offsets every time: a golden-ratio walk keyed to the shot index. Learnable scatter, which is what
"loose" should have meant. `discordgunship` is the only user.

### A flaky assertion, found by accident

The suite failed once in four runs on *"two of the same drone are phase-offset"* — it spawned
exactly TWO drones and demanded their hover differ, while `droneInit` seeds `ph` from
`Math.random()`, so two can land together by chance. **A test that fails at random is worse than no
test: it teaches you to re-run until green, which is how a real failure gets waved through.** It
samples a formation of ten now, and eight consecutive runs come back identical.

## 5. SETTLED, AND STILL OPEN

Settled:

* **"skimmer" on level 5 is `fractureskimmer`**, the arsenal drone — not the stage-7 pool type.
* **dambreaker to level 4 is fine** — the `ndr_dambreaker` art is not the miniboss level 1
  actually uses, so level 1 loses nothing. The §4 warning is withdrawn.
* **The windows** are set at §0 and asserted. One-hit-death drove them: with no health bar the
  telegraph is the only thing standing between "hard" and "unfair".

Still open:

* **`discordgunship`** — the 15th arsenal drone, still unplaced. Level 5 would make six there;
  parking it is also fine. It is the only one running the `spray` attack, which is the one attack
  in the table built on `Math.random()` per bullet. In a one-hit game a randomly-placed bullet can
  close the lane the player already committed to — the shmup guidance warns random patterns
  "create unfair situations", and one-hit makes that a run-ender. If it goes in, `spray` should be
  reseeded deterministically so it is loose but not a fresh dice roll.
* **The per-unit tuning in §4** — none of it is written yet. The scaffold gives every unit the same
  honest tell; §4 is what makes them ask different questions.

---

**Sources for §2** — Boghog's bullet hell shmup 101 (shmups.wiki) for the aimed/static/random
taxonomy, chunking, and the lanes model; "Enemy Attacks and Telegraphing" (gamedeveloper.com) for
the wind-up/charge/flash telegraph rules; StrategyWiki and the Contra Encyclopedia for Contra III's
enemy behaviour, including the turn-to-fire centipede that the movement-as-telegraph idea comes
from.
