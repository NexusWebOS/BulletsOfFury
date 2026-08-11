/* scenario_amini.js — put the stage's arsenal mini on screen so its ART can be looked at.
 *
 *   python3 _BUILD_SOURCE/shoot.py --state PLAY --stage 2 \
 *           --script _BUILD_SOURCE/scenario_amini.js --seconds 4 --fps 3 --warm 200
 *
 * The tier triggers at ~0.34 of the stage clock, which is minutes of real play, so it is
 * effectively unreachable from a capture. This spawns it directly through the game's own
 * spawnArsenalMini so the unit, its behaviour and its art are the real ones.
 *
 * The suite can prove it spawns with the right HP and the drone contract attached. It cannot
 * prove ndr_<slug>_idle_* resolves and draws — that is what this is for, and it is exactly the
 * gap that let a muzzle flash "not exist" for a drop while drawing on the wrong frame.
 */
(() => {
  player.reset();
  player.invuln = 1e9;
  enemies.length = 0;
  const slug = (typeof arsenalMiniFor === 'function') ? arsenalMiniFor(run.stage) : null;
  if (slug && typeof spawnArsenalMini === 'function') {
    const e = spawnArsenalMini(slug);
    if (e) {
      e.y = 170; e._dr.entry = 0.4;   // settled on screen rather than still entering
      /* ⚠ PIN IT. It descends at 0.9/frame, and shoot.py's dt inflates between captures — each
         screenshot is a separate evaluate, so the next frame sees the real wall-clock gap. It
         drops off the bottom before the second shot and the frame looks like it never spawned.
         Traced: alive and healthy at y=132 on frame 240 when stepped at a true 16.7ms.
         This is a capture aid for looking at the ART, and nothing else — the unit's own motion
         is verified in the suite, not here. */
      e.vy = 0; e.pattern = null;
      const keep = e.y;
      if (typeof window !== 'undefined') {
        const origLoop = window.loop;
        window.loop = function () { const r = origLoop.apply(this, arguments); if (!e.dead) e.y = keep; return r; };
      }
    }
  }
})();
