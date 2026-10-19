#!/usr/bin/env python3
"""probe_player_shield_checks_1018.py - the player shield, measured through the REAL drawPlayer in real Chromium.

Mike, 1018: "why are the shields so big. I mainly wanted just a specific outline of each pilot's ship that pixel
glows and lets you know they are protected internally with a shield that glows over them too."

For every pilot the real drawPlayer draws the ship at (120,120) on a cleared black square, at four game-clock times,
once with run.shield=0 and once with run.shield=3. What the shield ADDS is the per-pixel difference, so the hull,
its flame flicker and the background cannot pollute the measurement:
  TIGHT     every added pixel lies within 3 px of the hull's drawn rect (the old shell reached ~20 px out)
  OUTLINE   most added pixels lie OUTSIDE the hull's ink (the 1-2 px rings) ...
  INTERNAL  ... and a real number lie INSIDE it (the sheen over the ship)
  ANIMATED  the shield's own pixels change between game-clock times
  FOLLOWS   a barrel roll frame still gets its shield; a blinked-off hull gets none
  BUSTED    the pre-1018 drawShield (PS18.base, orbiting orbs) fails TIGHT, so the check can fail
Sheet: _shots/shield_1018/outline_sheet.png (each pilot at 4x, shield off | on t0 | on t1).
"""
import os, sys, json, base64, io
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import shoot as sh
from PIL import Image
PILOTS = ['cole', 'maverick', 'lizzie', 'juggernaut', 'yuri', 'freezer', 'falva', 'decker', 'axel']
OUT = os.path.join(os.path.dirname(HERE), '_shots', 'shield_1018')

MEASURE = r"""async (cfg) => {
  const pk = cfg.pilot, out = {pk};
  run.pilot = pk; const pi = PILOTS.findIndex(p => p.key === pk); if (pi >= 0) pilotIndex = pi;
  run.spaceMode = false; try { gravityMode = null; } catch (e) {}
  player.dead = false; player.invuln = 0; player.roll = null; player.somer = null; player._bank = 0; player._spawnClearT = 0;
  for (const k of ['ship_' + pk, 'ship_' + pk + '_br2', 'ship_' + pk + '_g1', 'ship_' + pk + '_g2']) XART.rdy(k);
  for (let i = 0; i < 80 && !XART.rdy('ship_' + pk); i++) await new Promise(r => setTimeout(r, 50));
  // busted arm: the previous 1018 shield - the baked crystal-shell reel fitted round the hull - drawn in its place
  const R = typeof SHIELD_PX_1018 !== 'undefined' && SHIELD_PX_1018[pk];
  if (cfg.busted && R) { XART.rdy(R.key); for (let i = 0; i < 80 && !XART.rdy(R.key); i++) await new Promise(r => setTimeout(r, 50)); }
  const sDS = drawShield; if (cfg.busted) drawShield = function (x, y) { const H = ps18HullInk(pk); if (!R || !H || !XART.rdy(R.key)) return;
    ctx.drawImage(XART.get(R.key), 0, 0, R.w, R.h, Math.round(x + H.cx - R.hole[0]), Math.round(y + H.cy - R.hole[1]), R.w, R.h); };
  const shot = (shield, t, prep) => {
    run.shield = shield; efxClock = t; player.x = 120; player.y = 120; player._lx = 120; if (prep) prep();
    ctx.save(); ctx.setTransform(1,0,0,1,0,0); ctx.globalAlpha = 1; ctx.globalCompositeOperation = 'source-over'; ctx.fillStyle = '#000'; ctx.fillRect(0, 0, 240, 240);
    try { drawPlayer(); } catch (e) { out.err = String(e).slice(0, 160); }
    ctx.restore(); player.roll = null; return ctx.getImageData(0, 0, 240, 240).data.slice(); };
  const diff = (a, b) => { const m = new Uint8Array(240 * 240); let n = 0; for (let i = 0, p = 0; i < a.length; i += 4, p++)
    if (Math.abs(a[i]-b[i]) > 30 || Math.abs(a[i+1]-b[i+1]) > 30 || Math.abs(a[i+2]-b[i+2]) > 30) { m[p] = 1; n++; } return {m, n}; };
  const times = [0, .37, .53, .86], off = [], on = [];
  for (const t of times) { off.push(shot(0, t)); on.push(shot(3, t)); }
  const F = PS18.lastFit; out.fit = F && {pk: F.pk, hull: F.hull.map(v => +v.toFixed(1))};
  // the hull's own ink, from the shield-off frame
  const ink = new Uint8Array(240 * 240); for (let i = 0, p = 0; i < off[0].length; i += 4, p++) if (off[0][i] + off[0][i+1] + off[0][i+2] > 24) ink[p] = 1;
  const D = diff(off[0], on[0]);
  let x0 = 1e9, y0 = 1e9, x1 = -1, y1 = -1, outside = 0, inside = 0;
  for (let p = 0; p < D.m.length; p++) if (D.m[p]) { const x = p % 240, y = (p / 240) | 0; x0 = Math.min(x0, x); x1 = Math.max(x1, x); y0 = Math.min(y0, y); y1 = Math.max(y1, y); if (ink[p]) inside++; else outside++; }
  out.added = D.n; out.inside = inside; out.outside = outside; out.addBox = [x0, y0, x1, y1];
  const hb = F && F.hull; out.reach = hb ? +Math.max(hb[0] - x0, y0 >= 0 ? hb[1] - y0 : 0, x1 - hb[2], y1 - hb[3]).toFixed(1) : null;
  // animation: the shield's own pixels at t0 vs t2 (shield-on minus shield-off at each time, then compared)
  const A0 = diff(off[0], on[0]).m, A2 = diff(off[2], on[2]).m; let anim = 0; for (let p = 0; p < A0.length; p++) if (A0[p] !== A2[p]) anim++;
  const C0 = on[0], C2 = on[2]; let animC = 0; for (let p = 0; p < A0.length; p++) if (A0[p] || A2[p]) { const i = p * 4; if (Math.abs(C0[i]-C2[i]) + Math.abs(C0[i+1]-C2[i+1]) + Math.abs(C0[i+2]-C2[i+2]) > 40) animC++; }
  out.animPx = anim + animC;
  // a barrel-roll frame still carries its shield
  const d0 = PS18.draws; const rollPrep = () => { player.roll = {t: .3, dur: 1, dir: 1}; };
  if (!cfg.busted) { shot(3, .2, rollPrep); out.rollDrawn = PS18.draws > d0;
    // a blinked-off hull draws no shield
    const d1 = PS18.draws; shot(3, .2, () => { player.invuln = 4; }); player.invuln = 0; out.blinkDrawn = PS18.draws > d1; }
  drawShield = sDS;
  if (cfg.sheet) { const cv = document.createElement('canvas'); cv.width = 240 * 3; cv.height = 240; const g = cv.getContext('2d');
    [off[0], on[0], on[2]].forEach((d, i) => { const id = new ImageData(new Uint8ClampedArray(d), 240, 240); g.putImageData(id, i * 240, 0); });
    out.img = cv.toDataURL('image/png'); }
  return out; }"""

LEVELS = r"""async (cfg) => {
  const pk = cfg.pilot, out = {pk, reach: [], added: [], imgs: []};
  run.pilot = pk; const pi = PILOTS.findIndex(p => p.key === pk); if (pi >= 0) pilotIndex = pi;
  run.spaceMode = false; try { gravityMode = null; } catch (e) {}
  player.dead = false; player.invuln = 0; player.roll = null; player.somer = null; player._bank = 0; player._spawnClearT = 0;
  XART.rdy('ship_' + pk); for (let i = 0; i < 80 && !XART.rdy('ship_' + pk); i++) await new Promise(r => setTimeout(r, 50));
  const shot = (shield, t, prev) => {
    PS18.lastLv[1] = prev == null ? shield : prev; PS18.shards = []; if (prev == null) PS18.fx = {};
    run.shield = shield; efxClock = t; player.x = 120; player.y = 120; player._lx = 120;
    ctx.save(); ctx.setTransform(1,0,0,1,0,0); ctx.globalAlpha = 1; ctx.globalCompositeOperation = 'source-over'; ctx.fillStyle = '#000'; ctx.fillRect(0, 0, 240, 240);
    try { drawPlayer(); } catch (e) { out.err = String(e).slice(0, 160); }
    ctx.restore(); return ctx.getImageData(0, 0, 240, 240).data.slice(); };
  const reachOf = (off, on) => { const hb = PS18.lastFit.hull; let x0 = 1e9, y0 = 1e9, x1 = -1, y1 = -1, n = 0;
    for (let i = 0, p = 0; i < off.length; i += 4, p++) if (Math.abs(off[i]-on[i]) > 30 || Math.abs(off[i+1]-on[i+1]) > 30 || Math.abs(off[i+2]-on[i+2]) > 30) {
      const x = p % 240, y = (p / 240) | 0; n++; x0 = Math.min(x0, x); x1 = Math.max(x1, x); y0 = Math.min(y0, y); y1 = Math.max(y1, y); }
    return {n, reach: Math.max(hb[0] - x0, hb[1] - y0, x1 - hb[2], y1 - hb[3])}; };
  const t = 0.2, off = shot(0, t);   // not on a level-1 stutter frame (floor(t*7)%5===0)
  for (let lv = 1; lv <= 5; lv++) { const on = shot(lv, t); const r = reachOf(off, on); out.reach.push(+r.reach.toFixed(1)); out.added.push(r.n); out.imgs.push(on); }
  // level up 2 -> 3: the change frame flares further out than a steady level 3
  const up = shot(3, t, 2); out.flareReach = +reachOf(off, up).reach.toFixed(1); out.flareFx = PS18.fx[1] && PS18.fx[1].kind;
  efxClock = t + .6; const after = shot(3, t + .6); PS18.lastLv[1] = 3;
  // level down 4 -> 2: shards are thrown
  shot(2, t, 4); out.shards = PS18.shards.length; out.downFx = PS18.fx[1] && PS18.fx[1].kind;
  PS18.shards = []; PS18.fx = {};
  if (cfg.sheet) { const cv = document.createElement('canvas'); cv.width = 120 * 6; cv.height = 120; const g = cv.getContext('2d');
    [off, ...out.imgs].forEach((d, i) => { const c2 = document.createElement('canvas'); c2.width = 240; c2.height = 240;
      c2.getContext('2d').putImageData(new ImageData(new Uint8ClampedArray(d), 240, 240), 0, 0); g.drawImage(c2, 60, 60, 120, 120, i * 120, 0, 120, 120); });
    out.img = cv.toDataURL('image/png'); }
  delete out.imgs; return out; }"""

def main():
    from playwright.sync_api import sync_playwright
    os.makedirs(OUT, exist_ok=True)
    port, stop = sh.serve(sh.GAME)
    ok = fail = 0; rep = {}; tiles = []
    def check(name, cond, info=''):
        nonlocal ok, fail
        ok += 1 if cond else 0; fail += 0 if cond else 1
        print(('ok   ' if cond else 'FAIL ') + name + ('  ' + str(info)[:260] if info != '' else ''), flush=True)
    with sync_playwright() as p:
        errs = []
        b = p.chromium.launch(args=['--disable-gpu', '--no-sandbox', '--mute-audio'])
        pg = b.new_page(viewport={'width': 1000, 'height': 1100})
        pg.on('pageerror', lambda e: errs.append(str(e)[:200]))
        pg.on('console', lambda m: errs.append(m.text[:200]) if m.type == 'error' else None)
        pg.goto('http://127.0.0.1:%d/index.html' % port, wait_until='load', timeout=120000)
        pg.wait_for_function("() => typeof setState==='function' && (window.__bofFrames|0) > 4", timeout=120000)
        pg.evaluate(sh.TRAP_RAF); pg.wait_for_timeout(60)
        pg.evaluate("() => { ASSETS.ready = true; startRun(4); curStage = STAGES[3]; beginStage(4); setState(GS.PLAY); player.reset(); }")
        for pk in PILOTS:
            r = pg.evaluate(MEASURE, {'pilot': pk, 'sheet': True}); img = r.pop('img', None); rep[pk] = r
            if img: tiles.append(Image.open(io.BytesIO(base64.b64decode(img.split(',', 1)[1]))).crop((40, 40, 680, 200)))
            check('%s: the shield is drawn and traced on this hull (%d px added)' % (pk, r['added']), r['added'] > 80 and r.get('fit') and r['fit']['pk'] == pk, r.get('fit'))
            check('%s: TIGHT - nothing reaches more than 3 px past the hull (reach %s px)' % (pk, r['reach']), r['reach'] is not None and r['reach'] <= 3.0, r['addBox'])
            check('%s: OUTLINE - the rings outside the ink (%d px) and INTERNAL glow over it (%d px)' % (pk, r['outside'], r['inside']), r['outside'] > 60 and r['inside'] > 40)
            check('%s: ANIMATED - %d px of the shield change between game-clock times' % (pk, r['animPx']), r['animPx'] > 40)
            check('%s: follows a barrel-roll frame, and blinks off with the hull' % pk, r.get('rollDrawn') and not r.get('blinkDrawn'), (r.get('rollDrawn'), r.get('blinkDrawn')))
            check('%s: no draw error' % pk, not r.get('err'), r.get('err'))
        ltiles = []
        for pk in PILOTS:
            r = pg.evaluate(LEVELS, {'pilot': pk, 'sheet': True}); img = r.pop('img', None); rep['levels_' + pk] = r
            if img: ltiles.append(Image.open(io.BytesIO(base64.b64decode(img.split(',', 1)[1]))))
            R = r['reach']
            check('%s: LEVELS - one ring per level, reach grows 1..5 (%s px) and never past the level' % (pk, R),
                  all(R[i] < R[i + 1] for i in range(4)) and all(R[i] <= i + 1 for i in range(5)) and not r.get('err'), r['added'])
            check('%s: LEVEL UP flares past a steady level 3 (%s > %s px); LEVEL DOWN throws %d shards' % (pk, r['flareReach'], R[2], r['shards']),
                  r['flareFx'] == 'up' and r['flareReach'] > R[2] and r['downFx'] == 'down' and r['shards'] >= 12)
        if ltiles:
            w, h = ltiles[0].size; S = Image.new('RGBA', (w, h * len(ltiles)), (0, 0, 0, 255))
            for i, t in enumerate(ltiles): S.paste(t, (0, i * h))
            S.resize((w * 2, h * len(ltiles) * 2), Image.NEAREST).save(os.path.join(OUT, 'levels_sheet.png'))
        r = pg.evaluate(MEASURE, {'pilot': 'cole', 'busted': True}); rep['busted'] = r
        check('busted arm: the pre-1018 shield is NOT tight (reach %s px) - the TIGHT check can fail' % r['reach'], r['reach'] is None or r['reach'] > 3.0, r['addBox'])
        check('0 page/console errors', not errs, errs[:3])
        b.close()
    stop()
    if tiles:
        w, h = tiles[0].size; S = Image.new('RGBA', (w, h * len(tiles)), (0, 0, 0, 255))
        for i, t in enumerate(tiles): S.paste(t, (0, i * h))
        S = S.resize((w * 2, h * len(tiles) * 2), Image.NEAREST); S.save(os.path.join(OUT, 'outline_sheet.png'))
    json.dump(rep, open(os.path.join(OUT, 'checks.json'), 'w'), indent=1)
    print('%d ok / %d fail' % (ok, fail)); sys.exit(1 if fail else 0)

if __name__ == '__main__':
    main()
