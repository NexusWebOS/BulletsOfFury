# Front-facing hammer poses and truthful hit feedback — 2026-11-09

Dracodia's hammer copy now uses 32 new full-body poses across overhead and left/right follow-ups. His face, chest and both shoulders stay toward the player. The purple double-ended spiked cylinder is preserved. Five materials share identical alpha masks: regular, chromium, rage, white hit and red hit. Editable Aseprite banks, raw generated sheets, prompts and normalization inputs are in `_ART_SOURCES/boss_hammer_frontal_1109c`.

Chronos's repeat white flash came from a native target array containing the owning boss. The generic hit monitor counted that object as a child and overwrote the same health snapshot twice, creating a false decrease every tick. It now excludes the owning boss and counts aliased child objects once. Actual damage and native hit flashes remain enabled; flashes still expire normally.

Both bosses retain complete chromium overhead and horizontal hammer banks. One initial jump/landing, then planted attacks: Normal one down; Hard two down; Furious two down plus left and right. Attack routing, actual native hit masks, damage, recovery, death and rewards are preserved. No core `assets/game.js` edit.

Validation: 38 native combo checks passed, with zero browser exceptions and zero planted-root drift. Five hit-feedback checks passed, including self/alias exclusion, no-hit appearance, real hit flash, expiry and health-loss feedback. 229 undamaged native paint samples contained zero white flashes. New source exports: 32 poses × five materials with matching alpha, uncut canvas bounds and registered soles. Four regular/chromium GIFs and two MP4s are focused live-engine Furious attack checkpoints, not full fights.

Evidence: `_shots/boss_hammer_frontal_1109c`, `docs/qa/boss_hammer_frontal_1109c.json`. Full regression still stops on the pre-existing `difficultyHealthBaseline15` ReferenceError at `assets/combat_polish_0927b.js:151`, reached from `_BUILD_SOURCE/test_fl.js:4537`; it did not reach the suite summary. Syntax checks passed for the core game, hit monitor, art metadata and attack runtime.
