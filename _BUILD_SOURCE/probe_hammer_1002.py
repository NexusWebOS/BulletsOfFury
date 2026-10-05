"""probe_hammer_1002 - the Stage 5 Chrome Hammer Archmage, three of Mike's 1002 notes, in real Chromium.

    python3 _BUILD_SOURCE/probe_hammer_1002.py [--diff normal] [--old]

1. FLASH: through a long fight driven by real hitBoss calls, every sampled frame where a hit landed is
   drawn twice over the same canvas - boss.flash 0, then boss.flash 0.16 - and the pixels that turn
   near-white in the second draw are counted. A hit that shows nothing is listed by state.
2. VOLLEY: while the heal charges, the passive volley rack is launched repeatedly; the recovery must
   still be charging and no volley may lock or strike the hammer.
3. FLOOR: lethal damage is poured on until the fr_twirl has played; he must never die first.
--old loads the tree without feedback_1002.js (the busted arm).
"""
import argparse, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import shoot

SETUP = r"""
(cfg)=>{
  ASSETS.ready=true; window.__bofStepNow=performance.now(); diffKey=cfg.diff; if(typeof DIFFS!=='undefined'&&DIFFS[cfg.diff])DIFF=DIFFS[cfg.diff];
  run.pilot='cole'; run.stage=5; run.mode='arcade'; curStage=STAGES[4];
  beginStage(5); setState(GS.PLAY); player.reset(); playerHit=function(){};
  spawnBoss('chromehammer'); bossActive=true; boss._be=null; boss._symEntry=null; boss.enter=false;
  window.__log={states:[],flash:[],deaths:[],twirl:false,volley:null};
  {const bd=bossDie;bossDie=function(){const b=boss;window.__log.deaths.push({A:!!fr27Armor(b),cp:fr27Armor(b)&&fr27Armor(b).checkpoints,done:b._hammer._fb2RageDone,floor:fb2HammerFloor(b),hp:b&&b.hp,state:b&&b._hammer&&b._hammer.state,stack:String(new Error().stack).split('\n').slice(1,7).join(' | ')});return bd.apply(this,arguments);};}
  return {kind:boss&&boss.kind,name:boss&&boss.name,hp:boss&&boss.hp};
}
"""

# One chunk: n frames of real loop, hitting the body every `every` frames with `dmg`.
CHUNK = r"""
(a)=>{
  const L=window.__log, c=document.querySelector('#screen').getContext('2d');
  for(let i=0;i<a.n;i++){
    window.__bofStepNow+=1000/60; loop(window.__bofStepNow);
    if(!boss||boss.dead){ if(boss&&boss.dead&&!L.dead){L.dead={state:boss._hammer&&boss._hammer.state,twirl:L.twirl,restored:!!boss._hammer.restorationSeen,preset:L.preset}; } return {done:true}; }
    const h=boss._hammer; if(!h) return {done:true,err:'no hammer'};
    if(L.states[L.states.length-1]!==h.state) L.states.push(h.state);
    L.restored=!!h.restorationSeen; L.preset=!!(fr27Armor(boss)&&fr27Armor(boss)._fb2TwirlPreset);
    if(h.state==='fr_twirl') L.twirl=true;
    if(a.hit && (i%a.every)===0 && !boss._noHit){
      const head=hammerHeadPoint(boss), onHammer=(i/a.every)%3===1;
      const x=onHammer?head.x:boss.x, y=onHammer?head.y:boss.y+10;
      _dmgBullet={kind:'mg',x,y}; _lastHitX=x; _lastHitY=y;
      boss.flash=0;
      if(bossHitTest(x,y)){ const hp0=boss.hp; hitBoss(a.dmg);
        if(a.measure && boss.flash>0 && !boss.dead){
          // draw twice over the same canvas: flash 0, then 0.16; count pixels newly near-white
          const f=boss.flash; c.save(); c.setTransform(2,0,0,2,-camX*2,0);
          const W=c.canvas.width,H=c.canvas.height;
          boss.flash=0; drawBoss(); const A=c.getImageData(0,0,W,H).data;
          boss.flash=.16; drawBoss(); const B=c.getImageData(0,0,W,H).data; c.restore(); boss.flash=f;
          let n=0; for(let k=0;k<A.length;k+=16){ const wb=B[k]>225&&B[k+1]>225&&B[k+2]>225, wa=A[k]>225&&A[k+1]>225&&A[k+2]>225; if(wb&&!wa)n++; }
          L.flash.push({state:h.state,white:n,onHammer,armor:typeof fr27Armor==='function'&&fr27Armor(boss)?Math.round(fr27Armor(boss).hp):null});
        } else if(a.measure){ L.flash.push({state:h.state,white:-1,onHammer,flash:boss.flash}); }
      }
      _dmgBullet=null;
    }
  }
  const h=boss&&boss._hammer;
  const A=typeof fr27Armor==='function'&&fr27Armor(boss);
  return {done:false,state:h&&h.state,mode:h&&h.mode,hp:boss&&Math.round(boss.hp),max:boss&&Math.round(boss.maxhp),A:A&&{hp:Math.round(A.hp),cp:A.checkpoints,half:A.half,rage:A.rage,barrier:A.barrier},noHit:boss._noHit,ht:!!boss._hammerTime};
}
"""

VOLLEY = r"""
()=>{
  // put him straight into a checkpoint heal and fire the volley rack into it
  const b=boss,h=b._hammer,A=fr27Armor(b); if(!A) return {err:'no armor'};
  A.hp=0; fr27Restore(b,.10,false,true);
  const out={hits:0,locks:0,broke:false,launched:0};
  for(let i=0;i<150;i++){
    if(i%20===0){ spaceVolleyLaunchRack(3); out.launched++; }
    for(const q of pBullets) if(q.kind==='spaceVolley'&&q._target&&q._target._retinaId==='hammer') out.locks++;
    window.__bofStepNow+=1000/60; loop(window.__bofStepNow);
    if(h.recovery&&h.recovery.status==='cancelled') { out.broke=true; break; }
  }
  out.state=h.state; out.recovery=h.recovery&&h.recovery.status; return out;
}
"""


def run(diff, old, novolley=False):
    from playwright.sync_api import sync_playwright
    port, stop = shoot.serve(shoot.GAME)
    res = {}
    with sync_playwright() as p:
        chrome = os.environ.get('BOF_CHROME', '/opt/pw-browsers/chromium-1194/chrome-linux/chrome')
        b = p.chromium.launch(args=['--disable-gpu', '--no-sandbox', '--mute-audio'], **({'executable_path': chrome} if os.path.exists(chrome) else {}))
        pg = b.new_page(viewport={'width': 1100, 'height': 1200})
        errs = []
        pg.on('pageerror', lambda e: errs.append(str(e)[:300]))
        if old:
            pg.route('**/assets/feedback_1002.js', lambda r: r.fulfill(status=200, content_type='application/javascript', body='/* busted arm */'))
        pg.goto(f'http://127.0.0.1:{port}/index.html', wait_until='load', timeout=60000)
        pg.wait_for_function("() => (window.__bofFrames|0) > 4", timeout=45000)
        pg.evaluate(shoot.TRAP_RAF)
        res['setup'] = pg.evaluate(SETUP, {'diff': diff})
        pg.wait_for_timeout(1500)
        # let him arrive and armor up, no hits
        for _ in range(40):
            r = pg.evaluate(CHUNK, {'n': 15, 'hit': False, 'every': 6, 'dmg': 0, 'measure': False}); pg.wait_for_timeout(10)
        # a measured stretch of ordinary fire
        for _ in range(60):
            r = pg.evaluate(CHUNK, {'n': 15, 'hit': True, 'every': 5, 'dmg': 18, 'measure': True}); pg.wait_for_timeout(10)
            if r.get('done'): break
        res['volley'] = {'skipped': True} if novolley else pg.evaluate(VOLLEY)
        # pour damage on: he must reach the twirl before he can die
        for _ in range(400):
            r = pg.evaluate(CHUNK, {'n': 15, 'hit': True, 'every': 2, 'dmg': 400, 'measure': False}); pg.wait_for_timeout(5)
            if r.get('done'): break
        res['end'] = r
        res['log'] = pg.evaluate('()=>window.__log')
        res['errors'] = errs
        b.close()
    stop()
    return res


if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('--diff', default='normal'); ap.add_argument('--old', action='store_true'); ap.add_argument('--dump', default=''); ap.add_argument('--novolley', action='store_true')
    a = ap.parse_args()
    r = run(a.diff, a.old, a.novolley)
    L = r['log']; fails = []
    shown = [f for f in L['flash'] if f['white'] > 25]
    dark = [f for f in L['flash'] if f['white'] <= 25]
    by = {}
    for f in L['flash']:
        k = f['state'] + ('/hammer' if f['onHammer'] else '/body'); by.setdefault(k, [0, 0]); by[k][0 if f['white'] > 25 else 1] += 1
    print('setup', r['setup'])
    print('flash samples', len(L['flash']), 'shown', len(shown), 'dark', len(dark))
    for k, v in sorted(by.items()): print('   %-28s white %3d  none %3d' % (k, v[0], v[1]))
    if not L['flash'] or len(dark) > len(L['flash']) * 0.05: fails.append('hits without a white flash: %d of %d' % (len(dark), len(L['flash'])))
    print('volley', r['volley'])
    v = r['volley']
    if v.get('broke'): fails.append('a passive volley broke the heal')
    if v.get('locks'): fails.append('volley missiles locked the hammer %d times' % v['locks'])
    print('end', r['end'], 'dead', L.get('dead'), 'twirl', L['twirl'])
    D = L.get('dead')
    if D and not D.get('restored'): fails.append('he died before his recovery (state %s)' % D.get('state'))
    if D and not D.get('preset') and not D.get('twirl'): fails.append('he died before the 15%% twirl (state %s)' % D.get('state'))
    if not D and not a.old: fails.append('he never died - the floor must lift once the recovery has played')
    print('deaths', json.dumps(L.get('deaths'))[:1500])
    print('states', ' > '.join(L['states'])[:900])
    print('errors', len(r['errors']), r['errors'][:3])
    if r['errors']: fails.append('page errors')
    if a.dump: json.dump(r, open(a.dump, 'w'))
    print('FAIL' if fails else 'PASS', fails)
