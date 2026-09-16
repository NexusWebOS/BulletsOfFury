# 0916 — the chaingun gets icons in the house style, and every name is lettered in its element

Mike, with a strip of four weapon icons in which the chaingun is the odd one out:

> "generatre new chaingun icons to match our current style of icons. Recolor each text to match what
> the weapon type is - Bullet weapons - Orange, Lightning - yellow, thermoshock - red/blue shade,
> laser mist - aqua blue, ice - ice blue, fire - neon red etc."

## 1. What the style actually is

Rendered side by side, it is unmistakable and the chaingun had none of it. Every weapon icon on
`bof_player_weapon_special_icons.png` is a **framed badge**: a bevelled ring around a dark field
holding the weapon's emblem, with a metal tag at the bottom carrying the tier in Roman numerals.
The chaingun's five were loose 64×64 sprites with a small blue number underneath and no frame.

⚠ **AND THE BADGES ARE COLOUR-CODED PER TIER, NOT PER WEAPON** — orange, blue, green, silver, red
for I…V. That is also why every icon in Mike's strip is green: they are all tier 3. A first cut
that assumed "green = the special family" found no ring at all on four of the five tiers.

## 2. ⚠ SUPERSEDED BY §4b — the icons are two pieces of authored art, composited

CLAUDE.md's first standing rule is never to create a placeholder or procedural sprite, and to
search the existing art first. Both halves already existed:

- the **frame and its tier tag** are `micon_icebreath_N` — tier N's own badge, so the ring, the
  Roman numeral and the size progression are the authored ones;
- the **emblem** was the chaingun art already shipping in `chaingun_icon_N`, cut out and re-seated.
  **Superseded by §4:** Mike asked for a chain BARREL, so the emblem is now a generated one and
  those sprites are the fallback. The frame work below is unchanged and is what §4 seats it in.

The old files are kept as `chaingun_icon_N.pre0916.png`; nothing was overwritten.

### Four cuts at finding the badge's interior, and why each failed

The interior has to be cleared before the chaingun can go in, and this was the whole job:

1. **Flood from the centre** — the centre *is* the emblem, so it flooded nothing and returned an
   empty mask.
2. **Largest enclosed black island** — the ring is SEGMENTED and its joints are near-black, so the
   field and the badge's outer outline are one connected region. It returned 7×3px pockets.
3. **Bounded by the green ring** — only tier 3 is green (see above).
4. **The layer walk** (outline → ring → field, per row) — correct in principle, but where the
   donor's crystal *touches* the ring the walk runs straight through it and the ray outside the
   landing point survives. It showed as blue streaks in the badge's lower corners.

**What holds:** the ring is a constant thickness on a hex, so the inset is measured once as the
median over the rows where the walk is unambiguous and then applied to every row. No row depends on
its own pixels being clean.

⚠ **AND TWO MORE FAULTS ONLY THE RENDER FOUND.** The old icon files carry their own little blue
tier tag, and on three of five tiers it *touches* the gun — so "largest connected island" brought it
along and a second, smaller numeral appeared inside the badge. It is cut at the gap in the row
profile instead, which every one of the five files has. And the first tag guard protected "anything
bright in the bottom third", which is where the donor's emblem also is: the crystal survived below a
hard horizontal edge. The guard is bounded to the tag's own measured geometry (rows 99..111,
x 19..79, 58–61% of the width on every tier).

## 3. Every name is lettered in its weapon's element

`UNLOCK_TINT`, keyed off the icon key's family (`micon_<family>_<tier>`) — the only thing a row
carries besides its name, so a row added later is coloured by existing code rather than by a second
table someone has to remember to extend.

| element | colour | families |
|---|---|---|
| bullets | orange `#ff9a3a` | mg, spread, chaingun, missile |
| lightning | yellow `#ffe03a` | lightningorb |
| thermoshock | violet `#c07cff` | thermoshock |
| laser mist | aqua `#3fe3ff` | lasermist |
| ice | ice blue `#9fdcff` | icebreath, iceorb |
| fire | neon red `#ff3b2a` | fireorb, firewall |
| unknown | green `#8de23a` | the visible default |

⚠ **THERMOSHOCK is his "red/blue shade"**: the weapon is half fire and half ice and a single tint
can only be one colour, so it takes the violet the two mix to.

**Two he did not name, flagged rather than guessed silently:** MISSILE is grouped with the bullets
as kinetic ordnance, and LASER keeps the default green. Say the word and either moves.

## 4. ⚠ SUPERSEDED BY §4b — the emblem is a chain barrel, in five tier colours

Mike, with a photo of a six-barrel minigun: *"chaingun icon should be a chain barrel icon with
lvl1-5 upgrade color variants like our current scheme"* / *"something ike, generate it please."*

**The barrel is GENERATED** — SpriteCook, `gemini-3.1-flash-image`, three variations, 36 credits
(balance 6,324 → 6,288; CLAUDE.md's "22 left" note was stale). The one chosen has its muzzle face
square to the viewer, which is what reads at icon size — the same thing the MG badge's own emblem
does with its revolver face.

⚠ **PALETTE-LOCKED FIRST, BECAUSE `pixel:true` DOES NOT GIVE PIXEL ART.** Measured on opaque pixels
only — counting the RGB under transparent pixels is how this gets waved through — the generated
barrel is **656 colours**. It is a continuous-tone render wearing pixel-art clothes, and dropped in
as-is it sits inside hand-authored art at a different fidelity. It is snapped, **dither off**, to
the palette of `micon_mg_4` — the SILVER tier, the family's own neutral metal, which has no hue of
its own to inject. **656 → 161 colours.**

⚠ **THEN THE TIER COLOUR IS A HUE ROTATION, NOT A PAINT.** Each tier's hue is measured off **that
badge's own ring** (the family is colour-coded per tier) and the barrel is rotated onto it with its
VALUE untouched, so every bevel, muzzle shadow and rim light survives — 0906t: rotate the hue,
never set it. Measured: tier 1 hue 0.060, tier 2 0.620, tier 3 0.329, tier 5 0.008. **Tier 4 is
silver: its ring has no hue to measure, so the barrel is left neutral rather than rotated onto
noise.**

The barrels ship as `chaingun_barrel_1..5.png` beside the badges, so the emblem can be re-tinted or
replaced without touching the frame work. The pre-0916 sprites remain as the fallback.

Builder: `_BUILD_SOURCE/chaingun_barrel_0916.py` (`--check` renders the five tiers without writing).
Proof: `docs/proofs/chaingun_icons_0916/03_generated.png` (the three variations),
`04_barrel_tiers.png` (the five colours), `01_new_icons.png` (was / donor / now).

## 4b. Generated from scratch — the cut that shipped

> "you have to generate those chaingun icons by scratch, they look clearly edited."

He was right, and it is worth being plain about why: §2 and §4 built each icon by taking **another
weapon's badge**, clearing its interior and dropping a generated barrel in. Every step of that was
careful and the result still reads as what it is — a composite. Four separate cuts at "find the
interior" and two at "protect the tag" are the tell: that much machinery to make one picture sit
inside another picture is the process telling you it is the wrong process.

**The icons are now generated COMPLETE** — frame, field, barrel and Roman-numeral tier plate, one
job per tier. Three authored badges (`micon_icebreath_3/4/5`) were uploaded as a **style reference
asset**, so the segmented bevelled ring, the black field and the tag come back in the family's own
language rather than being described in words and hoped for.

SpriteCook, `gemini-3.1-flash-image`, **two variations per tier**; the pick is the one whose muzzle
face reads clearest at icon size. 120 credits for the five tiers plus the barrel work
(6,324 → 6,168).

⚠ **THE NUMERALS CAME BACK CORRECT AND THAT IS NOT GUARANTEED.** Generated text usually is not.
Every tier was rendered and read before selection — I, II, III, IV, V — and one rejected variation
had a **gold V on a red frame**. Read the numeral on any regeneration; never assume it.

⚠ **SIZE IS A HINT.** 112×112 was requested; the jobs returned 100, 106 and 200. Each is scaled to
the family's own **112 height** with its aspect kept, because the icons are drawn by height beside
the other badges — and tier 4's first pick was dropped for a sibling because it came back
noticeably wider than the rest.

⚠ **NO PALETTE LOCK, AND THAT IS A MEASUREMENT.** 0905's rule — snap a generated plate to the
reference's palette because `pixel:true` does not give pixel art — was written against a boss plate
whose authored counterpart is **61 colours**. This family is not that: `icebreath_3` is **6,329**
opaque colours, `icebreath_1` 4,977, `mg_5` 4,775, `thermoshock_3` 2,875. The generated badges come
back at 4,600–5,600, **inside that range**, so a snap would only flatten them. It is kept behind
`--snap` with the numbers recorded, rather than applied because a rule said so.

Builder: `_BUILD_SOURCE/chaingun_badges_0916.py`. Proof:
`docs/proofs/chaingun_icons_0916/06_scratch_all.png` (all ten variations),
`07_final_badges.png` (the five that shipped). The composite path and its barrels stay on disk as
`chaingun_barrel_*.png` and `chaingun_icons_0916.py`; the pre-0916 sprites remain as the fallback.

## 5. Measured

`_BUILD_SOURCE/probe_unlocks_0916.py` — **66 ok / 0 fail**, real Chromium, 0 page or console
errors. It checks the table *and* the pixels: one row per element driven through the page's own
entry point, with the ink read back off the canvas — fire `(255,189,171)`, ice `(189,216,222)`,
bullet `(255,193,129)`, laser mist `(138,227,230)`. Every chaingun tier resolves at **112px tall**,
the geometry the other weapon badges use.

⚠ **Two probe faults on the way, both the store trap.** The reference badge was asked of `XART`,
where `micon_*` icons have never lived — they are rects in `BOFX.icons`, the third store `iconBlit`
exists to reach — so it read null and failed against a build where the art is fine. And it was
asked cold, so `XART.rdy` was false on its first call for the chaingun's own loose files.

Suite **4,628 ok / 56 fail**, final summary reached — zero new failure names against a clean
worktree at `97265703`.

Builder: `_BUILD_SOURCE/chaingun_icons_0916.py` (`--check` renders was/donor/now without writing).
Proofs: `docs/proofs/chaingun_icons_0916/00_before.png`, `01_new_icons.png`,
`docs/proofs/unlocks_0916/06_elements.png`.
