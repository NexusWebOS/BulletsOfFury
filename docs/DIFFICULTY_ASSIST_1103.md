# Normal/Hard difficulty assist (November 3)

Mike approved building the fire budget and hazard tuning from the wave pressure audit
(docs/WAVE_AUDIT_1103.md, report `docs/previews/wave_audit_1103/index.html`).

New last-loaded layer `assets/difficulty_assist_1103.js` (DA13). `window.DA13_OFF=1` disables it.
It is active only on **Normal and Hard**, and only during **regular waves**: never while a boss or
miniboss is active. Furious, Insanity and Easy are untouched. No game.js edits.

| | Normal | Hard |
|---|---|---|
| Fire budget: live enemy rounds on screen | 25 | 45 |
| Fire budget: aimed rounds per second (rolling 2 s) | 1.5 | 2.5 |
| Longest hold before a round fires anyway | 0.6 s | 0.6 s |
| Aimed round speed cap | 260 px/s | 360 px/s |
| Pattern round speed cap | 330 px/s | 420 px/s |
| Stage 2 firewall fall time (native 1.25 s) | 1.7 s | 1.45 s |
| Stage 2 firewall catch box (native 0.34 of sprite) | 0.24 | 0.30 |
| Stage 2 fire debris launched | every 2nd dropped | every 4th dropped |
| Stage 2 debris hit radius (of native) | 65% | 80% |
| Stage 8 beam/flamethrower dodge time after the lane locks | +0.30 s | +0.15 s |
| Budget halved after a respawn | 8 s | none |

## How it works

- **Fire budget.** `eShoot` and `eShootT` are wrapped outermost.
  - The gate is decided once per frame, so all rounds spawned in that frame travel as one group.
  - When the gate is closed, the frame's new rounds are spliced out of `eBullets` (in place; the
    array identity never changes) and held. Each group is released whole, when the budget allows
    or after 0.6 s.
  - The caller still holds the same object, so tags it assigns after the call land as usual. Rings
    and fans come back intact. No round is deleted.
  - When a boss or miniboss arrives, everything held is released at once.
- **Speed split.** Each enemy round is classified once (aimed if it is born pointing within 8° of the
  pilot). Every frame, rounds over their cap have `vx/vy` scaled down, along with `spd`, `_maxspd` and
  `speed` when present, because homing and accelerating updaters rebuild velocity from those fields.
  This also reaches stage guns that bypass `DIFF.ebSpeed` (Stage 6).
- **Firewall.** The wave's `y` and `t` are pulled back each frame to the slower fall.
  `playerHit` calls whose stack comes from `wfxUpdate` are refused outside the narrower box. The
  arrival alarm stays off (Mike, 0801ad).
- **Fire debris.** `debrisLaunch` marks the dropped chunks dead at launch. `playerHit` calls from
  `debrisTick` are refused outside the reduced radius. Each live chunk shows its next 0.4 s of path as
  pixel dots (`drawEffects`).
- **Stage 8 beams.** Lanes lock at half the warning (`A.t >= A.warm*.5`). Extending the warning at the
  start would delay the lock and let the beam aim *better*. So the native lock time is kept, and the
  bonus is added to `A.warm` the moment `A.committed` turns true (`s811Tick` wrapper).

## Natural-pacing re-measure (supersedes the numbers below where they differ)

The earlier on/off runs used the paced observer (see docs/WAVE_AUDIT_1103.md, Correction). Natural
pacing, novice lives/min while waves run, DA13 on vs off: Normal (Stages 1-5) summed 5.05 vs 7.53 (-33%);
Hard (Stages 1-9) 16.4 vs 20.5 (-20%). Stages 1, 2, 5, 8, 9 improve clearly. Hard Stages 4, 6 and 7 came
out slightly higher with DA13 on: single runs of 1-7 hits, inside the noise, reported as measured.


## Measured (novice pilot, lives lost per minute; DA13 on vs off, today's code)

| Stage | Normal on | Normal off | Hard on | Hard off |
|---|---|---|---|---|
| 1 | 0.15 | 0.00 | 0.15 | 0.15 |
| 2, bot sees hazards | **1.76** | 3.31 | | |
| 2, hazard-blind bot | **2.98** | 3.91 | **3.58** | 5.22 |
| 4 | 0.31 | 0.25 | 0.71 | 0.67 |
| 6 | 0.71 | 0.65 | 0.53 | 0.83 |
| 7 | **0.50** | 1.03 | 0.96 | 1.10 |
| 8 (repeats averaged) | 0.97 | 0.96 | 1.36 | 1.13 |

- Stage 2 firewall deaths fell from 12 to 3 in the hazard-aware Normal runs.
- Stage 7 on Furious, where DA13 is inactive, measured 1.06/min as a control.
- The bots cannot see beams, so the Stage 8 dodge-window change shows no effect on them by design;
  it gives a human player time to move off a visible lane.
- Single runs vary about ±40%. Only Stage 2 (both tiers) and Stage 7 Normal are clear wins; the rest
  are within noise.

Re-measure with `_BUILD_SOURCE/sweep_after_1103.sh` (DA13 on) and `sweep_base_1103.sh` (DA13 off):
`_shots/waves_1103/{after,base,after_see,base_see,s8on_*,s8off_*}`.

## Verification

`python _BUILD_SOURCE/probe_difficulty_assist_1103.py` (add `hazards` for the Stage 2/8 part only).
Result: **15/15**, plus the 4/4 hazard-only run. It checks:

- Furious: DA13 is inert.
- Normal/Hard Stage 7: rounds are held, `held == released + queued`, no wait over 0.62 s, and zero
  speed-cap violations among live rounds.
- A boss fight: DA13 stands down and holds nothing.
- Stage 2: debris is thinned and the firewall falls at the slower pace.
- Stage 8: beam dodge windows are extended.
- Zero page errors.

## Not done (from the audit, still open)

- Stage 9's regular waves are the quietest in the game.
- Stage 4 fires less on Furious than on Hard, and Stage 9 less on Furious than on Normal.
- Readability caps (explosion flash size, at most two warning lanes at once).
- Dead-air pacing on Stages 1 and 6.

These change content or Furious and belong to the stage owners. Another session was working on waves
the same day (`galaga_flight_1103.js`, `wave_followup_1103`).
