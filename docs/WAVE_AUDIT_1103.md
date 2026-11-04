# Wave pressure audit: Normal, Hard and Furious (November 3)

Mike: *"inspect the waves of the game, do an analysis, how I could improve things as this is currently on
furious, and how to make it optimized for hard and normal so we don't overwhelm the underskilled players.
Also suggest better firing patterns or animations."*

Report: `docs/previews/wave_audit_1103/index.html`, published as a private artifact. This was analysis
only. No game file changed. Another session was working on the waves concurrently (`wave_followup_1103`).

## Correction (natural pacing re-run)

The first measurements were wrong in several places. `wave_observe_1102.js` defines `WO16.start`/`input`
twice: further down the file they are replaced by a **paced inspection mode** (one wave at a time, the
next held until the last is cleared, `t=Infinity`, adaptive off). The difficulty substitution also never
reached the stage build in that mode. Results now come from the observer's original functions
(`wo16Start`, `wo16Input`, top-level consts), which keep the native schedule, with the difficulty set
before the stage is built. Data: `_shots/waves_1103/nat_off/` (DA13 off), `nat_on/` (DA13 on),
`report_data_nat.json`. Analysis: `analyse_waves_nat_1103.py`. Older `sweep/`, `after/`, `base/` runs are
paced and invalid for absolute numbers.

**Withdrawn:** 40-66% quiet seconds; Stage 9 is quiet; reversed difficulty scaling on Stages 4 and 9;
Stage 6 rounds at 276 px/s on every tier; Normal numbers for Stages 6-9 (Easy/Normal end at Stage 5).

**Natural results, novice lives/min while waves run (N 1-5 / H / F):**
S1 0.68/1.76/2.35, S2 4.46/5.7/3.0, S3 0/0/0, S4 0.69/0.98/3.39, S5 1.7/0.81/1.79, S6 -/1.08/1.73,
S6R -/1.31/-, S7 -/1.77/3.74, S8 -/5.6/4.29, S9 -/1.5/4.11. Skilled on Furious:
0, 5.6, 0, 2.71, 0.97, 1.44, 1.91, 0.17, 4.16, 1.78.
- Fire scales with difficulty everywhere (S1 2.3/3.4/7.5 rounds/s; waves 23/30/36). No reversed scaling.
- Pacing is tight: 1-28% quiet, gaps <=9 s, except Stage 6 (about 44% quiet, a 56-62 s gap). That gap is the
  team-argument cutscene (fb2Talk, feedback_claude_1003.js), which freezes combat and since
  feedback_1003h.js cannot be skipped. Carrier assaults hold the clock only ~10-13 s each
  (`_BUILD_SOURCE/diag_s6_hold_1103.py` logs every hold flag per second).
- Killers: S2 firewalls/debris (+ s2needle on Hard), S5 s5rammer contact (all Normal deaths), S4/S6 lane
  dash (`game.js:38310`) on Furious, S7 mg, S8 s8needle + alien beams, S9 s9needle.
- Open: Stage 6 story scene has no skip/advance; units below the screen still count toward the dispatch cap; the dead
  `DIFF.density` dial; Stage 5 rammer tells on Normal.


## Method

- `_BUILD_SOURCE/measure_waves_1103.py` drives the real engine at 60 Hz through today's observer fixture
  (`wave_followup_1103/wave_observe_1102.js`, WO16), run as a copy with the chosen difficulty substituted.
  Ambient, onslaught and adaptive reinforcements stay on; bosses and minibosses are suppressed.
- `_BUILD_SOURCE/wave_telemetry_1103.js` (WT) replaces the observer's pilot with a dodge bot:
  - novice: 250 ms decisions, sees 150 px, plans 0.25 s;
  - skilled: 85 ms decisions, sees everything, plans 0.5 s.

  Both fly level-3 weapons, invulnerable, and every `playerHit` call is counted (1.2 s apart = one
  life). Each second WT logs rounds on screen, rounds fired, speed, aimed share, enemies, safe space
  and nearby rounds. Hit causes name the calling function.
- `_BUILD_SOURCE/sweep_waves_1103.sh` runs one process per case with a timeout. `analyse_waves_1103.py`
  writes `_shots/waves_1103/analysis.json`.
- Coverage:
  - novice: 10 stage routes × 3 difficulties;
  - skilled: Furious on every stage, Normal on some;
  - four repeat runs, two Stage 2 hazard-aware runs and three attribution runs.

## Headline results (novice, lives lost per minute, N / H / F)

| Stage | 1 | 2 | 3 | 4 | 5 | 6 | 6R | 7 | 8 | 9 |
|---|---|---|---|---|---|---|---|---|---|---|
| Normal | 0 | 5.07 | 0.19 | 0.13 | 0.77 | 1.49 | 0.91 | 1.78 | 1.45 | 0.60 |
| Hard | 0.45 | 6.03 | 0.17 | 1.38 | 0 | 1.38 | 2.12 | 2.74 | 2.46 | 0.49 |
| Furious | 0.45 | 6.09 | 0.44 | 0.66 | 0.56 | 1.42 | 0.99 | 4.26 | 1.56 | 0.30 |

- **Stage 2:** every Normal hit is a firewall (`wfxUpdate`) or fire debris (`debrisTick`). With the
  hazards made visible to the bots, skilled-Furious drops 34 → 2 and novice-Normal is still 2.8/min.
- **Stage 7:** fires 6.2 / 8.2 / 12.1 rounds/s, at least 3× any other stage. Most of its hits are `mg`
  rounds.
- **Difficulty dials:** they don't reach every gun. Stage 6 rounds measure 276 px/s on all tiers.
  Stage 9 fires less on Furious than on Normal; Stage 4 fires less on Furious than on Hard (both runs).
- **Dead air:** 40–66% of seconds are quiet on most stages; Stage 6 runs 12–14 minutes.
- **Safe space:** the 5th-percentile safe share of the lower screen is 0.67–0.96. Deaths come from speed
  (up to 670 px/s on Furious), aim and hazards, not density.
- **Run-to-run variance:** about ±40%. Only large gaps are treated as findings.

## Traps

- The terrain scroll (`mapScroll`) advances inside the background draw. A harness that never calls
  `drawWorld` stalls ground-anchored waves on terrain retries (1 of 23 waves fired). Call
  `drawWorld(3/60)` every 3 steps.
- The stage asset loader needs real time; wait for `stageLoadReady` before stepping.
- WO16 is declared with `const`, so test `typeof WO16`, not `globalThis.WO16`.
- Some runs went silent at near-zero browser CPU. A dedicated hunter with a CDP pause watchdog didn't
  reproduce it in three Stage 6 Hard passes, so per-case timeouts guard the sweep. No game freeze is
  proven.
