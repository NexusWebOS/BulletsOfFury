# 0917 — Weapon infusions: the combination system

Mike, overnight brief: *"toy around with being able to toy around with the orbs, lasers, missiles
and pellet based weapons. Combinations could be incendiary bullets, lightning bullets, ice bullets
or lasers or missiles. This does not apply to level 5 or level 9, space levels are in-eligible from
this system. You may also wire up kinetic energy, sonic wave based upgrades ... the water
combinations after level 9 ... chromium energy upgrades, prism upgrades and toxic/sludge/slime
upgrades for poison and decay damage ... Prism Wave, Luminaire, Eradication, Fireburst, Glacial
Strike, God's Wrath ... Dark Matter ... only be used in New Game +."*

---

## 1. What an infusion is

An **infusion** is an element layered on whatever **carrier** the pilot is holding — the machine
gun, the spread, the laser, the chaingun, the missiles. It is not a weapon slot: it never changes
what you are holding. It changes what the round *does* when it lands, and what it looks like on the
way.

It rides the round as `b._inf`, stamped the first frame the round is live, and fires from **one
hook** inside `_hitEnemyCore` — where `_dmgBullet` already names the live round. Three levels per
element: picking the same element again raises it, a different element replaces it at level 1.
Level 3 is the **named** combination from Mike's list. Death clears it, the way death drops the gun.

| element | rounds | on hit | level 3 |
|---|---|---|---|
| **fire** | INCENDIARY | the target **burns** (the incendiary shotgun's own `_burn`) | **FIREBURST** — the hit detonates, igniting neighbours |
| **ice** | GLACIAL | the target is **slowed**; every 3rd / 2nd hit stacks a **freeze** | **GLACIAL STRIKE** — every hit stacks a freeze; three shatters |
| **lightning** | VOLTAIC | the hit **arcs** to a neighbour (`chainZap`) | **GODS WRATH** — a kill can strike every hostile on screen from the sky, with a white-out and blasts |
| **prism** | PRISM | the hit **splits** into 2 shards past the target | **LUMINAIRE** (L2, 3 shards) → **PRISM WAVE** (5) |
| **toxic** | TOXIC | the target is **poisoned**, ticking with no more rounds | **ERADICATION** — a poisoned kill spreads to a neighbour |
| **kinetic** | KINETIC | +15%/level damage and **knockback** | **SONIC WAVE** — a shock ring on the first hit |
| **water** *(after stage 9)* | TIDAL | the target is **soaked** — takes lightning 35% harder | **GEYSER** — a kill raises a column that hurts what crosses it |
| **dark** *(New Game + only)* | DARK MATTER | pulls nearby hostiles toward the impact | **VOID** — a kill opens a point that pulls and eats |

Fire and ice carry the **element** (`b._el`), so the existing 2× / absorb rules apply to an
infused round unchanged.

---

## 2. Every effect reuses a mechanism the game already had

Fire sets `e._burn`, which is Decker's incendiary shotgun's burn (`dkBurnTick`). Ice stacks
`e._frozen`, the ice weapon's own counter — three shatters, by the rule already in `killEnemy`.
Lightning *is* `chainZap`, Yuri's arc. A second burn system beside the first is how a codebase ends
up with two flags sharing one name (0810q), and it is the thing this design refuses to do.

⚠ **THE ON-HIT HOOK MUST NOT RE-ENTER ITSELF.** `chainZap` calls `hitEnemy` on the arc's target
while `_dmgBullet` is *still* the infused round — so without `_infBusy`, a lightning hit arcs, the
arc hits, the hit arcs again, and it only stops when the hitset runs out. Guarded, released in
`finally`.

---

## 3. Eligibility is a rule, not a list

`infusionEligible()` refuses stage 5, stage 9, any stage whose `bg` is `space`, and any time the
space weapons are live. The probe drives it: **400 kill drops on stage 5 yield zero infusion
pickups; 600 on stage 2 yield 41.** Water opens on the same signal LASER MIST already opens on
(`laserMistIsUnlocked`, i.e. a real stage-9 boss kill); dark matter on `run.ngplus`.

The drop is a **kill drop**, beside the bomb / shield / life roll — 5.5% × `dropMul`, biased by
stage (fire on 2, ice on 3, lightning on 4 and 6, toxic on 7, prism on 8) but never locked, so every
element stays reachable anywhere it is eligible.

---

## 4. The round wears it

An infused round skips the 0825 plate and goes through the P87 pack, which is the path that can
wear a palette — `p87Body(lv, inf)` swaps to the element's body colour and `p87Draw` takes the
element's glow, so the element is visible **in flight**, not only on impact. The equipped box
carries a badge of the element top-right of the weapon icon with its level as pips.

**Eight badges** were generated as one sheet in the weapon-badge family (hex ring, dark field, one
emblem). ⚠ **The first variation baked my prompt's own words into the badges** — `FLAME`,
`ICE CRYSTAL`, `LIGHTNING BOLT` — the 0916 medal-sheet trap, exactly. Read before slicing; the
other variation shipped.

---

## 5. Prism shards start on the far side of the target

Spawned at `(e.x, e.y)` they sat inside the hitbox that had just been struck and were eaten by it
the same frame — the probe counted **zero** shards in flight on a build that was pushing five.
Refraction continues *past* the thing it hit, which is also where the shards belong: they now start
`(size/2 + 8)` along the round's heading, beyond the target. Shards are stamped `_inf: null` so they
can never split again.

---

## 6. Verified

`probe_infusion_0917.py` — **31 ok / 0 fail**, 0 page or console errors. Every element through the
real path: a round pushed by `pShoot`, stepped by the live loop, landing through `_hitEnemyCore`,
asserted on the **target**:

    FIRE       burning after the hit (2.60s), and still losing hp with no more rounds
    ICE        slowed (vy 2.0 -> 0.61); GLACIAL STRIKE stacks a freeze every hit
    LIGHTNING  the hit arcs (2 zaps) and the neighbour loses 10hp
    PRISM      4 shards in flight past the target, every one stamped _inf null
    TOXIC      poisoned (2.80s), ticking with no more rounds (56 -> 52)
    KINETIC L3 the same rounds deal 5.8 where plain deals 4, and the target is shoved 26px
    GODS WRATH 16 zaps, all five hostiles struck, on a single kill
    the round draws through the pack with the FIRE palette (2 fire draws in the trace)
    the pickup grants; death clears

⚠ **THREE PROBE FAULTS, ALL MINE.** The drones I spawned as targets were **shooting the player**
during the 60-frame runs, so by the pickup test the pilot was dead — the pickup "failed" and the
death test "passed" on an infusion that was never granted, two green-looking results from one
corpse. The prism window was 12 frames and the round reaches the target on frame ~12. And the palette
trace demanded every `p87Body` call be `fire` when the **muzzle flash** legitimately draws through
it with none.

⚠ **THE BOLT ART IS WARMED AT GRANT, NOT AT THE FIRST BOLT.** `XART.rdy` is false on its first call,
so the first god's wrath of a run was drawing sixteen bolts through the thin fallback line. Warmed
in `infusionGrant('lightning')`. The probe's synchronous burst still cannot give it decode time —
the proof frame shows the white-out and the struck hostiles, and real play will show the bolts.

Suite section 367. Proofs: `docs/proofs/infusion_0917/01_fire_rounds.png`, `02_gods_wrath.png`,
`docs/proofs/infusion_0917_icons.png`.

---

## 7. Still to come on this brief

Water and dark are wired and gated but have not been driven in play (their gates are closed on a
fresh profile). The **geyser attacks** exist as a mechanism (`geyserSpawn` — fire, water, lightning)
and fire from water L3 kills; a geyser *weapon* is not built. **Chromium energy** is not built. The
laser beam and missiles carry the on-hit effects but not yet the palette. **New Game +** is next.
