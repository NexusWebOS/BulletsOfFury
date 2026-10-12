# Stage 8 Phase 3 — open alien void

Mike requested a darker alien hell void with no side structures, retaining
animated parallax code/computer lights as the battle begins. Installed locally
on October 11, 2026; no commit or push in this pass.

The cathedral backdrop and foreground ribs are replaced in this encounter by
a newly generated black/crimson atmospheric plate. It covers the entire view,
with faint oily currents and buried red fissures. A second low-opacity copy
of the same authored atmosphere moves at a different depth. Six sparse emerald
code fragments use sixteen unique drawn poses and three parallax depths.
Their light rises during the first four seconds of actual combat; releases
from charged attacks add a small light pulse. The existing portal, speech,
boss forms, collision geometry, warnings, other stages and homecoming remain
under their original controllers.

## Art and ownership

- Built-in `image_gen` generated both assets. Exact prompts and the input
  reference are recorded in
  [`prompts.json`](../_ART_SOURCES/void_arena_1011/prompts.json).
- Original generated files are retained in
  [`_ART_SOURCES/void_arena_1011/returned`](../_ART_SOURCES/void_arena_1011/returned).
- Shipping artwork is in
  [`assets/game/levels/stage_08/stage/void_arena_1011`](../assets/game/levels/stage_08/stage/void_arena_1011).
  Backdrop: 1024 × 1536. Code: sixteen 320 × 320 RGBA cells, pivot 160,160.
- The code generation returned a 1254-square source instead of the requested
  1536-square sheet. The builder copies each native cell into an even 320-square
  canvas with transparent padding, preserving alpha and pixels at scale 1.
  No per-frame rescaling, interpolation, recoloring or opaque matte.
- [`build_void_arena_1011.py`](../_BUILD_SOURCE/build_void_arena_1011.py) owns
  exports, their hashes, `void_arena_art_1011.js` and the taxonomy entry together.
  Existing shared atlases and old source graphics are preserved.
- [`void_arena_1011.js`](../assets/void_arena_1011.js) replaces the existing
  arena draw callback at its established position beneath combat. It warms
  Stage 8 dependencies, advances clocks only in simulation, preserves those
  clocks across copied forms, and uses proportional cover at each camera zoom.
  Black is the loading fallback; the old walls never reappear while decoding.

## Verification

- `node --check assets/game.js` and the new runtime/review scripts passed.
- `node _BUILD_SOURCE/test_fl.js`: **8,700 passes, zero failures**, final
  `FALVA/LIZZIE BUILD OK, 0 ERRORS` summary, exit 0.
- Native Chromium arena probe: **20 passed, zero failed**, no page, console or
  missing-asset errors. Includes actual intro/monologue-to-combat transition,
  all code cells, proportionate rendering, left/right/fit camera coverage,
  pixel animation, real Pause, three parallax depths, copied-form/HP continuity,
  mobile framing and stage/escape isolation.
- Existing native finale probe: **14 passed, zero failed**, no browser errors.
  Drone/ghost behavior and the continuous second portal still pass.
- The review page passes five Chromium checks for asset loading, capture
  pause, code scrubbing/onion skin, mobile width and zero browser errors.
- Captured backgrounds have 98.8–99.6% of pixels below RGB 28. The camera-limit
  and fit captures have zero uncovered diagnostic pixels. Screenshots were
  visually inspected through the actual game renderer.
- The first arena test assumed combat began immediately after the portal;
  it was still in Dracodia's authored monologue. The fixture now waits for
  that speech to finish naturally. No intro or combat timing was shortened.

Portable evidence: [`docs/qa/void_arena_1011.json`](qa/void_arena_1011.json).
Native review and a silent animated game capture:
[`The final void`](previews/void_arena_1011/index.html).
The probes use protected bounded encounters, not a full human campaign clear.
