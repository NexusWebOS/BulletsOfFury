# Yuri30 — restore the established pilot identity

The Escape29 sprites drifted into a sleeveless, slick-haired character. This
correction restores Yuri's brown mohawk, close beard, red jacket sleeves and
shoulder insignia, fitted black armor and red-black boots against the approved
Yuri28 reference derived from the original Yuri motion sprite.

108 source drawings produce213 left/right runtime exports. Aiming, run, vault,
roll, crouch, prone, cover and slide poses are corrected. The original artwork
is preserved; the new manifest overrides only Escape29's Yuri entries in memory.
The enemies, backgrounds, controls and encounter logic are unchanged.

Tool: PixelLab reference outfit transfer. Exact prompts, seeds, inputs and jobs
are in art/yuri30/source/generation_requests.json. Two duplicate-prone results
were rejected and regenerated; their selected repair is recorded separately.
Export owner: _research/build_yuri30.py. Fixed192x224 cells, anchor96,160,
one0.5 proportional body scale, binary alpha, whole authored drawings, retained
per-frame roots and gun sockets. No per-frame fitting or body-part puppetry.

Validation: 15 native Chromium checks pass; no browser/missing-asset
errors. All213 corrected assets load through actual ART. In-game top-down aim,
run, roll, vault and reverse slide were captured; movement/review onion views
and full source contact sheets were inspected. Action sequences and muzzle
coordinates are unchanged. Original Escape29 assets, game.js, combat29.js and
escape29.js match their pre-correction hashes;820 retained art files also match.
This is an art correction, not a new gameplay balance or physical-controller test.

Review: art/yuri30/preview.html. Build: overdrive1015-yuri30-r1.
QA: docs/qa/overdrive_yuri30_1015.json and docs/qa/yuri30_views.
No commit or push was made.
