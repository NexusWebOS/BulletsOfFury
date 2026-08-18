# DROP 0814D — ITEM 5: THE DAM SWAP HAS BEEN CORRECT, AND A THOUSAND ROWS OFF SCREEN

> 5. Stage 1 does not move the camera to the blown-up dam after the helicopter boss dies.

---

# 1. TWO THINGS CLAUDE.MD SAYS ABOUT THIS ARE STALE

The standing note warns at length that `cfg.destroyed` "needs a destroyed 800×4800 RC2 master,
which RC2 does not ship". **Both plates are registered and both are on disk:**

    jungle800_v3_intact     assets/game/jungle800_v3_intact.png       800x4800
    jungle800_v3_destroyed  assets/game/jungle800_v3_destroyed.png    800x4800

Rendered side by side, the destroyed plate is the same level with the dam **breached** — rubble
spilling down the channel, water pouring through the gap, smoke off the top. It is exactly the
asset the swap was written for. Nothing was missing.

⚠ **AND THE `ndam_*` OBJECT-ART PLAN IS NOT NEEDED.** The same note recommends drawing `ndam_*`
(222×290, four staged variants) as the dam the boss fights at, on the reasoning that the master
swap had no plate. It has one. `ndam_*` stays unused and unassigned; that recommendation should
not be acted on without Mike, because it would replace authored terrain with an object.

---

# 2. WHERE THE DAM IS, AND WHERE THE CAMERA STOPS

The dam's position was taken by **diffing the two plates** — the rows that change ARE the dam, so
this cannot be wrong about which part of the plate matters.

    the dam            master rows 0..949 of 4800
    at boss trigger    visible window is rows 1537..2049

srcY DECREASES as a stage runs, so the plate is consumed bottom-to-top and **the top of the plate
is the END of the level**. The dam therefore sits **588px above the top of the screen before the
fight even begins**.

The level does resume scrolling when the boss dies — `bossActive` goes false, so `_bossRun` stops
holding it — at the ordinary 40px/s. Covering 1,537px at 40px/s takes **38 seconds**, and
`stageEnding` hands over to the flyover at **6.4**. Measured across the entire death:

| t after the kill | srcY | dam in frame? | state | damBroken |
|---|---|---|---|---|
| 2s | 1454 | no | play | false |
| 5s | 1333 | no | play | false |
| 8s | 1211 | no | **flyover** | true |
| 11s | 1089 | no | flyover | true |

**Never within a thousand rows of it.**

## ⚠ SO `damBroken` HAS BEEN FIRING PERFECTLY, AND INVISIBLY, FOR DROPS

It flips on schedule at `dying >= 6.7`. The plate swaps on schedule. And it swaps a piece of
terrain **1,089 rows below the thing that changed** — so the only part of the level that differs
between the two plates was off screen every single time.

0801cr's *"swap under the peak white, camera held"* was right about the swap and wrong that the
camera should stay put: there was nothing to hide under the white, because there was nothing in
frame that changed. And 0809m's fix, and every check since, confirmed the swap was *happening* —
which it was. Nobody asked whether it was happening anywhere the player could see.

⚠ **AND THE FLYOVER STARTED BEFORE THE SWAP EVEN FIRED.** `endT` for stage 1 was **6.4** and
`damBroken` flips at **6.7** — both clocks start at `bossDie`, so the state changed 0.3s before
the dam was swapped at all.

---

# 3. THE FIX — FLY THE LAST OF THE LEVEL

A run-in: when the boss dies, ease the remaining scroll out to `range` over `DAM_RUN_IN` (3.2s),
smoothstepped. The existing beat then works as designed and for the first time has something in
frame to work on:

    0.0 - 3.2s   the camera runs the last 1,537px in; the dam arrives
    6.0 - 6.7s   the whiteout blooms and holds
    6.7s         damBroken flips - the plate swaps UNDER the white, dam on screen
    7.3 - 8.6s   the white fades back and the BREACH is revealed
    9.2s         the flyover takes over

⚠ **GATED ON `cfg.destroyed`, NOT ON `run.stage===1`.** A stage that ships a destroyed plate has
a finale worth flying to; one that does not is untouched. Stage 1 is the only declarer today, and
a stage that declares one later inherits this with no wiring.
⚠ **IT NEVER RUNS BACKWARDS** — `Math.max` against the current scroll, so a fight that happened to
end near the top keeps the ordinary scroll and this adds nothing.
⚠ **`endT` FOR STAGE 1 GOES 6.4 -> 9.2**, which is **2.8s longer** and is the only stage affected.
Mike's "stop taking screen pauses" (0809v) is about dead air; this is the payoff he asked for. It
is one number if he wants it tighter.

## Measured after the change — `probe_dam_0814d.py`

| t after the kill | srcY | dam in frame? | state | damBroken |
|---|---|---|---|---|
| 2s | 452 | **YES** | play | false |
| 5s | **0** | **YES** | play | false |
| 8s | **0** | **YES** | play | **true** |
| 11s | 0 | **YES** | flyover | true |

`docs/proofs/dam_0814d.png` — the breached dam on screen: rubble down the centre, water pouring
through the gap, the towers either side. It has never been visible before.

---

# 4. TWO PROBE FAULTS, BOTH WORTH KEEPING

⚠ **THE MINIBOSS FREEZES STAGE PROGRESSION, SO A PROBE THAT SHOOTS NOTHING NEVER REACHES THE
BOSS.** `stageTimer -= dt` runs for as long as `subBossActive`. 20,000 frames — 333 seconds of
simulated play — returned `reached=false`, which reads as a broken boss trigger and is not. The
probe clears the mini the way a player would.

⚠ **A LOW DIFF THRESHOLD SPREADS THE ANSWER ACROSS THE WHOLE PLATE.** At `rows>20` the dam
measured as rows **0..2332** — half the level — because the two renders also differ mildly all the
way down the channel. The dam is where they differ *most*: taking rows carrying at least a quarter
of the peak row's changed pixels gives **0..949**, which matches what the eye sees. A difference
map needs a threshold chosen against the signal, not against zero.

---

# 5. VERIFICATION

    pixels   probe_dam_0814d.py - dam in frame from 2s, srcY reaches 0 by 5s,
             the swap lands at 8s with the dam on screen

    suite    run 1   2,662 ok / 4 failures
             run 2   2,661 ok / 5 failures      <- NO CODE CHANGE BETWEEN THEM

## ⚠ THE SUITE IS NOT DETERMINISTIC, AND CLAUDE.MD'S CLAIM THAT IT IS IS NOW FALSIFIED

The failure that moves is *"every volley fired is 5-8 rounds (6, 3)"*. It passed on the first run
of this drop and failed on the second, with the tree untouched in between.

⚠ **DO NOT READ THE 4 AS THIS DROP FIXING THE VOLLEY.** I nearly wrote that. It is the
order-dependent fixture CLAUDE.md already documents at length — *"the fixture only produces
volleys because of state left by the ~200 sections before it, so its result is meaningless in
isolation and no threshold should be touched on the strength of it"*. This drop changes stage-1
scroll timing and `endT`, which plausibly shifts the accumulated state it inherits; that makes the
flip explainable, not a fix.

⚠ **WHAT IS NEW IS THAT IT MOVES AT ALL.** 0811x wrapped three fixtures in `seedWaves()` and
recorded *"three consecutive runs now give identical 2500 ok / 5 fail / 221 sections"*, and the
standing header says **"THE SUITE IS DETERMINISTIC NOW — EVERY RUN"**. That is no longer true for
this assertion. Either the seeding does not cover the path this fixture now takes, or something
since has reintroduced an unseeded source.

**Treat 4-or-5 as the expected band until that is chased**, and read the assertion NAMES rather
than the count alone — which is the only way this was caught.
