#!/usr/bin/env python3
"""
probe_tempest_0913b.py - THE TEMPEST LEVIATHAN, STAGE 6's MINIBOSS JET DUEL, IN REAL CHROMIUM.

    python3 _BUILD_SOURCE/probe_tempest_0913b.py                  # proofs -> docs/proofs/tempest_0913b/
    python3 _BUILD_SOURCE/probe_tempest_0913b.py --out DIR --overlay DIR [--repo REPO]
        --overlay serves every file under DIR in place of the repo's copy at the same path (DIR/assets/game.js,
        DIR/assets/game/bosses/tempest/tlv_*.png), so a patch can be proved BEFORE it is applied. The integrator,
        running it inside the patched repo, passes neither.

Mike, 0912: "this is our new mini-boss and fighting style for level 6's miniboss" and "Showcase the new level 6
mini boss dual ship fight".

Drives the REAL game through shoot.py's server, TRAP_RAF and STEP, and the real spawn path - BOSSMODE.start(6,'mini'),
which raises the sub-boss warning and lets updatePlay spawn SUBBOSS[6]:
  * stage 6's miniboss IS the Tempest Leviathan and it arrives through the warning
  * the draw ASKS FOR every tlv_ plate - recorded by wrapping XART.get, which returns an object with no stable
    identity and no .src (0905h) - and the barrage reel it borrows
  * the hull blit carries NO rotation: ctx.getTransform() at the drawImage itself (ctx OWNS drawImage - 0905h)
  * EVERY tempestUpdate moves the hull on ONE axis (wrapped by caller: a top-level declaration is reassignable)
  * while targetable the hull top never enters the 77px gauge band
  * PIXELS: the hull region against the same region with the jet moved away - a key asked for is not a pixel
  * a REAL player round on a live aperture takes its pool and leaves the bar alone; a round over bare air flies on;
    a real killing round silences the aperture - no beam and no bolt from it afterwards - and costs the hull its share
  * the gates advance at 75/50/25% driven through hitSubBoss, and a round mid-crossing does nothing; the jet crosses
    BELOW the player for the pursuit and back ABOVE for hell, and the player is never moved
  * a ram starts at a CAMERA edge and crosses the screen flat on its row
  * a hell dive: ONE retina, needles one at a time, every one lock-bound
  * the kill runs the ordinary sub-boss death and frees the slot
  * the sound keys fire (Audio.SFX wrapped), and enemyMachineShotHeavy has a TAME row and its file serves 200
  * zero page errors and zero console errors - a draw that throws is swallowed and simply never appears
The pilot is kept alive by STUBBING playerHit, never by pinning invuln (0912v: invuln 99999 hides the ship).
Writes <out>/01..08_*.png and <out>/_contact.png. LOOK AT THEM: no number here can see a hull in the wrong place.
"""
import os, sys, io, base64, argparse, importlib.util, traceback

HERE = os.path.dirname(os.path.abspath(__file__))

HOOK = r"""
() => {
  const W = window.__tl = window.__tl || {};
  W.keys = {}; W.snd = W.snd || {}; W.steps = 0; W.diag = 0; W.xs = 0; W.ys = 0; W.bandMin = 1e9; W.vulnFrames = 0;
  W.hullBlits = 0; W.rot = 0; W.hits = 0; W.bolts = []; W.beamIds = {}; W.rams = []; W.seenNeedles = new WeakSet();
  W.playerMoves = 0;
  if (W.hooked) return 'rehooked';
  W.hooked = true;
  const og = XART.get.bind(XART);
  XART.get = function (k) {
    if (typeof k === 'string' && (k.indexOf('tlv_') === 0 || k.indexOf('nxp_barrage_') === 0)) W.keys[k] = (W.keys[k] || 0) + 1;
    return og(k);
  };
  const ou = window.tempestUpdate;
  window.tempestUpdate = function (b, dt) {
    const x0 = b.x, y0 = b.y, px = player.x, py = player.y, r = ou(b, dt);
    W.steps++;
    const dx = Math.abs(b.x - x0) > 1e-9, dy = Math.abs(b.y - y0) > 1e-9;
    if (dx && dy) W.diag++; if (dx) W.xs++; if (dy) W.ys++;
    if (player.x !== px || player.y !== py) W.playerMoves++;
    const T = b._tlv;
    if (T && T.vuln && !b.dead) { W.vulnFrames++; W.bandMin = Math.min(W.bandMin, b.y - b._drawH / 2); }
    return r;
  };
  const od = window.tempestDraw;
  window.tempestDraw = function (b) { W.inDraw = b; try { return od(b); } finally { W.inDraw = null; } };
  const odi = ctx.drawImage;
  ctx.drawImage = function (im) {
    if (W.inDraw && arguments.length === 5 && Math.abs(arguments[3] - W.inDraw._drawW) < 1.5 && Math.abs(arguments[4] - W.inDraw._drawH) < 1.5) {
      const m = ctx.getTransform(); W.hullBlits++;
      if (Math.abs(m.b) > 1e-6 || Math.abs(m.c) > 1e-6) W.rot++;
    }
    return odi.apply(this, arguments);
  };
  const ob = window.tempestBolts;
  window.tempestBolts = function (b, t, dir, rapid) {
    const n0 = eBullets.length, r = ob(b, t, dir, rapid);
    for (let i = n0; i < eBullets.length; i++) { const q = eBullets[i];
      if (q && q.kind === 'tlvBolt') W.bolts.push([Math.round((q.x - b.x) * 10) / 10, q.vy > 0 ? 1 : -1]); }
    return r;
  };
  const ol = window.tempestLasers;
  window.tempestLasers = function (b, dir, t, warn, dur) {
    const r = ol(b, dir, t, warn, dur);
    for (const q of b._tlv.beams) if (q.active) W.beamIds[q.id] = (W.beamIds[q.id] || 0) + 1;
    return r;
  };
  const oc = window.tempestChange;
  window.tempestChange = function (b, state) {
    const prev = b._tlv.state, r = oc(b, state);
    if (state === 'ram') W.rams.push({x0: b.x, y: b.y, L: camLeftX(), R: camRightX(), side: b._tlv.side});
    if (prev === 'ram' && state === 'punish-rise' && W.rams.length) { const k = W.rams[W.rams.length - 1];
      if (k.x1 == null) { k.x1 = b.x; k.y1 = b.y; k.L1 = camLeftX(); k.R1 = camRightX(); } }
    return r;
  };
  window.playerHit = function () { W.hits++; };
  for (const n of ['enemyMachineShotHeavy', 'enemyPulseLaserBlue', 'maverickHelixRelease', 'explosionAirSmall01',
                   'explosionJetBreakup', 'explosionBossCore', 'retinaCharge', 'retinaLockBeep']) {
    const f = Audio.SFX[n]; W.snd[n] = 0;
    Audio.SFX[n] = function () { W.snd[n]++; return f && f.apply(this, arguments); };
  }
  return 'hooked';
}
"""

STATE = r"""
() => {
  const b = (typeof subBoss !== 'undefined') ? subBoss : null;
  if (!b || !b._tlv) return {none: true, subBossDone: (typeof subBossDone !== 'undefined') ? subBossDone : null};
  const T = b._tlv;
  return {phase: T.phase, state: T.state, t: T.t, st: T.st, x: b.x, y: b.y, hp: b.hp, maxhp: b.maxhp, dead: !!b.dead,
    dying: b.dying || 0, vuln: T.vuln, cross: !!T.cross, ramWarn: !!T.ramWarn, ap: T.ap.map(function (A) { return A.hp; }),
    beams: T.beams.map(function (q) { return [q.id, q.active ? 1 : 0]; }), hist: T.history.join('>'),
    locks: playerLocks.filter(function (L) { return L.src === b; }).length, py: player.y,
    needles: eBullets.filter(function (q) { return q.kind === 'tlvNeedle' && !q.dead; }).length};
}
"""

NEW_NEEDLES = r"""
() => { const W = window.__tl, out = [];
  for (const q of eBullets) { if (q.kind !== 'tlvNeedle' || W.seenNeedles.has(q)) continue; W.seenNeedles.add(q); out.push(!!q._lockId); }
  return out; }
"""

GATE_HIT = r"""
() => { const b = subBoss, T = b._tlv, m = b.maxhp; hitSubBoss(m * 5, b.x, b.y); return T.phase + '@' + Math.round(b.hp / m * 100); }
"""

GEO = r"""
() => { const b = subBoss; const cam = (worldWidth() > viewW()) ? camX : 0;
  return {x: b.x, y: b.y, w: b._drawW, h: b._drawH, cam: cam, vh: VH, vw: viewW(),
          vz: (typeof viewZoom === 'function' ? viewZoom() : 1), stage: run.stage, worldW: worldWidth()}; }
"""

CAP = "() => { const c = document.getElementById('screen'); return c ? c.toDataURL('image/png') : null; }"


def n(v, spec='.1f'):
    """format a number that may not have arrived"""
    return format(v, spec) if isinstance(v, (int, float)) else str(v)


def main():
    ap = argparse.ArgumentParser(description='The Tempest Leviathan in real Chromium')
    ap.add_argument('--out', default=None, help='proof directory (default: <repo>/docs/proofs/tempest_0913b)')
    ap.add_argument('--overlay', default=None, help='serve files under this directory in place of the repo copies')
    ap.add_argument('--repo', default=None, help="the BulletsOfFury root (default: this file's parent directory)")
    a = ap.parse_args()

    repo = a.repo or os.path.dirname(HERE)
    shoot_py = os.path.join(repo, '_BUILD_SOURCE', 'shoot.py')
    if not os.path.isfile(shoot_py):
        print('no shoot.py under', repo, '- pass --repo'); return 2
    spec = importlib.util.spec_from_file_location('shoot', shoot_py)
    sh = importlib.util.module_from_spec(spec); spec.loader.exec_module(sh)
    from playwright.sync_api import sync_playwright
    from PIL import Image, ImageDraw

    out = a.out or os.path.join(repo, 'docs', 'proofs', 'tempest_0913b')
    os.makedirs(out, exist_ok=True)
    fails, n_ok, errs, caps = [], [0], [], []

    def ok(c, m):
        if c: n_ok[0] += 1; print('  ok  ', m, flush=True)
        else: fails.append(m); print('  FAIL', m, flush=True)

    def to_img(d):
        return Image.open(io.BytesIO(base64.b64decode(d.split(',', 1)[1]))).convert('RGB')

    port, stop = sh.serve(repo)
    with sync_playwright() as p:
        br = p.chromium.launch(args=['--disable-gpu', '--no-sandbox', '--mute-audio'])
        pg = br.new_page(viewport={'width': 1100, 'height': 1200})
        pg.on('pageerror', lambda e: errs.append('pageerror: ' + str(e)[:220]))
        pg.on('console', lambda m: errs.append('console.error: ' + m.text[:220]) if m.type == 'error' else None)
        if a.overlay:
            ov = os.path.abspath(a.overlay)
            def _serve(fpath):
                # ONE parameter: Playwright hands a two-parameter handler (route, request)
                def _h(route):
                    route.fulfill(path=fpath)
                return _h
            for root, _d, files in os.walk(ov):
                for fn in files:
                    full = os.path.join(root, fn)
                    rel = os.path.relpath(full, ov).replace(os.sep, '/')
                    pg.route('http://127.0.0.1:%d/%s' % (port, rel), _serve(full))
                    print('overlay:', rel, flush=True)

        def step(k, wait=18):
            e = pg.evaluate(sh.STEP, k)
            if e: errs.append('STEP threw: ' + str(e)[:200])
            if wait: pg.wait_for_timeout(wait)

        def st():
            return pg.evaluate(STATE)

        def until(cond, frames, per=2, each=None):
            s = st()
            for _ in range(0, frames, per):
                if cond(s): return s
                step(per)
                s = st()
                if each: each(s)
            return s

        def shot(name, label):
            d = pg.evaluate(CAP)
            if not d: return None
            im = to_img(d); im.save(os.path.join(out, name)); caps.append((label, im)); return im

        def guard(label, fn):
            try:
                fn()
            except Exception as e:
                traceback.print_exc()
                ok(False, '%s: the probe itself threw %r' % (label, e))

        ctx = {}

        # ---------------- boot and the real spawn ----------------
        pg.goto('http://127.0.0.1:%d/index.html' % port, wait_until='load', timeout=120000)
        pg.wait_for_function("() => typeof state!=='undefined' && (window.__bofFrames|0) > 4", timeout=120000)
        pg.evaluate(sh.TRAP_RAF); pg.wait_for_timeout(60)
        pg.evaluate("() => { ASSETS.ready = true; }")
        slot = pg.evaluate("() => ({kind: SUBBOSS[6].kind, alt: (typeof ALTBOSS!=='undefined' && ALTBOSS[6]) ? ALTBOSS[6].kind : null, "
                           "name: BOSSMODE.name(SUBBOSS[6].kind), rig: typeof tempestInit})")
        print('slot', slot, flush=True)
        ok(slot['kind'] == 'tempestleviathan' and slot['rig'] == 'function',
           "stage 6's miniboss is the TEMPEST LEVIATHAN (SUBBOSS[6].kind = %s)" % slot['kind'])
        ok(slot['alt'] == 'blacksteel' and slot['name'] == 'TEMPEST LEVIATHAN',
           'the Blacksteel is ALTBOSS[6] and the fight list names it %s' % slot['name'])
        started = pg.evaluate("() => !!BOSSMODE.start(6, 'mini', 'cole', false)")
        s = st()
        for _ in range(240):
            if not s.get('none'): break
            step(6, 12); s = st()
        ok(started and not s.get('none'), "BOSSMODE.start(6,'mini') raised the warning and updatePlay spawned it (%s)" % s.get('phase'))
        if s.get('none'):
            br.close(); stop(); print('\n%d ok / %d fail' % (n_ok[0], len(fails))); return 1
        print('hook', pg.evaluate(HOOK), flush=True)
        warm = ['tlv_hull', 'tlv_hull_damaged', 'tlv_beam', 'tlv_charge', 'tlv_bolt', 'tlv_needle'] + \
               ['nxp_barrage_%d' % i for i in range(8)] + ['nsd_chim_%d' % i for i in range(8)]
        rdy = []
        for _ in range(40):      # XART.rdy is false on its first call - poll with REAL waits so the decodes land (0905)
            rdy = pg.evaluate("(ks) => ks.map(function(k){ return XART.rdy(k); })", warm)
            if all(rdy): break
            step(2, 90)
        ok(all(rdy), 'every tlv_ plate and both borrowed reels decode (%d/%d)' % (sum(1 for r in rdy if r), len(warm)))

        # ---------------- arrival -> chase, its weapons, pixels ----------------
        def chase():
            s = until(lambda s: s.get('phase') == 'chase', 600)
            ok(s.get('phase') == 'chase', 'it flies in and opens the CHASE (%s)' % s.get('hist'))
            pg.evaluate("() => { window.__tl.keys = {}; }")
            got = [False]
            def grab(s):
                if not got[0] and any(q[1] for q in s.get('beams', [])):
                    got[0] = True; shot('01_chase_rear_lasers.png', 'chase: twin rear lasers')
            until(lambda s: False, 330, 2, grab)
            if not got[0]: shot('01_chase_rear_lasers.png', 'chase (no beam caught)')
            keys = pg.evaluate("() => window.__tl.keys")
            ok(all(keys.get(k) for k in ['tlv_hull', 'tlv_bolt', 'tlv_beam', 'tlv_charge']),
               'the chase draw asks for its own plates: %s' % sorted(k for k in keys if k.startswith('tlv_')))
        guard('chase', chase)

        def pixels():
            until(lambda s: s.get('phase') == 'chase' and s.get('state') in ('strafe', 'climb', 'laser-track'), 240, 1)
            pg.evaluate("() => { subBoss.x += 5000; }"); step(1, 40)
            base = to_img(pg.evaluate(CAP))
            pg.evaluate("() => { subBoss.x -= 5000; }"); step(1, 40)
            g = pg.evaluate(GEO); withb = to_img(pg.evaluate(CAP))
            ctx['geo'] = g
            sc = withb.width / float(g['vw']); vz = g['vz'] or 1.0
            cx = (g['x'] - g['cam']) * vz * sc; cy = (g['y'] * vz + g['vh'] * (1 - vz)) * sc
            box = (int(cx - g['w'] * 0.4 * sc), int(cy - g['h'] * 0.4 * sc), int(cx + g['w'] * 0.4 * sc), int(cy + g['h'] * 0.4 * sc))
            m1 = base.crop(box).resize((1, 1), Image.BOX).getpixel((0, 0)); m2 = withb.crop(box).resize((1, 1), Image.BOX).getpixel((0, 0))
            diff = sum(abs(x - y) for x, y in zip(m1, m2))
            def cyan(im):
                raw = im.crop(box).tobytes(); c = 0
                for i in range(0, len(raw), 3):
                    if raw[i + 2] > 190 and raw[i + 1] > 160 and raw[i] < 150: c += 1
                return c
            cb, cw = cyan(base), cyan(withb)
            print('pixels box %s mean without %s with %s | cyan without %d with %d | geo %s' % (box, m1, m2, cb, cw, g), flush=True)
            ok(diff > 25 and cw > cb + 12, 'PIXELS: the hull lands where the jet is - mean shift %d, cyan aperture pixels %d -> %d' % (diff, cb, cw))
        guard('pixels', pixels)

        # ---------------- apertures, with REAL player rounds ----------------
        def apertures():
            until(lambda s: s.get('vuln') and s.get('phase') == 'chase', 240, 1)
            r = pg.evaluate("""() => { const b=subBoss, T=b._tlv, p=tempestPortXY(b,1);
              const air={x:b.x+TLV_HULL_BOX[0]*TLV_S+4, y:b.y, vx:0, vy:0, w:2, h:2, dmg:1, t:0};
              window.__tl.air=air;
              pBullets.push({x:p.x, y:p.y, vx:0, vy:0, w:4, h:8, dmg:1, t:0}); pBullets.push(air); return {a0:T.ap[1].hp, h0:b.hp}; }""")
            step(1, 0)
            r2 = pg.evaluate("() => { const b=subBoss, T=b._tlv, W=window.__tl; const alive=pBullets.indexOf(W.air)>=0 && !W.air.dead; W.air.dead=true; return {a1:T.ap[1].hp, h1:b.hp, airAlive:alive}; }")
            ok(r2['a1'] < r['a0'] and r2['h1'] == r['h0'], 'a REAL round on the rear-left aperture takes ITS pool (%s -> %s) and leaves the bar (%s)' % (r['a0'], r2['a1'], r2['h1']))
            ok(r2['airAlive'], 'and a round over bare air beside the hull flies on - only a live part stops a shot (0805c)')
            until(lambda s: s.get('vuln') and s.get('phase') == 'chase', 240, 1)
            # ONE killing round: a second one would land on the plug, which is hull, and ride the bar to the gate
            pg.evaluate("() => { const b=subBoss, p=tempestPortXY(b,1); window.__tl.h0=b.hp; pBullets.push({x:p.x, y:p.y, vx:0, vy:0, w:4, h:8, dmg:9999, t:0}); }")
            step(1, 0)
            r3 = pg.evaluate("() => { const b=subBoss, T=b._tlv, W=window.__tl; W.bolts=[]; W.beamIds={}; return {a:T.ap.map(function(A){return A.hp;}), cost:1-b.hp/W.h0, want:TLV_AP_COST, phase:T.phase}; }")
            ok(r3['a'][1] == 0 and abs(r3['cost'] - r3['want']) < 0.002 and r3['phase'] == 'chase',
               'one real killing round destroys it and the hull pays its share (%s of the bar, the pack\'s 90/8000 = %s)' % (n(r3['cost'], '.4f'), n(r3['want'], '.4f')))
            got = [False]
            def grab(s):
                if not got[0] and any(q[1] for q in s.get('beams', [])):
                    got[0] = True; shot('02_aperture_silenced.png', 'rear-left aperture silenced')
            until(lambda s: s.get('phase') != 'chase', 460, 2, grab)
            if not got[0]: shot('02_aperture_silenced.png', 'aperture silenced (no beam caught)')
            sil = pg.evaluate("() => ({bolts: window.__tl.bolts, beams: window.__tl.beamIds})")
            rear = [q for q in sil['bolts'] if q[1] > 0]
            left_rear = [q for q in rear if q[0] < 0]
            ok(len(rear) > 0 and not left_rear and sil['beams'].get('3') and not sil['beams'].get('1'),
               'SILENCED: %d rear bolts since, %d from the dead aperture; active beam frames by aperture %s' % (len(rear), len(left_rear), sil['beams']))
        guard('apertures', apertures)

        # ---------------- the gates, through hitSubBoss ----------------
        def overtake():
            until(lambda s: s.get('vuln') and s.get('phase') == 'chase', 240, 1)
            g1 = pg.evaluate(GATE_HIT)
            step(8, 20)
            shrug = pg.evaluate("() => { const b=subBoss, h=b.hp; hitSubBoss(b.maxhp,b.x,b.y); return {same: b.hp===h, cross: !!b._tlv.cross}; }")
            ok(g1 == 'overtake@75', 'a 5x overkill on the hull stops at the 75%% gate and starts the OVERTAKE (%s)' % g1)
            ok(shrug['same'] and shrug['cross'], 'a round while the jet crosses the player does nothing')
            s0 = st()
            got = [False]
            def grab(s):
                if not got[0] and s.get('cross') and (s.get('t') or 0) > 0.15:
                    got[0] = True; shot('03_overtake_band.png', 'overtake: warning band, jet crossing')
            s = until(lambda s: s.get('phase') == 'pursuit', 600, 2, grab)
            ok(s.get('phase') == 'pursuit' and isinstance(s.get('y'), (int, float)) and s['y'] > s['py'],
               'the jet crosses BELOW the player on its own column (y %s -> %s, player %s) and the pursuit begins' % (n(s0.get('y'), '.0f'), n(s.get('y'), '.0f'), n(s.get('py'), '.0f')))
        guard('overtake', overtake)

        def pursuit():
            got = [False]
            def grab(s):
                if not got[0] and s.get('state') == 'ram-warn' and (s.get('st') or 0) > 0.12:
                    got[0] = True; shot('04_ram_band.png', 'pursuit: side-ram warning band')
            until(lambda s: len(pg.evaluate("() => window.__tl.rams.filter(function(k){return k.x1!=null;})")) >= 1, 900, 2, grab)
            rams = pg.evaluate("() => window.__tl.rams")
            done = [k for k in rams if k.get('x1') is not None]
            if not done:
                ok(False, 'no ram completed in the pursuit window (%s)' % rams); return
            k = done[0]
            start_in = min(k['x0'] - k['L'], k['R'] - k['x0']); end_in = min(k['x1'] - k['L1'], k['R1'] - k['x1'])
            ok(start_in <= 60, 'a ram starts at a CAMERA edge: %spx in from it (camera %s..%s on a %s world)' % (n(start_in), n(k['L'], '.0f'), n(k['R'], '.0f'), (ctx.get('geo') or {}).get('worldW')))
            ok(abs(k['x1'] - k['x0']) >= (k['R'] - k['L']) - 120 and end_in <= 60 and abs(k['y1'] - k['y']) < 1e-6,
               'and runs the whole screen flat on its row (%spx, ending %spx from the far edge)' % (n(abs(k['x1'] - k['x0']), '.0f'), n(end_in)))
            until(lambda s: s.get('vuln'), 120, 1)
            g2 = pg.evaluate(GATE_HIT)
            ok(g2 == 'return@50', 'the 50%% gate starts the RETURN (%s)' % g2)
            s = until(lambda s: s.get('phase') == 'hell', 600)
            ok(s.get('phase') == 'hell' and isinstance(s.get('y'), (int, float)) and s['y'] < s['py'],
               'the jet climbs back ABOVE the player (y %s, player %s) and HELL begins' % (n(s.get('y'), '.0f'), n(s.get('py'), '.0f')))
        guard('pursuit', pursuit)

        # ---------------- hell: needles on the retina ----------------
        def hell():
            until(lambda s: s.get('state') == 'dive', 600, 1)
            pg.evaluate(NEW_NEEDLES)
            per, total, bound, retinas, got = 0, 0, 0, 0, False
            for _ in range(80):
                step(1, 10)
                fresh = pg.evaluate(NEW_NEEDLES); s = st()
                per = max(per, len(fresh)); total += len(fresh); bound += sum(1 for f in fresh if f)
                retinas = max(retinas, s.get('locks', 0) or 0)
                if not got and (s.get('needles') or 0) > 0:
                    got = True; shot('05_hell_needles.png', 'hell: needles on the retina')
            if not got: shot('05_hell_needles.png', 'hell dive (no needle caught)')
            ok(retinas == 1 and total >= 1 and per == 1 and bound == total,
               'a hell dive puts ONE retina on the player; %d needle(s), max %d per frame, %d/%d lock-bound' % (total, per, bound, total))
            until(lambda s: s.get('vuln'), 120, 1)
            g3 = pg.evaluate(GATE_HIT)
            ok(g3 == 'falsecrash@25', 'the 25%% gate starts the FALSE CRASH (%s)' % g3)
            step(20, 20); shot('06_falsecrash.png', 'false crash: burning, falling out')
            until(lambda s: s.get('phase') == 'frenzy', 300)
            until(lambda s: s.get('vuln') and (s.get('t') or 0) > 1.2, 300, 2)
            shot('07_frenzy.png', 'frenzy: damaged plate')
            keys = pg.evaluate("() => window.__tl.keys")
            ok(keys.get('tlv_hull_damaged') and keys.get('tlv_needle') and any(k.startswith('nxp_barrage_') for k in keys),
               'the damaged plate, the needle and the barrage reel were all asked for')
        guard('hell', hell)

        # ---------------- the kill ----------------
        def kill():
            until(lambda s: s.get('vuln'), 120, 1)
            pg.evaluate("() => { const b=subBoss, m=b.maxhp; hitSubBoss(m*5,b.x,b.y); }")
            s = st()
            ok(s.get('dead') is True, 'the last share kills it through hitSubBoss (%s)' % s.get('hist'))
            step(12, 30); shot('08_death.png', 'death: the ordinary sub-boss death FX')
            for _ in range(40):
                s = st()
                if s.get('none'): break
                step(6, 12)
            ok(s.get('none') and s.get('subBossDone') is True, 'the ordinary death branch ran its 1.9s clock and freed the slot')
        guard('kill', kill)

        # ---------------- the whole-run rules ----------------
        def rules():
            W = pg.evaluate("() => { const W=window.__tl; return {steps:W.steps, diag:W.diag, xs:W.xs, ys:W.ys, band:W.bandMin, vf:W.vulnFrames, blits:W.hullBlits, rot:W.rot, snd:W.snd, hits:W.hits, pm:W.playerMoves}; }")
            print('run', W, flush=True)
            ok(W['steps'] > 600 and W['diag'] == 0 and W['xs'] > 50 and W['ys'] > 50,
               'EVERY STEP MOVED ON ONE AXIS - %d diagonal of %d steps (%d on x, %d on y)' % (W['diag'], W['steps'], W['xs'], W['ys']))
            ok(W['blits'] > 100 and W['rot'] == 0, 'FIXED NOSE-UP - %d hull-sized blits, %d with any rotation in the transform' % (W['blits'], W['rot']))
            ok(W['vf'] > 100 and W['band'] >= 77, 'while targetable the hull top never entered the 77px gauge band (highest %s over %d frames)' % (n(W['band']), W['vf']))
            ok(W['pm'] == 0, 'the rig never moved the player (%d updates changed player.x/y)' % W['pm'])
            need = ['enemyMachineShotHeavy', 'enemyPulseLaserBlue', 'maverickHelixRelease', 'explosionAirSmall01', 'explosionJetBreakup', 'explosionBossCore', 'retinaCharge']
            ok(all((W['snd'] or {}).get(k, 0) > 0 for k in need), 'every sound key fired: %s' % {k: (W['snd'] or {}).get(k, 0) for k in need})
            tame = pg.evaluate("""async () => { const r = await fetch('assets/game/sounds/enemy_machine_shot_heavy.wav');
              return {status: r.status, tame: (typeof Snd!=='undefined' && Snd.TAME && Snd.TAME.enemyMachineShotHeavy) ? Snd.TAME.enemyMachineShotHeavy : null,
                      path: BOFA.sfx.enemyMachineShotHeavy}; }""")
            ok(tame['status'] == 200 and tame['tame'] and tame['tame'].get('min', 0) > 0,
               'enemyMachineShotHeavy -> %s serves %s and carries a TAME row %s' % (tame['path'], tame['status'], tame['tame']))
        guard('rules', rules)
        br.close()
    stop()

    ok(not errs, 'zero page and console errors' + ('' if not errs else ' - %d: %s' % (len(errs), errs[:3])))

    if caps:
        cw, ch, cols = 360, 384, 4
        rows = (len(caps) + cols - 1) // cols
        sheet = Image.new('RGB', (cw * cols, (ch + 22) * rows), (12, 12, 16))
        d = ImageDraw.Draw(sheet)
        for i, (label, im) in enumerate(caps):
            x, y = (i % cols) * cw, (i // cols) * (ch + 22)
            sheet.paste(im.resize((cw, ch), Image.LANCZOS), (x, y + 22))
            d.text((x + 6, y + 5), label, fill=(235, 235, 235))
        sheet.save(os.path.join(out, '_contact.png'))
        print('wrote', os.path.join(out, '_contact.png'), flush=True)

    print('\n%d ok / %d fail' % (n_ok[0], len(fails)))
    for f in fails: print('  FAIL', f)
    return 1 if fails else 0


if __name__ == '__main__':
    sys.exit(main())
