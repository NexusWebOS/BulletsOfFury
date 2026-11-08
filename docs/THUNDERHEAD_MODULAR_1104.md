# Thunderhead — regenerated modular wind-cannon kit

November4: Mike requested giant wind beams from the two cannon outlets during
an accelerating reactor charge, a1015 aura over the entire unit, and a complete
regeneration including the hull, reactor and turrets.

The live Furious Stage6 Thunderhead is now assembled from a new empty hull,
separate reactor, four instantiated gun turrets and two independent cyclone
cannon pods. The old Thunderhead plate is retained as a historical source; it
is superseded in the native renderer by `TM115` after `THS114`.

## Charge and wind beams

- The two living cyclone cannons show native green/yellow/red lane warnings for1.7s.
- Both emit giant animated wind beams from their actual turbine-mouth sockets while the central reactor is still charging. Six authored startup frames precede the16frame flowing loop; six recovery frames dissipate the beam.
- Contact begins after the0.25s startup. Each beam uses an84px-wide danger lane below its mouth; the central escape corridor was tested through the native player-hit owner. Rolls/shields/GOD retain their native handling.
- Each surviving cannon owns its own beam. Breaking one cancels its damage immediately and completes its finite recovery; its partner keeps firing. Death/retry/stage exit clear both.
- Healthy cannon charges add2.2s to the existing core tells: cyclone/tornado3.8s, thunderstorm4.1s and giant tempest5.0s. With both cannons destroyed, the original core-only timings remain.
- Core light, armor material highlights and every living component's silhouette aura increase through authored charge levels. Actual sampled aura frame changes accelerated from12.27/s early to28.64/s late. The simulation-time phase integral avoids discontinuous clock-times-frequency jumps.
- The whole hull, reactor, turret bodies and cannon armor participate. Auras follow the actual part shapes; destroyed parts use their separate charred frames. Hit flashes remain native and visibly replace the part pixels before expiring.
- Native charge/release and wind sounds accompany the turn; one gated wind cue sustains the pair without doubling each report.

## Art and integration

The built-in image generator produced the modular kit and separate16frame beam
loop. Original outputs, exact prompts and reference provenance are in
[`PROMPTS.md`](../_BUILD_SOURCE/thunderhead_modular_1104/PROMPTS.md).
Measured extraction rectangles preserve the generator's intruding row gutters
and full cannon caps. The reactor detaches at its coupling collars.

The pack has19 banks,313 authored frames and11.2MB of runtime PNG pages, with
editable Aseprite sources. All native cells have even dimensions and fixed roots;
each bank has one proportional scale. Main assembly uses a576px cell at1:1.
The gun has generated neutral/left/right poses, recoil, charge, white hit and
charred states; cannons and reactor have independent charge/hit/wreck states.

- Runtime: `assets/thunderhead_modular_1104.js`.
- Art/physical mounts: `assets/thunderhead_modular_art_1104.js` and `assets/game/levels/stage_06/boss/thunderhead_modular_1104/manifest.json`.
- Builder/editable sources: `_BUILD_SOURCE/thunderhead_modular_1104/`.
- Exact collision data:869,760 bytes;190 masks match source alpha. No per-frame GPU readbacks or new runtime recolouring/compositing/transforms are used by the kit.

FB112 retains the native6348HP budget, six-weapon protection gate, damage
attribution, hit flashes, rewards and defeat. TM115 supplies the new measured
model, masks, three-pose bores and live part targets. The existing cyclone,
tornado, thunderstorm and giant-core-tempest book/weather remain active.
Normal/Hard, Stage X, Razorwake and Rough Riders retain their existing owners.

## Verification

- 37/37 native checks pass, including source-pixel targets, actual armor and hit-flash pixels, observed charge acceleration, both muzzle anchors, beam contact/safe corridor, pause, per-cannon cancellation, core gate, death cleanup and route separation.
- 313/313 frames survive real Aseprite re-export and match the packed runtime cells in visibleRGBA and exact alpha. All isolated effects keep their fringes inside their cells; the continuous beam intentionally meets its emitter edge. All190 collision masks match source pixels.
- 55s high-quality native profile:59.73FPS solo;56.83FPS with native allies, with no browser errors.
- Final real-engine movie: 55.74 engine FPS across 103.656s, native6348HP and defeat, labelled invulnerable Cole input bot,55s player hold-fire and native allies. No enemy HP/phase/timer edits after spawn. Audio peak-1.5dB; charge, release, wind and lightning cues were observed. Full decode/source-stability/browser/asset/audio checks pass.
- WebM/H264 capture caused a separate slowdown in the diagnostic take. Native MP4 capture keeps the same960x1024 high-quality game canvas and preserves performance. The boss bar is in this canvas; cabinet side rails are outside the movie.
- 11/11 review-page checks pass: frames/dimensions, sound, playback, chapter seeking, byte ranges and mobile width.
- Syntax checks pass. Required `_BUILD_SOURCE/test_fl.js` still stops before its summary on the pre-existing `difficultyHealthBaseline15 is not defined` in combat_polish_0927b.js:151. This is not a full-suite pass.

Review: http://127.0.0.1:65118/?thunderhead=modular-1104#thunderhead .
Movie: `_shots/boss_comparison_1102/thunderhead-modular-mp4-1104/stage6-boss/stage6-furious.mp4`.
Receipts: `docs/qa/thunderhead_modular_1104/`.

The GOD film verifies rendering and behavior. Human dodgeability and a full
campaign remain playtest work. No commit or push was requested for this pass.
