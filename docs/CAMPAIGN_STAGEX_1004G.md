# Floating Stage X island — October 4

Stage X was rendered as a coastal city on the connected campaign landscape,
so its small bob did not read as a floating island. The city now sits on a
separately generated deep, tapering rock base, elevated above the fixed terrain
anchor with a ground shadow, gentle bobbing and additional hover lift.

The city, chrome X flag, pointer bounds and Harrier/five-Rebel orbit center
share one live pose. The whole island opens its briefing. An earned encounter
still uses the existing controller; viewing locked Stage X cannot unlock or
launch a fight. Focus framing keeps the complete island between the menu and
progression panels. The locked briefing now holds focus so its letters are
not reset by the underlying selected-stage briefing every frame.

Art was edited through the built-in OpenAI imagegen tool using the existing
city as the edit target. Original source, exact final prompt and source hash:
`_ART_SOURCES/campaign_stagex_1004g/`. The final prompt is in `prompt.json`.
Shipping art: `assets/game/campaign_stagex_1004g/region_hub.png`, with grayscale,
shadow and highlight variants. Builder: `_BUILD_SOURCE/build_campaign_stagex_1004g.py`.
Normalization preserves generated alpha and uses nearest-neighbor containment;
variants derive from authored pixels. The earlier coastal city remains stored.

Runtime: `assets/campaign_landscape_1004e.js` and the Stage X hit test in
`assets/campaign_focus_1004b.js`. No music, combat balance, unlock conditions or
save-format changes. Existing local work preserved; no commit or push.

Review: `_shots/campaign_stagex_1004g/review.html` opens directly on the island.
Native proof covers actual game-context draw calls, permanent elevation,
ground shadow, live bob, hover/click, locked typing, menu clearance, whole
Harrier/Rebel hulls, both real confirm launches and compact framing. Screenshots
were inspected after adjusting the camera to expose the entire skyline.
The final verification record is `docs/qa/campaign_stagex_1004g.json`.
Final validation: 7,146 full-suite assertions, exit 0 and final BUILD OK banner;
19/19 native/review checks, with zero page or console errors.
