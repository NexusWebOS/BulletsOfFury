# Passover 0812d — the nca_87 pack on the machine gun and the spread

> Mike: *"nca_87 - these should replace the machine gun and spread projectiles immediately. palette
> swap the bullet and glow to where the glow is as we had it - lvl 1 orange lvl 2 blue lvl 3 green
> lvl 4 white lvl 5 red lvl 6 gold lvl 7 black lvl 8 purple. palette swap the bullet to mesh
> properly with these colors each time - level 1 could be brownish, level 2 could be silver, level 3
> could be white, level 4 could be black, lvl 5 could be the bullet standard color itself. 6 use
> blue, and 7 use red."*

Done for both weapons, all eight tiers.
Proof: `docs/proofs/p87_mg_levels_0812d.png`, `p87_spread_levels_0812d.png`, `p87_size_0812d.png`.

---

## 1. ⚠ nca_87 IS NOT SLICED — it is one whole-sheet key

There are no cell keys, so `XART.rdy('nca_87_bullet_1')` would be false forever and any attempt to
address it by name silently draws nothing.

The grid was **measured off the sheet's own alpha**, not read off the thumbnail: four bands at
`10..181, 202..373, 394..565, 586..757` in both axes — a clean 4×4 at a **192 pitch**. Cells are
indexed against that pitch directly, so no manifest edit is needed — which is also correct on its
own terms, because the manifest is generated and the edit would be lost on the next regeneration.

What each row is, measured as **ink per cell** rather than eyeballed:

```
row 0  MUZZLE FLASH     8842 / 7581 / 10081 / 5076     a reel, peak at frame 2
row 1  ROUND IN FLIGHT  w 50 / 33 / 26 / 38            <- see below
row 2  IMPACT           7062 / 11269 / 3947 / 929      grows to frame 1, then decays
row 3  [0] straight   [1] +46.2deg   [2] -46.2deg   [3] a second, wider flash
```

⚠ **ROW 1 IS THE 0811y TRAP AGAIN, AND WORSE.** 50px wide at frame 0 against 26px at frame 2 — a
**92% swing**. Looping that, or driving it off `performance.now()`, makes the round throb: exactly
the *"projectiles appear wobbly"* that 0811y already fixed once for the enemy pellet. The reel runs
**monotonically off `b.t` and holds on the last frame** — fat leaving the barrel, streamlined at
speed. Two rounds fired a frame apart animate independently, as they should.

⚠ **THE DIAGONALS ARE AUTHORED AT ±46.2°, NOT 45.** Measured as the principal axis of each cell's
ink. The spread picks the **nearest authored pose and rotates only by the residual** — the idiom the
helix pack (`nhxv_`) already established here — so hand-pixelled diagonals are drawn as drawn
instead of being resampled through an arbitrary angle.

## 2. ⚠ The pack had to go FIRST, or it would never have drawn

Both arms of `drawBullets` are chains of five fallbacks that each `continue`. **Drop 0720 lost a
whole art pack to exactly this** — `nmg_` ran first and returned, so the authored per-level art
below it was unreachable, and it survived unnoticed because the glow kept a hint of the tier.
`§219` asserts the **order**, not a line number.

## 3. The palette

`xartPalette` already had what this needs and it is not the obvious path:

⚠ **WHITE AND BLACK MUST NOT GO THROUGH THE HUE SWAP.** The default is a `'color'` composite — hue
and saturation from the fill, luminosity from the plate — and an achromatic fill has no hue to
give, so white and black would both come out the **same grey**. `xartPalette` carries two special
cases (a `multiply` for black, a colour-then-`screen` pass for white); levels 3 and 4 route through
them, and `§219` pins that they still exist.

⚠ **ONE SHADOWED DRAW WAS NOT A GLOW.** Measured the halo per tier off a render: every level came
back within a few units of the background (14..26 of 255) — the colour was technically present and
visually absent, and **level 8's purple read as blue**, because the round's own baked blue-white
casing outweighed it. The halo is its own pass now: a wide soft shadow, a tighter hot ring, then the
clean sprite. That is what puts the colour *around* the round instead of averaging it in.

⚠ **SIZE WAS PICKED AGAINST THE SHIP**, not in the abstract — rendered at 32 / 48 / 67 beside Cole's
airframe. At 32 the round is a sliver; at 67 consecutive rounds merge into one unbroken bar. 48 is
about a quarter of the fuselage width, which is where the capsule reads as a capsule.

⚠ **LEVEL 8's BODY IS MY CHOICE, NOT MIKE'S.** He gave bodies for 1–7 and said only that 8 is
Cole's fusion cannon with a purple glow. It uses the **standard authored gold** — hottest against
violet and the least invention. **Say the word and it changes.**

Levels 6, 7 and 8 needed no new gating: `run.wlevel` is already clamped to `colePilot() ? 8 : 5`
at every read site.

## 4. ⚠ An assertion matched documentation instead of behaviour — the third time

`§219`'s "is the pack tried before the older fallbacks?" check failed on correct code. The
machine-gun arm **opens with a long comment that names `nmg_` and `mfx_mg_` in prose**, so the
search was answering a question about a sentence. Raw text put them at 373/730 against the pack at
3504; with comments stripped they sit at 1186/1034 against the pack at **97**. It strips comments
first now.

## 5. Suite

**2,526 assertions / 224 sections / 5 failures** — the same five long-standing ones.

## 6. Not done, and deliberately

- **The muzzle flash (row 0) and impact (row 2) reels are identified and available but not wired.**
  The ask was the projectiles; the cells are named in the code so wiring them is a small job.
- **The other sheets Mike named are recorded, not used yet.** `nca_75` — Freezer's fire/ice ball
  ICONS; `nca_69` — the fire/ice ball ITSELF; `nca_77` — also his fire/ice ball; `nca_66` — more
  effects. These are the art for the **still-open level-2 icebreath / level-3 fireorb icon bug**
  from his earlier list, where the wrong icon shows from a powerbox. That is the obvious next job
  and it now has its source.
