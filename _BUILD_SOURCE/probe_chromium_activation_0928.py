#!/usr/bin/env python3
"""probe_chromium_activation_0928.py - the Stage 5 Furious CHROMIUM ARMOR activation, frame by frame in real
Chromium (Mike 0928: "the chromium armor activate sequence was horrible and needs to be re-done").
Spawns the Chrome Hammer on Furious, waits for its arrival, and captures the activation every 0.2 s,
recording state, time, the gauge fraction, whether the boss is hittable, what art keys the draw asked
for, and errors. Also checks the hand-off: the fight resumes, armor is full, and the boss takes damage.
  python3 _BUILD_SOURCE/probe_chromium_activation_0928.py [--tag name]
"""
import os, sys, json, base64, argparse, http.server
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
http.server.SimpleHTTPRequestHandler.log_message = lambda *a: None
import shoot as sh
from playwright.sync_api import sync_playwright

SETUP = r"""
() => {
  diffKey='furious';DIFF=DIFFS.furious;run.mode='arcade';run.pilot='maverick';run.stage=5;curStage=STAGES[4];
  beginStage(5);setState(GS.PLAY);player.reset();story=null;special=null;
  stagePlan=[];waveIdx=999;spawnClock=9999;enemies=[];eBullets=[];pBullets=[];powerups=[];
  boss=null;bossActive=false;subBoss=null;subBossActive=false;subBossDone=true;
  window.__hits=0;window.playerHit=function(){window.__hits++;};
  spawnBoss(curStage.boss);bossActive=true;const b=boss;b.enter=false;b._noHit=false;
  if(b._hammerTime){b._hammerTime.mode='attack';b._hammerTime.shield=false;}
  b._hammer.balance0922=true;window.__B=b;
  window.__asked={};if(!window.__xg){window.__xg=XART.get.bind(XART);XART.get=function(k){window.__asked[k]=(window.__asked[k]||0)+1;return window.__xg(k);};}
  return {state:b._hammer.state};
}
"""
READ = r"""() => { const b=window.__B,h=b._hammer,A=h.frArmor; const asked=Object.keys(window.__asked);window.__asked={};
  return {state:h.state,t:+(h.t||0).toFixed(2),noHit:!!b._noHit,gauge:+bossHealthFraction(b).toFixed(3),armor:A?Math.round(A.hp):null,
    armorMax:A?Math.round(A.max):null,activated:!!(A&&A.activated),hp:Math.round(b.hp),x:Math.round(b.x),y:Math.round(b.y),
    asked:asked.filter(k=>/fr27|chrom|arch|bmbar|ht27|hammer/i.test(k)).slice(0,12),shake:+(typeof shake!=='undefined'?shake:0).toFixed(2)}; }"""

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--tag', default='before'); a = ap.parse_args()
    out = os.path.join(sh.GAME, '_shots', 'opus0928', 'chromium_activation', a.tag); os.makedirs(out, exist_ok=True)
    port, stop = sh.serve(sh.GAME); errs = []
    with sync_playwright() as pw:
        br = pw.chromium.launch(args=['--no-sandbox', '--mute-audio'])
        pg = br.new_page(viewport={'width': 1000, 'height': 1100})
        pg.on('pageerror', lambda e: errs.append(str(e)[:200]))
        pg.on('console', lambda m: errs.append('console:' + m.text[:200]) if m.type == 'error' or 'draw error' in m.text else None)
        pg.goto('http://127.0.0.1:%d/index.html' % port, wait_until='load', timeout=120000)
        pg.wait_for_function("() => (window.__bofFrames|0)>4", timeout=120000)
        pg.evaluate(sh.TRAP_RAF); pg.evaluate(SETUP)
        pg.evaluate("() => { XART.rdy('fr27_chromium_actions'); }"); pg.wait_for_timeout(1500)
        for _ in range(60):
            pg.evaluate(sh.STEP, 6); pg.wait_for_timeout(20)
            if pg.evaluate("() => window.__B._hammer.state==='fr_activation'"): break
        rows = []; t = 0.0
        while t < 8.0:
            s = pg.evaluate(READ); s['wall'] = round(t, 1); rows.append(s)
            d = pg.evaluate("() => document.getElementById('screen').toDataURL('image/png')")
            open(os.path.join(out, 'a_%04.1f.png' % t), 'wb').write(base64.b64decode(d.split(',', 1)[1]))
            pg.evaluate(sh.STEP, 12); pg.wait_for_timeout(30); t += 0.2
        # hand-off: a round into the body after activation must land on the armor
        post = pg.evaluate("() => { const b=window.__B,A=b._hammer.frArmor,a0=A?A.hp:0,h0=b.hp; _lastHitX=b.x;_lastHitY=b.y; hitBoss(40); return {armorDelta:Math.round(a0-(A?A.hp:0)),hpDelta:Math.round(h0-b.hp),state:b._hammer.state}; }")
        br.close()
    stop()
    json.dump({'rows': rows, 'post': post, 'errs': errs}, open(os.path.join(out, 'run.json'), 'w'), indent=1)
    for r in rows: print(r['wall'], r['state'], r['t'], 'noHit' if r['noHit'] else 'hit', 'gauge', r['gauge'], 'armor', r['armor'], r['activated'], r['asked'])
    print('post', post, 'errs', len(errs), errs[:3])

if __name__ == '__main__':
    main()
