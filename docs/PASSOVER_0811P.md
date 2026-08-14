# Passover 0811p — "projectiles appear wobbly sometimes": exactly one system, and it is fixed

> Mike, 0811m: *'Projecticles - "Appear wobly" sometimes'*

I had this down as needing him to say which projectile, because pellets, missiles and the volley
layer are three separate systems. **"Sometimes" turned out to be the whole diagnosis** — a shape
that is always the same is an authored corkscrew; one that changes with the frame time is a bug —
so it was measurable without him.

---

## 1. Measured: every kind, twice, over the same simulated time

`_BUILD_SOURCE/probe_wobble.py` flies every enemy bullet kind for 1.4 simulated seconds — once at a
steady 1/60, once with the frame time jittering the way a real browser's does — and reports the
largest sideways excursion from the straight line between its first and last point.

**`lateral` is not itself a fault.** A swirl missile is *supposed* to corkscrew. What matters is
`drift`: how much that shape CHANGES between the two arms. A projectile whose shape depends on how
long a frame took reads as wobbling whenever the machine hitches and looks clean on a good run —
which is exactly "sometimes".

⚠ Both arms cover the same simulated DURATION, not the same frame count, or the jittered arm would
simply travel further and every kind would look broken.

```
kind                 steady   jittered      drift
mg                     0.00       0.00       0.00
shell                  0.00       0.00       0.00
dart                   0.00       0.00       0.00
ice                    0.00       0.00       0.00
flare                  0.00       0.00       0.00
minigunT               0.00       0.00       0.00
chaingunT              0.00       0.00       0.00
bolt                   0.00       0.00       0.00
emissile               0.00       0.00       0.00
groundup               0.00       0.00       0.00
emissile + swirl      27.68      22.84       4.84   <= the only one
```

**Ten of eleven fly perfectly straight and are frame-rate independent.** The pellets, shells, darts,
ice, flares and bolts do not wobble at all. One system does: the swirl missile — the black bomber's
quad launch from 0808w.

---

## 2. ⚠ TWO CLOCKS IN ONE MOTION

```js
const sw = Math.cos(b.t*7.4 + b._swPh) * b._swAmp * 1.9;   // phase advances on TIME
b.x += Math.cos(a-Math.PI/2)*sw;                            // offset accumulates per FRAME
```

The lateral offset was **added to position once per frame** while its phase advanced on **real
time**, and `b.x += b.vx` two branches down has no `dt` either — so the forward travel is per-frame
while the swirl is per-second. Any hitch desynchronises them.

The accumulated amplitude also scaled with frame rate: summing a cosine over frames gives
`(amp*1.9)/(HZ*dt)` — about 15px at 60fps and something else at every other rate. The corkscrew was
literally a different size on a different machine.

**The offset is an absolute function of time now, applied as its delta.** Integrating a cosine gives
a sine, hence the change of function; the `- sin(_swPh)` term keeps the missile starting ON its
line rather than one phase-step beside it.

⚠ **The amplitude constant reproduces the 60fps look deliberately.** Mike asked for this swirl and
signed it off — the fix is to make it frame-rate independent, **not** to "correct" the weapon into a
straight line. `SWIRL_AMP = 1.9*60/7.4` is exactly what the old accumulation produced at 60fps, and
the measurement confirms it:

```
                     steady   jittered      drift
before                27.68      22.84       4.84
after                 27.68      26.65       1.03      <- same shape, 79% less frame dependence
```

**Steady is 27.68 in both.** The look is unchanged to the decimal.

---

## 3. ⚠ THE RESIDUAL 1.03px HAS A KNOWN CAUSE, AND IT IS NOT THIS

`b.x += b.vx` has no `dt`: **the entire enemy bullet system moves per FRAME, not per second.** So
under a jittering frame time a bullet covers a different distance in the same simulated duration,
and `emissile`'s homing turn then integrates over a different path. That is the whole of the
remaining 1.03px.

It is left alone deliberately. Putting `dt` on that line changes the speed of **every enemy bullet
in the game** — every `spd` value in every `eShoot` call was tuned against per-frame motion — so it
is a balance change across nine stages wearing a bug fix, and it needs Mike. Recorded here so the
next person does not "discover" it and ship it quietly.

---

## 4. Suite

**2,491 assertions / 220 sections / 4 standing failures.**

## 5. Still owed from Mike's 0811m list

- **Cinematics wide/fullscreen** — not started. Structural; any resize moves the frame-for-frame
  handoffs `probe_arrival` / `probe_exit` measure, so it wants its own drop with those re-run.
- **Projectile variety / screen-filling patterns** — the largest remaining item, and design as much
  as code. Five boss patterns and the quad-laser's lanes landed this for BOSSES in 0810s; the
  ordinary roster is still the stage-3 change only. Needs a brief on which stages get which shapes.
- **Boats**: fewer on screen since 0811n. Mike has not seen it; if he wants more it is a wave-script
  change, not a placement one.
