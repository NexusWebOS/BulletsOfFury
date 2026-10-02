# Downloaded build — October 2, 2026

Mike requested the updated GitHub build. Fetched origin and inspected the incoming changes. The newest build was on `origin/claude/epic-clarke-rtfnuk`, at `d19c966693d8a5e73b5394f69207801725e163eb`; `origin/main` remained at `3cf07043`. Local `main` was fast-forwarded to the new build. No new commit was made and nothing was pushed.

Includes the incoming trailer workflow, Stage X duel fix, bomber hit flashes, Falva portrait repairs, Stage 7 escape, Stage 6 turn, Stage 9 backdrop/asteroid changes and consistent launch sizes/speeds. Details: `docs/FEEDBACK_1001B.md` and `docs/LAUNCH_SCALE_1001C.md`.

The four local tracked HAMA edits were backed up under `_shots/github_download_1002/local_before/`, then reapplied to the incoming versions. Both sets of script/test additions are present. All 3,349 existing untracked paths were preserved. The active HAMA song still contains only the approved hook and OH chants. `assets/game.js` remains LF and `_BUILD_SOURCE/test_fl.js` CRLF.

Verification: syntax checks pass; **6,247 assertions pass, zero errors**, full final summary reached, no new failing assertion names versus 6,203/0. **14 HAMA Chromium checks pass**, including actual audio playback, captions, pause/resume, both physical slam cues, looping and exit. Ground Stage 2 and space Stage 9 launch probes pass with no page/console errors: hull sizes stay 60px and 48px respectively, no off-scale blits, no stopped launch frames. Their countdown/play screenshots and HAMA screenshot were inspected. These are integration/launch/media checks, not full campaign playthroughs.

Portable results: `docs/qa/github_download_1002.json`. Logs, screenshots and actual HAMA gameplay recording: `_shots/github_download_1002/`.
