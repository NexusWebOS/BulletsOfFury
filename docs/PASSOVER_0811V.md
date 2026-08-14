# Passover 0811v — the wobble, actually found: a 48° sprite flip

> Mike, asked which projectiles look wobbly: *"almost all of them do. bullets from the planes,
> ships, jets, level 1 boss etc."*

Drop 0811p measured every projectile PATH, found ten of eleven geometrically perfect (0.00 lateral,
frame-rate independent), fixed the one that was not, and reported the item closed. **That
measurement was correct and it was answering the wrong question.** A bullet can travel a dead
straight line and still wobble, because the thing that wobbles is the SPRITE.

---

## 1. ⚠ `atan2(b.vx, -b.vy)` PUTS STRAIGHT-DOWN ON ITS OWN DISCONTINUITY

The arsenal / boss projectile branch — the one whose own comment says the arsenal *"wins wherever
it has art"*, i.e. most bullets in the game — rotated every round by:

```js
const _ang = Math.atan2(b.vx, -b.vy);
ctx.rotate(Math.max(-0.42, Math.min(0.42, _ang)));
```

Negating `vy` puts straight-down travel at **±π**, not at 0. In a vertical shmup that is exactly
where almost every bullet lives. Computed:

```
   vx      atan2(vx,-vy)   clamped        atan2(vx,vy)   clamped
 -0.005       -3.1396       -0.420           -0.0020      -0.002
  0            3.1416       +0.420            0.0000       0.000
 +0.005        3.1396       +0.420           +0.0020      +0.002
 +0.300        3.0222       +0.420           +0.1194      +0.119
```

**Two faults from one sign:**

1. **Every straight round is drawn permanently tilted at the clamp** — 0.42 rad, **24°** — instead
   of pointing where it is going. Note the whole column: *every* value of `vx` clamps to ±0.42, so
   the angle carries no information about the round's actual heading at all.
2. **The instant `vx` crosses zero the sprite snaps between +0.42 and −0.42 — a 48.1° flip.** Any
   round whose lateral drift changes sign does this: homing missiles correcting, swirl rounds,
   spreads, anything with a sine on it.

`atan2(vx, vy)` is 0 for straight down and continuous through it — the same crossing now moves
**0.004 rad**. It also matches this branch's own stated contract (*"NO FLIP … the plate is drawn
exactly as authored"*): straight down is now rotation 0, i.e. drawn as authored.

### ⚠ THE OTHER `atan2(vx,-vy)` SITES ARE NOT THIS BUG — DO NOT "FIX" THEM

- **20558 / 20756** feed a 24-direction sprite INDEX through `mod 24`. `+π` and `−π` both land on
  index 12, so the wrap makes them continuous. Correct as written.
- **21320** rotates with **no clamp**. `π` for straight-down is the right convention for a sprite
  authored pointing UP. Correct as written.
- **5775** is enemy FACING and its comment states the convention deliberately.

The fault was `atan2(vx,-vy)` **combined with a ±0.42 clamp** that assumes a near-zero angle while
the formula produces ±π. The clamp is what turned a convention into a bug.

---

## 2. ⚠ AND MY FIRST HYPOTHESIS DID NOT SURVIVE ITS OWN MEASUREMENT

I first said the wobble was bilinear smoothing on a rotated sprite, by analogy with the ship hulls
in 0811r. I built `probe_bulletshimmer.py` to prove it and **it came back the other way** —
25.4% churn smoothed against 28.5% nearest, i.e. worse under the fix I had just made. The metric
counts discrete per-pixel differences, which nearest-neighbour *maximises* by snapping whole pixels
instead of smearing fractions. It was measuring the wrong property, and the honest reading is that
it did not support the claim.

**The nearest-neighbour change on the bullet pass is kept, but NOT as the wobble fix.** It stands on
the same ground as the hulls: this file states a nearest-neighbour pack contract at a dozen other
draws and the bullet pass never set it, and rendered side by side the sprites are visibly crisp
pixel art instead of blurred (`docs/proofs/bulletshimmer_0811v.png`). That is a legitimate
improvement and a separate one. **The wobble is §1.**

Recorded because the sequence matters: a confident analogy, a probe built to confirm it, and a
result that refused. The analogy was doing the work, not the evidence.

---

## 3. Suite

**2,505 assertions / 221 sections / 5 failures** — unchanged from the deterministic baseline
established in 0811u.

---

## 4. NOT DONE — the rest of Mike's message

He asked for three more things in the same breath and none of them are in this drop:

- **Palette-swap the projectiles** to red / blue / green / gold. The machinery exists
  (`xartPalette`, and the standing rule is palette/luminance swaps, never overlays) but which
  round becomes which colour is a design table, not a guess.
- **16-bit shaded pixel glows that animate.** A real effects system, and the biggest of the three.
- **The level-3 laser is underwhelming, and all lasers need a consistent yet upgradeable look as
  they advance in level.** This is the most specific of the three and the best next job — it has a
  clear success condition (five tiers that read as one weapon getting stronger) where the other two
  need his colour calls.

Those are the next drop. Nothing about them is started, and this passover does not claim otherwise.
