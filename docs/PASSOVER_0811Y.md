# Passover 0811y — the machine gun pellet: a blob and a streak, swapped 7× a second

> Mike, clarifying which projectiles look wobbly: *"I meant the machine gun pellets sorry"*

That correction mattered. **The 0811v wobble fix did not touch these.** It repaired
`atan2(vx, -vy)` on the arsenal branch — which is gated `if(b._boss && !b._noArsenal)`, i.e. **boss
bullets only**. Ordinary pellets from planes, ships and jets take the FIRETYPES path and never went
near it. Two different bugs wearing one description.

Proof: `docs/proofs/pellet_reel_0811y.png` (the art) and `pellets_0811y_live.png` (in flight).

---

## 1. ⚠ THE PELLET WAS TOGGLING BETWEEN TWO DIFFERENT SHAPES ON THE WALL CLOCK

```js
art:(b)=>['mfx_mg_2_0','mfx_mg_2_2'][(floor(performance.now()/70) + b._ph) % 2]
```

Those are not two poses of one thing. Measured:

```
mfx_mg_2_0    18x20    ink 123      a compact blob
mfx_mg_2_2    20x45    ink 380      a long thin streak      (+209% ink)
```

`mfx_mg_<fam>_0..4` is a **birth sequence** — a round blob that stretches into a tracer
(18x20 → 23x33 → 20x45 → 33x51 → 34x57). Alternating frame 0 against frame 2 is not playing it;
it is flipping between a blob and a streak seven times a second. At the fixed draw height of 16 that
swings the round's on-screen **width between about 14px and 7px**, in flight.

That is the wobble, and nothing about it is trajectory — which is exactly why 0811p measured every
path as geometrically perfect and still had not found it.

Measured through the real picker, one round's first 0.40s:

```
before (wall-clock toggle)   0 2 0 2 0 2 0 2 0 2 ...
after  (own age, birth)      0 0 0 1 1 1 2 2 2 3 3 3 4 4 4 4 4 4 ...
                             monotonic, all five frames, holds on the tracer
```

⚠ **AND THE PELLET WAS THE ONLY FIRETYPE DOING THIS.** Every sibling — comet, homing, missile —
already animates off the round's own age `b.t`. Only the pellet used `performance.now()`, so two
rounds fired a frame apart were locked in step with each other and out of step with their own
flight. It now plays its reel from `b.t`, once, then holds.

---

## 2. ⚠ FIVE COLOUR FAMILIES WERE AUTHORED. FOUR HAD NEVER BEEN DRAWN.

> Mike: *"you can have alot of fun by palette wapping them to red, blue, green gold etc"*

`mfx_mg_0..4` are **red, blue, orange, green and white**, five frames each — **25 registered plates,
of which the game used two.** No palette swap was needed at all; the art was already there and
unreferenced.

`PELLET_FAM` gives each stage the family matching the identity the rest of the file already asserts
(*"a level-3 shot is ice, a level-8 shot is necro"*):

```
1 orange   2 red   3 blue   4 orange   5 white   6 blue   7 green   8 red   9 white
```

Verified: all 25 plates resolve, none missing. `T.glow` may be a function now so the halo follows
the plate — otherwise a green tracer would sit inside an orange glow.

Seen in flight on stages 1, 3 and 7: the reel reads as a round striking and stretching away, and
the colours suit their stages.

---

## 3. Suite

**2,505 assertions / 221 sections / 5 failures** — unchanged from the deterministic 0811u baseline.

## 4. Still owed

- **Animated 16-bit shaded glows** — the remaining half of Mike's original message. The pellets now
  carry a per-family glow colour, but it is a flat halo, not the shaded animated effect he
  described.
- The rest of the arsenal (`mfx_ea_`, `mfx_hom_`, `mfx_emr_`, comets) has not been checked for the
  same class of fault. Given the pellet used a different clock from every one of its siblings, and
  given four of five colour families sat unused, **the other families are worth the same audit** —
  both faults were invisible until someone rendered the reel.
- `nlz_<lv>_m0..5`, the laser muzzle reel, still does not exist at any level.
