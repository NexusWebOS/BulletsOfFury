from pathlib import Path
import sys,json,http.server,hashlib
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];W=R/'_shots/sewer_rescue_1031';W.mkdir(parents=True,exist_ok=True);O=W/'probe';O.mkdir(exist_ok=True);sys.path.insert(0,str(R/'_BUILD_SOURCE'));from shoot import serve,STEP,TRAP_RAF
http.server.ThreadingHTTPServer.request_queue_size=256;checks=[];errors=[]
def ck(n,v,d=None):checks.append(dict(name=n,passed=bool(v),data=d));(W/'checks.json').write_text(json.dumps(checks,indent=2));print('PASS'if v else'FAIL',n,str(d)[:250]if not v else'',flush=True)
def step(p,n):
 for i in range(0,n,10):
  e=p.evaluate(STEP,min(10,n-i));assert not e,e;p.wait_for_timeout(1)
def snap(p,n):p.evaluate('drawWorld(0)');p.screenshot(path=str(O/(n+'.png')))
port,stop=serve(str(R))
try:
 with sync_playwright()as pw:
  br=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required']);p=br.new_page(viewport={'width':1280,'height':800});p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text)if m.type=='error'or'draw error'in m.text else None)
  p.goto(f'http://127.0.0.1:{port}/index.html',wait_until='load',timeout=180000);p.wait_for_function('window.__bofFrames>5');p.mouse.click(3,3);p.evaluate('()=>{run.stage=7;stageLoadBegin(7)}');p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(7)}',timeout=180000);p.evaluate(TRAP_RAF)
  p.evaluate("()=>{diffKey='furious';debugStartFight({stage:7,role:'boss',kind:'sludgeemperor'},{pilot:'cole',record:false});spawnBoss('sludgeemperor');debugFight.spawned=true;bossActive=true;warnT=0;DBGT.god=true;player.invuln=1e9;BOFCinematicDirector.cancel();setState(GS.PLAY);window.B=boss;}");step(p,650)
  ck('Actual explosion, smoke and gated portal art preloads',p.evaluate("Object.values(SR93_ART).every(a=>XART.rdy(a.key))&&Object.values(SC86_ART).filter(a=>a.key.includes('green')).every(a=>XART.rdy(a.key))"))
  p.evaluate("()=>{debugFight=null;run.mode='campaign';window.M=B._s7mod;for(const p of M.parts)p.hp=0;for(const p of M.er28Canisters||[]){p.hp=0;p.dead=true;}M.shield=0;M.core=10;B.hp=10;s7mSet(B,'recover');player.x=343;player.y=VH-65;mapScroll=levelScrollRange()-1800;drawWorld(0);window.score93=run.score;s7mHit(B,11,B.x,B.y,'core');}");step(p,1)
  p.evaluate('window.E=M.frExit;window.Q=E.sc86;window.C=Q.sr93');ck('Real Warden core defeat begins fast travel immediately',p.evaluate("M.mode==='dead'&&C.phase==='run'&&Q.phase==='advance'&&!B.dead"))
  start=p.evaluate('Q.source');step(p,30);end=p.evaluate('Q.source');ck('Travel remains a fast400px/s instead of easing to a stop',abs((start-end)-200)<1,[start,end]);snap(p,'01-fast-collapse')
  ck('Blasts and smoke rings are active throughout the run',p.evaluate('SR93.fx.length>5&&SR93.draws.dense>0&&SR93.draws.ring>0'))
  ck('No reward is granted during the escape',p.evaluate('run.score===score93&&!B._forgeRewardDropped'))
  p.evaluate('window.a93=Q.age;window.s93=Q.source;window.f93=SR93.fx.map(f=>f.age);setState(GS.PAUSE)');step(p,40);ck('Pause freezes the route and collapse effects',p.evaluate('Q.age===a93&&Q.source===s93&&SR93.fx.every((f,i)=>f.age===f93[i])'));p.evaluate('setState(GS.PLAY)')
  p.evaluate('window.x93=player.x;Input.keys.a=true');step(p,8);p.evaluate('Input.keys.a=false');ck('Pilot can steer during the fast escape',p.evaluate('player.x<x93-5'))
  samples=[]
  for _ in range(300):
   if not p.evaluate("C.phase==='run'"):break
   samples.append(p.evaluate('({source:Q.source,age:Q.age,fx:SR93.fx.length})'));step(p,3)
  ck('Original chamber is reached continuously without a map reversal',all(a['source']>=b['source']for a,b in zip(samples,samples[1:])))
  ck('Gate forms automatically while the floor is still moving',p.evaluate("C.phase==='form'&&Q.source>200"),p.evaluate('({phase:C.phase,source:Q.source})'))
  step(p,12);snap(p,'02-unexpected-gate');ck('Decker cries the exact warning with the selected pilot name',p.evaluate("B._s7warden.final.radio.who==='DECKER'&&B._s7warden.final.radio.full==='WHAT IS THAT? COLE, NOOOO!'"),p.evaluate('B._s7warden.final.radio'))
  ck('Portal stays registered in the original stone aperture',p.evaluate('E.portalX===343&&Math.abs(E.portalY-(310-Q.source))<.001'))
  for _ in range(90):
   if p.evaluate("C.phase==='enter'"):break
   step(p,1)
  ck('Entry starts without waiting for an approach prompt',p.evaluate("C.phase==='enter'&&Q.source>200"),p.evaluate('({phase:C.phase,source:Q.source})'));step(p,20);snap(p,'03-nick-of-time-entry')
  ck('Actual green gate loop and shrinking jet frames are used',p.evaluate('SC86.draws.green_form>0&&SC86.draws.green_loop>0&&C.phase===\'enter\''))
  for _ in range(90):
   if p.evaluate("C.phase==='close'"):break
   step(p,1)
  ck('Pilot disappears just before the explosion front reaches the gate',p.evaluate('B._s7warden.final.shipHidden&&C.safeMargin>=20&&C.safeMargin<=25'),p.evaluate('({margin:C.safeMargin,portal:E.portalY,source:Q.source})'));snap(p,'04-saved-as-blast-catches-up')
  ck('Terrain only stops after the aircraft is inside the gate',p.evaluate('Q.source<15'))
  for _ in range(180):
   if p.evaluate('run.stage===8&&state===GS.WARPENTRY'):break
   step(p,3)
  ck('Native Stage8 portal handoff completes',p.evaluate('run.stage===8&&state===GS.WARPENTRY'),p.evaluate('({stage:run.stage,state})'))
  ck('Native Forge reward and score remain single owned grants',p.evaluate('B._forgeRewardDropped&&B.dead&&B._s7warden.final.finished&&run.score>=score93+35000'))
  ck('Campaign progression retains the direct Stage8 entry flag',p.evaluate('run._l78Entry===1&&campaign.unlockedMax>=8'))
  ck('Effects cannot leak into Stage8',p.evaluate('SR93.fx.length===0&&!SR93.owner'))
  ck('Explosion budget stays bounded',max(s['fx']for s in samples)<76)
  ck('No browser or rendering errors',not errors,errors)
  ck('Core engine source remains unchanged',hashlib.sha256((R/'assets/game.js').read_bytes()).hexdigest()=='024a0933c5729b6afa2a6e88864574636293bdb535d9f4e5eb91d36bb98509de')
  (W/'events.json').write_text(json.dumps(p.evaluate('SR93.events'),indent=2));br.close()
finally:stop()
print('RESULT',sum(c['passed']for c in checks),'/',len(checks));assert all(c['passed']for c in checks)
