# Passover 0811t — the jet-speed claim, verified — and a bug I put in two drops ago

Drop 0811o said the catch-all edge pin was the cause of CLAUDE.md's long-standing

> *"Jets: observed speed varies 96–138 even on `straight`; something outside `jetTick` displaces
> them."*

and then **did not verify it against the speed figure**. A cause that explains a symptom is not the
same as a cause that removes it, and this file has been burned by that distinction before. So it
was measured. Two of the three things it found were not what 0811o claimed.

`_BUILD_SOURCE/probe_jetspeed.py`, seeded, per-frame displacement over dt — **not** a velocity read
off the unit, which would report what `jetTick` intended and say nothing about what moved the jet
afterwards (the `probe_seam.py` mistake). Three arms: the pin always-on (the pre-0811o behaviour),
the pin gated, and gated with enemy separation off.

```
route      pin      sep  nominal   min   p50   p95    max   frame 1
straight   always   on        96    96    96    96     96        96
straight   gated    on        96    96    96    96     96        96
straight   gated    OFF       96    96    96    96     96        96

curveL     always   on        96    60    96   125  127.9        96
curveL     gated    on        96    60    96   125  127.9        96
curveL     gated    OFF       96    60    96    96     96        96

cornerLR   always   on        96    96    96    96  154.3    1365.4
cornerLR   gated    on        96    96    96    96  142.8        96
cornerLR   gated    OFF       96    96    96    96     96        96
```

---

## 1. ⚠ "VARIES 96–138 EVEN ON STRAIGHT" IS NO LONGER TRUE — STRAIGHT IS EXACTLY 96

Flat across every arm: min, median and max all 96. Whatever that figure measured, a straight jet
today flies at one airspeed and nothing displaces it. **The open item in CLAUDE.md can be closed on
the `straight` half.**

## 2. ⚠ AND THE CURVE VARIANCE IS NOT THE PIN — 0811o's IDENTIFICATION WAS ONLY HALF RIGHT

`curveL` reads 60..127.9 **identically with the pin always-on and gated**. If the pin were the
cause those two rows would differ. It is not the cause, and 0811o's note implying the two open
items were one bug is corrected here: they overlapped, they were not the same thing.

Turning **enemy separation** off collapses the high end to 96. So:

- the **>96 excursions (125–143) are `enemySeparate` (0811l)**, pushing a jet clear of another
  unit. That is the pass doing its job — a jet shoved apart genuinely covers more ground that
  frame — and it is capped at `SEP_CAP` 130.
- the **<96 dip (60) on `curveL`** is `jetTick`'s own `_entered` clamp at x=22. A curveL jet
  reaching the left margin has its x pinned, so its displacement falls to the y component alone.
  That is the deliberate "a jet must not leave sideways" rule from 0809a.

Every part of the residual is attributable to a mechanism someone chose on purpose. Nothing is
left hand-waved.

---

## 3. ⚠ AND THE MEASUREMENT FOUND A BUG I INTRODUCED IN 0811o

`cornerLR`, pin gated, still showed **one frame at 923 px/s against a 96 px/s airspeed** — a 15px
jump. Smaller than the 91px teleport 0811o removed, and the same bug.

0811o latched `_inField` the moment the unit's BOX was inside `[0, W]`. But the pin clamps to
`_edgeM` = `w*0.66`, which is a **stricter** bound than `w*0.5`. That leaves a band between the two
where the latch fires and the pin then immediately snaps the unit — measured at exactly `_edgeM`
minus half the width.

Latching on `_edgeM` instead makes the transition a no-op by construction: the unit is already
where the pin would put it, so the pin has nothing to do. `cornerLR` frame 1 is 96 now, and with
separation off the whole route is 96 flat.

**A fix that removes a 91px teleport and leaves a 15px one is not finished, and only measuring the
thing it claimed to fix would ever have shown that.**

---

## 4. Suite

**2,505 assertions / 221 sections / 4 standing failures**, plus the flaky *"every volley fired is
5-8 rounds"* — now failed on 3 of roughly 9 runs today with no code change between them. It belongs
with §202 and `curveL bleeds LEFT` in the order-dependent family; all three run long play
simulations and inherit globals from earlier sections. **They want lifting into standalone probes**,
which is a job in itself and is recorded rather than started here.

## 5. Still owed — all of it needs Mike

- **Cinematic aspect** — ten plates at 640x480 against a 480x512 playfield; cover crops 31.7% of the
  width. New plates are the only clean fill; `drawCutscene` already fits any aspect.
- **Boats** — fewer on screen since 0811n.
- **`STORY_TINT` vs `PILOTS[].tint`** — two colour tables, nine pilots, disagreeing.
- **0811s's stage assignments** — the four new volley shapes are built to his sentence, but which
  stage gets which is a call I made from the table. Every assignment is one row.
