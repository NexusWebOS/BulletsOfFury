# Passover 0811x — the laser, done properly: two palette swaps, with a real before/after

0811w failed at this and said so. The failure was **method, not impossibility**: I had tried to add
tiered light on top of the plates, additively, with no baseline to compare against. This drop does
the same job the way the file's own rules say to.

Proof: `docs/proofs/laser_tiers_0811x_before.png` / `_after.png` — all five tiers, live, on stage 1.

---

## 1. ⚠ THE BASELINE I SHOULD HAVE TAKEN FIRST

0811w rendered the **art** before changing anything and never the **live beam**, so two rounds of
tuning ran against nothing. This drop captured all five tiers firing on the real stage first, and
two faults were obvious the moment they were side by side and had nothing to do with tiering:

- **Level 4 is pure white** — `#ffffff` plate, `#ffffff` glow. Over stage 1's bright blue sea it
  reads as a hole punched in the screen rather than a beam. It is the only tier with no colour.
- **Level 3 is a pale mint** — `#5fe07a` over `#8fffa0`. Low saturation against a blue background,
  so it recedes exactly where the other tiers pop. That is the one Mike named.

The other three are his own colours and read fine.

---

## 2. Two palette swaps — the sanctioned mechanism, not an overlay

> Mike: *"you can have alot of fun by palette wapping them to red, blue, green gold etc"*

`xartPalette(key, hex)` composites with **`'color'`** — hue and saturation from the fill,
**luminosity from the plate** — then `destination-in` to re-mask. The authored shading and the
six-frame animation survive intact. That is the standing palette/luminance rule in this file, and
it is precisely what a `source-atop` flood would have destroyed; the same flood once repainted the
BOF font's drop shadow and turned every **E into a B** for three drops.

```
level 3   #5fe07a pale mint  ->  #25c94a saturated green
level 4   #ffffff white      ->  #ffc21a gold        (a colour Mike named)
```

Cached per key+mode, so six frames × two levels is twelve canvases built once.

⚠ **ONLY THE TWO THAT MEASURE WEAK WERE TOUCHED.** Swapping all five to a scheme of my choosing
would be redesigning Mike's weapon rather than fixing what he pointed at.

⚠ **AND `col`/`glow` MOVED WITH THEM.** The energy pulses, the hot core's shadow and the muzzle orb
all read from that table — leaving it on the old values would have put a green beam inside a
pale-mint muzzle. One table, two entries, both moved together.

The set now reads **orange → blue → green → gold → red**, every tier with a white-hot core, widening
18px → 34px. Consistent in structure, upgradeable in width and heat.

---

## 3. ⚠ AND THE PROBE HAD TWO FAULTS THAT LOOKED LIKE GAME BUGS

Both worth keeping, because both invented a defect that did not exist:

- **Levels 1 and 2 "did not draw".** The probe walks all five tiers on one page, and `pShoot`
  early-returns while `player.fireCd` is counting down — so the first tiers produced no beam and
  their crops came back as bare terrain. State carrying between iterations, exactly the way the
  suite's own order-dependent fixtures do. It clears `fireCd` and retries until a beam exists now.
- **The crop framed the wrong column.** It cropped at the beam's WORLD x while the canvas is in
  SCREEN space; `drawWorld` runs under `translate(-camX)`. Same world-vs-screen fault this file
  already records for the launch seam, the outbound routes and the dialogue window — the fourth
  instance, and the first one to appear inside a probe rather than the game.

Also carried forward from 0811w and now written into the probe's header: **no frame diffing.**
`drawWorld` reads `performance.now()` directly, so two draws of one tick never match and a
with/without diff reports the whole row. The crop is the evidence; the only number quoted is
`beam.w`, read off the object rather than inferred from pixels.

---

## 4. Suite

**2,505 assertions / 221 sections / 5 failures** — unchanged from the deterministic 0811u baseline.

## 5. Still owed

- **`nlz_<lv>_m0..5`** — the muzzle reel the code has asked for since v2.2 and has never had (zero
  entries at all five levels; 0811w ungated the drawn orb as a stand-in). The lookup is written;
  art alone switches it on.
- **The plates' internal contrast** is still identical across tiers (ink 57–62%, core width 59–63%).
  Colour now separates them; only new art will make level 5 look *hotter* than level 1 rather than
  merely wider and redder.
- **Uncleaned white/magenta specks** along both edges of all five plates.
- **Projectile palette swaps and animated glows** for the rest of the arsenal — the other half of
  Mike's message. `xartPalette` is now proven on a moving, animated, per-frame sprite, which is the
  hard case; the same approach should carry to `mfx_`/`nep_` rounds. Not started.
