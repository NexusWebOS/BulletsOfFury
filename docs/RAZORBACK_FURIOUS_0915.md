# Furious Razorback hyper tank — September 15, 2026

## Result

S1-06 is complete. Stage 1 on Furious now fields one distinct giant Razorback hyper tank.

- The complete authored tank, its component hardpoints, collision silhouette, held-beam geometry and Retina targets scale to exactly 150% of the Normal encounter.
- A luminance-preserving crimson palette covers the authored hull, treads and mounted weapons while retaining dark outlines and mechanical shading.
- Hyper movement advances 62% faster, turns 55% faster and runs its attack clock 30% faster than the baseline tank.
- The Furious sonic release expands from five to nine rounds, widens its fan and launches a pressure wave more than twice the baseline width and expansion speed.
- Resonance nova pressure rises to 28 individually animated sonic rounds and a larger red wave.
- Razor Rack launches fourteen larger, faster missiles through one shared Retina warning.
- Normal remains the original single tank. Hard remains the two-tank encounter completed in S1-05.

## Verification

- `node --check assets/game.js`, test/probe syntax checks, LF/CRLF preservation and the CRLF-aware diff check pass.
- Focused suite section 331: **14/14** assertions pass for difficulty isolation, exact scaling, matching hardpoints/hit geometry, faster movement and ordnance, Furious sonic/nova/rack attacks and the crimson palette.
- The complete suite reaches its final summary with the exact established **57 failure names** and no new failures.
- Real Chromium through `_BUILD_SOURCE/razorback_furious_0915/probe.py`: **17 passed / 0 failed**, with zero page, console or game-loop errors.
- Pixel-reviewed native frames confirm the giant authored silhouette, preserved mechanical detail, readable red charge, nine-round release and resonance nova. The probe records a five-second native gameplay video.

Machine-readable Chromium evidence: [qa/razorback_furious_0915.json](qa/razorback_furious_0915.json).
