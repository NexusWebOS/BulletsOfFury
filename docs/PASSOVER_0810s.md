# Passover 0810s — the ship bosses, the fireball icon, and the quad-laser's beams

Mike, asleep, on the South-Facing Ship pack: *"the volcano one is your new lava MAIN boss, and the
ice ship is the new ice boss. black edge the units. Wire them up, give them attacks that fit, make
them challenging, glow white when shot etc. The bottom left corner — use that boss for the stage 2
miniboss but palette swapped to look fire red. Use the bottom middle one and also palette swap to a
black/ice blue appearance, thats your stage 3 miniboss. use the bottom right corner one for the
stage 5 boss. again Im aslepe, so figure it out. surprise me."*

Suite at the end of this drop: **2,453 assertions / 218 sections / 4 failures** — the same four
standing ones (preload count, the two `_superseded`, naval flash families).

---

## 1. The five ship bosses

| kind | slot | pattern | what it denies |
|---|---|---|---|
| `infernoreaver` | stage 2 boss | `ember` | a wall of fire with one moving two-column gap |
| `cryospear` | stage 3 boss | `lance` | three lanes, two closed, the safe one rotates |
| `voidbat` | stage 5 boss | `void` | converging Vs from both wingtips |
| `siegeember` | stage 2 mini | `siege` | broadsides left then right — you cross on the beat |
| `thornrime` | stage 3 mini | `rime` | a slow spiral that closes every straight line |

This also settles three items off the 0810q list — the level 2 and 3 bosses and the level 3
miniboss are all replaced. The magma/cryo rigs are **not deleted**, only unassigned.

**None of the five aims at the player.** The file already argues for that at `eshot`'s `push()` —
bullets stay readable, difficulty raises SPEED not count, and a pattern keeps its shape so what the
player learned still applies. It is also what *"shmup patterns where I have to keep myself at
certain spots to survive"* actually asks for: the fun is in the geometry denying space, not in
dodging something that follows you. All five scale by `DIFF.ebSpeed` like every other pattern.

Measured in real Chromium (`_BUILD_SOURCE/probe_shipboss.py`). Draw and flash are **frame diffs**,
never blit counts — a blit count already reported 0 for two minibosses a screenshot showed drawn in
full (0810l).

| kind | draw px | flash px | bullets/wave | spread |
|---|---|---|---|---|
| infernoreaver | 97,966 | 63,282 | 7 | 712px / 9 lanes |
| cryospear | 90,486 | 49,318 | 6 | 566px / 5 lanes |
| voidbat | 73,169 | 69,671 | 12 | 178px / 2 wingtips |
| siegeember | 67,436 | 42,564 | 6 | 704px / 12 lanes |
| thornrime | 57,108 | 33,068 | 5 | spiral from one point |

### What the measurements caught that reading the code did not

**The minis came out at 42 HP.** `spawnBoss` seeds `maxhp` from the stage; `spawnSubBoss__inner`
seeds a flat 100. One multiplier across both is two different fights. They carry absolute HP now —
235/225 scaled by difficulty, against the quad-laser's 210.

**The `ice_black` swap passed its own numbers and was still wrong.** Mean hue 0.55, saturation 0.25
— exactly on target — and it rendered as uniform gunmetal slate: dark everywhere, blue nowhere,
neither half of *"black/ice blue"*. Value and saturation have to curve in **opposite** directions
(`vv**1.9` and `vv**2`) so the hull crushes to black and only the lit edges carry the ice. Render
the swap; the mean hue will lie to you.

### ⚠ The probe was wrong before the game was

`probe_shipboss.py`'s first run reported both minibosses as failed spawns.
**`spawnSubBoss__inner` ASSIGNS the global and returns nothing** — it ends on `subBoss=b;
subBossActive=true;`. Every fixture in `test_fl.js` reads `subBoss` for exactly that reason.

It also crashed the renderer outright ("Target crashed") doing five frame-diffs plus five
`toDataURL` calls on one page, which CLAUDE.md already records as long warms plus many captures
exhausting the renderer. Measurements and screenshots now run on separate browsers, and each result
prints **as it arrives** — when that crash hit, every measurement taken before it was lost with it.

---

## 2. The fireball icon — it was the surface, not the art

**Nothing was lost.** Rendering the existing icons first (`docs/proofs/icons_existing_0810s.png`)
settled it: `micon_fireorb_1..5` are hexagon-framed tier icons in the same house style as the new
sheet, and so are iceorb, icebreath, thermoshock, firewall and laser. So swapping the art alone
would not have fixed anything.

The EQUIPPED box lives in `index.html` as its own classic script on its own canvas, and it had two
faults:

- it probed `micon_*` against **XART**. Those 57 keys live in `BOFX.icons`, the third store, which
  XART can never answer for — so the `micon_` candidate was false for every weapon on every frame
  and it silently fell through to an older `*_icon_*` set. **Its own comment asserted "micon_* DOES
  NOT EXIST. NOT ONE OF THE 30 KEYS THIS ASKED FOR IS REGISTERED"**, which is how the wrong
  conclusion survived three drops. A confident comment is not a measurement.
- it kept a **second weapon table** hard-coding `5:'iceorb'`, bypassing `weaponIconKey` entirely, so
  slot 5 could never show the fireball whichever store answered. Measured: stage 3 with the fireball
  equipped drew an ICE icon, near-identical to stage 2's ice orb.

`iconBlit(g, key, x, y, h, centred)` is `iconDraw` into a caller-supplied context — the reason the
box could not simply call `iconDraw` — so both surfaces share one lookup and cannot drift again.
Before/after: `docs/proofs/icons_equipbox_0810s.png`.

Icon entries may now name their own sheet via a **5th element** on the rect. New art:
`assets/game/nia_icons2.png`, de-keyed by **border flood** (these have hot pink-white cores at tier
IV/V that a colour sweep would eat), halo converted to a black edge, 4,215 spill pixels pulled back.

⚠ Downscaled with LANCZOS, not decimated. Re-expanding a NEAREST decimation mismatches the source by
16% at block 2 and 19% at block 3 — there is no pixel grid to preserve. 192px is 2× the existing
family's 96 and took the sheet from 1,025 KB to 569 KB.

---

## 3. The quad-laser's four beams

*"Program lasers to shoot from the beams on the level 1 miniboss."*

They never had. The four muzzle anchors were read into `_qlCan` at spawn and used for one thing — a
muzzle flash gated on `b._muz`, **which nothing ever set for this unit**, so even that never drew a
pixel. The guns were geometry and a health pool, and the fight fell through to the generic sub-boss
cases. That is why shooting the turrets off changed nothing you could see.

Each live cannon now holds a **fixed vertical lane** and they fire together — the fight Mike
designed in 0801if (*"you have go destroy the lasers first on this miniboss, then his hull is
attackable"*). Four lanes is a wall you stand between; every cannon you break **opens** its lane for
good, so the arena widens as you earn it and the reward is spatial rather than a number going down.

Then the nose takes over: *"when his lasers are gone, he should begin shooting charge lasers."*
`_qlChg` / `_qlChgN` were declared for that in 0801if and **read by nothing** — the charge phase had
never been built. It winds up over two beats so the release is telegraphed, and alternates a
straight lance with a fan.

Measured (`_BUILD_SOURCE/probe_quadlaser.py`):

| case | alive | lanes fired |
|---|---|---|
| all four alive | 4 | `[421, 449, 543, 571]` — exactly the four live muzzles |
| left_outer destroyed | 3 | `[449, 543, 571]` — that lane is gone |
| both outers destroyed | 2 | `[449, 543]` |
| all destroyed | 0 | 5-shot charge from the nose |

⚠ That probe failed all three live cases on its first run and **the game was right**. It snapshotted
the unit's x during setup, but `updateSubBoss` drifts an air miniboss to WORLD centre, so a stage-1
unit placed at `VW/2`=240 is near 496 by the time it shoots — every volley read as off-target by a
constant 256. Lanes are computed at FIRE time now. Same family as `probe_seam.py` recomputing the
value under test.

---

## Still open for Mike

- **Which weapon should wear the ice shards?** `micon_iceshard_1..5` is registered and additive but
  dresses nothing yet. The existing ice families are `iceorb` (the ball) and `icebreath` (Freezer's
  cone).
- **More projectiles for the ordinary enemy roster.** The five boss patterns and the quad-laser's
  lanes land the ask for bosses; the regular units are still the stage-3 change only.
- **The atlas reorg** is still blocked on names, not packing — 5,064 of 9,733 keys sit in families
  whose names say nothing. Repacking those into tidy sheets would leave Mike exactly as unable to
  find anything. `atlas_fammap.py` derives names from the code that draws each family; that map
  needs reviewing before any repack.
- **The stage-1 sheets are still not on disk** — they came through as pasted images. The stage-7
  overlay (`~/Desktop/level7corrected.png`, 800×4062) IS on disk and is not wired yet.
- Level 1 pop-in: 2 of 29 units still appear rather than enter, both at (21,67).
