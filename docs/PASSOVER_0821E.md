# 0821e — A TAP IS NOT A MACHINE GUN

Mike: *"We need to add a short delay to his laser if you tap the button instead of charge, and a
similar delay to Yuri's Chain Lightning."*

| weapon | before | after |
|---|---|---|
| Maverick's tapped laser | **10 shots/sec** | **3.3 shots/sec** |
| Yuri's chain lightning | 7.1 shots/sec | 3.75 shots/sec |

---

## WHAT WAS ACTUALLY HAPPENING

A tap fell through to `_weaponCadence()`, which is **0.085s** at weapon 0 — the basic pellet gun's
cadence. So tapping fired MAVERICK'S LASER ELEVEN TIMES A SECOND while his HELD lance is 0.38s.
**Tap-spam was strictly better than the weapon's own design**, which is exactly the thing a charge
weapon exists to prevent.

Both delays are **one constant**, `SPECIAL_TAP_CD = 0.28`, sitting next to `TAP_WINDOW`. Mike
asked for Yuri's to be "similar", so making them one number means they cannot drift apart later.

⚠ **THE SHOT STILL LEAVES ON THE FRAME YOU PRESS.** What is delayed is the NEXT tap. A tap that
fires late reads as input lag, which is a worse problem than the one being fixed.

⚠ **SCOPED TO MAVERICK**, who is who Mike named. The tap branch is shared by every charge pilot —
Falva's tap is her ordinary gun and Cole's is the fusion cannon, and neither was reported.

Yuri's was a straight swap of the `0.14` literal in the cadence block.

---

## ⚠ MY OWN MEASUREMENT LIED TWICE BEFORE THE FIX LOOKED APPLIED

Worth recording, because both failures were in the harness rather than the game and both would
have sent the next person editing working code.

**First:** a 4-second tap run reported **40 shots from 40 taps** — no gating at all — while a
14-frame trace of the same input showed `fireCd` jumping to 0.28 and counting down correctly.
Both could not be true. The 4s number was wrong: my sub-tests ran sequentially in one page and
shared state, so counts from one contaminated the next. The same run reported `pShootDisabled:
{}` once and `{venomx: 5}` the next time, which is the tell.

**Second:** on the strength of that bad number I concluded `pShoot` did not own the tap shot and
went looking for another firing path. Disabling `pShoot` outright produced zero shots — it owns it
after all.

The measurement that settled it logs the gate at each RELEASE frame:

    frame  fireCd  fired
      2     0.28     1     <- fires
      8     0.18     0     <- blocked
     14     0.08     0     <- blocked
     20     0.28     1     <- fires

One shot every 18 frames. *Measure the gate, not the outcome* — a shot count aggregates every
path that can produce a bullet, while the gate is the thing under test.

---

## ⚠ ONE SUITE FAILURE THIS PASS WAS FLAKY, NOT REAL

`the flurry races — every bolt is fast` failed once and passed on re-run with no change to that
code — the same warning 0819c already records. Re-measured directly before re-running rather than
assuming: across a full flurry over 40 frames the **minimum bolt speed is 17.19** against a
threshold of 14, and `_hspd` is seeded `17+rnd*6`, so speed cannot be the cause. Whatever the
variance is, it is in which bolts exist at the sample moment, not in how fast they travel.

**Re-run this one before chasing it.**

---

## HOW TO VERIFY

    node --check assets/game.js
    node --max-old-space-size=3072 _BUILD_SOURCE/test_fl.js     2,701 ok / 3 fail

The 3 are environmental: the preload key count and the two `_superseded/` ledger checks.

`SPECIAL_TAP_CD` is the dial for both weapons. 0.28 is a beat you can feel without the tap
becoming useless; raise it if tapping still reads as spam, lower it if the weapon feels stuck.
