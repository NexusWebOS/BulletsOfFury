# The Warhive Carrier and the Nightwing Ace — Stage 6's new boss (0918)

Mike's spec, 0918 (condensed):

> A giant jet carrier comes down on screen with massive thruster noise. It does not cut into the boss
> music and shows no HP bar. It opens its bay door and about 6 elite black fighter jets come out. It
> raises backwards while closing the door and goes off screen until the jets are defeated, then comes
> back. Repeats until both spinning thrusters are destroyed. Smoke and fire anchored to the modular
> pieces, slow → mid → fast → massive blow up. As the carrier goes down and blows up, a super-elite
> blue-black fighter jet emerges and becomes the boss. It mirrors the player's kit: missiles, retina,
> somersault, barrel roll. Smart reactive AI: partly input detection, partly orbiting/position
> detection, partly RNG. **Hard:** 8 jets, +25% thruster and door HP, the thrusters become cannons
> (glowing energy balls, single flurries, spreads of 3, a charge-up into a beam 1/3 of the screen),
> and the ace gains a charge dash, a helper orb at 50%, and at 25% a fast charge off the bottom,
> criss-cross wobbling passes, then a somersault into inverted flight, shadowing the player's lateral
> position while firing volleys.

Mike, on the first escort pick: *"no, that was cole's ship recolored. your going to make new ones
inspired by these designs and stage 6's enemy roster."* So every plate below is NEW SpriteCook art.

## Where it lives

| what | where |
|---|---|
| stage slot | `STAGES` stage 6 `boss:'warhive'` — `'doomsdaycarriermk2'` restores the Mk II fight, which is kept whole and still spawns by kind |
| rig | `warhiveInit / warhiveTick / warhiveDraw / warhiveHitTest / warhiveDamage / warhiveRetinaTargets`, all `whv*` helpers, placed just above `updateBoss` |
| hooks | `spawnBoss` switch, top of `updateBoss`, top of `drawBossInner`, `bossHitTest`, `hitBoss` (beside the hammer), `bossHealthVisible`, `retinaBossTargets`, the boss-warning music line, `drawBoss` fade |
| escort | `ELITEX.hivewing` + `case 'xelite_hivewing'` + `ENEMY_ART.xelite_hivewing`, driven by its own `hivewingTick` — NO shield (Mike 0918) |
| art | `assets/game/bosses/skycarrier/` (25 PNGs), registered at the top of game.js beside the Tempest |
| probe | `_BUILD_SOURCE/probe_warhive_0918.py --diff normal|hard` — Normal 19/19, Hard 24/24, 0 errors |
| proofs | `docs/proofs/warhive_0918/{normal,hard}/` + `hard/_beam.png` |

## Art (SpriteCook, 0918)

- **Carrier**: one 512×288 plate in three door states — `carrier_closed`, `carrier_open`,
  `carrier_broken`. The two door states are `edit_asset_id` edits of the closed plate (silhouette IoU
  **0.994**), so the ship never moves when the door changes. Generated against the Doomsday Carrier's
  plate as the style reference.
- **Fan** (`carrier_fan`): a 12-blade rotor, drawn spinning inside each nacelle — the spin is a real
  in-plane rotation of a radially symmetric part, not a derived bank.
- **Wrecked nacelle** (`carrier_thruster_wreck`): drawn over a dead thruster. Nothing detaches.
- **Escort** (`elite_jet`): matte black / blood-red trim, cranked delta, generated against a sheet of
  Stage 6's own roster (the black flying wing, the steel fighters) plus the Void Reaver and Iron
  Serpent aces as a style reference.
- **Ace**: `ace_top`, `ace_belly` (an edit — the generator can draw a VIEW, 0906y), `ace_damaged`
  (an edit, swapped in under 50%). The barrel roll `ace_br0..7` and somersault `ace_so0..7` are
  DERIVED by foreshortening between the top and belly views, exactly the 0906y method.
- Every plate is palette-locked with dither OFF (83/84/83 colours on the carrier, 72 on the ace, 46 on
  the escort, 38 on the fan) — the 0905 SpriteCook trap: its output is never true pixel art.
- Credits: 404 spent (2,213 → 1,809), including the rejected candidates.

Measured geometry (plate px, centre-relative): nacelle hubs **(±169.5, −10)**, fan disc radius
**24**, pod radius **37**, bay door **(0, 45) 83×82**. Draw scale **0.9** (461×259 on screen).

## The fight as built

**Carrier** (no HP bar; the stage track keeps playing):

1. `descend` — 2.6 s ease-out from off-screen to y 142, thruster + rumble loops, the fans spooling up.
2. `open` — the bay opens at 0.35 s with a hiss, a puff and a thump.
3. `launch` — one escort every 0.42 s (Normal) / 0.5 s (Hard) out of the bay: **6 / 8**.
4. `hold` — 3.6 s (Normal) / 5.2 s (Hard) on station: the window to shoot the parts.
5. `retreat` — the door closes, and the carrier backs up off the top of the screen, accelerating.
6. `away` — it waits until every escort is dead or has left (45 s safety), then comes back.

Objectives are hit regions on the plate: **left thruster, right thruster** (520 HP Normal; ×0.8 Easy,
×1.25 Hard, ×1.35 Furious) and the **bay door** (half a thruster). A round on bare hull armour does
nothing. The Retina targets the three parts while the carrier is on screen. Breaking the door leaves
it open for good. Killing both thrusters ends the carrier.

Damage shows without a bar, anchored to each part every frame: **>75%** clean · **<75%** one slow
smoke plume · **<50%** smoke + a small fire · **<25%** two fast plumes, a bigger fire and pops ·
**dead** a six-blast blow-up with two shock rings, a shake and a flash, then the wreck plate burning.

**Hard cannons** (only while the door is open on screen): the live thrusters take turns through
**flurry** (5 aimed cyan energy balls, 0.2 s apart) → **spread** (two volleys of 3) → **beam**
(1.55 s shared green/yellow/red warning cone, then a cyan beam **VW/3 = 160 px** wide straight down
for 1.25 s). The charge glows in the fan before every attack.

**The fall** (4.4 s): every escort is killed, and the carrier sinks with accelerating chain
explosions. The door bursts at 1.5 s. At **2.4 s the ace launches out of the bay**, the boss track
starts and the HP bar appears. At 3.6 s comes the final blast (nine large blasts, three shock rings,
a flash), and the hull goes out.

**Nightwing Ace** (b.hp = the engine-settled maxhp; the bar is the ace's own):

- **Movement**: three sources are mixed. Input detection leads the player's own velocity. Position
  detection is an orbit swing around the player's column. RNG picks a new offset every 1.1–2.3 s. It
  stays in its own airspace (y 74–232).
- **Barrel roll**: a player round climbing into the hull triggers a roll away. It uses the player's
  0.46 s window and a 150 px dash, with i-frames, a 60% chance on Normal and 80% on Hard, and a
  cooldown.
- **Somersault**: triggered by a player missile within 150 px, or a player Retina LOCKED on it.
  It uses the player's 0.62 s window, with i-frames.
- **Guns**: twin streams when lined up with the player, as three-round bursts.
- **Missiles + Retina**: 2 (Normal) / 4 (Hard) lock-bound missiles through `enemyLockOn`, so the
  player's roll, somersault or a shoot-down breaks them (the 0912q header rule).
- **Hard, charge dash**: a 0.95 s shared-warning lane, the aim committed at 60%, then a 440 px ram
  with afterimages and an eased return.
- **Hard, 50%**: a helper orb (Falva's, palette-swapped to the ace's blue). It orbits at 54 px and
  fires 5-bolt spreads.
- **Hard, 25%**: a warned charge off the bottom of the screen, then three criss-cross passes. Each
  pass is warned 0.62 s ahead, flies from the camera edge and wobbles. Then it re-enters from the
  top, somersaults, and holds **inverted** (belly plate). Inverted, it glides to the player's x
  ("I go left, he goes left") inside its own zone, fires 3-way volleys, and somersaults again every
  3.5–5 s.
- **Death**: the player's own death mirrored — a spin-out with explosions anchored to the hull for
  2.4 s, then the crash (seven blasts, three shock rings), then the whiteout.

## The escorts — elite by pattern, not armour (Mike 0918)

*"Please do not use shields on our elite jets here, when I meant elite, I meant their patterns, attack speed and
styling is considered elite."* So `hivewing` has no shield (60 HP ×DIFF) and its own `hivewingTick`:

- **Squadron slots.** Each jet holds a slot in a staggered two-row line 54 px apart. The line tracks
  a blend of the player's column and the screen centre, and weaves.
- **Fast aimed bursts.** 3 rounds 0.07 s apart at 4.4 px/frame, every 0.9–1.3 s ÷ `DIFF.eFire`.
- **Strafing dives, one at a time.**
  - A 0.4 s nose-flash tell comes first.
  - Then a committed run at 380 px/s down the vector to where the player WAS, firing along its
    heading every 0.075 s and trailing smoke.
  - The dive stops at 80% of the screen height, then the jet climbs back to its slot.
  - Dives are staggered by slot, and `hivewingDiving()` holds the others off while one is running.
- **Faster evasive roll** (230 px/s) out of rounds climbing into it.

## Known / for Mike

- Carrier hull contact hurts the player, like any boss body.
- Numbers to tune after play: thruster HP 520, hold windows 3.6/5.2 s, ace roll chance 0.6/0.8, ace
  missile cadence 6–8 s.
- The Doomsday Carrier Mk II is not deleted. Setting stage 6 back to `'doomsdaycarriermk2'` restores
  it.
