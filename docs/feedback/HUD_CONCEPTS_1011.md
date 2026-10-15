# Armored Command selected and installed

Mike selected **Armored Command** on October 11. The live implementation is
`assets/armored_command_1011.js`, using the approved generated plate registered
by `build_armored_command_1011.py`. Stocks are above the playfield; the larger
lower HUD keeps weapon, special, maneuvers, speed, shield and lock. No radar.
Both co-op seats read their own stocks. The current review is
`docs/previews/playthrough_1011/index.html`; native verification is recorded in
`docs/qa/playthrough_1011.json`.

The original concept-only pass is retained below for provenance.

Mike: lives and missiles remain hard to see during play. Requested arcade text
and icons directly below the score, a larger existing-style lower HUD with bars
and text retained, no radar, and five generated concepts to review first.

Review: `docs/previews/hud_concepts_1011/index.html`.
Generated source plates and exact prompts: `_ART_SOURCES/hud_concepts_1011/`.

1. Fury Classic
2. Bold Cabinet
3. White Interceptor
4. Armored Command
5. Neon Fury

All have prominent stocks below the score, actual native icons and Command
Alloy letters, a larger/wider lower cockpit, and no radar. Current lower HUD's
weapon, Roll, Somersault, special/status meter, Speed, Shield and retina lock
remain represented. Upper and lower frames sit outside the actual playfield.
The original preview includes Stage1 and the busy Stage6 Rebel fight, normal/low/empty stock
examples, magnification, comparison gallery and PNG export. Prefer2 for stock
hierarchy or1 for continuity with the current cockpit; Mike owns the choice.

Concepts only: shipping HUD, radar, state and index.html were not edited by
this pass. No Git changes were committed or pushed. Live binding, pilot-specific
stock icons, multiplayer layout and performance verification follow selection.
The five frames are generated raster art, not CSS placeholder sprites. Original
plates remain unchanged; measured even crops and uniform banner scaling preserve
proportions. Full source prompts and SHA256 are registered alongside the review.

Verification: real Chromium through the existing shoot.py server; all five
concepts, controls and readable stock states inspected in screenshots. Fifteen
preview checks pass with zero page, console or asset errors. The game regression
suite was not rerun because this pass changes no game code or shipping data.
Scratch captures and logs remain under ignored `_shots/hud_concepts_1011/`.
