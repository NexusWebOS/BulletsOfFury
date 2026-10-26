"use strict";
/* =============================================================================
 * Chronos glow pass (Claude, October 25): 16-bit pixel glow and transformation
 * effects for the Stage 5 boss in every form. HE glows; nothing big is drawn
 * around him (Mike: "I meant to make HIM glow, not put that giant glow/aura
 * around him").
 *
 * The pixel glow here is the 1015 method (docs/PIXEL_GLOW_1015.md): light that
 * comes off the art's own pixels in HARD one-pixel steps, its brightness walking
 * a fixed ladder on the game clock like a palette cycle. No blur, no soft fade,
 * no extra silhouette. Everything is traced from the exact plate the fight
 * draws this frame (offset-draw dilation, 'source-in' recolour, an SVG colour
 * matrix for the cores), so it follows every pose. Nothing reads pixels back,
 * so it also runs from file://.
 *
 *   rim     one-pixel shells just outside his outline that pulse outward
 *   lit     his armour lit from within in the form's colour, on the ladder
 *   cores   the chest core and the hammer core (the plate's own vivid blue
 *           light) breathe and throw hard light rings outward
 *   sweep   chromium plating sweep / periodic chrome glint
 *   drive   escalating shake through each transformation, bursts on landing
 *
 * Forms (read off the live fight state, never set here): regular (cold blue),
 * fr_activation (cyan, faster and brighter as the plating builds), chrome
 * (cyan/white + glint), rage charge (red, strobing faster and brighter in hard
 * steps), rage (red/orange/gold, fast). A hit flashes the rim white. Dead or not
 * Chronos: draws exactly as before. Timing, damage, collision and state are
 * untouched.
 * ===========================================================================*/
const CG = {
  ladder: [0, .16, .32, .52, .74, .95],     /* the 1015 brightness steps */
  pal: {   /* ring colours, innermost first */
    regular: ['#9fe6ff', '#3fa8ff', '#1846a8'],
    chrome:  ['#ffffff', '#c8faff', '#6fe0ff', '#2a90ff', '#1040b0'],
    rage:    ['#fff6b0', '#ffd040', '#ffa030', '#ff6a18', '#ff3a10', '#d81808'],   /* no dark reds: added over blue space they read purple */
    hit:     ['#ffffff', '#ffffff', '#ffe0e0'],
  },
  cache: new Map(), wm: new WeakMap(), wmE: new WeakMap(), base: null,
  corePal: ['#b4f4ff', '#58d4ff', '#2a98ff', '#1a64e6', '#1040b0'],   /* core rings, innermost first */ under: null, body: null, prev: {}, events: [],
};
function cgWarm() { return true; }   /* nothing to load: every glow is traced from his own plates */
function cgLog(type, data = {}) { CG.events.push({ type, time: efxClock, ...data }); if (CG.events.length > 200) CG.events.shift(); }

/* The live form, read from Codex's controllers. */
function cgMode(b) {
  const h = b._hammer;
  if (h._hf22Charge) return { mode: 'ragecharge', k: clamp((h._hf22Charge.t || 0) / 1.8, 0, 1) };
  if (h._hf22Red) return { mode: 'rage', k: 1 };
  if (h.state === 'fr_activation') {
    const A = typeof C27_ARMOR !== 'undefined' ? C27_ARMOR : { raise: .65, plate: 2.9, end: 3.35 };
    return { mode: 'activation', k: clamp(((h.t || 0) - A.raise) / (A.plate - A.raise), 0, 1), t: h.t || 0, plate: A.plate };
  }
  if (typeof c26Material === 'function' && c26Material(b) === 'chrome') return { mode: 'chrome', k: 1 };
  return { mode: 'regular', k: 0 };
}
function cgActive(b) {
  return b && b._hammer && !b.dead && typeof c25Own === 'function' && c25Own(b);
}

/* ------------------------------------------------------------ silhouette rings
 * Dilating the plate's alpha by offset-draws: d(r+1) = d(r) drawn at its 8
 * neighbours. Ring r is d(r) minus d(r-1), filled with one flat colour: a hard
 * one-pixel step, never a gradient. */
function cgCanvas(w, h) { const c = document.createElement('canvas'); c.width = w; c.height = h; return c; }
const CG_N8 = [[1, 0], [-1, 0], [0, 1], [0, -1], [1, 1], [1, -1], [-1, 1], [-1, -1]];
function cgRings(im, sx, sy, sw, sh, pal, keyId) {
  if (keyId && !XART.rdy(keyId)) keyId = null;
  const P = pal.length + 1, ck = keyId ? keyId + '|' + sx + ',' + sy + ',' + sw + ',' + sh + '|' + pal.join() : null;
  if (ck && CG.cache.has(ck)) { const v = CG.cache.get(ck); CG.cache.delete(ck); CG.cache.set(ck, v); return v; }
  /* Unnamed per-frame canvases (the red rage plates): keep a trace for a
   * quarter second on the canvas object itself, then re-trace in case its
   * contents were redrawn. */
  const wk = sx + ',' + sy + ',' + sw + ',' + sh + '|' + pal.join();
  if (!ck) { const e = CG.wm.get(im); if (e && e.k === wk && efxClock - e.t < .25 && efxClock >= e.t) return e.v; }
  const W = Math.ceil(sw) + P * 2, H = Math.ceil(sh) + P * 2;
  let d = cgCanvas(W, H), g = d.getContext('2d');
  g.imageSmoothingEnabled = false;
  g.drawImage(im, sx, sy, sw, sh, P, P, sw, sh);
  const rings = [];
  for (let r = 0; r < pal.length; ++r) {
    const nd = cgCanvas(W, H), ng = nd.getContext('2d');
    ng.imageSmoothingEnabled = false;
    for (const [dx, dy] of CG_N8) ng.drawImage(d, dx, dy);
    ng.drawImage(d, 0, 0);
    /* the ring = new dilation minus the previous one, in one flat colour */
    const ring = cgCanvas(W, H), rg = ring.getContext('2d');
    rg.drawImage(nd, 0, 0);
    rg.globalCompositeOperation = 'destination-out'; rg.drawImage(d, 0, 0);
    rg.globalCompositeOperation = 'source-in'; rg.fillStyle = pal[r]; rg.fillRect(0, 0, W, H);
    rings.push(ring);
    d = nd;
  }
  const v = { rings, pad: P };
  if (ck) { CG.cache.set(ck, v); if (CG.cache.size > 48) CG.cache.delete(CG.cache.keys().next().value); }
  else CG.wm.set(im, { k: wk, t: efxClock, v });
  return v;
}
/* A white silhouette of the plate clipped to a horizontal band: the plating
 * sweep and the chrome glint. */
function cgBand(im, sx, sy, sw, sh, y0, y1) {
  const c = cgCanvas(Math.ceil(sw), Math.ceil(sh)), g = c.getContext('2d');
  g.imageSmoothingEnabled = false;
  g.drawImage(im, sx, sy, sw, sh, 0, 0, sw, sh);
  g.globalCompositeOperation = 'source-in';
  g.fillStyle = '#ffffff';
  g.fillRect(0, Math.floor(y0 * sh), sw, Math.max(1, Math.floor((y1 - y0) * sh)));
  return c;
}

function cgStep(rate, lo = 0, hi = 5) {   /* a ladder step on the game clock */
  const n = hi - lo + 1, i = Math.floor(efxClock * rate) % (2 * n - 2);
  return CG.ladder[lo + (i < n ? i : 2 * n - 2 - i)];
}

/* --------------------------------------------------------- per-form effects
 * Mike (Oct 25): "I meant to make HIM glow, not put that giant glow/aura around
 * him." So there is no aura sprite: the light is his own silhouette rim
 * (hard one-pixel shells that pulse outward, one step at a time), his armour
 * lit from within on the ladder, and the pixel-animated cores. */
const CG_PULSE = [.95, .74, .52, .32, .16, 0, 0, 0];

/* Before the body plate: the rim shells, outside his outline. */
function cgUnder(b, M, im, sx, sy, sw, sh, dx, dy, dw, dh) {
  const h = b._hammer, ky = dw / sw;
  let pal = null, rimA = 0, rate = 6, lit = 0, litCol = '#000';
  switch (M.mode) {
  case 'regular':
    pal = CG.pal.regular; rimA = cgStep(5, 1, 3); rate = 5;
    lit = .03 + cgStep(4, 0, 2) * .10; litCol = '#2a70ff';   /* low: the cores carry the light; the plating stays dark steel */
    break;
  case 'chrome':
    pal = CG.pal.chrome; rimA = cgStep(9, 3, 5); rate = 9;
    lit = .04 + cgStep(7, 0, 3) * .12; litCol = '#4fd0ff';   /* low: chrome must still read as silver */
    break;
  case 'activation':
    pal = CG.pal.chrome; rimA = .55 + .45 * M.k; rate = 12 + 14 * M.k;
    lit = (.04 + .14 * Math.floor(M.k * 6) / 6) * (Math.floor(efxClock * (8 + 16 * M.k)) % 2 ? 1 : .5); litCol = '#4fc8ff';
    break;
  case 'ragecharge': {
    pal = CG.pal.rage;
    /* ignition: he flashes on and off faster and faster, brighter each step */
    const tempo = 6 + 26 * M.k, on = Math.floor(efxClock * tempo) % 2 === 0 || M.k > .82;
    rimA = on ? .6 + .4 * M.k : .2; rate = 12 + 12 * M.k;
    lit = on ? .05 + .12 * Math.floor(M.k * 6) / 6 : .03;   /* low: the red pose itself burns in now (chronos_rageform_1026); more washes it to salmon */ litCol = '#ff3a10';
    break; }
  case 'rage':
    pal = CG.pal.rage; rimA = cgStep(16, 4, 5); rate = 14;
    lit = .22 + cgStep(12, 0, 3) * .40; litCol = '#ff4418';
    break;
  }
  if (h._cgFlare > 0) { rimA = 1; lit = Math.max(lit, .55 * h._cgFlare); }
  if (b.flash > 0) { pal = CG.pal.hit; rimA = 1; }
  CG.body = { im, sx, sy, sw, sh, dx, dy, dw, dh, ky, lit, litCol, m: ctx.getTransform() };   /* the plate's own transform: cgOver runs after the draw has restored it */
  if (!pal || rimA <= .01) return;
  const R = cgRings(im, sx, sy, sw, sh, pal, im.__k || null), step = Math.floor(efxClock * rate);
  ctx.save();
  ctx.imageSmoothingEnabled = false;
  ctx.shadowBlur = 0; ctx.filter = 'none';
  ctx.globalCompositeOperation = 'lighter';
  const x = dx - R.pad * ky, y = dy - R.pad * ky;
  for (let r = 0; r < R.rings.length; ++r) {
    /* the inner shell always holds some light; outer shells carry the pulse */
    const a = rimA * Math.max(.78 - r * .13, CG_PULSE[((step - r) % 8 + 8) % 8]);
    if (a <= .01) continue;
    ctx.globalAlpha = Math.min(1, a);   /* absolute: the plate that triggered us may be a faint halo copy */
    ctx.drawImage(R.rings[r], x, y, R.rings[r].width * ky, R.rings[r].height * ky);
  }
  ctx.restore();
}

/* His armour lit from within: the plate's own silhouette in one colour, added. */
function cgLit(im, sx, sy, sw, sh, col, keyId) {
  const ck = keyId ? 'L|' + keyId + '|' + sx + ',' + sy + ',' + sw + ',' + sh + '|' + col : null;
  if (ck && CG.cache.has(ck)) return CG.cache.get(ck);
  const c = cgCanvas(Math.ceil(sw), Math.ceil(sh)), g = c.getContext('2d');
  g.imageSmoothingEnabled = false;
  g.drawImage(im, sx, sy, sw, sh, 0, 0, sw, sh);
  g.globalCompositeOperation = 'source-in'; g.fillStyle = col; g.fillRect(0, 0, sw, sh);
  if (ck) { CG.cache.set(ck, c); if (CG.cache.size > 64) CG.cache.delete(CG.cache.keys().next().value); }
  return c;
}

/* ------------------------------------------------------------- core glow
 * Mike (Oct 25): "make the hammer core and center core of his armor pixel
 * animate/glow". The cores are the plate's own vivid blue light. An SVG colour
 * matrix keeps a pixel only where blue clearly beats red (the cores, the hammer
 * energy and the small panel lamps; silver highlights, black metal and the red
 * rage plating all drop out), with a hard alpha threshold so the mask is crisp
 * pixels, not a soft blob. The filter runs on the GPU and nothing is read back,
 * so this still works from file://. The mask then:
 *   - brightens on the 1015 ladder (the core "breathes"),
 *   - throws hard one-pixel light rings that pulse outward from the cores one
 *     step at a time, like a 16-bit palette cycle.
 * Charging states speed the pulse up. */
(function () {
  if (document.getElementById('cg25emit')) return;
  const NS = 'http://www.w3.org/2000/svg', svg = document.createElementNS(NS, 'svg');
  svg.setAttribute('width', '0'); svg.setAttribute('height', '0');
  svg.style.position = 'absolute'; svg.style.left = '-9px';
  svg.innerHTML = '<filter id="cg25emit" color-interpolation-filters="sRGB" x="0" y="0" width="1" height="1">' +
    /* alpha = 2.0*B + 0.8*G - 2.2*R - 0.55, then a hard step at .25: blue and
     * cyan light including the white-cyan core centres; neutral silver, white
     * highlights, black metal and red plating stay out (measured off the
     * idle, chrome and rage plates) */
    '<feColorMatrix type="matrix" values="1 0 0 0 0  0 1 0 0 0  0 0 1 0 0  -2.2 0.8 2.0 0 -0.55"/>' +
    '<feComponentTransfer><feFuncA type="discrete" tableValues="0 1 1 1"/></feComponentTransfer>' +
    '<feComposite in2="SourceAlpha" operator="in"/></filter>' +
    /* near-white light: the white-hot centres the blue test leaves as holes */
    '<filter id="cg25bright" color-interpolation-filters="sRGB" x="0" y="0" width="1" height="1">' +
    '<feColorMatrix type="matrix" values="1 0 0 0 0  0 1 0 0 0  0 0 1 0 0  1 1 1 0 -2.45"/>' +
    '<feComponentTransfer><feFuncA type="discrete" tableValues="0 1"/></feComponentTransfer>' +
    '<feComposite in2="SourceAlpha" operator="in"/></filter>';
  (document.body || document.documentElement).appendChild(svg);
})();
function cgEmissive(im, sx, sy, sw, sh, keyId) {
  if (keyId && !XART.rdy(keyId)) keyId = null;
  const ck = keyId ? 'E|' + keyId + '|' + sx + ',' + sy + ',' + sw + ',' + sh : null;
  if (ck && CG.cache.has(ck)) return CG.cache.get(ck);
  if (!ck) { const e = CG.wmE.get(im); if (e && efxClock - e.t < .25 && efxClock >= e.t) return e.v; }
  const P = 7, W = Math.ceil(sw) + P * 2, H = Math.ceil(sh) + P * 2;
  const m = cgCanvas(W, H), g = m.getContext('2d');
  g.imageSmoothingEnabled = false;
  g.filter = 'url(#cg25emit)';
  g.drawImage(im, sx, sy, sw, sh, P, P, sw, sh);
  g.filter = 'none';
  /* fill the core centres: near-white pixels that sit within 3 px of blue light
   * (bright AND near-blue, by destination-in), so silver highlights stay out */
  {
    let grow = m;
    for (let r = 0; r < 3; ++r) {
      const nd = cgCanvas(W, H), ng = nd.getContext('2d');
      for (const [dx, dy] of CG_N8) ng.drawImage(grow, dx, dy);
      ng.drawImage(grow, 0, 0); grow = nd;
    }
    const hb = cgCanvas(W, H), bg = hb.getContext('2d');
    bg.imageSmoothingEnabled = false;
    bg.filter = 'url(#cg25bright)'; bg.drawImage(im, sx, sy, sw, sh, P, P, sw, sh); bg.filter = 'none';
    bg.globalCompositeOperation = 'destination-in'; bg.drawImage(grow, 0, 0);
    g.drawImage(hb, 0, 0);
  }
  /* the rings: dilate the mask, keep each new one-pixel shell in a flat colour */
  const rings = [];
  let d = m;
  for (let r = 0; r < CG.corePal.length; ++r) {
    const nd = cgCanvas(W, H), ng = nd.getContext('2d');
    ng.imageSmoothingEnabled = false;
    for (const [dx, dy] of CG_N8) ng.drawImage(d, dx, dy);
    ng.drawImage(d, 0, 0);
    const ring = cgCanvas(W, H), rg = ring.getContext('2d');
    rg.drawImage(nd, 0, 0);
    rg.globalCompositeOperation = 'destination-out'; rg.drawImage(d, 0, 0);
    rg.globalCompositeOperation = 'source-in'; rg.fillStyle = CG.corePal[r]; rg.fillRect(0, 0, W, H);
    rings.push(ring);
    d = nd;
  }
  /* the core itself, pushed toward white-cyan (added light, not a flat paint) */
  const hot = cgCanvas(W, H), hg = hot.getContext('2d');
  hg.drawImage(m, 0, 0);
  hg.globalCompositeOperation = 'source-in'; hg.fillStyle = '#5fd8ff';   /* added cyan light; white would flatten the hammer face into a sticker (1015) */ hg.fillRect(0, 0, W, H);
  /* the core's OWN lit pixels, cut out by the mask: added back as light, so the
   * hammer face's lightning and the reactor's rings brighten in their own colours */
  const self = cgCanvas(W, H), sg = self.getContext('2d');
  sg.imageSmoothingEnabled = false;
  sg.drawImage(im, sx, sy, sw, sh, P, P, sw, sh);
  sg.globalCompositeOperation = 'destination-in'; sg.drawImage(m, 0, 0);
  const dim = cgCanvas(W, H), dg = dim.getContext('2d');
  dg.drawImage(m, 0, 0); dg.globalCompositeOperation = 'source-in'; dg.fillStyle = '#0a2a90'; dg.fillRect(0, 0, W, H);
  /* the heart: the core's near-white centre only (the bright mask, before the rings) */
  const heart = cgCanvas(W, H), hrg = heart.getContext('2d');
  hrg.imageSmoothingEnabled = false;
  hrg.filter = 'url(#cg25bright)'; hrg.drawImage(im, sx, sy, sw, sh, P, P, sw, sh); hrg.filter = 'none';
  hrg.globalCompositeOperation = 'destination-in'; hrg.drawImage(m, 0, 0);
  hrg.globalCompositeOperation = 'source-in'; hrg.fillStyle = '#ffffff'; hrg.fillRect(0, 0, W, H);
  const v = { hot, rings, self, dim, heart, pad: P };
  if (ck) { CG.cache.set(ck, v); if (CG.cache.size > 64) CG.cache.delete(CG.cache.keys().next().value); }
  else CG.wmE.set(im, { t: efxClock, v });
  return v;
}
function cgCoreGlow(b, M, B) {
  const E = cgEmissive(B.im, B.sx, B.sy, B.sw, B.sh, B.im.__k || null), k = B.ky, L = CG.ladder;
  const fast = M.mode === 'activation' || M.mode === 'ragecharge';
  /* PIXEL GLOW (the 1015 method): the core's own pixels added back as light,
   * then hard one-pixel rings spilling past them; every brightness is a step of
   * the fixed ladder, walked on the game clock like a 16-bit palette cycle.
   * The core breathes up and down the ladder, and the spill swells outward one
   * ring per step and draws back in. No blur, no flat repaint, no overlay art. */
  const fps = fast ? 18 : M.mode === 'rage' ? 12 : 9;
  const t = Math.floor(efxClock * fps), cyc = 8, ph = t % cyc;
  const lvl = ph <= 4 ? ph : cyc - ph;                 /* 0 1 2 3 4 3 2 1: the swell */
  const flare = b.flash > 0 ? 1 : 0;
  ctx.save();
  ctx.imageSmoothingEnabled = false;
  ctx.globalCompositeOperation = 'lighter';
  const x = B.dx - E.pad * k, y = B.dy - E.pad * k, w = E.self.width * k, h = E.self.height * k;
  /* the bottom of the swell: the core dims a palette step toward deep blue
   * (source-over over its own mask), so the climb back up reads as light */
  if (lvl <= 1 && !flare) {
    ctx.globalCompositeOperation = 'source-over';
    ctx.globalAlpha = lvl ? L[3] : L[4];
    ctx.drawImage(E.dim, x, y, w, h);
    ctx.globalCompositeOperation = 'lighter';
  }
  /* the top of the swell: the core's own colours added back, then the white heart */
  if (lvl >= 2 || flare) {
    ctx.globalAlpha = L[Math.min(5, lvl + 1 + flare)];
    ctx.drawImage(E.self, x, y, w, h);
    if (lvl >= 3 || flare) { ctx.globalAlpha = L[lvl + flare >= 4 ? 5 : 4]; ctx.drawImage(E.heart, x, y, w, h); }
  }
  /* the spill: hard one-pixel rings past the core; ring r lights once the swell
   * reaches it, the newest ring brightest, each older one a step dimmer */
  const reach = lvl + (fast ? 1 : 0) + flare;
  for (let r = 0; r < Math.min(reach, E.rings.length); ++r) {
    ctx.globalAlpha = L[Math.max(1, 5 - r)];
    ctx.drawImage(E.rings[r], x, y, w, h);
  }
  ctx.restore();
}
/* The DETACHED hammer (throws, recalls, the boomerang, knockaways) is C35's
 * separate flight sprite, not part of his body plate, so its core gets the same
 * pixel glow here: the blit c35Tool makes is caught and glowed in place, under
 * the same transform, in step with his chest. */
(function () {
  if (typeof c35Tool !== 'function' || c35Tool.__cg) return;
  const base = c35Tool;
  c35Tool = function () {
    const b = typeof boss !== 'undefined' ? boss : null;
    if (!b || !cgActive(b)) return base.apply(this, arguments);
    let hit = null;
    const di = ctx.drawImage;
    ctx.drawImage = function (im) {
      const a = arguments;
      if (!hit && a.length >= 9 && im && im.__k === 'arch_hammer_flight_0926')
        hit = { im, sx: a[1], sy: a[2], sw: a[3], sh: a[4], dx: a[5], dy: a[6], dw: a[7], dh: a[8], m: ctx.getTransform(), alpha: ctx.globalAlpha };
      return di.apply(this, arguments);
    };
    let r;
    try { r = base.apply(this, arguments); } finally { ctx.drawImage = di; }
    if (hit && hit.alpha > .05) {
      try {
        ctx.save(); ctx.setTransform(hit.m);
        cgCoreGlow(b, cgMode(b), { ...hit, ky: hit.dw / hit.sw });
        CG.toolGlows = (CG.toolGlows || 0) + 1;
      } catch (e) { cgLog('tool-glow-error', { e: String(e) }); }
      finally { ctx.restore(); }
    }
    return r;
  };
  c35Tool.__cg = true;
})();

/* After the body: the plating sweep / chrome glint over the armour, then the core glow. */
function cgOver(b, M) {
  const B = CG.body;
  if (!B) return;
  ctx.save();
  if (B.m) ctx.setTransform(B.m);
  try { cgOverBody(b, M, B); } finally { ctx.restore(); CG.body = null; }
}
function cgOverBody(b, M, B) {
  const h = b._hammer;
  let y0 = -1, a = 0;
  if (M.mode === 'activation' && M.k > 0 && M.k < 1) { y0 = M.k - .06; a = .55; }
  else if (M.mode === 'chrome') {
    const ph = (efxClock % 2.6) / .45;   /* a glint every 2.6 s, crossing in .45 s */
    if (ph < 1) { y0 = ph * 1.1 - .08; a = .42; }
  }
  if (B.lit > .01) {
    ctx.save();
    ctx.imageSmoothingEnabled = false;
    ctx.globalAlpha = Math.min(1, B.lit);
    ctx.globalCompositeOperation = 'lighter';
    ctx.drawImage(cgLit(B.im, B.sx, B.sy, B.sw, B.sh, B.litCol, B.im.__k || null), B.dx, B.dy, B.dw, B.dh);
    ctx.restore();
  }
  if (y0 > -1 && a > 0) {
    const band = cgBand(B.im, B.sx, B.sy, B.sw, B.sh, Math.max(0, y0), Math.min(1, y0 + .06));
    ctx.save();
    ctx.imageSmoothingEnabled = false;
    ctx.globalAlpha = a;
    ctx.globalCompositeOperation = 'lighter';
    ctx.drawImage(band, B.dx, B.dy, B.dw, B.dh);
    ctx.restore();
  }
  try { cgCoreGlow(b, M, B); } catch (e) { cgLog('core-error', { e: String(e) }); }
  void h;
}

/* Shakes, flashes and the power-up bursts. Runs once per drawn frame. */
function cgDrive(b, M) {
  const h = b._hammer, P = h._cgPrev || (h._cgPrev = {});
  if (h._cgFlare > 0) h._cgFlare = Math.max(0, h._cgFlare - 1 / 30);
  if (M.mode === 'ragecharge') {
    /* the ground trembles harder as the power builds, in hard steps */
    shake = Math.max(shake, 2 + Math.floor(M.k * 5) * 1.6);
    if (Math.floor(M.k * 6) !== P.rageStep) {
      P.rageStep = Math.floor(M.k * 6);
      flashScreen = Math.max(flashScreen || 0, .05 + .03 * P.rageStep);
      /* a power-up wave per step (not before the hammer is gone) */
      if (P.rageStep >= 2 && !CG.noRings && typeof spawnShockRing === 'function') {   /* the rage forming (c45) uses strikes instead */
        spawnShockRing(b.x, b.y, 90 + 22 * P.rageStep, 'comet');
        shake = Math.max(shake, 6 + 2 * P.rageStep);
        h._cgFlare = Math.max(h._cgFlare || 0, .35);
        cgLog('ssj-beat', { step: P.rageStep });
      }
    }
  }
  if (M.mode === 'activation' && M.k > 0) shake = Math.max(shake, 1 + Math.floor(M.k * 4) * 1.2);
  /* the moment a form locks in */
  if (M.mode === 'rage' && P.mode === 'ragecharge' && !h._c45Burst) {
    fxBurst(b.x, b.y, 170, { color: '#ff3a18', rings: 3 });
    shake = Math.max(shake, 22); flashScreen = Math.max(flashScreen || 0, .55); h._cgFlare = 1;
    cgLog('rage-burst');
  }
  if (P.mode === 'activation' && M.mode !== 'activation') {
    fxBurst(b.x, b.y, 140, { color: '#7fd8ff', rings: 2 });
    shake = Math.max(shake, 14); flashScreen = Math.max(flashScreen || 0, .40); h._cgFlare = .8;
    cgLog('chrome-burst');
  }
  P.mode = M.mode;
}


/* --------------------------------------------------------- red swirl bolts
 * Mike (Oct 25): "those electric lines should be palette swapped to red, and
 * only form when hes charging up and swirling around him." During the rage
 * charge his stock blue c25Bolt lines (the static "A" from his feet to over his
 * head, and the diagonal) are suppressed and replaced by the same lightning
 * sprite palette-swapped to red ('color' composite: hue from red, luminosity
 * from the art, so the white-hot cores stay white), running as arcs that orbit
 * him in rising rings. Each arc is split at the ellipse's near/far side so the
 * far half passes behind his body and the near half in front. More rings join
 * as the charge builds. Bolts outside the rage charge (hammer recovery,
 * chromium) keep their own colour and draw as before. */
const CG_BOLT = 'arch_hammer_lightning_0926';
function cgRedBoltSheet() {
  if (CG.redBolt) return CG.redBolt;
  if (!XART.rdy(CG_BOLT)) return null;
  const im = XART.get(CG_BOLT), w = im.naturalWidth || im.width, h = im.naturalHeight || im.height;
  if (!w || !h) return null;
  const c = cgCanvas(w, h), x = c.getContext('2d');
  x.drawImage(im, 0, 0);
  x.globalCompositeOperation = 'color'; x.fillStyle = '#ff2410'; x.fillRect(0, 0, w, h);
  x.globalCompositeOperation = 'destination-in'; x.drawImage(im, 0, 0);
  return (CG.redBolt = c);
}
/* c25Bolt's own geometry (frame cell, stretch along the segment), red sheet. */
function cgBolt(from, to, t, width, alpha) {
  const im = cgRedBoltSheet(), L = Math.hypot(to.x - from.x, to.y - from.y);
  if (!im || !(L >= 1)) return;
  const f = Math.floor(t * 18) % 8;
  ctx.save();
  ctx.translate(from.x, from.y);
  ctx.rotate(Math.atan2(to.y - from.y, to.x - from.x) - Math.PI / 2);
  ctx.globalAlpha = alpha; ctx.globalCompositeOperation = 'lighter'; ctx.imageSmoothingEnabled = false;
  ctx.drawImage(im, f % 4 * 384 + 78, Math.floor(f / 4) * 512 + 48, 228, 416, -width / 2, 0, width, L);
  ctx.restore();
}
/* front: true draws the near half of every ring, false the far half. */
function cgSwirl(b, M, front) {
  if (M.mode !== 'ragecharge') return;
  const k = M.k, rings = k < .25 ? 2 : k < .55 ? 3 : 4, spin = 2.4 + 5.5 * k;
  const cx = b.x, foot = b.y + 130, head = b.y - 85, rx = 96, ry = 26;
  for (let i = 0; i < rings; ++i) {
    /* each ring rises from his feet to over his head and starts again */
    const v = (efxClock * (.55 + .5 * k) + i / rings) % 1, cy = lerp(foot, head, v);
    const a0 = efxClock * spin + i * 2.1, span = 2.9;
    for (let s = 0; s < 4; ++s) {
      const aa = a0 + span * s / 4, ab = a0 + span * (s + 1) / 4, mid = (aa + ab) / 2;
      if ((Math.sin(mid) > 0) !== front) continue;   /* sin>0: the near side, in front of him */
      const P = a => ({ x: cx + Math.cos(a) * rx * (1 - .25 * v), y: cy + Math.sin(a) * ry });
      const w = 30 + 16 * k, al = Math.min(1, .7 + .3 * k) * (front ? 1 : .75), tt = efxClock + i * .37 + s * .11;
      cgBolt(P(aa), P(ab), tt, w, al);
      if (front) cgBolt(P(aa), P(ab), tt + .05, w * .6, al);   /* a second pass: hotter, brighter core */
    }
  }
}

/* Draw fn() as Chronos's body with the glow around it: the first solid big plate
 * fn blits gets the rim shells under it, and the lit / sweep / core glow go over
 * it afterwards, in that plate's own transform. Other layers that take over his
 * draw (the rage forming) call this so he still glows. */
function cgWithGlow(b, M, fn, stockFlags) {
  const prev = ctx.drawImage;
  let done = false;
  ctx.drawImage = function (im) {
    if (!done && im && im.width >= 200 && im.height >= 200) {
      const k = im.__k || '';
      /* the body is drawn solid: halo/aura copies come first at low alpha or additive */
      if (!/glow|lightning|beam|fx|aura|bolt/i.test(k) && ctx.globalAlpha >= .95 && ctx.globalCompositeOperation === 'source-over') {
        done = true;
        const a = arguments;
        let sx = 0, sy = 0, sw = im.width, sh = im.height, dx, dy, dw, dh;
        if (a.length >= 9) { sx = a[1]; sy = a[2]; sw = a[3]; sh = a[4]; dx = a[5]; dy = a[6]; dw = a[7]; dh = a[8]; }
        else if (a.length >= 5) { dx = a[1]; dy = a[2]; dw = a[3]; dh = a[4]; }
        else { dx = a[1]; dy = a[2]; dw = im.width; dh = im.height; }
        try { cgUnder(b, M, im, sx, sy, sw, sh, dx, dy, dw, dh); } catch (e) { cgLog('under-error', { e: String(e) }); }
      }
    }
    return prev.apply(this, arguments);
  };
  try { return fn(); }
  finally {
    ctx.drawImage = prev;
    if (stockFlags) { CG.noBolts = false; CG.inCharge = false; try { cgThrowFlight(b, M); } catch (e) { cgLog('throw-error', { e: String(e) }); } }
    try { cgOver(b, M); } catch (e) { cgLog('over-error', { e: String(e) }); }
    if (stockFlags) try { cgSwirl(b, M, true); } catch (e) { cgLog('swirl-error', { e: String(e) }); }
  }
}
/* ------------------------------------------------------------- the draw hook */
CG.base = hammerBossDraw;
hammerBossDraw = function (b) {
  if (!cgActive(b)) return CG.base.apply(this, arguments);
  const M = cgMode(b);
  cgDrive(b, M);
  CG.noBolts = M.mode === 'ragecharge';
  CG.inCharge = M.mode === 'ragecharge';
  try { cgSwirl(b, M, false); } catch (e) { cgLog('swirl-error', { e: String(e) }); }
  if (M.mode === 'ragecharge') try { cgHeldTool(b); } catch (e) { cgLog('held-error', { e: String(e) }); }   /* behind him: his fist closes over the handle */
  return cgWithGlow(b, M, () => CG.base.apply(this, arguments), true);
};
/* XART.get tags images with their key so the rings can be cached per plate
 * (untagged per-frame canvases, like the red rage plates, are traced fresh). */
(function () {
  const get = XART.get;
  if (get.__cg) return;
  XART.get = function (k) { const im = get.apply(this, arguments); if (im && typeof k === 'string' && !im.__k) try { im.__k = k; } catch (e) {} return im; };
  XART.get.__cg = true;
})();

/* The stock blue bolts are skipped only inside Chronos's draw during the rage charge. */
(function () {
  if (typeof c25Bolt !== 'function' || c25Bolt.__cg) return;
  const base = c25Bolt;
  c25Bolt = function () { if (CG.noBolts) { CG.boltsSkipped = (CG.boltsSkipped || 0) + 1; return; } return base.apply(this, arguments); };
  c25Bolt.__cg = true;
})();

/* --------------------------------------------------- the longer SSJ charge
 * Mike (Oct 25): "he should have a frame of him throwing the hammer up, not
 * making it just shoot up like that ... can you make the transformation a
 * little longer like a true ssj though?"
 *
 * Length: the live charge is already CG_SSJ = 4.8 s (see below).
 *
 * Pose: the charge now opens on the authored C27 "throw_empty" bank. Frames
 * 0-3 wind up and heave the hammer overhead with both hands; the hammer leaves
 * his hands at frame 3 and only then flies, spinning, up and out of the top of
 * the screen while frames 4-8 play the empty-handed follow-through; then the
 * rage bank takes over from its first frame (no jump), and the stock recall
 * catches it at the end as before. The stock hammer flight (which started at
 * the very first frame, straight out of an idle grip) is skipped in favour of
 * this one.
 *
 * Between: six power-up beats, one per hard step of the charge, each a shock
 * ring, a shake spike and a rim flash, so the long build reads as power
 * surging in waves rather than a held pose. */
/* The live charge is ALREADY 4.8 s: chronos_commitment_1025.js feeds the 1.8 s
 * clock dt*1.8/4.8. A second stretch here compounded it to ~10.7 s, so this
 * layer only reads the length (earlier review clips stepped the clock over
 * 1.8 s and showed the charge 2.7x too fast). */
const CG_SSJ = 7.2;   /* read-only: chronos_commitment feeds the 1.8 s clock dt*1.8/7.2 (lengthened 10-25 by the other session) */
const CG_THROW = { wind: .10, follow: .20, flightEnd: .34 };   /* in charge u (0..1) */
function cgChargeU(b) { const C = b._hammer._hf22Charge; return C ? clamp((C.t || 0) / 1.8, 0, 1) : null; }
function cgThrowPose(b) {
  const u = cgChargeU(b), T = CG_THROW;
  if (u == null || u >= T.follow || typeof c27Pose !== 'function') return null;
  const n = C27_ART.banks.throw_empty_regular ? C27_ART.banks.throw_empty_regular.count : 17;
  /* frames 0-3 over the wind-up, 3-8 over the follow-through */
  const f = u < T.wind ? u / T.wind * 3 : 3 + (u - T.wind) / (T.follow - T.wind) * 5;
  return c27Pose(b, 'throw_empty', clamp(f / (n - 1), 0, 1), 1, typeof c26Material === 'function' ? c26Material(b) : 'regular');
}
/* where the hammer leaves his hands: the hammer tip of throw frame 3 */
function cgReleasePoint(b) {
  const C = b._hammer._hf22Charge;
  if (C._cgRel) return C._cgRel;
  const p = cgHeldHead(b, 3);
  if (cgChargeU(b) >= CG_THROW.wind) C._cgRel = p;   /* freeze it once he has let go */
  return p;
}
(function () {
  const base = ha21Blue;
  ha21Blue = function (b) {
    if (cgActive(b) && b._hammer._hf22Charge) {
      const u = cgChargeU(b);
      const q = cgThrowPose(b);
      if (q) return q;
      /* after the throw: the rage bank from its first frame, not from mid-reel */
      if (u < .86 && typeof c29Pose === 'function' && C29_ART.banks.rage_regular) {
        const mat = u >= .62 ? 'red' : (typeof c26Material === 'function' ? c26Material(b) : 'regular');
        const N = C29_ART.banks.rage_regular.length;
        return c29Pose('rage', clamp((u - CG_THROW.follow) / (.86 - CG_THROW.follow), 0, 1) * (N - 1), mat);
      }
    }
    return base.apply(this, arguments);
  };
})();
/* c30ChargeDraw's expanding aura blits the stencil at the plate's NATIVE size,
 * which is right for the C29 rage plates (drawn 1:1) and wrong for the C27
 * throw plate (drawn at C27_ART.worldScale): it trailed off up-left of him as
 * a ghost outline. While the charge draws, a C27 key gets a stencil rescaled
 * to the size the plate is actually drawn. c27TraceAura is not affected. */
(function () {
  if (typeof c30ChargeDraw !== 'function' || typeof c27AuraStencil !== 'function') return;
  const draw = c30ChargeDraw, sten = c27AuraStencil, cache = new Map();
  c30ChargeDraw = function () { CG.c30 = true; try { return draw.apply(this, arguments); } finally { CG.c30 = false; } };
  c27AuraStencil = function (key) {
    const m = sten.apply(this, arguments);
    if (!m || !CG.c30 || typeof key !== 'string' || key.indexOf('c27_') !== 0) return m;
    if (cache.get(key)?.src === m) return cache.get(key).out;
    const ws = C27_ART.worldScale, pad = m.pad, W = Math.round(m.sourceW * ws) + pad * 2, H = Math.round(m.sourceH * ws) + pad * 2;
    const sc = c => { const o = document.createElement('canvas'); o.width = W; o.height = H; const g = o.getContext('2d'); g.imageSmoothingEnabled = false;
      g.drawImage(c, pad - pad * ws, pad - pad * ws, c.width * ws, c.height * ws); return o; };
    const out = { ...m, edge: sc(m.edge), red: sc(m.red), outer: sc(m.outer), sourceW: W - pad * 2, sourceH: H - pad * 2, scaled: ws };
    cache.set(key, { src: m, out }); while (cache.size > 24) cache.delete(cache.keys().next().value);
    return out;
  };
})();
/* skip the stock flight (it launched from an idle grip on the first frame) */
(function () {
  if (typeof c29Tool !== 'function') return;
  const base = c29Tool;
  c29Tool = function (b) {
    if (CG.inCharge && b && b._hammer && b._hammer._hf22Charge && cgChargeU(b) < CG_THROW.flightEnd) return;
    return base.apply(this, arguments);
  };
  CG.toolBase = base;
})();
/* The throw bank is authored EMPTY-HANDED, and its tip/grip fields are synthetic
 * (always 126 apart, nowhere near the hands), so the raised fist is measured off
 * the plate's own pixels: ink centroid of the top 30 rows, native cell px. */
const CG_FIST = [[210, 175], [214, 175], [214, 175], [190, 148]];
const CG_FIST_DX = [12, 12, 12, 0];   /* world px: puts the handle through the fist, not beside it (read off the render) */
/* The detached hammer is C35's eight authored flight views (c35Tool picks one by
 * angle, never rotates, and places its HEAD at the given point). View 1 has the
 * head up-left with the handle running down-right; view 2 is upright. */
const CG_TOOL_VIEW = [Math.PI / 4, Math.PI / 4, Math.PI / 4, Math.PI / 2];   /* cocked back, then up at the release */
const CG_TOOL_K = .687 / .72, CG_TOOL_REACH = 195;  /* catch size (c35Catch); fist-to-head along the handle, flight-sheet px */
function cgThrowBank(b) { return C27_ART.banks['throw_empty_' + ((typeof c26Material === 'function' && c26Material(b)) || 'regular')] || C27_ART.banks.throw_empty_regular; }
/* where the hammer head sits on wind-up frame f: up the handle from the fist */
function cgHeldHead(b, f) {
  const ws = C27_ART.worldScale, pv = C27_ART.pixelPivot, F = CG_FIST[f], a = CG_TOOL_VIEW[f], L = CG_TOOL_REACH * .72 * CG_TOOL_K;
  const gx = b.x + (F[0] - pv[0]) * ws + CG_FIST_DX[f], gy = b.y + (F[1] - pv[1]) * ws;
  return { x: gx - Math.cos(a) * L, y: gy - Math.sin(a) * L, a };
}
/* the wind-up: the hammer is in his hand */
function cgHeldTool(b) {
  const u = cgChargeU(b);
  if (u == null || u >= CG_THROW.wind || !CG.toolBase) return;
  const f = Math.min(3, Math.floor(u / CG_THROW.wind * 3 + 1e-6)), h = cgHeldHead(b, f);
  CG.toolBase(b, h, h, 0, CG_TOOL_K, h.a);
}
function cgThrowFlight(b, M) {
  if (M.mode !== 'ragecharge') return;
  const u = cgChargeU(b), T = CG_THROW;
  if (u < T.wind || u > T.flightEnd || !CG.toolBase) return;
  const p = (u - T.wind) / (T.flightEnd - T.wind), from = cgReleasePoint(b);
  const to = { x: from.x + 60, y: viewTopY() - 220 };
  /* spins end over end as it goes, shrinking into the distance */
  CG.toolBase(b, from, to, p, lerp(CG_TOOL_K, .3, p), CG_TOOL_VIEW[3] + p * Math.PI * 5);
}
