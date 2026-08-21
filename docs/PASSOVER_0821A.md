# 0821a — THE STAGE-1 SWAP, AND THREE BUGS THAT WERE ALREADY THERE

Mike's six-item list, plus the CF_CoastlineDam stage-1 replacement.

| # | item | state |
|---|------|-------|
| — | CF_CoastlineDam-Lvl1 installed as stage 1 | **DONE** |
| 1 | stage 4/6 backgrounds + clouds | **MIKE + GPT** — not mine |
| 2 | "enemies too chaotic with projectiles" | **FIRST PASS, MEASURED** |
| 3 | stage 5 enemies disappearing behind satellites | **FIXED** |
| 4 | stage 4 boss = NCA_56 blue airship, not the tank | **ALREADY CORRECT — verified in pixels** |
| 5 | Maverick helix ball (4 parts) | **ALL FOUR DONE** |
| 6 | Falva cannot attack while the ball bounces | **FIXED** |

---

## THE STAGE-1 PLATE

Authored **natively at 680** — the width the game standardised on — so unlike stages 4/5/6
nothing was resized. 680x4212, shipping both states, which drop straight onto the `damBroken`
swap that already existed. Water is carried AS ALPHA, which is what lets the animated bed show
through and what `_buildLandMask` reads.

Verified in the browser, not from filenames: both plates decode at 680x4212, the cfg reports
4212, the bottom 800 reads WATER and the mid-plate reads LAND, with the centre column staying
water past 3412 — the river mouth, exactly as authored.

### ⚠ 3412 came from the pack, not from my eye

The runtime map declares `full_scroll_height 4212` / `open_water_height 800`, so terrain begins
exactly 3412 from the top. No coastline was measured by hand.

---

## THREE THINGS THAT WERE ALREADY BROKEN, FOUND BY SWAPPING THE PLATE

### 1. ⚠ THE STAGE-1 LAND MASK HAD NOT EXISTED FOR A LONG TIME

`drawBG` tries `drawLevelMaster` FIRST and **returns on success**. Stage 1 has carried a
`master:` since 0811h. The mask build lived inside `drawStageMap`, below that return — so it was
**dead code**, `_landMasks` stayed empty, and `_isLand` fell through to its "no mask yet -> don't
block spawns" default. **Every point on stage 1 counted as land.** Tanks and boats were being
placed with no water awareness whatsoever.

0811h's reasoning was right and is preserved — the plate is its own mask, so the two cannot
disagree. It just needed to run somewhere that executes. `ensureS1LandMasks()` reads the keys out
of the stage cfg rather than naming the plates twice, so it follows the master by construction.

### 2. ⚠ THE COASTLINE WAS WRITTEN OUT THREE TIMES AND I ONLY FOUND TWO

`grep _COAST` finds the naval swap and the wave gate. It does **not** find the third one, an
inline `4605-60` inside the naval tick. Against a 4212 plate that test is true on frame one, so
**every naval unit beached at sea, drifted down the screen and died without firing**.

The suite caught it as `every volley fired is 5-8 rounds (1)` — and note that "(1)" was itself
misleading: with an empty `rounds` array the test's own grouping yields `[[undefined]]`. It
meant ZERO.

One owner now: `const S1_COAST`. A future plate swap changes that line and nothing else.

### 3. ⚠ MASTER_W IS 800 AND FOUR STAGES ARE NOT

1/4/5/6 all ship 680-wide plates. The pre-decode fallback answered 800 and then SNAPPED to 680
once the art landed — reintroducing, from the other direction, the exact fault 0801bb fixed: the
engine believing a wrong world width while it places the player and the camera. The cfg declares
`plateW` now.

---

## 5. THE HELIX BALL — FOUR ASKS, FOUR CAUSES

Mike: remove the centre laser; it shouldn't explode until contact; on break the lasers go out in
volleys in multiple directions; the flash fills the screen.

- **The centre laser was `_ballOff:1`.** It suppressed the ball art so a full charge drew as a
  travelling LANCE and only became a ball at the stop. 0806k had already decided he launches a
  ball; the flag enforcing the old behaviour outlived the decision.
- **Two detonators owned one ball.** The contact path (0806m) was correct. But the `glow` phase
  ALSO burst on `_hT>=HELIX_TELL` — 0.34s after crossing mid-screen, by which point the ball has
  eased to 0.42 speed and barely moved. It detonated in empty air near the middle of the screen
  every time, and the timer always won. The glow is a look now, not a fuse.
- **One upward fan became three rings.** The mover hardwired vertical travel; it advances along
  `_hdir` with the sine PERPENDICULAR, which is the same arithmetic line-for-line at the default
  heading. The 24-way art needed no help — `drawBullets` already picks its sprite from the tangent.
- **The flash was 480 wide in a 680 world.** Same class of miss as the stage-6 weather not
  covering the top. It paints the world and the whole view now, at the blinding hold.

Measured in the browser: ball art from launch, no line, burst on contact at 0.52s, **three waves
of 8 bolts** at frames 0/7/15, wave one covering a full ring, flash at 1.31.

---

## 6. FALVA — AND A MEASUREMENT THAT LIED TO ME FIRST

`pShoot()` carried `if(run.pilot==='falva' && rollers.length>0) return;`. Drop 0724cf meant
"exclusive **while equipped**" — but it keyed on a ball being ALIVE. A full ball carries `life:10`
against a 15s special, so any ball thrown in her last ten seconds outlives the special, and every
one of those seconds left her gun silent with no way to get it back.

⚠ **My first probe said she could fire, and it was wrong.** It wrapped `pShoot` and counted
CALLS — but the gate is INSIDE `pShoot`, so every call returned having emitted nothing. Counting
bullets instead of calls is what found it. *A call is not a shot*, in the same family as 0819c's
*a frame count is not a clock*.

Bounded by `specialActive` now. Verified by KIND: during the special with a ball alive she emits
17 `flaser` (her helper balls, which are supposed to fire) and **zero** `mg` — 0724cf intact.
After it expires with the ball still bouncing, 40 `mg`.

---

## 3. STAGE 5 — AND MY OWN CHANGE MADE IT WORSE

The near deck was three pieces of orbital HARDWARE at 0.80 scale sweeping OVER the fight, and
0819g raised `L5_FIELD_ALPHA` to 0.92 to answer "the transparency of the satelittes is too much"
— which made that occluder near-solid. **Both reports were the same object.** Solid is right for
background hardware and fatal for a foreground one. Satellites are big opaque silhouettes, so
they can never pass over the play field; the deck keeps its scale and drift and reads its depth
from behind.

---

## 2. THE PROJECTILE CHAOS, MEASURED

Rounds per unit per second, over 40s of real play, **before** touching anything:

    stage 1 (the stage he is happy with)   0.69 - 2.52
    eye 12.93   octo 9.30   s1jetDeltaB 7.73   mdrone 7.32   l6x_tf 7.25   talon 6.87

The cause is one line, and its own comment says so: `0.16` was chosen when stage 7 "read as
empty" because its units were off-camera in an 800-wide world. Density has since gone to 1.00 and
the on-screen cap up with it, so the metronome that was feeding an empty screen is now feeding a
full one. **Nothing about it was wrong when it was written.**

Fixed with the rhythm Mike already approved for the naval guns — a burst, then a FIXED silence
you can learn. Shapes are untouched: fan/rake/pincer and the `alt` cycling are what make a volley
learnable (0811s), and they were never the problem. Overrides live in the `ENEMY_VOLLEY` row so
this stays a table.

| stage | peak before -> after | mean before -> after |
|-------|----------------------|----------------------|
| 2 | 128 -> **67** | 60.5 -> **32.1** |
| 3 | 129 -> **83** | 36.8 -> **27.0** |
| 4 | 70 -> **50**  | 26.4 -> **22.6** |
| 5 | 137 -> **74** | 49.7 -> **29.1** |
| 6 | 120 -> **96** | 51.6 -> **38.0** |

`eye` 12.93 -> 4.42, `octo` 9.30 -> 4.94, `talon` 6.87 -> 4.79. Stage 1 is untouched at 2.09.

⚠ **THIS IS A FIRST PASS, NOT THE WHOLE JOB.** Everything now sits in a 2-5 band instead of
0.7-12.9, but stage 6 is still the heaviest and its load is spread across many types rather than
one offender. That part is genuinely "one by one" and wants Mike watching it.

---

## 4. THE STAGE-4 BOSS WAS ALREADY RIGHT

Rendered all nine `_master` cells on nca_56 rather than trusting the names. `mbs6` — STORM
SOVEREIGN, already fielded by stage 4 — is the blue winged airship with the four turbine pods.
`mbm4` is the grey tank. If he meant the other blue hull, `mbc6` (CYCLONE ESCORT, a flight-deck
carrier) is the one-word change.

---

## ASSERTIONS REPOINTED (nine, all pinning a line rather than a rule)

Seven pinned stage 1's OLD plate by name, width (800) or height (4800). The rules kept: stage 1
flies a wide master with a breached twin that differs from it, and the world is exactly as wide as
the plate it declares.

⚠ **`stage-1 declares its plate height (4800)` was made STRONGER, not just repointed.** It could
never have caught the failure that actually matters — a cfg height that DISAGREES with the art.
It reads the installed PNG's IHDR now and compares, so the two cannot drift whatever plate stage 1
flies.

⚠ **`WITH the ball equipped she fires nothing else` was pinning Mike's bug in place.** It pushed a
roller with NO special running and called that "equipped" — a state the game cannot reach, since
`rollers.push` lives only in `falvaCharge`. Both halves are pinned now, including that a leftover
ball must NOT disarm her.

⚠ **`the flurry races` measured `b.vy`**, which is only the bolt's speed while every bolt flies
straight up. It measures the speed now.

---

## HOW TO VERIFY

    node --check assets/game.js
    node --max-old-space-size=3072 _BUILD_SOURCE/test_fl.js     2,701 ok / 3 fail
    python _BUILD_SOURCE/shoot.py --state PLAY --stage 1 --seconds 8 --fps 2

**The 3 failures are environmental**: the preload key count and two `_superseded/` ledger checks.
That folder lives on the primary machine and is never committed, so they cannot pass here.

⚠ `--max-old-space-size=3072` is not optional — without it the suite can die with
`FATAL ERROR: Zone Allocation failed`, which presents as a stall rather than an error.

---

## STILL OPEN

- **the projectile pass, per enemy** — see above. Stage 6 first.
- stage 4/6 backgrounds and clouds — Mike + GPT.
- cinematic zoom; pickup scaling (still fixed 34/30/40px).
- Lizzie's residual LATERAL thruster offset (0819c).
- `laser` fire mode is still fielded only by stage 3.
