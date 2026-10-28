from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image,ImageDraw
import sys,json,base64
R=Path(__file__).resolve().parents[1];
import argparse
ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,default=R/'_shots/hud_timers_1027');W=ap.parse_args().out;W.mkdir(parents=True,exist_ok=True);
sys.path.insert(0,str(R/'_BUILD_SOURCE'));from shoot import serve,TRAP_RAF,STEP
port,stop=serve(str(R));errors=[];console=[];http=[];checks=[];layouts=[];portraits=[]
with sync_playwright()as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required']);p=b.new_page(viewport={'width':1280,'height':800});p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:console.append(m.text)if m.type=='error'or'draw error'in m.text else None);p.on('response',lambda r:http.append({'url':r.url,'status':r.status})if r.status>=400 else None)
 p.goto(f'http://127.0.0.1:{port}/index.html?hudrev=solid-r-1027d',wait_until='load',timeout=180000);p.wait_for_function('window.__bofFrames>5&&typeof HUD28!=="undefined"&&pm27Live()',timeout=120000);p.mouse.click(3,3);p.evaluate(TRAP_RAF)
 p.evaluate('stageLoadBegin(1)');p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(1)}',timeout=180000)
 def step(n):
  e=p.evaluate(STEP,n)
  if e:raise RuntimeError(e)
 def test(name,value):checks.append({'name':name,'pass':bool(value)});assert value,name
 def read():return p.evaluate('()=>({stage:HUD28.stage.seconds,encounter:HUD28.encounter?.seconds??null,kind:HUD28.encounter?.kind??null,actor:HUD28.encounter?.actor===boss,finished:!!HUD28.encounter?.finished,state})')
 def setup():
  p.evaluate("()=>{coopOn=false;pilotIndex=PILOTS.findIndex(p=>p.key==='cole');run.mode='arcade';startRun(1);beginStage(1);BOFCinematicDirector.cancel();story=null;debugUnlocked=true;DBGT.god=true;player.invuln=0;setState(GS.PLAY);stagePlan=[];UI20.dirty=true;}")
 setup();step(90);a=read();test('Stage clock runs during ordinary waves before any boss',a['stage']>1 and a['encounter']is None)
 p.evaluate("setState('paused')");step(90);z=read();test('Pause holds stage time',z['stage']==a['stage']);p.evaluate('setState(GS.PLAY)');step(30);test('Resume advances the same stage clock',read()['stage']>a['stage'])
 p.evaluate('()=>{spawnSubBoss(SUBBOSS[1].kind);subBossActive=true;}');step(60);m=read();test('Miniboss gets its own clock while stage time continues',m['kind']=='MINIBOSS'and m['encounter']>.5 and m['stage']>a['stage'])
 p.evaluate("setState('paused')");step(60);test('Pause holds encounter and stage clocks',read()['encounter']==m['encounter']and read()['stage']==m['stage']);p.evaluate('setState(GS.PLAY)');step(30)
 p.evaluate('()=>{subBoss.dead=true;subBossActive=false;}');step(30);d=read();step(30);test('Defeated encounter time is held',read()['encounter']==d['encounter']and read()['finished'])
 p.evaluate('()=>{spawnBoss(STAGES[0].boss);bossActive=true;}');step(15);q=read();test('Boss appearance starts a fresh encounter clock',q['kind']=='BOSS'and 0<q['encounter']<1 and q['actor']);step(60);test('Boss entrance and phase ownership do not reset its clock',read()['encounter']>q['encounter'])
 p.evaluate("()=>{const a=achievementStageComplete,f=furiousConvertStage;try{achievementStageComplete=()=>{};furiousConvertStage=()=>{};computeStageResults();}finally{achievementStageComplete=a;furiousConvertStage=f;}}")
 value=p.evaluate('drawStageClear._res.clearT');test('Stage result snapshots the full completion time',abs(value-read()['stage'])<.001);step(30);test('Result time stays frozen after later simulation',p.evaluate('drawStageClear._res.clearT')==value)
 p.evaluate('beginStage(1)');test('Retry/new stage resets both clocks',read()['stage']==0 and read()['encounter']is None)
 p.evaluate('()=>{BOFCinematicDirector.cancel();story=null;setState(GS.PLAY);stagePlan=[];}');step(90)
 p.wait_for_function("()=>PILOTS.every(p=>XART.rdy(commPortrait(p.key,'idle')))&&ui20IconReady('ship_cole')",timeout=120000);p.evaluate('UI20.dirty=true');step(10)
 for width,height,name in [(1280,800,'wide'),(1920,1080,'large'),(960,720,'small-wide'),(390,844,'portrait')]:
  p.set_viewport_size({'width':width,'height':height});p.evaluate('window.__bofFit()');step(8);L=p.evaluate('()=>({mode:SC12.mode,headers:HUD28.layout.headers,panels:SC12.panels.map(c=>{const r=c.getBoundingClientRect();return{x:r.x,y:r.y,w:r.width,h:r.height}}),fs:(()=>{const r=document.getElementById("fs-btn").getBoundingClientRect();return{x:r.x,y:r.y,w:r.width,h:r.height}})(),field:SC12.layout.field})');layouts.append({'name':name,**L});p.screenshot(path=str(W/('hud-'+name+'.png')))
  for H in L['headers']:
   if not H['visible']:continue
   test(name+' timer stays inside viewport',H['x']>=-.1 and H['y']>=-.1 and H['x']+H['w']<=width+.1 and H['y']+H['h']<=height+.1)
  if L['mode']=='sides':
   test(name+' clocks sit above their HUD columns',all(H['y']+H['h']<=P['y']+.2 for H,P in zip(L['headers'][:2],L['panels'])))
   test(name+' fullscreen button stays above the right clock',L['fs']['y']+L['fs']['h']<=L['headers'][1]['y'])
 p.set_viewport_size({'width':1280,'height':800});p.evaluate('window.__bofFit()');step(5)
 for key in p.evaluate('PILOTS.map(p=>p.key)'):
  p.evaluate("key=>{run.pilot=key;UI20.dirty=true;SC12.refresh();}",key);data=p.evaluate('SC12.panels[1].toDataURL().split(",")[1]');(W/('pilot-'+key+'.png')).write_bytes(base64.b64decode(data));metrics=p.evaluate('key=>{const im=XART.get(commPortrait(key,"idle")),c=document.createElement("canvas");c.width=c.height=260;const r=ui20Portrait(c.getContext("2d"),commPortrait(key,"idle"),{x:10,y:10,w:228,h:228});return{pilot:key,size:[im.width,im.height],rect:r,nameWidth:pm27Width(key.toUpperCase(),pm27Fit(key.toUpperCase(),28,198,"fury_strike").height,"fury_strike")}}',key);portraits.append(metrics);r=metrics['rect'];test(key+' full portrait fits square opening',r['x']>=10 and r['y']>=10 and r['x']+r['w']<=238.1 and r['y']+r['h']<=238.1);test(key+' name fits the narrow name strip',metrics['nameWidth']<=198)
 p.evaluate("()=>{coopOn=true;pilotIndex=PILOTS.findIndex(p=>p.key==='cole');p2Index=PILOTS.findIndex(p=>p.key==='axel');startRun(1);beginStage(1);BOFCinematicDirector.cancel();story=null;setState(GS.PLAY);UI20.dirty=true;}");step(60);p.evaluate('window.__bofFit()');step(10);p.screenshot(path=str(W/'hud-coop.png'));test('Co-op keeps two native HUD rows and one shared stage clock',p.evaluate('seatList().length===2&&SC12.panels[0].height===2048&&HUD28.layout.headers[0].visible'))
 setup();step(60);p.wait_for_function("()=>XART.rdy(commPortrait('cole','idle'))&&ui20IconReady('ship_cole')",timeout=120000);p.evaluate('UI20.dirty=true');step(20);p.screenshot(path=str(W/'hud-final.png'))
 p.evaluate('()=>{spawnSubBoss(SUBBOSS[1].kind);subBossActive=true;}');step(75);p.screenshot(path=str(W/'hud-miniboss.png'))
 p.evaluate('setState(GS.TITLE)');step(5);test('Menu hides all clock canvases',p.evaluate('HUD28.canvases.every(c=>c.style.display==="none")'));b.close()
stop();(W/'checks.json').write_text(json.dumps({'checks':checks,'layouts':layouts,'portraits':portraits,'pageErrors':errors,'consoleErrors':console,'HTTPerrors':http},indent=2));assert not errors;assert not http;print(json.dumps({'checksPassed':len(checks),'pageErrors':errors,'HTTPerrors':http,'console':console[:8]},indent=2))
