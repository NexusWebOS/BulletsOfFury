# Stage 8 shoulder arcs — October 18

The Infused host, Ghost, Colossus and volcano now perform physical left and
right arm swipes. The previous host/Ghost motion only pointed toward a target
and returned; the Colossus used a whole-body scythe clip. Combat swipes now
use the authored individual limbs, fixed measured shoulder sockets and a
133-degree sweep that passes through the committed target. No arm is stretched.
Existing roar, avatar, defeat and reform banks remain in place.

Owner: `assets/stage8_identity_1018.js`, after the existing Stage 8 layers.
The normal campaign attack books call these arcs; they are not preview-only.
The volcano adds its swipes between native Furnace attacks, during its arms
phase. Its arms/body/head pools, flamethrower and cannon remain native. Hammer
retains the real Stage 5 controller and its authored left/right strike banks.
The aircraft forms keep their physical pods, fans and launchers.

Each side commits a position, approaches during its warning, plants the
shoulder, sweeps across the target and recovers harmlessly. The next side
gets a separate warning and target. Normal and Hard perform two alternating
swipes; Furious adds a third crossover. Destroying an arm cancels its contact
and subsequent attacks; phase changes clear the entire swipe controller.
Body return is continuous, including the handoff back to Furnace movement.

| Timing in seconds | Normal | Hard | Furious |
| --- | ---: | ---: | ---: |
| First warning | 1.28 | 1.08 | 0.90 |
| Follow-up warning | 0.86 | 0.74 | 0.62 |
| Each active sweep | 0.62 | 0.52 | 0.43 |

The curved warning reuses the native green/yellow/red FOV artwork and alert,
clipped to the measured blade/forearm's radial envelope. The first visual
inspection caught overlapping short cones producing a starburst; that was
replaced with one continuous field. Claw collision inverse-transforms the
actual source alpha, excludes the upper shoulder, and samples the angular
motion at intervals no greater than five pixels of tip travel. It damages
only during the active stroke. Ordinary rectangle/body contact does not run
under this dedicated melee controller. Bullets, module locks and visible hit
flashes continue to use the same moving rig and their existing damage paths.

No production art or atlas was modified. Cells remain 320×320, with the
existing fixed canvas/pivot and one proportional scale; only joint rotations
and world positions change. Both native module and owner flash timers render
and expire normally.

The existing review page has four new selectors: Infused swipes, Ghost rakes,
Colossus scythes and volcano swipes. Its onion option overlays the actual
shoulder sweep poses. It still uses the full real playfield and side HUD,
isolates campaign saves and grants invulnerability only in the review.

Verification:

- Native Chromium swipe probe: **89 passed, 0 failed**, across Normal, Hard
  and Furious. Covers both arcs, fixed shoulders, uniform scale, committed
  targets, actual contact, dodge space, hit pixels/expiry, arm destruction,
  cleanup and natural campaign scheduling.
- Native Stage 8 sequences: **32 passed, 0 failed**, including the real
  Hammer/Furnace attacks, modular damage, phase fades and one campaign clear.
- Delivered preview: **24 passed, 0 failed**, including all four new selectors
  and their actual onion views. No page, console, drawing or asset errors.
- `node --check assets/game.js` and the edited Stage 8 script: passed.
- `_BUILD_SOURCE/test_fl.js`: final BUILD OK banner, exit 0, **8,784 passing
  assertions, 0 errors**, matching this turn's measured baseline.

Records: `docs/qa/stage8_swipes_1018.json`. Full screenshots, onions and real
gameplay GIF captures: `_shots/stage8_swipes_1018/`. The first browser run also
caught a Furnace return snap, which was fixed and retested on all three
difficulties. Earlier local `game.js` and `test_fl.js` edits and line endings
are preserved. No commit or push was requested or performed.
