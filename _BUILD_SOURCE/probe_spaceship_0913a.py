#!/usr/bin/env python3
"""
probe_spaceship_0913a.py - THE FURY SPACESHIP IS THE PLAYER'S SHIP WHEREVER THE PLAYER IS IN SPACE.

    python _BUILD_SOURCE/probe_spaceship_0913a.py [--out docs/proofs/spaceship_0913a] [--compare before/report.json]

Mike (0913): "You must wire up the new space ship we have and do the palette swap for each player." and
"Show the spaceship transformation scene and make it properly fixed and working in-game."

Everything is RECORDED off the game's own draw calls, never recomputed (probe_seam 0810a: a probe that
recomputes the thing under test asserts the fix it was meant to test):
  - ctx.drawImage is wrapped on the #screen context INSTANCE. The context carries its own drawImage, so a
    prototype trap catches nothing (0905h). Each blit keeps the transform in force, so every rect below is
    where the pixels landed, in VW px.
  - every blit is tagged by its CALLER - drawShipSprite (the plane), spaceAtlasDraw (with the atlas KEY it
    was asked for), gravityModeDrawShip, drawDeathSpin, _drawPlayerCore - because XART.get hands back a
    canvas with no .src and no stable identity. Top-level function declarations are reassignable, so the
    wraps sit on the game's own call sites.
  - the loop is stepped on a synthetic clock (shoot.TRAP_RAF, one loop() per 1/60 s) in chunks with a real
    pause between them, so lazily decoded art can land (0905: a tight STEP loop decodes nothing).
  - the player is kept alive by stubbing playerHit, never by pinning invuln (0912v: the damage blink hid the
    ship for a whole recording). The death checks restore the real playerHit.
  - `shake` is zeroed while the countdown hands over to PLAY, and ONLY there: drawWorld translates the whole
    world by rnd(-shake,shake), which is noise on top of the geometry being measured. The raw value is still
    recorded on every frame.

Checks: the stage-5 transformation (drawn size and position frame by frame, the space sweep, no crossfade),
a direct stage-5 fight by both debug routes and shoot.py's SETUP route, respawn and continue after a death,
the death spin-out and the somersault on space frames, the stage-9 launch and the rift return to stage 5
without a replay, and all nine pilots' palettes. Page errors and console errors must be zero.
"""
import os, sys, json, math, base64, io, argparse, time, itertools, colorsys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import shoot

ROOT = shoot.GAME
PILOTS = ['axel', 'cole', 'maverick', 'decker', 'yuri', 'freezer', 'juggernaut', 'lizzie', 'falva']

INSTRUMENT = r"""
() => {
  const W = window;
  if (W.__P) return 'already';
  const cvs = document.getElementById('screen');
  const c = cvs.getContext('2d');
  const HULL = /^ship_(base|bank_[lr][123]|roll_\d\d|so_\d\d)$/;
  const P = W.__P = { rec: null, tag: [], key: null, log: [], frame: 0, bandH: null, fadeA: null, err: null };
  const od = c.drawImage;
  c.drawImage = function (im) {
    if (P.rec && P.tag.length) {
      const n = arguments.length; let dx, dy, dw, dh;
      if (n === 3) { dx = arguments[1]; dy = arguments[2]; dw = im.width; dh = im.height; }
      else if (n === 5) { dx = arguments[1]; dy = arguments[2]; dw = arguments[3]; dh = arguments[4]; }
      else { dx = arguments[5]; dy = arguments[6]; dw = arguments[7]; dh = arguments[8]; }
      const m = this.getTransform(), sx = cvs.width / VW;
      const q = [[dx, dy], [dx + dw, dy], [dx, dy + dh], [dx + dw, dy + dh]]
        .map(p => [(m.a * p[0] + m.c * p[1] + m.e) / sx, (m.b * p[0] + m.d * p[1] + m.f) / sx]);
      P.rec.push({ stack: P.tag.join('>'), top: P.tag[P.tag.length - 1], key: P.key,
        cx: (q[0][0] + q[1][0] + q[2][0] + q[3][0]) / 4, cy: (q[0][1] + q[1][1] + q[2][1] + q[3][1]) / 4,
        /* the drawn size along the image's own axes - a rotation does not inflate it */
        w: Math.hypot(m.a * dw, m.b * dw) / sx, h: Math.hypot(m.c * dh, m.d * dh) / sx,
        rot: Math.atan2(m.b, m.a), ga: this.globalAlpha });
    }
    return od.apply(this, arguments);
  };
  const orect = c.rect;
  c.rect = function (x, y, w, h) {
    /* the FIRST rect(0,0,..) of the frame is the band's own clip - the level drawn inside it may issue others */
    if (P.rec && P.bandH == null && P.tag[P.tag.length - 1] === 'stage5SkyToSpaceDraw' && x === 0 && y === 0) P.bandH = h;
    return orect.apply(this, arguments);
  };
  const wrap = (name) => {
    const f = W[name]; if (typeof f !== 'function' || f.__probe) return false;
    const g = function () { P.tag.push(name); try { return f.apply(this, arguments); } finally { P.tag.pop(); } };
    g.__probe = true; W[name] = g; return true;
  };
  const sad = W.spaceAtlasDraw;
  W.spaceAtlasDraw = function (g, key) {
    const pk = P.key; P.key = key; P.tag.push('space');
    try { return sad.apply(this, arguments); } finally { P.tag.pop(); P.key = pk; }
  };
  ['drawShipSprite', 'gravityModeDrawShip', '_drawPlayerCore', 'drawDeathSpin', 'stage5SkyToSpaceDraw'].forEach(wrap);
  /* the fusion white is a full-screen fill: a size change drawn UNDER it at >=0.95 cannot be seen, so the
     continuity metric has to know how white each frame was - recorded off the call, not inferred from the phase */
  const gw = W.gravityWhite;
  W.gravityWhite = function (alpha) {
    if (P.rec) { const a = Math.max(0, Math.min(1, +alpha || 0)); P.white = (P.white == null) ? a : Math.max(P.white, a); }
    return gw.apply(this, arguments);
  };
  const ecd = W.entryConnectorDraw;
  W.entryConnectorDraw = function () {
    if (P.rec && P.tag.indexOf('stage5SkyToSpaceDraw') >= 0) { const a = c.globalAlpha; P.fadeA = (P.fadeA == null) ? a : Math.min(P.fadeA, a); }
    return ecd.apply(this, arguments);
  };
  if (!W.__realHit) W.__realHit = W.playerHit;
  P.alive = function () { W.playerHit = function () {}; };
  P.mortal = function () { W.playerHit = W.__realHit; };
  const r2 = (v) => (v == null ? null : +(+v).toFixed(2));
  const rr = (r) => r ? { cx: r2(r.cx), cy: r2(r.cy), w: r2(r.w), h: r2(r.h), rot: +r.rot.toFixed(3), key: r.key || null } : null;
  P.sample = function () {
    const R = P.rec || [];
    let plane = null; for (const r of R) if (r.top === 'drawShipSprite') plane = r;
    let hull = null; for (const r of R) if (r.top === 'space' && HULL.test(r.key || '') && r.stack.indexOf('drawDeathSpin') < 0) { hull = r; break; }
    const spinSpace = R.filter(r => r.stack.indexOf('drawDeathSpin') >= 0 && r.top === 'space' && HULL.test(r.key || ''));
    const spinPlane = R.filter(r => r.top === 'drawDeathSpin');
    const planePlay = R.filter(r => r.top === '_drawPlayerCore' && r.h >= 40);
    const keys = {}; for (const r of R) if (r.top === 'space' && r.key) keys[r.key] = 1;
    let anchorErr = null;
    try {
      const s = player._spin;
      if (s && s.anchor && s.anchor.length) { anchorErr = 0;
        for (const a of s.anchor) { if (!a.e) continue; anchorErr = Math.max(anchorErr, Math.hypot(a.e.x - (player.x + a.ox), a.e.y - (player.y + a.oy))); } }
    } catch (e) {}
    return {
      i: P.frame, st: state, ph: (drawLaunch._phase === undefined ? null : drawLaunch._phase),
      gm: gravityMode ? gravityMode.phase : null, gt: gravityMode ? r2(gravityMode.t || 0) : null,
      stage: run.stage, space: !!run.spaceMode, ready: !!run.gravityShipReady,
      plane: rr(plane), hull: rr(hull), keys: Object.keys(keys),
      spinSpace: spinSpace.length, spinPlane: spinPlane.length, spinRot: spinSpace.length ? +spinSpace[0].rot.toFixed(3) : null,
      planePlay: planePlay.length, band: r2(P.bandH), fadeA: (P.fadeA == null ? null : +P.fadeA.toFixed(3)),
      px: r2(player.x), py: r2(player.y), dead: !!player.dead, inv: player.invuln | 0,
      somer: !!player.somer, roll: !!player.roll,
      spin: player._spin ? { t: r2(player._spin.t), crashed: !!player._spin.crashed } : null,
      anchorErr: (anchorErr == null ? null : +anchorErr.toFixed(4)), shake: r2(+shake || 0), lives: run.lives,
      flash: r2(+flashScreen || 0), white: r2(P.white), spinR: rr(spinSpace.length ? spinSpace[0] : null)
    };
  };
  P.step = function (n, recOn, stopOnBeat, zeroShake) {
    let last = P.log.length ? P.log[P.log.length - 1] : null;
    for (let k = 0; k < n; k++) {
      W.__bofStepNow = (Number.isFinite(W.__bofStepNow) ? W.__bofStepNow : performance.now()) + 1000 / 60;
      let rawShake = null; try { rawShake = +shake || 0; } catch (e) {}
      if (zeroShake) { try { shake = 0; } catch (e) {} }
      P.rec = recOn ? [] : null; P.bandH = null; P.fadeA = null; P.white = null;
      try { loop(W.__bofStepNow); } catch (e) { P.err = String(e).slice(0, 200); }
      P.frame++;
      if (recOn) {
        const s = P.sample(); s.shakeRaw = (rawShake == null ? null : +rawShake.toFixed(2)); P.log.push(s);
        if (stopOnBeat && last && (s.st !== last.st || s.ph !== last.ph || s.gm !== last.gm)) { P.rec = null; return { beat: true, n: k + 1, s: s }; }
        last = s;
      }
      P.rec = null;
    }
    return { beat: false, n: n, s: P.log.length ? P.log[P.log.length - 1] : null };
  };
  P.canvas = function () { return cvs.toDataURL('image/png'); };
  P.sx = function () { return cvs.width / VW; };
  /* the palette the runtime actually blits: the pilot's cached ship canvas, averaged over the blue mask */
  P.paletteMean = function (pk) {
    const src = spaceAtlasCanvas('ship_base', pk), r = spaceAtlasRect('ship_base_blue');
    if (!src || !r) return null;
    const im = XART.get('ngm_space_atlas');
    const m = document.createElement('canvas'); m.width = src.width; m.height = src.height;
    const mg = m.getContext('2d'); mg.drawImage(im, r.x, r.y, r.w, r.h, 0, 0, r.w, r.h);
    const md = mg.getImageData(0, 0, m.width, m.height).data;
    const t = document.createElement('canvas'); t.width = src.width; t.height = src.height;
    const tg = t.getContext('2d'); tg.drawImage(src, 0, 0);
    const td = tg.getImageData(0, 0, t.width, t.height).data;
    let sw = 0, sr = 0, sg = 0, sb = 0;
    for (let i = 0; i < md.length; i += 4) { const a = md[i + 3] / 255; if (a <= 0) continue; sw += a; sr += a * td[i]; sg += a * td[i + 1]; sb += a * td[i + 2]; }
    return sw > 0 ? [sr / sw, sg / sw, sb / sw] : null;
  };
  /* mean colour of a horizontal strip of the live canvas, in VW rows */
  P.strip = function (y0, y1) {
    const g = cvs.getContext('2d'), sx = cvs.width / VW;
    const d = g.getImageData(0, Math.round(y0 * sx), cvs.width, Math.max(1, Math.round((y1 - y0) * sx))).data;
    let r = 0, gg = 0, b = 0, n = 0; for (let i = 0; i < d.length; i += 16) { r += d[i]; gg += d[i + 1]; b += d[i + 2]; n++; }
    return [+(r / n).toFixed(1), +(gg / n).toFixed(1), +(b / n).toFixed(1)];
  };
  return 'ok';
}
"""

WARM = r"""
(keys) => { for (const k of keys) { try { if (XART._touch) XART._touch(k); XART.rdy(k); } catch (e) {} } return true; }
"""
READY = r"""
(keys) => keys.every(k => { try { return XART.rdy(k); } catch (e) { return false; } })
"""


def serve_overlay(root, overlay):
    """shoot.serve, plus an optional OVERLAY directory whose files are served in place of the tree's - so a
    baseline copy of game.js and the space atlas can be measured while the tree itself is being edited."""
    import http.server, functools, threading
    served = []

    class H(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *a, **k):
            pass

        def translate_path(self, path):
            p = super().translate_path(path)
            if overlay:
                rel = os.path.relpath(p, root)
                alt = os.path.join(overlay, rel)
                if not rel.startswith('..') and os.path.isfile(alt):
                    served.append(rel.replace(os.sep, '/'))
                    return alt
            return p

    httpd = http.server.ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(H, directory=root))
    httpd.daemon_threads = True
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return httpd.server_address[1], httpd.shutdown, served


def png_from_dataurl(u):
    from PIL import Image
    return Image.open(io.BytesIO(base64.b64decode(u.split(',', 1)[1]))).convert('RGBA')


class Probe:
    def __init__(self, pg, out):
        self.pg, self.out = pg, out
        self.fails, self.oks, self.report = [], [], {'checks': []}
        self.GS = pg.evaluate("() => GS")

    def ok(self, cond, msg, **data):
        (self.oks if cond else self.fails).append(msg)
        print(('  ok   ' if cond else '  FAIL ') + msg, flush=True)
        self.report['checks'].append({'ok': bool(cond), 'msg': msg, **data})

    def js(self, body, arg=None):
        return self.pg.evaluate(body, arg) if arg is not None else self.pg.evaluate(body)

    def step(self, n, rec=True, beat=False, zero_shake=False, chunk=20, pause=25):
        got = []
        left = n
        while left > 0:
            k = min(chunk, left)
            r = self.pg.evaluate("([k, rec, beat, zs]) => window.__P.step(k, rec, beat, zs)", [k, rec, beat, zero_shake])
            left -= r['n']
            if r.get('beat'):
                got.append(r['s'])
                return got, left
            self.pg.wait_for_timeout(pause)
        return got, 0

    def log_from(self, i0):
        return self.pg.evaluate("(i0) => window.__P.log.filter(s => s.i >= i0)", i0)

    def frame(self):
        return self.pg.evaluate("() => window.__P.frame")

    def canvas(self):
        return png_from_dataurl(self.pg.evaluate("() => window.__P.canvas()"))

    def wait_ready(self, keys, timeout_s=60):
        self.js(WARM, keys)
        t0 = time.time()
        while time.time() - t0 < timeout_s:
            if self.js(READY, keys):
                return True
            self.pg.wait_for_timeout(250)
            self.js(WARM, keys)
        return False

    def wait_stage_loaded(self, n, timeout_s=90):
        self.js("(n) => { try { if (typeof warmStage==='function') warmStage(n); } catch (e) {} return true; }", n)
        t0 = time.time()
        while time.time() - t0 < timeout_s:
            if self.js("(n) => (typeof stageLoadReady!=='function') || stageLoadReady(n)", n):
                return True
            self.pg.wait_for_timeout(300)
        return False


def series_deltas(log, field, hide_white=0.95):
    """max |frame-to-frame change| of rect.cx/cy/h across consecutive samples that both carry the rect.
    A change drawn while the fusion white covers the screen at >= hide_white on either frame cannot be seen, so it
    is not scored - it is LISTED under 'hidden' instead, with the white it was drawn under, so nothing is dropped."""
    worst = {'cx': (0, None), 'cy': (0, None), 'h': (0, None)}
    hidden = []
    prev = None
    for s in log:
        r = s.get(field)
        if r and prev and prev.get(field) and s['i'] == prev['i'] + 1:
            wmax = max(s.get('white') or 0, prev.get('white') or 0)
            for k in ('cx', 'cy', 'h'):
                d = abs(r[k] - prev[field][k])
                if wmax >= hide_white:
                    if d > 1.0:
                        hidden.append({'frame': s['i'], 'field': k, 'delta': round(d, 2), 'white': wmax})
                    continue
                if d > worst[k][0]:
                    worst[k] = (round(d, 2), s['i'])
        prev = s
    worst['hidden'] = hidden[:12]
    return worst


def boundary(log, pred, field):
    """the change in rect `field` across the first frame where pred(sample) becomes true"""
    for a, b in zip(log, log[1:]):
        if pred(b) and not pred(a):
            ra, rb = a.get(field), b.get(field)
            if ra and rb:
                return {'frame': b['i'], 'dcx': round(rb['cx'] - ra['cx'], 2), 'dcy': round(rb['cy'] - ra['cy'], 2),
                        'dh': round(rb['h'] - ra['h'], 2), 'from': ra, 'to': rb}
            return {'frame': b['i'], 'missing': True, 'from': ra, 'to': rb}
    return None


def cinematic(P, pilot):
    """stage 5 from its stage card through the whole launch and 90 frames of PLAY - password/stage-select route"""
    print('\n== the stage-5 transformation, %s ==' % pilot, flush=True)
    P.wait_stage_loaded(5)
    P.js("() => { window.__P.alive(); return true; }")
    info = P.js("""([pk]) => {
      try { debugRecStop(); } catch (e) {}
      debugFight = null; run.mode = 'arcade'; diffKey = diffKey || 'normal';
      try { _coleScene = 0; } catch (e) {}
      run._l78Entry = 0; run._s5ResumeArm = 0; coopOn = false; PENDING_STAGE = 1;
      const i = PILOTS.findIndex(p => p.key === pk); if (i >= 0) pilotIndex = i;
      startRun(5);
      try { floaters.length = 0; } catch (e) {}
      const o = { state: state, stage: run.stage, pilot: _pilotKey(), gm: gravityMode ? gravityMode.phase : null, space: !!run.spaceMode };
      if (state === GS.INTRO) stateT = 3.599;
      return o;
    }""", [pilot])
    P.report['cinematic_entry'] = info
    i0 = P.frame()
    shots = {}
    frames = 0
    mid_charge = False
    while frames < 7000:
        st = P.js("() => ({st: state, ph: drawLaunch._phase, pt: drawLaunch._pt})")
        zero = (st['st'] == P.GS['PLAY']) or (st['ph'] == 'cd' and (st['pt'] or 0) > 3.2)
        got, left = P.step(20, rec=True, beat=True, zero_shake=zero)
        cur = P.js("() => window.__P.log[window.__P.log.length-1]")
        frames = cur['i'] - i0
        if got:
            s = got[0]
            label = '%05d_%s_%s_%s' % (s['i'] - i0, s['st'], s['ph'], s['gm'])
            img = P.canvas()
            if len(shots) < 30:
                shots[label] = img
            if s['st'] == P.GS['PLAY'] and 'handoff' not in P.report:
                # the frame the launch hands to PLAY, read back as pixels: a cleared canvas is alpha 0 everywhere
                small = img.convert('RGB').resize((96, 96))
                mean = sum(sum(px) for px in small.getdata()) / (96 * 96 * 3.0)
                P.report['handoff'] = {'frame': s['i'] - i0, 'alpha_bbox': img.getchannel('A').getbbox(),
                                       'mean_rgb': round(mean, 2)}
        if cur['gm'] == 'charge' and (cur['gt'] or 0) > 2.0 and not mid_charge:
            mid_charge = True
            shots['%05d_mid_charge' % (cur['i'] - i0)] = P.canvas()
        if cur['st'] == P.GS['PLAY']:
            break
        if cur['ph'] == 'load':
            P.pg.wait_for_timeout(150)
    # 90 frames of play, the first of them with shake zeroed (see the header)
    P.step(90, rec=True, zero_shake=True)
    shots['%05d_play' % (P.frame() - i0)] = P.canvas()
    log = P.log_from(i0)
    return log, shots


def analyse_cinematic(P, log, VH):
    GS = P.GS
    L = [s for s in log if s['st'] in (GS['LAUNCH'], GS['PLAY'])]
    launch = [s for s in L if s['st'] == GS['LAUNCH']]
    play = [s for s in L if s['st'] == GS['PLAY']]
    # the frame the stage card hands over is SAMPLED as LAUNCH but drawLaunch has not drawn on it: the card's own draw
    # called setState(GS.LAUNCH) mid-frame, so its gravityMode is still what spaceModeStage set. Scored from the
    # first frame the launch actually drew; the handover frame's value is reported, not hidden.
    prev_st = {b['i']: a['st'] for a, b in zip(log, log[1:])}
    drawn = [s for s in launch if prev_st.get(s['i']) == GS['LAUNCH']]
    seen = []
    for s in drawn:
        if s['gm'] and (not seen or seen[-1] != s['gm']):
            seen.append(s['gm'])
    res = {'frames_launch': len(launch), 'frames_play': len(play), 'gravity_phases': seen,
           'handover_frame_gm': [s['gm'] for s in launch if prev_st.get(s['i']) != GS['LAUNCH']]}
    plane_frames = [s for s in launch if s['plane']]
    hull_frames = [s for s in L if s['hull']]
    res['plane_deltas'] = series_deltas(plane_frames, 'plane')
    res['hull_deltas'] = series_deltas(hull_frames, 'hull')
    res['kit_arrival'] = boundary(L, lambda s: s['gm'] == 'drift', 'plane')
    res['brake_start'] = boundary(L, lambda s: s['ph'] == 'brake', 'plane')
    res['settle_start'] = boundary(L, lambda s: s['ph'] == 'settle', 'plane')
    res['countdown_start'] = boundary(L, lambda s: s['ph'] == 'cd', 'hull')
    res['handoff'] = boundary(L, lambda s: s['st'] == GS['PLAY'], 'hull')
    res['play_hull_h'] = sorted({s['hull']['h'] for s in play if s['hull']})[:6]
    res['play_first_shake'] = play[0]['shake'] if play else None
    # what the transformation left behind for PLAY's first frame: drawWorld translates by rnd(-shake,shake) and
    # paints flashScreen as an orange wash, and neither is spent anywhere inside LAUNCH
    # the probe itself zeroes shake from the tail of the countdown on, so the leftover is read off the RAW value
    # the frames before any zeroing carried - the worst of the last 40 launch frames and the first play frame
    tail = launch[-40:] + play[:1]
    res['play_first_shake_raw'] = max(((s.get('shakeRaw') or 0) for s in tail), default=None)
    res['play_first_flash'] = play[0].get('flash') if play else None
    res['crossfade_frames'] = sum(1 for s in launch if s['fadeA'] is not None and s['fadeA'] < 0.999)
    bands = [(s['i'], s['band']) for s in launch if s['band'] is not None]
    res['band_max'] = max((b for _, b in bands), default=None)
    rev = [s for s in launch if s['gm'] == 'reveal']
    res['band_at_reveal'] = rev[0]['band'] if rev else None
    first_full = next((i for i, b in bands if b >= VH - 0.5), None)
    res['band_full_frame'] = first_full
    res['reveal_frame'] = rev[0]['i'] if rev else None
    return res


def check_cinematic(P, res, VH, SPACE):
    order = ['drift', 'charge', 'scatter', 'snap', 'pixelglow', 'whiteout', 'reveal', 'active']
    P.ok(res['gravity_phases'] == order, 'the launch walks the whole transformation in order: %s' % res['gravity_phases'])
    pd, hd = res['plane_deltas'], res['hull_deltas']
    P.ok(pd['h'][0] <= 2.0 and pd['cy'][0] <= 4.5 and pd['cx'][0] <= 4.5,
         'the plane is continuous frame to frame through run/brake/settle/kit (worst dh %.2f @%s, dcy %.2f @%s, dcx %.2f)'
         % (pd['h'][0], pd['h'][1], pd['cy'][0], pd['cy'][1], pd['cx'][0]))
    ka = res['kit_arrival']
    P.ok(bool(ka) and not ka.get('missing') and abs(ka['dh']) <= 2.0,
         'no size pop when the kit arrives (plane dh %s)' % (ka and ka.get('dh')))
    hid = hd.get('hidden') or []
    P.ok(hd['h'][0] <= 2.0 and hd['cy'][0] <= 4.5 and hd['cx'][0] <= 4.5,
         'the finished ship is continuous from fusion through countdown, GO and play (worst visible dh %.2f @%s, dcy %.2f @%s, dcx %.2f; %d changes drawn under >=95%% white, largest %s)'
         % (hd['h'][0], hd['h'][1], hd['cy'][0], hd['cy'][1], hd['cx'][0], len(hid), max((x['delta'] for x in hid), default=0)))
    cd = res['countdown_start']
    P.ok(bool(cd) and not cd.get('missing') and abs(cd['dh']) <= 2.0 and abs(cd['dcy']) <= 4.5,
         'no size drop and no jump when 3-2-1 starts (dh %s, dcy %s)' % (cd and cd.get('dh'), cd and cd.get('dcy')))
    ho = res['handoff']
    P.ok(bool(ho) and not ho.get('missing') and max(abs(ho['dh']), abs(ho['dcy']), abs(ho['dcx'])) <= 1.0,
         'GO hands the ship to PLAY at the same size and place (dcx %s dcy %s dh %s)' % (ho and ho.get('dcx'), ho and ho.get('dcy'), ho and ho.get('dh')))
    P.ok((res.get('play_first_flash') or 0) <= 0.01 and (res.get('play_first_shake_raw') or 0) <= 5.01,
         "nothing the transformation set lands on PLAY's first frame (flashScreen %s, shake %s; GO's own punch is 5)"
         % (res.get('play_first_flash'), res.get('play_first_shake_raw')))
    P.ok(bool(res['play_hull_h']) and all(abs(h - SPACE) <= 0.5 for h in res['play_hull_h']),
         'PLAY draws the ship at SPACE_SHIP_SIZE %s: %s' % (SPACE, res['play_hull_h']))
    P.ok(res['crossfade_frames'] == 0, 'the level never fades in over the space band (%d crossfaded frames)' % res['crossfade_frames'])
    P.ok(res['band_full_frame'] is not None and res['reveal_frame'] is not None and res['band_full_frame'] <= res['reveal_frame'],
         'the space band has swept the whole screen by the reveal (band max %s, full at %s, reveal at %s)'
         % (res['band_max'], res['band_full_frame'], res['reveal_frame']))


def play_route(P, label, setup_js, pilot, frames=90):
    P.js("() => { window.__P.alive(); return true; }")
    info = P.js(setup_js, [pilot])
    i0 = P.frame()
    P.step(frames, rec=True)
    log = P.log_from(i0)
    PLAY = P.GS['PLAY']
    pl = [s for s in log if s['st'] == PLAY]
    hull = sum(1 for s in pl if s['hull'])
    plane = sum(1 for s in pl if s['planePlay'])
    keys = sorted({k for s in pl for k in s['keys'] if k.startswith('ship_')})
    P.ok(len(pl) > 0 and hull > 0 and plane == 0,
         '%s: the spaceship is the player ship (%d/%d play frames drew it, %d drew a plane, space=%s, keys %s)'
         % (label, hull, len(pl), plane, pl[-1]['space'] if pl else None, keys[:4]), info=info)
    return log


def death_route(P, lives, expect_continue, center=False):
    PLAY, CONT = P.GS['PLAY'], P.GS['CONTINUE']
    # center: the proof death happens in open space - at the bottom of the field it spins UNDER the EQUIPPED box, and
    # occlusion is not a missing draw (CLAUDE.md), so a proof taken there shows the box and proves nothing
    P.js("""([lives, center]) => { const P = window.__P;
      if (special && typeof endSpecial === 'function') endSpecial(); special = null;
      run.shield = 0; player.invuln = 0; player.roll = null; player.somer = null; player.dead = false; run.lives = lives;
      if (center) { player.x = worldWidth() / 2; player.y = VH * 0.5; player._bank = 0; }
      P.mortal(); playerHit(); P.alive();
      return { dead: player.dead, spin: !!player._spin }; }""", [lives, center])
    i0 = P.frame()
    shots = []
    for _ in range(400):
        P.step(3, rec=True, pause=6)
        cur = P.js("() => window.__P.log[window.__P.log.length-1]")
        if cur['spin'] and not cur['spin']['crashed'] and cur.get('spinR') and len(shots) < 8 and (cur['i'] - i0) % 9 < 3:
            shots.append((cur, P.canvas()))
        if expect_continue:
            if cur['st'] == CONT:
                break
        elif not cur['dead'] and cur['st'] == PLAY and not cur['spin']:
            break
    if expect_continue:
        P.step(30, rec=True)
        P.js("() => { BOSSMODE.injectTap('enter'); return true; }")
        for _ in range(30):
            P.step(4, rec=True, pause=10)
            if P.js("() => state") == PLAY:
                break
    P.step(60, rec=True)
    log = P.log_from(i0)
    return log, shots


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', default=os.path.join(ROOT, 'docs', 'proofs', 'spaceship_0913a'))
    ap.add_argument('--compare', default=None, help='an earlier report.json to overlay on the size track')
    ap.add_argument('--pilot', default='cole')
    ap.add_argument('--overlay', default=None, help='a directory whose files are served instead of the tree\'s (a baseline copy)')
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    from playwright.sync_api import sync_playwright
    from PIL import Image, ImageDraw
    port, stop, overlay_served = serve_overlay(ROOT, a.overlay)
    page_errors, console_errors = [], []
    t_start = time.time()
    with sync_playwright() as pw:
        br = pw.chromium.launch(args=['--disable-gpu', '--no-sandbox', '--mute-audio'])
        pg = br.new_page(viewport={'width': 1100, 'height': 1060})
        pg.on('pageerror', lambda e: page_errors.append(str(e)[:240]))
        pg.on('console', lambda m: console_errors.append(m.text[:240]) if m.type == 'error' else None)
        pg.goto('http://127.0.0.1:%d/index.html?bossmode=1' % port, wait_until='load', timeout=90000)
        pg.wait_for_function("() => window.BOSSMODE && window.BOSSMODE.ready", timeout=120000)
        pg.evaluate(shoot.TRAP_RAF)
        print('instrument:', pg.evaluate(INSTRUMENT))
        P = Probe(pg, a.out)
        VH, VW = pg.evaluate("() => [VH, VW]")
        SPACE = pg.evaluate("() => SPACE_SHIP_SIZE")
        warm = ['ngm_space_atlas', 'bg_stage05_loop', 'stage6_blue_master', 'scard_5', 'scard_9'] + \
               ['ship_%s' % p for p in PILOTS] + ['ship_%s_sp0' % p for p in PILOTS] + ['ship_%s_so0' % p for p in PILOTS] + \
               ['nfx_s5gate96_%d' % i for i in range(8)]
        P.report['warm_ready'] = P.wait_ready(warm, 90)
        R = P.report
        R['has'] = pg.evaluate("""() => ({spaceShipActive: typeof spaceShipActive==='function',
            so: !!(typeof spaceAtlasRect==='function' && spaceAtlasRect('ship_so_00')),
            gain: typeof GRAVITY_PILOT_LUM!=='undefined'})""")
        print('has:', R['has'])

        # ---- 1. the transformation, measured frame by frame ------------------------------------------
        log, shots = cinematic(P, a.pilot)
        res = analyse_cinematic(P, log, VH)
        R['cinematic'] = res
        R['cinematic_log'] = log
        print(json.dumps({k: v for k, v in res.items() if k not in ('plane_deltas', 'hull_deltas')}, default=str)[:1800])
        print('plane deltas', res['plane_deltas'], 'hull deltas', res['hull_deltas'])
        check_cinematic(P, res, VH, SPACE)
        ho = R.get('handoff') or {}
        P.ok(bool(ho) and ho.get('alpha_bbox') is not None and (ho.get('mean_rgb') or 0) > 2,
             'the frame GO hands to PLAY is a picture, not a cleared canvas (alpha bbox %s, mean rgb %s)'
             % (ho.get('alpha_bbox'), ho.get('mean_rgb')))
        rev = [s for s in log if s['st'] == P.GS['LAUNCH'] and s['ph'] == 'cd']
        # the sky is gone when the numerals start: the bottom strip is space, not the stage-6 blue
        bottom = None
        if rev:
            bottom = pg.evaluate("() => window.__P.strip(VH-48, VH)")
        R['cd_bottom_strip'] = bottom
        # contact sheet of the beats
        names = sorted(shots)
        thumbs = [(n, shots[n]) for n in names][:24]
        if thumbs:
            tw, th = 240, 256
            cols = 6
            sheet = Image.new('RGB', (tw * cols, (th + 18) * math.ceil(len(thumbs) / cols)), (8, 10, 16))
            d = ImageDraw.Draw(sheet)
            for k, (n, im) in enumerate(thumbs):
                x, y = (k % cols) * tw, (k // cols) * (th + 18)
                sheet.paste(im.convert('RGB').resize((tw, th)), (x, y + 18))
                d.text((x + 4, y + 3), n[:38], fill=(255, 210, 120))
            sheet.save(os.path.join(a.out, '01_transformation_beats.png'))

        # ---- 2. inside that same stage-5 PLAY: somersault, roll, respawn, continue --------------------
        print('\n== manoeuvres and deaths in space ==', flush=True)
        pg.evaluate("() => { window.__P.alive(); player._somerCool = 0; player.somer = null; player.roll = null; player._rollCool = 0; player._tapU = -9; player.invuln = 0; return true; }")
        avail = pg.evaluate("() => ({so: somersaultAvailable()})")
        i0 = P.frame()
        pg.evaluate("() => { BOSSMODE.injectTap('w'); return true; }")
        P.step(1)
        pg.evaluate("() => { BOSSMODE.injectTap('w'); return true; }")
        so_shots, so_seen = [], set()
        for _ in range(90):
            P.step(1, rec=True, pause=2)
            cur = pg.evaluate("() => window.__P.log[window.__P.log.length-1]")
            k = cur['hull']['key'] if (cur['somer'] and cur['hull']) else None
            if k and k not in so_seen:          # one tile per frame of the reel the game actually drew
                so_seen.add(k)
                so_shots.append((cur, P.canvas()))
            if not cur['somer'] and cur['i'] - i0 > 6:
                break
        slog = P.log_from(i0)
        so_keys = sorted({s['hull']['key'] for s in slog if s['somer'] and s['hull']})
        P.ok(any(s['somer'] for s in slog), 'a double-tap UP somersaults in space (available=%s)' % avail['so'])
        P.ok(len([k for k in so_keys if k.startswith('ship_so_')]) >= 6 and not any(k.startswith('ship_roll_') for k in so_keys),
             'the somersault walks the spaceship PITCH reel, never the roll reel: %s' % so_keys)
        R['somersault_keys'] = so_keys
        pg.evaluate("() => { player._rollCool = 0; player._somerCool = 0; player.somer = null; startRoll(1); return !!player.roll; }")
        i0 = P.frame()
        P.step(40, rec=True, pause=5)
        rlog = P.log_from(i0)
        roll_keys = sorted({s['hull']['key'] for s in rlog if s['roll'] and s['hull']})
        P.ok(len([k for k in roll_keys if k.startswith('ship_roll_')]) >= 6 and not any(k.startswith('ship_so_') for k in roll_keys),
             'the barrel roll still walks the roll reel (%d roll frames)' % len(roll_keys))
        R['roll_keys'] = roll_keys

        dlog, spin_shots = death_route(P, 2, False, center=True)
        spin = [s for s in dlog if s['spin'] and not s['spin']['crashed'] and s['dead']]
        rots = sorted({s['spinRot'] for s in spin if s['spinRot'] is not None})
        aerr = max((s['anchorErr'] for s in spin if s['anchorErr'] is not None), default=None)
        R['death'] = {'spin_frames': len(spin), 'space_frames': sum(1 for s in spin if s['spinSpace']),
                      'plane_frames': sum(1 for s in spin if s['spinPlane']), 'rotations': rots, 'anchor_err': aerr}
        P.ok(len(spin) >= 30 and all(s['spinSpace'] for s in spin) and not any(s['spinPlane'] for s in spin),
             'the death spin-out turns the SPACESHIP on every spin frame (%d frames, %d space, %d plane reel)'
             % (len(spin), R['death']['space_frames'], R['death']['plane_frames']))
        P.ok(len(rots) >= 5, 'and it actually turns: %d distinct drawn angles' % len(rots))
        P.ok(aerr is not None and aerr <= 0.01, 'the fire and explosions stay anchored to it while it turns (worst %s px)' % aerr)
        after = [s for s in dlog if s['st'] == P.GS['PLAY'] and not s['dead'] and not s['spin']]
        P.ok(len(after) > 0 and sum(1 for s in after if s['hull']) > 0 and not any(s['planePlay'] for s in after),
             'after the respawn the spaceship flies again (%d frames, %d drew it, %d drew a plane)'
             % (len(after), sum(1 for s in after if s['hull']), sum(1 for s in after if s['planePlay'])))

        clog, _ = death_route(P, 0, True)
        cst = [s['st'] for s in clog]
        cafter = []
        seen_cont = False
        for s in clog:
            if s['st'] == P.GS['CONTINUE']:
                seen_cont = True
            elif seen_cont and s['st'] == P.GS['PLAY']:
                cafter.append(s)
        P.ok(seen_cont and len(cafter) > 0 and sum(1 for s in cafter if s['hull']) > 0 and not any(s['planePlay'] for s in cafter),
             'CONTINUE comes back in the spaceship (%s continue, %d play frames after, %d drew it, %d a plane)'
             % ('saw' if seen_cont else 'NO', len(cafter), sum(1 for s in cafter if s['hull']), sum(1 for s in cafter if s['planePlay'])))

        # proof: somersault strip + death spin strip, cropped around the player
        def crops(pairs, fname, title, field, label):
            if not pairs:
                return
            sx = pg.evaluate("() => window.__P.sx()")
            tiles = []
            for s, im in pairs:
                r = s.get(field)
                if not r:
                    continue
                # centred on the rect the game DREW (recorded off ctx.drawImage) - never on a recomputed camera, which
                # the first cut sampled after the fact and so framed an asteroid and the HUD instead of the ship
                box = (int((r['cx'] - 60) * sx), int((r['cy'] - 64) * sx), int((r['cx'] + 60) * sx), int((r['cy'] + 64) * sx))
                tiles.append((im.crop(box).convert('RGB').resize((180, 192)), label(s, r)))
            sh = Image.new('RGB', (180 * max(1, len(tiles)), 234), (8, 10, 16))
            dd = ImageDraw.Draw(sh)
            dd.text((6, 4), title, fill=(255, 210, 120))
            for k, (tile, lab) in enumerate(tiles):
                sh.paste(tile, (k * 180, 22))
                dd.text((k * 180 + 4, 218), lab, fill=(220, 222, 230))
            sh.save(os.path.join(a.out, fname))
        crops(so_shots, '05_somersault_space.png', 'somersault in space - one tile per pitch frame the game drew', 'hull',
              lambda s, r: '%s  h%.0f' % (r['key'], r['h']))
        crops(spin_shots, '04_death_spin_space.png', 'the spin-out in space - the spaceship turns, the fire rides it', 'spinR',
              lambda s, r: 'rot %+.0f deg  t%.2f' % (math.degrees(r['rot']), (s.get('spin') or {}).get('t') or 0))

        # ---- 3. direct stage-5 fights: BOSSMODE / debug list / capture harness, and shoot.py SETUP ------
        print('\n== direct entries ==', flush=True)
        play_route(P, 'BOSSMODE.start(5, boss)', "([pk]) => ({ok: BOSSMODE.start(5, 'boss', pk, false), st: state})", 'maverick')
        dshot = P.canvas()
        dshot.save(os.path.join(a.out, '03_direct_fight_stage5.png'))
        play_route(P, 'debugStartFight(stage 5 mini) - the capture harness route',
                   "([pk]) => { const e = debugFightFor(5, 'mini'); return {ok: debugStartFight(e, {pilot: pk}), name: e && e.name, st: state}; }", 'juggernaut')
        play_route(P, "shoot.py SETUP (beginStage(5) + setState(PLAY))",
                   "([pk]) => { debugFight = null; const i = PILOTS.findIndex(p => p.key === pk); if (i >= 0) pilotIndex = i; run.pilot = pk; beginStage(5); setState(GS.PLAY); player.reset(); return {st: state}; }", 'lizzie')

        # ---- 4. stage 9, then the rift return to stage 5 - it must NOT build the ship again -------------
        print('\n== stage 9 and the rift return ==', flush=True)
        P.wait_stage_loaded(9)
        pg.evaluate("""([pk]) => { window.__P.alive(); try { debugRecStop(); } catch (e) {}
            debugFight = null; run.mode = 'arcade'; run._s5ResumeArm = 0; coopOn = false; PENDING_STAGE = 1;
            const i = PILOTS.findIndex(p => p.key === pk); if (i >= 0) pilotIndex = i;
            startRun(9); if (state === GS.INTRO) stateT = 3.599; return state; }""", ['falva'])
        i9 = P.frame()
        for _ in range(400):
            P.step(20, rec=True)
            if pg.evaluate("() => state") == P.GS['PLAY']:
                break
            if pg.evaluate("() => drawLaunch._phase") == 'load':
                pg.wait_for_timeout(150)
        P.step(30, rec=True)
        l9 = [s for s in P.log_from(i9) if s['st'] == P.GS['LAUNCH']]
        ph9 = sorted({s['gm'] for s in l9 if s['gm']})
        P.ok(len(l9) > 0 and ph9 == ['active'] and not any(s['plane'] for s in l9),
             'the stage-9 launch flies the retained spaceship, no kit and no plane (phases %s, %d plane frames)'
             % (ph9, sum(1 for s in l9 if s['plane'])))
        hd9 = series_deltas([s for s in l9 if s['hull']], 'hull')
        R['stage9_hull_deltas'] = hd9
        P.ok(hd9['h'][0] <= 2.0 and hd9['cy'][0] <= 4.5 and hd9['cx'][0] <= 4.5,
             'and carries it without a size or position jump (worst dh %.2f @%s, dcy %.2f @%s, dcx %.2f)'
             % (hd9['h'][0], hd9['h'][1], hd9['cy'][0], hd9['cy'][1], hd9['cx'][0]))
        pg.evaluate("""() => { run.mode = 'campaign'; try { campaign.unlockedMax = Math.max(campaign.unlockedMax||1, 8); campaign._booted = true; } catch (e) {}
            window.__P.alive(); riftFallbackStart(); return state; }""")
        route = 'riftFallback -> map -> riftReturn -> sselDeploy -> beginStage(5)'
        reached = False
        for _ in range(160):
            P.step(20, rec=False, pause=20)
            s = pg.evaluate("() => ({st: state, stage: run.stage})")
            if s['st'] == P.GS['INTRO'] and s['stage'] == 5:
                reached = True
                break
        if not reached:
            route = 'DIRECT (the map did not deploy in time): run._s5ResumeArm=1; beginStage(5)'
            pg.evaluate("() => { run._s5GateOut = 1; run._s9taken = 1; run._s5ResumeArm = 1; beginStage(5); return state; }")
        R['rift_route'] = route
        pg.evaluate("() => { if (state === GS.INTRO) stateT = 3.599; return true; }")
        i5 = P.frame()
        rshot = None
        for _ in range(500):
            P.step(20, rec=True)
            cur = pg.evaluate("() => window.__P.log[window.__P.log.length-1]")
            if cur['st'] == P.GS['LAUNCH'] and rshot is None and cur['ph'] == 'settle':
                rshot = P.canvas()
            if cur['st'] == P.GS['PLAY']:
                break
            if cur['ph'] == 'load':
                pg.wait_for_timeout(150)
        P.step(40, rec=True)
        if rshot is None:
            rshot = P.canvas()
        rshot.save(os.path.join(a.out, '06_stage9_return_no_replay.png'))
        rl = P.log_from(i5)
        rlaunch = [s for s in rl if s['st'] == P.GS['LAUNCH']]
        rph = sorted({s['gm'] for s in rlaunch if s['gm']})
        rplay = [s for s in rl if s['st'] == P.GS['PLAY']]
        R['rift_return'] = {'route': route, 'phases': rph, 'ready_flag': rlaunch[0]['ready'] if rlaunch else None,
                            'plane_frames': sum(1 for s in rlaunch if s['plane']), 'launch_frames': len(rlaunch),
                            'launch_hull_frames': sum(1 for s in rlaunch if s['hull'])}
        P.ok(len(rlaunch) > 0 and rph == ['active'] and not any(s['plane'] for s in rlaunch),
             'the return to stage 5 does NOT replay the transformation (%s; phases %s, %d plane frames, gravityShipReady %s)'
             % (route.split(' ')[0], rph, R['rift_return']['plane_frames'], R['rift_return']['ready_flag']))
        P.ok(sum(1 for s in rplay if s['hull']) > 0 and not any(s['planePlay'] for s in rplay),
             'and stage 5 plays on in the spaceship (%d play frames drew it)' % sum(1 for s in rplay if s['hull']))
        hdr = series_deltas([s for s in rlaunch if s['hull']], 'hull')
        hs = [s['hull']['h'] for s in rlaunch if s['hull']]
        R['rift_return']['hull_deltas'] = hdr
        R['rift_return']['hull_h'] = [round(min(hs), 1), round(max(hs), 1)] if hs else None
        P.ok(hdr['h'][0] <= 2.0 and hdr['cy'][0] <= 4.5 and hdr['cx'][0] <= 4.5,
             'its launch carries the ship without a jump (worst dh %.2f @%s, dcy %.2f @%s; drawn %s px)'
             % (hdr['h'][0], hdr['h'][1], hdr['cy'][0], hdr['cy'][1], R['rift_return']['hull_h']))

        # ---- 5. all nine palettes, live ----------------------------------------------------------------
        print('\n== the nine palettes ==', flush=True)
        means, tiles = {}, {}
        for pk in PILOTS:
            pg.evaluate("([pk]) => { window.__P.alive(); return BOSSMODE.start(5, 'mini', pk, false); }", [pk])
            got = None
            for _ in range(20):
                P.step(10, rec=True, pause=30)
                cur = pg.evaluate("() => window.__P.log[window.__P.log.length-1]")
                if cur['hull'] and cur['st'] == P.GS['PLAY'] and cur['hull']['key'] == 'ship_base':
                    got = cur
                    break
            means[pk] = pg.evaluate("([pk]) => window.__P.paletteMean(pk)", [pk])
            if got:
                sx = pg.evaluate("() => window.__P.sx()")
                im = P.canvas()
                h = got['hull']
                box = (int((h['cx'] - h['w'] * 0.85) * sx), int((h['cy'] - h['h'] * 0.62) * sx),
                       int((h['cx'] + h['w'] * 0.85) * sx), int((h['cy'] + h['h'] * 1.05) * sx))
                tiles[pk] = im.crop(box).convert('RGB')

        def lab(rgb):
            def f(c):
                c /= 255.0
                return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
            r, g, b = (f(float(v)) for v in rgb)
            X = (0.4124 * r + 0.3576 * g + 0.1805 * b) / 0.95047
            Y = (0.2126 * r + 0.7152 * g + 0.0722 * b)
            Z = (0.0193 * r + 0.1192 * g + 0.9505 * b) / 1.08883
            ff = lambda t: t ** (1 / 3) if t > 0.008856 else 7.787 * t + 16 / 116
            return (116 * ff(Y) - 16, 500 * (ff(X) - ff(Y)), 200 * (ff(Y) - ff(Z)))
        labs = {k: lab(v) for k, v in means.items() if v}
        pairs = sorted((math.dist(labs[x], labs[y]), x, y) for x, y in itertools.combinations(sorted(labs), 2))
        R['palette_means'] = {k: [round(c, 1) for c in v] if v else None for k, v in means.items()}
        R['palette_closest'] = [(round(d, 1), x, y) for d, x, y in pairs[:4]]
        chroma = {k: math.hypot(v[1], v[2]) for k, v in labs.items()}
        R['palette_chroma'] = {k: round(v, 1) for k, v in chroma.items()}
        cole_h = colorsys.rgb_to_hsv(*[c / 255.0 for c in means['cole']])[0] * 360 if means.get('cole') else None
        P.ok(len(labs) == 9 and pairs and pairs[0][0] >= 10.0,
             'all nine palettes are distinct (closest pair %s dE %.1f)' % ('/'.join(pairs[0][1:]), pairs[0][0]) if pairs else 'palettes missing')
        P.ok(all(v >= 15 for v in chroma.values()), 'no pilot flies an uncoloured ship (lowest chroma %.1f)' % min(chroma.values()) if chroma else 'no chroma')
        P.ok(cole_h is not None and 70 <= cole_h <= 150, "Cole's ship is green (hue %.0f)" % (cole_h or -1))
        if tiles:
            from PIL import Image as _I
            import re as _re
            man = open(os.path.join(ROOT, 'assets', 'manifest.js'), encoding='utf-8').read()
            TW, TH = 150, 300
            sheet = _I.new('RGB', (TW * 9, TH), (8, 10, 16))
            d = ImageDraw.Draw(sheet)
            for k, pk in enumerate(PILOTS):
                x = k * TW
                d.text((x + 6, 4), pk.upper(), fill=(235, 235, 240))
                t = tiles.get(pk)
                if t:
                    s = 150 / t.height
                    t2 = t.resize((max(1, int(t.width * s)), 150))
                    sheet.paste(t2, (x + (TW - t2.width) // 2, 20))
                m = _re.search(r'"ship_%s":\[([0-9,]+)\]' % pk, man)
                sh = _re.search(r'"nsa_ship_%s":"([^"]+)"' % pk, man)
                if m and sh:
                    xx, yy, ww, hh, ox, oy, cw, ch = [int(v) for v in m.group(1).split(',')]
                    src = _I.open(os.path.join(ROOT, sh.group(1))).convert('RGBA')
                    cvp = _I.new('RGBA', (cw, ch), (0, 0, 0, 0)); cvp.paste(src.crop((xx, yy, xx + ww, yy + hh)), (ox, oy))
                    s = 100 / ch
                    cvp = cvp.resize((max(1, int(cw * s)), 100))
                    bg = _I.new('RGBA', cvp.size, (8, 10, 16, 255)); bg.alpha_composite(cvp)
                    sheet.paste(bg.convert('RGB'), (x + (TW - cvp.width) // 2, 186))
                mv = means.get(pk)
                if mv:
                    d.rectangle((x + 20, 290 - 6, x + TW - 20, 296), fill=tuple(int(c) for c in mv))
            sheet.save(os.path.join(a.out, '07_nine_palettes_live.png'))

        # ---- 6. the size / position track --------------------------------------------------------------
        def track(logs, fname):
            W_, H_ = 1400, 520
            img = Image.new('RGB', (W_, H_), (10, 12, 18))
            d = ImageDraw.Draw(img)
            L0 = [s for s in logs[0][1] if s['st'] in (P.GS['LAUNCH'], P.GS['PLAY'])]
            if not L0:
                return
            n = max(len([s for s in lg if s['st'] in (P.GS['LAUNCH'], P.GS['PLAY'])]) for _, lg in logs)
            X = lambda k: 60 + k * (W_ - 80) / max(1, n)
            Yh = lambda v: 250 - v * 1.6
            Yy = lambda v: 510 - v * 0.5
            d.text((8, 6), 'drawn HEIGHT of the craft (top, px) and centre Y (bottom, px) per frame, stage-5 launch -> PLAY', fill=(255, 210, 120))
            palette = {'before': ((95, 95, 105), (165, 165, 175)), 'now': ((110, 220, 255), (255, 170, 60))}
            for li, (name, lg) in enumerate(logs):
                cols = {li: palette.get(name, palette['now'])}     # plane / ship colour by series, not by slot
                L = [s for s in lg if s['st'] in (P.GS['LAUNCH'], P.GS['PLAY'])]
                ph_prev = None
                for k, s in enumerate(L):
                    tag = ((s['ph'] or '?') if s['st'] == P.GS['LAUNCH'] else 'PLAY') + ('/' + s['gm'] if s['gm'] and s['gm'] != 'active' else '')
                    if li == len(logs) - 1 and tag != ph_prev:
                        d.line((X(k), 24, X(k), H_ - 4), fill=(40, 44, 56))
                        d.text((X(k) + 2, 24 + (k % 3) * 11), tag[:16], fill=(150, 150, 170))
                        ph_prev = tag
                for fld, colr in (('plane', cols[li][0]), ('hull', cols[li][1])):
                    pts_h, pts_y = [], []
                    for k, s in enumerate(L):
                        r = s.get(fld)
                        if r:
                            pts_h.append((X(k), Yh(r['h']))); pts_y.append((X(k), Yy(r['cy'])))
                        else:
                            if len(pts_h) > 1:
                                d.line(pts_h, fill=colr, width=2); d.line(pts_y, fill=colr, width=2)
                            pts_h, pts_y = [], []
                    if len(pts_h) > 1:
                        d.line(pts_h, fill=colr, width=2); d.line(pts_y, fill=colr, width=2)
                d.text((W_ - 300, 8 + li * 14), '%s: plane / ship' % name, fill=cols[li][1])
            img.save(os.path.join(a.out, fname))
        logs = []
        if a.compare and os.path.exists(a.compare):
            try:
                logs.append(('before', json.load(open(a.compare))['cinematic_log']))
            except Exception as e:
                print('compare failed', e)
        logs.append(('now', log))
        try:
            track(logs, '02_drawn_size_track.png')
        except Exception as e:
            print('track plot failed:', e)

        R['overlay_served'] = sorted(set(overlay_served))
        R['page_errors'] = page_errors[:20]
        R['console_errors'] = console_errors[:20]
        R['step_error'] = pg.evaluate("() => window.__P.err")
        P.ok(not page_errors and not console_errors and not R['step_error'],
             '0 page errors, 0 console errors, 0 loop throws (%d / %d / %s)' % (len(page_errors), len(console_errors), R['step_error']))
        br.close()
    stop()
    R['seconds'] = round(time.time() - t_start, 1)
    R['summary'] = {'ok': len(P.oks), 'fail': len(P.fails), 'fails': P.fails}
    json.dump(R, open(os.path.join(a.out, 'report.json'), 'w'), indent=1, default=str)
    print('\n%d ok / %d fail  (%.0fs)' % (len(P.oks), len(P.fails), R['seconds']))
    for f in P.fails:
        print('  FAIL', f)
    for e in (page_errors + console_errors)[:10]:
        print('  error:', e)
    sys.exit(1 if P.fails else 0)


if __name__ == '__main__':
    main()
