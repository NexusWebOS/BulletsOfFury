# PASSOVER — drop 0807r   (LEVEL 1: A HONEST PROBE, AND THE FIRST REAL FIX)

Build: `BulletsOfFury_0807r`
Harness: **2,184 assertions / 202 sections / 0 failing**, twice, reaching the banner.

Mike will not run the game until Level 1 is fixed. This is the first pass, and it does NOT finish
that job — but it replaces guesswork with measurement, and closes the miniboss item.

---

## 1. ⚠ THE HARNESS HAS BEEN LYING ABOUT LEVEL 1

`verify_atlas_0806z.js` reports "boss reached" for stage 1. **It gets there by force-killing the
subboss and overriding boss state.** It proves every graphic resolves; it proves nothing about
whether the level plays. That is why not one of Mike's stage-1 complaints ever surfaced from a
green suite.

`_BUILD_SOURCE/play_level1.js` is new and plays it honestly: it holds fire, damages what is in
front of it, kills the miniboss by actually hurting it, and lets the scroll advance on its own.

## 2. TWO OF MY OWN PROBES MISLED ME FIRST

Recorded because both were my error, not the game's:

* **"mapScroll never advances"** — it does. The scroll is advanced in the DRAW path, and my probe
  only called `updatePlay`. An update-only probe never moves the level, so every ground wave
  looked gated out. Adding `drawWorld` showed scroll running 0 -> 2208 and the tanks spawning.
* **"4 enemies spawn in thin air"** — they do not. I checked only Y; those `intcp` spawn at
  x=-28, correctly off the left edge, and fly in. Checking both axes drops it to 2 of 25.

## 3. WHAT THE HONEST RUN ACTUALLY FOUND

    miniboss appears      t=54.9s   scroll 2197
    miniboss destroyed    t=62.5s   scroll 2209
    BOSS arrives          t=76.4s   scroll 2763
    boss destroyed        t=78.3s   scroll 2775
    final scroll 2775 of 4800 — the level never reaches its end

    waves fired                       12 of 15
    enemies popping in on screen       2 of 25
    miniboss shield STATE while sealed 19 of 19 samples correct

⚠ **The boss arrives at 58% of the level.** Mike: *"I am no longer pulling up to the dam when
fighting the helicopter boss."* That is this — the boss triggers at scroll 2763 when the dam is at
the end of a 4800 level. Not fixed here; now measured.

## 4. THE MINIBOSS AURA — FIXED

The state was right all along: `_qlArmor` and `_qlShield` were set on every sample while sealed.
**But the glow only fired for the 0.3s after a BLOCKED shot.** Unless you were hitting it at that
exact instant there was nothing to see, and approaching without firing showed a plain hull.

A shield is a STATE, not a reaction. It now draws a slow breathing aura the entire time a turret
lives, with the hit pulse still riding on top. Measured: 9 draw calls while sealed and untouched
against 1 with the shield down.

## 5. WHAT IS STILL OPEN ON LEVEL 1

    the boss triggering at 58% instead of at the dam        MEASURED, not fixed
    3 of 15 waves never firing                              MEASURED, not fixed
    2 enemies popping in on screen                          MEASURED, not fixed
    inner turrets dying while outer ones live looks wrong
    the jet flyby noise · the silent flamethrower
    the intro: runway -> liquid flyover -> centred start
    enemies reading half shmup, half high-speed action

`play_level1.js` is the tool for all of them now, and it will not let me claim a fix I have not
made.
