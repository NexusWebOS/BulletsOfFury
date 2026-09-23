# Full-screen campaign map — 2026-09-22

The previous screen combined the native center canvas with a separate wide-map renderer. Only the native canvas applied the deployment zoom, leaving the outer islands stationary. The two renderers also updated at different rates.

Campaign selection now expands the existing canvas to the viewport aspect ratio. Ocean, islands, flags, clouds and the player share the same camera and deployment transform. The top bar, stage briefing and portrait/stat overlays remain fixed. Gameplay restores its original 480 x 512 virtual viewport on exit. The obsolete world extender is no longer loaded; its source remains available.

Pointer coordinates include the wide viewport offset. A first island click selects it; a second click deploys. Hover no longer silently preselects an island, and the same mouse click cannot fall through as keyboard Fire. Save/Load button flashes use the corrected offset. The clock hides while their dropdown is open, and the progression heading scales to fit narrower side panels.

Verification:
- JavaScript syntax checks passed for game.js and widescreen_hud_0918.js.
- Real Chromium probe: 1920 x 1080, 1280 x 720 and 1600 x 1200; full canvas bounds, outside-center island selection without accidental deployment, Save/Load opening, synchronized deployment zoom screenshots, restoration of the gameplay viewport, no page/console errors.
- Full test_fl.js suite reached its final summary, exit 1: 76 failures. All normalized failure names already occurred in the preceding blaster batch (78 failures); this is not a green suite.
- Evidence: _shots/campaign_full_0922/, _shots/campaign_full_suite_0922.log.
- Reusable probe: _BUILD_SOURCE/probe_campaign_full_0922.py. The older probe_wide_map_0919.py delegates to it because the old separate-canvas contract was removed.

No art was regenerated, and no commit or push was performed.
