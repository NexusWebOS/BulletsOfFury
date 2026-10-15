# Original static pilot ships — October 10 correction

Mike rejected the generated Cole aircraft likeness and explicitly allowed
static ship images. The ending now uses the original in-game pilot sheets
for all nine pilots. No new ship generation or recoloring is involved.

The straight front image is `ship_<pilot>_so6`; the straight rear image is
`ship_<pilot>_so2`. Cole keeps his actual wings, cockpit and twin engines.
The portal exit uses the original front image. Earth descent, coastal
approach and landing use the same original rear image. The source rectangle
comes from the owning `BOFX.ships` trim within the `XART.get` canvas.
The renderer preserves the complete authored crop, proportions and palette;
it does not rotate a top-down view into a head-on shot.

These aircraft remain static. Translation, proportional scaling and the
shared camera animate the flight and touchdown. Approach and landing meet
at the same position, size and image. The parked aircraft stays fixed while
the selected pilot disembarks, walks around it and enters the animated HQ
doors. The existing portal, downwash, pilot animation, camera push, fades,
satellite infection, green code and sounds remain active.

The 432 generated aircraft cells from the previous homecoming pass are
preserved as archived candidates. They are excluded from the live ending's
dependency lists and renderer. The generated environment plates and
32-frame satellite infection remain active. Do not restore those generated
jet reels as approved aircraft likenesses.

Owners: `assets/homecoming_1010.js`, `assets/hq_landing_1010.js` and the
existing ship manifest. No atlas, source sprite or gameplay hull was edited.
Existing odd-sized source canvases stay unchanged; no new odd-sized frames
are exported. All original nine front/rear views were rendered and inspected
through native Chromium and the game's own `drawImage` context.

Use [the real-engine preview](previews/hq_landing_1010/index.html?scene=portal&pilot=cole&revision=1010e).
Verification details are in `docs/qa/static_pilot_ships_1010.json`.

All four JavaScript syntax checks passed. The required full suite completed
8,335 assertions with zero errors and exit 0. Real Chromium passed 27 native
checks, 32 camera/doorway checks and 14 preview checks, with zero page,
console or asset errors. All 18 active ship images are pixel-identical to
the original in-game views under the same nearest-neighbor draw settings.
Every pilot's approach-to-landing seam is continuous. Native screenshots
and the corrected 43.7-second engine film were inspected; its original
sound track decodes correctly. Existing gameplay/test-source hashes and
LF/CRLF line endings are unchanged. Local only; no commit or push.
