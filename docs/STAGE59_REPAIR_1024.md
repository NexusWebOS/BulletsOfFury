# Stage 5 and Stage 9 repair — October 24

Stage5's space miniboss could retain a destroyed core at the front of the space collision list. A laser intersected that dead target, its damage was refused, and the surviving right turret received nothing. The reproduced last-turret fixture recorded `hit: bomber-core`, with right-turret HP unchanged. This was the space bomber, not the similarly named Earth bomber covered by the prior pass.

`stage59_repair_1024.js` returns only live bomber Retina pieces, puts surviving modules before the broad core, and excludes dead objects from space collision candidates. It does not reduce health or grant a clear. Normal/Hard/Furious probes use native travelling space lasers and held-beam routing, exhaust the actual final pool and reach native defeat/rewards. Actual authored Retina pixels are verified over the remaining right turret after native acquisition. Dead targets stop being advertised.

Stage9's refitted fleet retained legacy full-canvas `_drawW/_drawH` metadata, even after the new hull was painted. Shield growth and death-pattern size both read that metadata. The repair records the refit's actual proportional hull span and supplies it to the native death owner. Bubble shells are bounded to144 world pixels, kept close to their owners, and remain transparent enough to read the ship. Energy, deploy, hit and break clocks retain their owners. Repeated ordinary space impacts use a small bounded spark and merge nearby decoration; shadow blasts and the native burning-spin/crash/shock-ring/death sequence remain.

The Stage9 miniboss uses the larger black Event Horizon from entry onward. Its new eye-registered acting includes restrained drift, a whole-body spin and a source-preserving lens charge. The previous borrowed off-wing Warden attack book is replaced with four committed eye-origin turns: aimed fan, orbiting fan, flight/strafe sweep and a spinning ring with a deliberate gap. All emitted rounds and native muzzle flashes originate at the same eye. Existing PixelLab water needle/orb effects supply the projectile art. Native approved electric/orb gun cues use the shared mixer and retrigger gates, with silent volley partners. HP, part damage, native death and reward ownership remain.

The last Stage5 portal retains its actual aircraft capture and gate entry, then fills the entire game area, including side HUDs, with an opaque PixelLab water-speed tunnel. A protected three-second travel beat precedes the existing white/map handoff. The overlay is pointer-transparent, uses one proportional cover scale, and hides on handoff or state exit. It does not silently unlock or launch Stage9.

## Art and ownership

The owning builder is `_BUILD_SOURCE/build_stage59_1024.py`. It writes the atlas sheets,95 registered cells, manifest, taxonomy and output hashes together:60 visible cells plus35 white-hit partners, seven lossless WebP sheets,914680bytes. Black acting uses fixed320x320 cells with common transparent padding, one source scale and an eye pivot at160,160. Warp cells are256x256 and fully opaque. Eye positions are measured from the actual cyan lens; frames translate around that physical pivot without per-frame silhouette fitting.

Sources, game-exported black identity references, PixelLab receipts, original frames and export decisions remain in `_ART_SOURCES/stage59_1024/`. Rejected: the first mechanical-looking warp, external rings/gray blobs in the initial eye charge, and drift frames that invented colored sparks. The accepted charge keeps the original armor and uses generated lens pixels only. The accepted water vortex has foam, bubbles and streaming wave ribs. All installed frames/contact sheets were inspected.

PixelLab displayed balance3.47USD to3.16USD:0.31USD plus two bonus generations used. No top-up or active jobs remain.

## Verification and limits

- Focused native combat probe:13 passed, zero failures across Normal/Hard/Furious.
- Native pixel/Retina/shield/hit-expiry probe:5 passed, zero failures.
- All60 animation cells, decoded audio, silent partners, full-screen warp and native map handoff:6 passed, zero failures. Real media playing events and nonzero analyser samples verify both eye cue routes.
- No page/console errors in the final probes. Some static-server teardown logs report aborted requests after the test browser closes; those are separate from the captured game errors.
- Required game/runtime/registry syntax checks pass. The required full `_BUILD_SOURCE/test_fl.js` exits1 before any assertions because the downloaded GitHub build is missing `retired_art_archive_1022.cjs`. This is the same pre-change blocker recorded when the build was downloaded; no BUILD OK or full-suite pass is claimed.

Early fixtures exposed cold-load debug respawning and the debug-only portal return route; final visual fixtures mark the spawned fight and the portal proof uses its non-debug route. The first art probe caught a missing native `nca_` atlas prefix; the builder now registers the correct sheet keys, and the final pixel checks use the new frames rather than fallback art.

Review controls: `docs/previews/stage59_repair_1024/index.html`, with full Stage5 miniboss, last-right-turret reproduction, Stage9 fleet, black miniboss and water warp. GOD is enabled only in that clearly labeled review page. Reports: `docs/qa/stage59_repair_1024.json`. Full captures/logs stay under ignored `_shots/stage59_1024/`.

Changes remain local; this request did not ask for a commit or push. Human play is still the test of whether the revised Stage9 patterns feel fair; the native probes establish functioning attacks, readable source geometry and intact progression.
