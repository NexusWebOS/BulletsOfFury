# Startup layout stabilization — October 7

On a delayed cold load, the initial game frame was 480×65 at y417.5. The page's layout owner did not execute until after all runtime scripts, moving the frame to 700×846 at y27: a 390.5px upward jump. The game loop also ran while later extensions were still registering, and the six outside control hints appeared over the unfinished shell.

The existing layout/fullscreen owner now runs before the first external runtime script. The frame participates in normal layout from the start, and equal flexible credit rails prevent the font swap from nudging it horizontally. `fitCanvas` delegates to that same layout owner; obsolete load/60ms/300ms refits were removed.

The game loop starts at DOMContentLoaded, after the final classic extension script has executed. Boot/loading/attract screens keep the outside control strip hidden while all six authored icons prepare together. The complete strip appears when the interactive UI can use it. Existing boot prompts, fullscreen controls, menu input, cinematic/map viewports and game art are preserved.

Native Chromium verification: 32/32 checks, zero page/console/missing-asset errors. Cold loads deliberately delayed game.js, the last extension and the credit font. The entire playfield remained at identical coordinates from first paint through load at 1280×900,390×844 and1920×1080. Warm reloads, actual keyboard navigation, fullscreen entry/exit, resizing and the campaign viewport also passed. Screenshots inspected: `_shots/startup_layout_1007/contact.jpg`; before/after geometry and portable evidence in `docs/qa/startup_layout_1007.json`.

Full regression: 7,681 assertions passed, 0 failures, final success banner and exit0. `node --check assets/game.js` and CRLF-aware `git diff --check` passed. Local only; prior encounter/art work retained.
