# Passover 0812e — the Jungle Cruiser takes stage 1, and stage 6 stops fielding a placeholder

> Mike: *"dont forget to wire up our new minibosses and bosses and upgrade all remaining minis and
> regular bosses. get rid of level 1 miniboss use the new jungle cruiser I gave you. thats a start."*

Stage 1 and stage 6 are done. What the survey found about the rest is in §5 — including that the
"new minibosses and bosses" were **already wired**, which is not what I expected going in.

---

## 1. ⚠ THE SOURCE FOLDER AND THE BUILD DISAGREE, AND THE SOURCE IS THE WRONG ONE TO READ

`_ART_SOURCES/BOF2_South_Facing_Ships_v1/` holds six hulls. Read as source frames they look
crossed with their stages — the **Olive Siegecarrier** is olive-green but sits on the volcano, the
**Thorn Cruiser** is green but sits on the ice. I nearly "fixed" three correct assignments on that
basis.

⚠ **THE IMPORTED PLATES ARE RECOLOURED.** Measured off the registered art, not the sources:

```
nsb_siege_ember     ember RED     -> stage 2 volcano   correct
nsb_thorn_rime      rime TEAL     -> stage 3 ice       correct
nsb_blacksteel      gunmetal      -> stage 4 airbase   correct
nsb_inferno_reaver  fire ORANGE   -> stage 2 BOSS
nsb_cryo_spear      ice BLUE      -> stage 3 BOSS
nsb_void_bat        void PURPLE   -> stage 5 BOSS
```

Every one of the six is in use and every one matches its stage. **"Filenames lie" extends to
source folders**: the frames are the un-recoloured originals, and the build is the truth.

## 2. The Jungle Cruiser

The pack's only *Cruiser* is the Thorn Cruiser, and its **source** frame is olive-green — jungle.
So stage 1 gets that hull under a jungle palette rather than a seventh 256×256 file, which is
exactly how `siegeember` and `thornrime` were built in the first place: one silhouette family,
recoloured per theme.

`shipBossDraw` gained a `pal` field. It routes through `xartPalette`, which keeps the plate's own
shading (hue/saturation from the fill, luminosity from the art) and caches per key+mode — so a
themed hull costs **one canvas for the whole run**, not one per frame. It falls back to the
untinted plate rather than drawing nothing, because an invisible boss is the worst failure this
file produces and that guard already exists three lines above.

⚠ **HP IS THE QUAD-LASER'S 210, DELIBERATELY.** This is the first miniboss a player ever meets and
Mike tuned that fight at 210; a cruiser-sized 245 would quietly make stage 1 harder than stage 4's.
`at` and `afterScroll` are untouched too — 0801ke moved that trigger three times to land the fight
after the beach tanks and the grass jets, and that sequencing is about the STAGE, not the unit.

⚠ **THE QUAD-LASER IS UNASSIGNED, NOT DELETED.** Its `nqx_` art, its four per-cannon hitboxes and
its charge attack all remain, so it can take another slot without being rebuilt.

Proof: `docs/proofs/miniwarm_s1_0812c.png` — olive hull over the river, health bar reading
JUNGLE CRUISER.

## 3. ⚠ STAGE 6 WAS FIELDING A UNIT LITERALLY NAMED "SUB-BOSS"

`SUBBOSS[6]` said `'ss'` and **`spawnSubBoss__inner`'s switch has no arm for it**, so it fell
through to the generic 130×120 default: no art, no attack profile, the stock 100 HP. Nothing
failed and nothing logged — it simply was not a miniboss, and it had been that way long enough to
survive a rendered miniboss audit one drop earlier (`miniboss_s6_0812c.png`).

It is now the **STORM LANCE** — the Blacksteel interceptor silhouette in storm-steel, 265 HP (the
toughest of the minis, being late), `lance`+`void`.

## 4. Suite

**2,533 assertions / 225 sections / 5 failures** — the same five long-standing ones.

⚠ **NINE ASSERTIONS FAILED ON A ONE-WORD CHANGE THAT BROKE NOTHING**, because they tested the
quad-laser by asking *what stage 1 happens to field*. The system still exists and is still worth
testing, so they now spawn it **by kind**. The one genuinely valuable coupling — that 200 simulated
seconds of stage 1 actually *reach* a miniboss — is kept and now asserts the cruiser. Two claims,
two units, one run.

New **§220** asserts the property that would have caught stage 6 years ago: **every stage 1–8
fields a NAMED miniboss**, plus that each palette-swapped hull warms its source plate (a `pal`
whose key is unwarmed opens the fight on the silhouette fallback — the 0812c bug, reintroduced by
a new unit).

## 5. The survey, for whoever takes the rest

Bosses and minis as they now stand:

```
stage   boss              miniboss
1       damkeeper         junglecruiser   <- 0812e
2       infernoreaver     siegeember
3       cryospear         thornrime
4       warhawk           blacksteel
5       voidbat           subcore
6       stormsovereign    stormlance      <- 0812e
7       toxicleviathan    ratking
8       vileexistence     herald
```

Still worth doing, in the order I would take them:

- ⚠ **The Herald's `mba_vr_*` plates are not in `XART._src` at all** — zero keys start with
  `mba_vr`, so `XART.rdy` on them can never return true. It draws today only because 0812c warmed
  its venom reel and the fallback path took over. **Routed around, not resolved.**
- **`subcore` (stage 5) and `ratking` (stage 7)** are the two remaining minis with no new-pack art.
  Both render, so this is an upgrade rather than a fix.
- **Stage 8's boss** is still Mike's *"filler shit"* — four forms, one attack pattern, not coded.
- The **muzzle-flash and impact reels of nca_87** (rows 0 and 2) are identified in code and unwired.
