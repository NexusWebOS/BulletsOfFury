from pathlib import Path
import json,time,sys
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[2];O=R/'_shots/boss_boot_1109';O.mkdir(exist_ok=True)
checks=[];errors=[];states=[]
def ck(name,q):
 checks.append(dict(name=name,passed=bool(q)));print(('PASS 'if q else'FAIL ')+name,flush=True)
 assert q,name
with sync_playwright()as pw:
 for stage in ([8]if '--stage8-only'in sys.argv else[5,8]):
  br=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required'])
  ctx=br.new_context(viewport={'width':1280,'height':800});p=ctx.new_page()
  p.on('pageerror',lambda e:errors.append(str(e)))
  p.on('console',lambda m:errors.append(m.text)if m.type=='error'else None)
  p.goto('http://127.0.0.1:8879/index.html',wait_until='load',timeout=180000)
  p.wait_for_function('window.__bofFrames>5&&typeof BP119!=="undefined"',timeout=180000)
  p.mouse.click(3,3)
  q=p.evaluate('(s)=>{debugUnlocked=true;diffKey="furious";const ok=debugStartFight(debugFightFor(s,"boss"),{pilot:"cole"});DBGT.god=true;return{ok,pending:bp119Pending(),time:stageTimer,warn:warnT};}',stage)
  ck(f'Stage{stage}: native debug entry waits for resources',q['ok']and q['pending'])
  p.wait_for_timeout(1500)
  held=p.evaluate('()=>({pending:bp119Pending(),time:stageTimer,warn:warnT,boss:!!boss,load:stageLoadInfo(run.stage),overlay:typeof drawStageLoadOverlay==="function"})')
  ck(f'Stage{stage}: combat clocks and warning held while loading',held['time']==q['time']and held['warn']==q['warn']and not held['boss'])
  p.screenshot(path=str(O/f'stage{stage}-loading.png'))
  ck(f'Stage{stage}: existing loading overlay is active',held['pending']and held['overlay'])
  started=time.monotonic()
  # Read-only polling: all resource work comes from the unmodified native RAF loop.
  p.wait_for_function('!bp119Pending()&&stageLoadReady(run.stage)',polling=100,timeout=180000)
  ready=p.evaluate('()=>({load:stageLoadInfo(run.stage),events:BP119.events.slice(),time:stageTimer})')
  ready['seconds']=round(time.monotonic()-started,2);ready['stage']=stage;states.append(ready)
  print(json.dumps(ready),flush=True)
  ck(f'Stage{stage}: native frame loop releases after decoded load',ready['load']['ready']and any(e['type']=='ready'for e in ready['events']))
  p.wait_for_function('!!boss&&bossActive',timeout=20000)
  p.wait_for_timeout(5000)
  q=p.evaluate('()=>({stage:run.stage,boss:boss?.kind,active:bossActive,time:stageTimer,portrait:!!XART.rdy("cole_portrait")})')
  ck(f'Stage{stage}: boss encounter starts after load',q['active']and bool(q['boss']))
  p.screenshot(path=str(O/f'stage{stage}-ready.png'))
  if stage==8:
   p.wait_for_function('boss?._r30?.mode==="v18arrival"&&boss._r30.t>.6',timeout=45000)
   ck('Stage8: gated entrance reaches a decoded visible drone',p.evaluate('RD71.last?.gated&&XART.rdy(RD71_ART.drone_emerge.key)'))
   p.screenshot(path=str(O/'stage8-drone-visible.png'))
  if stage==5:
   p.evaluate('()=>{debugStartFight(debugFightFor(5,"boss"),{pilot:"cole"});BP119.pending=debugFight;setState(GS.TITLE);debugFight=null;}')
   ck('Leaving preview clears its loading ownership',p.evaluate('!bp119Pending()'))
  ctx.close();br.close()
ck('Cold launches have no browser or renderer errors',not errors)
(O/('stage8-entrance-checks.json'if '--stage8-only'in sys.argv else'cold-entry-checks.json')).write_text(json.dumps(dict(checks=checks,errors=errors,loads=states),indent=2),encoding='utf8')
print(json.dumps(dict(passed=len(checks),errors=errors)),flush=True)
