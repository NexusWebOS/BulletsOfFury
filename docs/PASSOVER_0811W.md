# Passover 0811w — the laser: one real fix, four findings, and an attempt I reverted

> Mike: *"level 3 laser looks underwhelming and needs an upgrade. all the lasers need to have a
> consistent yet upgradeable look as they advance in level."*

**I did not deliver the visual upgrade.** I tried twice, made it worse both times, and reverted. What
came out of it is one real fix and four measurements that say the job is art, not code. Written up
that way rather than dressed as a win.

---

## 1. ⚠ THE LIVE LASER HAS BEEN FIRING OUT OF NOTHING — fixed

The v2.2 branch reaches for a muzzle sprite `nlz_<lv>_m0..5`. **The manifest holds ZERO of those, at
every one of the five levels** — measured, not assumed. And the legacy muzzle orb further down the
same function was explicitly gated off whenever the v2.2 beam was live:

```js
if(!_v22beam){ ...muzzle orb... }        // and _v22beam is true at every level
```

Between the two, the beam emerged from empty space at the ship's nose. The orb is ungated now. It is
drawn code that already existed and was authored for this — it only ever needed to be allowed to
run. No new art, no placeholder.

---

## 2. ⚠ THE FIVE PLATES ARE THE SAME PICTURE IN FIVE HUES

Measured off the authored art:

```
level   src       ink%   mean luminance   core width
  1    64x320     61.0        179            61%
  2    64x320     59.6        161            61%
  3    64x320     62.5        175            63%
  4    64x320     57.0        189            59%
  5    64x320     61.8        157            63%
```

Structurally identical on every axis. **The art cannot carry an upgrade** — only the hue changes.
Level 3 is a flat poster green whose lit centre is barely brighter than its body, which is exactly
why it is the one Mike singled out; level 4 reads as dirty grey rather than white-hot. All five
also carry uncleaned white/magenta specks along both edges.

## 3. ⚠ AND THE WIDTH ALREADY GROWS — I NEARLY "FIXED" IT TWICE

`pShoot` sets `beam.w = 14 + lv*4` on every shot, so the beam genuinely runs **18px at level 1 to
34px at level 5**, and that width drives the hit column as well as the draw.

My first probe drew every tier at a constant 14 and produced a strip where all five looked the same
size. **A probe that invents its own scale is not showing the game**, and I was one step from
building a width progression on top of one that already worked. Corrected, and the note is in the
probe so the next reader does not repeat it.

---

## 4. ⚠ WHAT I TRIED, AND WHY IT IS REVERTED

Since the art is uniform, I put the tiering in the draw: an animated outer glow, a widening warm
halo and a white spine, all scaled per level. Rendered, the beams came out as **near-white slabs
washing out most of the frame**. I cut the layers back and it was still a white column.

Two things I got wrong, both worth keeping:

- **Additive layers compound far faster than their alphas suggest.** Three `lighter` passes at
  0.2–0.5 over an authored plate that already carries its own light, plus the energy-pulse blobs
  that were already there, saturate to white long before any single layer looks strong.
- **I had no baseline.** I rendered the *art* before changing anything but never the *live beam*, so
  I spent two iterations tuning against nothing. The before/after discipline that has worked all
  session — and that I have written into three passovers — I simply skipped here.

⚠ **AND THE MEASUREMENT I REACHED FOR CANNOT WORK IN THIS RENDERER.** To size the beam objectively I
drew the frame with and without it and diffed the row. It reported ~475px lit at every tier, i.e.
the whole screen: `drawWorld` reads `performance.now()` directly for water frames, clouds and
scanlines, so two draws of one tick never match. **That is documented in CLAUDE.md from drop 0811m,
by me, and I walked into it again.** The crop is the evidence for anything visual here; the only
number worth quoting is `beam.w`, which is read off the object rather than inferred from pixels.

Everything visual is back to exactly what it was. The only behaviour change in this drop is §1.

---

## 5. What the laser actually needs

Not draw tuning. The plates are identical, and every intensity I add stacks on top of pulses that
are already there. **"Consistent yet upgradeable" wants art with per-tier internal contrast** — the
same silhouette at all five levels, with the lit core growing hotter and the shading deepening as
the tier rises. That is Mike's to author; the draw already scales width, and the moment the plates
differ the tiering will read on its own.

Two things he could hand over that would land immediately:

- **`nlz_<lv>_m0..5`** — the muzzle reel the code has been asking for since v2.2 and has never had.
  The lookup is already written; art alone switches it on.
- **Repainted `nlz_3_*` and `nlz_4_*`** — the two whose internal contrast is lowest.

## 6. Suite

**2,505 assertions / 221 sections / 5 failures** — unchanged from the deterministic 0811u baseline.

## 7. Also still owed

Palette-swapping projectiles to red/blue/green/gold and animated 16-bit pixel glows — the other two
things in the same message — are **not started**. On the evidence above I would want Mike's colour
table before touching either, since both are the same class of change that just failed here.
