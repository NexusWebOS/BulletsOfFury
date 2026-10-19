#Stage7–8 roster follow-up: stored-boss veterans and delayed native attack gates
were subsequently updated and verified in `docs/LEGACY_LEGION_1018.md`. Those
196 native checks include six wave observations, not a repeat of the complete
campaign clears below.

 Full game playtest — 18 October 2026

Stage6 repair follow-up: the reactor hatch pixels, live combat captions, fan
effects and missing carrier-to-Nightwing sequence were subsequently repaired
and verified in `docs/STAGE6_REPAIR_1018.md`. The completion results below describe
the earlier build; stage-clear assertions did not establish those visual and
follow-up-encounter requirements.

All **30 planned invulnerable-bot runs completed**: Levels 1–9 on Normal, Hard and Furious, with both Stage 6 paths on every difficulty. Six additional complete Stage 6 runs passed after the fix below. No remaining progression blocker, page error, console/draw error or missing-asset response was recorded in these runs.

## Fixed during the pass

**Stage 6's pursuit prompt still paused flight.** Cole's radio dialogue allowed movement, but holding movement at “Choose Your Pursuit” left both the ship and effect clock frozen until confirmation. The older route handler in `furious_review_0927.js` returned before its flight update; the later live-radio wrapper did not bypass that return.

`stage6_radio_1017.js` now polls the original pursuit input once, temporarily removes that pause condition while an unconfirmed choice is open, and restores the prompt flag after the native update. New enemy arrivals, scheduled waves and stage time remain held. The menu retains its native input and presentation. One loader cache tag changed to `live-choice-1018`.

The natural-sequence focused probe passed **14 checks**. Holding movement changed the ship's X by 396.3px during radio and -366.7px at the prompt; prompt effect time advanced 2.00s. Stage time, wave index and spawn clock stayed fixed; no new enemies spawned. The prompt stayed open until the real keyboard A/fire action confirmed the selected route. Both complete routes then passed again on all three difficulties.

## Coverage

| Level / route | Normal | Hard | Furious |
|---|---|---|---|
| 1 | Passed | Passed | Passed |
| 2 | Passed | Passed | Passed |
| 3 | Passed | Passed | Passed |
| 4 | Passed | Passed | Passed |
| 5 | Passed | Passed | Passed |
| 6 — Harrier | Passed | Passed | Passed |
| 6 — Rebel Fury | Passed | Passed | Passed |
| 7 → 8 portal | Passed | Passed | Passed |
| 8 | Passed | Passed | Passed |
| 9 | Passed | Passed | Passed |

Stage 7 enters Stage 8 directly through its native portal. Those three runs observed the natural handoff and continued through Stage 8's ending. Each difficulty also received a separate Level 8 entry. Level 9 completed its Void Horizon miniboss, twin sentinels, fusion and Tidal Sovereign fight.

The Stage 6 rechecks observed the cargo-fortress miniboss and the selected Harrier or Rebel Fury encounter through stage clear. An additional full Normal Harrier run supplied combat, departure/flyover, destroyed-module and open-reactor screenshots after the first run's image allowance was consumed by its miniboss.

Representative full-window images were inspected for wave combat, minibosses, boss phases, portal transitions, Hammer's ending, the Stage 6 modules/reactor, Stage 8 transformations and Stage 9 fusion. Native art keys actually blitted through the game's own `drawImage` were logged. The screenshot browser keeps the regular field of view and both HUD sides; it does not crop encounters into small rectangles.

## Method and limits

- Native Edge/Chromium, actual game initialization and loop, Cole in single player, fresh temporary browser saves for each entry.
- Bot invulnerability exists only in these browser sessions: a test-only `playerHit` guard prevents deaths without pinning the ship's blinking invulnerability timer. The ship remains visible.
- Native starting equipment, pickups, weapon selection and finite missile stock. Movement, firing, rolls, somersaults and manual missiles use the existing input/action paths. No enemy HP, phase, wave clock, spawn or kill is forced.
- Native frames are stepped at 60 simulated updates per second in accelerated batches, yielding for lazy asset loading. This verifies functionality and rendering, not real-time frame rate, input latency or audio mixing. The browser was muted.
- These are isolated level entries, with the natural Stage 7-to-8 continuation noted above; they are not an uninterrupted unassisted campaign. God mode cannot establish human difficulty balance, and this pass does not cover every pilot/weapon combination.

## Verification and preservation

`node --check assets/game.js` and `node --check assets/stage6_radio_1017.js` passed. The full suite reached `FALVA/LIZZIE BUILD OK, 0 ERRORS`: **8,755 passed, 0 failed, exit 0**. Its current count includes the existing pixel-shield reel checks; the previously recorded 8,754 total was historical.

The pass changed only the live-choice adapter and its cache tag in gameplay files. `assets/game.js` and `_BUILD_SOURCE/test_fl.js` retained their starting hashes and line endings. Existing shield work, staged/unstaged changes and untracked files were preserved. Test drivers and raw output stay under ignored `_shots/playtest_full_1018/`. Nothing was committed or pushed.

The original 30 runs remain in the raw reports; the six post-fix Stage 6 rechecks establish the final behavior of the changed scene.

## Evidence

- [Full-view screenshot browser](../_shots/playtest_full_1018/review.html).
- [Machine-readable results](qa/playtest_full_1018.json), including all cases, modes, actual starting gear, native handoffs, projectile counts and the focused check.
- Raw logs/reports, the invulnerable input driver and before/after pursuit screenshots: `_shots/playtest_full_1018/`.
