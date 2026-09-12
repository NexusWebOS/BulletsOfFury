#!/usr/bin/env python3
"""
probe_frostcruiser_0912s.py - STAGE 3's FROST CRUISER, AND ALTBOSS3 STILL ALIVE, IN REAL CHROMIUM.

    python3 _BUILD_SOURCE/probe_frostcruiser_0912s.py --out /tmp/frost

Mike, 0912: "Take THAT stage 1 miniboss, palette swap to an icey combination, and use as the new
stage 3 mini boss. store that stage 3 miniboss were replacing for later as ALTBOSS3."

  * stage 3's miniboss spawns as the FROST CRUISER and draws nsb_frost_cruiser - identified by
    recording the KEY XART.get is asked for, never by size (both plates are 256x256)
  * it runs the Jungle Cruiser's own authored director, not the generic ship queue, and fires
  * the drawn hull is ICE: its opaque pixels on the live canvas skew blue, where the olive plate
    skews yellow-green
  * ALTBOSS[3] is the Rime Thorn, and it still spawns
"""
import os, sys, argparse, base64
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import shoot

SETUP = r"""
async () => {
  const B=window.BOSSMODE, fr=()=>new Promise(r=>requestAnimationFrame(()=>r()));
  let role=null;
  for(const r of ['mini','sub','subboss','miniboss']){ try{ if(B.start(3,r,'cole',false)){ role=r; break; } }catch(e){} }
  const t0=performance.now();
  while(performance.now()-t0<30000 && !(typeof subBoss!=='undefined' && subBoss && subBoss._ship && B.player && !B.player.dead)) await fr();
  B.setInvuln(true);
  const t1=performance.now();
  while(performance.now()-t1<12000 && !XART.rdy('nsb_frost_cruiser')) await fr();
  window.__fk=[];
  const og=XART.get.bind(XART);
  XART.get=function(k){ if(typeof k==='string' && k.indexOf('nsb_')===0) window.__fk.push(k); return og(k); };
  return {role:role, kind:(SUBBOSS[3]||{}).kind, ship:subBoss?subBoss._ship:null, name:subBoss?subBoss.name:null,
          jc:!!(subBoss&&subBoss._jc), ready:XART.rdy('nsb_frost_cruiser')};
}
"""

FIGHT = r"""
async () => {
  const fr=()=>new Promise(r=>requestAnimationFrame(()=>r()));
  const b=subBoss; let maxB=0, states={};
  const t0=performance.now();
  while(performance.now()-t0<9000 && subBoss===b && !b.dead){ await fr();
    maxB=Math.max(maxB, eBullets.length); if(b._jc) states[b._jc.state]=1; }
  const keys=[...new Set(window.__fk)];
  return {maxBullets:maxB, states:Object.keys(states), keys:keys, x:b.x, y:b.y, w:b.w};
}
"""

# sample the hull's pixels off the live canvas, in the unit's screen rect
COLOUR = r"""
() => {
  const b=subBoss, c=document.querySelector('#screen'); if(!b||!c) return null;
  const g=c.getContext('2d'), T=g.getTransform ? null : null;
  const s=BOSSMODE.snapshot(), cam=(s.camX||0), k=c.width/(s.VW||480);
  const vz=(typeof viewZoom==='function')?viewZoom():1;
  const X=x=>(x-cam)*vz*k, Y=y=>(y*vz+VH*(1-vz))*k;
  const x0=Math.max(0,Math.floor(X(b.x-b.w*0.30))), x1=Math.min(c.width,Math.ceil(X(b.x+b.w*0.30)));
  const y0=Math.max(0,Math.floor(Y(b.y-b.h*0.30))), y1=Math.min(c.height,Math.ceil(Y(b.y+b.h*0.30)));
  const d=g.getImageData(x0,y0,Math.max(1,x1-x0),Math.max(1,y1-y0)).data;
  let n=0, blue=0, yel=0;
  for(let i=0;i<d.length;i+=4){ const r=d[i],gg=d[i+1],bb=d[i+2]; n++;
    if(bb>r+18 && bb>=gg-6) blue++; if(gg>bb+18 && r>bb+10) yel++; }
  return {n:n, blueShare:+(blue/Math.max(1,n)).toFixed(3), olivShare:+(yel/Math.max(1,n)).toFixed(3)};
}
"""

ALT = r"""
async () => {
  const fr=()=>new Promise(r=>requestAnimationFrame(()=>r()));
  const alt=(typeof ALTBOSS!=='undefined' && ALTBOSS[3]) ? ALTBOSS[3].kind : null;
  subBoss=null; subBossActive=false; subBossDone=false;
  spawnSubBoss(alt);
  for(let i=0;i<5;i++) await fr();
  return {alt:alt, spawned:!!(subBoss && subBoss.kind===alt), name:subBoss?subBoss.name:null};
}
"""

SNAP = r"""() => { const c=document.querySelector('#screen'); return c ? c.toDataURL('image/png') : null; }"""


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--out', default='/tmp/frost'); a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    from playwright.sync_api import sync_playwright
    port, stop = shoot.serve(shoot.GAME); errs = []; fails = []; n_ok = [0]
    def ok(c, m):
        if c: n_ok[0] += 1; print('  ok  ', m)
        else: fails.append(m); print('  FAIL', m)
    with sync_playwright() as p:
        b = p.chromium.launch(args=['--disable-gpu', '--no-sandbox', '--mute-audio'])
        pg = b.new_page(viewport={'width': 1100, 'height': 1000})
        pg.on('pageerror', lambda e: errs.append('pageerror: ' + str(e)[:220]))
        pg.on('console', lambda m: errs.append('console.error: ' + m.text[:200]) if m.type == 'error' else None)
        pg.goto(f'http://127.0.0.1:{port}/index.html?bossmode=1', wait_until='load', timeout=60000)
        pg.wait_for_function("() => window.BOSSMODE && window.BOSSMODE.ready", timeout=90000)
        st = pg.evaluate(SETUP)
        print('setup', st)
        ok(st['kind'] == 'frostcruiser' and st['ship'] == 'frostcruiser',
           "stage 3's miniboss spawns as the FROST CRUISER (%s / %s)" % (st['kind'], st['ship']))
        ok(st['jc'], "and it runs the Jungle Cruiser's own authored director (_jc present)")
        f = pg.evaluate(FIGHT)
        print('fight', f)
        ok('nsb_frost_cruiser' in f['keys'] and 'nsb_jungle_cruiser' not in f['keys'],
           'it draws the ICE plate and never the jungle one: %s' % f['keys'])
        ok(f['maxBullets'] > 0 and len(f['states']) >= 2,
           'and it fights - %d rounds on screen at peak, director states %s' % (f['maxBullets'], f['states']))
        c = pg.evaluate(COLOUR)
        print('colour', c)
        d = pg.evaluate(SNAP)
        if d: open(os.path.join(a.out, '01_frost_cruiser.png'), 'wb').write(base64.b64decode(d.split(',', 1)[1]))
        ok(c and c['blueShare'] > c['olivShare'],
           'the hull on the live canvas is ICE - blue-dominant pixels %.3f against olive %.3f' % (c['blueShare'], c['olivShare']))
        al = pg.evaluate(ALT)
        print('alt', al)
        ok(al['alt'] == 'rimewall' and al['spawned'], 'ALTBOSS[3] is the Rime Thorn and it still spawns (%s)' % al['name'])
        b.close()
    stop()
    print('\n%d ok / %d fail' % (n_ok[0], len(fails)))
    for x in fails: print('  FAIL', x)
    if errs:
        print('page errors (%d):' % len(errs))
        for e in errs[:8]: print('   ', e)
    sys.exit(1 if fails or errs else 0)


if __name__ == '__main__':
    main()
