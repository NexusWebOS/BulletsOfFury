# Frame pacing: one tick per frame (October 9, 2026)

Mike, after watching Shadow Gangs Zero (JKM Corp, Neo Geo): *"Idk how they got the game to animate this smooth
and feel and run so smooth, but thats what we need!"*

YouTube blocks downloads from this environment, so the footage itself could not be stepped through. Only its
public keyframes and the developer's notes were available. Those notes credit two things: **more animation frames
per character**, and a board that runs one game tick per vertical blank and never drops one.

The second is engine work, and BOF was measurably failing at it.

## The bug

`maneuver_safety_1007.js` correctly runs combat on a fixed 60 Hz tick. However, it decides **how many** ticks a
frame gets with a time accumulator.

On a 60 Hz display, the accumulator sits exactly on its threshold, so sub-millisecond rAF jitter decides on every
frame whether it runs 0 ticks or 2. The ship holds still for one frame, then jumps double the distance, while
flying straight.

`_BUILD_SOURCE/probe_pacing_1009.py` drives the real `loop()` with synthetic vsync timestamps:

| display | before: off-cadence frames | after |
|---|---|---|
| 60 Hz, ±0.35 ms jitter | **231 / 450** (115 holds + 116 double jumps) | **0** |
| 59.94 Hz | 0 | 0 |
| 120 Hz | 0 | 0 |
| 144 Hz | 0 (inherent 0/1 mix) | 0 |
| 60 Hz, ±2.5 ms jitter | 0 | 1 (warm-up right after the rate change) |

## The fix

`assets/frame_pacing_1009.js` adds a **cadence lock**:

- The game tracks the display interval.
- **Near a whole multiple of the tick** (60, 30 or 20 Hz): every frame runs `round(frame / tick)` ticks, with no
  carried debt.
- **Near a whole fraction** (120, 180 or 240 Hz): a phase counter runs exactly one tick every k frames.
- **Anything else** (144 or 75 Hz): the original accumulator still runs.

A real hitch still catches up, capped at 3 ticks. Per-tick speed is unchanged. Taps latch until read, so a no-tick
frame never drops a button press. Only `combatFrame` is replaced; `updatePlay` and everything the suite calls are
untouched.

The Overdrive ground build (`expansion/topdown/js/main.js`) had the same accumulator, and now uses the same lock.

`ART.draw` there also rounds every sprite to whole world pixels. The camera was already rounded, so sprites now sit
on the same grid as the floor, which is how a sprite chip draws, and stop shimmering a pixel against it while they
move.

## Verification

- Base game: full `test_fl.js` gives **7,952 ok, 0 errors**, and reaches the `FALVA/LIZZIE BUILD OK` banner.
- Expansion probes, native Chromium: museum **28/28**, campaign **29/29**, ground **23/23**.
- Data: `docs/qa/frame_pacing_1009.json`.

## Not done here, and why

- **More animation frames.** This is the other half of Shadow Gangs Zero's smoothness, and it is art. BOF's enemy
  reels are mostly 4–8 frames, and SpriteCook has 10 credits left. Adding in-between frames to the most-seen
  sprites (the pilots' ships, the stage-1 roster) is the next step if Mike wants it.
- **Sub-pixel snapping in the base game.** Sprites there draw at fractional positions on a 2× backing store. Fixing
  that means touching hundreds of draw sites, and it is measured as a smaller effect than the cadence bug.
- **Hitstop** (a 2–4 frame freeze on heavy hits). It is a common source of arcade "feel", but it could not be
  confirmed in this footage. It is offered as an option rather than guessed in.
