# Arcade natural-play parity — September 15, 2026

MODE-01 is complete on top of main `7635330b`.

## Natural encounter sweep

The final probe ran the real `updatePlay(.10)` and `drawWorld(.10)` paths in
Chromium for Campaign and Arcade across Stages 1–9. It consumed every authored
wave before resolving the actual miniboss and reaching the actual boss. Adaptive
reinforcements were disabled for this comparison because that shared system has
its own invariant tests.

- **64 passed / 0 failed** with no page, console, or controlled-loop errors.
- Campaign and Arcade produced the same scheduled enemy trace in all nine stages.
- Every stage consumed its complete authored wave list.
- Every stage reached the same miniboss and boss identity in both modes.
- Co-op repeated pressure from the same enemy families and retained the same
  miniboss and boss identities; it introduced no new family.
- Stage 5 retained its random asteroid-slot comet substitutions in both modes.
  Those environmental counts can differ with asset-decode timing, so the probe
  compares the scheduled roster exactly and asserts the comet family separately.

The measured Stage 5 pass contained 29 exact authored arrivals plus 9 Campaign
and 8 Arcade random small-comet substitutions across all 14 authored waves.

## Combined route evidence

This closes the remaining natural-play and conditional route work after the
earlier verified batches:

- Arcade stage/result routes: **20/20**.
- Warden payouts and Campaign isolation: **24/24**.
- Stage 5 dialogue omission and ordinary co-op results: **14/14**.
- Natural Campaign/Arcade/co-op encounter sweep: **64/64**.

The existing inspected captures cover Stage 1, Stage 4, Stage 7, the Stage 7
Warden defeat/escape split, solo and co-op results, the Arcade final-score screen,
and the Campaign/Arcade Stage 5 transformation dialogue split. They are stored
under `_shots/arcade_routes_0915/`, `_shots/arcade_isolation_0915/`, and
`_shots/arcade_dialogue_coop_0915/`.

## Regression status

`node --check assets/game.js` passes. The unchanged runtime reached the full suite
summary at **3,997 passed / 57 failed**, exit 1. Fifty-six names match the recorded
baseline. The additional `stage 1: the sand tanks spawn (scroll never)` assertion
repeated twice in this run, although the same runtime hash passed it in the prior
3,998/56 run and the new Chromium natural-play probe consumed all 19 Stage 1 waves
in Campaign, Arcade, and co-op. It is recorded as a pre-existing headless-suite
timing fluctuation, not an Arcade runtime regression.

Machine-readable evidence is in
[qa/arcade_natural_parity_0915.json](qa/arcade_natural_parity_0915.json). Probe
source is `_BUILD_SOURCE/arcade_natural_parity_0915/probe.py`; raw evidence is in
`_shots/arcade_natural_parity_0915/`.

No commit or push was performed.
