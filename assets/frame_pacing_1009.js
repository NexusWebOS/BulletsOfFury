'use strict';
/* frame_pacing_1009.js - one logic tick per displayed frame, the way an arcade board runs.

   Mike, 2026-10-09, after watching Shadow Gangs Zero on the Neo Geo: "Idk how they got the game to
   animate this smooth and feel and run so smooth, but thats what we need!"

   A Neo Geo runs exactly one game tick per vertical blank, so every frame advances the world by the
   same amount and motion never stutters. BOF's fixed 60 Hz combat clock (maneuver_safety_1007.js)
   gets the TICK right but leaves the CADENCE to a time accumulator, and on a 60 Hz display that is
   the worst case: the accumulator sits exactly on its threshold, so sub-millisecond rAF jitter
   decides every frame whether it runs zero ticks or two. Measured with _BUILD_SOURCE/probe_pacing_1009.py
   at 60 Hz with +-0.35 ms jitter: 231 of 450 frames (51%) were a 0-tick hold or a 2-tick jump - the
   ship visibly shuffling while flying straight.

   Cadence lock: the display interval is tracked with an average. When it is close to a whole multiple
   of the tick (60 Hz -> 1 tick, 30 Hz -> 2) each frame runs round(frame/tick) ticks with no carried
   debt, so jitter can never split a tick across frames. When it is close to a whole fraction (120 Hz
   -> every 2nd frame, 240 -> every 4th) a phase counter runs exactly one tick on every k-th frame.
   Anything else (144, 75 Hz...) keeps the accumulator. A real hitch (a frame well over the expected
   interval) still catches up, capped at 3 ticks like before. Per-tick game speed is unchanged; a
   59.94 Hz display runs 0.1% slow instead of dropping a tick every 17 seconds.

   Taps are latched until read (Input.tap), so a frame that runs no tick never drops a button press.
   Only combatFrame changes: updatePlay, every timer and every test that calls it directly are untouched. */
const BOF_PACE = { avg: 1 / 60, mode: 'free', phase: 0, tol: 0.07, log: { lock: 0, div: 0, free: 0 } };
function bofPaceSteps(dt) {
  const C = BOF_COMBAT_CLOCK, P = BOF_PACE;
  P.avg += (Math.min(dt, 0.1) - P.avg) * 0.06;
  const r = P.avg / C.step, n = Math.round(r), k = Math.round(1 / r);
  if (n >= 1 && n <= 3 && Math.abs(r - n) < P.tol * n) {            // 60 / 30 / 20 Hz: whole ticks per frame
    P.mode = 'lock'; C.debt = 0; P.phase = 0;
    return Math.max(1, Math.min(3, Math.round(dt / C.step)));
  }
  if (k >= 2 && k <= 4 && Math.abs(1 / r - k) < P.tol * k) {        // 120 / 180 / 240 Hz: one tick per k frames
    P.mode = 'div'; C.debt = 0;
    if (dt > P.avg * 1.6) { P.phase = 0; return Math.max(1, Math.min(3, Math.round(dt / C.step))); }
    P.phase = (P.phase + 1) % k; return P.phase === 0 ? 1 : 0;
  }
  P.mode = 'free';                                                   // no clean ratio: the original accumulator
  C.debt += Math.min(dt, 0.05); let s = 0;
  while (C.debt + 1e-9 >= C.step && s < 3) { C.debt = Math.max(0, C.debt - C.step); s++; }
  return s;
}
combatFrame = function (dt) {
  const C = BOF_COMBAT_CLOCK; C.steps = 0;
  if (state !== GS.PLAY || !Number.isFinite(dt) || dt < 0 || dt > 0.25) { combatClockReset(); return 0; }
  const want = bofPaceSteps(dt); BOF_PACE.log[BOF_PACE.mode]++;
  while (C.steps < want && state === GS.PLAY) {
    if (C.steps) Input.clearTaps();
    C.steps++; C.total++;
    updatePlay(C.step);
  }
  if (state !== GS.PLAY) C.debt = 0;
  return C.steps;
};
