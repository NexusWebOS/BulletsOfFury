# Campaign controls and persistent save slots — October 4

The map's Stage X handler was reading controls before the Save/Load/Exit bar.
Horizontal navigation also relied on screen coordinates, leaving a dead end
after Stage VIII. The prior map review discarded storage writes while the save
function reported success without verifying them.

The campaign now has a reversible mission ring: Left from I reaches VIII, VII,
VI and the remaining missions. Locked missions and Stage IX's earned gate
remain authoritative. The ship points downward from III to IV. Up from VI
selects the floating Stage X island; Down from X returns to VI. Both pending
encounters retain their introductions and launch behavior. The ship actually
travels between VI and X, with its trail behind the correct heading.

Start opens the existing top menu. Left/Right selects Save Game, Load Game or
Exit Game; Start or A confirms. A on the map deploys. Up cannot escape an open
slot picker, and B returns to the menu. Exit requires the explicit Exit choice.
Slots use Up/Down to select and Left/Right to change pages. Twenty-four manual
slots remain available, plus the actual autosave entry in Load Game.

Manual saves verify the exact stored bytes before reporting success. Failed
writes leave the selected slot open and display an error. Map saves now retain
the selected stage, Stage IX access and optional Stage X focus, in addition to
the existing campaign progress, pilot, difficulty, score and equipment data.
The save format remains version 1. Loading restores the selected mission and
earned Stage X route. The campaign hub uses the same cartridge art and keeps
its save receipt through the confirmation flash.

The new review persists demo saves under a separate localStorage namespace,
`bof_map_review_1004h_`. Its authored demo progression cannot overwrite live
campaign slots. Use the ordinary index page for actual campaign saves; the
review includes a direct link to it. Refresh older map review tabs to replace
their previously loaded no-op storage adapter.

The blank chrome cartridge was generated with the built-in imagegen tool using
`assets/game/campaign_map_v2/btn_save.png` as a material/style reference. The
exact generation prompt is archived in
`_ART_SOURCES/campaign_controls_1004h/prompt.json`, alongside the untouched
source PNG. `_BUILD_SOURCE/build_campaign_controls_1004h.py` owns the shipping
normalization and red/white/blue variants. Palette changes affect saturated red
accents and preserve neutral metal, outlines, dark screen and alpha. The game
supplies the original font, saved pilot ship and live text; no lettering is
baked into the generated panel. Seven shipping PNGs and their manifest are in
`assets/game/campaign_controls_1004h/`, with an ART_TAXONOMY role registration.
No atlas repack was needed.

Implementation is in `assets/campaign_controls_1004h.js`, small storage edits
in `assets/game.js`, and the existing map ship controller in
`assets/campaign_landscape_1004e.js`. The extension loads after the landscape
layer. Existing staged, unstaged and untracked work was preserved; no commit or
push was made.

Validation includes both Node syntax checks and the complete test_fl suite,
which reaches its final BUILD OK summary with 7,160 assertions and exit 0.
The native Chromium map/storage probe passes 81 checks; the supplementary
pointer, normalized controller-input, autosave and campaign-hub probe passes
17. Both report zero page/console errors. Screenshots were inspected for the
real renderer's wide and compact slot layouts, pointer selection and hub
heading/receipt spacing. XART assets were checked through the game context's
own drawImage path. Save/reload/load exercises cover slots 3 and 24, Stage IX,
Stage X, blocked writes and empty slots.

Early probe fixtures selected hidden `#hud` instead of `#screen`, and used
`pad_b12/13` instead of the input system's normalized `pad_up/down`. Those
fixtures were corrected before the completed native passes. The initial
supplementary fixture report is retained under `_shots/`. Controller checks
inject the game's normalized input events; they are not a physical gamepad
hardware test. This pass verifies campaign navigation and persistence, not a
complete combat playthrough.

Review: `_shots/campaign_controls_1004h/review.html`.
Portable evidence: `docs/qa/campaign_controls_1004h.json`.
