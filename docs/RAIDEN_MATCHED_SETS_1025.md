# Matched modular roster — October 25

Mike correctly rejected mismatched pieces and colors in the component preview.
The former three-hull families shared generic six-part sets: olive equipment
appeared on sand tanks, purple aircraft, orange craft and gray fixtures. The
previous functional checks verified removability, not visual design agreement.

Every one of the 24 hulls now has its own six-part generated hardware bank:
144 matched modules. Wings follow the individual airframe silhouette; painted
engine, turret, rack and utility housings follow the owning hull's materials.
The builder offers only that vehicle's matching options. Hiding or swapping a
part never substitutes an old shared olive component. Steel, rubber, optics,
missiles and indicators keep their distinct material colors.

The seven mobile ground machines retain fully independent running gear.
Its 11 complete module types now have olive, sand and neutral gunmetal banks:
33 running-gear objects. The tan tank uses sand fittings and gray Flak uses
gunmetal fittings. All belts, wheels, sprockets, idlers and suspension remain
separate from their complete bare hulls.

Current catalog: 24 bases + 144 vehicle-specific hardware modules + 33 running
gear modules = 201 objects. Sixteen enemy, four miniboss and four boss fitouts.
The old generic files remain on disk as prior work; they are absent from current
compatibility lists, the component library and the updated ZIP.

Generation and paint corrections use built-in image_gen. All original candidates,
cleaned candidates, exact prompts and reference hull strips are retained in
_ART_SOURCES/raiden_components_1024/matching/. Rejected side-view wheel candidates
were not registered. Correct overhead wheel paint edits retain the camera.
Solid hardware exports apply a recorded alpha cutoff of 200 to the preserved
generated alpha, preserving retained RGB and removing background haze. Sources
remain untouched. No translucent effects are processed through that hardware rule.

Every component has a 512x512 master, 256x256 native and matching white-hit PNG.
One proportional normalization per hardware bank, fixed measured attachment
pivots, scalar per-slot fit scales; no width/height stretching. Aircraft engine
orientation and module sizing are recorded. Alpha/pivot changes are regenerated
with the owning builder.

Build owner: _BUILD_SOURCE/build_raiden_components_1024.py, with
_BUILD_SOURCE/match_raiden_components_1025.py registering matched sets before
manifest export. Manifest/catalog, native/master/hit images and ZIP agree.

Chromium QA: _BUILD_SOURCE/probe_raiden_components_1024.py. Final 79 passed,
0 failed, no page or console errors. All 201 objects decode; all default fits
remain unclipped; every compatible part has the correct owning set or gear
palette. All 24 default and alternate fits captured and reviewed, including
the small orange-wing vent and sand-rack tongue paint fixes. All seven vehicles
retain individual wheel removal/replacement, visible white hits and recovery,
gear-off views and unchanged bare hulls. Evidence: _shots/raiden_components_1024/.

This changes the standalone art kit and preview. Shipping game files retain
their starting hashes. No gameplay, combat, audio, commit or push changes.
