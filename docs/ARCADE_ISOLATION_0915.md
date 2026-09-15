# Arcade Warden exit and campaign isolation — September 15, 2026

Continuation of [the Arcade route pass](ARCADE_ROUTES_0915.md), on top of
`main` commit `7635330b` and the existing local changes.

## Fixed

Stage 7's Warden previously sent Arcade directly to Stage 8 after the story
escape. That bypassed the results handler and its completion bonuses. Arcade now
keeps the authored last-stand frames, screams, limb explosions and final blast,
then opens Stage 7 results. Confirming pays the completion bonus to each active
seat and advances to the ordinary Stage 8 card. Repeated defeat/finish callbacks
cannot pay the kill score twice.

Arcade's Warden defeat holds for 0.65 seconds before the shared explosion beats,
then finishes 3.72 seconds into that sequence. It omits story dialogue, portal
opening, forced player flight and the campaign whiteout. The player remains
visible at their existing position. Campaign keeps its original longer sequence,
dialogue, portal flight, map unlock and suspended session.

Entering Stage 9 in Arcade no longer spends `campaign.bonusUnlocked`. Campaign
entry still spends its own unlock. Debug fights no longer clear the campaign's
pending Stage 8 arrival. Existing Arcade save guards were exercised as well:
pause saving, suspension and title return preserve the campaign session and save
slots.

## Verification

- Native Chromium: **24 passed / 0 failed**, with zero page, console or controlled
  loop errors. Real lethal-hit routing enters the Warden defeat; controlled frames
  drive the actual update/render paths; real Enter input confirms results.
- Solo and co-op both reach results, award the appropriate completion bonuses,
  retain lives/ammunition/continues and leave the campaign's unlocks, session and
  save values unchanged. Campaign retains its separate escape/map behavior.
- All nine main-boss spawns were compared between Campaign and Arcade at each of
  Easy, Normal, Hard and Furious: names, hull identifiers, max HP and special boss
  selections match. This does not claim complete attack-pattern equivalence.
- Earlier Arcade route probe rerun: **20 passed / 0 failed** on this runtime.
- Inspected actual canvas pixels: Arcade Warden defeat, fully revealed solo and
  co-op results, and the retained campaign portal/dialogue scene.
- The obsolete unconditional bonus-unlock source assertion is replaced with
  real `beginStage(9)` calls in an isolated VM for each mode. No child process is
  required by this regression test.

Syntax passes. Full suite: **3,851 passed / 57 known failures, exit 1**. The final summary was reached with no new failing assertion names against the preceding Arcade pass. Details are in
[qa/arcade_isolation_0915.json](qa/arcade_isolation_0915.json).
Source: `_BUILD_SOURCE/arcade_isolation_0915/probe.py` and
`_BUILD_SOURCE/test_arcade_isolation_0915.cjs`. Local logs and screenshots:
`_shots/arcade_isolation_0915/`. Runtime LF and suite CRLF are preserved.

## Remaining work

MODE-01 remains **partial**. Remaining work includes pilot-specific dialogue
outside the shared story system (for example the Stage 5 transformation and
Freezer's Stage 3 exchanges), natural-play encounter comparison and the remaining
co-op routes. This batch uses forced encounter boundaries rather than a complete
campaign playthrough. Later-stage balance and new encounter designs retain their
separate checklist entries.

Tally: **148 requests — 79 complete / 8 partial / 61 pending**. All earlier work
is preserved. No commit or push was performed.
