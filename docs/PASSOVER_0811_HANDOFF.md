# Passover 0811 — full handoff

> **⚠ SUPERSEDED IN PART BY `docs/PASSOVER_0811L.md`.** Read that first, then this.
> §2.1 (enemies stack) is **DONE** — the banking channel and the separation pass both landed and
> are measured in pixels. §2.2, §2.3 and §2.4 below are still owed and their diagnoses still hold.
> Two numbers here are retracted: the 839 / 71.9% baselines were **one sample of an unseeded
> distribution** that swings between 839 and 424, and `worst` is a max that cannot tell "stacked"
> from "spawned together". `probe_stack.py` is seeded now and reports a settled-burial column
> instead. Do not tune against the figures in §2.1.

Everything from drops **0810s → 0811j**. Suite at the end: **2,463 assertions / 218 sections /
4 failures** — the same four that have stood for weeks (preload count, the two `_superseded`, the
naval flash families).

Read `CLAUDE.md` first. This document is what changed since, what is still owed, and — most
usefully — **the exact reason each unfinished thing failed**, so none of it has to be rediscovered.

---

## 1. What landed and is verified

| drop | what |
|---|---|
| 0810s | Five ship bosses — stages 2/3/5 and minibosses on 2/3, from Mike's South-Facing Ship pack |
| 0810s | Mike's fire orb icons; the EQUIPPED box was drawing the wrong one entirely |
| 0810s | The quad-laser's four beams fire, and its charge phase (declared in 0801if, never built) |
| 0810t | Stage 7 on Mike's corrected plate, sludge showing through 68% of it |
| 0810t | Ice breath icons — Mike named the row; 0810s had guessed "ice shard" |
| 0810u | The positional volley layer (`ENEMY_VOLLEY`) |
| 0810v | Mike's loopable runway (`nrun_v2`, via `runwayKey()`) |
| 0810w | Five silent rosters armed — stages 2/5/6/7/8 had almost no shooters |
| 0810x | Enemy fire actually reaching the screen — the volley needed its own clock |
| 0810y | Toxic sludge darkened to 50% value |
| 0810z | The arcade intro cards' blank right panel |
| 0811a | Music on the Fury HQ cutscenes (they played in silence) |
| 0811b | Stage 4's miniboss — it had **none**; the Blacksteel Raptor takes the slot |
| 0811c | Boss phases, and the ship bosses had been firing **every frame** |
| 0811d | **The stage 2 boss was invisible**; arcade intros bypassed → straight to title |
| 0811e | Spawn clearance (the negative-y half of the pop-in) |
| 0811f | The pilot confirm window uses the authored face |
| 0811h | **Stage 1 is Mike's plate**, with the dam-breached variant wired |

---

## 2. Still owed to Mike — with the diagnosis

### 2.1 Enemies stack on each other  ⚠ diagnosed, reverted, baselines recorded

**Baselines** (`_BUILD_SOURCE/probe_stack.py`, no fix in tree):

```
stage 1   839 overlapping pair-frames, worst 71.9% burial
stage 4   127 overlapping pair-frames, worst 153.6% (one unit entirely inside another)
```

A relaxation pass (push half the overlap on X, capped, air units also easing on Y) took stage 1 to
**152 pair-frames / 51.8%** — a large improvement that still did not clear it.

⚠ **But it broke "a straight jet never leans", and that is the load-bearing finding.**
**Jet banking is derived from x movement** — a jet leans by how much its x changed this frame — so
an external nudge on x is indistinguishable from the jet choosing to turn. A separation force and a
facing model reading the same quantity cannot both be right.

**The fix needs the push to have its own channel.** Either a `_sepX` the draw applies *after*
banking is computed, or banking driven off the pattern's *intended* dx rather than the observed
one. That is a change to how every air unit is drawn, and it is the actual work here.

### 2.2 Boats only exist on the water  ⚠ failed twice, for two different reasons

`pickWaterX` is written and correct (the exact mirror of `pickLandX`). It needs no second mask,
because `_isLand` reads the stage plate's **alpha** and on Mike's 0811 plate the water **is** that
alpha — "not land" is "water", free. **It is not in the tree**; both call sites were reverted.

```
every frame   correct result (3,244 samples, ZERO on land) but 70 candidate scans per unit per
              frame changed what section 202's 200-second play simulation reaches. Reproducible,
              twice — not flaky.
at init       free, but did NOTHING: 955/955 still on land. Boats spawn ABOVE the screen, so the
              mask row derived from their y is a part of the plate they never sit on.
```

**The right form: once, on the first frame the boat is actually on screen (`y > 0`).** A boat that
starts in water and rides a river stays in water, so one solve is enough — but it has to happen
where the boat really is.

### 2.3 The pop-in  ⚠ half fixed, half reverted, formula known

**Shipped:** spawn y is the unit's **centre**, and the wave scripts were written for small craft —
`spawnEnemy('s1tankheavy', x, -34)` puts a 100px tank 50px into frame. Every spawn now clears the
top by its own half-height.

**Reverted:** the bigger half. Measured — stage 1 puts four `s1jetdelta_b` in at y 96/150 and
stage 4 seven units at y 82..236, **inside the frame**, materialising in open sky. Mirroring them
above the edge took both stages to **zero** pop-ins:

```js
c.y = -(c.h*0.5) - 6 - c.y;     // preserves a formation's ORDER and SPACING
```

⚠ A blanket lift broke *"crawling tank NEVER leaves the drivable band (47 violations)"*. For a
tracked unit, spawn y is **not a starting line — it is a position inside its band**, and the band
is what its movement model is written against. Excluding `c.ground / c._tracked / c._crawler /
c._sx` did **not** clear it, so at least one ground rig receives those flags somewhere other than
its spawn case. **Finding that predicate is the remaining work.**
Probe: `_BUILD_SOURCE/probe_popin.py`.

### 2.4 Not attempted

- **Per-enemy hitboxes.** Enemies collide as a single `w`/`h` box.
- **The bridge.** Mike: *"we no longer need the bridge, it doesnt exist."* It lives on the stage-1
  plate, which is now replaced — worth re-checking what actually still renders before removing code.
- **The stage-end screen.** Mike: *"still having problems fitting everything ... make your own with
  html and our fills and font and the portraits then."*
- **The confirm-window BODY text** still uses canvas text — it wraps and types out, and
  `stageText`/`msgText` have no wrap and return no measure, so it needs a line-breaker.
- **The atlas reorg** — still blocked on naming 5,064 keys, not on packing. See CLAUDE.md.
- **Stage 9** fields nothing: no `buildStagePlan` branch, not in `STAGES[]`.

---

## 3. Traps found this session — these cost real time

**⚠ Systems declared and never fired.** This was the dominant failure mode, five times over: the
quad-laser's muzzles, `_qlChg`, `enemyVolley` sharing a `fireCd` its unit's tick owns, `micon_`
asked of the wrong store, `lordshadows` registered and referenced nowhere. In every case the state
looked correct and no pixel moved. **Render it, then believe it.**

**⚠ `XART.rdy` is what STARTS a lazy load, and is false on that first call.** The stage 2 boss was
invisible for a whole drop because of it — it had a name, a health bar, HP and a working attack and
drew nothing. Two things follow: warm the art at spawn, and **never let a draw return false into a
chain that has no branch for your unit** — draw a silhouette. Wrong art is recoverable; no art is
not.

**⚠ A probe that polls art ready tests a case the game never starts in.** `probe_shipboss.py`
reported 97,966 drawn pixels for a boss that is invisible on a cold spawn, because it polls the
plate ready before measuring. That is the correct way to beat the lazy-load race and it made every
run test the wrong thing.

**⚠ The pools are REASSIGNED, not mutated.** `enemies = enemies.filter(...)`, and the same for
bullets. Wrapping `eBullets.push` to count rounds reported **0 on every stage including the
baseline** — the wrapper was discarded on the first cull. Tag the object, not the array.

**⚠ Comparing two runs measures wave randomness, not your change.** A before/after on bullet totals
read −56% on stage 4 purely from different waves spawning, and "2 new sideways bullets" that were
all a kind no volley fires. **Attribute to the code under test.**

**⚠ A confident comment is not a measurement.** The EQUIPPED box asserted *"micon_* DOES NOT EXIST.
NOT ONE OF THE 30 KEYS THIS ASKED FOR IS REGISTERED"* — which is how a wrong conclusion survived
three drops. They exist, in the third art store.

**⚠ A palette swap can pass its own numbers and still be wrong.** `ice_black` hit mean hue 0.55 and
saturation 0.25 — exactly on target — and rendered as uniform gunmetal slate. Value and saturation
must curve in **opposite** directions. Render the swap.

**⚠ An RGB histogram cannot see an alpha channel.** I called stage 7's sludge channel absent after
measuring the master converted to RGB. It had 8,412 alpha-0 px, the exact figure game.js already
records.

**⚠ Heuristics beat me twice, rendering caught both.** Identifying intact vs breached by
transparency-at-top gave the plates backwards. Measuring a text width before setting the font gave
the wrong centring.

**⚠ `_muz` is only decremented for enemies**, never for a sub-boss. Any sub-boss that sets it holds
its muzzle flash lit for the whole fight.

**⚠ `spawnSubBoss__inner` ASSIGNS the global and returns nothing.** Reading its return value reports
every miniboss as a failed spawn. Every fixture in `test_fl.js` reads `subBoss` for that reason.

**⚠ Renderer exhaustion is real.** Six stage masters and many `toDataURL` calls on one page crash
Chromium outright ("Target crashed"), silently losing every measurement taken before it. Use a
fresh browser per stage, and **print each result as it arrives**.

---

## 4. New tools

| tool | proves |
|---|---|
| `probe_shipboss.py` | the six ship bosses draw / flash / fire (frame diffs, not blit counts) |
| `probe_quadlaser.py` | each live cannon holds a lane, and killing one opens it |
| `probe_icons.py` | which icon key each weapon resolves, from which sheet, and whether it drew |
| `probe_volley.py` | the volley layer is in scope, called, and fires downward |
| `probe_types.py` | which enemy types each stage actually fields, and how many shoot |
| `probe_popin.py` | any unit whose top edge is inside the frame on its first drawn frame |
| `probe_stack.py` | worst enemy overlap, and boats-on-land — **with baselines recorded** |
| `probe_ticks.py` | whether the per-tick firing systems actually fire |

Build scripts: `build_shipbosses_0810s.py`, `build_weaponicons_0810s.py`, `build_stage7_0810t.py`,
`darken_sludge_0810y.py` (has `--restore`).

---

## 5. Where I would start

1. **The jet-banking channel** (2.1). It unblocks enemy separation, which is the most visible of
   Mike's complaints, and the fix is understood.
2. **Boats on water** (2.2) — smallest remaining job. `pickWaterX` is written; it needs one call in
   the right place.
3. **The pop-in predicate** (2.3) — find which ground rig gets `_tracked`/`ground` outside its spawn
   case, then the mirror formula lands.
4. **The bridge** — check what the new stage-1 plate actually renders before touching code.

---

## 6. Standing notes

- The four suite failures are long-standing and understood. **Always check the assertion COUNT** —
  a crash reports zero failures and looks like a pass.
- **Section 202 is flaky** (200s play simulation) and so is *"every volley fired is 5-8 rounds"* —
  both sample the quad-laser mid cannon-destruction. Re-run before blaming a change.
- The `validate_antipatterns.py` hook errors on **every** write; its script path does not exist.
  Harmless, but it makes every Write look like it failed.
- Two 404s at boot, still unidentified.
