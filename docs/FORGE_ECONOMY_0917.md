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
