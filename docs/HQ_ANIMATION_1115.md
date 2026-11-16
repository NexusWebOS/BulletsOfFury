# November15: actual pilot animation, sliding HQ doors and guarded escape

Original BOF checkout: `D:/BOF-Downloads/2026-11-14/RevG-source`. This continues HQ19 and supersedes the straight simultaneous launches and four-pose cutout performances in the November14-15 reel. No unrelated game, boss, combat or release changes.

The starfield stops scrolling once Earth reaches its settled reveal position (return t4.8). The actual selected Furyship continues south and scales down. Both the native scroll value and rendered starfield pixels hold; the existing real Chronos destruction and native one-time settlement remain.

The HQ now has a physical sixteen-frame two-leaf door opening. Approved blue ribbed leaves slide into their side pockets over a newly generated recessed hangar with visible yellow floor rails. All environment pixels outside the aperture are identical across the bank. It reverses for closing; there is no color crossfade masquerading as movement. An animated preview is saved as `_shots/hq_animation_1115/door-opening.gif`.

All nine actual pilot identities now have newly generated eight-frame rightward walk cycles and eight-frame grounded celebration loops. These replace HQ19's four-pose stride/static emotional-pose switching, without changing the global C112/CP112 libraries. Proper heel contact, passing, weight transfer and opposing arm swing are authored in the drawings. The generation uses the current actual approved roster export for each pilot, including the newer green-uniform Cole likeness. The existing pilot-specific top-down disembark/walk frames remain in the small exterior entry shot.

Each delivered actor cell is384x384 with pivot192,360. The source sheets are normalized with one scale (no per-pose resize), waist/boot registration and shared padding. Low-alpha matte noise is discarded at192; accepted body RGB is preserved and exported with binary alpha. Native pixel comparisons prove the walk/celebration cells match accepted source pixels without white/gray fringes. Sixteen cells per pilot,144 actor cells total, plus16 door cells. Sources and prompts: `_ART_SOURCES/hq_animation_1115`; runtime banks: `assets/game/shared/cinematics/hq_animation_1115`; full art/prompt manifest: `docs/HQ_ANIMATION_ART_1115.json`. Built-in image_gen, no SpriteCook. Applied Mike's arcade-graphics and sprite-pipeline skills: actual identity seeds, complete-sheet animation, shared scale/pivot, motion and native pixel review.

The seven first-wave departures now run one aircraft at a time on curved paths, alternating southwest/southeast. Each ship clears before the next starts, with animated thrusters and proportional scale-up. The launch beat is21.7s; the five-second empty-base interval remains. Decker and Axel then emerge, smoothly turn to defend the apron, fire from their actual noses and shoot down six attacking jets using engine gun/muzzle/tracer/explosion art and shared mixer cues. They leave only after those takedowns, one at a time: Decker southeast, Axel southwest, continuing the alternating nine-ship order. Reinforcements still surround the base afterwards. The existing two quotes/selection avatars/fixed metal box remain. Guard beats9.6s+6.8s provide time to fight and exit without overlapping departures.

Existing Easy/Normal completion is retained; Hard/Furious use the established Stage6 continuation. The single-frame corridor, reunion and radar layout,16-frame radar alarm, scoped Stage6 airborne radio and native rewards remain.

## Evidence

- Native Chromium71/71 pixel/asset/scene checks: all9 pilot banks, all8 actual rendered poses per bank, exact source compositing, all16 distinct physical door frames, progressively exposed opening, fixed exterior, visible counterfire/takedown.
- Lifecycle26/26: real Chronos death, delayed Earth reveal and frozen star pixels/scroll, all11 native HQ beats, seven first aircraft/two guards, exactly one departing at any sampled time, alternating all9 directions, both guards shooting and six visible takedowns, continued reinforcements,5s quiet pause, original metal avatars, all16 radar frames, actual co-op pilots and decoded shared-bus audio.
- Final solo/co-op views7/7; new cast fits the wide native scene. No page, console or HTTP errors in final probes/captures.
- Full regression8,969 passed/0 failures,exit0; failing-name list remains[] against the preceding green baseline. Syntax passes. game.js remains LF and test_fl.js CRLF, both unchanged.
- Full revised recording137.69s, H264/AAC1824x1024 at30fps; strict decode zero errors. Sixteen chapter playbacks plus geometry/duration,Range206 and browser errors19/19 pass. Native audio: [Parsed_volumedetect_0 @ 000001ae7d456e00] mean_volume: -14.3 dB; [Parsed_volumedetect_0 @ 000001ae7d456e00] max_volume: -1.1 dB.
- Real Chromium, Cole/Hard. Two prepared cinematic checkpoints with no cinematic dialogue skipped; result/equipment menus between checkpoints omitted. The full85.7s authored HQ sequence continues natively through Stage6's card, fly-in and five opening radio lines to the first interactive missile interception. This is cinematic verification, not an unassisted campaign win or balance claim.

Video: `_shots/hq_animation_1115/stage5-to-6-hq-animation.mp4`.
Review: http://127.0.0.1:8766/_shots/hq_animation_1115/review.html
Receipt: `docs/qa/hq_animation_1115.json`.
Repro: `_BUILD_SOURCE/hq_animation_1115_{pack,probe,lifecycle,verify_views,record,package,verify_movie}.py`.
Owner: `assets/hq_return_attack_1114.js`; art registry: `assets/hq_animation_art_1115.js` before that owner. Prior owner/index snapshots are retained in the new art-source directory. Previous sources and reels remain. No commit, push, installer or publication.
