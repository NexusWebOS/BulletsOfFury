# Razorwake — modular wind refit

Completed November 5, 2026, continuing the November 4 art pass. Mike requested
proper rotary machine guns, strong coherent exhaust, accelerating wing-flap
wind attacks, warning signs and genuine removable weapons with intact wings.

## Result

RW117 supersedes the live Furious Stage 6 Razorwake presentation and attack
book. A regenerated fuselage, left wing, right wing and two complete gun pods
assemble at fixed sockets. Breaking a gun throws the complete pod away with
an actual explosion and anchored receiver smoke. No wing pixels are erased.
The native total is still 1,653 HP: 496 per gun and 661 core. Both guns must
break before the core can absorb damage; player bullets can reach the guns.
Native white hit flashes, Retina/beam routing, rewards and one defeat remain.

- The chainguns rev actual eight-phase barrel-cap frames, recoil separately and fire fast, committed straight wind-slug streams from their real mouths. The former gun spread attack is removed. Each paired burst has one heavy machine-gun report through the shared mixer.
- The engines use one generated static exhaust silhouette, with six authored pixel-light grades and fixed cruise/throttle sizes. The large white/teal flames stay attached to both nozzles; they are not animated lightning strips.
- Charged core-cyclone attacks have whole-body source-pixel 1015 emission and wind ribbons around the aircraft. These larger wind weapons are separate from the gun ammunition.
- A 3.6-second tornado summon darkens the layered city, displays the actual metal warning symbol above the aircraft, and accelerates 24 hinge poses from roughly 0.4 to 2.75 flaps/second. Wind ribbons draw behind the ship so the wings remain readable.
- A generated tornado forms over eight startup frames, sweeps and rebounds across the arena for 5.4 seconds and finishes through eight recovery frames. Its damaging area is smaller than its visible funnel. Each later pass remains dangerous after a successful roll. At most one tornado exists at once.
- The original intact true-depth rolling flyby remains while both guns are alive. A gun breaking during that flight interrupts the roll into recovery, rather than displaying an old whole-craft damage mask. This pass does not claim newly generated roll poses.
- Gun/core destruction, defeat, retry and stage changes cancel owned effects, muzzle clocks and ordinary wind rounds. Pause/render-only calls do not advance the wing, barrel or weather clocks. Normal/Hard, Thunderhead, Rough Riders and Stage X retain their separate owners.

All ordinary wind ammunition is unshootable from birth. Existing authored
FOVs, the metal charge warning and shared audio retrigger gates are used.
There is no circular shield or bullet-attached asterisk system.

## Art and implementation

Two new sources were generated with the built-in image generator, using the
existing Razorwake artwork as the identity reference for the modular kit.
No PixelLab generation or new PixelLab charge is claimed. Exact prompts and
original outputs are retained in `_BUILD_SOURCE/razorwake_modular_1104/PROMPTS.md`.
The exterior connected pale matte was removed offline, preserving enclosed
chrome highlights. Original generated files remain unchanged.

2,620 authored frames in 25 banks use 34 compact runtime PNG pages. All frames
have even fixed cells, stable pivots and shared proportional source scales.
There are 32 baked headings, 24 wing hinge poses, distinct source-derived
shadows, native hit plates, charge grades, gun spin/recoil, exhaust and wind
effects. Runtime uses direct frame blits and exact source-derived collision
bits. The 656 collision masks occupy 305,222 bytes. No runtime sprite rotation,
alpha animation, tint synthesis or shadow readback is added.

The generated wing plates are normalized into one shared ship layout. Smooth
hinge projections, gun-cap rotation, headings and glow states are authored
offline and exported through real Aseprite batch mode. Editable `.aseprite`
files, untrimmed strips, manifests, scripts and original generated sources are
retained under `_BUILD_SOURCE/razorwake_modular_1104/`. Rebuild with
`build_razor.py`, verify with `verify_art.py`, install with `install.py`.

Runtime: `assets/razorwake_modular_1104.js` and its art registry, loaded after
the existing encounter owners. New owned rounds bypass PFX13's runtime
cleanup/trail generation. `assets/game.js` is unchanged.

Decoded image pages and combined readiness are cached after loading and
invalidated on every stage load. This removes repeated per-tick asset scans
without reducing image quality, native health or attack speed. The instrumented
profile's average FB112 update time fell from about 1.8 ms to 0.08 ms; its
render cadence remained approximately 41 FPS. That profile is retained rather
than presented as a successful 60 FPS test.

## Verification and footage

- **35/35 native checks pass:** full attack cycles at untouched health; actual twin muzzle origins; one direction per gun burst; real barrel pixel changes; core gate; target masks; wing pixels unchanged on gun destruction; detached pods and receiver smoke; native hit-pixel expiry; charge/death cleanup; pause; retry; cache invalidation/repopulation; native defeat and route separation.
- **2,620/2,620 frames** match real Aseprite re-export and packed runtime visible RGBA/alpha. All banks are even, unclipped and registered. **656/656 masks** match source alpha.
- **Fresh full-fight video:** 79.225 seconds, **54.83 engine FPS**, native Furious 1,653 HP, 45 seconds of player hold-fire, then an invulnerable input-only Cole bot. Native solo rules keep NPC allies out. No enemy health, attack-timer or phase edits after spawning. The 960×1024 high-quality game canvas includes the boss bar; cabinet side rails are outside the film. Media capture is 30 FPS.
- Full media decode, audible audio (peak −1.0 dB), source stability and browser/asset/audio checks pass. Movie frames were inspected for gunfire, charge, tornado and module destruction. All loaded script and index hashes were stable throughout recording.
- **11/11 preview checks pass:** real video dimensions, playback, audible sound, chapters, range serving and mobile width. The first 64 KiB served by the preview matches the final movie exactly.
- Syntax and whitespace checks pass. Required `_BUILD_SOURCE/test_fl.js` still stops before its summary on the pre-existing `difficultyHealthBaseline15 is not defined` at `assets/combat_polish_0927b.js:151`. This is not a full-suite pass. Original failure log is retained.

Review: http://127.0.0.1:65120/?razorwake=modular-wind-1104#razorwake

Movie: `_shots/boss_comparison_1102/razorwake-modular-wind-1104/stage6-mini/stage6-furious.mp4`.
Receipts: `docs/qa/razorwake_modular_wind_1104/`.

The native GOD recording verifies behavior, rendering, module damage and
completion. Human dodgeability and a full campaign remain playtest work.
No commit or push was requested for this pass.
