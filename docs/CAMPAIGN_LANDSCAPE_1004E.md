# Connected campaign landscape — October 4

Mike approved the new island scheme and requested broad landscapes underneath
the stage regions, rather than nine disconnected floating areas. The campaign
now has a connected eight-biome continent with coastal bays, rivers, roads,
bridges and offshore islets. Larger stage landmarks sit over their matching
landscapes and lift on pointer hover or selection; the continent stays anchored.

The central city retains Stage X and the surviving Harrier/Rebel encounter.
Fury HQ has its own coastal complex and original HQ icon. Stage 9 sits offshore
to the northeast, with a generated asteroid reef, stars and a cyan/violet portal.
Its existing Stage 5 gate-run unlock and exclusive bonus navigation remain intact.
Stages 1–8 retain their original flags, completion ranks and locks. The original
animated blue ocean, authored cloud art, pilot ship, typed briefing, Theater
Progression and portrait UI remain in use.

Arrival zooms from a distant overview into the complete theater. Selecting a new
stage brings its region closer. Start focuses the existing menu bar and restores
the world overview. Horizontal navigation favors travel along the requested axis
so the large southern regions remain reachable. The retired western data-barrier
hit strip is outside this campaign's new local geography; no expansion levels or
unlocks were added.

Runtime: `assets/campaign_landscape_1004e.js`, loaded after the Rebel arsenal.
Two marker-scale limits in `assets/game.js` preserve original flag/portal screen
size at the new distant overview. No combat or music changes. Existing Stage X
flight and Stage 5/9 portal cinematics use the shared new landmark positions and
camera framing.

Four built-in imagegen requests supplied the authored north and south regions,
city/HQ/cosmic/islet kit, and connected terrain. Unchanged source files and SHA-256
hashes live in `_ART_SOURCES/campaign_landscape_1004e`. Mechanical sheet separation,
nearest-neighbor normalization and derived lock/shadow/glow masks are owned by
`_BUILD_SOURCE/build_campaign_landscape_1004e.py`. Fresh `map4e_` registrations are
documented in `assets/data/ART_TAXONOMY.json`; no atlas repack or procedural terrain.

Validation: `node --check assets/game.js` and extension syntax checks pass. The
full suite reaches its final summary with 7,130 passing assertions, exit 0.
Native Chromium has 23 checks covering the uninterrupted animation loop, authored
drawImage keys, all eight stages through real D-pad input, hover lift, pointer
selection, locked regions, earned bonus portal, Stage X city and a fresh compact
viewport boot. Final page/console errors: zero. Live review controls also passed
12 checks. Wide/compact screenshots and selected regions were inspected.

The first held-click probe was corrected to render a frame between button-down
and button-up. A navigation iteration also revealed an incorrect hook name in
Chromium, which was corrected to `sselMoveHorizontal`. The final native run is
required evidence; syntax and VM assertions alone did not catch that browser
failure. `_shots/campaign_landscape_1004e_initial_nav_failure.log` preserves it.

Review: `_shots/campaign_landscape_1004e/review.html`. Practice changes are isolated
from campaign save writes. Portable evidence:
`docs/qa/campaign_landscape_1004e.json`. This pass verifies campaign map behavior,
not a human completion of all stages. Local only; no commit or push.
