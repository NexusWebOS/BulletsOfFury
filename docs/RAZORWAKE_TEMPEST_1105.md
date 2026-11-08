# Razorwake — aggressive wind cycle and storm Helix

November 5, 2026. RW118 supersedes RW117's live attack book and selected art.
Mike rejected the surrounding wind ribbons, prior cyclone/tornado pattern
and capsule-like exhaust, and specified forward rolling gun runs, three burst
positions, accelerating throttle passes and a breakable growing wind orb.

## Flight and combat

The approved silver/teal fuselage, blue cockpit, detachable gun pods, intact
wings and modular core gate remain. There is no surrounding wind-ribbon,
cyclone-salvo or summoned-tornado draw in this revision.

1. Curve out of the fight, roll across the middle while firing forward, turn outside view, return across the upper screen rolling and firing in the opposite direction, then curve south back into position. Twelve authored roll projections keep both guns and engine sockets on their actual mounts. Heading/roll anchors use the selected authored pose rather than an intermediate angle.
2. Move to center, right, then left of original center. Each position has a committed straight-south gun FOV and rapid twin bursts. No player tracking, spread fan or ghost gun fire. Modules have actual spinning caps, recoil, anchored muzzle flashes and heavy machine-gun reports.
3. Show the actual metal warning and teal 1015 charge, commit a south dive toward the pilot, exit below, then enter north from below. Sixteen diagonal on/offscreen zigzags accelerate from 0.90 to 0.36 seconds; after eight, route order reverses while actual speed continues increasing to 2.5 times the first pass. Turns stay offscreen and each diagonal has its own 0.80–0.70-second lane tell. See docs/RAZORWAKE_ZIGZAG_1105.md for the current capture and collision checks. Roll lanes cover the full possible wing span; throttle contact stays inside its warning footprint.
4. Curve back into the fight from above. The cockpit and body flash teal, a source-pixel perimeter aura pulses, wing flaps accelerate, and a wind Helix orb grows at the nose. The layered sky/city darkens through authored shade frames. Sixteen individual branching lightning strikes accelerate with the existing Chronos/Dracodia strike sound, followed by the Helix release cue.

The orb rotates faster and grows through twelve authored travel sizes, up to
944 pixels. It moves from the nose toward the middle of the view, expands
over the field, then exits naturally. Exactly one can exist at a time.
Primary bullets, beams/flame and physical player missiles can break it; the
break releases exactly nine medium wind balls. Those fragments fly outward,
expire or exit, and remain unshootable, like ordinary gun slugs. They do not
bounce around indefinitely. Orb interception runs before and after the native
projectile pass so the hull cannot eat an incoming shot first.

Once both guns are destroyed, the core uses only throttle and storm-orb turns;
empty gun-only states are skipped. Core damage remains gated by both real gun
pools, with normal native hit flashes, Retina/beam routing, rewards and one
native encounter defeat.

## Exclusive vortex death

Native roll/invulnerability, shield, special and GOD protections resolve first.
On a fatal orb contact, the native life/death/loadout owner runs exactly once.
The burning wreck is carried in the orb, thrown above view, then falls back
with the actual pilot's native spin reel through 810 degrees. It crashes near
79% of screen height with the native shock ring and explosions. The orb rises offscreen with the airborne throw, clearing the falling wreck and crash. The native death banner is delayed until that crash. The sequence
does not fabricate a win, bypass GOD or charge a second life. Retry and stage
reset remove its owner. All orb/fragment effects are bounded and cancelled
with their launching encounter.

## Difficulty and art

The browser comparison measured the existing Hard Stage 6 fortress at
**1,552 HP**. Razorwake now has **1,785 HP**, about 15% more and 8% above its
previous total: 536 left gun, 536 right gun and 713 protected core. Existing
compound difficulty/NG+/co-op scaling is retained through the original factory
budget. The aggressive pattern book is the main difficulty difference.

Two new sources were made with the built-in image generator: a coherent
sixteen-frame internal wind-orb loop referenced from the actual Maverick Helix
ball, and one tapered shock-cell exhaust silhouette. No PixelLab job is
claimed. Originals and exact prompts are retained in
`_BUILD_SOURCE/razorwake_tempest_1105/PROMPTS.json`.

There are **1,601 new authored frames in 38 banks**, including precomposed pixel-identical hull/wing presentation, twelve roll
projections, independent gun roll/recoil states, new exhaust grades,
perimeter/cockpit emission, charge sizes, orb travel sizes, nine-ball rupture,
branching lightning and background shade steps. The existing approved storm
bolt pixels were recolored offline into teal/white. The engine does not add
sprite rotation, scaling, alpha animation or procedural wind art. New exhaust
uses one silhouette with pre-authored glow grades and fixed cruise/throttle
sizes. Cells are fixed and even with stable pivots; packed pages restore exact
source positions. Source-derived roll masks complement the existing native
modular gun/core masks. Full-bleed shade tiles intentionally meet their edges.

Editable Aseprite sources, strips, manifests, original outputs and rebuild
scripts are retained under `_BUILD_SOURCE/razorwake_tempest_1105/`.
Runtime owners are `assets/razorwake_tempest_1105.js` and its art registry,
loaded after RW117. Core `assets/game.js` remains unchanged. Other encounters
and difficulty owners keep their existing routes.

## Verification and review

- **33 native checks pass:** native Hard comparison and health budget; all attack families at untouched health; both forward rolling streams; three fixed south-firing positions; sixteen accelerating/reversed passes; useful base-speed response time; no old wind ribbons; real aura/cockpit pixels; finite ordnance; pause; physical gun targets, wing pixels, detachment and hit expiry; full core gate; dangerous core-only attack choices; beam/bullet/missile orb breaks into exactly nine; GOD/shield protection; full native vortex lift/fall/crash; retry; native defeat/cleanup and no browser/render errors.
- **1,601/1,601 frames** pass actual Aseprite re-export and packed-runtime visible RGBA/alpha comparisons, with 24 exact roll masks. Non-tile graphics are unclipped; background shade cells have explicit full-bleed edges.
- The first full capture exposed a sustained-firing/core-phase regression (30.85 average FPS; several severely stalled windows). It was rejected. Profiling located the cost in repeated hull/wing layer blits rather than the controller. The same hull, wing, shadow, charge and hit pixels are now composed offline into fixed frames; actual guns remain independent. This reduced the boss presentation from up to nine hull/wing blits to two or three without reducing resolution. About 454 MB of superseded Razorwake/shadow preload pages are also excluded; current Thunderhead and exhaust assets remain available. An ImageBitmap experiment did not improve sustained firing and was removed.
- The final uncaptured sustained-fire diagnostic measured **57.97 FPS**, compared with 41.70 FPS for the earlier drawing path under the same profiler. Boss drawing fell from about 7.6 ms per drawn frame to 1.2 ms, with 9.5 ms maximum in that measured sample. Capture requests complete native frames at 30 Hz rather than asking the browser to capture every draw automatically. This is a measured desktop result, not a guarantee of a locked 60 FPS on all machines.
- Final native full fight: **57.10 engine FPS across 114.164 seconds**, 60 seconds player hold-fire, then an input-only Cole GOD bot; full native 1,785 HP, modules, timers, audio and defeat. No enemy HP/phase/timer writes after spawn. 960×1024 native high-quality game canvas, 30 FPS media; cabinet side panels are outside the movie. Audio peak **-1.7 dB**. Decode/source stability/browser/asset/audio checks pass.
- Separate real-RAF vortex film: earlier attacks use GOD; it switches off when the first natural orb releases. The pilot holds fire. The untouched boss remains alive, while the native player dies once through capture, throw, fall and crash. The short review clip is trimmed from this actual engine recording, with actual game audio.
- Six compatibility checks also pass: Normal excludes the Furious alternate; Hard keeps its native fortress; Stage X is excluded; Furious Thunderhead retains its six modules and controller; obsolete page exclusion preserves current art readiness; no browser/render errors. These are scoped checks, not complete campaign playtests.
- **14 preview checks pass**, including video/audio, chapters, range serving, the separate vortex film and mobile fit.
- Syntax and Windows-line-ending-aware whitespace checks pass. Required `_BUILD_SOURCE/test_fl.js` still stops on the pre-existing `difficultyHealthBaseline15 is not defined` in `assets/combat_polish_0927b.js:151`. This is not a full-suite pass. The failure log is retained.

Review: http://127.0.0.1:65121/?razorwake=tempest-final-1105#razorwake

Full movie: `_shots/boss_comparison_1102/razorwake-tempest-final-ready-1105/stage6-mini/stage6-furious.mp4`.
Vortex: `_shots/boss_comparison_1102/razorwake-vortex-final-1105/stage6-mini/vortex-death.mp4`.
Receipts: `docs/qa/razorwake_tempest_1105/`.

These are isolated native encounter/death recordings and automated counter
checks, not a completed human dodgeability test or full campaign run.
No commit or push was requested.
