# PASSOVER 0813D — the tanks were being displaced from outside their own pattern

Continuing Mike's list in order. **Item 4 fixed.** **Item 5 diagnosed and waiting on Mike** — the
remaining work there is a creative mapping, not code.

---

## 4. "tanks do not go sideways"

There were **two** lateral movers, and the obvious one was a decoy.

### The decoy

`case 'tankpatrol'` carried a block that re-targeted `e.x` every 1.6–3.2s, 30–80px toward the
player's lane, and eased the hull across:

```js
const want = clamp(e.x + clamp(player.x-e.x,-1,1)*rnd(30,80), 40, worldWidth()-40);
```

Removed. The tanks **kept sliding**, and one of them travelled *further* than before (55.6 → 132.5px).
That is the tell: the block used `rnd()`, so if it had been the cause the numbers would have moved
around, not stayed put at 55.6 across two runs.

### The real one

Trapped writes to a roadtank's `x` with a property setter and captured `new Error().stack` on each
one. **All 62 lateral writes came from `updatePlay:14580` — `enemyEntrySweep`**, which lays a
decaying lateral arc on top of whatever the pattern does and kept writing long after the entry flags
had cleared. The pattern case was not moving them at all.

> ⚠ This is the standing jet trap wearing different clothes. CLAUDE.md already records: *"Jets:
> observed speed varies 96–138 even on `straight`; something outside `jetTick` displaces them. A
> rescale inside `jetTick` does not fix it — the other mover runs after."* Identical shape, and it
> cost the same two wrong fixes before the trap was used.

A sweep is an aircraft's entrance; a tracked hull turns and drives. `enemyEntrySweep` now returns
early for `_vkind==='tank'`, which every ground vehicle sets at spawn.

| | before | after |
|---|---|---|
| lateral writes (traced unit) | 62 | **0** |
| moving frames | 61 / 103 | 3 / 14 |
| x span | 55.6 / 132.5px | 6.5 / 29.3px |

**Not claimed clean.** The span probe still sees 3 and 14 moving frames (max step 2.2px) while the
setter trap reports zero writes on the unit it armed. The trap arms on the FIRST tank it finds, so at
least one unit keeps a small residual that has not been chased. Do not read the 0 as "all tanks".

### ⚠ Three probe faults before any of this was true

Each produced a confident wrong answer:

1. **A matcher so loose it wasn't measuring tanks.** Matching on `e.art` and `e.wheels` as well as
   type swept up jets, mines, corvettes and landing craft — **14 of the 16 "sideways tanks" were not
   tanks**.
2. **Then one so tight nothing matched.** `/(^|[^a-z])(tank|apc)/` rejects `roadtank`, because a
   letter precedes "tank". Reported "NO TANKS MEASURED".
3. **Reading the wrong field.** The pattern lives on `e.pattern`; `e.pat` is undefined, so the
   pattern column printed `?` for every unit. The switch at 14596 is `switch(e.pattern)`.

Span alone also cannot tell a one-frame spawn snap from continuous sliding — the probe now tracks
moving-frame count and max single-frame step so the two are distinguishable.

## 5. "you didnt replace the bosses and minibosses on the other levels like I asked" — DIAGNOSED

Audited every boss and miniboss for whether it resolves its art (`probe_bossart.py`).

**Only stages 2, 3 and 5 run new-pack `nsb_*` bosses:**

| stage | boss | art |
|---|---|---|
| 2 | infernoreaver | `nsb_inferno_reaver` |
| 3 | cryospear | `nsb_cryo_spear` |
| 5 | voidbat | `nsb_void_bat` |

**Stages 1, 4, 6, 7, 8 still run legacy art** through `spawnBoss`'s `switch(kind)` — e.g. `damkeeper`
draws `ovbody_intact` (game.js:1705, 8744), not an `nsb_` plate. That is exactly what Mike is
describing.

And there are **five unassigned new-pack bosses**, against those five stages:

`nsb_blacksteel` · `nsb_jungle_cruiser` · `nsb_olive_carrier` · `nsb_siege_ember` · `nsb_thorn_rime`

All five resolve their art. They are simply not wired to any stage. The counts matching 5-to-5 is
suggestive but **which plate belongs on which stage is a creative decision and Mike's call** — the
names hint (`jungle_cruiser` → stage 1, `olive_carrier` → stage 4) but this file has been wrong about
names three times in two drops, and `siege_ember` is already in service as a stage-2 miniboss.
**Not guessed.** Mike names the mapping, the wiring is then mechanical.

> ⚠ `probe_bossart.py` also reported "8 minibosses have NO ART KEY AT ALL". **That is a probe fault,
> not a finding** — `SUBBOSS` is keyed by stage NUMBER (`1:{at:0.62,...}`) and holds its art under a
> different field than the `key`/`art` the probe looked for. The miniboss audit is unfinished; do not
> quote that line.

## Suite

**2,636 assertions / 234 sections / 5 failures** — the same long-standing five, across all three runs
in this drop.

## Still open — items 6-9

6. Purple halos on level 7 (rule: converted to a black edge, never deleted).
7. Wrong region highlighted for level 5 — `CMAP_REGIONS.stage05`, game.js:32813.
8. Square boxes around background objects on space/sky. Repro: `docs/proofs/stage5_scrollwalk.png`.
9. Old chain-lightning graphic in stage 8's scrolling terrain.

Plus **item 3**, blocked: there is no bridge asset anywhere in the manifest, and `cfg.props` holds
exactly one prop game-wide (`nst4_crash_overlay`, the approved pileup, drawn 1:1).
