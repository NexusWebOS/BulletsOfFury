# Browser performance and Field Manual — October 12, 2026

Main game changes are local and uncommitted. Existing HUD dirty-region rendering, per-frame effect graphic lookup sharing, hidden legacy HUD skip and stage cache byte retirement fixes are retained.

Native 480×512 backing now defaults across Edge, Chrome and Firefox. The former 960×1024 backing rendered four times as many pixels. CSS playfield size, hitboxes, simulation, particle counts and authored frames remain unchanged. Add `?quality=high` to opt into supersampling. This reduces backing pixel count 75%; it is not a claim of 75% faster game FPS.

## Measured native rendering

Sequential real-browser headless smoke tests: 240 frames of movement/fire and repeated explosions each, stages 1 and 6. Main submission means: Edge 9.46/6.53ms, Chrome 9.37/5.34ms, Firefox 23.33/20.59ms. Observed display cadence: Edge 47.5/52.8, Chrome 48.5/60.0, Firefox 39.4/44.0 FPS. No page/console errors; finite player motion, positive live shots/effects, state remains playable. Samples are short and headless; hardware/browser rendering paths differ from the user's laptop. Heavy scenes still miss 60 FPS here, especially Firefox. These results do not establish sustained laptop FPS, all-stage performance or universal hardware support. No robust overall FPS speedup claim can be made from these short samples.

Prior paired Edge HUD tests establish 54–58% lower HUD submission CPU. That narrow result remains the defensible before/after timing evidence. See EDGE_PERFORMANCE_1012.md.

## Field Manual

`extensions/bof-field-manual/`: offline Manifest V3 package, 58 searchable dossiers. Nine pilots and actual shipped portrait art, current abilities/weapons/difficulties, all campaign stages and bonus routes, current encounter roster, focused Hard Corps tactics, notes/bookmarks, responsive layout and print styling. BlackOpsOne font and BOF logo shipped locally. Icon generated specifically for the manual, with 16/32/48/128 resolutions and 512px source. No host permissions or network code. Local storage preserves notes/bookmarks; no web access or tracking.

Detailed tactics exist for key encounters; other roster cards explicitly identify that detailed timings are not documented. This is a first edition, not an exhaustively measured guide for every attack. Overdrive is described as a separate ruleset, without presenting base numbers as Overdrive data.

Guide tests pass in Edge, Chrome and Firefox: search, notes persistence, bookmarks, difficulty selector, art readiness, narrow-screen overflow. Actual unpacked MV3 extension loads in Playwright Chromium; toolbar popup opens its full guide tab. Chrome/Edge manual install uses Developer Mode / Load unpacked. Not published to the Web Store. Firefox can use guide.html as a standalone page; this is not a Firefox add-on.

ZIP delivered at workspace/output/bof-field-manual/BOF-Field-Manual-1.0.zip (~1.49 MiB). Source lives in the user's GitHub coding folder; no push performed.

Final validation: complete _BUILD_SOURCE/test_fl.js suite reached FALVA/LIZZIE BUILD OK, 0 ERRORS; JavaScript syntax and whitespace checks passed. Actual desktop, narrow layout and native game screenshots inspected. Existing authored sprites/effect counts remain intact.

Revision 1.1 responds to missing graphics and incomplete ability summaries: all 18 runtime roster encounters now have authored plates or live captures; 24 enemy recognition plates; 9 ability badges; actual HUD panels; Sonic Boom wave and Heavy Turret mount. Five dual-ability loadouts are explicitly described from PC_SPECIAL and implementation controllers. The 1.1 ZIP supersedes the text-heavy 1.0. Some encounters still have general survival advice rather than measured attack-by-attack timings. Base-game code was not changed in this revision.
