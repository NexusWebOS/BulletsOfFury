# Pilot fullscreen presentation — 2026-09-14

UI-08 is implemented and desktop-verified, but remains partial for portrait/live-resize visual verification.

Pilot select now owns the browser viewport, with a proportional backing buffer instead of stretching the gameplay canvas. The card, portrait bay, ship bay and nine-pilot roster adapt to the available width. Existing art, typed text, stat fills and generated D-pad/Start/B controls remain. Pointer coordinates use the pilot surface dimensions. Leaving pilot select restores the original gameplay buffer and page framing.

Desktop Chromium proof covers Axel, Lizzie's five-stat card and B returning to mode selection at 1280x720. All art keeps its proportions. The isolated review fixture uses actual index/scripts, controlled frame buttons and the real input action. A mouse selection also triggered the existing launch slide, but pointer navigation has not received a complete interaction matrix.

Portrait/live resize is not certified: resizing to 390x844 reports correct bounds and nonblack backing pixels, but Chromium capture stays black even after rendering. Fresh default-size tabs recover. The cause has not been established; do not describe mobile behavior as verified. Browser viewport overrides were reset. The unfinished item stays at the front of the queue.

Syntax passes; existing pilot reveal checks 9/0 and control checks 25/0. Full regression suite reached its summary: 3851 passing assertions, 57 known failures, exit 1, no new failure names against control_hints_0914.json. An initial run exposed a missing classList in the VM host; viewport setup now guards that optional DOM interface and the complete rerun finished. No test assertions or authored assets were changed for this item.

Reproduce with `python _BUILD_SOURCE/create_pilot_fullscreen_review_0914.py`, serve the repository, then open `/_shots/pilot_fullscreen_0914/review.html`. Render after lazy assets load. [QA and screenshot hashes](qa/pilot_fullscreen_0914.json). Nothing committed or pushed.

## Follow-up: responsive verification complete

The same actual game in a fixed browser iframe renders at 390x844 and resizes live to 1100x620 and back. Both orientations and Lizzie's five-stat layout were inspected. No game-code workaround was needed for the earlier viewport-tool capture issue. One unlocated MutationObserver error was reported by the outer review session; it did not recur as a game draw error, and its source was not established. The initial capture limitation above is historical. UI-08 is complete for viewport filling and resize; this does not claim a full mobile gameplay audit.
