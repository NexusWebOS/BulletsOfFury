# Passover 0812i — the minibosses were firing, but not at you

> Mike: *"make them a little bit more challenging and make them attack. same with my bosses."*

Measured first. Every miniboss was already putting **3.2–4.1 rounds a second** in the air — and
**0.00 to 0.31 of them per second anywhere near the player.** They were not quiet. They were
shooting somewhere else.

---

## 1. ⚠ TWO PATTERNS WERE WRITTEN AS IF `_shipShot` TOOK AN ANGLE

```js
_shipShot(b.x, y, Math.PI/2 + i*0.22, 2.2, 11)     // fan2, before
_shipShot(b.x, y, Math.PI/2 + t,      2.4, 11)     // pincer2, before
```

`_shipShot(x, y, vx, vy, w)` takes **velocity components**. `Math.PI/2 + off` was going straight
into `vx`, so every round in both "fans" left at **vx 0.91 … 2.23 — all of them to the right**, at
nearly the same angle. A fan that is a one-sided spray, and a pincer that only ever pinched one way.

Real components now, fanned about straight down:

```js
for(let i=-3;i<=3;i++){ const a=i*0.22; _shipShot(b.x, y, Math.sin(a)*2.2, Math.cos(a)*2.2, 11); }
```

`§223` asserts this as **symmetry** rather than as a code string — the vx of a pattern's rounds
must sum to ~0 and span both signs, which is the property a fan has and a spray does not, and which
catches the same mistake written any other way. Measured after: fan2 7 rounds, sum 0, 3 left 3
right; pincer2 6 rounds, sum 0, 3 and 3.

## 2. And they now shoot AT you

The patterns above are all fixed geometry — columns, lanes, radial arms — and that is **deliberate**:
their own comments describe doorways and safe lanes, and a readable pattern is what makes a fight
learnable instead of a wall of bullets. So none of it was touched.

An **aimed pair** is added on top, on every other volley. That is what turns "bullets are happening"
into "it is shooting at me", and the every-other cadence leaves the authored shape legible between
aimed beats.

```
                          threat/s  (rounds reaching the player's row, per second)
MINIBOSS   stage 1..8     0.87  0.87  1.38  0.62  1.84  0.64  1.82  2.02
BOSS       stage 1..8     2.22  1.78  1.20  4.51  4.18  6.87  7.22  0.44
```

⚠ **STAGE 8's BOSS IS THE OUTLIER — 0.44 threat/s and 4.2-second silences**, the least threatening
unit in the game while being the last one you fight. That is `vileexistence`/APOSTLE COCOON, which
Mike has already called *"filler shit"* and not yet built, so it is consistent rather than new — but
it is now measured, and it is the number to beat when it does get built.

## 3. ⚠ Two more measurement faults, both of which produced a wrong answer first

- **THREAT WAS COUNTED AT THE BULLET'S BIRTH.** The first metric asked "was this round spawned in
  the player's column", which an aimed shot — fired from the boss, *toward* the player — can never
  satisfy. It reported 0.00 for units that had just been fixed. A round counts once now, the first
  time it actually reaches the player's row.
- **THE SUITE STUB FIRED THE AIMED PAIR TOO.** `_sbStep:1` makes the step land even, so the aimed
  volley joined the sample — and it is *supposed* to be asymmetric. A correct fan measured as
  lopsided. `_sbStep:0` isolates the pattern.

## 4. The end screen — NOT REPRODUCED

> *"4th screenshot - end screen, shouldnt remain paused."*

Played stage 1 and 2 end to end in the real update+draw loop:

```
stage 1   miniboss 49s   killed 56s   boss 74s   ->  FLYOVER at 87.5s
stage 2   miniboss 44s   killed 50s   boss 59s   ->  FLYOVER at 100.2s
```

The flow completes. ⚠ Two probe setups had to be corrected before that was true, and both had
looked like the bug: **`drawLevelMaster` is what advances `mapScroll`**, so a probe that pumps only
`updatePlay` measures a stage that never moves; and **the miniboss HOLDS the scroll until it dies**
(0801hn), so a probe that never fires freezes the level itself and then reports the level as frozen.

I cannot see what he saw. **Mike: which moment is it?** — the stage-clear panel, the flyover, the
map after a level, or the cutscene?

## 5. Suite

**2,551 assertions / 228 sections / 5 failures** — the same five long-standing ones.
