# Campaign flags, Stage X, Fury HQ and vertical travel — October 4

Mike requested a permanent Stage X home, no added landscape labels, an actual
Fury headquarters with its name built into the building, and downward 4→5 and
upward 7→8 / 8→1 ship travel. He then approved the generated X flag and requested
I, II, III, IV, V, VI, VII, VIII and IX in the same style.

All nine campaign flags now use separately generated chrome masts, rectangular
frames, ivory Roman numerals and the original stage color families. Normal,
grayscale lock, two selected highlights, three completion-rank palettes and
white unlock silhouettes are registered together. Rank palette changes affect
the colored cloth and preserve neutral chrome, lettering, outlines and alpha.
The flags share normalized dimensions and measured mast-base anchors. The
original flag atlas remains available as a cold-load fallback.

Stage IX now has a matching flag over its authored cosmic portal region. The
existing bonus gate remains authoritative; seeing its locked flag grants no
unlock. Stage X has a permanent flag over the central city. A locked X can be
inspected without launching a fight. Completing Stage 6 still determines which
pending encounter is available. The escaped Harrier or all five Rebel ships
orbit the city; both launches retain their existing encounter controllers.
The old oversized encounter plaque no longer obscures the city.

The HQ island is regenerated with raised FURY HQ lettering physically built
into the building's frontage. The tiny old HQ overlay and all three added map
location labels are removed. The native review caught an existing HQ bobbing
error: the string `hq` produced NaN coordinates. Its animation now uses a finite
numeric phase and the actual building is visible.

The three requested legs retain their up/down headings after arrival. The
approved pilot hulls are rotated once into cached cardinal frames; complete
sprite dimensions and centered placement are preserved for all nine pilots.
The engine trail follows the selected heading, and map movement sounds fire
once per selection rather than on terrain bobbing. Direct travel still eases
between the existing stage anchors.

Runtime changes: `assets/campaign_landscape_1004e.js`, the optional flag renderer
hook in `assets/game.js`, the two legacy Stage X plaque guards, and generated
`assets/campaign_flags_art_1004f.js` loaded before the map extension. No combat,
music, progression unlock or save-format changes. Existing dirty work remains
preserved; no commit or push.

Art was produced through built-in OpenAI imagegen. Eleven unchanged originals
and exact prompts are archived under `_ART_SOURCES/campaign_landscape_1004f`.
HQ/X prompts: `prompts.json`; Roman flag prompts: `flag_generation.json` and
`flag_manifest.json`. Shipping art lives in
`assets/game/campaign_landscape_1004f`. The two owning builders perform visible
alpha bounds measurement, nearest-neighbor normalization, cloth-only palettes
and silhouette masks. No existing atlas was edited or repacked.

Validation: syntax checks pass. The full suite reaches its final summary with
7,143 assertions and exit 0. `assets/game.js` keeps LF; `test_fl.js` keeps CRLF.
Final native Chromium reports: map/navigation 37/37, flag/control 16/16,
uninterrupted orbit/HQ 5/5, live review 11/11. All report zero page/console
errors. Wide/compact overview, travel, locked/unlocked flags, both Stage X routes,
HQ close-up and shipped-art contact sheets were visually inspected.

Two initial fixture failures are preserved under `_shots/`: the route fixture
left a different selected stage before its pointer assertion; the flag fixture
prematurely enabled the bonus unlock and its genuine cinematic redirected IV
to IX. Corrected fixtures passed. These initial exits were nonzero, with zero
browser errors; the final reports above are the completion evidence.

Live review: `_shots/campaign_markers_1004f/review.html`. It runs the actual
engine, provides both X routes and an HQ close-up, and blocks campaign save
writes. Portable evidence: `docs/qa/campaign_markers_1004f.json`.
