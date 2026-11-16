from pathlib import Path
from playwright.sync_api import sync_playwright
import sys,json
R=Path(__file__).resolve().parents[1];O=R/'_shots/cinema_overnight_1116/missile-stats';O.mkdir(parents=True,exist_ok=True);sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
errors=[];rows=[]
with sync_playwright()as w:
 b=w.chromium.launch(args=['--no-sandbox']);
 for mode in["baseline","current"]:
  guided=False
  p=b.new_page(viewport={'width':1440,'height':1000});p.set_default_timeout(120000);p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text)if m.type=='error'else None);p.goto('http://127.0.0.1:8765/index.html?night-missile-stats=1116');p.wait_for_function('window.__bofFrames>6');p.evaluate(shoot.TRAP_RAF)
  if mode=='baseline':p.evaluate('()=>{hitBoss=NMS16.base.boss;hitSubBoss=NMS16.base.mini;retinaMissileDamage=NMS16.base.retina;}')
  p.evaluate("()=>{BOFOnline.submitScore=()=>{};debugUnlocked=true;BOSSMODE.start(1,'mini','cole',false,'normal');DBGT.god=true;Input.clearTaps();for(const k of Object.keys(Input.keys))Input.keys[k]=false;window.MS16=[];const hit=hitSubBoss;hitSubBoss=function(...a){const b=subBoss,before=b?.hp,m=stageStats.mslHits;const r=hit.apply(this,a);MS16.push({before,after:b?.hp,source:_dmgSrc,kind:_dmgBullet?.kind,mslBefore:m,mslAfter:stageStats.mslHits,dmg:a[0]});return r;};}")
  p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(1)}')
  for i in range(90):e=p.evaluate(shoot.STEP,6);assert not e;p.wait_for_timeout(1)
  setup=p.evaluate("guided=>{const target=_lockTargets().filter(t=>!t.dead).sort((a,b)=>Math.abs(a.x-player.x)-Math.abs(b.x-player.x))[0];if(!target)throw Error('No native live target');player.x=target.x;player.y=Math.min(VH-36,target.y+210);if(guided)Input.keys['c']=true;return {target:{x:target.x,y:target.y,hp:target.hp},hp:subBoss.hp,ammo:run.bombs,stats:{...stageStats}};}",guided)
  if guided:
   for i in range(60):e=p.evaluate(shoot.STEP,6);assert not e;p.wait_for_timeout(1)
  p.evaluate("()=>{Input.injectTap('k');}")
  for i in range(100):e=p.evaluate(shoot.STEP,6);assert not e;p.wait_for_timeout(1)
  q=p.evaluate('({hits:MS16,hp:subBoss.hp,ammo:run.bombs,stats:{...stageStats},missiles:pBullets.filter(p=>hammerMissile(p)).map(p=>({kind:p.kind,dead:p.dead,t:p.t}))})');rows.append({'mode':mode,'guided':guided,'setup':setup,**q});p.screenshot(path=str(O/(mode+'-physical.png')));p.close()
 b.close()
(O/'physical-shipping.json').write_text(json.dumps({'rows':rows,'errors':errors,'scope':'Prepared native Normal Stage1 miniboss with no primary fire. God protects player only. Align player before launching one actual default manual missile, with/without held native Retina. Native actor HP/damage/timers remain. Baseline restores only the three pre-accounting native routers; current uses the shipping accounting owner. Tests accounting, not campaign wins.'},indent=2),encoding='utf8');print(json.dumps({'errors':errors,'rows':[{'guided':r['guided'],'hpBefore':r['setup']['hp'],'hpAfter':r['hp'],'mslHits':r['stats']['mslHits'],'hits':r['hits']}for r in rows]},indent=2))

assert not errors and len(rows)==2 and all(r['setup']['hp']-r['hp']==34 for r in rows)and rows[0]['stats']['mslHits']==0 and rows[1]['stats']['mslHits']==1
