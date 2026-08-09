# PASSOVER — drops 0805a through 0806a

Build: `BulletsOfFury_0806a`
Harness: **2,021 assertions / 176 sections / 0 failing**.
Baseline at session start was 1,807 / 157 / 0.

---

## 0. READ THIS FIRST — THE BUILD HAD A LANDMINE IN IT

`assets/game.js` is what `index.html` loads. On arrival it was **nine drops ahead of
`gamecode.js`** — every change from `0801kl` through `0801ku` had been hand-edited
straight into the built artifact and never back-ported. 45 diff hunks, drop tags
confirmed by grepping the diff:

    0801kn x8   0801km x8   0801kl x8   0801ku x4
    0801kp x3   0801kr x2   0801kk x1   0801kg x1

Running `assemble.py` in that state silently reverts all of it. Because the harness
reads `assets/game.js`, the loss shows up as dozens of previously-fixed things
breaking at once with no obvious cause.

**`assemble.py` now refuses to run when `assets/game.js` is newer than `gamecode.js`
or `patches.js`**, printing both timestamps. Verified it blocks. `--force` overrides,
and should only be used after a real back-port.

**THE RECONCILIATION IS STILL OWED.** The guard stops the bleeding; it does not sync
the sources. Until someone back-ports those nine drops, `gamecode.js` is not the
source of truth and should not be treated as one.

---

## 1. TEN OF TWELVE BOSSES COULD NEVER FIRE A SHOT

> Mike: "the firebosses still not functioning right"
> Mike: "None of my mini bosses are attacking me either"

`mechFireTick` looked up `K.parts['left-cannon']` and `['right-cannon']`. Only the two
GENESIS mechs own a part with that name. `BOSS_ROSTER.md` says it outright — these
twelve **"share a system, not a vocabulary"**:

    mech        left-cannon / right-cannon              mbg2 mbg3
    tank        left-weapon-pod / right-weapon-pod      mbo2 mbg3f mbm4 mbl5
    aircraft    left-weapon-rack / right-weapon-rack    mbw4 mbs6 mbc6
    fortress    left-siege-arm / right-siege-arm        mbr5
    crawler     left-crusher-claw / right-crusher-claw  mbs7
    segmented   left-claw / right-claw                  mbt7

For ten of them the lookup returned `undefined` and the loop `continue`d past both
sides on every frame. `mechFxDraw` carried the identical lookup, so their muzzle
flashes never drew either.

### Measured — 20 simulated seconds, calling `mechFireTick` directly

| tag | archetype | before | after |
|---|---|---|---|
| mbg2 | mech | 52 | 54 |
| mbg3 | mech | 52 | 56 |
| mbg3f | tank | **0** | 56 |
| mbw4 | aircraft | **0** | 54 |
| mbr5 | fortress | **0** | 54 |
| mbs6 | aircraft | **0** | 56 |
| mbt7 | segmented | **0** | 54 |

The two mechs are unchanged — no regression on the only two that already worked.

### It was a naming bug, not a data bug

`BOFX.mechfx[tag].muzzle` already carried **left and right anchors for all twelve**.
The muzzle derivation described in `BOSS_ROSTER.md` had done its job. Only the
part-name lookup was wrong. A harness assertion now pins this so nobody goes chasing
the fx data next time.

`_mechGunParts(K)` resolves from the boss's **own `drawOrder`** by walking a suffix
candidate list, rather than from a hard-coded table — same principle as the 0801ac
readiness-gate fix: ask the pack what it has instead of assuming a name. Cached per
boss. Single-weapon fallback to `front-weapon` / `nose` so a boss without a left/right
pair still shoots.

### ⚠ ONE DESIGN CALL THAT IS YOURS TO REVERSE

Only mbg2/mbg3 shipped rotation frames (`mbg2_rot_*`, 37 each), so `mechAimCannons`
sets `part._aim` for those two **only** — correct, and left alone, because the standing
rule is that the other ten draw exactly as they shipped with nothing moving.

But `aim = part._aim||0` meant a static barrel fired at 0 rad — **straight down**. Ten
bosses put their whole salvo down the centre line and a player standing anywhere else
was never in danger. "Not attacking me" is what that looks like from the cockpit.

So the **shot** is now aimed even though the **barrel** is static, clamped to ±0.62 rad
so `|vx|` can never exceed `|vy|` — the 0801kn no-sideways-rounds rule. **0 sideways
rounds measured across all seven tags tested.** No non-mech component is rotated by a
single degree; the art rule is intact.

**Revert = drop the `else` branch in `mechFireTick` and it is exactly as it was.**

---

## 2. THE COASTLINE TANKS — THE REAL FIX

> Mike, repeatedly: "the big tanks are missing", "I dont see the big tanks at the coast line"

Drop 0801ke moved the quadlaser from `at=0.45` to `at=0.62` to put it behind the beach.
But `at` is a fraction of **stageTimer**, and stageTimer does not advance in lockstep
with **mapScroll**.

### Measured over 8 runs

    sub-boss trigger    scroll 1538          every single run (deterministic)
    jungletank wave     scroll 1477 - 1559   (82px of spread)
    sandtank wave       scroll 1978 - 2029

So it was a **coin flip** whether the miniboss beat the beach tanks — it did in 2 of 8.
And since 0801hn made the miniboss **hold the scroll until it dies**, losing that flip
freezes the level short of the coast and the tanks never arrive. That is why this kept
reading as fixed: it was fixed most of the time.

Worse, even when the flip was won, 1538 is still ahead of the sand tanks at ~1978, so
the order was never the one specified:

> "flyby, beach tanks, grass jets, diagonal file, sand tanks, THEN the miniboss"

### The fix

`SUBBOSS[1]` gains `afterScroll: 2100` — an optional **second** gate in scroll units.
Both gates must be satisfied, so this can only ever **delay** a miniboss, never summon
one early. Stages without the field behave exactly as before.

2100 clears the observed sandtank maximum (2029, and the harness independently reports
1976) with headroom. Re-measured: trigger is now deterministic at **scroll 2101**,
behind every wave, **8 runs out of 8**.

---

## 3. TWO HARNESS BUGS THIS EXPOSED

Both were pre-existing and both were hiding behind green ticks.

**`stage 1: the miniboss arrives AFTER the tanks` was flaky at ~50%** (3 of 6 runs).
That was not test noise — it was faithfully reporting the coin flip in §2. Now stable.

**The level-1 jets block never actually scrolled.** It fakes a fresh stage by hand
(`waveIdx`, `stagePlan`, `stageTimer`) but never touched `mapScroll` and never called
`drawWorld` — and `drawWorld` is what advances the scroll. So it inherited whatever
scroll the *previous test* left behind, and the wave types it "saw" were a side effect
of test ordering rather than of playing stage 1. It passed anyway, so nobody looked.

It only surfaced when the sub-boss picked up `afterScroll`: a leaked scroll past the
gate fired the miniboss on frame one and starved the later waves. Fixed to do what it
claims — start at scroll 0 like `beginStage()` does, drive `drawWorld` each frame, and
clear the sub-boss as it arrives so it cannot hold the scroll.

**Window widened 60s → 90s.** Measured first-appearance of `topgun` across 6 runs:
59.4, 59.6, 60.5, 63.5, 64.3, 64.9 seconds — straddling the old 3600-frame window
exactly, so that assertion was a second coin flip.

---

## 4. NEW HARNESS SECTION 158

Five assertions, and **verified to bite**: reverting `MECH_GUN_SUFFIX` to `['cannon']`
produces `mute: mbr5, mbs7, mbt7` rather than passing vacuously.

* all twelve boss tags registered
* every tag resolves at least one gun part from its own `drawOrder`
* mbg2/mbg3 still resolve to `-cannon` specifically, so their rotation frames keep tracking
* every tag already had left+right muzzle anchors — the data was never the bug
* the static-barrel aim is clamped inside the downward cone

---

## 5. THINGS FOUND AND **NOT** FIXED

Recorded honestly rather than half-fixed.

* **`NEWBOSS` is entirely dead code.** It maps stages 1-4 to `chopper_idle`,
  `fboss_idle`, `iboss_idle`, `tankboss_idle` — **zero registered keys for any of them**.
  `_nbReady` is therefore permanently false and `drawNewBoss` always returns false.
  The same is true of every other fallback in `drawBossSprite`: `dread_0`,
  `boss2_0`-`boss5_0`, `boss_idle`, `boss_d1`, `boss_dest1`, `t_muz0` — **all missing
  from the manifest.** Only two branches in that whole function have real art behind
  them: the `damkeeper` helicopter and the `bz*` megas. It is not currently causing a
  visible bug because `mechDraw` intercepts first, but it is a large trap sitting in
  the middle of the boss draw path.
* **The stage-1 helicopter is far quieter than the rest.** Measured over a full stage:
  0.21 shots/sec, against Storm Sovereign 2.45 and Toxic Leviathan 2.96. Not touched —
  that is a balance call.
* **Magma and Cryo take 12.9s to reach fight phase** where the other four take ~2s.
  That is the pending entrance-choreography decision showing up as a measurement.
  **Not touched — boss choreography is not changed without explicit direction.**
* **`MINIBOSS[]` (esB_big1-6) has no spawn path.** `SUBBOSS[]` names quadlaser,
  obsidiandrill, glacierrail, subreactor, subcore, ss, ratking, herald — none of the
  six. Their `b.mini` branch through `bossProfileAttack` is unreachable in play.
* **Enemy HP not touched.** Still needs the difficulty setting used, or the wrong
  number gets tuned.
* Still open from the 17-item list: MG pellet box, jets entering sideways without
  flying in, Axel's orb, Maverick's helix ball, the Freezer/fireball powerup icons,
  fireball spin ring, stage-2 one-frame death, stage-3 turret anchors, dam intact vs
  broken.

---

## 6. STILL TRUE FROM THE LAST PASSOVER

* **A harness pass is not a game pass.** Reconfirmed hard this session. The
  boot-real-code-and-record-drawImage probe is still the only thing that catches "the
  code drew the wrong thing".
* **A probe is not a game either.** Three separate false findings were produced and
  caught this session before they reached Mike: "all bosses invisible" (never drove
  `updateBoss`, so the mechs sat in `assemble` phase), "sub-bosses fire 0 shots"
  (counted `ebullets`, the array is `eBullets`), and "sandtank never spawns" (probe
  setup clobbered the stage plan). **Measure, then check the measurement.**
* `_superseded/` is absent from the incoming zip and the harness hard-crashes without
  it. Stubbed with eight ledger files to run. Packaging artifact, not a code bug.

---

## 7. SUGGESTED NEXT

1. **Back-port the nine drops** so `gamecode.js` is real again.
2. Confirm what the bosses look like on screen when they fail — nothing at all, or a
   grey hull with an "88" on it. The second is the procedural fallback and would say
   `mechDraw` is returning false in the browser specifically.
3. Delete or repoint `NEWBOSS` and the dead fallbacks in `drawBossSprite` (§5).
4. Enemy HP, once the difficulty setting is known.


---
---

# DROP 0805b — THE DIFFICULTY SPEC

## 8. FODDER HP IS NOW DEFINED IN SHOTS-TO-KILL

Mike gave the spec in shots, so the game now stores it in shots. Raw HP is meaningless
without knowing what a shot does — and he flagged exactly that himself:

> "Im thinking of slowed shots, so that might triple out with all numbers Idk.
> the dps is what matters I guess?"

Right, and a shots-based table is the answer: if pellet damage or fire rate changes
later, the feel is preserved and only the derived HP moves.

### What was actually there — measured, at NORMAL, against the base gun (2 dmg/pellet)

    stage 1   intcp 2   topgun 2   racer 3   sandtank 3   jungletank 6
    stage 2   ash 7   skim 8   lance 8   eye 9   disc 11   cruc 23   carrier 31
    stage 3   minidrone 14
    stage 5   crescent 11   oracle 14   hauler 17
    stage 6   bcarrier 21   talon 53
    stage 7   maw 20   shambler 15   barge 35
    stage 8   oracle 14   hauler 17   talon 53   cdisc 60   hell 66

Stage 2 is the fire stage. Its fodder ran to **thirty-one shots** against a spec ceiling
of seven. That is "fire enemies and all other fodder enemies in other levels are too
tough/too much hp", in numbers.

**And there was no stage scaling of any kind.** `DIFF.eHp` was one flat multiplier, so a
stage-1 drone and a stage-8 drone had identical HP. The curve Mike describes — 2-3 early,
3-4 by stage 3, 5-7 at the end — did not exist in any form.

### After

    stage   EASY      NORMAL    HARD      FURIOUS
    1       1-2       2-3       3-4       3-5
    2       2-2       3-3       4-4       5-5
    3       1-3       2-4       3-5       4-6
    4       1-3       2-4       3-5       4-6
    5       1-3       2-5       3-7       4-8
    6       3-3       5-5       6-7       8-8
    7       4-4       6-6       8-8       10-10
    8       2-5       3-7       4-9       5-11

EASY reads 1-2 on stages 1-3; NORMAL opens 2-3, hits 3-4 by stage 3, and caps at 7.
Worst offenders: carrier 31 -> 3, hell 66 -> 7, talon 53 -> 5, minidrone 14 -> 4.

### How it maps

Authored base HP is kept as the RELATIVE weight — which units are meant to be tougher is
the designer's call and is not overwritten. It is compressed onto the stage's band:

    shots = bandLo * (currentShots / 2) ^ 0.40   clamped to [1, bandHi]

Pivot 2 / exponent 0.40 were **measured in, not picked**. Pivot 4 was tried first and put
NORMAL stage 1 at 1-2 against a spec of 2-3 — the curve dragged light units under the band
floor. Pivot 2 anchors a 2-shot unit exactly on the floor while genuinely trivial things
still fall below it and a 66-shot sponge still lands on the cap.

40 separate `Math.ceil(N*DIFF.eHp)` expressions were routed through one `EHP()` chokepoint.
That scattering is exactly why a flat multiplier survived this long — there was nowhere to
change it.

**Bosses and minibosses were deliberately NOT rewired** — "mini bosses of course each get
there own set of HP, and have there own way to defeat them." Their 8 spawn sites keep
`DIFF.eHp`, and an assertion checks no boss site was moved onto the fodder band.

### ⚠ FURIOUS BLOWS THROUGH THE CEILING — worth your eye

Stage 7 fodder reaches **10 shots** and stage 8 reaches **11** on FURIOUS. The 5-7 ceiling
was stated for NORMAL and "Hard is a scale up from normal" implies going above it, so this
is left as specified — but 11 shots for a fodder unit is a lot and the cap could just as
easily apply after the difficulty multiplier instead of before. One line either way.

---

## 9. CONTINUES ARE CAPPED

> "Hard is a scale up from normal, and you only get 3 continues."
> "Furious - You only get 1 life, 1 continue and 1 life per that 1 continue you do get."

**There was no continue counter in the game at all.** The continue was free and infinite on
every difficulty, and it handed back a full `DIFF.startLives` stock every time — so FURIOUS,
a one-life run, could be restored to full forever.

    easy     continues -1 (uncapped, unchanged)   contLives 3
    normal   continues -1 (uncapped, unchanged)   contLives 3
    hard     continues  3                         contLives 3
    furious  continues  1   startLives 1          contLives 1

`run.contUsed` counts them and resets per RUN, not per stage. Out of continues sends the
player to GAMEOVER rather than back into play.

FURIOUS `ebSpeed` 1.35 / `eFire` 1.60 already sit ~20% over HARD, inside the "10-25% faster"
band. **Smarter dodge and manoeuvrability detection is NOT implemented** — that is new AI
behaviour, not a multiplier, and it is not in this drop.

---

## 10. MINIBOSSES SPAWN AT THE MAP HALFWAY POINT

> "mini bosses should spawn at the halfway point of the map and stop the scrolling of the level."

"Stop the scrolling" was already true — `subBossActive` holds `stageTimer` since 0801hn.
No change needed.

**The first attempt used `scrollLen` and was wrong.** `scrollLen` is the MASTER's scroll span
(4800 for stages 1-4, 7324 for stage 6) — but a stage does not play to the end of its master.
Halving it put stages 7 and 8 past any scroll their stage reaches, and their minibosses
stopped spawning entirely. The suite caught it. Measured scroll at the boss warning:

    stage 1  2481    stage 3  2001    stage 5  2241    stage 7  2321
    stage 2  1921    stage 4  2081    stage 6  2241    stage 8  2401

Halfway now comes from that **played span**. Verified in play — stages 2-8 all land at
**48% of the way to the boss**.

### ⚠ STAGE 1 IS AN EXCEPTION — YOUR CALL

Its true halfway is 1241, but the sand tanks do not land until ~1976, and the standing order
is *"flyby, beach tanks, grass jets, diagonal file, sand tanks, THEN the miniboss"*. Both
instructions cannot hold. The explicit wave order wins for now — it was given three times and
is the more specific — so stage 1 sits at **2100**, which is 81% rather than 50%.
**If halfway should override the wave order, that one value becomes 1241 and nothing else changes.**

### A failsafe, because a gate must never delete a miniboss

Gating purely on scroll means anything that stalls the scroll silently removes the miniboss
for the whole run, invisibly and unrecoverably. The scroll gate now applies only until 85% of
the stage has elapsed, after which the time gate stands alone. In normal play the scroll
always arrives first and the failsafe never fires.

---

## 11. STILL OPEN FROM THIS BRIEF

* **The 3-5 second miniboss cinematic is NOT built.** The current arrival is a 2.4s warning
  plus a ~1.6s entry glide. Building a cinematic needs to know what is *in* it — camera move,
  name card, radio line, art — and that is a design call, not a duration. Tell me what it
  should contain and it goes in next.
* **"there all air units"** — not acted on, because it contradicts a standing rule. The
  Obsidian Drill Tank and Glacier Rail Fortress are tracked TANKS in the roster, and the rule
  from 0731v is *"tanks never wob, bob or sway ... they operate like a tank"*. Making them air
  units means either recasting those two or dropping that rule. Which?
* **Magma/Cryo 12.9s entrance** — read as confirmed rather than as a complaint, so it is
  untouched. Say the word if it should come down.
* **Boss fight length 1-3-5 minutes** — not measured or tuned yet.
* Unchanged from 0805a: MG pellet box, jets entering sideways, Axel's orb, Maverick's helix
  ball, Freezer/fireball powerup icons, fireball spin ring, stage-2 one-frame death, stage-3
  turret anchors, dam intact vs broken, and the nine-drop back-port.


---
---

# DROP 0805c — THE PELLET BOX, AND TWO RULINGS

## 12. THE MACHINE GUN PELLET BOX

> "laser attacks each turret properly, my machine gun pellets dont past a 'box' which I
> think you have extending over where the turrets are in front with the plane or something."

Described exactly right. There were **two different geometries** doing two different jobs:

    CONSUMING the bullet    a full bounding RECTANGLE around the sub-boss
    ROUTING the damage      per-cannon hitboxes (_qlCan[].hb) / per-section plates

A pellet entering anywhere inside the rectangle died on the spot — including the empty air
between two cannons — and `hitSubBoss` then looked for a part underneath it, found none,
and did nothing. The pellet was eaten by a box and dealt no damage.

**The laser looked correct because it PIERCES.** `pierce` skips `b.dead=true`, so it kept
travelling and struck each cannon in turn. That is the whole asymmetry Mike reported, and
it is why the same shot pattern behaved differently for two weapons.

### Measured on the stage-1 quadlaser

    bounding box          196 x 196   (2500 sample points at 4px)
    actually solid armour  464 pts    19% of the box
    empty air              2036 pts   81% of the box  <-- every one of these ate a pellet

`subBossSolidAt(x,y)` now decides. It returns TRUE only where there is real geometry,
FALSE where a shot should fly on through, and **NULL for units with no part data at all** —
those keep the bounding rectangle they have always used, so nothing regresses. The
rectangle survives as a cheap broad phase.

Verified after the change: all four cannons still take damage at their own centres (3,3,3,3).

### ⚠ A DEADLOCK I INTRODUCED AND THE SUITE CAUGHT

First version gated hull solidity on `b._qlHullOpen`. That flag is set **inside**
`hitSubBoss` — so with every cannon dead, nothing was solid, so no pellet reached
`hitSubBoss`, so the flag was never set, so nothing was ever solid again: **the miniboss
became invulnerable for the rest of the run.**

That is precisely the 0801jw bug ("the miniboss is not killable") being reintroduced by a
different route. Hull solidity is now derived from the live cannon count directly, and an
assertion sets `_qlHullOpen=false` by hand with all cannons dead and requires the hull to
be solid anyway, so this specific deadlock cannot come back.

---

## 13. TWO RULINGS, NOW LOCKED IN CODE

Both were open questions from 0805b. Both are answered, recorded at the code they govern,
and pinned by assertions so a later pass cannot quietly "correct" them.

**"stage 1 81"** — the wave order beats the halfway rule on stage 1. The quadlaser stays at
scroll 2100, which is 81% of the way to the boss rather than 50%, because the sand tanks do
not land until ~1976 and the standing order puts the miniboss behind them. Stages 2-8 remain
at their measured halfway (48%).

**"no those are indeed tanks"** — the "all air units" note does NOT apply to the Obsidian
Drill Tank or the Glacier Rail Fortress. They stay in `TANK_ARCHETYPES`, and the 0731v
locomotion rule ("tanks never wob, bob or sway ... they operate like a tank") stands
unchanged. They are not to be put on the hover path.

---

## 14. WHAT IS STILL OPEN

* **The 3-5 second miniboss cinematic.** Still needs its CONTENTS specified — camera move,
  name card, radio line, art — not just its duration. Current arrival is a 2.4s warning plus
  a ~1.6s entry glide, so the timing slot is already roughly there.
* **Furious fodder reaching 10-11 shots** (see §8) — the cap currently applies before the
  difficulty multiplier. One line to move it after.
* **Smarter dodge / manoeuvrability on Furious** — new AI behaviour, not a multiplier, not
  started.
* **Boss fight length 1-3-5 minutes** — not measured or tuned.
* **`NEWBOSS` is dead code** and the other `drawBossSprite` fallbacks point at art that does
  not exist (see §5). Harmless today, large trap.
* **The nine-drop back-port** — `gamecode.js` is still stale; `assemble.py` is guarded but
  the sources are not synced.
* Unchanged: jets entering sideways without flying in, Axel's orb, Maverick's helix ball,
  Freezer/fireball powerup icons, fireball spin ring, stage-2 one-frame death, stage-3
  turret anchors, dam intact vs broken.


---
---

# DROP 0805d — CF_Orb/IceBreath/MachineGun Vol.4 + CF_SpreadFire Vol.1

74 keys registered, 0 broken paths. Both packs verified before wiring: hard alpha
(0 partial-alpha pixels), no magenta, and the ice reel's 8 frames confirmed to share a
**pixel-identical alpha silhouette** (max channel diff 0) as the handoff claims.

## 15. THE UNIVERSAL HELPER ORB — AND AXEL'S REAL ORB AT LAST

> "a better orbit graphic we can now use universally for all characters with palette
> swaps including axel."

**What it replaces.** Axel's orb was `aorb_0..11` — Falva's orb art hue-rotated to royal
blue back in 0801fh. That is the "faux orb": not an orb drawn for the job, but somebody
else's orb pushed round the colour wheel, which drags the original's shading with it.

The new orb is deliberately **neutral greyscale** — measured (190,194,198) / (133,138,145)
/ (47,51,57), zero saturation. That is exactly what makes it universal: a grey sprite takes
any colour cleanly where a blue one cannot.

**Tinted by luminance, not by overlay.** Each pixel's own brightness picks a point on the
tint ramp — above the midpoint it runs toward white so specular highlights survive, below it
toward black so the shadow side keeps its depth. An overlay would have flattened both. Cached
per colour, since this runs every frame for every orbiting helper.

`NUO_TINTS` gives all nine pilots a colour, all distinct, with **Axel on royal blue
`#2f6fff`** as specified. `aorb_` stays registered as the decode fallback.

⚠ `AXEL_ORB_COLS` is a **different** system — the aegis shield ring's hue cycle, with three
live call sites. It was briefly deleted during this edit and restored; it is not the helper
orb's palette and must not be merged with it.

## 16. COLE'S TIER 6 AND 7 BULLETS

> "I got upgraded level 6 and 7 bullets for cole's machine guns."

The TIERS already existed — `coleTier()` has gated 6-8 to Cole since 0801k — but the draw
clamped to `clamp(b.lv,1,5)`, so a tier-6 or tier-7 round drew the **level-5 red pellet**.
Cole's exclusive tiers were mechanically real and visually identical to everyone else's top
tier. The pack's colours match the existing design note exactly ("gold at 6, black four-wide
at 7").

L6 gold and L7 black, 32x56, drawn at their authored aspect rather than square. Verified the
gate still holds: **falva -> 5,5,5 · cole -> 6,7,8**.

⚠ **Tier 8 has no art in this pack** and falls through to the L7 black — better a correct
top-tier look than a red level-5 pellet, but it is a placeholder decision and yours to change.

## 17. THE NEW ICE BREATH

The old ice breath was the **flamethrower reel hue-rotated 195 degrees** — same silhouette as
fire, just cooler. That is why it always read as flame-shaped and had to be shrunk and made
translucent in 0801ku to stop it blotting out the screen.

The new reel is drawn for the job: 8 frames, 80x192, fixed alpha mask, 75ms/frame. Only the
internal charge veins and light bands move, so the plume never crawls.

**The additive burn and core passes are skipped for it.** The pack declares
`internal_glow_only` and the handoff says outright "There is no outer glow" — the glow is
painted into the frames. Stacking two more additive copies is right for the flame plate and
wrong here: it would blow a near-white ice mass into a solid slab and undo the 0801ku
translucency fix. It still counts as ICE, so it keeps the 0801ku size and 50% alpha.

## 18. SPREAD FIRE — ART ONLY, AMOUNTS UNTOUCHED

> "do not change the output of the spread fire amounts."

All 60 frames registered (5 levels x travel/muzzle/impact x 4).

**This instruction was load-bearing.** The pack ships its own `spreadPattern` with
`shotCount` 3/5/7/9/11 for levels 1-5, and adopting it would have been the natural way to
wire the art — it is right there in the map JSON. The game fires `n = 2+lv` (2,3,4,5,6,7)
at `sprd = 0.22+lv*0.05`. Both are **unchanged and asserted**, so a later pass cannot
"align them with the pack".

## 19. LIZZIE'S FUTURE ATTACK — REGISTERED, NOT WIRED

> "you can use the regular bullets for a new attack for lizzie that'll introduce later."

Nothing wired, by design — "introduce later". The art is registered and addressable.

⚠ **Which set is "the regular bullets"?** It could be the spread pack's straight `travel`
frames, or the plain MG pellets that Cole's gold/black tiers sit above. Both are on disk and
either would work. Say which and it goes in.

## 20. A THIRD HAND-ROLLED TEST FOUND

The `topgun` flake from 0805a was **misdiagnosed by me** and the wider window only masked it.
Measured properly: through `beginStage(1)` topgun appears at **34-38s across 8 runs**, against
a boss warning at 64.4s — a 26-30 second margin, not marginal at all. The 59-65s figure came
from the test's hand-assembled stage state, the same pattern as the two tests fixed in 0805a.
It now calls `beginStage()` like the game does. Stable across 5 runs.

**The lesson is now three-for-three: any harness block that builds stage state by hand instead
of calling `beginStage()` is measuring a stage the game never starts.**


---
---

# DROP 0805e — ICE BREATH SIZE

> "Ice breath may be a little too small. should be just a little smaller than the flame
> thrower graphics."

## 21. 0801ku FIXED IT TWICE

The original complaint — *"ice breath is wayy too large of a graphic and needs to be 50%
translucent"* — was two instructions, and 0801ku applied both: it shrank the plate to
0.62 x 0.80 **and** dropped it to half opacity. The opacity was doing most of the work. A
near-white ice mass is only screen-blotting because it is OPAQUE; at 50% alpha the player
can see straight through it, so the plate never needed to be that small as well.

### Measured drawn size, against the 480-wide camera

    lv    flamethrower        ice at 0801ku       ice now
          (alpha 1.0)         (0.62 / 0.80)       (0.85 / 0.90)
    1      82 x 176            51 x 141            69 x 158
    3     132 x 228            82 x 182           113 x 205
    5     193 x 280           119 x 224           164 x 252
                              25% of screen       34% of screen

Level 5 goes from 119px back up to 164px, against the flamethrower's 193px — under it at
every level, in both dimensions, which is what "just a little smaller" asks for.

**The 50% alpha is untouched.** That is the part that stopped it blotting the screen and it
is asserted so it cannot drift while someone is adjusting size.

## 22. ⚠ AN ASPECT TRADE WORTH KNOWING

The new reel is **80x192 natively (aspect 0.417)**; the flame plate is **112x226 (0.496)**.
Because the drawn width follows the flame's FLARE and the height follows its reach, the ice
art is stretched to a slightly different aspect at each level — **0.36 at lv1 rising to 0.53
at lv5** — rather than held at its own 0.417.

Locking it to native aspect would stop that, but the flare would go with it and the plume
would read progressively NARROWER as the weapon levels up, which is backwards for a breath
weapon. Kept the flare. One constant to change if the pack's fixed silhouette matters more.

## 23. TWO PROCESS FIXES

**A duplicate `const ICE_W` was left behind** when the new one was inserted above the old.
Two `const` declarations in one block is a SyntaxError, caught immediately by `node --check`.
There is now an assertion that exactly one survives.

**`_superseded/` stopped being deleted before every zip.** The harness hard-crashes without
it and reports `1721 ok / 0 fails` — a clean-looking pass that is really a crash at section
149. That trap was hit three times this session. The stub now stays in the tree permanently
and is excluded at zip time instead, so the harness always runs and Mike never receives stub
ledgers.


---
---

# DROP 0805f — THE WRONG PROJECTILE FAMILY

> "I found the projectile problem. you've been use the wrong family the entire time.. your
> using the 1st screenshot family when it should've been the other 2 screenshot families.
> and you have to rotate some of thes attacks to be vertical. remove all flips in code, as
> we wil correct the images instead."

He is right, and it is the second-path problem again — the same shape as the MG pellet
colours in 0801b and the boss draw path in 0805a.

## 24. THREE FAMILIES, AND THE WRONG ONE WAS WINNING

    nep_ / nbp_    126 keys   the CF_EnemyArsenal per-stage grid     <- was drawing
    mfx_*          133 keys   pellet/flare/comet/blast/homing/missile
                              the six kept in 0801hj, via FIRETYPES  <- should draw (enemies)
    bfx_*_p         72 keys   12 bosses x 6 animated frames          <- should draw (bosses)

The arsenal block ran first and returned — its own comment said so outright: *"This runs
BEFORE the old FIRETYPES path, so the arsenal wins wherever it has art."* It had art for
126 of 126 stage/slot combinations, so **FIRETYPES never executed**. Every palette, spin,
glow and derived type in it was dead code, and 0801ki's careful slot-mapping work was
tuning a family that should not have been on screen at all.

**bfx_ was never drawn once.** Measured: the string `bfx_` appeared exactly ONE time in
game.js, inside a comment. 216 keys registered — 12 bosses x {projectile, muzzle, impact} x
6 frames — completely orphaned. All twelve bosses fired the same anonymous per-stage round.

### After — measured, by recording real draw calls

    stage 1-4 enemy bullets:   mfx_ only, ZERO nep_ draws
    boss bullets:              bfx_magma_p, bfx_cryo_p, bfx_warhawk_p, bfx_rampart_p,
                               bfx_storm_p, bfx_toxic_p — each boss firing its own ammunition

Mapped off the **mech tag, not the stage**, because a boss owns its ammunition — Magma's
fireball should look like Magma's fireball wherever it is fought. `nep_`/`nbp_` stay
registered and unconsulted; deleting 126 keys is Mike's call, not a side effect.

## 25. THE PELLETS WERE AUTHORED SIDEWAYS — AND THREE CALL SITES DISAGREED ABOUT IT

Measured ink orientation of every live projectile family. **Only `mfx_mg` was horizontal** —
aspect 2.0 to 2.7, head on the right, 25/25 consistent. Every bfx_ plate and every other
mfx_ family was already vertical.

Worse, three call sites each assumed a *different* authored facing for those same 25 files:

    FIRETYPES align   ang = atan2(vy,vx) - PI/2   assumes the art points DOWN
    coleTriDraw       ang = atan2(vy,vx) + PI/2   assumes the art points UP
    player MG draw    ang = -PI/2                 assumes the art points RIGHT

Only the third matched the art. So **enemy pellets drew sideways** — which is exactly
*"all enemy projecticles are verticle unless its a ball"* going unmet — and Cole's homing
trident drew 180 degrees out, tail first.

### Fixed in the images, per instruction

The 25 plates are rotated 90 clockwise on disk so the head points DOWN — the direction
`align` already assumes and the direction an enemy round travels. Verified after: ink aspect
flipped to 0.53 and the bright head sits at the bottom, **25 of 25**.

Then the two code-side compensations that existed only to work around the bad authoring were
removed: the player MG's `-PI/2` became `PI` (art points down, a player round goes up), and
`coleTriDraw`'s `+PI/2` became `-PI/2`. `FIRETYPES align` is **untouched** — the art was
moved to match the convention, not the other way round.

Originals backed up to `assets/fx/_preroll_0805f/` before rotating, and the rotation reads
from that backup rather than from the file it writes — the clobbering rule from the flame
generator.

## 26. ⚠ THE OTHER FLIPS — NOT TOUCHED, AND WHY

"Remove all flips in code" was read as scoped to the projectiles, because the codebase has
16 `ctx.scale(-1..)` calls and most are nothing to do with attacks — snow plumes blowing
outward, terrain tiles mirrored to hide repetition, the stage-6 fire wave, gib scatter.
Removing those would break unrelated art.

There is, however, a real cluster of the *same class* of bug still present — art authored
facing away, compensated at draw time:

    b._flipY          sub-boss and assigned units      lines 5440, 5452, 5571, 23107
    _facesDownNatively enemy sprite facing             line 13194
    D.flip            drone facing                     line 19827
    ASSIGNED_FLIP     the table driving _flipY

**Say the word and those get the same treatment** — rotate the source art 180, delete the
compensation. It is the same fix, just wider, and it wants doing in one pass with a proof
sheet rather than piecemeal.

## 27. STILL OPEN

* The three flip clusters above.
* The 3-5s miniboss cinematic — still needs its CONTENTS.
* Which set is "the regular bullets" for Lizzie's future attack.
* Cole tier 8 has no bullet art (falls through to L7 black).
* Furious fodder reaching 10-11 shots.
* `NEWBOSS` dead code; the nine-drop back-port.


---
---

# DROP 0805g — OLD PROJECTILES DELETED, AND THE PALETTE ANSWER

## 28. CAN HTML5 PALETTE-SWAP LIVE? YES — AND IT IS ALREADY IN THE BUILD

No separate frames are needed for recolours. `nuoTinted()` takes ONE greyscale orb and
produces every pilot colour at runtime.

### ⚠ BUT MY FIRST VERSION WOULD HAVE FAILED SILENTLY ON MIKE'S MACHINE

It used `getImageData`. Chrome treats **every local file as its own origin**, so reading
pixels back from a canvas that has had a `file://` image drawn into it throws SecurityError
unless the browser was started with `--allow-file-access-from-files`. This game ships as a
`file://` page. The `catch` returned null, the caller fell back to untinted — so **Axel's orb
would have rendered grey, not royal blue**, and nothing would have reported it.

The codebase already knew this (`xartDeKey` and `flamePair` carry the same warning from
0801bl), which makes it worse, not better: the lesson was written down and I did not read it.

Rewritten with compositing, which never touches pixel data and has no origin rules:

    1. draw the grey source
    2. 'multiply' a flat tint      grey x colour keeps the authored shading
    3. 'destination-in' the source restores the true alpha
    4. 'lighter' the source @0.34  lifts the specular core back out of the tint

Verified by simulating the exact chain offline. Asserted that the orb tint contains no
`getImageData`.

### The three options, cheapest first

    ctx.filter = 'hue-rotate(..) saturate(..)'   GPU, one line, but shifts everything crudely
    composite multiply + destination-in          no pixel reads, file:// safe   <- used here
    getImageData + luminance ramp                finest control, DOES NOT WORK from file://

## 29. THE OLD PROJECTILES ARE GONE

112 of the 126 `nep_`/`nbp_` keys deleted, files removed, `BOFPI` ink rects pruned 126 -> 14,
**1.52 MB** freed.

The kill list ran through a guard against `PROTECTED_ASSETS.json` and it fired: the fourteen
**stage-9** plates (`nep_9_*`, `nbp_9_*`) are on the protected list as planned content and
were held back. Stage 9 is not in `STAGES[]` yet and its wiring is outstanding, so those keys
stay until that lands — flagging it, since the draw path that used them is now gone.

## 30. THE FOLDER — MEASURED, AND WHY I DID NOT MASS-DELETE

    images on disk        9,812   (9,803 PNG + 9 JPEG)
    disk, compressed        435 MB
    total pixels            723 Mpx
    DECODED RGBA in RAM   2,891 MB   <-- the number that actually matters

**2.9 GB** is what the browser would hold if everything were resident. It only works today
because of lazy `XART._touch` and stage-scoped `warmStage`. That is the real cost, not disk.

The memory is also SPREAD, not concentrated — the top 50 images are just 15% of it, the top
1,000 are 52%. Thousands of small decodes, which is exactly the case atlases fix.

### ⚠ AN AUDIT I RAN AND THEN THREW AWAY

A family-prefix reference scan reported **4,871 keys / 174 MB unreferenced**. It was WRONG.
It flagged `mbg2_rot_left-cannon-forearm` (built dynamically by `mechAimCannons`) and
`lvl1_master` (built by `_levelCfg`) as dead. Any key assembled from string fragments at
runtime looks orphaned to a grep. **Deleting on that basis would have destroyed working art**,
so nothing was deleted on it and the number is recorded here only as a warning.

### What palette-swapping actually saves

Measured properly — same alpha silhouette AND same luminance structure, i.e. a genuine
recolour rather than an animation frame:

    true palette variants   2,309 keys in 665 groups
    disk recoverable         10.2 MB

Only 10 MB, because the bulk of 435 MB is large unique art, not colour variants. The win is
**key count** — 2,309 keys collapsing to 665 — which is decode calls and Image objects, not
megabytes. Mostly UI bar fills (`nbb_fill`, `nui_fill`, `nsb_speed`, `nmb_fill`).

## 31. RECOMMENDED ORDER — NOT YET DONE, NEEDS A GO

1. **Collapse the 665 recolour groups** to one master + runtime tint. ~1,650 fewer keys.
   Lowest risk: they are UI fills, and the tint path is proven.
2. **Atlas the small sprites.** Thousands of <64px plates into a handful of sheets with an
   offset table. Cuts decode calls hard; needs a `drawImage(sheet, sx,sy,sw,sh, ...)`change at
   each call site, which is mechanical but wide.
3. **Then re-audit orphans PROPERLY** — instrument a real playthrough and record every key
   `XART._touch` actually requests, per stage. That is measured truth, unlike a grep, and it
   is the only safe basis for mass deletion.


---
---

# DROP 0805h — SHIP BANKING, AND THE FIRST PALETTE COLLAPSE

## 32. THE INVERTED TURN — MEASURED, AND IT WAS TWO BUGS, BOTH COLE'S

> "some characters you have them turning right when we twist left and turning left when we
> twist right."

Measured the signed horizontal centroid of every bank frame against its own neutral (pv2),
for all nine pilots. Mirror IoU between pv0 and flipped pv4 is 0.88-0.97 across the board, so
the frames are genuine opposing pairs and the measurement is trustworthy.

**Defect 1 — Cole's frames were scrambled.** Eight pilots read (pv0,pv1) one way and
(pv3,pv4) the other. Cole alternated:

    axel     + +  - -     consistent
    cole     - +  - +     SCRAMBLED
    falva    - -  + +     consistent

`pv1` and `pv3` were swapped in the files. Swapped back on disk; he now reads `- - + +` like
everyone else. Originals in `assets/ships/_preswap_0805h/`.

**Defect 2 — he was in `SHIP_BANK_FLIP` and should not have been.** Measured pv4 lean:

    LEAN LEFT  (authored reversed, needs the flag) : axel, decker, freezer, yuri
    LEAN RIGHT (authored normally, no flag)        : cole, falva, juggernaut, lizzie, maverick

Cole leans RIGHT — the normal convention — so the flag was inverting a pilot that was already
correct. That is precisely the reported symptom. Removed; the other four match the
measurement and are untouched.

## 33. CLIPPING — IT IS NOT COLE

Checked every frame of all nine ships for ink touching the canvas edge. Canvas sizes are
internally consistent per pilot (Cole is a uniform 226x271 across all five).

    falva  pv2   152x280   ink x 0-151   LEFT + RIGHT edge
    lizzie pv2   222x280   ink x 0-221   LEFT + RIGHT edge

Those two neutral frames run wingtip-to-wingtip with zero margin, so the tips are cut in the
SOURCE art. **Cole did not flag on this test at all.** Rather than guess at what is wrong with
his, I need to know what you are seeing — clipped in flight, on the select card, or during a
roll — because those are three different draw paths.

## 34. RETINA — 72 KEYS BECOME 8

> "the retinas colors are - yuri/red axel/blue cole/neon green decker/yellow
> juggernaut/orange lizzie/gold falva/pink freezer/purple maverick/forest green"

Measured first: the nine sets are **pixel-identical in silhouette** — alpha IoU 1.000 for
every pilot in both retA and retB. Never different art, only different colour.

And two did not match the brief anyway:

    cole        ( 48, 48, 48)   GREY, not neon green
    juggernaut  (116, 95, 82)   BROWN, not orange

72 keys collapsed to **8 greyscale masters**, built by averaging all nine sets (cancels any
one pilot's colour cast) and normalising luminance 2-98% so the tint gets full range. Tinted
through the same compositing path as the helper orb — no `getImageData`, so it survives
`file://`. **2.28 MB freed, 72 files deleted.**

⚠ A tinted plate is a **canvas**, which has `.width` but no `.naturalWidth`. All four retina
draw sites used `naturalWidth` and would have scaled by NaN. Caught and fixed at each.

## 35. MAVERICK'S HULL — FOREST GREEN

Measured his ship at hue **97 degrees** — a yellow-green, not forest. Shifted the saturated
hull pixels to **134 degrees** and deepened lightness 7%, leaving unsaturated metal, cockpit
and canopy untouched so the panel detail survives. All 17 frames; originals in
`assets/ships/_prehue_0805h/`.

## 36. ⚠ WHAT I DID **NOT** GET TO — AND WHY IT IS NOT STARTED

Being explicit rather than leaving these looking done:

* **The single missile graphic + per-fighter tip/middle tint.** Not started. It is the same
  pattern as the retina and should go the same way, but the missile art needs the same
  silhouette-identity check first — if the nine missiles are NOT one shape, a single master
  changes their read, and that is a design decision.
* **Thruster glow / animation on all ships.** Not started. This is the biggest single item on
  the list and it is not a palette job — it needs the thruster pixels identified per hull
  (there is already a `thruster_rig.html` covering 147 units) and an animated glow pass.
* **Ship / jet atlases.** Not started.
* **Weapon-level and projectile-family atlases.** Not started.

**On the atlas question specifically:** they are worth doing, but for decode count, not disk.
The measurement from 0805g stands — 9,754 keys, 435 MB on disk, **2.9 GB decoded**, and the
top 50 images are only 15% of it. The cost is thousands of small decodes, which is exactly
what an atlas fixes. The work is mechanical but WIDE: every `drawImage(im, ...)` call site
becomes `drawImage(sheet, sx,sy,sw,sh, ...)`. It wants doing one family at a time with the
harness green after each, not in one sweep.


---
---

# DROP 0805i — COLE'S SONIC BOOM + LIZZIE'S HEAVY MG

CF_LizzieColeSpecialWeapons-Vol.3 installed: 22 keys, 0 broken paths, verified hard alpha
(0 partial-alpha pixels) and no magenta across all 22 before wiring.

## 37. NEITHER SPECIAL WAS TOUCHED

Worth stating first because it would be the easy mistake: **Cole still has NUKE STRIKE and
Lizzie still has ATOM BOMB.** `startSpecial()` is not changed by a line. These are WEAPON
pickups that sit alongside the special — "He now gets his nuclear warhead like before, but
when he picks this box/icon up..." Asserted both ways.

## 38. COLE — SONIC BOOM

Built from the pack's own three layers rather than one sprite, because that is what makes it
read as sound rather than as a bullet:

    nsw_ring_0..3    the damaging front, 30 -> 90px of ink across four frames
    nsw_circ_0..3    a one-shot compression pulse at the muzzle, does not travel
    nsw_dist_0..3    the translucent distortion, LEFT BEHIND at 50% on 'lighter'
                     (the pack's own recommendedOpacity and its own blendMode note)

The distortion is deliberately **dropped as a trail** — a plate is parked at the wave's
position every 60ms and fades in place while the wave races on at 9.2px/frame. A wave that
carried its distortion along would just look like a bigger sprite; leaving it behind is what
makes the air look disturbed after the boom has passed.

Measured in play: 367 wave samples in the air over 3s, **11 distortion plates parked**, and
`nsw_ring_*`, `nsw_circ_*`, `nsw_dist_*` all confirmed drawing.

## 39. LIZZIE — HEAVY MG MOUNT, AND A REAL 50/50

The crate rolls a literal coin. Measured over 6,000 rolls: **2,004 / 1,996**.

The mount flies in on an **arc** rather than a straight line, so it reads as swinging round to
the front the way Mike described, and shrinks 1.0 -> 0.38 on the way ("this attachment would
scale dow"). It docks at the pack's own `mountAnchor` [80,156] — bottom-centre, the end that
meets the hull, which is what makes it *connect* instead of overlap.

Docked, she fires **heavy slugs**: 6 damage against a base pellet's 2, at a 0.16s cadence from
two barrels. A mounted gun trades rate for weight — deliberately not a faster pea-shooter.

Every other pilot's crate is unchanged and still yields `specialicon`.

## 40. ⚠ A REAL BUG THE SUITE CAUGHT — STALE PICKUP STATE

The Lizzie assertion failed with **zero slugs fired**, and the cause was not the test.

Both new weapons replace the primary inside `pShoot` and return early. Neither `run.sonicT`
nor `lzMount` was being reset on a new run or a new stage — so a sonic timer left over from a
previous run **silently suppresses the next pilot's gun entirely**. In the suite a Cole test
set `run.sonicT` and the Lizzie block after it fired nothing at all.

Cleared in both `beginStage()` and the new-run reset. That is a bug that would have shipped as
"my gun stopped working after I died" and been very hard to trace.

## 41. A FLAKY ASSERTION FIXED (pre-existing, not a regression)

`atomBooms` secondaries asserted a stagger `> 0.7s` and failed about 1 run in 3. It sits on
the tail of its own generator: scattered pops take `t = 0.28 + rnd(0, 0.9)`, so with eight
draws the largest is usually ~0.8 but can land near 0.5, against a fixed earliest pop of
~0.235. Threshold moved to 0.45, which still proves the intent ("one by one, not all at
once") while sitting clear of the tail. **A flaky assertion is worse than a loose one — it
trains you to ignore red.**

## 42. ⚠ WHAT I DID **NOT** DO FROM THIS BRIEF

Four of the six items are untouched. Saying so plainly rather than letting them look done:

* **Thrusters angled and anchored per rotation frame, animated.** NOT STARTED. This is the
  single biggest item on the list. It needs the thruster pixels located per hull per bank
  frame — `thruster_rig.html` already covers 147 units and is the right starting point — then
  an anchored, angled glow pass per frame. It is a drop of its own.
* **Per-character ship/jet atlases.** NOT STARTED.
* **Pickup / special icon / box / pill atlas.** NOT STARTED.
* **UI stages 6-9 sorted onto the atlas and wired.** NOT STARTED, and it is the one I know
  least about — "this was never done or wired up" means there is no existing pattern to
  follow, so it needs a look at what stage 1-5 UI actually does before anything is built.

The atlas measurement from 0805g still stands and still argues for doing them: 9,776 keys,
**2.9 GB decoded**, top 50 images only 15% of it. But every `drawImage` call site changes, so
it wants one family at a time with the harness green after each.


---
---

# DROP 0805j — THE PER-FRAME THRUSTER RIG

> "the thrusters were trying to use look yanky ... take each characters rotational patterns and
> try to angle and anchor the thrusters to each frame and animate them properly."

## 43. WHY IT LOOKED YANKY — MEASURED, ACROSS ALL 153 SHIP FRAMES

The plume was placed from **two per-PILOT constants** — `_NZ` (nozzle offset) and `_HB` (hull
bottom) — and drawn with **no rotation at all**. But a ship has seventeen frames and its tail
moves in every one of them. Measured nozzle travel within a single pilot's own bank set:

    lizzie   anchor x 0.324 -> 0.677   0.354 of canvas width   ~78 px
    yuri     anchor x 0.362 -> 0.631   0.269                   ~64 px
    cole     anchor x 0.467 -> 0.525   0.058                   ~13 px

and the airframe's own axis swings by up to **+/-17.8 degrees** while the plume stayed bolted
vertical. So on the worst frames the flame sat ~78px sideways of the engine and 18 degrees out
of line with the hull. **No amount of tuning one offset could fix that** — the number had to be
per frame. That is the jank, in numbers.

## 44. THE RIG

`SHIP_THR` carries, for all nine pilots and all seventeen frames, measured from the art:

    x, y   the tail centroid as a fraction of the canvas
    a      the airframe axis in radians, from the ink centroid of the frame's top quarter
           to that of its bottom quarter — 0 means straight down the canvas
    m      nozzle offsets from the spine

5.7 KB of table. Verified in play: Cole's anchor tracks **0.399 -> 0.495 -> 0.596** as he rolls
left/level/right, Axel tilts **+/-7.1 degrees**, and twin-engine pilots draw two plumes while
single-engine pilots draw one.

### ⚠ TWO THINGS I GOT WRONG AND THE SUITE CAUGHT

**First: I re-derived the nozzle mounts and picked up wingtips.** My lobe detection returned
`cole/pv2 = -0.4309` — out at the wing, not either side of the spine. That is *exactly* the
mistake the 0724co note warned about ("what my first two detections kept catching"), and the
assertion inherited from that drop failed on my data immediately.

**Second: constraining it then lost four of the five twin-engine pilots.** The right answer was
to stop re-deriving what was already correct — the `_NZ` twin spacing was measured and verified
in 0724co, so it is kept verbatim. This drop contributes the per-frame **anchor and angle**,
which is what was actually asked for, and nothing else.

## 45. ONE FUNCTION NOW OWNS THE FRAME CHOICE

The hull picked its frame with an inline chain and the thruster had no way to know which frame
was on screen — which is *why* they could drift apart in the first place. Both now call
`_shipFrameKey()`. They cannot disagree by construction.

## 46. THE PIXELS GLOW AND MOVE

> "make thruster pixels glow and transform to appear moving on all ships"

The reel already advanced four authored frames; what it lacked was life between them, so at low
throttle it read as a static cone. Three cheap things off one clock:

1. **Length breathes** with throttle plus a fast flicker — a rigid plume is most of what reads
   as fake.
2. **A hot core** is drawn over it, shorter and narrower, on `lighter` — the glow comes from
   the plume's own pixels, not an invented sprite.
3. **The core runs on a different clock** from the body, so the inside appears to travel down
   the flame while the outline holds. Motion without new frames.

## 47. STILL OPEN

* **Per-character ship/jet atlases** — not started.
* **Pickup / icon / box / pill atlas** — not started.
* **UI stages 6-9 sorted and wired** — not started, and still the one with no existing pattern
  to copy.
* **Enemy thrusters** are untouched. `drawThruster(e)` still pastes a generic `nthr_` reel at a
  fixed `-e.h*0.30` offset with no per-frame anchor — the same bug this drop just fixed for the
  player, on every enemy that uses it. The rig approach transfers directly.
* falva pv2 and lizzie pv2 are still edge-clipped in the source art (0805h §33), and Cole's
  clipping still needs a description of what you are seeing.


---
---

# DROP 0805k — 246 JET FRAMES THAT HAD NEVER BEEN ON SCREEN

Went to give the enemy thrusters the same per-frame rig the player ships got, found the
enemies they belong to were not drawing at all.

## 48. THE LEVEL-6 JET PACK WAS DEAD CODE

`drawThruster` has exactly one caller — `drawL6Jet` — and `drawL6Jet` returned false on every
call, so neither the jets nor their engines had ever been drawn.

`_l6frames` was corrected in **0801gf**: wrong prefix, wrong ship codes, wrong state names, all
three. But the correction stopped at the COUNTER. The line that actually fetched the image kept
every original mistake:

    prefix       n6j_          not one n6j_ key exists; the pack ships as n6x_
    ship code    e._h6         the roster key 'talon', where the art uses 'st'
    state name   death/launch  where the art uses die/hom

So `_l6frames` counted a real reel and returned a frame count, the guard above passed, and then
`XART.get` looked up a key that could not exist. `im` came back undefined and the function bailed.

**246 registered keys — six jets x seven states — invisible.** Same shape as `bfx_` (0805f) and
`NEWBOSS` (0805a): the count and the fetch built their keys independently and disagreed.

Both now go through one `_l6key()`. Verified after: all six jets resolve all seven states, and
`drawL6Jet` returns true drawing airframe **and** thruster for talon, fang, widow, raptor, lance
and warden.

## 49. THE ENEMY PLUME WAS A BODY-LENGTH OUT OF PLACE

It drew from `-e.h*0.30` — thirty percent **above** the entity centre — and ran downward, putting
the flame over the middle of the airframe.

Measured the real tail across all 246 frames: the ink ends at **0.833 to 0.870** of canvas
height, tightly clustered. The jet draws at `e.h*1.5*pScale` centred on the entity, so its tail
sits at **+0.36** of that height below centre, not 0.30 above it. The plume was roughly
**0.84 of a body-length** out of position. Now anchored at the measured tail and flipped so the
wide end meets it, same as the player ships got in 0801fp.

## 50. A RIG I MEASURED AND THEN DID NOT BUILD

I expected these jets to need per-state anchors the way the player ships did, and measured all
246 frames per state to build the table. **They do not need it.** Anchor x is 0.497 and the axis
~0 degrees for `bl`, `idle` AND `br` on every one of the six — their banked frames move the
wings, not the tail.

So there is no `L6_THR` table. It would have been 1.2 KB of data that changes nothing, and the
real fix turned out to be a single measured constant. The player ships genuinely needed the rig;
these genuinely did not. Recording it because "measured, found unnecessary, did not ship" is a
result worth keeping — the next person to look will otherwise measure it again.

## 51. STILL OPEN

* Per-character ship/jet atlases; pickup/icon/box/pill atlas; UI stages 6-9 sorted and wired.
* falva `pv2` and lizzie `pv2` are edge-clipped in the source art (0805h §33).
* **Cole's clipping still needs a description** — measurement says he is NOT edge-clipped, so
  I need to know whether you see it in flight, on the select card, or mid-roll.


---
---

# DROP 0805l — THE STAGE 1-9 BOX + PILL ATLAS

## 52. FIRST, A CORRECTION: STAGES 6-9 WERE ALREADY WIRED

"this was never done or wired up" is half right. `drawCrate` has read `nlc6-9` since drop 0720
and `npup6-9` draw for speed/shield pickups. What never happened is the **folder move** — the
set sat split across `ui/stageboxes/` and `pickups/pills/` while `items/` and
`ui/minibosspills/` were both empty. The atlas supersedes the folder question entirely.

## 53. THE ATLAS — AND TWO FAILED ATTEMPTS BEFORE IT WORKED

**Attempt 1, uniform grid at source resolution: 36.5 MB decoded against 10.7 MB for the 45
separate files.** Far worse. Cells run from 139x170 to 480x396, so a grid sized for the largest
wastes most of the sheet.

**Attempt 2, tight shelf pack of the trimmed art, width searched from 600 to 2400: still
+9.9%.** The trimmed ink is 2.63 Mpx against 2.68 Mpx of raw canvas — these sprites already
fill their canvases, so trimming recovers 2% and packing overhead eats it.

**What was actually wrong was resolution, not packing.** `drawCrate` scales to 46px and
`drawCapsule` to ~49px, while the source art runs to **480px** — about ten times the size it is
ever drawn at. Nobody had compared the draw scale against the stored scale.

Packed at 96px — still double the drawn size, so there is headroom for a hi-dpi pass later:

    decoded RAM   10.71 MB  ->  1.36 MB     7.9x less
    disk           5610 KB  ->   773 KB     7.3x less
    decode calls        45  ->  1

Sheet is 496x683. Cells keep their own rect rather than being stretched to a grid.

## 54. THE SET IS NOW COMPLETE FOR ALL NINE STAGES

    boxes   1-5  crate1 / crate2b / crate3 / crate4 / crate5      4 frames each
            6-9  nlc6 / nlc7 / nlc8 / nlc9                        4 frames each   = 36
    pills   1-5  pill1 / pill2 / pill3 / pill_missile / pill5
            6-9  npup6 / npup7 / npup8 / npup9                                    =  9

Before this, stages **7, 8 and 9 had no themed capsule at all** — `drawCapsule` fell through to
`pill_speed` for anything past stage 6. Folding `npup7-9` into the pill row closes that.

Verified per stage: all nine draw both box and pill out of the sheet, 45/45 cells resolve, and
a proof sheet of every cell is attached. The 45 source files are deleted and de-registered;
manifest is down to **9,732 keys**.

## 55. WHAT THIS SAYS ABOUT THE REMAINING ATLASES

The 0805g measurement said 2.9 GB decoded across the library and pointed at atlases. This drop
shows the headline number there is probably **not packing at all — it is that art is stored far
larger than it is ever drawn**. Worth auditing draw-scale against stored-scale across the whole
library before building any more sheets; that is where the 7.9x came from here, and packing on
its own would have made things worse.

## 56. STILL OPEN

* Per-character ship/jet atlases; the pickup/special-icon atlas.
* falva `pv2` / lizzie `pv2` edge-clipping, and **Cole's clipping still needs a location** —
  in flight, on the select card, or mid-roll.


---
---

# DROP 0805m — THE DRAW-SCALE AUDIT: 308 MB RECOVERED

Acting on 0805l's own conclusion — that the box/pill 7.9x came from resolution, not packing —
and asking the same question of the whole library before building any more sheets.

## 57. THE PROBE

`probe_drawscale_0805m.js` drives all nine stages and records, for every `drawImage`, the DRAWN
rectangle against the STORED rectangle.

⚠ **`drawImage` has three signatures and the older probes only handled one.** On a nine-argument
call, arguments 4 and 5 are the SOURCE rect — reading those would have made every atlas blit
look perfectly sized and hidden the exact thing the probe exists to find. `arguments.length` is
the only safe discriminator.

First pass: **441.7 MB observed across 1,393 keys, with 359 keys stored 4x or more above their
drawn size.**

## 58. THE BIG ONE — BOSS FX PLATES AT 60-90x

    mb*_mflash_0..5  and  mb*_impact_0..5     144 plates, every one 512x512
    drawn at                                  54px (impact, fixed) / 64.8px (mflash, worst)

`impact` is a hard-coded `h=54`. `mflash` is `54*S*1.6` where `S=(b.w||352)/384`, and measuring
every boss puts them all at `b.w=288` — so the worst case in the entire game is **64.8px**.
Against a 512px plate that is a **60 to 90x** oversize.

Capped at 128 — exactly 2x the worst draw, the same rule that worked on the box/pill sheet:

    decoded   151.0 MB  ->   9.4 MB     16.0x less
    disk         6.4 MB  ->   0.8 MB

**141.6 MB recovered from 144 files.**

## 59. THE SECOND TIER

294 more keys capped at 2x their own measured draw — mostly the `nxp_` explosion reels, which
are soft additive FX and very forgiving of downscaling. **39.4 MB more.**

Deliberately skipped: the 19 `mb*_rot_*` cannon frames. Crisp mechanical art, about 1 MB each,
and softening the barrel-tracking frames to save that is a bad trade.

## 60. ⚠ WHAT THE RATIO METRIC LIES ABOUT

Two categories look like the worst offenders and must never be touched:

* **Scrolling level masters.** `nst2_master` is 800x4800 drawn 800x512 — a "9.4x ratio" that is
  not waste at all, because the whole strip is consumed as the level scrolls. Shrinking one
  would wreck its stage. Excluded, and an assertion now fails if any master's height drops
  below 1500.
* **Atlases.** `nba_boxpill` reports a "150x ratio" because each blit is one small cell. The
  sheet is doing exactly what it should.

Both are excluded by rule, not by hand.

## 61. THE NUMBER

    library decoded RGBA     2,891 MB  ->  2,583 MB
    the 432 rescaled plates    214 MB  ->     39 MB
    disk                       435 MB  ->    416 MB
    images                      9,812  ->    9,726

**308 MB of decoded RAM recovered this session**, none of it from packing.

## 62. STILL OPEN

* `nxp_fall`, `nxp_roll` and `nxp_upward` (24 plates at 384px) never drew in a full nine-stage
  run and sit in no size bucket in `fxBurst`. **No measurement means no cap** — asserting a
  number I have not measured would be inventing one. Either they are dead and can go, or
  something triggers them that a driven run does not reach. Worth a look.
* 515 keys are still stored at 2x or more of their drawn size (184 MB). The 2x rule is
  conservative on purpose; a 1.5x pass would recover more if you want it.
* Per-character ship/jet atlases and the pickup/special-icon atlas — and on the evidence here,
  **audit their draw scale first**; packing alone made things worse every time it was tried.
* falva/lizzie `pv2` clipping, and Cole's clipping still needs a location from you.


---
---

# DROP 0805n — THE THREE UNMEASURED EXPLOSION REELS

Chasing the one item 0805m left explicitly open: 24 plates at 384px that never drew in a full
nine-stage run. Every previous "registered but never drawn" family this session turned out to be
a bug — `bfx_`, `NEWBOSS`, the 246-key `n6x_` jet pack. **This one is not.**

## 63. nxp_fall AND nxp_roll ARE UNUSED ON PURPOSE

`DEATH_CLASS` documents it plainly. Both are SIDE-VIEW art with a built-in gravity direction —
`fall` measures 0.38 aspect (a tall column dropping) and `roll` 1.66 (a wide horizontal sweep).
In a top-down shooter there is no down or sideways on screen, so both read as a stray effect
pasted over the unit rather than an explosion coming out of it. Neither is assigned to any
death class, deliberately.

So: not a bug, and nothing to fix. Worth having chased it — the same shape has been a real bug
three times this session, and the only way to tell them apart is to look.

## 64. nxp_upward IS WIRED — MY PROBE JUST NEVER KILLED A BOAT

`DEATH_CLASS.boat` uses it. The 0805m probe drove all nine stages but never happened to destroy
a boat-class unit, so the family recorded zero draws and I could not cap it.

Fixed by driving the DEATH CLASSES directly through `killEnemy` — boat, mboat, crate, drone,
turret, jet, tank — rather than hoping a playthrough produces one of each. Verified the
classifier first: `barge` and `skiff` resolve to `boat`, `microturret` to `turret`, `racer` to
`jet`, `jungletank` to `tank`.

**And they all draw at exactly the same size: max 113x113, every family.** So the set takes ONE
cap instead of nine separate guesses:

    all 80 nxp_ plates capped at 256   (2.26x the measured 113px)
    decoded  47.2 MB -> 21.0 MB

`fall` and `roll` are capped too. They are spares, but a spare at 384px costs exactly as much
RAM as a used one.

⚠ Note: this pass re-derived from the ORIGINAL backups rather than resampling already-resampled
files, so a few plates the 0805m stage-run had capped near 200px are now 256. That is
deliberate — 113px measured from real deaths is a better number than ~100px inferred from a
playthrough that never triggered half the classes — and it costs a little RAM to be correct.

## 65. WHERE THE LIBRARY STANDS

    images            9,812  ->  9,726
    disk             435 MB  ->  415 MB
    decoded RGBA   2,891 MB  ->  2,577 MB      314 MB recovered

## 66. STILL OPEN

* **`nxp_fall` / `nxp_roll` are 16 plates of art that will never be drawn** by the current
  design. Capped, so they are cheap now, but they are still dead weight — your call whether
  they go or stay as spares.
* 515 keys remain at 2x or more of their drawn size. The 2x rule is deliberately conservative.
* Per-character ship/jet atlases and the pickup/special-icon atlas — audit draw scale first.
* falva/lizzie `pv2` clipping; Cole's clipping still needs a location from you.


---
---

# DROP 0805o — DELETING nxp_fall / nxp_roll, AND THE WARNING THAT NEARLY STOPPED IT

Mike: "delete". Straightforward — except the suite refused, and it was right to make me look.

## 67. THERE WAS A LANDMINE HERE, LEFT BY A PREVIOUS PASS

Deleting the 16 plates turned four assertions red, two of which read:

> `nxp_fall_0` was KEPT — the suite failed without it, so something reaches it that no static
> scan sees

That assertion exists because of drop **0724dq**: an asset sweep passed **1,751 assertions** and
then threw **4,000+ missing-asset errors in Mike's browser**. The conclusion recorded at the
time was exactly right — *"the suite exercises far fewer draw paths than a real frame does, so
green was not the same as safe"* — and these two families were put on a do-not-remove list so a
future pass would not try again.

I was that future pass. So rather than overriding it, I checked why it was there.

## 68. WHAT THE CHECK FOUND

**The four red assertions are all COUNT assertions**, not draw paths: "all 10 explosion sets at
8 frames", the two keep-list entries, and my own 80-plate count from 0805n. Nothing in the suite
actually reaches the art.

**DEATH_CLASS assigns neither family to anything**, and documents why: both are side-view art
with a baked gravity direction — `fall` at 0.38 aspect (a column dropping), `roll` at 1.66 (a
horizontal sweep) — which cannot read in a top-down shooter. They are also absent from
`EXPLODE_FILL`, the eight-entry scale table.

**And every dynamic explosion path is already readiness-guarded**:

    drawShockRings    if(!XART.rdy(k)) continue;
    liquid falls      if(!fam || !XART.rdy(fam+'_0')) return;

A family that is gone is **skipped**, not drawn as a broken image. That guard is the thing the
0724dq sweep did not have, and it is what turns "probably safe" into "cannot error".

Deleted: **16 files, 16 keys, 445 KB**. Their backups were removed too, so the tree keeps no
stale copy.

## 69. VERIFIED THREE WAYS, NOT ONE

Given the history, the suite alone was not treated as sufficient:

1. **Static** — zero references to either family name anywhere in `game.js`.
2. **Runtime** — a full nine-stage driven playthrough plus every death class through
   `killEnemy`: 1,312 keys observed drawing, **zero** touching either family, no load errors.
3. **Integrity** — 9,716 manifest keys, **0 broken paths**, and a new assertion that every
   family `DEATH_CLASS` names still resolves, so removing a family that IS used would fail loudly.

The keep-list still protects the other five entries (`fx_lava_0`, `nmb_fill_1_0`,
`nwx_rainD_0`, `n6e_sky_cf_crit`, `mfx_bshot_0_0`) — nothing was learned about those and they
stay exactly as they were.

## 70. STILL OPEN

* 496 keys remain stored at 2x or more of their drawn size (179 MB). The 2x rule is
  conservative on purpose.
* Per-character ship/jet atlases and the pickup/special-icon atlas — audit draw scale first.
* falva/lizzie `pv2` clipping; Cole's clipping still needs a location from you.


---
---

# DROP 0805p — THE ICON ATLAS, AND AN ALIAS TRAP THAT CAUGHT ME

## 71. FIRST: THE DRAW-SCALE THREAD IS EXHAUSTED

Re-running the audit after 0805n, the remaining safe candidates total **5.1 MB** — down from
the 141.6 MB and 39.4 MB of the previous two passes. The big wins are done. Reporting that
rather than chasing the tail: the largest remaining entries are the `mbg2_rot_*` cannon frames
(540x540 drawn at 258x258), which are deliberately left crisp.

Ships were checked before considering an atlas for them: `ship_axel` is 90x120 drawn at 45x60.
**Ship art is already correctly sized** — an atlas there would be for decode count only, not RAM.

## 72. THE ICON ATLAS

The other half of "an atlas sheet for all pickup and special icons, boxes, pills" — boxes and
pills went in 0805l.

Measured first, per the 0805l lesson. The HUD weapon icon draws at `isz = ch*0.072`, about 33px
on a card and 36px in play, while `micon_` plates are stored **160x160** and `spicon_` around
**204x232**. Roughly 20x oversize, the same disease as the boxes. Packed at 96px:

    decoded  5.63 MB -> 1.75 MB    3.2x less
    disk     1629 KB ->  891 KB
    decodes       57 -> 1

`iconDraw()` takes the same key string the call sites already build and blits the cell. An
unknown key returns null and the caller's own XART path runs unchanged, so the sheet cannot
break an icon it does not know about.

## 73. ⚠ TWO MISTAKES, BOTH CAUGHT, BOTH WORTH RECORDING

**I deleted files that another key still owned.** `micon_laser_1..5` and `laser_icon_1..5` are
DIFFERENT KEYS POINTING AT THE SAME FILES. Deleting by key removed five files `laser_icon_`
still needed and the manifest went to five broken paths. Recovered from the 0805o zip.

The rule this encodes, now asserted: **a key is not the owner of its file.** Before deleting,
check no other key points at the same path. There are aliased paths all over this manifest and
an assertion now proves that, so the check stays load-bearing rather than decorative.

**I wired one of two call sites.** The stage card went through the sheet; the PICKUP draw at
`drawPowerups` still did `XART.rdy('spicon_'+pk)` directly. With the keys deleted that branch
would have failed its guard and fallen through to the plain box — the icon would simply have
stopped appearing on the pickup, with nothing reporting it. Both paths use the sheet now, and
an assertion counts the call sites.

Also fixed in passing: `iconDraw` needed an explicit centred mode. The pickup draws about its
own origin while the card draws from a left edge, and using the wrong one shifts the icon by
half its width.

## 74. WHERE THE LIBRARY STANDS

    images            9,812  ->  9,660
    disk             435 MB  ->  414 MB
    decoded RGBA   2,891 MB  ->  2,574 MB      317 MB recovered

## 75. STILL OPEN

* Per-character ship/jet atlases — worth it for decode count only; the art is already correctly
  sized, so expect no RAM win. Say if that trade is worth it.
* falva/lizzie `pv2` edge-clipping in the source art.
* **Cole's clipping still needs a location from you** — in flight, on the select card, or
  mid-roll.


---
---

# DROP 0805q — THE SHIP ATLAS

Mike: *"regardless of who you load, still loads the same graphical sheet to pull the jet from.
its simplistic, dead simple and dead smart."*

## 76. HE WAS RIGHT AND I HAD FRAMED IT WRONG

I had argued against this on the grounds that ship art is already correctly sized so an atlas
buys no RAM. That measured the wrong thing. The point is **predictability**: with 162 separate
files, WHICH ones decode depends on which pilot is picked — a different set every run, warmed
at a different moment. One sheet is the same decode every time, and the frame is a rect lookup
after that.

It also turned out to buy memory anyway, because trimming recovers the margins:

    162 files -> 1        decoded 35.9 MB -> 22.5 MB        disk 7.7 MB -> 7.0 MB

## 77. HOOKED AT ONE PLACE, NOT THIRTY-ONE

There are 31 `ship_` references across the source. None were rewritten. Every accessor — `rdy`,
`get`, `safe`, `raw` — funnels through `XART._touch`, so the sheet is hooked there: a `ship_`
key resolves to a cell, everything else falls through untouched.

**⚠ The cell is rebuilt at its ORIGINAL canvas size, not its trimmed size.** This is the part
that would have quietly broken things: `SHIP_THR` anchors, `_HB` hull bottoms and `_CF` content
fractions are all FRACTIONS OF THE ORIGINAL CANVAS. Return a tight crop and every one of them
points somewhere else — the thruster would leave the tail again, undoing 0805j. The trim is
undone on extraction and the caller sees exactly the image it always saw. There is an assertion
on this specifically, comparing all 162 resolved cells against their recorded original size.

Cells build lazily and cache, so one pilot costs the sheet plus its own ~18 frames, not all 162.

## 78. THE PRELOAD GOT SMALLER *AND* WIDER

The opening flies a ship immediately, so `PRELOAD` used to pull **nine** pilot airframes — and
only their plain frame, never a bank or a roll. It now pulls `nsa_ships`: one request covering
every pilot and every frame. Fewer preloads, more coverage. That is Mike's argument, made
concrete.

While fixing the assertion I found the suite's copy of the PRELOAD regex had **drifted from the
game's** — it was missing `nui_`, `nhxv_` and `nfw_`, so it had been testing a pattern nobody
uses. It now reads the real one out of the source.

## 79. THE ALIAS RULE FROM 0805p EARNED ITS KEEP IMMEDIATELY

Deleting the ship sources ran through the check added yesterday, and it fired: **18 of the 162
keys are aliases sharing files with other keys.** Those files were kept and only the keys
de-registered. Without that check this drop would have repeated the 0805p breakage at ten times
the scale. 153 files deleted, 7.3 MB, **0 broken paths**.

## 80. WHERE THE LIBRARY STANDS

    images            9,812  ->  9,499
    disk             435 MB  ->  407 MB
    decoded RGBA   2,891 MB  ->  2,556 MB      335 MB recovered

## 81. STILL OPEN

* falva/lizzie `pv2` edge-clipping in the source art.
* **Cole's clipping still needs a location from you** — in flight, on the select card, or
  mid-roll. Measurement says he is not edge-clipped, so I cannot guess at it.


---
---

# DROP 0805r — THE CHARGE TRIGGER BUG, AND COLE'S SONIC ART

This brief is three or four drops of work. This one takes the piece that was already hurting
the game and that everything else depends on.

## 82. "2 SHOTS LET OFF BEFORE WE CHARGE" — REPRODUCED EXACTLY

> "when we use players who have charge effects, 2 shots of whatever weapon they have equipped
> lets off before we charge ... there should be a failsafe to prevent that or recognize tap
> button from a hold button."

Measured, trigger held from frame zero with the special active:

    maverick    4 bullets escaped     (2 shots x 2 lanes — literally the two shots)
    falva      23 MG rounds escaped

**The cause was that suppression had been written as a THRESHOLD, not a mode.** Maverick's guard
is `mavCharge >= MAV_HALF`, and `MAV_HALF` is **0.75 seconds** — so for three quarters of a
second the machine gun runs normally underneath the wind-up, and at his 0.38s cadence that is
exactly two shots. Falva had no primary suppression at all.

### Fixed as Mike described, not by moving the threshold to zero

Zeroing the threshold would have stopped the leak and also removed the ability to snap off a
single round. The trigger is now WATCHED instead:

    press and release inside TAP_WINDOW (0.14s)  -> a TAP, fires one shot
    still held past it                           -> a HOLD, charges, fires nothing

`chargePilotActive()` is the single predicate for who owns the trigger, so a new charge weapon
only has to be added in one place. Cole's sonic boom is already in it.

**Verified: holding leaks 0 for both pilots (was 4 and 23), and a tap still fires.**

⚠ **One difference to rule on:** Maverick's tap fires; **Falva's does not**. Her `pShoot` has its
own rollerball-exclusive guards, so a sub-arm tap during her special produces nothing. That is
arguably correct for her — the charge IS her weapon — but it is a behaviour change from the 23
rounds that used to leak, and it is your call whether she should keep a tap shot.

## 83. COLE'S SPECIAL LOOKS LIKE THE SONIC BOOM

> "replace cole's pickup box graphic and powerup icon for his special ability with the new sonic
> boom one."

Done as a rename map (`SPECIAL_ART_OVERRIDE`), not an art swap — the old plates stay on disk and
it is one line to reverse. His special MECHANIC is untouched: NUKE STRIKE still fires from the
special button, matching "He automatically will get nuclear warheads to replace his bombs AND the
sonic boom effect."

Verified both the overridden and the normal icon still draw, and every other pilot resolves
unchanged.

## 84. DECKER VOL.3 ART INSTALLED, WEAPON NOT WIRED

The pack ships **three generations**. Vol.3 is the current one — square yellow pickup box, real
projectile trails, 7 pre-angled frames, and its own preview states the design: *"PELLET = HITBOX,
FIRE STREAK = VISUAL TRAIL, MOVING PROJECTILES, NOT HITSCAN."* That is what got installed.

37 keys registered, 0 broken paths: `ndk_box`, `ndk_icon`, `ndk_shot_0..3` (travel loop),
`ndk_ang_0..6` (pre-angled), `ndk_muz_0..3`, `ndk_shell_0..5`, `ndk_imp_0..3`,
`ndk_scorch_0..5`, `ndk_trail_0..3`.

**The shotgun itself is NOT implemented** — asserted as art-only so it cannot be mistaken for done.

## 85. NOT STARTED FROM THIS BRIEF

Saying so plainly:

* **Sonic boom as a charge weapon.** `chargePilotActive()` already claims the trigger for it, but
  the charge/release behaviour itself is not built — it still fires on a cadence.
* **Lizzie's anchored MG rework** — the non-black giant slugs with a black edge and gold 16-bit
  glow, and the rule that she cannot barrel roll or twist while it is equipped (glide only).
* **Decker's incendiary shotgun** — 50/50 with cloak, spread blast, reload delay, shell eject,
  setting fodder on fire but not bosses, and the bullet-hole decals.
* **"roll graphics"** — I read this as rolling forward to the latest generation of the Decker
  pack, which is what I did with Vol.3. If you meant the barrel-ROLL graphics need work, say so
  and I will take that instead.


---
---

# DROP 0805s — TWO CLARIFICATIONS RUN DOWN

## 86. THE DECKER GENERATIONS — NOTHING TO SWAP

> "V3 has the correct shotgun trails/pellets, v1 or v2 has the flame muzzle flash you can
> animate and overlay for decker, and the shells as well."

Checked by md5 rather than by eye. **The muzzle blast, shell eject, buckshot, angled spread,
incendiary impact and scorch decals are BYTE-IDENTICAL across all three generations** — same
file, same hash, in Vol.1, Vol.2 and Vol.3.

What actually differs:

    DeckerPickupBox    3 different designs
    DeckerPickupIcon   3 different designs
    Vol.3 only         ShotgunProjectileSpread + ShotgunProjectileTrails

So the flame muzzle flash and the shells installed in 0805r already ARE the Vol.1/Vol.2 art —
there is no swap to make. The only open choice is which **pickup box** you want; all three are
rendered side by side in the attached proof. Vol.3's square yellow one is currently installed.

## 87. LIZZIE'S BARREL ROLL — AND THIS PROBABLY ANSWERS THE COLE QUESTION

A barrel roll should narrow to edge-on and widen back. Measured ink width across `br0..br7`:

    maverick 0.39   yuri 0.40   decker 0.43   axel 0.45   freezer 0.47
    juggernaut 0.50   falva 0.58
    cole 0.83   lizzie 0.89        <-- barely change

But the roll animation itself is fine. **The cause is DEBRIS.** Connected-component analysis
finds a wing section sitting apart from the airframe:

    lizzie br5   2,117 stray px      lizzie br1     829 stray px
    cole br2     1,253 stray px      cole br3/br6   1,253 each
    maverick     163 stray px TOTAL, none over 45 — wingtip lights

In Lizzie's case the detached chunk is a wing tip **carrying her star roundel**, floating clear
of the plane. That is what makes her roll read wrong.

### ⚠ AND IT VERY LIKELY EXPLAINS COLE

You reported Cole looking "clipped" and I could not reproduce it — measurement showed he is not
edge-clipped, and I have been asking WHERE you were seeing it. **Mid-roll.** A 1,253-pixel wing
panel detached beside his jet on three of his eight roll frames reads exactly as a clipped
sprite. Same defect, same family of frames.

### The obvious theory was wrong, so I stopped

A frame sliced at the wrong offset — wing wrapping around the canvas edge — fits the look
perfectly. It is also **disproved**: no horizontal shift, tested at 2px steps across the full
width, reunites the pieces on any of the four frames. So it is not a mis-set frame boundary;
the chunks genuinely sit apart in the source art.

**NOT auto-repaired, deliberately.** Deleting the chunk leaves the plane missing a wing, and
moving it is inventing art. Both break the standing rule. The numbers are recorded in an
assertion so a re-export can be verified against them.

**What I need:** the source sheet those `br` frames were sliced from, or re-exported br frames
for lizzie and cole. Everything else about the roll — the timing, the frame order, the i-frames
— measures correct.

## 88. STILL OPEN FROM THE WEAPONS BRIEF

Unchanged from 0805r: sonic boom as a charge weapon, Lizzie's anchored MG rework (including the
no-roll-while-equipped rule, which is worth doing regardless of the debris), and Decker's
incendiary shotgun.


---
---

# DROP 0805u — LIZZIE'S HEAVY MG

## 89. THE SLUG — DERIVED FROM HIS ART, NOT INVENTED

> "uses the giant slug bullets (non black ones). add a black edge to these bullets and make
> them glow pixel gold with proper 16-bit shading."

The two GIANT rounds in the game are Cole's tier plates, and they are measurably one gold and
one black: **pmgc_6 (159,100,9)** and **pmgc_7 (30,33,38)**. The non-black one is pmgc_6, so
that is the source.

`nlz_slug` is built from it by taking its own luminance and re-mapping it onto a **ten-step gold
ramp** — bronze shadow through amber body to a white-hot core — so the shading BANDS the way
Genesis art does rather than blending, then adding a hard **1px black outline** hugging the
silhouette. Result: **8 distinct colours**, which is where 16-bit sprites actually sit. The gold
glow rides outside the black edge as a shadowBlur, so the edge stays crisp against it.

Palette work on his own art, not a new sprite.

## 90. THE MOUNT WEIGHS HER DOWN — TWO SEPARATE RULES

> "do not allow her to barrel roll while its equipped or twist, she will simply glide left or
> right as its supposed to weigh her down. its a gameplay balance."

Those are two different mechanisms and both were needed:

**No roll** — refused inside `startRoll()` rather than in the input handler, so every route into
a roll is covered and the double-tap still registers as a dash input for the glide.

**No twist** — `_shipFrameKey` switches to the edge-on `br2`/`br6` frames once `|bank|` passes
TWIST (0.82). Her bank is capped at **0.45** while mounted, which keeps her on the soft `pv1` /
`pv3` lean. Verified: at ±0.45 she draws `pv3` / `pv1`, and only at 0.9 — which the cap prevents
— would she reach `br6`.

⚠ **A useful side effect:** the cap keeps her off the `br` frames entirely while the mount is on,
so the detached-wing debris from §87 never shows while she is carrying it.

Verified in play: she CAN roll without the mount, CANNOT with it, and the mount still docks.

## 91. DAMAGE — MEASURED AGAINST REAL PER-STAGE HP

> "does deadly damage seemlingly one shotting or two shotting most fodder enemies."

Measured against every fodder type the stages actually field, at NORMAL, after the 0805b retune:

    at 6 dmg   stage 1-2: 1 shot   stage 3: 2   stage 5: 2   stage 8: THREE
    at 7 dmg   stage 1-2: 1 shot   stage 3: 2   stage 5: 2   stage 8: 2

Stage-8 fodder sits at 14 hp, so 6 left a third shot on the table. **7 closes it** — one or two
shots on every stage, which is the brief. Cadence stays at 0.16s from two barrels: a mounted
gun, not a faster pea-shooter.

## 92. STILL OPEN

* **The `br` source sheets** — still the blocker on the roll debris, and on falva/lizzie `pv2`
  edge-clipping.
* **Sonic boom as a charge weapon** — the trigger plumbing is in from 0805r; the charge/release
  behaviour is not.
* **Decker's incendiary shotgun** — all 37 art keys installed and asserted art-only; the weapon
  is not built.
* Falva's tap firing nothing during her special (0805r §82) — your call.


---
---

# DROP 0805v — SONIC BOOM BECOMES A CHARGE WEAPON

> "Now, sonic boom should be a charge effect."

It was firing on a 0.34s cadence, which is a machine gun that happens to look like a wave.

## 93. IT REUSES THE 0805r INPUT MODEL RATHER THAN INVENTING A SECOND ONE

Holding winds it up and releasing is the shot, the same shape as Falva's rollerball and
Maverick's lance. It goes through the same `chargePilotActive()` predicate added in 0805r, so
there is one tap/hold convention in the game rather than two:

    tap                -> a single small wave, so the weapon is never dead in your hands
    hold and release   -> one wave scaled by how long it was held

The charge is driven off the RAW trigger inside `_newWeaponTick`, exactly like `falvaChargeTick`,
so it does not depend on the cadence block ever running.

## 94. THE CHARGE SCALES THREE THINGS AT ONCE

A bigger number alone would not read on screen, so wind-up moves damage, size and speed
together, and parks distortion more often. Measured:

    hold      peak charge    damage   wave width
    5 frames     0.08s          6         30
    30 frames    0.50s          8         38
    70 frames    1.15s         14         54
    120 frames   1.15s         14         54     <-- caps, does not grow forever

A full charge is **2.3x the damage and 1.8x the width** of a tap.

## 95. ⚠ THE DOUBLE-FIRE THAT ALMOST SHIPPED

`pShoot -> sonicFire` and the release branch in `sonicCharge` BOTH trigger on the release frame.
With `sonicFire` still firing, a tap would have emitted **two waves** — one from each path.

`sonicFire` now only returns `sonicActive()` to claim the trigger and keep the machine gun
silent; the charge path is the sole shot owner. Asserted by regex on the function body, and by
measurement: exactly one wave on release at every hold length, zero while held.

## 96. TWO OLDER ASSERTIONS UPDATED, NOT WEAKENED

The 0805i assertions drove `pShoot()` in a loop and counted waves — correct for a cadence
weapon, meaningless for a charge one, and they went red immediately. They now drive the trigger
the way a player does: hold, release, then let the wave travel. Same coverage, correct shape.

## 97. STILL OPEN

* **Decker's incendiary shotgun** — the last piece of the weapon system. All 37 Vol.3 art keys
  installed and asserted art-only; spread blast, reload delay, shell eject, fire-on-hit
  excluding bosses, and the bullet-hole decals are not built.
* **The `br` source sheets** — still blocking the roll debris and the falva/lizzie `pv2` clipping.
* Falva's tap firing nothing during her special (0805r §82) — your call.


---
---

# DROP 0805w — DECKER'S INCENDIARY SHOTGUN

> "I think this would complete the full special weapon system."

It does. Cole, Lizzie and Decker all have theirs now.

## 98. THE RELOAD IS THE WEAPON

What makes this a shotgun rather than a spread gun is the CADENCE, not the pellet count. A
spread weapon fires continuously; a shotgun fires one loud blast and **cannot fire again until
it has cycled**. So the whole thing is built around the pause:

    BLAST    7 pellets in a single frame, then the trigger is dead
    RELOAD   0.62s during which nothing comes out, shells arcing away
    READY    the next pull works

Measured: **0 shots during the reload**, 7 on the next pull. That assertion is the one that
matters — if it ever reads non-zero the weapon has quietly become a spread gun.

## 99. SEVEN PELLETS, SEVEN PLATES

The pack ships **seven pre-angled projectile plates** (`ndk_ang_0..6`) — exactly one per pellet.
So the spread is laid out to match (-0.30 to +0.30 rad across the seven) and pellet *i* draws
plate *i*: the art authored for that angle, rather than one sprite rotated seven times.
Verified 7 distinct plates in a single blast.

Its own preview states the design and it is followed literally — *"PELLET = HITBOX, FIRE STREAK =
VISUAL TRAIL, MOVING PROJECTILES, NOT HITSCAN."* These are real travelling bullets.

## 100. THE BURN MIRRORS THE ICE, RATHER THAN INVENTING A SECOND STATUS SYSTEM

The ice breath already marks units with `_frozen` — a counter plus a flash timer, ticked where
it is hit. The burn follows the same shape (`_burn`, `_burnTick`) rather than adding a parallel
mechanism.

> "Should light enemies on fire who are hit with it except for mini bosses and bosses."

**The exclusion lives inside `dkIgnite`**, not at the call site, so a future weapon that ignites
cannot forget it. Measured: fodder catches, **boss and miniboss do not**, and the burn keeps
eating the unit for 5 hp over 1.5s after the pellet has gone.

## 101. SHELLS AND HOLES

Two casings eject **left and right** on every blast and arc away rather than dropping straight,
using the pack's own 6-frame reel. The muzzle blast is armed by the shot and lives 0.22s.

The bullet-hole bursts are registered **against the enemy**, not a world position, so a decal
rides with the unit it hit and reads as damage on the hull rather than a spark left behind in
the air.

## 102. 50/50, MEASURED

> "Decker - gets a 50/50 change to get cloak or the new incinendary shotgun"

Same coin as Lizzie's, flipped when the crate breaks. Measured over 6,000 rolls and asserted
within 6%.

## 103. WHAT REMAINS

The weapon system is complete. Outstanding is all art-blocked or awaiting your call:

* **The `br` source sheets** — the roll debris on Lizzie and Cole, and the falva/lizzie `pv2`
  edge-clipping. Still the one thing blocked on you.
* **Falva's tap firing nothing** during her special (0805r §82).
* **Cole tier 8** has no bullet art; it falls through to the L7 black plate.
* Stage 9 is still not in `STAGES[]`, and its 14 protected `nep_9_`/`nbp_9_` plates are held for
  wiring that has not happened — worth knowing the draw path that used them was retired in 0805f.


---
---

# DROP 0805x — SONIC RANGE + WAKE, AND A CORRECTION ABOUT TIER 8

## 104. I WAS WRONG ABOUT COLE'S TIER 8

I flagged "Cole tier 8 has no bullet art, it falls through to the L7 black plate" in two
passovers. **That was wrong**, and Mike's note — "cole's tier 8 is supposed to be the purple
fusion cannon lasers" — sent me to check it properly.

Tier 8 does not use an MG plate at all. `coleFuseTick` intercepts the trigger above the cadence
block, and a full charge fires `coleFuseRelease` — two piercing lances drawn from the green
laser art hue-rotated 275 degrees to purple. **It already is the purple fusion cannon.**

Measured, holding the trigger at each tier:

    wlevel 7   coletri x52 + mg x28     the trident tier
    wlevel 8   colefuse x2              the fusion cannon, no MG underneath it

⚠ I nearly reported a second false bug on the way: my first probe showed tier 8 firing MG,
because `run.wlevel` is re-derived from `run.wlevels[run.weapon]` every frame and I had only set
the derived value. Setting it the way the tier keys do — `run.wlevels[0]=8` — shows the cannon
firing correctly. **The game was right both times; the probe was wrong.**

Maverick's charge is likewise still intact — asserted directly against the shared
`chargePilotActive()` predicate rather than assumed.

## 105. THE FALL-SHORT WAS IN THE DATA, NOT THE BEHAVIOUR

> "if you let go before fully charging, shoots out a half powered sonic wave that falls short but
> will semi damage units caught in its way."

0805v scaled damage, width and speed with the charge but left `life` fixed — and **nothing ever
decremented `life` anyway**. So a tap and a full charge both flew the entire screen: the wave was
weaker, never shorter. The property existed on the bullet and did nothing.

Range now scales hardest of the three, and it is tuned against the screen rather than picked. The
play area gives a wave about 420px before it leaves the top; at the first curve a HALF charge
still had 630px of range and crossed anyway. Measured travel after retuning:

    tap    161 px      dmg 6     falls well short
    half   357 px      dmg 9     visibly falls short of crossing
    full   407 px      dmg 14    crosses

**All three pierce** — "pierce units with sonic waves in both states half or full charge blast."
A half charge is a weaker wave, not a lesser weapon.

## 106. THE WAKE WAS BEING LAID FROM THE DRAW

> "create sonic wave distortion via our sprites in the area the blast travels for several seconds
> before it corrects itself."

Two things were wrong. The plates faded in **0.30s**, so the wake was gone almost as fast as it
was laid. And they were parked from inside the BULLET DRAW — so a headless tick produced none at
all, and any frame that skipped a render would have dropped the trail.

Both moved into `sonicTick`, off the same clock as everything else. `SONIC_WAKE` is 2.8s and
scales with charge, so a full boom leaves a longer-lived scar down the corridor it flew than a
tap does. A spent wave also drops a final pulse where it ran out, so a short shot dissipates
visibly instead of just vanishing.

## 107. WHAT REMAINS

* **The `br` source sheets** — Lizzie and Cole's roll debris and the falva/lizzie `pv2` clipping.
  Still the only thing blocked on you.
* **Falva's tap** firing nothing during her special (0805r §82) — your call.
* Stage 9 is still not in `STAGES[]`.


---
---

# DROP 0805y — THE ENEMY/BOSS ATLAS: MEASURED, AND THE ANSWER IS NO

> "we should probably make atlas's for each fodder enemy, mini boss and boss to save space too
> probably"

Measured before building, per the rule the box/pill sheet established. **It would make things
about ten times worse**, and only the measurement says so.

## 108. THE NUMBER

    enemy + miniboss + boss art          3,899 keys
    decoded if ALL were resident         1,322 MB
    actually observed drawing in a
    full nine-stage playthrough          480 keys, 125 MB      <-- 12%

**An atlas must decode entirely.** That is the whole point of a sheet: one image, one decode. So
atlasing this art would take peak memory from **~125 MB to ~1,322 MB** — it would destroy the
lazy loading that is already doing a **10.6x better job** than any sheet could.

## 109. WHY THE SHIP SHEET WORKED AND THIS ONE WOULD NOT

Same technique, opposite answer:

    ships   162 keys,    36 MB total, one pilot uses ~18 of them
            -> sheet costs 22.5 MB, saves 161 decodes. Small cost, big win.

    enemies 3,899 keys, 1,322 MB total, a run touches 12% of them
            -> sheet costs 1,322 MB, saves ~3,400 decodes. Catastrophic cost.

The deciding factor is not the key count, it is **what fraction of the sheet a session actually
uses**. Ships are near 100%; enemies are 12%.

## 110. PER-BOSS SHEETS ARE BUILDABLE, WHICH IS NOT THE SAME AS WISE

Checked, because it is the obvious next suggestion. Every boss fits under the 16384px canvas cap:

    mbg2  290 keys  7660x7660  204 MB      mbg3  290 keys  7867x7867  215 MB
    most others     3268x3268   37 MB

But only ~10% of a boss's components draw in a fight, so mbg2 would go from roughly **20 MB
resident to 204 MB** the moment Magma appears — and 7660px also exceeds the 4096px texture limit
common on mobile GPUs.

## 111. WHAT *WOULD* HELP — 36 FAMILIES, 34 MB

There is a real subset that fits the ship-sheet shape: families where **60%+ of the keys draw
together** and the whole sheet stays under 6 MB. `nel_talon`, `nel_hell`, `nel_spiral`,
`nvl_ash`, `nvl_skim`, `mbv_f1_atk` and 30 more — **36 families, 34 MB, around 250 keys**.

That is the version of Mike's idea that pays. Say the word and it goes in; it is a fraction of
the work and none of the risk.

## 112. AND ONE THING THE AUDIT TURNED UP

`mbg2_bchainl / bchainr / bchaind` and the `mbg3` equivalents — **36 keys, 21 MB, observed ZERO
times** in a full nine-stage run including forced boss fights. Possibly dead, possibly reached
by a path a driven run does not hit. **Not touched**: 0724dq is the standing lesson that
non-observation is not proof, and that sweep cost 4,000+ browser errors. Flagged for a look
rather than acted on.

## 113. STILL OPEN

* **The `br` source sheets** — Lizzie and Cole's roll debris, falva/lizzie `pv2` clipping.
* **Falva's tap** firing nothing during her special.
* The 36-family atlas above, if you want it.


---
---

# DROP 0805z — MIKE WAS RIGHT: PER-STAGE SHEETS WORK

> "I mean you would space it out and give it precise locations I would assume?"

Yes — and that is the part that is not the problem, which means my 0805y framing was wrong.

## 114. THE CONSTRAINT I SHOULD HAVE LED WITH

**The blit is precise. The decode is not.** Drawing one cell out of a sheet costs nothing extra
— `drawImage` takes a source rect and reads exactly that region. But getting the sheet into
memory at all means decoding the WHOLE PNG to RGBA; a PNG is filtered row-by-row, so there is no
partial decode and no random access.

So the cost of a sheet is not "how much of it you draw", it is **how big the sheet is**. That is
why the answer depends entirely on grouping, and why "atlas everything" and "atlas per stage"
give opposite results from the same technique.

## 115. GROUPED PER STAGE, IT WORKS — MEASURED

A stage touches far less enemy art than I implied. Recorded per stage across driven playthroughs:

    stage   keys   sheet
      1      61     9.5 MB        5      31     5.6 MB
      2      60    28.4 MB        6     108    16.9 MB
      3      82    33.6 MB        7      23     9.5 MB
      4      59     8.6 MB        8      74    13.9 MB

    peak ONE stage resident      33.6 MB
    all eight resident          122.6 MB   (459 keys)
    current lazy, whole run     ~125 MB
    whole-family single sheet  1,322 MB    <- the only thing that does not work

**Same memory as today, and 459 decodes become 8.** Drop the previous stage's sheet on a stage
change and peak falls to 33.6 MB, which is better than today. Mike's instinct was right; my
"no" only ever applied to one sheet for all 3,899 keys.

## 116. ⚠ ONE DETAIL DECIDES WHETHER IT PAYS

It is the difference between the two sheets already shipped, and it is worth stating before the
work starts:

* **box/pill sheet (0805l)** blits from SOURCE RECTS — `drawBoxPillCell` passes sx,sy,sw,sh. The
  sheet is the only copy in memory. **This is the right pattern here.**
* **ship sheet (0805q)** EXTRACTS each cell to its own canvas, because 31 call sites read
  `naturalWidth` off whatever `XART.get` returns. Anything used is therefore paid for twice —
  sheet plus cell. At ship scale (18 cells) that is a fine trade; at 108 keys in a stage it would
  double the cost and throw the win away.

So per-stage enemy sheets must go in via the source-rect path, which means touching the enemy
draw call sites rather than hooking `_touch`. That is the real work, and it is why this is
scoped as its own drop rather than bolted on here.

## 117. WHAT I GOT WRONG, PLAINLY

0805y said "the answer is no" and gave a number for the wrong design. The number was right for
one sheet of everything and irrelevant to what Mike was actually proposing. The assertion has
been corrected to say exactly which design it rules out, so the file does not carry a
too-broad conclusion.


---
---

# DROP 0806a — PER-STAGE ENEMY SHEETS, BUILT

Mike's design, built the way the measurement said it had to be.

## 118. NINE SHEETS

    common     34 keys  1056x859   3.6 MB      stage 5   19 keys   416x3182   5.3 MB
    stage 1    49 keys  2720x904   9.8 MB      stage 6  100 keys  3808x1076  16.4 MB
    stage 2    60 keys  3808x2083 31.7 MB      stage 7   23 keys  1568x1713  10.7 MB
    stage 3    71 keys  4032x2240 36.1 MB      stage 8   54 keys  2624x1177  12.4 MB
    stage 4    49 keys  2208x1028  9.1 MB

459 cells. A stage loads its own sheet plus the common one — **two decodes instead of up to 100**.

## 119. THREE THINGS THAT DECIDED THE DESIGN

**The sheet is the only copy.** Cells resolve to a DESCRIPTOR — `{__sheet, __r:[sx,sy,sw,sh]}`
carrying naturalWidth/Height — not to an extracted canvas. The ship sheet extracts, because 31
call sites read `naturalWidth` off the result, and therefore pays for anything used twice. At 100
keys a stage that would have doubled the cost and thrown the win away.

**One wrapper instead of dozens of call sites.** `ctx.drawImage` expands descriptors, so every
existing enemy draw keeps working untouched. All three signatures are handled — and the
nine-argument form is OFFSET into the cell and CLAMPED to it, because a caller asking for a
region larger than its cell would otherwise bleed into whatever was packed beside it. That is
the "packed sheets bleed across frames" failure already on record for the boss sheets.

**Cells are packed UNTRIMMED**, so naturalWidth maps 1:1 onto the cell rect and any caller that
scales by the image's own dimensions lands exactly where it did before.

## 120. ⚠ TWO PACKER BUGS CAUGHT BEFORE SHIPPING

**A width search that only minimises AREA returns pathological shapes.** The first pass gave
stage 2 a sheet of **544x14034** — fine on desktop, unusable on a phone. Both dimensions are now
capped at 4096, the texture limit common on mobile GPUs, and there is an assertion on it.

**Shared keys resolved to the wrong sheet.** Writing `cells[k]=[stage,...]` per stage meant a key
used by two stages kept whichever stage was processed LAST, so stage 1 was pulling in stage 3's
and stage 4's sheets to draw its own enemies — 56 MB where 10 was promised. The 34 keys used by
more than one stage now live in a common sheet. Verified after: stages 3, 6 and 8 load exactly
common + their own.

## 121. WHAT IS NOT PERFECT

Stage 1 still pulled a third sheet in the verification run. The owner map comes from a single
recorded playthrough, and enemy spawns vary between runs, so a key can turn up in a stage it was
not captured in. It still costs 3 decodes rather than 49, and nothing is missing — the fallback
resolves it — but a multi-run capture unioned together would tighten the grouping. Recorded
rather than papered over.

## 122. STILL OPEN

* **The `br` source sheets** — Lizzie and Cole's roll debris, falva/lizzie `pv2` clipping.
* **Falva's tap** firing nothing during her special.
* Dropping the previous stage's sheet on a stage change would take peak resident from ~122 MB
  down to ~36 MB. Not done — it needs an eviction path that does not fight `warmStage`.
