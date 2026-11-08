# Furious boss performance correction — November 4

Razorwake stalled during first-use shadow compositing and collision readbacks.
The measured high-quality native RAF sample averaged30.7FPS, with533.5ms99th
percentile gaps and up to1724.2ms inside its draw. The original full-cabinet
Furious film averaged26.7 native engine FPS.

## Change

`assets/furious_encounters_1102.js` now reads precomputed exact alpha bits for
all11 collision banks and source-derived shadow pages. Six large source banks
(body/hit/flow/roll/roll-hit/exhaust) use smaller lossless pages behind their
original cells and pivots. No giant-sheet uploads, runtime shadow recoloring or
GPU pixel readbacks are needed for this encounter. Original source art remains.
All native health pools, source hit threshold >24, directional poses, animation
clocks, warning windows, attack books, impacts, audio and high-quality2x backing
remain unchanged. StageX and Normal/Hard retain their original owners.

`assets/furious_perf_art_1104.js` registers the prepared pages and mask metadata
before the encounter controller. A size-checked async loader prepares3,717,885
collision bytes during stage loading; combat waits for readiness. Existing
64MB cell cache and stage-exit cleanup remain. The small shared collision data
is retained once; the raw original large sheets are retained as rebuild sources.

## Evidence

- Same native18-second high-quality profile:58.0FPS after the complete fix,
  p99 gap33.4ms; maximum encounter draw71.2ms. The remaining occasional cold
  frame is recorded honestly; this is not a universal locked60FPS claim.
- The first shadow/mask-only pass reached54.8FPS but still had a large first-use
  roll upload, so the final pass also pages that art.
- Fresh full-health, input-only, real-RAF Razorwake film:57.7 average native FPS,
  versus26.7 before. The fresh Thunderhead film improves48.0→57.2FPS. Native defeat, source stability and full audio/video decode
  pass with no game, browser, asset or audio-tap errors.
- All1,035 opaque source cells verify exhaustively offline.15,525 native point
  queries across every pose agree. All1,152 repacked graphic cells retain exact
  alpha and visible source RGB. Eight native shadow comparisons preserve exact
  silhouette alpha; premultiplied colour differs at most one8-bit step.
-29/29 existing native Furious encounter ownership/HP/socket/pixel/defeat and
  Normal/Hard/StageX/RoughRiders/Sumpjaw route checks pass.

The fresh films and updated preview page retain the labelled invulnerable Cole
input bot. No enemy HP/phase/attack-timer writes occur after recording spawn.
The regular Stage7 Sumpjaw controller was not modified.

## Reproduction

Run `_BUILD_SOURCE/build_furious_perf_1104.py` after the original Furious art
builder. It owns the66 pages, compact masks, original source hashes and exact
pixel checks. `_BUILD_SOURCE/furious_perf_1104/` contains the native profiler,
mask/shadow and encounter probes; `before_controller.js` is the diagnostic-only
baseline. Use `profile.py --baseline --label before` versus
`profile.py --label after` in separate browsers. Detailed receipts are in
`docs/qa/furious_perf_1104/`; raw profiles/captures stay under ignored `_shots/`.

Core game.js is untouched. Syntax checks pass. The required full suite exits1
before its summary on the existing `difficultyHealthBaseline15 is not defined`
VM setup error at combat_polish_0927b.js:151. No globals are stubbed. The updated
preview passes11/11 real-browser playback, seek, audio and mobile checks.
No commit/push is performed in this correction pass.
