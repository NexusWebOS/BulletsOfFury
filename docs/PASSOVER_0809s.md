# Passover 0809s — the arcade plate's panels are drawn, not baked

Mike, looking at the Decker plate: *"Use the text we have in-game for font, use the dialogue box
for the bottom, underline the top text dont make a faux text window."*

## What was actually in the art

The pack ships three files per pilot: `-arcade-background-640x480`, `-pilot-layer`, and a
flattened `-arcade-intro-640x480` composite. Diffing the composite against `background + layer`
shows both offending panels live **only in the composite**:

| panel | background has | composite adds |
|---|---|---|
| top, x 351–623 y 41–84 | nothing — clean tech wall | a rounded faux box + PILOT DEPLOYED in a mono face |
| bottom, x 329–623 y 341–455 | a **proper authored HUD frame**, empty | a plainer rounded box painted **over** it + the name in a generic bold sans |

The bottom one is the worse offence: the pack's own flattening covered a nicer frame than the box
it drew. Both panels sit at identical coordinates on all nine plates.

## The fix

All nine `aintro_*.png` are rebuilt as **background + pilot layer only**, and the panels are drawn
at runtime by `drawAintroPanels(k, alpha)`:

- **top** — `PILOT DEPLOYED` in the BOF face with a rule under it in the pilot's tint. No box.
- **bottom** — `dlg_window`, the same authored panel the dialogue path uses, with the name in the
  pilot's tint and the affiliation beneath it.

It mirrors `attDrawFit`'s CONTAIN transform exactly so the panels track the plate at any viewport.

Both lines **shrink to fit**: `JUGGERNAUT` and `PRINCESSES OF THE SKY` both reach the frame at the
nominal size, and trusting the longest string to be short enough is how you get text kissing a
border on one pilot in nine.

## Two things this also bought

**The Decker/Freezer swap is now structurally impossible.** The name is no longer a picture — it
comes from the pilot key through `PILOTS`. There is nothing left to mis-file.

**⚠ The affiliations existed only as baked pixels.** `ORDER OF THE MATRIX`, `PRINCESSES OF THE
SKY`, `BROTHERHOOD OF FURY`, `STRATEGIC ORDNANCE`, `FURY FOUNDER` — none of these are in `PILOTS`
(whose `role` field holds ability names like `FROSTBITE`, a different dataset entirely). They were
read off the plates and transcribed into `AINTRO_AFFIL` before the panels were stripped. **Do not
regenerate the plates from the pack without carrying that table forward** — the source for those
strings is now the table, not the art.

## Verified

Decker (blond, gold tint, ORDER OF THE MATRIX), Juggernaut and Falva all captured from the real
game: BOF face throughout, underlined top with no box, `dlg_window` at the bottom, no overflow.
