# October 1 — Dialogue, animated map wall, elemental critical feedback

Local changes based on `db406eca`. No commit or push in this pass.

## Behavior

- Dialogue portraits have a stable left bay, centered vertically and horizontally within that bay, with an inset clear of the frame. They retain their aspect ratio. Layout reserves their space while lazy art decodes. Full text determines wrapping while the typewriter reveals letters, and enlarged cinematic boxes lift above A/Start prompts.
- The locked East Coast data wall uses a newly generated eight-frame RGBA sheet at 6 fps. Binary rows and bright scan packets change while the wall's destination stays fixed. Original v6 art remains archived. Source, exact built-in image-generation prompt, import procedure and runtime paths: `../_ART_SOURCES/campaign_1001/generation.md`.
- Ice against Fire flashes the struck silhouette blue (`#83d9ff`); Fire against Ice flashes red (`#ff3b30`). Matching authored bitmap text reads `+50% DMG CRIT`, with a dark outline. Damage applies on every hit; the text is throttled to once per target per 0.45 seconds and lasts 0.85 seconds.
- Opposing-element damage is consistently 1.5×, including the Furnace shield, minibosses and modular Stage 3 parts. This replaces the older 2× Furnace/Furious Stage 3 exceptions. Freezer's existing pre-scaled attacks are not multiplied twice. Neutral hits remain white; existing same-element resistance and Stage 8 boss immunity are preserved.

## Verification

- `node --check assets/game.js` and all changed runtime JavaScript: passed.
- `node _BUILD_SOURCE/test_fl.js`: exit 0, final `FALVA/LIZZIE BUILD OK, 0 ERRORS` banner, **6,129 passing assertions**. Recorded incoming baseline: 6,121 passes, zero failing names. Eight new feedback assertions; prior expectations updated for the requested 50% bonus and colored hit flashes. No failing names in either run.
- `_BUILD_SOURCE/probe_feedback_1001.py`: real Chromium, 606 authored dialogue lines across nine pilots at each of three viewport sizes (1,818 measurements), with no portrait/text overflow. Screenshots inspected. Eight distinct wall frame hashes and source rectangles; identical destination rectangle. Native map video recorded and decoded frames inspected.
- Registered Magma Skimmer and Ice Interceptor hits: 20 base damage removed 30 HP, with the matching colored flash and label. Modular Rime Bastion gun hit removed 30 from its own pool and visibly tinted its authored plates red.
- `_BUILD_SOURCE/probe_feedback_shields_1001.py`: native Furnace arms phase shield and current Magma Ward hull each lost 30 from a 20-damage ice hit, with one blue critical label. The current miniboss does not use the old fire-barrier field; the probe tests its actual hull.
- Existing `_BUILD_SOURCE/probe_cinema_0930.py`: **33 passing browser checks**, including A reveal/advance, Start skip, route continuations, all nine pilot upgrade scenes and review controls. Run through `_shots/run_existing_cinema_1001.py` to isolate physical controller input and keep older evidence.
- Zero page or console errors in the successful browser runs. Initial probe mistakes (stale XART-key attribution, retired enemy IDs and an assumed miniboss barrier) were corrected before accepting evidence. An actual white-text tint issue found in pixels was fixed with a flat color mask of the authored font.

Evidence and review: `_shots/feedback_1001/review.html`, `report.json`, `shields.json`, `cinema_regression/results.json`, `data_wall.webm`. Suite log: `_shots/feedback_1001_suite.log`.

These are focused rendering, input and damage checks, not full campaign clears or a new difficulty-balance certification. `assets/game.js` remains LF and `_BUILD_SOURCE/test_fl.js` remains CRLF. Existing unrelated untracked projects and earlier authored work were preserved.
