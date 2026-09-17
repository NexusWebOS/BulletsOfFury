# The Forge economy — Furious Points, the ladder, and where a combination comes from

Mike, 0917, in two messages that together replace the run-end score bank this document used to
describe:

> "These are not to be purchased through the achievement system. 1000 score points is the equivilent
> of 1 Furious Point for conversion. At the end of each level, your Maintain your 'Score Points' as a
> high score record keeper, but at the end of each level, your 'points' convert into FP = Furious
> Points. Thats how to make this balanced to start off. Additionally, you dont unlock all these weapon
> combination upgrades. Your going to make powerup upgrade's for these new weapon types that drop from
> the boss when they die at each level, and thats how we gain new combinations and such."

> "Achievement points are also tied to this. It is expected that most players will unlock at least 1-4
> achievements on Level 1 alone ... Collecting items, powerups and special abilities also gives you
> points like 250 each. Somersalting, or barrel rolling before a projectile would've impacted you
> grants you a 'Stylish!' award of 500 points that appears letter by letter and glows before fading
> away letter by letter. Therefore, scale our new system to start with each upgrade at about 1000.
> Once you do so, the points to unlock your next weapon type or upgrade goes up by 25%. Easy simple
> scaling."

---

## 1. Where the points come from

| source | amount | where |
|---|---|---|
| a level's own score | 1 FP per 1,000, remainder carries | `furiousConvertStage`, at the STAGE CLEAR |
| an achievement | its own point value | `achievementPoints()` |
| collecting anything | 250 score | `applyPowerup` / `PICKUP_SCORE` |
| a STYLISH dodge | 500 score | `stylishAward` / `STYLISH_SCORE` |

    furiousBalance() = achievementPoints() + furiousConverted() - furiousSpent()

**The score itself is never spent.** The conversion reads a level's delta and leaves `run.score`
alone, because it is the high-score record — "Maintain your Score Points as a high score record
keeper". The remainder carries into the next level, so two 900-point levels are worth a point
between them rather than nothing.

**The awards gallery still sells nothing.** Mike's "not ... purchased through the achievement
system" is about the SHOP: the Vault and the Armory are where points are spent, and that has not
changed. What the second message added is that an award's points land in the same balance a level
converts into.

⚠ **The two incomes are not the same size and are not meant to be.** A first Stage 1 clear plausibly
pays 10 + 200 + 100 + 200 = 510 in awards (STAGE 1 CLEAR, NO DEATH, MISSILE DISCIPLINE, a HARD boss),
or 1,010 with the FURIOUS boss instead — against a first upgrade of 1,000. The level's own score at
1,000:1 is tens of points on top. So achievements set the pace early and the score conversion is the
reason to keep replaying a level you have already cleared, which is the incentive Mike asked for in
the first place.

## 2. What an upgrade costs

One ladder, for every upgrade, rising 25% per purchase:

| purchases made | price |
|---|---|
| 0 | 1,000 |
| 1 | 1,250 |
| 2 | 1,560 |
| 3 | 1,950 |
| 4 | 2,440 |

`FORGE_UPGRADE_BASE` 1000, `FORGE_UPGRADE_STEP` 1.25, rounded to the nearest ten so a price reads as
a price (the exact curve gives 1562.5 and 1953.125; ten holds the ladder inside 0.2% of ×1.25).

⚠ **The price depends on how many you have BOUGHT, not on which rung you are buying.** The table this
replaces priced by level, so a tenth weapon's level II cost the same 150 as the first one ever
bought. One ladder is what "the points to unlock your next weapon type or upgrade goes up by 25%"
describes.

⚠ **Only a PAID purchase advances it.** A combination earned from a boss is free, so counting it
would make a reward quietly raise the price of everything else. `cost` is written by `furiousBuy`
and by nothing else, which is what separates the two.

⚠ **Each purchase records the price it actually paid.** That is what makes a moving ladder safe:
re-tuning the base or the step later cannot re-price what an existing profile already bought.

## 3. Where a combination comes from

A combination is one ELEMENT on one WEAPON SLOT. Fire on the machine gun is INCENDIARY SLUGS and is a
different thing from fire on the laser.

**Every boss death drops exactly one**, at the point the boss died, naming a pair the player does not
own yet — biased toward the stage's own element and toward the weapon in their hands, so it reads as
belonging to the fight that paid for it. It pays nothing only when there is nothing left to give.

Picking it up owns that pair permanently: `forge_<elem>_<slot>_C` in the same profile store as the
Armory's levels, with no `cost` on the record, surviving `achievementNormalize`.

⚠ **The drop is guaranteed, not a roll.** "Thats how we gain new combinations" is a progression
promise; a boss that sometimes paid nothing would stall the whole system behind chance.

⚠ **A field infusion pickup no longer licenses anything.** It used to call `forgeDiscover(elem)` and
open that element on all nine slots at once — one crate on stage 1 unlocking nine combinations, which
is exactly the "you dont unlock all these weapon combination upgrades" Mike ruled out. It still
records what has been seen; `forgeElemsFor(w)` is what may actually be combined.

## 4. What each screen does

- **THE FORGE** combines an EARNED pair onto its slot. Its element strip is the slot's own roster:
  earned elements lit, the rest dim, captioned EARNED FOR THIS WEAPON. A pair that was never given
  is refused in words.
- **THE ARMORY** sells LEVELS II–V of a pair you already own, at the ladder price. A row for an
  unearned pair is dim, says BOSS DROP, shows no price, and refuses with `EARN <NAME> FROM A BOSS
  FIRST`. ⚠ Selling the level of a combination you cannot use would be an undeliverable sale, which
  is the rule the Vault already follows.
- **THE VAULT** has no EXCHANGE row any more. The conversion is automatic at the end of every level,
  so there was nothing there to press.

## 5. STYLISH

A barrel roll and a somersault both set `player.invuln` for their whole duration, and the enemy
bullet loop returns on `invuln>0` **before** it tests the hitbox — so a round that would have hit you
is exactly a round that overlaps the hitbox during those frames. `stylishCheck` runs in front of that
return, gated on a live manoeuvre, so ordinary post-hit or respawn i-frames — where you were lucky,
not stylish — award nothing.

⚠ **One award per manoeuvre.** A roll through a curtain of twenty rounds would otherwise pay 10,000,
more than the level converts.

The word types in, holds glowing, and is erased from the front in the same order it arrived. It is
drawn in SCREEN space through `worldXformEscape` at a fixed place, because seeding it from `player.x`
— a WORLD x — would put it up to a camera's width off centre on a wide stage.

⚠ **The glow is offset copies at the same size, not one larger copy.** A 1.14× pass centred on the
same point puts every glyph's edge somewhere different from its core and reads as ghosting. Rendered
and looked at, not reasoned about.

## 5b. STAGE THOROUGH — the award the income model assumes

Mike listed what a player should plausibly earn on Level 1: *"finishing on insanity, hard, normal,
easy, defeating the level without dying and earning a set amount of points thats 75% of what you
could accuimalate if you were to kill all enemies, collect as many items, powerups etc."*

That last one did not exist. The registry had STAGE CLEAR, NO DEATH and MISSILE DISCIPLINE and no
score award at all — and the whole "1-4 achievements on Level 1, therefore price an upgrade at 1,000"
argument rests on it being there. `stage_score_<n>` — STAGE N THOROUGH, 200 points, nine rows — is it.
Registry definitions: 66 → 75.

⚠ **The ceiling is measured from the stage, never hand-written.** `stageStats.scoreMax` accumulates
what the stage actually put on the field: every enemy's own score as it spawns, every pickup at 250 as
it appears, and the boss bonus. A table of per-stage ceilings would be wrong the day a wave was
re-tuned, and wrong *silently* — the award would quietly become trivial or impossible. Measured on a
real 30-second run of stage 1: 19 units and 8 pickups gave a ceiling of 9,240.

⚠ **It is accumulated at `enemies.push`, the one place every spawn path converges.** `spawnEnemy` has
several exits and a switch that overwrites earlier assignments, and the drone path increments
`spawned` before its object exists — so the counter beside it is not a safe hook for anything needing
`e.score`.

⚠ **A ceiling of zero must award nothing.** `got >= 0 * 0.75` is true, so a stage that offered
nothing — a debug jump, an empty fixture — would hand out a free award on a score of zero. That arm
is driven deliberately in the probe.

The numerator is this level's own delta, the same quantity the conversion uses, so a fat score
carried in from stage 1 cannot buy stage 2's award. The kill chain and the STYLISH award are *not* in
the ceiling, which makes the bar easier to clear: skilful play should clear it, and a ceiling
including every bonus would demand a perfect run rather than a thorough one.

`_BUILD_SOURCE/probe_thorough_0917.py` — **12 ok / 0 fail**, real Chromium, 0 errors.

## 6. Verified

`_BUILD_SOURCE/probe_bossdrop_0917.py` — **34 ok / 0 fail**, real Chromium, 0 page or console errors.
The ladder, the pool, a real `bossDie()` leaving one pickup at the boss's position, the grant
surviving a save round trip with no cost, the Forge and Armory refusals, the per-slot element list,
the 250 pickup, and the STYLISH award read back as lit pixels on the canvas as it types in and out.

`_BUILD_SOURCE/probe_armory_0917.py` — **32 ok / 0 fail**, the conversion driven through the real
`computeStageResults`, the run end banking nothing, and a level bought through the UI with real key
presses.

`_BUILD_SOURCE/probe_dropreach_0917.py` measures the reachability window: the drop lands in the
playfield, holds, closes on the player and is collected at frame 107 of a fight that stays in PLAY
until frame 346. Before the fix it survived **0 frames**.

Proof frames: `docs/proofs/bossdrop_0917/`.
