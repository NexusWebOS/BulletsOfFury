# The Forge economy (0917): score -> Furious Points -> Armory levels

Mike, 0917: *"we need to design our currency system to unlock these upgrades. Furious Points are the
answer to incentivise playing the game on higher difficulties and other pilots, and your Score Points
in-game. Yes, the high-score points now become useful instead of a show off. You use your high score
points to purchase Furious Points. All icons here should get their level 1-5 upgrade generated
variants, and upgraded projectiles and more. Also, you may only equip 1 weapon type of each type - I.E
1 machine gun upgrade type, 1 laser upgrade type, 1 orb upgrade type, 1 spread upgrade, 1 missile
upgrade, 1 flamethrower/ice breath/other types upgrade."*

## The loop

```
  a run ends (game over / victory)
      -> its SCORE is deposited in the profile's SCORE BANK as CREDIT
         credit = score x difficulty x (first run on this pilot ? 1.5 : 1)
  THE VAULT, first row: EXCHANGE SCORE
      -> credit becomes FURIOUS POINTS at 1 point per 1,000 credit (the remainder stays banked)
  THE VAULT, last row: THE ARMORY
      -> Furious Points buy Forge LEVELS II..V, per weapon x element, for ever
  THE FORGE, between stages
      -> combining an element opens the weapon at the level you OWN, wearing that level's badge
```

| difficulty | credit multiplier |
|---|---|
| EASY | x0.5 |
| NORMAL | x1.0 |
| HARD | x1.5 |
| FURIOUS | x2.0 |
| INSANITY | x3.0 |

The first run banked on each pilot pays **x1.5** on top - that is the "other pilots" half of the
incentive. A 120,000 HARD run on a pilot you have not flown before is 270,000 credit = 270 points.

| Forge level | price (Furious Pts) |
|---|---|
| I | earned in play - discover the element, combine it in the Forge |
| II | 150 |
| III | 300 |
| IV | 600 |
| V | 1,000 |

The achievement points (10 to 1,000 an award, 66 awards) and the score exchange feed ONE balance:
`furiousBalance() = achievementPoints() + furiousExchanged() - furiousSpent()`.

## What a level does

- Levels I-III are the infusion system's own three levels (0917): the element's on-hit effect grows and
  level III is the NAMED combination (FIREBURST, GODS WRATH, ...).
- **A pickup in the field never lifts an element past III** (`INFUSION_PICKUP_MAX`). IV and V are the
  Armory's alone, which is what makes them worth buying.
- Above III every level grows the round and its damage a step - **+12% size, +10% and +1 damage per level**
  (a 2-damage pellet rounds a bare +20% away to nothing, so the +1 is what a machine gun feels),
  stamped once on the round where the element is (`_infScaled`). The beam is one reused object that sets
  its own width every shot, so it is left alone; the named effects keep scaling on `lv` as they did.
- The badge on every surface (Forge boxes, the picker, HUD, EQUIPPED box, crate) is the level's own
  plate: `micon_forge_<elem>_<slot>_<lv>` for II..V, `micon_forge_<elem>_<slot>` for I.

## One upgrade per weapon type, by construction

`run.forge` is keyed by SLOT and a slot holds one `{elem, lv}`; `forgeCombine` REPLACES it, and the
loadout can never carry a slot twice (`forgePick` swaps). So the rule is the shape of the data rather
than a check that could be forgotten - section 372 pins it. Flamethrower, laser mist and the lightning
orb are not carriers (their rounds cannot wear an element), so they have no Forge row and no Armory
tab; the "other types" upgrade Mike lists for them is open, and I have not invented one.

## The ledger

⚠ **What has been exchanged is the SUM of the exchange entries, never a counter** - the same rule the
0916 shop applies to what was spent. `achievementState.bank = {credit, runs, pilots, exchanges[], last}`
rides the achievement store (one profile, one save) and `achievementNormalize` re-types every field on
the way in, exactly as it does `owned`. The Armory's levels are `owned` rows under
`forge_<elem>_<slot>_L<n>`, matched by pattern in the normaliser so a re-priced level cannot change
what an existing player has left. ⚠ **The store version is NOT bumped** - a bump returns an empty
store and deletes every award every player has earned.

## The 216 level badges

Tiers II..V are the tier-I sheets EDITED (`edit_asset_id`, never a fresh generation - a fresh generation
redraws the emblem): the tag numeral and N gems on the frame are the only change, 24 jobs at 12
credits. ⚠ **The tier-V prompt's "faint glow around the whole frame" tinted the gutters** and the
slicer read the sheet as 3x1 - the rows only separate at a lower background floor
(`find_cells(im, 200)`), and one sheet (spread) needed regenerating with the gutters named clean.
`forge_icons_tiers_0917.py`; cards in `docs/proofs/forge_icons_0917/slot<n>_tiers.png`.

## Proof

- `probe_armory_0917.py` in real Chromium: a HARD run ends and GAME OVER prints the BANKED line; the
  VAULT exchanges it; THE ARMORY buys TESLA BEAM level II with real key taps and the row's badge changes
  by KEY; the shortfall is named on the refused level III; the Forge opens the laser at level II; RETINA
  opens the Armory from the Forge and BACK returns; a level-V machine-gun round measures bigger and
  harder than the bare gun's.
- suite section 372.

## Open, for Mike

- The rates (1 point per 1,000 credit, x0.5..x3.0, x1.5 first pilot) and the level prices are my
  numbers, sized against the award points (a stage clear is 10, a Furious boss 500, INSANITY costs
  2,000). Retune in `SCORE_BANK_RATE`, `SCORE_BANK_DIFF`, `SCORE_BANK_NEW_PILOT`, `FORGE_LEVEL_COST`.
- Whether level I should ALSO cost points (today it is free once discovered, so the Forge is playable on
  a first run).
- An upgrade path for the three non-carriers (flamethrower / ice breath, laser mist, lightning orb).

## The level's look (0917, later): the round appears upgraded per level

Mike: *"like our previous level 1-5 variants, they should appear upgraded per each level even in this
new bullet elemental form or laser upgrade form. Just for extra graphical effect."*

Level I is the element palette on the authored round, unchanged. From II every carrier round wears an
additive **glow plate** in its element's glow colour - a radial gradient baked once per element x level
x size (`infusionGlowPlate`, cached) and blitted `'lighter'` at an integer origin; III adds a wider
faint halo baked into the same plate; IV brightens and grows again; V adds a pulsing four-point core
flare. A **trail of element sparks** follows every round from II, denser each level (`INF_TRAIL_P`,
spawned from the UPDATE loop, tagged `_infTrail`, capped at `INF_TRAIL_CAP`). The **beam** wears a
soft-edged element **column plate** under the authored beam (`infusionColumnPlate`, a horizontal
gradient stretched down the column) that widens with the level, a second wider plate from III, and
sparks crackle along it from IV. The level rides the round as `b._infLv`, stamped beside `b._inf`.

- ⚠ **Never `shadowBlur`** - 0916ab measured 138 blurred draws a frame at 1.4 fps; every layer here is
  a baked plate or a particle. Section 373 pins that the aura's source never names it.
- ⚠ **Never a flat `fillRect` beside the beam** - the first cut's column was a flat slab and read as
  an overlay, the one thing the palette rule forbids; the gradient plate replaced it.
- ⚠ **A particle's `t` advances inside the step that spawned it**, so a probe counting `t===0` after the
  step counted ZERO on a build spawning 266 in 60 frames. Mark each spark seen instead.
- ⚠ **My first insertion put the trail block INSIDE the stamp `if` and closed it early**, leaving the
  kinetic SONIC WAVE trigger inside an `if(false){}` - dead, with `node --check` green. Read the block
  you are inserting into to its closing brace, not to the line you anchored on.

Measured (`probe_infusion_levels_0917.py` 12/0, real trigger, real Chromium): INCENDIARY SLUGS I..V -
aura plate widths 0/22/26/34/46, trail sparks per 60 frames 0/82/153/206/266; TESLA BEAM I..V - column
blits 0/60/120/120/120 (II one plate, III+ two), sparks 0/0/0/34/44. Card:
`docs/proofs/infusion_levels_0917/levels_card.png`.

## All nine weapon types (0917, later still)

Mike's equip rule named nine upgrade types: *"1 machine gun upgrade type, 1 laser upgrade type, 1 orb
upgrade type, 1 spread upgrade, 1 missile upgrade, 1 flamethrower/ice breath/ other types upgrade."*
The last clause was the one thing still open - the flamethrower / ice breath (slot 4), laser mist (6)
and Yuri's lightning orb (8) were listed as CANNOT TAKE AN ELEMENT.

⚠ **That reason was read off the KIND table, not off the muzzles, and it was wrong.** Measured:

| slot | pushes | reaches the hook |
|---|---|---|
| 4 flamethrower / ice breath | `{kind:'flame', pierce:true}` into `pBullets` | the loop's flame branch calls `hitEnemy` with `_dmgBullet` set, throttled by `FLAME_TICK`'s ledger - one element hit per enemy per tick, not per frame |
| 6 laser mist | `{kind:'lasermist'}` | `laserMistTick` is called FROM the bullet loop and calls `hitEnemy`; the lance dies on its hit |
| 8 lightning orb | `{kind:'yuriLightningOrb'}` / `Bolt` | `yuriLightningOrbTick` likewise, through `hitOnce`, once per target |

So all three already reached `infusionOnHit` through the ONE hook the Forge was built on. `FORGE_WEAPONS`
is `[0..8]` now, `INFUSION_CARRIERS` names their kinds, and every element x new slot has a name
(BLAST FURNACE, EMBER MIST, MAGMA SPHERE ...). What they do NOT take is the palette swap - each has its
own authored draw - so the element rides them as the aura, the trail and the on-hit effect.

- ⚠ **The flame is a COLUMN, not a round.** Its `h` is `flameReach(lv)` (200+px), so the round aura plate
  would have sized off that and painted a blob the height of the screen. It takes the beam's column path.
- ⚠ **And the stamp must not overwrite the flame's own `_el`.** `flameFire` re-asserts it every weapon beat
  and `elementMultiplier` reads it, so a FLAMETHROWER forged with ICE stays a fire weapon that also
  chills - measured `_el fire, _inf ice`.
- ⚠ **THE ARMORY'S NEW TABS DREW NOTHING, AND THE GUARDS HID IT.** Both of its row branches built a
  `micon_forge_*` key and those plates existed only for the six slots whose sheets were generated:
  measured 0 lit px against the weapon's own working icon at 2349 / 1759 / 2101. `weaponIconKey` takes
  `{bare:1}` now so the row can ask the ONE resolver for the tier icon instead of rebuilding that logic.
- ⚠ **And `micon_lasermist_*` is not on `nia_icons`** - `iconBlit` routes it to the mist's own atlas, which
  returns null until that sheet is warmed. Touching the icon key starts nothing. Both screens warm it.
  (My own probe hit this first and reported a working icon as 0 px.)
- ⚠ **Three suite pins DEFENDED THE LIMITATION** (`FORGE_WEAPONS==='[0,1,2,3,5,7]'`, `!forgeCanTake(4)`,
  `forgeCombine(4,'fire')==='cannot'`) and one more named a LINE the drop then edited (373's beam regex).
  All repointed with the reason, to the durable claim: every forgeable slot's round kind is a CARRIER.

**The badge set is complete: 9 elements x 9 weapons x 5 levels = 405.** The three new sheets were
generated against the authored badge strip like the rest, their tiers II-V by `edit_asset_id`.
Cards: `docs/proofs/forge_icons_0917/slot{4,6,8}_tiers.png`.

Proof: `probe_forge_noncarriers_0917.py` 21/0 (each slot's rounds carry the element and the level, the
element's own touch lands through the shared hook, the flame takes the column aura and keeps its own
element), `probe_forge_icons_0917.py` 16/0, `probe_armory_0917.py` 27/0.
