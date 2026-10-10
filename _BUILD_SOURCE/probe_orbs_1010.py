"""Orb weapon audit (Mike, 2026-10-10: "all orbs need to be more powerful... some of them even break
and just disappear with no effects, no blasts, no nothing and you just die").

    python _BUILD_SOURCE/probe_orbs_1010.py [label] [row|bosses|all]

row     every orb variant plus MG / spread / missile / laser hold fire for SECONDS against a fixed
        row of high-HP targets: damage per second, how each orb ended, silent endings.
bosses  the orb variants fight every stage's miniboss and boss: damage per second against the
        encounter, and every orb ending recorded with the function that ended it.
An ending is SILENT when nothing visible appears within 60px of the orb on the frame it ends
(no explode, efxBurst, iceBurst/shard, thermoshock fx or zap). Writes _shots/orbs_1010/<label>.json.
Fixtures pin the targets, refill encounter HP and protect the pilot; this is not a balance run.
"""
import json, os, sys
from pathlib import Path
from playwright.sync_api import sync_playwright
sys.path.insert(0, str(Path(__file__).parent))
import shoot as sh

ROOT = Path(__file__).resolve().parents[1]
LABEL = sys.argv[1] if len(sys.argv) > 1 else 'run'
MODE = sys.argv[2] if len(sys.argv) > 2 else 'all'
OUT = ROOT / '_shots/orbs_1010'
OUT.mkdir(parents=True, exist_ok=True)
LV = 3
REFERENCE = [('mg', 0, 'cole', ''), ('spread', 1, 'cole', ''), ('missile', 2, 'cole', ''), ('laser', 3, 'cole', '')]
ORBS = [
    ('iceorb', 5, 'cole', "run.wvars[5]='iceorb';"),
    ('fireorb', 5, 'cole', "run.wvars[5]='fireorb';"),
    ('fireice', 5, 'freezer', "run.wvars[5]='fireice';"),
    ('toxicorb', 5, 'cole', "run.wvars[5]='toxicorb';"),
    ('forge_fire', 5, 'cole', "run.forge={5:{elem:'fire',lv:1}};"),
    ('forge_ice', 5, 'cole', "run.forge={5:{elem:'ice',lv:1}};"),
    ('forge_lightning', 5, 'cole', "run.forge={5:{elem:'lightning',lv:1}};"),
    ('forge_prism', 5, 'cole', "run.forge={5:{elem:'prism',lv:1}};"),
    ('forge_toxic', 5, 'cole', "run.forge={5:{elem:'toxic',lv:1}};"),
    ('forge_kinetic', 5, 'cole', "run.forge={5:{elem:'kinetic',lv:1}};"),
    ('forge_chrome', 5, 'cole', "run.forge={5:{elem:'chrome',lv:1}};"),
    ('forge_water', 5, 'cole', "run.forge={5:{elem:'water',lv:1}};"),
    ('forge_dark', 5, 'cole', "run.forge={5:{elem:'dark',lv:1}};"),
    ('yuri_orb', 8, 'yuri', ''),
]

INSTALL = r"""()=>{
  if(window.__orbAudit)return;window.__orbAudit=1;window.__fx=[];
  const wrap=(name,xy)=>{const f=window[name];if(typeof f!=='function')return;window[name]=function(){const p=xy(arguments);if(p)__fx.push(p);return f.apply(this,arguments);};};
  // classic-script globals are reassigned through eval so the game's own callers see the wrapper
  for(const [n,ix,iy] of [['explode',0,1],['efxBurst',1,2],['iceBurst',0,1],['tsFx',0,1],['spawnShockRing',0,1]]){
    try{const f=eval(n);if(typeof f!=='function')continue;window['__o_'+n]=f;
      eval(n+'=function(){__fx.push({x:+arguments['+ix+'],y:+arguments['+iy+']});return window.__o_'+n+'.apply(this,arguments);}');}catch(e){}
  }
  window.__isOrb=q=>q&&(q.kind==='orb'||q.kind==='yuriLightningOrb');
  window.__orbLog=[];
  window.__frame=function(){
    const z0=(typeof zaps!=='undefined'?zaps.length:0);__fx.length=0;
    const live=pBullets.filter(q=>__isOrb(q)&&!q.dead);
    for(const q of live){if(q.__trap)continue;q.__trap=1;let dead=false;
      Object.defineProperty(q,'dead',{get(){return dead},set(v){if(v&&!dead){
        q.__why=new Error().stack.split(String.fromCharCode(10)).slice(2,4).map(z=>z.trim().replace(/\(?http:\/\/127.0.0.1:\d+\/assets\//,'').replace(/\?v=[^:]*/,'').replace(/:\d+\)?$/,'')).join(' < ');
        q.__at={x:q.x,y:q.y,life:q.life};}dead=v;},configurable:true});}
    window.__bofStepNow+=1000/60;loop(window.__bofStepNow);
    const zap=(typeof zaps!=='undefined'?zaps.slice(z0):[]);
    for(const q of live){if(!q.dead&&pBullets.includes(q))continue;
      const at=q.__at||{x:q.x,y:q.y,life:q.life};
      const near=__fx.some(f=>Number.isFinite(f.x)&&Math.hypot(f.x-at.x,f.y-at.y)<60)||zap.some(z=>Math.hypot(z.x1-at.x,z.y1-at.y)<60);
      __orbLog.push({why:q.__why||'spliced out of pBullets',impact:!!q._impact,life:+(at.life||0).toFixed(2),x:Math.round(at.x),y:Math.round(at.y),silent:!near,offscreen:at.y<-20});}
  };
}"""

ARM = r"""([w,lv,setup,pilot])=>{
  run.pilot=pilot;run.forge={};run.wvars=run.wvars||{};run.wvars[5]=null;run.infusion=null;
  if(!run.wlevels)run.wlevels=WEAPONS.map(()=>0);
  (new Function(setup))();
  if(w===8&&typeof yuriLightningOrbIsUnlocked==='function'){window.__yu=window.__yu||yuriLightningOrbIsUnlocked;yuriLightningOrbIsUnlocked=()=>true;}
  if(run.forge&&run.forge[w])run.infusion={elem:run.forge[w].elem,lv:1};
  run.weapon=w;run.wlevel=lv;run.wlevels[w]=lv;pBullets.length=0;__orbLog.length=0;
}"""

ROW = r"""(seconds)=>{
  window.__bofStepNow=window.__bofStepNow||performance.now();
  enemies.length=0;eBullets.length=0;efxBursts.length=0;player.x=worldWidth()/2;player.y=VH-70;
  const T=[];
  for(const [dx,dy] of [[0,-150],[-46,-210],[46,-210],[-120,-150],[120,-150],[0,-280]]){
    const e=spawnEnemy('s1tankheavy',player.x+dx,player.y+dy,{});if(!e)continue;
    Object.assign(e,{x:player.x+dx,y:player.y+dy,hp:1e6,maxhp:1e6,pattern:'__dummy',shoots:false,fk:null,vx:0,vy:0,_noSep:true,t:0});e.__home={x:e.x,y:e.y};T.push(e);}
  for(let i=0;i<seconds*60;i++){
    for(const e of T){e.x=e.__home.x;e.y=e.__home.y;e.t=0;}
    player.invuln=1e9;player.x=worldWidth()/2;player.y=VH-70;Input.keys['j']=true;__frame();}
  Input.keys['j']=false;
  return {dealt:T.reduce((a,e)=>a+(1e6-e.hp),0),log:__orbLog.slice(),targets:T.length};
}"""

FIGHT = r"""([kind,which,seconds])=>{
  window.__bofStepNow=window.__bofStepNow||performance.now();
  enemies.length=0;eBullets.length=0;pBullets.length=0;
  if(which==='mini'){spawnSubBoss(kind);}else{spawnBoss(kind);}
  const B=()=>which==='mini'?subBoss:boss;
  // let it arrive
  for(let i=0;i<300&&B()&&(B().enter||B()._noHit);i++){player.invuln=1e9;Input.keys['j']=false;window.__bofStepNow+=1000/60;loop(window.__bofStepNow);}
  if(!B())return {err:'no encounter'};
  let dealt=0;const floor=B().maxhp*.5;
  for(let i=0;i<seconds*60;i++){
    const b=B();if(!b||b.dead)break;
    if(b.hp<floor){dealt+=floor-b.hp+0;b.hp=b.maxhp;}
    const h0=b.hp;player.invuln=1e9;player.x=b.x;player.y=Math.min(VH-60,(b._drawY||b.y)+190);Input.keys['j']=true;__frame();
    const b2=B();if(b2)dealt+=Math.max(0,h0-b2.hp);
  }
  Input.keys['j']=false;
  return {dealt,log:__orbLog.slice(),name:B()&&B().name};
}"""


def summarize(log):
    why = {}
    for d in log:
        k = d['why'] + (' [impact]' if d['impact'] else '')
        why[k] = why.get(k, 0) + 1
    silent = [d for d in log if d['silent'] and not d['offscreen']]
    return why, silent


def newpage(b, port, stage, pilot):
    pg = b.new_page(viewport={'width': 1100, 'height': 1200})
    errs = []
    pg.on('pageerror', lambda e: errs.append(str(e)[:200]))
    if os.environ.get('ORB_BASELINE'):   # the pre-rework orb: serve an empty orbs_1010.js
        pg.route('**/orbs_1010.js*', lambda r: r.fulfill(status=200, body='', content_type='application/javascript'))
    pg.goto(f'http://127.0.0.1:{port}/index.html')
    pg.wait_for_function("()=>window.__bofAssetRuntimeReady&&(window.__bofFrames|0)>4", timeout=120000)
    pg.evaluate(sh.TRAP_RAF)
    pg.evaluate(sh.SETUP, {'state': 'PLAY', 'stage': stage, 'pilot': pilot, 'invuln': True})
    pg.evaluate("()=>{window.__bofStepNow=performance.now();}")
    # Stage 6's scripted opening locks every weapon (MG included); end it so the fight is measurable
    pg.evaluate("()=>{if(typeof s6OpeningActive==='function'&&s6OpeningActive())s6Opening=null;}")
    pg.evaluate(INSTALL)
    return pg, errs


def main():
    port, stop = sh.serve(str(ROOT))
    results = {'row': {}, 'bosses': {}}
    try:
        with sync_playwright() as pw:
            b = pw.chromium.launch(args=['--mute-audio'])
            if MODE in ('row', 'all'):
                pg, errs = newpage(b, port, 1, 'cole')
                for name, w, pilot, setup in REFERENCE + ORBS:
                    pg.evaluate(ARM, [w, LV, setup, pilot])
                    r = pg.evaluate(ROW, 6)
                    why, silent = summarize(r['log'])
                    results['row'][name] = {'dps': round(r['dealt'] / 6, 1), 'orbs': len(r['log']), 'endings': why, 'silent': len(silent), 'silentSample': silent[:3]}
                    print(f"ROW {name:16s} targets {r.get('targets')} dps {r['dealt']/6:7.1f} orbs {len(r['log']):3d} silent {len(silent):3d} {json.dumps(why)[:240]}", flush=True)
                results['row_errors'] = errs[:5]
                pg.close()
            if MODE in ('bosses', 'all'):
                for stage in [int(x) for x in os.environ.get('ORB_STAGES', '1,2,3,4,5,6,7,8').split(',')]:
                    pg, errs = newpage(b, port, stage, 'cole')
                    targets = pg.evaluate("n=>({mini:SUBBOSS[n]&&SUBBOSS[n].kind,boss:STAGES[n-1]&&STAGES[n-1].boss})", stage)
                    for which in ('mini', 'boss'):
                        kind = targets.get(which)
                        if not kind:
                            continue
                        for name, w, pilot, setup in [REFERENCE[0], REFERENCE[3]] + ORBS:
                            pg.evaluate(ARM, [w, LV, setup, pilot])
                            try:
                                r = pg.evaluate(FIGHT, [kind, which, 5])
                            except Exception as e:
                                r = {'err': str(e)[:200], 'log': [], 'dealt': 0}
                            why, silent = summarize(r.get('log', []))
                            key = f's{stage}-{which}-{kind}'
                            results['bosses'].setdefault(key, {})[name] = {'dps': round(r.get('dealt', 0) / 5, 1), 'orbs': len(r.get('log', [])), 'endings': why, 'silent': len(silent), 'silentSample': silent[:2], 'err': r.get('err')}
                            if silent or r.get('err'):
                                print(f"{key:28s} {name:16s} dps {r.get('dealt',0)/5:7.1f} SILENT {len(silent)} {r.get('err') or ''} {json.dumps(why)[:300]}", flush=True)
                        print(f"{f's{stage}-{which}-{kind}':28s} done: " + ' '.join(f"{n}={v['dps']}" for n, v in results['bosses'][f's{stage}-{which}-{kind}'].items()), flush=True)
                    results.setdefault('boss_errors', {})[stage] = errs[:5]
                    pg.close()
            b.close()
    finally:
        stop()
    (OUT / (LABEL + '.json')).write_text(json.dumps(results, indent=1))


if __name__ == '__main__':
    main()
