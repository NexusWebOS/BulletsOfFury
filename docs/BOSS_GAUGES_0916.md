# 0916 — the gauges: a centred label, the shield's own bar, our own fills

Mike, 0916, with a shot of the BOSS tab:

> "text in boss bars and min boss bars shold centered all around including vertically. Shield
> should get it's own shield like boss bar, not the same as the boss bar. our own custom
> solid/shield fills too. and Shield should be colored Blue as text."

## 1. The label is centred in the SOCKET, not in the tab

The word was drawn at `ty + th*0.72` — 72% down the tab plate. The tab's dark socket is **rows
5..29 of 30**, measured off the plate's own pixels as the longest contiguous near-black run
(identical on all three tabs), so its centre is **17.5**, not 21.6. The word sat **4.6px low at
plate scale**, which is the air above it and the feet on the seam in Mike's screenshot.

⚠ **`stageText`'s `cy` IS THE CENTRE of the H-tall cap box** — it draws each glyph at
`cy - H/2 + gb.dy` — so handing it the socket's centre centres the lettering, and nothing else
needs an offset. `BMTAB.in = {dx:5, dy:5, w:194, h:25}` is that socket; the fit is against it too,
so MINI BOSS still cannot reach the rails.

Measured on the canvas, not asserted from the source: **0.00 px off centre vertically** on BOSS,
SHIELD and MINI BOSS, 1.0–1.5px horizontally (the odd pixel of an odd-width ink box).

## 2. The shield has its own bar

`bmbar_frame_shield` and `bmbar_tab_shield` are new cells on `ui_bossbar`.

⚠ **The shield frame is the boss frame HUE-ROTATED, not a new drawing and not a flat repaint.**
CLAUDE.md's rule is palette/luminance swaps, and 0906t's correction is *rotate* the hue, never set
it — setting one hue flattens the gradient that makes metal read as metal. +151° takes the rails
from gold→orange to pale cyan→deep blue with every bevel, rivet, lamp and hazard block intact, and
**the opaque colour count only moves 9,057 → 8,279 (0.91)**, which the builder asserts before it
writes (0906o: a halved palette is the signature of a shredded one).

The two bars are therefore the same object in two liveries — their well geometry is identical, so
`BMBAR.boss` still describes the shield bar's fill rect and the 0910c seating is untouched.

⚠ **The shield's well carries a faint hex lattice**, so an EMPTY shield bar still reads as a field
rather than as an empty HP bar.

⚠ **AND THE TAB IS BUILT FROM THE CLEAN FRAME.** `build_tab` samples a 60x8 patch of the well and
stretches it to 204x30 — harmless on flat black, catastrophic on a texture. The first cut latticed
the frame first and the tab came back with five stretched hexes the height of the whole plate. It
was obvious at 2x in the `--check` render and **no number in the build said a word about it**; the
tab now gets its own lattice at its own scale inside its own socket.

## 3. Our own fills

| key | what |
|---|---|
| `bmbar_fill_solid` | the boss HP fill: a solid tube, replacing the pack's hazard stripes |
| `bmbar_sf2_over/hex/plasma/low` | the shield: a blue hex field in four charge states |

⚠ **They are authored at a LUMINANCE RAMP, not at a colour.** `xartPalette` composites in `'color'`
— hue and saturation from the fill, luminosity from the plate — so a fill with a flat interior
tints to a flat slab. Each carries the lit top row, the body and the two shaded bottom rows the
authored fills on this sheet carry, which is the part that survives the swap and keeps the bar
reading as a tube at every stage's colour.

The four shield states are **one construction at four energies**, so a shield at 90% and one at 10%
are the same field with different power in it rather than two materials. (0912e's generated
"failing shield" quadrant was dropped for exactly that reason: at 13px it read as television
static.)

**`bmbar_fill_seg` stays registered** — putting the hazard stripes back on the HP bar is one key in
`bmbarFill`. Mike should see the solid fill in play and say which he prefers.

## 4. SHIELD is blue

`bmbarTabColour` — `#7fd8ff` for the shield, the existing `#ffe9b0` for BOSS and MINI BOSS.
Measured off the canvas in a live fight: the SHIELD ink averages **(137,192,213)** against BOSS at
**(197,176,128)**.

## 5. Measured

`_BUILD_SOURCE/probe_gauge_0916.py` — **25 ok / 0 fail**, real Chromium, 0 page or console errors,
on the Stage-2 Furnace Tyrant (a real barrier, so both bars are live) and the Stage-1 miniboss.

⚠ **The plates cannot be told apart by size** — both frames are 700x33, all three tabs 204x30,
every fill 578x13 — so `XART.get` is wrapped and the blit identified by the KEY it was asked for,
with the game context's own `drawImage` (never the prototype) recording where each landed.

Proofs: `docs/proofs/bossbar_0916/01_new_art.png` (the new cells),
`03_gauges_live.png` (BOSS over SHIELD in the Stage-2 fight), `04_mini_live.png`.

Suite **4,598 ok / 56 fail**, final summary reached — zero new failure names against a clean
worktree at `97265703`; the only difference is the documented stage-1 sand-tank flake, which
passed this run. Section 363 is 18/18.

Builder: `_BUILD_SOURCE/bossbar_shield_0916.py` (`--check` renders the cells without writing).
Atlas 704x274 → 704x418; `manifest.js` +7 cells.
