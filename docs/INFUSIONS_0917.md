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

The drop is a **kill drop**, beside the bomb / shield / life roll — `INFUSION_DROP_P` (0.14) × `dropMul`
inside `dropPowerup`, which itself sits behind killEnemy's 18% drop gate (⚠ at the first 0.055 that
was about one infusion per 100 kills, measured 2 in 300 on HARD — too rare to be felt), biased by
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

⚠ **THE BOLT ART IS WARMED AT GRANT, NOT AT THE FIRST BOLT** — `XART.rdy` is false on its first
call. ⚠⚠ **BUT THAT WAS NOT WHY THE BOLTS WERE INVISIBLE, AND THE DIAGNOSIS ABOVE WAS WRONG** (found
later the same night by `probe_wrath_0917.py`, which waited for the reel in real time and STILL
recorded zero bolt blits). `updatePlay` hard-clears the zap list every frame unless Yuri's special
is live — `if(!specialActive('yuri')) zaps.length=0` — so every lightning arc and every one of the
wrath's sixteen bolts was deleted the frame it was born, for every pilot but Yuri mid-special. The
white-out and the damage were real; the picture never had the bolts in it. Infusion zaps are tagged
`_inf` now (chainZap tags while `_infBusy`, godsWrath tags its own) and only Yuri's untagged zaps
are hard-cleared. Measured: **72 bolt-art asks** in the frame that draws the wrath, 0 before
(`docs/proofs/infusion_0917/12_gods_wrath_bolts.png`). **A "not decoded yet" explanation for a
missing sprite is a hypothesis, not a finding, until the reel is proven decoded and the sprite is
still missing.**

Suite section 367. Proofs: `docs/proofs/infusion_0917/01_fire_rounds.png`, `02_gods_wrath.png`,
`docs/proofs/infusion_0917_icons.png`.

---

## 7. Later the same night: the other carriers, CHROMIUM, and the cross-element geysers

**The beam and the missiles wear the element now.** The beam goes through the same `xartPalette`
swap its tier colours already use (`INFUSIONS[elem].body` at every tier); an infused missile is the
pilot's own missile plate through `xartPalette` under a soft halo in the element's glow
(`infusionMissileDraw`, falling through to the normal draw while the swap cannot be built).
⚠ **THE BEAM IS ONE OBJECT REUSED ACROSS SHOTS** - `pShoot` finds it in `pBullets` and re-arms it -
so the once-only `_inf` stamp left it wearing the element it was born with after a new pickup. It is
restamped every frame. `probe_infusion_carriers_0917.py` 7/0: the plate swaps identified by KEY and
by the element's body colour, a second pickup re-stamps the same beam, and the control (no infusion)
swaps nothing.

**CHROMIUM** (*"chromium energy upgrades"*) is the ninth element: a hit MIRRORS every enemy round
within `38+16*lv` px of the impact - the round dies where it is and a bright shard leaves that point
straight up the screen as the player's own (`chromeMirror`). Level 3 **MIRROR SHELL** turns the
whole screen on a kill. Shards wear the chrome palette (`_inf:'chrome'`) and are marked `_mirror` so
they can never mirror again. Stage 6's bias moved from lightning to chrome (the neon city). Badge
generated against the prism badge as the reference; the variation with the family's hex ring shipped.

**The geysers Mike named** - fire, water, lightning: water's own at level 3 (and 35% at level 2), and
a **soaked** target (water has hit it) killed by fire or lightning raises THAT element's column.
`probe_chrome_0917.py` 10/0, with a DRY-target control that raises none.

**The water orb** (*"the water combinations after level 9 where we can now create water orb"*): the
orb weapon's wheel and its shards are carriers now (`INFUSION_CARRIERS.orb/shard`), and an infused
orb is the authored 0825 ice wheel through `xartPalette` in the element's body colour - tidal blue
for water, slime green for toxic - with the halo in the element's glow. Ice keeps the authored
plate. Measured in the carrier probe (10/0): a live orb carries `water` and the wheel is asked for in
`#3fa7ff`; the plain orb asks for no swap.

**The giant beam** (*"giant laser beams like the fireboss has"*): a KINETIC infusion on the laser
widens `beam.w` x1.5 / x2.0 / x2.5 by level, and because the draw and the hit test both read
`beam.w`, the wider column burns a wider lane. `probe_giantbeam_0917.py` 7/0: the object, the blit
(88px against 35.2 at level 3, off the context's own `drawImage`) and a unit 38px off the centre
line missed by the plain beam and burned by the giant one.

**The sonic wave** (*"sonic wave based upgrades"*): KINETIC level 3 on the machine gun or spread
also releases Cole's own half-charge sonic wave (`sonicRelease(0.45)` - the authored piercing wave,
not a new projectile) every 24th round. Counted on ROUNDS at the stamp site, so the cadence follows
the gun's and a probe can reproduce it: 7 waves from 180 rounds, none at level 2.

**FUSION** (*"surprise me with some fun upgrades"*): a level-3 element replaced by a DIFFERENT
pickup does not go quietly - the pair detonates once across the screen before the new element takes
the gun at level 1. Every on-screen hostile takes 30 and BOTH elements' touch (burn + freeze stack
for fire+ice), the blasts wear the new element's colour, and a chrome pair mirrors the whole
screen. Named by the pair in `INFUSION_FUSIONS` - THERMAL SHOCK, NAPALM, HYDRO VOLT, SPECTRUM,
SHOCKWAVE INFERNO, EVENT HORIZON, TESLA MIRROR, FLASH FREEZE, AVALANCHE, ACID RAIN, BLACK SUN,
KALEIDOSCOPE - and a plain FUSION otherwise. The same element again still just caps; a level-2
element traded away fuses nothing, so the fusion is the reward for holding a named combination and
choosing to trade it. `probe_fusion_0917.py` 9/0.

**The void beam** (*"Dark Matter ... Void like weaponry"*): DARK on the laser bends the field -
every hostile within `90+30*lv` px of the live column is drawn toward it at `40+25*lv` px/s, so the
beam gathers what it burns. One lookup per frame in the enemy loop; tanks and set pieces are not
moved. Carrier probe: a drone 80px off the column is at 37px after half a second; a fire beam moves
it nothing.

## 8. Still to come on this brief

Water and dark are wired and gated but have not been driven in play (their gates are closed on a
fresh profile). The **geyser attacks** exist as a mechanism (`geyserSpawn` — fire, water, lightning)
and fire from water L3 kills; a geyser *weapon* is not built. **Chromium energy** is not built. The
laser beam and missiles now carry the palette (§7). **New Game +** is built (`docs/NGPLUS_0917.md`).
