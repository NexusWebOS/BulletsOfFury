# PASSOVER — drop 0807c   (EXPLOSION PATTERNS, MEASURED OFF THE RECORDING)

Build: `BulletsOfFury_0807c`
Harness: **2,095 assertions / 191 sections / 0 failing**, twice, reaching the banner.

---

## 1. I CANNOT HEAR AUDIO — SO I MEASURED IT INSTEAD

Mike mouthed the explosions into `explosion_types.mp3`: *"Every time you hear me mocking the
sound of an explosion going off, thats how many times you should be setting off an explosive
frame animation all over the unit and around it. certain ones can be big blasts as I have these
longer holding type of sounds."*

I have no way to listen to a file. But what he encoded is **count, spacing and duration**, and
all three are in the envelope. Decoded to 22kHz mono, short-time RMS at 10ms hops, onset
detection with hysteresis so a burst is not split by a micro-dip, then each burst classified by
zero-crossing rate and spectral flatness to separate broadband mouth-noises from speech.

35 bursts over 34 seconds, clustering into 11 utterances, seven of them demonstrations:

    2.8s    5 hits   ~135ms held, 129ms apart      fast chain
   13.1s    1 hit     299ms
   14.3s    1 hit     259ms
   15.5s    9 hits   ~256ms held, 127ms apart      with an 878ms HOLD partway through
   20.1s    1 hit     907ms
   24.3s    5 hits   ~351ms held, 104ms apart      slow, heavy
   28.5s    1 hit    1586ms — loudest in the file  THE big blast
   32.1s    1 hit    1027ms

⚠ **Two were ambiguous and I asked rather than guessed.** The 28.5s one is low-frequency and
un-hissy, so the classifier called it speech — but it is the loudest and longest thing in the
recording. And the 7.4s burst sat inside a stretch I read as talking. Mike confirmed both are
blasts. Had I guessed, I would have built a 1.6-second explosion out of a sentence.

## 2. THOSE NUMBERS ARE THE TABLE, VERBATIM

    turret / crate / drone   1 hit                              ~280ms
    jet / mboat              5 hits, 129ms apart                 135ms each
    tank / boat              5 hits, 104ms apart                 351ms each
    miniboss / boss          9 hits, 127ms apart                 256ms each,
                             with an 878ms HOLD landing on hit 4

Not "roughly a chain of five" — the measured spacing. Verified in the engine: jet fires 5 across
517ms, tank 5 across 417ms, miniboss 9 across 1017ms, and every queued blast fires with none
stranded.

Offsets run out to 0.62 of the unit radius and grow with each hit, so a chain covers the hull
and then spills past it — *"all over the unit and around it"*.

## 3. THE HOLD IS NOW A REAL THING

`explode()` computed duration purely from size, so a big blast was only ever a WIDER one — it
could not linger. It takes an optional hold now, and the measured value rides through the chain.
A miniboss death runs nine explosions whose holds span 0.256s to 0.878s. Every existing caller
omits the argument and keeps its old duration exactly.

## 4. ⚠ I SCALED THE WRONG NUMBER FIRST, AND NINE ASSERTIONS CAUGHT IT

For *"dont be afraid to scale up the size of the explosions used on enemies by 25-50%"* my first
cut multiplied the per-class `unit` size. **Nine assertions failed, correctly.**

That number is only the NOMINAL size. What the player sees is governed by `COVER_TARGET`, which
divides out each explosion sprite's transparent padding via `EXPLODE_FILL` so every class lands
on identical visible coverage — the property the 0801cw work exists to maintain. Scaling
per-class desynchronises them, which is exactly what the assertions measured.

Moved to where visible size is actually decided:

    fodder            1.38 -> 1.79   (+30%)
    bosses and minis  1.62 -> 2.19   (+35%)

One place, every class together, coverage still uniform. Same lesson this codebase keeps
teaching: **find the thing that owns the behaviour before changing it.**

## 5. AND THE CHAINS ARE TICK-DRIVEN, NOT setTimeout

The two follow-up blasts this replaces ran on `setTimeout(55*t)` — a wall clock the game does not
control. A 9-hit chain running 1.4s would still have been detonating after the stage cleared,
through a pause, into the next screen. They run off the frame delta now and are cleared with
everything else on a stage change. Asserted.

## 6. STILL OPEN

* Flame / ice breath fade-on-release · miniboss slow · stats-screen alignment ·
  helix contact burst POSITION.
* The **ice-level freeze** retest, and a browser look at the 78 packed sheets.
* `UNUSED_ART_CANDIDATES.txt` — 868 families awaiting your confirmation.
