# Arcade Stage 5 dialogue and co-op routes — September 15, 2026

Continuation of the Arcade route and campaign-isolation audit on top of main
`7635330b`.

## Stage 5 transformation

Arcade now omits the HQ prototype-dispatch line from the Stage 5 transformation.
The narration flag is resolved when the transformation state is created, so the
sequence does not spend time typing invisible text or wait for its hold timer.
Fast sky travel, solid clouds, part arrivals, assembly effects, sound cues, white
transition, ship reveal and countdown use the existing authored sequence.

Campaign retains the full HQ dispatch. Stage 3's thaw and Freezer lines remain in
both modes because they are live gameplay reactions rather than cutscenes and
explain the temporary weapon behavior the player is using.

## Co-op routes

Real results screens were exercised for Stages 1 through 7 with co-op active.
Each route pays both seats' completion bonuses, retains their independent scores,
lives and bombs, preserves the run-wide continue bank, and opens the next stage's
ordinary card. Stage 8 pays both seats and opens Arcade's score ending. A direct
Stage 9 clear pays both seats and follows the existing Stage 6 fallback without
opening the campaign map.

## Verification

- Native Chromium: **14 passed / 0 failed**, with zero page, console or
  controlled-loop errors.
- Campaign/Arcade Stage 5 captures use the game's own `dlgBox`, canvas and
  `drawImage` paths. The Campaign capture visibly contains the HQ dispatch; the
  Arcade capture shows the same fast cloud flight without the panel.
- The Arcade transformation progresses beyond its sky phase while narration is
  disabled. No game timing was shortened to satisfy the probe.
- All seven ordinary co-op results routes, the Stage 8 ending and direct Stage 9
  return were confirmed through real Enter input.
- Earlier regressions rerun on the reconstructed runtime: route **20/20** and
  Warden/campaign isolation **24/24**, all with no browser errors.

The first attempt to add this change exposed a large-file patching failure that
truncated unrelated sections of `assets/game.js`. Both malformed snapshots are
stored under the ignored `_shots/arcade_dialogue_coop_0915/recovery/` directory.
The shipped file was reconstructed from the exact `7635330b` Git blob using a
guarded 24-replacement script. Every source match is asserted once before writing,
and LF is checked. The final game diff is limited to the intended Arcade changes.

Final syntax and suite results are recorded in
[qa/arcade_dialogue_coop_0915.json](qa/arcade_dialogue_coop_0915.json). Probe and
reconstruction source: `_BUILD_SOURCE/arcade_dialogue_coop_0915/` and
`_BUILD_SOURCE/patch_arcade_routes_0915.cjs`. Local screenshots and logs:
`_shots/arcade_dialogue_coop_0915/`.

## Remaining work

MODE-01 remains **partial**. Natural-play parity through every full encounter and
the remaining conditional co-op/boss routes have not been claimed. Later-stage
behavior and difficulty balancing remain separate checklist entries.

Tally remains **148 requests — 79 complete / 8 partial / 61 pending**. No commit
or push was performed.
