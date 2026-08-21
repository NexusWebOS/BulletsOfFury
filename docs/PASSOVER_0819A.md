# 0819a — FIRE SHARK JETS, AND HOMING WAS NEVER IN THE MUZZLES

Mike's 0819 list, all six items:

| # | item | state |
|---|------|-------|
| 1 | level 1 and 3 jets: circle, then charge, **no projectiles** | **DONE** |
| 2 | homing missiles via fodder enemies — **CUT** | **DONE** |
| 3 | burst machine guns with pauses / spread / laser / **non-homing** missiles | **DONE** |
| 4 | remove homing from all bosses **past level 1** | **DONE** |
| 5 | increase the amount of enemies | **DONE** |
| 6 | remove all **drone** enemies from level 3 | **DONE** |

---

## THE ONE FINDING THAT MATTERS

⚠ **THE HOMING WAS NOT IN THE MUZZLES. IT WAS IN THE MOVER, AND IT APPLIED TO EVERY MISSILE IN
THE GAME.**

`updateBullets`' `emissile` branch ran one steering block for every round of that kind, with
`b.turn || 0.05` as the default turn rate. So a round fired by a muzzle that calls itself straight
— the bomber's rocket, `eMissile`, the tank shell, every boss volley — **curved after the player
anyway**. There was no flag to check and nothing opted out.

That is why this keeps coming back. 0801ea removed `fk:'homing'` from the racer. 0801kf changed
the diagonal file to guns and the jungle tank to a rocket. Each fixed the muzzle it was pointed
at, and the mover went on steering the result. **Renaming an `atk` row was never going to work.**

Homing is a **GRANT** now: the round steers only if its muzzle set `b.homing`, and only on stage 1.
Everything else flies the vector it launched on.

```js
if(b.homing && (typeof run==='undefined' || run.stage===1)){ ...steer... }
```

⚠ **MEASURE THE ROUND, NOT THE ROSTER.** §230 records each missile's heading before and after a
frame and counts direction changes. Stages 2-8: **0 curving frames** across 18,372 missile-frames.
Stage 1 is the **control** at 1,299 curving frames — without it this section would also pass on an
engine that had simply deleted enemy missiles.

---

## THE JETS

`loopcharge` is a new pattern: run in → **one full circle** → charge the player, accelerating on a
limited turn. Guns off, `shoots=false`, `_atk='none'`. The generic body-contact check already in
`updatePlay` is the entire threat, and the game is one-hit-death, so no new collision code was
needed — dodge it and it flies off screen and dies.

- **Gated on the STAGE, not the unit.** Stages 1 and 3 convert; stages 4 and 6 keep the same
  airframes as gunfighters, because their wave scripts are tuned around jets that shoot.
- ⚠ **THE GATE IS IN TWO PLACES ON PURPOSE.** `applyNefUnit` runs *after* `applyS1Jet` and
  overrides it (0812e). Setting the pattern only in `applyS1Jet` gets silently undone.
- ⚠ **A SIDE-EDGE SPAWN LOOPS FROM A LEVEL RUN-IN.** Descending along an off-screen edge puts the
  whole circle out of view. Units authored at `x<8` / `x>W-8` fly in level first (sideswirl's
  idiom) and curl off that leg.
- ⚠ **THE CIRCLE HAS TO BE VISIBLE.** `drawNewEnemyArt` rotates by `e.spin`; the vault air draw
  uses `_faceAng`. Driving only `_faceAng` would fly the loop **nose-south** — 0806h's bug — so
  `spin` is driven from the same facing. §230 asserts **26 distinct attitudes** through one loop.

`sideswirl` already had loop-then-dive and now fires nothing on either phase. `topgun` keeps its
twin guns and has lost its mid-dive lock-on.

---

## THE GUNS

Every mode now leaves a window, which was the actual ask ("pauses in between to give you enough
time to shoot them"):

| mode | before | after |
|---|---|---|
| `gun` (rake) | `fireCd 0.085` — an endless stream | 8 rounds, then **1.4s** |
| `mg` (strafer) | twin guns + a lock-on every 6th | 4 pairs, then **1.5s**, no missile |
| `homing` (legacy name) | twin guns + a **lock-on** every 4th | twin guns + a **straight rocket** |
| `laser` | did not exist | 3-bolt lance at spd 6.2, **2.0s** reload |

The rake's sweep survives across bursts (`_fireCycle` keeps counting), so it still reads as one
strafing run rather than restarting each time.

---

## STAGE 3, AND DENSITY

All `drone` / `mdrone` / `minidrone` / `turdrone` waves are gone — **replaced, not deleted**, since
the same message asks for *more* enemies. The slack goes to the stage's own authored cast and to
the loop-charge interceptors (`cryo` is the ELITE ICE INTERCEPTOR). `minishipC` left with them: it
has been in `_DELETE` since the art cull and its wave spawned nothing. `shieldd` **stays** — its
live art is `nef_s3_shard_mine`, a mine, not a drone.

Density: `_liveCap` 7→9 (stage 1) and 4→6 elsewhere; `DIFFS.density` 0.70/0.85/1.10/1.35 →
0.80/1.00/1.25/1.50. The dispatch formulas are untouched, so wave rhythm holds.

---

## TWO BUGS THE DENSITY RAISE EXPOSED

Both were latent and are unrelated to what Mike asked for.

⚠ **`sepGrounded` DID NOT KNOW ABOUT TANKS.** It tested `pattern==='ground'` only, so
`tankhold` / `tankpatrol` / `s1tank` units were pushed sideways by the separation pass **with no
`tankDrivable` check** — "tanks into the water" by the exact route rule 3 of that pass's own header
promises to close. Invisible until fields got crowded enough to shove them; the suite caught it at
**145 violations** of the drivable band.

⚠ **THE MINIBOSS GATE COUNTED SCENERY AND WAS PINNED TO THE OLD CAP.** `enemies.length<=7` was
written against a live cap of 7. With the cap at 9 a perfectly healthy field held the miniboss off
**forever** — §202's play-through ran 200 simulated seconds and never met the JUNGLE CRUISER, which
reads as a broken trigger and is not. Props never leave on their own, so a surviving barrel dump
did the same thing. It counts live non-prop units against 9 now.

---

## ASSERTIONS REPOINTED (read before "fixing")

Nine assertions failed by describing the design this drop replaces. Per CLAUDE.md, each was read
before being touched:

- **`topgun fires a lock-on missile mid-dive`** → **inverted**. A topgun that places a lock is now
  the regression.
- **`stage 3 fields the drone type <d>`** ×4 → **inverted** to absence checks.
  ⚠ **AND THAT FIXTURE'S SLICE WAS WRONG**: it bounded stage 3 with `split('return P;')`, a string
  that **is not in the source** (the plans return `_planSorted(P)`), so "stage 3" silently included
  every later stage's waves. Presence checks never noticed; the new absence checks would have
  false-failed on stage 4's own `mdrone` rows. Bounded on the next stage arm now.
- **§210 / §212 / §213 jet fixtures** (dodge, routes, banking, twin guns) → **repointed to stage 4**,
  where the deltas still fly `s1jet`. The claims are unchanged; only the stage they are measured on
  moved.
- **§213 spelling normalisation** stays on stage 1 and now expects `loopcharge` for the delta rows.
  The claim under test is untouched: **both spellings must land on the same pattern**, because a
  spelling that missed the roster would fall through to `sine`.

---

## AND A THIRD BUG — "NO PROJECTILES" WAS TRUE OF EVERY MUZZLE AND FALSE OF THE SCREEN

⚠ **`enemyVolleyTick` NEVER ASKED WHETHER THE UNIT WAS ARMED.** It is keyed on `e.type` and runs on
its own clock, *deliberately* outside the `if(e.shoots)` dispatch (0810x, because most units' ticks
own their own `fireCd`). `s1jetdelta` and `cryo` both have rows in `ENEMY_VOLLEY`, so the
loop-charge jets — `shoots=false`, `_atk='none'`, `fk=null`, every muzzle they own switched off —
went on firing **fan and rake volleys**.

Setting three flags on the unit was not enough, and nothing in the roster or the pattern would ever
have shown it. It is the shape this file keeps recording: a second system reaching the same screen
by a path the obvious gate does not cover.

Gated at the one place every volley passes through, so disarming any unit now disarms it here for
free. Units that carry a volley row *and* shoot are unaffected — they all have `shoots=true`.

**Found by the assertion, not by looking.** §230 claims zero rounds from a jet that the assertion
one line above proves is unarmed. With the wave plan emptied (below), every other shooter was ruled
out and 12 rounds were left standing.

---

## A PROBE FAULT IN MY OWN NEW SECTION, CAUGHT BY IT

§230's first cut asserted "the loop-charge jet fires nothing" by counting `eBullets` **globally**
over 12 live seconds. It reported **47 rounds** from a unit the assertion one line above proves is
unarmed (`shoots=false`). Those were the patrol boats and gunboats the stage-1 plan dispatches
alongside it — CLAUDE.md's "colour-classifying a band of the canvas measures the LEVEL" in a new
costume. The plan is emptied now (`stagePlan=[]`), so the only unit alive is the one under test.

The stage-1 wave-count assertion was also **guessed at `>=25`** and the real number is 24 (22
before this drop, plus two loop-charge waves). Measured, not assumed.

---

## HOW TO VERIFY

    node --check assets/game.js
    node _BUILD_SOURCE/test_fl.js                    § 230 is this drop
    python _BUILD_SOURCE/shoot.py --state PLAY --stage 1 --seconds 22 --fps 4 --gif
    python _BUILD_SOURCE/shoot.py --state PLAY --stage 3 --seconds 30 --fps 4 --gif

**Suite: 2,695 ok / 3 failures.** All three are the long-standing environmental ones — the preload
key count and two `_superseded/` ledger checks. ⚠ **`_superseded/` IS NOT IN THE REPO AT ALL** (it
is never committed), so those two cannot pass on a fresh clone; they are not evidence of anything
in this drop. Baseline for comparison was **2,664 / 3** on this same tree before §230 was added.

Pixels: stage 1 shows deltas rotated hard over mid-loop with **no enemy tracer on screen**; stage 3
shows an ice interceptor mid-loop with no drones anywhere, and the **ENEMY APPROACHING** banner
firing — which is the miniboss-gate fix landing in real play.

---

## STILL OPEN

- The `laser` mode is wired and asserted but **no wave outside stage 3 fields it yet**. Placing it
  on other stages is Mike's call.
- Stage 2's `el_lr` reavers still fly `s1jet` with guns (0812m authored that deliberately). They
  were not converted because Mike named **1 and 3**.
- Everything in 0814d's STILL OPEN list is untouched: level 9 through level 5, the full-size
  cutscenes, the stage-9 packs, and the apostrophe-renders-as-a-comma glyph bug.
