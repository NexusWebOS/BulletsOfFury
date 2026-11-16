from pathlib import Path
from playwright.sync_api import sync_playwright
import sys,json
R=Path(__file__).resolve().parents[1];O=R/'_shots/cinema_overnight_1116/boss-loading';O.mkdir(parents=True,exist_ok=True);sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
label=sys.argv[1]if len(sys.argv)>1 else'before';delayFrames=int(sys.argv[2])if len(sys.argv)>2 else 1080;checks=[];errors=[]
with sync_playwright()as w:
 b=w.chromium.launch(args=['--no-sandbox','--autoplay-policy=no-user-gesture-required']);p=b.new_page(viewport={'width':1440,'height':1000});p.set_default_timeout(180000)
 p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text)if m.type=='error'else None)
 p.goto('http://127.0.0.1:8765/index.html?night-boss-delay=1116');p.wait_for_function('window.__bofFrames>6');p.evaluate(shoot.TRAP_RAF);p.evaluate('()=>BOFOnline.submitScore=()=>{}')
 p.evaluate("()=>{BOSSMODE.start(8,'boss','cole',false,'furious');}");p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(8)&&Object.values(RD71_ART).every(a=>XART.rdy(a.key))&&Object.values(RD94_ART).every(a=>XART.rdy(a.key))}',polling=50)
 for typ in ['purple_form','drone_charge']:
  p.evaluate("typ=>{BOFCinematicDirector.cancel();story=null;Input.clearTaps();for(const k of Object.keys(Input.keys))Input.keys[k]=false;Input.mouse.down=false;window.NightRealRdy=XART.rdy;window.NightBlockedKey=(RD94_ART[typ]||RD71_ART[typ]).key;XART.rdy=function(k){return k===NightBlockedKey?false:NightRealRdy.call(this,k)};spawnBoss('vileexistence');debugFight.spawned=true;warnT=0;setState(GS.PLAY);DBGT.god=false;player.invuln=0;RD71.events=[];window.NightHp=boss.hp;}",typ)
  p.evaluate('()=>{window.NightStageClock=stageTimer;window.NightDistance=run.distance}')
  for i in range(delayFrames//6):
   e=p.evaluate(shoot.STEP,6)
   if e:raise RuntimeError(e)
  q=p.evaluate('({mode:boss._r30.mode,t:boss._r30.t,hp:boss.hp,initial:NightHp,protected:boss._noHit,dead:player.dead,cues:RD71.events.map(e=>e.event)})');checks.append({'name':typ+' delayed18seconds preserves start, health and protection without firing cinematic cues','ok':q['mode']=='dr5er23entry'and q['t']==0 and q['hp']==q['initial']and q['protected']and not q['dead']and not q['cues'],'data':q});p.evaluate('()=>{drawWorld(0);SC12.refresh()}');p.screenshot(path=str(O/(label+'-'+typ+'-waiting.png')))
  q=p.evaluate('({stageClock:stageTimer-NightStageClock,distance:run.distance-NightDistance})');checks.append({'name':typ+' asset waiting cannot advance campaign clock or travel','ok':abs(q['stageClock'])<1e-7 and abs(q['distance'])<1e-7,'data':q})
  p.evaluate('()=>{XART.rdy=NightRealRdy;NightBlockedKey=null}');p.evaluate(shoot.STEP,6)
  q=p.evaluate('({mode:boss._r30.mode,t:boss._r30.t,hp:boss.hp,cues:RD71.events.map(e=>e.event)})');checks.append({'name':typ+' decode release resumes from the beginning','ok':q['mode']=='dr5er23entry'and 0<q['t']<.2,'data':q})
  for i in range(240):
   e=p.evaluate(shoot.STEP,6)
   if e:raise RuntimeError(e)
   if p.evaluate("boss._r30.mode==='fight'"):break
  q=p.evaluate('({mode:boss._r30.mode,hp:boss.hp,initial:NightHp,protected:boss._noHit,events:RD71.events.map(e=>e.event)})');checks.append({'name':typ+' completes the normal reveal with native intact health','ok':q['mode']=='fight'and q['hp']==q['initial']and not q['protected'],'data':q});p.evaluate('()=>{drawWorld(0);SC12.refresh()}');p.screenshot(path=str(O/(label+'-'+typ+'-resumed.png')))
 checks.append({'name':'No page or console errors','ok':not errors,'data':errors});b.close()
(O/(label+'.json')).write_text(json.dumps({'checks':checks,'errors':errors,'scope':'Controlled required-bitmap readiness delay before a fresh native Stage8 boss spawn. Native loop, introduction, protection, HP and cues; no phase/timer/enemy HP writes. Not a spontaneous network report or combat win.'},indent=2),encoding='utf8');print(json.dumps(checks,indent=2));assert all(c['ok']for c in checks)
