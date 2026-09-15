# Generated control prompts — 2026-09-14

B is the logical Back action. Menu Back follows the assigned B/missile binding and controller B; Backspace only deletes password text. Keyboard assignments remain visible in Help and Options. Escape compatibility is retained without advertising a competing navigation label.

Shared rows use the existing ui_help atlas D-pad, A/B/C/Y and Start graphics. Converted the title, difficulty, mode, pilot, co-op, stage, options, password, help, credits, boot, results and continuation prompts, plus campaign prompt call sites and the outer HTML legend. Pilot launch uses Start. Options and password reserve space for the row. Password Delete no longer exits when empty, and typing no longer reserves K as a stop command. The standing rule is saved in AGENTS.md.

Validation: final syntax check passes; 25 focused behavior/atlas checks pass. The full suite completed with 3,851 passes and 57 failures (exit 1), all matching the previous baseline. It ran after the input changes; subsequent spacing and text-only changes received final syntax, focused and native checks. Two obsolete full-suite assertions were replaced with binding and actual-render behavior assertions.

Native Chromium checked the actual renderer on pilot, title, difficulty, mode, options, password, help, credits and boot. B returned from pilot; Backspace did not. This was controlled-frame menu verification, not a complete campaign playthrough. Direct campaign-hub rendering remains unverified because its existing CAMPHUB_ITEMS definition is missing; no fabricated data was supplied to conceal that error. Other checked screens produced no console errors.

Reproduce: run `python _BUILD_SOURCE/create_control_review_0914.py`, serve the repository, open `/_shots/control_hints_0914/review.html`, select a screen and press Render after lazy art loads. The fixture uses actual engine drawing and input functions. Evidence and screenshot hashes: [QA record](qa/control_hints_0914.json). Existing work remains local; nothing committed or pushed.
