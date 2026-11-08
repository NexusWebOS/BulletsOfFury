from pathlib import Path
import subprocess,json,time,urllib.request,sys
from playwright.sync_api import sync_playwright
W=Path(__file__).resolve().parent;R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');T=W.parent/'Releases/BulletsOfFury-Windows-2026-11-06';Q=R/'_shots/locked_pilot_1106/native';Q.mkdir(parents=True,exist_ok=True);port=48978;checks=[];p1=None
def ck(n,v,d=None):checks.append(dict(name=n,passed=bool(v),data=d));print('PASS'if v else'FAIL',n,str(d)[:100]if d is not None else'',flush=True)
try:
 p1=subprocess.Popen([str(T/'Bullets of Fury.exe'),'--qa-dir',str(Q),'--profile',str(Q/'profile'),'--debug-port',str(port)],cwd=T)
 end=time.monotonic()+60
 while time.monotonic()<end:
  try:
   urllib.request.urlopen(f'http://127.0.0.1:{port}/json/version',timeout=.4).close();break
  except:time.sleep(.2)
 with sync_playwright()as pw:
  b=pw.chromium.connect_over_cdp(f'http://127.0.0.1:{port}');p=b.contexts[0].pages[0];errors=[];missing=[];p.on('pageerror',lambda e:errors.append(str(e)));p.on('response',lambda q:missing.append(q.url)if q.status>=400 else None);p.wait_for_function('window.__bofFrames>3',timeout=180000)
  log=[json.loads(s)for s in(Q/'desktop.jsonl').read_text(encoding='utf8').splitlines()];row=[r for r in log if r['name']=='game-navigation'][-1]['data']
  ck('Updated game EXE still starts fullscreen at high quality',row['fullscreen']and row['bounds']==row['screen']and p.evaluate('()=>SS===2&&!DBGT.god'))
  sys.path.insert(0,str(R/'_BUILD_SOURCE'));from shoot import TRAP_RAF
  p.evaluate(TRAP_RAF);p.wait_for_function('()=>Object.values(LP116.banks).every(a=>XART.rdy(a.key))&&pm27Live()',polling=100,timeout=90000)
  p.evaluate("()=>{coleUnlocked=coleSessionUnlocked=false;run.mode='arcade';pilotIndex=PILOTS.findIndex(p=>p.key==='cole');pilotFrom=pilotIndex;pilotPending=null;pilotRot=0;setState(GS.PILOT);_setPilotViewport();ctx.setTransform(SS,0,0,SS,0,0);}")
  phases=[]
  for t,name in [(.1,'gray'),(.55,'black')]:
   phases.append(p.evaluate('t=>{stateT=t;drawPilot(0);return {phase:LP116.lastCard.phase,bg:lp116Background(),panel:lp116Panel(),body:!!LP116.lastCard.body,ship:!!LP116.lastCard.ship,lock:!!LP116.lastCard.lock};}',t));p.screenshot(path=str(Q/('locked-'+name+'.png')))
  ck('Packaged assets render both gray/black silhouettes, neutral backgrounds and padlocks',all(r['body']and r['ship']and r['lock']for r in phases)and phases[0]['phase']==0 and phases[1]['phase']==1,phases)
  ck('Packaged locked Cole cannot deploy',p.evaluate('()=>{confirmPilot();return state===GS.PILOT&&pilotPending===null;}'))
  p.evaluate('()=>{pwInput="COLE4U";submitPassword();setState(GS.PILOT);pilotRot=0;stateT=.2;}');p.wait_for_function('()=>XART.rdy("cole_body_0922")&&XART.rdy("ship_cole_pv2")',polling=100)
  ck('Packaged real unlock restores color and stops the silhouette cycle',p.evaluate('()=>{const n=LP116.draws;drawPilot(.5);return !isPilotLocked(PILOTS[pilotIndex])&&LP116.draws===n&&LP116.lastCard.phase!==undefined;}'))
  ck('Packaged game keeps the bullet/sonic interception contract',p.evaluate('()=>!enemyOrdnanceCanIntercept({kind:"s1bullet",_er26Art:"fire"})&&!enemyOrdnanceCanIntercept({kind:"rzbSonic",_er26Art:"fire"})&&enemyOrdnanceCanIntercept({kind:"emissile"})'))
  ck('No native game runtime errors or missing assets',not errors and not missing,{'errors':errors,'missing':missing})
  p.evaluate('()=>window.close()');p1.wait(timeout=20);p1=None;b.close()
finally:
 if p1 and p1.poll()is None:p1.terminate();p1.wait(timeout=15)
 (Q/'checks.json').write_text(json.dumps(checks,indent=2));(W/'native-verification.json').write_text(json.dumps({'directory':str(Q),'checks':checks},indent=2))
if any(not c['passed']for c in checks):raise SystemExit(1)
