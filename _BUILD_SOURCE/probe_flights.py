from pathlib import Path
import sys,json
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
O=R/'_shots/flight_variants_1012';O.mkdir(exist_ok=True);port,stop=shoot.serve(str(R));errors=[];result=[]
try:
 with sync_playwright() as pw:
  b=pw.chromium.launch(channel='msedge',args=['--mute-audio']);p=b.new_page(viewport={'width':1440,'height':1000});p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text) if m.type=='error' and '404' not in m.text else None)
  p.goto(f'http://localhost:{port}/index.html',timeout=120000);p.wait_for_function('window.__bofFrames>4');p.evaluate(shoot.TRAP_RAF)
  for stage in [1,4,6,8]:
   p.evaluate(shoot.SETUP,{'state':'PLAY','stage':stage,'pilot':'axel','invuln':True});p.wait_for_function('(n)=>{stageLoadTick();return stageLoadReady(n)&&XART.rdy(VP12_ART[n].key)&&XART.rdy(VP12_ART[n].rollKey)}',arg=stage,timeout=120000)
   p.evaluate('()=>{story=null;s6Opening=null;s6Wing=null;run._mission29OpeningDone=true;debugFight=null;waveIdx=999;spawnClock=9999;subBossTriggered=true;subBossDone=true;subBossActive=false;bossActive=false;warnT=0;if(wfx)wfx.fseq=null;stageTimer=1;VP12.next=9999;CP12.next=9999;run.shield=5;run.speedLevel=5;Input.keys={};}')
   for d in ['easy','normal','hard','furious']:
    n=p.evaluate('d=>{enemies=[];VP12.groups=[];diffKey=d;DIFF=DIFFS[d];vp12Spawn("orbit");return VP12.groups[0]?.live}',d);assert n=={'easy':3,'normal':5,'hard':7,'furious':9}[d],(stage,d,n)
   for pattern in ['orbit','corner','barrel','south','spiral','kamikaze','mixed']:
    p.evaluate('type=>{enemies=[];eBullets=[];VP12.groups=[];VP12.events=[];vp12Spawn(type);for(const e of enemies)if(e._vp12)e.hp=e.maxhp=50000;}',pattern)
    peak=0
    for i in range(9):
     p.evaluate(shoot.STEP,30);p.wait_for_timeout(10);peak=max(peak,p.evaluate('eBullets.filter(e=>e._vp12).length'))
     if i==2:p.screenshot(path=str(O/f's{stage}-{pattern}.png'))
    q=p.evaluate('()=>({stage:run.stage,events:VP12.events,live:enemies.filter(e=>e._vp12&&!e.dead&&e._dyingT==null).length,finite:enemies.filter(e=>e._vp12).every(e=>Number.isFinite(e.x)&&Number.isFinite(e.y)),state})');assert q['finite'] and q['state']=='play';assert q['live']>0 or pattern in ['barrel','kamikaze'],q;q['pattern']=pattern;q['peakShots']=peak;result.append(q);print(stage,pattern,peak,flush=True)
   p.evaluate('()=>{enemies=[];VP12.groups=[];vp12Spawn("corner");warnT=1;}');p.evaluate(shoot.STEP,3);assert p.evaluate('enemies.filter(e=>e._vp12&&!e.dead).length')==0
  b.close()
finally:stop()
(O/'verification.json').write_text(json.dumps({'results':result,'errors':errors},indent=2));assert not errors,errors;print('PASS',len(result),'patterns; four difficulty counts each stage; transition cleanup')
