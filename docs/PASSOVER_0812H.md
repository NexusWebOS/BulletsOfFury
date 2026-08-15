# Passover 0812h — Falva's twist, the colour overlay removed, the magenta, and the boats

Mike's six-item list. Four are fixed, one turned out not to be a bug, and two are **not started** —
listed plainly in §6 rather than implied to be done.

---

## 1. Falva does not twist — one unconditional line

> *"falva doesnt twist at all when I move her left and right."*

`_shipFrameKey` carried `if(pk==='falva') return 'ship_falva';` — no comment, no guard, no
condition. She alone never reached the pv lean or the br twist below it.

Measured across all nine pilots holding right: **every one ramps `_bank` to 1.0 and every one
resolves a `_br2`/`_br6` twist frame; Falva resolved the bare `ship_falva`.**

Removed rather than special-cased, because the reason it might have existed does not hold — her art
is all present and all distinct (pv0..4 at 152x280, br0/2/6 at 174x271, the same pv-vs-br shape
Cole has). Rendered all nine of her frames before deleting the line.

## 2. ⚠ NEVER RECOLOUR A MINIBOSS AT DRAW TIME — my own regression, one drop old

> *"The minibosses, dont ever color overaly them."*

0812e gave `shipBossDraw` a `pal` field and used it to theme stage 1 and stage 6 from existing
plates. **The field is gone and the mechanism with it**, so it cannot be reintroduced quietly.

Both units now use **authored art**: the South-Facing Ships pack's own Thorn Cruiser frame is
olive-green as drawn — a jungle cruiser without a single pixel changed — and the Olive Siegecarrier
likewise. Only their *recoloured* variants had ever been imported.

⚠ **Registered in code, not in `manifest.js`,** whose own first line says "Generated" and which
0810h already lost work to. `XART._src` is a plain key→path map, so adding to it in code is the
same registration by a route that survives the next regeneration.

## 3. The fire boss's magenta

180 purple pixels, in two symmetric patches at the wing roots plus scattered specks. **Not halos** —
interior fill, so the standing "convert a purple halo to a black edge" rule does not apply; a black
edge there would punch holes in the wing.

Each pixel takes the **median of its own non-purple neighbours**, iterated until the patch is gone
(5 passes, 0 unresolved). The wing adopts the surrounding authored fire palette rather than a colour
I picked. Before/after: `docs/proofs/reaver_magenta_0812h.png`.

## 4. The boats were stacking — and it is not what it looked like

> *"space them out thye cnanor stack on each other."*

Measured on a live stage-1 run, the stacking is **almost entirely naval**: corvette+landing craft
338 pair-frames, gunboat+patrol 96, worst overlap a full **1.00**. Not the jets. And **zero** of the
stacked pairs had `enter` set, which kills the obvious "they stack while flying in" explanation.

⚠ **THE CAUSE IS THAT EVERY HULL INDEPENDENTLY SEEKS THE NEAREST WATER.** `pickWaterX` had no
knowledge of the other boats and the naval tick calls it every frame, so two hulls in the same
neighbourhood converge on the same channel centre and hold there, one drawn on top of the other.
`enemySeparate` cannot undo that: it pushes them apart and the water pull steers them straight back.

The search now refuses an x another hull occupies, on the same row only. **Two passes, and the
second ignores traffic** — a narrow channel with a boat already in it must not return null, because
null means `_beached` and a beached hull *withdraws*. Trading a stacked boat for a vanished one is
the mistake 0809n already recorded: *"a metric can improve because the units left the field, and
that is not the fix."*

```
worst overlap  1.00  ->  0.37          boats beached: 0
```

The raw pair count rises because more boats now survive instead of withdrawing; the burial depth is
the number that matters and it more than halved.

## 5. Clouds spaced horizontally

`x: 40+rnd()*720` and nothing else, so two plates could land a few pixels apart and read as one
lumpy mass. The width is cut into `n` bands and each cloud takes one, jittered inside it, with the
band order shuffled against y so a stratified x does not read as a diagonal staircase. Measured
closest horizontal gap between vertically-near clouds: **60 / 66 / 85 / 176px** on stages 1/3/4/6.
Stratifying *guarantees* the spread rather than hoping for it.

## 6. ⚠ NOT A BUG, AND NOT DONE — read this before repeating my work

**"Enemies appeared out of thin air" — NOT REPRODUCED, and four probes were wrong before I knew it.**
Recorded in full because each looked convincing:

1. `probe_popin.py` reports **0 pop-ins on all 8 stages** — it watches `spawnEnemy`'s argument.
2. So I measured art readiness, and got "24 of 24 units art-cold, one blind for 5,220 frames".
   ⚠ **`e.art` holds a BASE** (`nef_s1_jungle_tank`); the draw appends a damage state. The base is
   never a key in any store, so `XART.rdy()` on it is false forever. That is what an always-false
   predicate looks like.
3. Trapping `enemies.push` found **zero** units pushed on screen — ⚠ and the trap was dead anyway,
   because **the pools are REASSIGNED, not mutated**, so the wrapper died at the first filter.
4. Tracking first-existence by polling finally worked and reported units at y=154, y=312 — ⚠ **but
   I was only checking y.** Their x was −28, 828, 846: they enter from the **sides**, off-screen,
   which is Mike's own stage-1 spec ("2, 1 on each side").

The one genuine exception is the naval group first existing at **y=40**, 40px inside the top edge.
Whether that reads as materialising is Mike's call.

**Still not started, both from this list:**
- **The end screen should not remain "paused"** (his 4th screenshot).
- **Minibosses and bosses should be more challenging and should attack.**

## 7. Suite

**2,543 assertions / 227 sections / 5 failures** — the same five long-standing ones. §220 now
asserts the *rule* (no ship boss or miniboss carries a draw-time palette) rather than the two units.
