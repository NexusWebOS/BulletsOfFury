# Pilot-selection reveal — UI-09

The composed pilot screen now follows the engine's reveal timer. Previously the timer and sound ticks ran, but this screen drew all copy and colored segments immediately.

Names, callsigns, affiliations, biography text, special names and stat labels reveal in sequence. Bars then fill left-to-right, one row at a time, using the existing segment ticks. Full copy determines wrapping and placement, so appearing letters do not move the layout. The styled name uses one cached full plate with a reveal clip. Re-entering the screen restarts the selected pilot's reveal. The existing Enter skip completes it without confirming that same press.

## Verification

- `node --check assets/game.js`: passed.
- `node _BUILD_SOURCE/test_pilot_reveal_0914.cjs`: all nine pilots pass partial-text, monotonic segment fill, row ordering, complete-copy, skip and restart checks against the actual game VM. Reveal durations are recorded in the JSON proof.
- Full `node _BUILD_SOURCE/test_fl.js`: 3850 passing assertions / 58 failures, exit 1, final summary reached. The 58 failure names match the downloaded GitHub baseline; none are new.
- Native Chromium screenshots verify Axel's text and intermediate first-bar fill, Enter skip, the seven other unlocked cards and Cole's locked card. Lizzie and Falva retain all five stat rows inside the panel. Screenshots are under `_shots/pilot_reveal_0914/`; hashes and exact coverage are in [the QA record](qa/pilot_reveal_0914.json).

The native pass used the real game scripts and renderer in a controlled-time review page. The ordinary intro route was not completed. One review tab crashed during a synchronous 360-frame batch; the recovered pass used bounded steps and single-frame completion in low quality. Its cause was not established, and this is not a full-game stability certification. Cole's unlocked animation is VM-covered; his native screenshot verifies the lock state.

## Reproduce

Run `python _BUILD_SOURCE/create_pilot_review_0914.py`, serve the repository locally, and open `/_shots/pilot_reveal_0914/review.html`. Restart clears the reveal; quarter-second steps expose partial words and bars; Enter uses the real input tap to skip; Finish reveal jumps to the final layout for roster review. This page stays under the ignored QA folder and is not part of game navigation.

UI-09 is complete. UI-08 remains next: fill the available game screen and improve space for the biographies currently limited to six rows. ACH-09 (boss fight timer) follows. No art, atlas, gameplay balance, music, commits or pushes in this batch.
