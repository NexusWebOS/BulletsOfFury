# Campaign briefing and Lizzie — October 3, 2026

Mike requested Theater Progression above the mission text box, regenerated blank text boxes, centered game-font lettering revealed one character at a time, and a stable Lizzie portrait with its complete right border.

## Delivered

- Theater Progression is now part of the game canvas, centered immediately above the mission panel at every viewport width. The map camera reserves room for both, and the old upper-left duplicate is removed. Ranks, elemental marks, unknown markers, and the current-stage highlight remain.
- Built-in image generation produced a blank gunmetal/olive mission frame with a navy interior. Stages 1–8 retain their authored briefing copy and use full current `STAGES` titles. Stage 9 and Stage X use the same blank plate. Command Alloy titles and Command Signal body copy reveal at 43 characters per second; wrapping and centering use complete lines, so partial words never push earlier letters sideways. Selecting another stage or rival, or reopening the map, resets the reveal. Letters wait for the plate and fonts to decode.
- The old Lizzie sheet was cut into equal quarters despite its irregular/shared borders. Her new complete golden bezel stays fixed. Original character art is rendered inside it, and talking changes only a small mouth region. Menu and communication directions share fixed 256×256 geometry; the surrounding face, body, and border remain pixel-identical throughout the talking loop. All existing Lizzie expression keys and side-panel portraits use the corrected rendering. Original source files are preserved.
- Narrow campaign screens keep the correct canvas aspect and hide the unrelated global control legend; the existing authored D-pad/A/Start prompt remains below the briefing.

## Ownership and art

- Runtime: `assets/map_briefing_1003g.js`; small integrations in `assets/game.js`, `assets/widescreen_hud_0918.js`, `assets/rival_fight_0924.js`, and `index.html`.
- Generated source and exact prompts: `_ART_SOURCES/map_briefing_1003g/generation.json`, `briefing_blank.png`, and `lizzie_frame.png`.
- Deployed unchanged images and measured source rectangles: `assets/game/map_briefing_1003g/manifest.json` and its two PNGs.
- Owner: `_BUILD_SOURCE/build_map_briefing_1003g.py`. No shared production atlas was repacked or hand-edited. The original Lizzie expression sheet supplies her character pixels.

## Verification

- JavaScript syntax checks passed for the game and affected runtime modules.
- Full `node _BUILD_SOURCE/test_fl.js`: **6,952 passing assertions**, final `FALVA/LIZZIE BUILD OK, 0 ERRORS` banner, **exit 0**. No change to its CRLF file. The game retains LF.
- `_BUILD_SOURCE/probe_map_briefing_1003g.py`: **25 native Chromium checks**, no page or console errors. Covers progressive reveal, stable centering, all nine stage briefs, real arrow selection, Stage X, both Lizzie portrait directions, pilot-menu routing, and narrow layout/aspect. Pixel comparison confirms that the frame and body do not change across mouth poses.
- Original `_BUILD_SOURCE/probe_campaign_0930.py`: all eight island clicks, keyboard navigation, fixed horizontal ships, locked western frontier, and Stage 9 portal pass, exit 0, no page/console errors.
- One initial fast-click regression run failed while the full suite and video recording were also running. Native pointer-coordinate inspection passed; the original unmodified probe then passed in isolation. This was a timing-sensitive verification run; no unrelated input changes were made.
- `_BUILD_SOURCE/record_map_briefing_1003g.py` records actual game selection and the shared dialogue renderer, with an enlarged current Lizzie portrait for review. No browser errors. Final stills use live animation callbacks so side HUD state is current.
- Portable evidence: `docs/qa/map_briefing_1003g.json`. Ignored captures, videos, logs, and review: `_shots/map_briefing_1003g/review.html`. Rebuild the page with `_BUILD_SOURCE/review_map_briefing_1003g.py`; verify it with `_BUILD_SOURCE/capture_map_review_1003g.py`.

Local only. Prior dirty and untracked work is preserved. Nothing committed or pushed.
