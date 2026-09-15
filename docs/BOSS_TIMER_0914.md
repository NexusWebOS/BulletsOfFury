# Boss/miniboss combat timer — ACH-09

The upper-right playfield shows the encounter time as 00:00, below the health bars. Boss and miniboss clocks are independent; simultaneous encounters use separate rows. The existing generated bitmap dialogue face renders the text.

Time starts after initial entry (and mechanical assembly), advances in active gameplay after the pause gate, continues through later transformations and player respawns, and freezes on unit death. Counting respawn time prevents a death from improving a speed result. New units start fresh, so stage/retry replacement cannot inherit an earlier clock. Pause and menu time is excluded. Defeated units retain their seconds for future achievement work; no achievements or persistent awards are implemented here. Display saturates at 99:59 while stored seconds remain precise.

Validation: syntax passed; 12 focused checks cover entry, minute rollover, pause, menus, transformation, inactive state, invalid delta, player death, defeat, replacement and assembly. Full suite completed with 3851 passes, 57 known failures (exit 1), no new names. Native Chromium inspected the actual stage-one boss/HUD at 01:00, pause and defeat retention; no console errors in final review. This is controlled-render proof, not a full natural nine-stage playthrough.

Reproduce with `node _BUILD_SOURCE/test_boss_timer_0914.cjs` and `python _BUILD_SOURCE/create_boss_timer_review_0914.py`; serve the repo and open `/_shots/boss_timer_0914/review.html`. [QA record](qa/boss_timer_0914.json). Nothing committed or pushed.
