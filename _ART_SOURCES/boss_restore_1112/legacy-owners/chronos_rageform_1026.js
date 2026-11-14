'use strict';
/* Chronos red-rage forming (Claude, Oct 26).
 *
 * This layer owns only the DRAW of the rage charge. C43 (chronos_transform_1025.js)
 * keeps the clock, the protection and the float; chronos_commitment_1025.js keeps the
 * length (CG_SSJ, 7.2 s). The charge runs u = 0..1 in five beats:
 *
 *   THROW    0-.17   his own two-handed throw, the authored arch_hammer_throw_0926
 *                    reel with the big square-headed hammer IN his hands; the hammer
 *                    leaves as his arms come over and spins up out of the screen.
 *   STOP     .17-.30 the raised-palm STOP pose from the Hammer Time fight (ht27 boss
 *                    12-15, with the hammer lifted out of his hand: he just threw it),
 *                    and above him, in the stage font: "ENOUGH! I'LL SHOW YOU REAL POWER!" 
 *   READY    .30-.38 he plants himself and sinks into the power stance (rage 0 -> 2).
 *   CHARGE   .38-.92 he holds the stance and SHAKES, harder and harder, rising slowly
 *                    through rage 2 -> 6; the black armour burns red one hard step at a
 *                    time; red lightning strikes the ground AROUND him and blows up,
 *                    closing in, faster and faster, until it is striking HIM.
 *   RELEASE  .92-1   the final strike straight down his centre: full red, the burst,
 *                    and he roars arms-out (rage 7 -> 12).
 *   Above him through CHARGE and RELEASE: "SUPER SAIYAN RAGE MODE ACTIVATED!" 
 *
 * Mike, in order: "please fix our lightning effects and red rage forming. Its very
 * janky atm" / "why is he glowing when he throws the hammer? ... the hammer should
 * anchor with his arm" / "We still need him to recoup, pose to get ready to charge,
 * then begin to shake and slowly charge up and do this animation. the lightning should
 * also strike around him and blow up."
 * Nothing glows until the CHARGE: no rim, no lit, no cores, no swirl before it.
 * Load after chronos_transform_1025.js and chronos_kame_1025.js. */
const C45 = { draw: hammerBossDraw, events: [] };
const C45_BEAT = { throwEnd: .17, recoupEnd: .30, readyEnd: .38, chargeEnd: .80 };
/* the release holds 1.44 s (u .80-1): white flash, then the glow fades out of him;
 * after the charge the aura carries on and fades over C45_AFTER s on the settled form */
const C45_AFTER = 1.4;
const C45_STRIKE = { n: 26, life: .16, width: 34 };
/* the body points a strike lands on late in the charge, as fractions of the pose's ink bounds */
const C45_TARGETS = [[.50, .06], [.22, .24], [.78, .24], [.12, .52], [.88, .52], [.50, .30]];

function c45Log(type, data) { C45.events.push({ type, t: efxClock, ...(data || {}) }); if (C45.events.length > 240) C45.events.shift(); }
const c45Ease = v => v * v * (3 - 2 * v);
/* world point on a C29 pose: bounds are native px, drawn around the pivot by b20Image */
function c45Point(b, q, fx, fy) {
  const a = q.a, k = q.k || 1, B = a.bounds || [0, 0, a.w, a.h], pv = a.pivot;
  return { x: b.x + (B[0] + (B[2] - B[0]) * fx - pv[0]) * k, y: b.y + (B[1] + (B[3] - B[1]) * fy - pv[1]) * k };
}
/* charge progress 0..1 */
function c45Prog(u) { return clamp((u - C45_BEAT.readyEnd) / (C45_BEAT.chargeEnd - C45_BEAT.readyEnd), 0, 1); }
/* strike n (1-based) lands at this u: the gaps shrink, so they come faster and faster */
function c45StrikeU(n) { const B = C45_BEAT; return B.readyEnd + (B.chargeEnd - B.readyEnd) * (1 - Math.pow(1 - Math.min(1, (n - 1) / C45_STRIKE.n), 1.6)); }
function c45StrikeCount(u) { if (u < C45_BEAT.readyEnd) return 0; let n = 0; while (n < C45_STRIKE.n && c45StrikeU(n + 1) <= u) ++n; return n; }

/* ------------------------------------------------------------------ THROW */
/* HAMMER_THROW_REEL rows are [sx, sy, sw, sh, pivotX, pivotY, headX, headY]; the
 * pivot is his chest core, as in the stock hammerChromiumPoseDraw. Frames:
 * 1 idle grip, 2 crouch, 3 wind-up, 4 swung back overhead, 5 swung over,
 * 6 arm thrown out (hand empty), 7 empty stand. */
const C45_REEL_KEY = 'arch_hammer_throw_0926';
const C45_THROW = { release: .135, fly: .20 };
const C45_THROW_FRAMES = [[1, .03], [2, .06], [3, .085], [4, .11], [5, .135], [6, .17]];
/* his idle plate draws the figure at .57 of this reel (the stock scale); the C29
 * banks after it are authored smaller, so he settles to .43 while his arm is out */
const C45_REEL_K = .57, C45_REEL_K_END = .43;
function c45ThrowFrame(u) { for (const [f, until] of C45_THROW_FRAMES) if (u < until) return f; return 6; }
function c45ReelK(u) { return lerp(C45_REEL_K, C45_REEL_K_END, c45Ease(clamp((u - C45_THROW.release) / (C45_BEAT.throwEnd - C45_THROW.release), 0, 1))); }
function c45ReelDraw(b, u) {
  if (typeof HAMMER_THROW_REEL === 'undefined' || !XART.rdy(C45_REEL_KEY)) return false;
  const r = HAMMER_THROW_REEL[c45ThrowFrame(u)], k = c45ReelK(u), im = XART.get(C45_REEL_KEY);
  /* as he shrinks after the release his feet drop to where the poses after him stand (b.y + 150) */
  const oy = 38 * c45Ease(clamp((u - C45_THROW.release) / (C45_BEAT.throwEnd - C45_THROW.release), 0, 1));
  const x = b.x + (r[0] - r[4]) * k, y = b.y + (r[1] - r[5]) * k + oy;
  ctx.save(); ctx.imageSmoothingEnabled = false;
  ctx.drawImage(im, r[0], r[1], r[2], r[3], x, y, r[2] * k, r[3] * k);
  if (b.flash > 0) { ctx.globalAlpha = Math.min(.85, b.flash / .12); ctx.drawImage(xartTint(C45_REEL_KEY, '#ffffff', 1), r[0], r[1], r[2], r[3], x, y, r[2] * k, r[3] * k); }
  ctx.restore();
  return true;
}
function c45ReelHead(b, f, k) { const r = HAMMER_THROW_REEL[f]; return { x: b.x + (r[6] - r[4]) * k, y: b.y + (r[7] - r[5]) * k }; }
/* the release: from where the head was on the last frame he held it, up and out of the top,
 * as C35's detached flight sprite (the same 0926 art family) at the reel's pixel scale */
function c45ToolFlight(b, u, C) {
  const T = C45_THROW;
  if (u < T.release || u > T.release + T.fly || typeof c35Tool !== 'function') return;
  if (!C.c45From) { C.c45From = c45ReelHead(b, 5, C45_REEL_K); shake = Math.max(shake, 6); c45Log('release'); }
  const p = (u - T.release) / T.fly, e = 1 - (1 - p) * (1 - p);
  const from = C.c45From, to = { x: from.x + 40, y: viewTopY() - 220 };
  c35Tool({ x: lerp(from.x, to.x, e), y: lerp(from.y, to.y, e) }, Math.PI * 3 / 4 + p * Math.PI * 6, 0, lerp(C45_REEL_K / .72, .45, p));
}
/* warm the reel with the stage, so the first throw frame is never a fallback pose */
if (typeof stageLoadBegin === 'function') { const base = stageLoadBegin; stageLoadBegin = function (n, keys) { return base.call(this, n, [...(keys || []), ...(n === 5 ? [C45_REEL_KEY] : [])]); }; }

/* ------------------------------------------------------------------- STOP */
/* the Hammer Time raised-palm STOP frames (ht27 boss 12-15) with the hammer lifted out
 * of his hand: built by _BUILD_SOURCE/build_stop_empty_1026.py. 4 cells of 314 px,
 * the source frames' own pivots [x, footY]. */
const C45_STOP_KEY = 'c45_stop_empty';
XART._src[C45_STOP_KEY] = 'assets/game/levels/stage_05/boss/chronos_rageform_1026/stop_empty.png';
const C45_STOP_PIV = [[174, 228], [167, 229], [153, 229], [147, 230]];
const C45_STOP_S = .74, C45_STOP_FOOT = 150;   /* figure ~207 px, feet where the C29 poses stand */
function c45StopDraw(b, u) {
  if (!XART.rdy(C45_STOP_KEY)) return false;
  const i = Math.min(3, Math.floor((u - C45_BEAT.throwEnd) / (C45_BEAT.recoupEnd - C45_BEAT.throwEnd) * 4)), P = C45_STOP_PIV[i], s = C45_STOP_S;
  ctx.save(); ctx.imageSmoothingEnabled = false;
  ctx.drawImage(XART.get(C45_STOP_KEY), i * 314, 0, 314, 314, b.x - P[0] * s, b.y + C45_STOP_FOOT - P[1] * s, 314 * s, 314 * s);
  ctx.restore();
  return true;
}
/* the lines, in the stage font, above him: typed on in hard steps, then held */
const C45_LINE_STOP = ['ENOUGH!', "I'LL SHOW YOU REAL POWER!"], C45_LINE_RAGE = ['SUPER SAIYAN', 'RAGE MODE ACTIVATED!'];
/* two lines, typed on together in hard steps (40 characters a second), the first larger */
function c45Line(b, lines, t, col) {
  if (typeof hamaTextDraw !== 'function') return;
  let n = Math.floor(t * 40);
  if (n <= 0) return;
  const y0 = Math.max(viewTopY() + 96, b.y - 170);
  for (let i = 0; i < lines.length && n > 0; ++i) {
    const L = lines[i], k = Math.min(L.length, n); n -= L.length;
    hamaTextDraw(L.slice(0, k), b.x, y0 + i * 32, i === 0 ? 30 : (L.length > 22 ? 19 : 24), col, true);
  }
}
if (typeof stageLoadBegin === 'function') { const base = stageLoadBegin; stageLoadBegin = function (n, keys) { return base.call(this, n, [...(keys || []), ...(n === 5 ? [C45_STOP_KEY] : [])]); }; }

/* --------------------------------------------------------- RECOUP / READY */
/* which C29 pose he wears, by u */
function c45Pose(u) {
  const B = C45_BEAT, NR = C29_ART.banks.rage_regular.length;
  if (u < .225) return { bank: 'stun', f: u < .19 ? 0 : 1 };        /* staggers, then hunches over */
  if (u < .27) return { bank: 'stun', f: 1, breathe: true };          /* catching his breath */
  if (u < B.recoupEnd) return { bank: 'recall', f: u < .285 ? 3 : 4 }; /* stands back up */
  if (u < B.readyEnd) return { bank: 'rage', f: Math.min(2, Math.floor((u - B.recoupEnd) / (B.readyEnd - B.recoupEnd) * 3)) };
  if (u < B.chargeEnd) return { bank: 'rage', f: 2 + Math.floor(c45Prog(u) * 4.999) };   /* 2..6, slowly */
  return { bank: 'rage', f: Math.min(9, 7 + Math.floor((u - B.chargeEnd) / .06 * 2)) };   /* roars arms-out, then HOLDS the pose */
}
/* how hard he is shaking (px), in hard steps; none before the charge */
function c45ShakeAmp(u) {
  if (u < C45_BEAT.readyEnd) return 0;
  if (u >= C45_BEAT.chargeEnd) return 0;
  return 1 + Math.floor(c45Prog(u) * 5);   /* 1..5 px */
}

/* ------------------------------------------------------------------- BODY */
function c45Body(b, u, C) {
  if (u < C45_BEAT.throwEnd && c45ReelDraw(b, u)) return null;
  if (u >= C45_BEAT.throwEnd && u < C45_BEAT.recoupEnd && c45StopDraw(b, u)) return null;
  const P = c45Pose(u), base = c29Pose(P.bank, P.f, 'regular');
  if (!base || !base.a) return null;
  let dx = 0, dy = 0;
  if (P.breathe) dy = Math.floor((Math.sin((u - .225) * CG_SSJ * 7) + 1) * 1.5);   /* heaving breaths, in whole px */
  const A = c45ShakeAmp(u);
  if (A) { const t = Math.floor(efxClock * 30); dx = ((t * 73) % (2 * A + 1)) - A; dy = ((t * 31) % (2 * A + 1)) - A; }   /* new jitter every frame, hard px */
  const q = { ...base, k: 1 }, L = CG.ladder;
  /* the red burns in one hard ladder step at a time through the charge, full at the release */
  const red = u >= C45_BEAT.chargeEnd ? 1 : u < C45_BEAT.readyEnd ? 0 : L[Math.min(5, Math.floor(c45Prog(u) * 6))];
  const qr = P.bank === 'rage' ? c29Pose('rage', P.f, 'red') : null;
  /* strikes: a 2-frame half white; the release: full white, held, then fading out of him in ladder steps */
  let flash = C.c45Flash > 0 ? .06 : 0;
  if (u >= C45_BEAT.chargeEnd) { const w = 1 - clamp((u - C45_BEAT.chargeEnd - .03) / .14, 0, 1); flash = .12 * L[Math.round(w * 5)] / .95; }
  ctx.save(); ctx.translate(dx, dy);
  if (red < 1 || !qr) b20Image(q.a, b.x, b.y, 1, 0, flash);
  if (qr && red > 0 && XART.rdy(qr.a.key)) { ctx.save(); ctx.globalAlpha = red; b20Image(qr.a, b.x, b.y, 1, 0, red >= 1 ? flash : 0); ctx.restore(); }
  ctx.restore();
  return q;
}

/* ---------------------------------------------------------------- STRIKES */
/* strike n: early ones hit the ground around him (closing in), later ones alternate onto
 * him, and the last few are all on him */
function c45StrikeTarget(b, q, n) {
  const prog = (n - 1) / C45_STRIKE.n;
  const onHim = prog > .82 || (prog > .45 && n % 2 === 0);
  if (onHim) { const T = C45_TARGETS[n % C45_TARGETS.length]; return { body: T, ground: false }; }
  const ang = n * 2.399, r = lerp(200, 78, prog), foot = c45Point(b, q, .5, 1).y;   /* golden-angle scatter, shrinking ring */
  return { pt: { x: b.x + Math.cos(ang) * r, y: foot - 6 + Math.sin(ang) * r * .32 }, ground: true };
}
function c45Strikes(b, u, C, q) {
  const n = c45StrikeCount(u), top = viewTopY() - 10;
  C.c45Live = C.c45Live || [];
  while ((C.c45N || 0) < n) {
    const k = C.c45N = (C.c45N || 0) + 1, T = c45StrikeTarget(b, q, k);
    const at = T.ground ? T.pt : c45Point(b, q, T.body[0], T.body[1]);
    C.c45Live.push({ k, T, u0: c45StrikeU(k), x0: at.x + (((k * 37) % 11) - 5) * 7 });
    shake = Math.max(shake, 4 + Math.min(7, k * .3));
    if (T.ground) {
      /* it blows up where it lands */
      if (typeof explode === 'function') explode(at.x, at.y, 30 + 30 * c45Prog(u), 'red', null, null, null, null, k % 3 !== 1);
      else if (typeof fxBurst === 'function') fxBurst(at.x, at.y, 40, { color: '#ff5a2a', rings: 1, chunks: 0 });
    } else {
      C.c45Flash = 2 / 60;
      if (typeof fxBurst === 'function') fxBurst(at.x, at.y, 34, { color: '#ff5a2a', rings: 1, chunks: 0 });
    }
    if (k % 3 === 1 && typeof c33Sound === 'function') c33Sound('thunder', b);
    c45Log('strike', { n: k, ground: T.ground });
  }
  C.c45Live = C.c45Live.filter(S => (u - S.u0) * CG_SSJ < C45_STRIKE.life);
  for (const S of C.c45Live) {
    const age = (u - S.u0) * CG_SSJ, st = Math.min(3, Math.floor(age / C45_STRIKE.life * 4)), al = [1, .95, .74, .32][st];
    const at = S.T.ground ? S.T.pt : c45Point(b, q, S.T.body[0], S.T.body[1]);
    cgBolt({ x: S.x0, y: top }, at, efxClock + S.k * .13, C45_STRIKE.width, al);
    if (st < 2) cgBolt({ x: S.x0, y: top }, at, efxClock + S.k * .13 + .05, C45_STRIKE.width * .55, al);
  }
  return n;
}

/* ------------------------------------------------------------- SSJ AURA */
/* Mike: "he should be more visible in this pose, its critical to the super saiyan way
 * and more energy emits off him like an energy aura". The aura is built from his OWN
 * silhouette (the pose he is wearing), dilated into three hard-edged layers, gold
 * inside, orange, red outside, drawn BEHIND him and stretched upward from his feet;
 * each layer licks up in flame tongues that step every frame like a 16-bit fire cycle.
 * No blur, no sprite overlay. */
const C45_AURA = [{ r: 3, col: '#ffe680', a: .55 }, { r: 6, col: '#ffa024', a: .42 }, { r: 10, col: '#ff3a10', a: .30 }];
const C45_AURA_PAD = 20;
function c45AuraMask(key, r, col) {
  C45.aura = C45.aura || new Map();
  const id = key + '|' + r + '|' + col;
  if (C45.aura.has(id)) return C45.aura.get(id);
  if (!XART.rdy(key)) return null;
  const im = XART.get(key), P = C45_AURA_PAD, W = im.width + P * 2, H = im.height + P * 2;
  const c = document.createElement('canvas'); c.width = W; c.height = H; const g = c.getContext('2d');
  g.imageSmoothingEnabled = false;
  for (let i = 0; i < 24; ++i) { const a = i / 24 * Math.PI * 2; g.drawImage(im, P + Math.round(Math.cos(a) * r), P + Math.round(Math.sin(a) * r)); }
  g.drawImage(im, P, P);
  g.globalCompositeOperation = 'source-in'; g.fillStyle = col; g.fillRect(0, 0, W, H);
  C45.aura.set(id, c); if (C45.aura.size > 90) C45.aura.delete(C45.aura.keys().next().value);
  return c;
}
/* strength 0..1: it builds through the end of the charge and blazes in the release */
function c45Aura(b, a, strength) {
  if (!a || strength <= 0) return;
  const L = CG.ladder, f = Math.floor(efxClock * 12), foot = b.y + (a.bounds ? a.bounds[3] - a.pivot[1] : 150);
  /* normal blending, outer layer first: additive stacking of nine copies summed to a white blob */
  ctx.save(); ctx.imageSmoothingEnabled = false;
  for (let li = C45_AURA.length - 1; li >= 0; --li) {
    const A = C45_AURA[li], m = c45AuraMask(a.key, A.r, A.col);
    if (!m) continue;
    const x = b.x - a.pivot[0] - C45_AURA_PAD, y = b.y - a.pivot[1] - C45_AURA_PAD;
    for (let t = 0; t < 2; ++t) {
      const ph = (f + li + t) % 3, stretch = 1.03 + .05 * ph + .06 * t;   /* tongues: the second copy taller, stepping */
      ctx.globalAlpha = A.a * strength * (t ? .55 : 1) * (ph === 0 ? 1 : .82);   /* hard flicker steps */
      ctx.save(); ctx.translate(0, foot); ctx.scale(1, stretch); ctx.translate(0, -foot);
      ctx.drawImage(m, x, y - 5 * t * (1 + ph));
      ctx.restore();
    }
  }
  ctx.restore();
}

/* ------------------------------------------------------------------- DRAW */
hammerBossDraw = function (b) {
  if (!c25Own(b) || b.dead || !b._hammer._hf22Charge || typeof cgWithGlow !== 'function') return C45.draw.apply(this, arguments);
  const C = b._hammer._hf22Charge, u = cgChargeU(b), M = cgMode(b), B = C45_BEAT;
  C.c45Flash = Math.max(0, (C.c45Flash || 0) - 1 / 60);
  ctx.save();
  if (u < B.readyEnd) {
    /* THROW, RECOUP, READY: his plain body, no glow, no swirl */
    c45Body(b, u, C);
    c45ToolFlight(b, u, C);
    ctx.restore();
    if (u >= B.throwEnd) c45Line(b, C45_LINE_STOP, (u - B.throwEnd) * CG_SSJ, '#ffffff');
    C45.last = { u, n: 0, beat: u < B.throwEnd ? 'throw' : u < B.recoupEnd ? 'stop' : 'ready' };
    return;
  }
  /* CHARGE and RELEASE */
  CG.noRings = true;
  try { cgDrive(b, M); } finally { CG.noRings = false; }
  try { cgSwirl(b, M, false); } catch (e) { c45Log('swirl-error', { e: String(e) }); }
  /* the aura, behind him: builds from 60% of the charge, blazes in the release */
  { const P = c45Pose(u), qa = c29Pose('rage', P.f, 'red'), st = u >= B.chargeEnd ? 1 - .35 * clamp((u - B.chargeEnd) / (1 - B.chargeEnd), 0, 1) : c45Ease(clamp((c45Prog(u) - .6) / .4, 0, 1)) * .8;
    if (qa && qa.a) c45Aura(b, qa.a, st); }
  let q = null;
  cgWithGlow(b, M, () => { q = c45Body(b, u, C); }, false);
  let n = 0;
  if (q) n = c45Strikes(b, u, C, q);
  /* the final strike: straight down his centre, the form locks red */
  if (u >= B.chargeEnd) {
    const top = viewTopY() - 10;
    if (!C.c45Final) {
      /* he must stay VISIBLE in this pose: a 3-frame flash and rings, not a white disc */
      C.c45Final = true; b._hammer._c45Burst = true; b._hammer._c45After = null;
      if (typeof chronosRageRings === 'function') chronosRageRings(b);
      else if (typeof spawnShockRing === 'function') { spawnShockRing(b.x, b.y, 150, 'comet'); spawnShockRing(b.x, b.y, 230, 'comet'); }
      if (typeof fxBurst === 'function') fxBurst(b.x, b.y, 120, { color: '#ff3a18', rings: 0, chunks: 0, sparks: 48 });
      shake = Math.max(shake, 18); flashScreen = Math.max(flashScreen || 0, .18);
      if (typeof c33Sound === 'function') c33Sound('thunder', b);
      c45Log('final');
    }
    const p = (u - B.chargeEnd) / (1 - B.chargeEnd), st = Math.min(3, Math.floor(p * 4));
    const at = { x: b.x, y: b.y + 40 };
    cgBolt({ x: b.x, y: top }, at, efxClock, 64, [1, 1, .8, .45][st]);
    cgBolt({ x: b.x, y: top }, at, efxClock + .07, 30, [1, .9, .6, .3][st]);
  }
  try { cgSwirl(b, M, true); } catch (e) { c45Log('swirl-error', { e: String(e) }); }
  /* flickers red/white in hard steps while he charges, solid red once it lands */
  c45Line(b, C45_LINE_RAGE, (u - B.readyEnd) * CG_SSJ, u >= B.chargeEnd ? '#ff3a18' : (Math.floor(efxClock * 8) % 2 ? '#ffffff' : '#ff5030'));
  ctx.restore();
  C45.last = { u, n, beat: u < B.chargeEnd ? 'charge' : 'release', final: u >= B.chargeEnd };
};
/* AFTER the charge: the aura keeps burning off his settled rage form and fades out
 * over C45_AFTER s in hard steps, so the transformation eases into the new form */
(function () {
  const base = hammerBossDraw;
  hammerBossDraw = function (b) {
    const h = b && b._hammer;
    if (!h || !c25Own(b) || b.dead || h._hf22Charge || !h._c45Burst || h._c45AfterDone) return base.apply(this, arguments);
    if (h._c45After == null) h._c45After = efxClock;
    const t = (efxClock - h._c45After) / C45_AFTER;
    if (t >= 1) { h._c45AfterDone = true; return base.apply(this, arguments); }
    const q = ha21Blue(b), k = .9 * CG.ladder[Math.max(0, Math.round((1 - t) * 5))] / .95;
    if (q && q.a && k > 0) try { c45Aura(b, q.a, k); } catch (e) { c45Log('after-error', { e: String(e) }); }
    const r = base.apply(this, arguments);
    /* crossfade: the held release pose dissolves into the settled form over the first .6 s, in ladder steps */
    const x = 1 - clamp((efxClock - h._c45After) / .6, 0, 1), rel = c29Pose('rage', 9, 'red');
    if (x > 0 && rel && rel.a) { ctx.save(); ctx.globalAlpha = CG.ladder[Math.round(x * 5)] / .95; b20Image(rel.a, b.x, b.y, 1, 0, 0); ctx.restore(); }
    return r;
  };
})();
window.BOF_CHRONOS_RAGEFORM = C45;
