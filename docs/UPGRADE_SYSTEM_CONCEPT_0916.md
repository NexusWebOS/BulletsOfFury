# The Weapon Forge — an upgrade screen between stages (concept, 2026-09-16)

Mike: *"make a note that I may want an upgrade system after our stats screen inbetween each level
where you can combine weapons to create new ones, which I think would be so fucking cool. generate a
graphical screen for this, and a concept of what we could do and upgrade and how that would work.
A few concepts would be great."*

This is a design note, not a build. Nothing here is wired. It sits on top of what the game already
has, and every number is a starting point for Mike to change.

**Concept plates:** `docs/marketing_0916/forge_concept_a.png` (round socket, two inputs left and
right of one output) and `forge_concept_b.png` (two inputs stacked, one output). Both are edge-to-edge
plates in the debrief's own language — the same steel, amber trim and recessed bays as the stat
screen, so the Forge reads as its third page: **debrief → unlocks → forge → next stage**.

---

## Where it sits in the flow

```
STAGE CLEAR (stats)  →  NEW WEAPONS UNLOCKED  →  THE FORGE  →  campaign map / next stage
```

The Forge only appears when the player is carrying something it can use — two or more fusible
weapons at level 2+, or a spendable resource. If not, it is skipped exactly the way the unlock page
is skipped when a stage has no row. A screen that shows up empty teaches players to mash through it.

---

## What the game already has that this builds on

- **Nine weapon slots** (`WEAPONS`): machine gun, spread, missiles, laser, flamethrower, ice orb,
  laser mist, chaingun, lightning orb — each with **five levels** (`run.wlevels`).
- **Held variants** (`run.wvars`): the same slot already carries a *variant* — flamethrower vs ice
  breath, ice orb vs fire orb vs **Thermoshock**. Thermoshock is the proof of concept: the game
  already fuses fire and ice into one weapon on stage 3. The Forge makes that a player choice
  instead of a scripted event.
- **Elements** (`attackElement` / `elementMultiplier`): fire, ice, and the 2x-against-opposite rule.
- **Manual missile tiers** (Standard → Super → Ultra → Uber) with caps.
- **Pilot specials**, one per pilot, on a timer.
- **Passwords and the campaign save slot**, which is where a persistent loadout would live.

---

## Concept 1 — FUSION (the one on the plates)

Two weapons in, one new weapon out. You pick two slots you hold at **level 3 or higher**; the Forge
consumes one level from each and produces a fused weapon that occupies one of the two slots.

| Input A | Input B | Fused weapon | What it does |
|---|---|---|---|
| Fire Orb | Ice Orb | **Thermoshock** | already in the game — this is the canonical fusion |
| Fire Orb | Lightning Orb | **Plasma Orb** | orb that arcs to a second target on impact, burns both |
| Flamethrower | Spread | **Napalm Fan** | five short flame tongues in the spread pattern |
| Ice Breath | Laser | **Cryo Beam** | a laser that slows what it touches; frozen enemies shatter for bonus |
| Missiles | Lightning Orb | **Storm Rack** | missiles that chain-lightning between targets they pass |
| Machine Gun | Laser | **Rail Gun** | slow cadence, pierces everything in the lane |
| Chaingun | Flamethrower | **Inferno Gatling** | the chaingun's heat bar becomes a fire bonus instead of an overheat |
| Spread | Ice Orb | **Shard Storm** | spread shot of ice shards that freeze on hit |
| Laser Mist | Lightning Orb | **Tempest Mist** | the three-lane mist with lightning between lanes |

Rules that keep it honest:
- **Fusions are elemental.** Anything with fire or ice in it inherits the element and the 2x rule.
  Plasma Orb is fire+shock; Cryo Beam is ice. Nothing is neutral by accident.
- **You cannot fuse a fusion.** One tier deep. Depth is where these systems become spreadsheets.
- **Fusions can be undone** at the next Forge (you get both parents back at level 1). Experiments
  should never lock a player out of a build they liked.
- **Freezer never gets fire orb**, so his fire fusions route through Thermoshock instead — his table
  is his own, the same way his crate bag already is.

## Concept 2 — MODS (attach, don't merge)

Instead of merging two weapons, you attach a **mod** to one. Mods are earned, one per stage clear
(they replace nothing; they appear in the unlock page's empty slots). Each weapon has **two mod
sockets**.

| Mod | Effect on any weapon |
|---|---|
| Overclock | +25% fire rate, -1 level of damage |
| Heavy Shell | +1 level of damage, -20% fire rate |
| Homing Gel | rounds curve gently toward the nearest target |
| Piercing Core | rounds pass through the first enemy |
| Elemental Coat: Fire / Ice / Shock | gives a neutral weapon an element |
| Ricochet Plate | rounds bounce once off the screen edge |
| Wide Bore | spreads the pattern 30% wider |
| Vampire Load | kills restore a sliver of shield |

This is cheaper to build than fusion — it is multipliers and flags on the existing weapons, no new
projectile art — and it is what most of the "so fucking cool" moments actually come from
(a homing, piercing flamethrower is a thing a player will tell a friend about).

## Concept 3 — SPECIAL TUNING (the pilot's own ability)

The nine specials are fixed. The Forge lets each pilot spend **Fury** — a currency earned per stage
from rank (F=5, S=4, A=3, B=2, C=1, D/L=0) — on their special:

- **Charge time** (faster recharge)
- **Duration**
- **Reach** (Cole's boom radius, Juggernaut's ball orbit, Freezer's freeze radius)
- One **signature upgrade** per pilot at max: Juggernaut's two wrecking balls become **three**;
  Cole's sonic boom fires **twice**; Freezer's time freeze **shatters** frozen enemies on release.

Fury not spent carries over, so a player who wants to save for the signature can.

## Concept 4 — THE ARSENAL DRAFT (arcade only)

Between stages in **arcade**, the Forge offers **three random cards** and you take one: a fusion
recipe, a mod, or a special tune. Three picks, one run, no persistence. This is the roguelite shape
and it is the cheapest way to make every arcade run feel different without touching the campaign.

---

## Recommendation

Build in this order:

1. **Mods** — flags and multipliers on existing weapons, one screen, immediate variety.
2. **Special Tuning** — a Fury currency gives rank a *reason*, which the stat screen currently lacks.
3. **Fusion** — the headline feature, but every recipe is new projectile art and a new draw path.
   Thermoshock exists as the template; each further fusion is roughly a day's art and a day's code.
4. **The Draft** for arcade once the pool of mods and recipes is deep enough to draw three from.

## How it would work in code (so nobody has to rediscover this)

- **A state `GS.FORGE`**, entered from `scLeaveStage()` the way the unlock page is — the exit
  refactor done for the unlock screen is exactly the seam the Forge needs.
- **Fusions are `run.wvars` values.** `heldVariant(w)` already decides element, art and projectile
  from the variant; a fusion is a new variant string on an existing slot. `WVAR_NAME`, `weaponIconKey`
  and `drawBullets` each gain a row. Thermoshock is the worked example of all three.
- **Mods are a `run.wmods[w]` array read at the three chokepoints**: cadence (`WEAPON_CADENCE` /
  `pShoot`), damage (`_hitEnemyCore`), and projectile spawn (the homing/pierce flags already exist
  on bullets for enemies — `b.homing`, `_shootable` — the same fields serve the player).
- **Fury lives in the campaign save** beside `contUsed` and the unlocks; arcade drafts live only in
  `run`.
- **Art:** the Forge plate is the debrief plate's sibling and its bays get measured the same way
  (flood the recesses, take fractions) — see `SC_SLOTS_FULL` and the note beside it. Weapon icons
  already exist for every slot (`micon_*`); fusions need one icon each.

## Open questions for Mike

- Do fusions persist across a campaign save, or reset every stage?
- Is the Forge in **co-op** per seat (two Forges) or shared?
- Should the Draft replace the unlock page in arcade, or follow it?
- Which three fusions ship first? Plasma Orb, Napalm Fan and Cryo Beam are the ones whose art is
  closest to what already exists.
