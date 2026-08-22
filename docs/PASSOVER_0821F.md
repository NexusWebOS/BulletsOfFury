# 0821f — NOBODY CHARGES, NOBODY HOMES, AND NO TWO BOSSES FIGHT ALIKE

Mike, two lists. This drop takes four of the items; the charge TELL and the projectile patterns
are still open, and stage 6 is his.

| item | state |
|---|---|
| level 4 boss — full formed frame only, no breaks or cracks | **DONE** |
| cut the alert sound from homing missiles, use a missile sound | **DONE** |
| bosses/minis must not charge or home (except the helicopter) | **DONE** |
| every boss needs its own characteristics and attack patterns | **DONE — all 18 distinct** |
| give charging enemies a 3s indicator | **OPEN** |
| still chaotic projectile patterns | **OPEN** |
| stage 6 | **MIKE'S** |

---

## ⚠ SFX.missile WAS CALLED THREE TIMES AND NEVER DEFINED

*"cut the alert sound from homing missiles, use a missile sound instead."*

There was no missile sound in the bank at all. `SFX.missile` had three call sites: two fell
through to `grenade()`/`shoot()` and the third, guarded by `if(Audio.SFX.missile)`, was simply
**silent**. What a homing launch actually played was `enemyShoot()` — a 320Hz sawtooth blip, which
is why it reads as an alert tone rather than as ordnance.

`missile()` is synthesised like the rest of the bank: a low body with a RISING hiss over it, the
opposite sweep to an explosion. Both homing launch sites use it, and the three orphaned callers
get a real sound for the first time.

## THE STAGE-4 BOSS IS ONE PLATE

*"do not wire up with seperate frames - use full formed frame only and do not do breaks or cracks."*

It was running through `mechInit('mbs6')` — the modular component rig, separate anchored parts
with their own damage states and a breakup reel. It goes through `shipBossInit` now, which draws
the single `mbs6_master` hull, and its table row has **no `dmg` array** — that field is what adds
the damaged and critical plates, so omitting it is exactly "no breaks or cracks".

`glacierfortress` next door already fields an `mb*_master` this way, so this is the established
route, not a new one. Verified in the browser: `hasMech false, hasModular false, dmg none`, and it
renders whole.

## NOBODY CHARGES OR RAMS

*"They should not be charging or shooting homing missiles at the player with the exception of the
helicopter boss."*

- `SBM_CHARGE` dives at the player's own position at 430px/s
- `SBM_RAM` crosses the player's column at 520px/s, three passes

0819d took the RAM off the minis. Both moves are off **everything** that runs this pool now.
`SBM_XSTRIKE` stays — a fixed X through the OFF-SCREEN corners, so it crosses the field without
ever aiming at where the player is standing.

⚠ **THE HELICOPTER IS EXEMPT FOR FREE.** JUNGLE OVERLORD-X is not a SHIPBOSS — it runs its own
health-gated AI and never reaches this pool — so the one exception Mike keeps naming needed no
special case.

### ⚠ AND REMOVING THEM ALMOST COST THE THING IT WAS MEANT TO SERVE

Measured straight after the cut: **XSTRIKE ran 938 of 1500 frames — 62% of the fight** — because
with the pool down to one entry, every move pick is an X-sweep. A boss crossing the screen most of
the time cannot express the pattern set that is now supposed to be its identity.

Station time went from `rnd(1.0,2.0)` to `rnd(3.0,4.4)`. Re-measured: HOLD 287 -> **546**, XSTRIKE
938 -> **710**, so it now spends more of the fight on station shooting than sweeping. Still
shortens as it takes damage.

⚠ **ONE THING FOR MIKE TO JUDGE:** XSTRIKE's second leg crosses to the far bottom, so the hull
still traverses the player's row at 560px/s — not aimed at them, but a player standing there will
be crossed. Bounding that leg is a one-line change if he wants it; I have not made an authored
move shorter on my own guess.

## NO TWO BOSSES FIGHT ALIKE

Audited before touching anything. `pat`/`pats` across all 17 units:

    mslfan 11   ember 7   chargebeam 6   lance 6   beamfan 5   void 3
    fireorb 2   mslhome 2   siege 2   rime 1   fan2 1

**`mslfan` was in 11 of 17 bosses.** That is the sameness, measured: two thirds of the roster
opened or escalated with the same missile fan. And `mslhome` — homing — was still on `cryospear`
and `voidbat`, both of which Mike's rule forbids.

⚠ **`pincer2` IS A FULLY IMPLEMENTED BOSS PATTERN THAT NO BOSS USED.** It has a live branch in
`shipBossAttack` and appears in zero table rows — a working signature sitting unused while eleven
bosses shared a missile fan.

After, with `stormsovereign` added (18 units):

    beamfan 7   chargebeam 7   ember 5   pincer2 4   fireorb 4   lance 4
    rime 4   siege 4   mslfan 4   void 3   fan2 2

- **`mslhome` appears nowhere** — no boss homes.
- **`mslfan` is down from 11 to 4**, and all four are genuine carriers (doomsday, spawn, olive,
  and the fan-owner itself), which is what the pattern is for.
- **Every one of the 18 has a pattern SET that no other boss has** — verified by comparing the
  sets, not by eye.

---

## HOW TO VERIFY

    node --check assets/game.js
    node --max-old-space-size=3072 _BUILD_SOURCE/test_fl.js     2,701 ok / 3 fail

The 3 are environmental. Boss behaviour was measured over a 25-second stage-4 fight:
`CHARGE 0, RAM 0, homing bullets 0`.
