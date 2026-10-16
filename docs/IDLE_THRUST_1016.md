# Idle thrusters (2026-10-16)

Mike: *"can you make our thrusters animate when were idle on all pilots?"*

## What was wrong
The animated plume is `pf27PlaneThrustDraw` (`assets/pilot_feedback_0927.js`): it stretches each pilot's own
flame tail and cycles the authored 6-frame plume reel. It returned early below 2.5% throttle, and
`pf27ThrustTick` eases throttle to 0 when the ship holds still - so a ship at rest showed only the baked flame
with the faint interior pulse from `d27ShipFrames`, which reads as static at play size.

## The change
`pf16IdleBurn(p)` is a FLOOR under `pf27ThrustPower()`: 0.14 +/- 0.06, two incommensurate sines on the game
clock (`efxClock`, so it freezes on pause), phase-offset for player 2. Real throttle still eases above it with its
own rates, so moving reads exactly as before. Dead/out ships carry no burn. The same floor reaches the space
plume (`pf27SpacePlumeDraw`), so the Furyship idles with a slightly longer, breathing flame too.
`window.PF16_IDLE = 0` switches it off (the probe's busted arm).

Both plume draws read pixels (`getImageData`); because the idle path now runs every frame, both reads are guarded
so a tainted `file://` canvas refuses the plume instead of throwing in the hull draw.

## Measured (real Chromium, stage 1, no input) - `_BUILD_SOURCE/probe_idle_thrust_1016.py` 46/0
All nine pilots: plume drawn 48/48 idle frames, cycling 6 distinct reel frames, length breathing ~1.2-2.2 px
(e.g. Cole 9.6..11.4, Juggernaut 11.7..13.9); busted arm draws 0; full throttle still 2.3x longer (Cole 26.9).
0 page/console errors. Visual: `docs/proofs/idle_thrust_1016/idle_on_off.png` (per pilot: off row, then on row,
8 consecutive frames). Suite section 381 (`test_idle_thrust_1016.cjs`).
