# Arcade life and continue rules — September 14, 2026

Arcade now starts with the stocks Mike requested and spends a finite continue
bank across the entire run. Its old Normal configuration gave four lives and
unlimited continues; Furious gave one life. The difficulty screen also displayed
stale life counts that did not match the runtime.

| Difficulty | Starting lives | Continues | Lives restored per continue |
| --- | ---: | ---: | ---: |
| Easy | 7 | 7 | 7 |
| Normal | 5 | 5 | 5 |
| Hard | 3 | 3 | 3 |
| Furious | 3 | 1 | 3 |

Restoring the selected starting stock on a continue is the implementation choice
for Mike's new life allowance. It does not reset weapons or grant a new bank.

`difficultyForRun` derives Arcade resources without changing the authored
Campaign/co-op difficulty table. Password/direct-stage routes resolve Arcade mode
before assigning the stock. Loading a campaign refreshes its difficulty while
preserving the save's remaining lives, so it cannot inherit Arcade tuning.
Difficulty descriptions use those same values, and the continue screen shows
remaining Arcade credits using the existing stage font.

Stage 9 previously capped the prompt at one continue and sent an exhausted run
through a campaign-map retreat that reset its continue counter. Arcade now uses
its remaining run-wide bank there and ends at GAME OVER when exhausted or when
the countdown expires. The direct retreat entry also cannot refund Arcade credits.
Campaign retains its existing rift behavior. Stage 9's separately authored bonus
life grant remains: starting lives are not a maximum-life cap.

## Verification

- `node --check assets/game.js`: passed. Runtime LF and suite CRLF preserved.
- Full `node _BUILD_SOURCE/test_fl.js`: **3,804 passed / 60 failed, exit 1**,
  final summary reached. All 17 new section-306 checks pass. No new failing
  assertion names against `docs/qa/stage_1_5_0914.json`; its variable sand-tank
  spawn assertion passed in this run. The existing suite is still not clean.
- Real Chromium using `shoot.py` controlled frames: **22 passed / 0 failed**,
  zero page, console or controlled-loop errors. Actual `startRun` checks all
  four difficulties. Real Enter input spends the final credit and cannot spend
  another; Stage 9 can use its fourth Normal credit without refunding the bank.
  Campaign loading and password entry are checked separately.
- Inspected actual canvas pixels for all four difficulty descriptions and the
  last/zero-credit continue prompts. The probe tracks the game's `stageText`
  calls and its own canvas `drawImage`; no fake font renderer or new art.

The native probe sets lives/credits at boundary conditions rather than playing
an entire run to exhaustion. The behavior suite separately spends every credit
in sequence. Full Arcade encounter/cutscene/map parity is still an open checklist
item; this batch verifies resources and the affected transition paths.

Sources: `_BUILD_SOURCE/arcade_rules_0914/`. Logs and screenshots:
`_shots/arcade_rules_0914/`. Machine-readable proof:
[qa/arcade_rules_0914.json](qa/arcade_rules_0914.json).

## Request tracking

[REQUEST_CHECKLIST_0914.md](REQUEST_CHECKLIST_0914.md) consolidates the conversation
into stable IDs with complete/partial/pending states and evidence. The JSON source
is editable; `_BUILD_SOURCE/update_request_checklist.py` regenerates counts.
No existing user changes were committed, pushed, integrated or discarded.
