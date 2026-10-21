from pathlib import Path
from PIL import Image
import io
import sys,json,base64,time,http.server
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'_BUILD_SOURCE'))
import shoot,probe_tutorial_1015 as old
O=R/'_shots/stormglass_1020';O.mkdir(exist_ok=True)
checks=[];errors=[]
def ck(name,passed,data=None):
 checks.append(dict(name=name,passed=bool(passed),data=data));print(('PASS ' if passed else 'FAIL ')+name,flush=True)
def shot(p,name):
 (O/(name+'.png')).write_bytes(base64.b64decode(p.evaluate('cv.toDataURL().split(",")[1]')))
def step(p,n=30):return p.evaluate(old.STEPN,n)
def until(p,pred,limit=2000):
 for i in range(0,limit,30):
  m=step(p)
  if pred(m):return m
  if i%300==0:p.wait_for_timeout(20)
 return m
driver=old.DRIVER.replace('K.j = true;', '''K.j = true;K.y=false;
    if(id==='multi'){stop();K.j=false;K.y=true;
      if((player._retinaScan?.marks||[]).filter(m=>m.phase==='locked').length>=2&&age%20===0)tap('k');return;}
''')
http.server.ThreadingHTTPServer.request_queue_size=128
port,stop=shoot.serve(str(R))
try:
 with sync_playwright() as pw:
  b=pw.chromium.launch(channel='msedge');p=b.new_page(viewport=dict(width=1366,height=768));p.set_default_timeout(120000)
  p.route('**/favicon.ico',lambda r:r.fulfill(status=204,body=''))
  p.on('pageerror',lambda e:errors.append(str(e)))
  p.on('console',lambda m:errors.append(m.text[:600]) if m.type=='error' else None)
  p.on('response',lambda r:errors.append(str(r.status)+' '+r.url) if r.status>=400 else None)
  p.on('requestfailed',lambda r:print('REQUEST FAILED '+r.url+' '+str(r.failure),flush=True))
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>4&&typeof ht27Stop==="function"');p.evaluate(shoot.TRAP_RAF)
  p.evaluate(old.SETUP,dict(pilot='cole',mode='arcade',clear=True));p.evaluate('startRun(1)');step(p,60)
  ck('Fresh pilot is offered the new academy',p.evaluate('state===GS.TUTASK&&tutAskRows()[0].includes("STORMGLASS")&&tutAsk.sel===0'))
  p.evaluate('Input.injectTap("j")');step(p,5);p.wait_for_function('BOFSTORMGLASS.artReady')
  p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(1)}')
  m=until(p,lambda m:m['state']=='intro',900);step(p,60);shot(p,'01-intro')
  p.evaluate(driver);m=until(p,lambda m:m['state']=='play' and m['lesson']=='move',12000)
  ck('New tutorial bypasses the campaign runway and reaches its own course',m['state']=='play' and p.evaluate('worldWidth()===680&&!!BOFSTORMGLASS.live'),m)
  p.wait_for_function('()=>{UI20.warm();return UI20_KEYS.every(k=>XART.rdy(k))}')
  seen={};start=time.monotonic();frames=0;foreign=0;minlives=initialLives=p.evaluate('run.lives');paused=False
  while frames<60*60*7:
   m=step(p,30);frames+=30;foreign=max(foreign,m['foreign']);minlives=min(minlives,m['lives'])
   if frames%300==0:p.wait_for_timeout(20)
   lid=m['lesson']
   if lid and lid not in seen:seen[lid]=dict(start=frames,hits=m['hits']);print('LESSON '+lid,flush=True)
   if lid and frames-seen[lid]['start']>=90 and 'shot' not in seen[lid]:shot(p,'lesson-'+lid);seen[lid]['shot']=True
   if lid=='fire' and not paused:
    travel=p.evaluate('BOFSTORMGLASS.live.travel');p.evaluate('Input.injectTap("p")');step(p,65)
    before=p.evaluate('BOFSTORMGLASS.live.travel');step(p,90);after=p.evaluate('BOFSTORMGLASS.live.travel')
    ck('Pausing freezes tutorial travel and exposes skip',p.evaluate('state==="paused"&&PLAY_PAUSE_ROWS[2]==="SKIP TUTORIAL"') and before==after,[travel,before,after])
    p.evaluate('Input.injectTap("p")');step(p,65);paused=True
   if lid and m['done']>0:seen[lid]['done']=True
   if not m['tut']:break
  print('END STATE '+json.dumps(p.evaluate('({state,lesson:TUT?.L?.def.id,L:TUT?.L,err:window.__perr})'),default=str)[:9000],flush=True)
  print('ERRORS '+json.dumps(errors)[:4000],flush=True)
  ck('Every lesson completed with real controls, including multi-lock and three-wave exam',not m['tut'] and set(p.evaluate('BOFSTORMGLASS.lessons'))<=set(seen),seen)
  ck('No campaign enemies entered the training field',foreign==0,foreign)
  ck('Hits cannot spend lives',minlives==initialLives and not m['dead'],[initialLives,minlives])
  ck('Graduation stores only a tutorial report and restores normal Stage 1',p.evaluate('!TUT&&run.stage===1&&run.mode==="arcade"&&run.score===0&&PLAY_PAUSE_ROWS[2]==="RESTART LEVEL"&&!!tutStoreRead().stormglassDone'),m)
  ck('Terrain used the new authored artwork in native rendering',p.evaluate('SG20.draws>100'),p.evaluate('SG20.draws'))
  # Controlled snapshots assess hit feedback and the announced, one-shooter ace pattern.
  p.evaluate('setState(GS.TITLE)');p.evaluate(old.SETUP,dict(pilot='cole',mode='campaign',clear=True));p.evaluate('startRun(1)');step(p,40);p.evaluate('Input.injectTap("j")');step(p,5)
  p.wait_for_function('BOFSTORMGLASS.artReady');until(p,lambda m:m['state']=='play' and m['tut'],3000)
  p.evaluate('TD=null;TUT.i=TUT_LESSONS.findIndex(l=>l.id==="exam")-1;tutNext();TUT.L.units.forEach(e=>e.dead=true);sg20ExamWave(TUT.L);TUT.L.units.forEach(e=>e.dead=true);sg20ExamWave(TUT.L)')
  p.evaluate('()=>{for(const k of Object.keys(Input.keys))Input.keys[k]=false;TUT.typed=10000;}')
  for n in ['bmfx_fov_green_tall','bmfx_fov_yellow_tall','bmfx_fov_red_tall']:p.wait_for_function('k=>XART.rdy(k)',arg=n)
  until(p,lambda m:p.evaluate('TUT.L.c?.t>1.4'),300);shot(p,'ace-yellow');p.screenshot(path=str(O/'native-desktop.png'))
  ck('Ace warning has a full three-second readable commitment window',p.evaluate('TUT.L.c.t<3&&TUT.L.c.t>1&&tutAlive(TUT.L.units).length===1'))
  # Pixel comparisons on native drawEnemy, with no screenshot approximation.
  fb=p.evaluate('''()=>{const e=tutAlive(TUT.L.units)[0],paint=()=>{ctx.setTransform(SS,0,0,SS,0,0);ctx.clearRect(0,0,VW,VH);ctx.save();ctx.translate(-camX,0);drawEnemy(e);ctx.restore();return Array.from(ctx.getImageData(0,0,cv.width,cv.height).data);};e.flash=0;const a=paint();markHit(e);const b=paint();e.flash=0;const c=paint();let changed=0,restored=0;for(let i=0;i<a.length;i+=4){if(a[i]!==b[i]||a[i+1]!==b[i+1]||a[i+2]!==b[i+2])changed++;if(a[i]!==c[i]||a[i+1]!==c[i+1]||a[i+2]!==c[i+2])restored++;}return{changed,restored};}''')
  ck('Instructor visibly flashes on hit and restores its authored pixels',fb['changed']>20 and fb['restored']==0,fb)
  layers=p.evaluate('''()=>{const S=sg20State(),before={time:S.time,travel:S.travel,camX},paint=t=>{S.time=t;S.travel=600;ctx.setTransform(SS,0,0,SS,0,0);ctx.save();ctx.translate(-camX,0);sg20Terrain();ctx.restore();return Array.from(ctx.getImageData(Math.round((SG20.width/2-camX-25)*SS),Math.round(280*SS),Math.round(50*SS),Math.round(150*SS)).data);};const a=paint(0),f0=SG20.waterFrame,b=paint(.17),f1=SG20.waterFrame;let changed=0;for(let i=0;i<a.length;i+=4)if(a[i]!==b[i]||a[i+1]!==b[i+1]||a[i+2]!==b[i+2])changed++;const positions=[];for(const cx of [80,160]){camX=cx;S.time=4;const rows=[],draw=ctx.drawImage;ctx.drawImage=function(im,...args){rows.push({kind:im===XART.get(SG20_WATER.key)?'ocean':im===XART.get(SG20.key)?'academy':this.globalAlpha<.16?'farCloud':'nearCloud',x:args[args.length===8?4:0]+this.getTransform().e/SS});return draw.call(this,im,...args);};ctx.setTransform(SS,0,0,SS,0,0);ctx.save();ctx.translate(-camX,0);sg20Terrain();ctx.restore();ctx.drawImage=draw;positions.push(rows);}S.time=before.time;S.travel=before.travel;camX=before.camX;return{changed,f0,f1,layers:SG20.layers,offsets:['ocean','farCloud','academy','nearCloud'].map(kind=>({kind,dx:positions[1].find(q=>q.kind===kind)?.x-positions[0].find(q=>q.kind===kind)?.x}))};}''')
  ck('Ocean genuinely animates while academy scroll is held fixed',layers['changed']>100 and layers['f0']!=layers['f1'],layers)
  expected={'ocean':-19.2,'farCloud':-28.8,'academy':-80,'nearCloud':-65.6}
  ck('All four authored parallax layers respond independently to camera movement',all(abs(q['dx']-expected[q['kind']])<2 for q in layers['offsets']),layers['offsets'])
  ck('Each parallax layer has its own travel speed',len(set(layers['layers'].values()))==4,layers['layers'])
  p.evaluate('()=>{ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);tutOverlayDraw();}')
  shot(p,'layered-course')
  p.keyboard.press('Shift');p.evaluate('Snd.prepare(["enemyMachineGunLight"])')
  p.wait_for_function('()=>Snd.pools.enemyMachineGunLight.slots.some(v=>v?.attached&&v.el.readyState>=3)',timeout=15000)
  cue=p.evaluate('''()=>{const events=[],play=Snd.play;Snd.play=function(name,...a){events.push(name);return play.call(this,name,...a);};tutShoot(340,220,Math.PI/2,3);Snd.play=play;return{events,decoded:Snd.pools.enemyMachineGunLight.slots.some(v=>v?.attached&&v.el.readyState>=3)};}''')
  ck('Training fire requests a decoded native machine-gun cue through the mixer',cue['decoded'] and 'enemyMachineGunLight' in cue['events'],cue)
  frames=[]
  for i in range(48):
   step(p,5)
   frames.append(Image.open(io.BytesIO(base64.b64decode(p.evaluate('cv.toDataURL().split(",")[1]')))).convert('RGB'))
  frames[0].save(O/'stormglass-live.gif',save_all=True,append_images=frames[1:],duration=83,loop=0,optimize=True)
  for difficulty in ['easy','normal','hard','furious']:
   out=p.evaluate('''key=>{diffKey=key;DIFF=difficultyForRun('arcade',key);eBullets=[];tutShoot(300,220,Math.PI/2,3);return{speed:Math.hypot(eBullets[0].vx,eBullets[0].vy),hp:tutSpawn('s1jetDelta',200,220,35).hp};}''',difficulty)
   ck(difficulty+' keeps beginner training armor and projectile speed',abs(out['speed']-3)<.0001 and out['hp']==35,out)
  p.evaluate('()=>{enemies=enemies.filter(e=>e._tut);eBullets=[];Input.injectTap("p");}');step(p,70)
  p.evaluate('()=>{playPauseChoose(2);}');step(p,5)
  ck('Skip restores Campaign and removes all academy state',p.evaluate('!TUT&&run.mode==="campaign"&&PLAY_PAUSE_ROWS[2]==="RESTART LEVEL"&&worldWidth()===SG20.base.width()'),p.evaluate('state'))
  p.evaluate(old.SETUP,dict(pilot='lizzie',mode='arcade',clear=True));p.evaluate('()=>{coopOn=true;p2Index=0;setState(GS.COOPROSTER);startRun(1);}');step(p,40);p.evaluate('Input.injectTap("j")');step(p,5)
  until(p,lambda m:m['state']=='play',3000)
  ck('Co-op tutorial is safely solo',p.evaluate('!!TUT&&!coopOn'))
  p.set_viewport_size(dict(width=390,height=844));p.evaluate('__bofFit()');step(p,120);shot(p,'native-narrow');p.screenshot(path=str(O/'phone-layout.png'))
  p.evaluate('tutFinish(false)');step(p,5);ck('Co-op restored on exit',p.evaluate('!TUT&&coopOn&&coopActive()'))
  ck('No native page, console or asset errors',not errors,errors)
  b.close()
finally:stop()
report=dict(passed=sum(c['passed'] for c in checks),total=len(checks),errors=errors,checks=checks)
(O/'report.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print(json.dumps({k:v for k,v in report.items() if k!='checks'}));raise SystemExit(not all(c['passed'] for c in checks))
