from pathlib import Path
import json,shutil,hashlib
W=Path(__file__).resolve().parent;R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');S=R/'_BUILD_SOURCE/thunderhead_modular_1104';Q=R/'docs/qa/thunderhead_modular_1104';Q.mkdir(parents=True,exist_ok=True)
for p in W.glob('*.py'):shutil.copy2(p,S/p.name)
shutil.copy2(W/'PROMPTS.md',S/'PROMPTS.md')
for a,n in [(W/'probe/report.json','native-checks.json'),(W/'art-roundtrip/report.json','art-checks.json'),(W/'profile/storm-cold.json','profile-solo.json'),(W/'profile/modular-allies.json','profile-allies.json'),(W/'test_fl.log','full-suite.log')]:shutil.copy2(a,Q/n)
P=R/'_shots/boss_comparison_1102/thunderhead-modular-mp4-1104';job=json.loads((P/'batch.json').read_text())['jobs']['stage6-boss'];film=json.loads((P/'stage6-boss/report.json').read_text());V=Path(r'C:/Users/Mike/Documents/New project/BOF-Furious-Boss-Videos-1104');preview=json.loads((V/'preview-checks.json').read_text())
summary={'nativeChecks':json.loads((Q/'native-checks.json').read_text())['checks'],'art':json.loads((Q/'art-checks.json').read_text()),'recording':job,'audio':film['audio'],'sourceHashes':film['sourceHashes'],'preview':preview,'gameSHA256':hashlib.sha256((R/'assets/game.js').read_bytes()).hexdigest(),'generation':'Built-in image_gen; exact source PNGs and full prompt set in _BUILD_SOURCE/thunderhead_modular_1104/PROMPTS.md','limits':'Native GOD/input-only isolated encounter footage and deterministic fixtures, not a full campaign or human dodgeability certification. Required broad suite retains the existing difficultyHealthBaseline15 VM setup error.'}
(Q/'summary.json').write_text(json.dumps(summary,indent=2))
fps=f"{job['nativeFps']:.2f}";seconds=f"{job['seconds']:.3f}";peak=str(job['peakDb'])
doc=f'''# Thunderhead — regenerated modular wind-cannon kit

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
[`PROMPTS.md`](../../_BUILD_SOURCE/thunderhead_modular_1104/PROMPTS.md).
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

-37/37 native checks pass, including source-pixel targets, actual armor and hit-flash pixels, observed charge acceleration, both muzzle anchors, beam contact/safe corridor, pause, per-cannon cancellation, core gate, death cleanup and route separation.
-313/313 frames survive real Aseprite re-export and match the packed runtime cells in visibleRGBA and exact alpha. All isolated effects keep their fringes inside their cells; the continuous beam intentionally meets its emitter edge. All190 collision masks match source pixels.
-55s high-quality native profile:59.73FPS solo;56.83FPS with native allies, with no browser errors.
-Final real-engine movie: {fps} engine FPS across {seconds}s, native6348HP and defeat, labelled invulnerable Cole input bot,55s player hold-fire and native allies. No enemy HP/phase/timer edits after spawn. Audio peak{peak}dB; charge, release, wind and lightning cues were observed. Full decode/source-stability/browser/asset/audio checks pass.
-WebM/H264 capture caused a separate slowdown in the diagnostic take. Native MP4 capture keeps the same960x1024 high-quality game canvas and preserves performance. The boss bar is in this canvas; cabinet side rails are outside the movie.
-11/11 review-page checks pass: frames/dimensions, sound, playback, chapter seeking, byte ranges and mobile width.
-Syntax checks pass. Required `_BUILD_SOURCE/test_fl.js` still stops before its summary on the pre-existing `difficultyHealthBaseline15 is not defined` in combat_polish_0927b.js:151. This is not a full-suite pass.

Review: http://127.0.0.1:65118/?thunderhead=modular-1104#thunderhead .
Movie: `_shots/boss_comparison_1102/thunderhead-modular-mp4-1104/stage6-boss/stage6-furious.mp4`.
Receipts: `docs/qa/thunderhead_modular_1104/`.

The GOD film verifies rendering and behavior. Human dodgeability and a full
campaign remain playtest work. No commit or push was requested for this pass.
'''
doc=doc.replace('\n-37/37','\n- 37/37').replace('\n-313/313','\n- 313/313').replace('\n+-','\n-').replace('\n-55s','\n- 55s').replace('\n-Final','\n- Final').replace('\n-WebM','\n- WebM').replace('\n-11/11','\n- 11/11').replace('\n-Syntax','\n- Syntax')
(R/'docs/THUNDERHEAD_MODULAR_1104.md').write_text(doc,encoding='utf8')
note=f'''<!-- thunderhead-modular-1104 -->
## November4 — regenerated Thunderhead, full-body aura and wind cannons

TM115 supersedes live FB112 Thunderhead art/model with a generated empty hull, separate reactor, four actual turret instances and two cyclone-cannon pods.313 authored frames /19 banks, editable Aseprite and exact prompts are retained. Both cannon mouths emit giant animated wind beams during a longer core charge; whole armor and silhouette1015 pulses accelerate continuously. Preserve native6348HP, six-module/core gate, per-piece hit flash, storm book/weather, exact-mask collision and once-only native defeat.37 native checks,313 frame/runtime comparisons,190 masks and11 review checks pass. Final high-quality native MP4 fight {fps}FPS with actual audible cues; allied live profile56.83FPS. Broad suite retains its pre-existing health-helper setup error. See docs/THUNDERHEAD_MODULAR_1104.md and docs/qa/thunderhead_modular_1104. Local review http://127.0.0.1:65118/?thunderhead=modular-1104#thunderhead . No commit/push.

'''
for n in ['HANDOFF_CODEX.md','CLAUDE.md']:
 p=R/n;old=p.read_bytes()
 if b'<!-- thunderhead-modular-1104 -->'not in old:p.write_bytes(note.replace('\n','\r\n').encode('utf8')+old)
print('Archived generated sources/prompts,37 native checks,313 frames,190 masks, profiles and final movie evidence.')
