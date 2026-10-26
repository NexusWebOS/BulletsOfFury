'use strict';
/* Chronos: the rage opener and the orb attack (Claude, Oct 26).
 *
 * Mike: "as soon as he forms and finalizes it, make him fly up, fly into the
 * background, begin moving left and right fast while gravitating and make him do a
 * kamehameha wave. Whenever he charges it, there should be a charge sound similar to
 * the dragon ball z sound they used, and the screen darkens as he charges up,
 * energy glows/his aura glows, and it should be a loud laser blast sound. then make
 * him fly back up north, return to the screen. And do his new attacks. You may also
 * include his orb laser beam attack ... but of course fix the animations."
 *
 * THE OPENER runs once, the moment the rage form settles (C30 starts its loop), on
 * the C30 state object (h.c30) with its own phases, all art already in the game:
 *   kame_up      north off the screen and back in, small, in the background
 *                (c35DepthFlight to scale .42, the same flight the rage loop uses)
 *   kame_strafe  two fast swings left and right across the sky, bobbing as he floats
 *   kame_charge  the hip gather (C30 cast 0-3), a BLUE energy ball growing between his
 *                hands, the screen darkening, his aura blazing (c45Aura), the
 *                committed lane warned; the charge sounds layered
 *   kame_thrust  the two-handed push (C30 thrust)
 *   kame_fire    the blue wave (wave_smooth, the authored 28-frame beam) down the
 *                locked lane; the loudest blast sounds layered, a shake and a flash
 *   kame_recover the dark lifts
 *   kame_return  north off the screen and back in to the foreground (scale 1)
 * then his normal rage loop (palm volleys, the wave, and the orb, below).
 * Load after chronos_rageform_1026.js. */
const C46 = { base: { tick: hammerBossTick, draw: hammerBossDraw, blue: ha21Blue }, events: [] };
const C46_T = { strafe: 2.24, charge: 2.6, lock: 1.75, thrust: .36, fire: 1.6, recover: .55 };
const C46_W = 2 * Math.PI / 1.12;   /* two full swings in the strafe, ending back on centre */
function c46Log(type, data) { C46.events.push({ type, t: efxClock, ...(data || {}) }); if (C46.events.length > 300) C46.events.shift(); }
function c46Own(b) { return typeof c30Own === 'function' && c30Own(b) && b._hammer.c30 && /^kame_/.test(b._hammer.c30.phase || ''); }
function c46Sfx(k) { try { const fn = Audio.SFX && Audio.SFX[k]; if (fn) fn(); else if (typeof Snd !== 'undefined' && Snd.play) Snd.play(k); } catch (e) {} }
if (typeof stageLoadBegin === 'function') { const base = stageLoadBegin; stageLoadBegin = function (n, keys) { if (n === 5 && typeof Snd !== 'undefined' && Snd.prepare) Snd.prepare(['warpCharge', 'hammerEradCharge', 'fusionBeam', 'expBig']); return base.apply(this, arguments); }; }
function c46Centre() { return (camLeftX() + camRightX()) / 2; }
function c46Sky() { return viewTopY() + 135; }

/* start it the first time the rage loop starts */
(function () {
  const start = c30Start;
  c30Start = function (b) {
    const r = start.apply(this, arguments), h = b._hammer;
    if (!h._c46Done && h.c30) {
      const R = h.c30;
      R.from = { x: b.x, y: b.y, scale: R.scale ?? 1 };
      R.to = { x: c46Centre(), y: c46Sky(), scale: .42 };
      R.hit = new Set(); R.lock = null; R.k46 = { dark: 0, sfx: {} };
      c30Phase(b, 'kame_up'); c46Log('opener');
    }
    return r;
  };
})();

function c46Hand(b) { return c30Hand(b, false); }
function c46Lock(b) {
  const R = b._hammer.c30, p = targetShip(b.x, b.y), from = c30Hand(b, true), dy = Math.max(90, p.y - from.y), dx = p.x - from.x;
  const L = (PLAY.y + PLAY.h + 90 - from.y) / dy;
  R.lock = { x: from.x + dx * L, y: PLAY.y + PLAY.h + 90 };
  c46Log('lock', { from, to: R.lock });
}
function c46Line(b) { const R = b._hammer.c30, from = c30Hand(b, true); return { from, to: R.lock || { x: player.x, y: PLAY.y + PLAY.h + 90 } }; }

hammerBossTick = function (b, dt) {
  if (!c46Own(b)) return C46.base.tick.apply(this, arguments);
  const h = b._hammer, R = h.c30, K = R.k46 || (R.k46 = { dark: 0, sfx: {} });
  if (typeof c30BudgetTick === 'function') c30BudgetTick(b, dt);
  R.t += dt; h.t = R.t; b._noHit = false;
  const once = (id, fn) => { if (!K.sfx[id]) { K.sfx[id] = true; fn(); } };
  switch (R.phase) {
    case 'kame_up':
      if (c35DepthFlight(b, R, .42)) { R.scale = .42; K.x0 = b.x; K.y0 = b.y; c30Phase(b, 'kame_strafe'); }
      break;
    case 'kame_strafe': {
      const span = (camRightX() - camLeftX()) * .34;
      b.x = K.x0 + Math.sin(R.t * C46_W) * span;
      b.y = K.y0 + Math.sin(R.t * 2.7) * 10 - Math.abs(Math.sin(R.t * C46_W)) * 8;   /* floats, dips at the turns */
      if (R.t >= C46_T.strafe) { b.x = K.x0; c30Phase(b, 'kame_charge'); K.sfx = {}; c46Log('charge'); }
      break;
    }
    case 'kame_charge':
      b.y = K.y0 + Math.sin(R.t * 2.7) * 4;
      once('c0', () => c46Sfx('warpCharge'));
      if (R.t >= .9) once('c1', () => c46Sfx('hammerEradCharge'));
      if (R.t >= 1.8) once('c2', () => c46Sfx('hammerEradCharge'));
      shake = Math.max(shake, 1 + Math.floor(R.t / C46_T.charge * 4) * 1.4);
      if (!R.lock && R.t >= C46_T.lock) c46Lock(b);
      if (R.t >= C46_T.charge) c30Phase(b, 'kame_thrust');
      break;
    case 'kame_thrust':
      if (R.t >= C46_T.thrust) {
        c30Phase(b, 'kame_fire');
        c46Sfx('fusionBeam'); c46Sfx('expBig');
        if (typeof c33Sound === 'function') c33Sound('thunder', b, 1);
        shake = Math.max(shake, 12); flashScreen = Math.max(flashScreen || 0, .3);
        c46Log('fire');
      }
      break;
    case 'kame_fire': {
      const L = c46Line(b);
      if (R.t > .05 && R.t < C46_T.fire - .2 && typeof c41Hit === 'function' && c41Hit(L.from, L.to, R.t, C46_T.fire, player))
        b20HitSegment(b, L.from, L.to, Math.hypot(L.to.x - L.from.x, L.to.y - L.from.y) * .27, 'Chronos kamehameha', R.hit);
      shake = Math.max(shake, 6);
      if (R.t >= .7) once('f1', () => c46Sfx('fusionBeam'));   /* the roar sustains */
      if (R.t >= C46_T.fire) { c30Phase(b, 'kame_recover'); c46Sfx('laserBeamEnd'); }
      break;
    }
    case 'kame_recover':
      if (R.t >= C46_T.recover) { R.from = { x: b.x, y: b.y, scale: R.scale }; R.to = { x: c46Centre(), y: viewTopY() + 190, scale: 1 }; c30Phase(b, 'kame_return'); }
      break;
    case 'kame_return':
      if (c35DepthFlight(b, R, 1)) {
        R.scale = 1; h._c46Done = true; R.lock = null; R.hit = new Set(); R.cycle = 0;
        c46Log('opener-done');
        c30Retreat(b);   /* into the normal rage loop */
      }
      break;
  }
  /* the dark builds through the charge and lifts in the recover */
  const target = R.phase === 'kame_charge' ? clamp(R.t / .7, 0, 1) * .74 : R.phase === 'kame_thrust' || R.phase === 'kame_fire' ? .74 : 0;
  K.dark = R.phase === 'kame_recover' ? .74 * (1 - clamp(R.t / C46_T.recover, 0, 1)) : target;
  b._drawY = b.y;
};

ha21Blue = function (b) {
  if (!c46Own(b)) return C46.base.blue.apply(this, arguments);
  const R = b._hammer.c30, k = R.scale ?? 1;
  if (R.phase === 'kame_charge') return c30Pose('cast', Math.min(3, R.t / .6 * 3), k);
  if (R.phase === 'kame_thrust') return c30Pose('thrust', R.t / C46_T.thrust * 8, k);
  if (R.phase === 'kame_fire') return c30Pose('cast', 5, k);   /* held: cast 5/6 at 14 fps read as a vibrating body */
  if (R.phase === 'kame_recover') return c30Pose('cast', 7, k);
  return c30Pose('cast', 0, k);
};

/* the blue energy ball between his hands: the head of the authored C30 wave, growing,
 * stepping brightness on the ladder */
function c46Ball(b, u) {
  const a = c30Row('wave', 0); if (!XART.rdy(a.key)) return;
  const p = c46Hand(b), k = b._hammer.c30.scale ?? 1, L = CG.ladder, f = Math.floor(efxClock * 14) % 4;
  const im = XART.get(a.key);   /* the red rage energy head, as authored */
  const size = lerp(16, 74, u) * Math.max(k, .72) * (1 + [0, .06, .12, .06][f]);   /* readable even in the background */
  ctx.save(); ctx.imageSmoothingEnabled = false;
  ctx.drawImage(im, 40, 0, 112, 85, p.x - size / 2, p.y - size * .38, size, size * .76);
  ctx.globalCompositeOperation = 'lighter'; ctx.globalAlpha = L[2 + (f & 1)];
  ctx.drawImage(im, 40, 0, 112, 85, p.x - size * .35, p.y - size * .27, size * .7, size * .53);
  ctx.restore();
}
hammerBossDraw = function (b) {
  if (!c46Own(b)) return C46.base.draw.apply(this, arguments);
  const R = b._hammer.c30, K = R.k46 || {};
  /* the screen darkens under him (everything already drawn), not over him */
  if (K.dark > 0) { ctx.save(); ctx.fillStyle = 'rgba(2,0,10,' + K.dark + ')'; ctx.fillRect(camLeftX() - 4, viewTopY() - 4, camRightX() - camLeftX() + 8, viewH() + 8); ctx.restore(); }
  /* the aura blazes while he charges and fires */
  const blazing = ['kame_charge', 'kame_thrust', 'kame_fire'].includes(R.phase);
  if (blazing && typeof c45Aura === 'function') {
    const q = ha21Blue(b), k = q.k ?? 1, st = R.phase === 'kame_charge' ? clamp(R.t / 1.2, .25, 1) : 1;
    ctx.save(); ctx.translate(b.x, b.y); ctx.scale(k, k); ctx.translate(-b.x, -b.y);
    try { c45Aura(b, q.a, st); } catch (e) { c46Log('aura-error', { e: String(e) }); }
    ctx.restore();
  }
  const r = C46.base.draw.apply(this, arguments);
  if (R.phase === 'kame_charge') {
    const L = c46Line(b), u = clamp(R.t / C46_T.charge, 0, 1);
    if (R.lock || R.t >= .9) C25.base.warning(b, { x: L.from.x, y: L.from.y, ex: L.to.x, ey: L.to.y, width: 76, progress: clamp((R.t - .9) / (C46_T.charge - .9), 0, 1), fieldOnly: true });
    c46Ball(b, u);
  } else if (R.phase === 'kame_thrust') c46Ball(b, 1);
  else if (R.phase === 'kame_fire' && typeof c41Draw === 'function') {
    const L = c46Line(b);
    c41Draw(L.from, L.to, R.t, C46_T.fire, true);   /* his red rage wave (Mike: 'he should be using the red one we had') */
    c46Ball(b, 1);
  }
  return r;
};
/* the low-HP damage vents are sized from his full-size box: during the opener they are off,
 * and anywhere else in the rage loop they are scaled to his depth (in the background they
 * floated around his head as big grey clouds) */
(function () {
  const base = encounterDamageOverlay;
  encounterDamageOverlay = function (b) {
    if (b && c46Own(b)) return;
    const k = b && typeof c30Own === 'function' && c30Own(b) ? (b._hammer.c30?.scale ?? 1) : 1;
    if (k >= .95) return base.apply(this, arguments);
    const w = b._drawW, h = b._drawH;
    b._drawW = (w || b.w || 120) * k; b._drawH = (h || b.h || 120) * k;
    try { return base.apply(this, arguments); } finally { b._drawW = w; b._drawH = h; }
  };
})();
/* THE ORB LASER (C42): chronos_kame_1025 switched it off (c42Active = false). Back on, on
 * every other wave turn: the rage loop's wave turns are cycles 2, 5, 8...; cycle%6<3 makes
 * them orb, wave, orb, wave. */
c42Active = function (b) { return typeof c42WavePhase === 'function' && c42WavePhase(b) && (b._hammer.c30.cycle || 0) % 6 < 3; };
/* and its animation, fixed: it used to hold one arms-out frame for the whole turn with a
 * 28 px crop as the orb. Now: he gathers it at his hip (cast 2-3) while it grows, swings
 * it forward (cast 4), and holds it out as the beam fires (cast 5/6); the orb is the
 * C30 energy head, growing and crackling, and it rides his hand the whole way. */
const C46_ORB = { hip: 1.0, swing: 1.35 };
(function () {
  const blue = ha21Blue, hand = c30Hand;
  ha21Blue = function (b) {
    if (!c42Active(b)) return blue.apply(this, arguments);
    const R = b._hammer.c30, k = c30Scale(b);
    if (R.phase === 'gather') return c30Pose('cast', R.t < C46_ORB.hip ? 2 + Math.min(1, Math.floor(R.t / C46_ORB.hip * 2)) : R.t < C46_ORB.swing ? 4 : 5, k);
    if (R.phase === 'thrust') return c30Pose('cast', 5, k);
    if (R.phase === 'beam') return c30Pose('cast', 5, k);
    return c30Pose('cast', 7, k);
  };
  c30Hand = function (b, release) {
    if (!c42Active(b) || release) return hand.apply(this, arguments);
    const q = ha21Blue(b);
    return q.a.frame === 5 || q.a.frame === 6 ? hb20World(c30Row('cast', 5), [130, 88], b, c30Scale(b), 0) : hb20World(q.a, q.a.tip || [128, 120], b, q.k, 0);
  };
})();
c42Orb = function (b) {
  if (!c42Active(b)) return;
  const R = b._hammer.c30, a = c30Row('wave', 0); if (!XART.rdy(a.key)) return;
  const u = R.phase === 'gather' ? clamp(R.t / C46_ORB.swing, 0, 1) : R.phase === 'recover' ? Math.max(0, 1 - R.t / .3) : 1;
  if (u <= 0) return;
  const p = c30Hand(b), k = Math.max(c30Scale(b), .72), f = Math.floor(efxClock * 14) % 4, L = CG.ladder, im = XART.get(a.key);
  const size = lerp(10, 66, u) * k * (1 + [0, .07, .14, .07][f]);
  ctx.save(); ctx.imageSmoothingEnabled = false;
  ctx.drawImage(im, 40, 0, 112, 85, p.x - size / 2, p.y - size * .38, size, size * .76);
  ctx.globalCompositeOperation = 'lighter';
  ctx.globalAlpha = L[2 + (f & 1)]; ctx.drawImage(im, 40, 0, 112, 85, p.x - size * .34, p.y - size * .26, size * .68, size * .52);
  ctx.restore();
  /* crackle: short red arcs spitting off the orb, a new pair every few frames */
  if (u > .3 && typeof cgBolt === 'function') {
    const t = Math.floor(efxClock * 9);
    for (let i = 0; i < 2; ++i) { const ang = (t * 2.1 + i * 3.1) % (2 * Math.PI), r = size * (.55 + .25 * ((t + i) % 2));
      cgBolt(p, { x: p.x + Math.cos(ang) * r, y: p.y + Math.sin(ang) * r }, efxClock + i * .3, 10 * k, .8); }
  }
  C42.lastOrb = { ...p, charge: u, phase: R.phase };
};
/* SMOOTHER LASER POSES (Mike: "better animation when shooting his lasers like not appearing to
 * jerk his body so much").
 *  - The red wave's beam phase (C30) flipped cast 5/6 at 14 fps: he holds cast 5 now.
 *  - The palm volleys (C32) swung the whole 9-frame twist (left palm out 0 <-> right palm out 8)
 *    on EVERY shot, .13-.16 s apart, and snapped to/from the guard (10) and dual (9) poses. Now
 *    the twist is half as wide (frames 2 and 6), each shot holds its pose for 40% of the gap as
 *    the recoil, then eases to the next shot's pose, arriving as it fires; the warning stance is
 *    the centre of the twist (4), so the first shot does not snap; the dual shot holds its pose
 *    for its whole beat. The palm sockets come from the same frame, so shots still leave the palm. */
(function () {
  const blue = ha21Blue;
  ha21Blue = function (b) {
    if (typeof c30Own === 'function' && c30Own(b) && b._hammer.c30?.phase === 'beam' && !(typeof c42Active === 'function' && c42Active(b))) return c30Pose('cast', 5, c30Scale(b));
    return blue.apply(this, arguments);
  };
})();
const C46_PALM = { single: [2, 6], dual: 9, centre: 4, hold: .4 };
function c46PalmTarget(beat) { return beat === 2 || beat === 5 ? C46_PALM.dual : C46_PALM.single[beat % 2]; }
C46.oldPalm = c32Pose;
c32Pose = function (b) {
  const R = b._hammer.c30, V = R.volley, rows = C32_ART.banks.palms;
  let f = C46_PALM.centre;
  if (R.phase === 'volley_fire') {
    const iv = hammerFurious() ? .13 : .16, k = R.t / iv, i = Math.min(5, Math.floor(k)), fr = k - i;
    const a = c46PalmTarget(i), z = i < 5 ? c46PalmTarget(i + 1) : C46_PALM.centre;
    if (a === C46_PALM.dual || z === C46_PALM.dual || fr < C46_PALM.hold) f = a;
    else { const e = (fr - C46_PALM.hold) / (1 - C46_PALM.hold), s = e * e * (3 - 2 * e); f = Math.round(lerp(a, z, s)); }
  }
  return { a: rows[f % rows.length], k: R.scale, rot: 0, kind: 'c32_palms' };
};
window.BOF_CHRONOS_KAMEHAMEHA = C46;
