from pathlib import Path
import sys,json,base64,time,http.server
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'_BUILD_SOURCE'))
import shoot,probe_tutorial_1015 as old
O=R/'_shots/instructor_bob_1020';O.mkdir(exist_ok=True)
checks=[];errors=[]
def ck(name,p,data=None):
 checks.append(dict(name=name,passed=bool(p),data=data));print(('PASS ' if p else 'FAIL ')+name,flush=True)
def shot(p,n):(O/(n+'.png')).write_bytes(base64.b64decode(p.evaluate('cv.toDataURL().split(",")[1]')))
def step(p,n=30):return p.evaluate(old.STEPN,n)
def until(p,pred,limit=5000):
 for i in range(0,limit,30):
  m=step(p)
  if pred(m):return m
  if i%300==0:p.wait_for_timeout(30)
 return m
driver=old.DRIVER.replace('K.j = true;', '''K.j=true;K.y=false;
    if(id==='bob_card'){stop();K.j=false;if(age<250&&age%45===0)tap('s');if(age>270&&age%30===0)tap('j');return;}
    if(id.startsWith('elements_')){const e=L.bob.parts.core;steer(e.x,low);return;}
    if(id==='multi'){stop();K.j=false;K.y=true;if((player._retinaScan?.marks||[]).filter(m=>m.phase==='locked').length>=2&&age%20===0)tap('k');return;}
    if(id==='exam'&&L.wave===3){const G=L.bob,e=['missile','cannon','core'].map(k=>G.parts[k]).find(e=>e&&!e.dead&&e.hp>0);if(e)steer(e.x,low);else stop();return;}
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
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>4&&typeof ht27Stop==="function"');p.evaluate(shoot.TRAP_RAF)
  p.evaluate(old.SETUP,dict(pilot='cole',mode='arcade',clear=True));p.evaluate('startRun(1)');step(p,60)
  p.wait_for_function('XART.rdy("ic20_neutral")');step(p,30);shot(p,'01-instructor-invitation')
  ck('Tutorial invite uses framed Instructor Cole',p.evaluate('state===GS.TUTASK&&!!XART.get("ic20_neutral")'))
  p.evaluate('Input.injectTap("j")');step(p,5);p.wait_for_function('BOFINSTRUCTOR.artReady');p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(1)}')
  m=until(p,lambda m:m['state']=='play' and m['lesson']=='move',12000);p.evaluate(driver)
  seen={};foreign=0;lives=p.evaluate('run.lives');minlives=lives;hits=[]
  for frames in range(0,60*60*8,30):
   m=step(p);foreign=max(foreign,m['foreign']);minlives=min(minlives,m['lives']);lid=m['lesson']
   if lid and lid not in seen:seen[lid]={'start':frames};print('LESSON '+lid,flush=True)
   if lid and frames-seen[lid]['start']>=150 and 'shot' not in seen[lid]:shot(p,'lesson-'+lid);seen[lid]['shot']=True
   if lid=='exam' and p.evaluate('TUT.L.wave===3') and not seen[lid].get('bob'):
    shot(p,'bob-live');seen[lid]['bob']=True
   if lid and m['done']>0:seen[lid]['done']=True
   if frames%300==0:p.wait_for_timeout(30)
   if not m['tut']:break
  print('END '+json.dumps(m),flush=True)
  ck('Entire course completed with real input',not m['tut'] and len(seen)==len(p.evaluate('BOFTUTORIAL.lessons')),seen)
  ck('Academy excludes campaign spawns and protects lives',foreign==0 and minlives==lives,[foreign,minlives,lives])
  ck('Completion restores normal arcade start',p.evaluate('!TUT&&run.stage===1&&run.mode==="arcade"&&run.score===0&&PLAY_PAUSE_ROWS[2]==="RESTART LEVEL"'))
  ck('Both elemental labs recorded resistance and counter hits',p.evaluate('Object.keys(IC20.labStats||{}).length===4&&["elements_ice:0","elements_fire:1"].every(k=>IC20.labStats[k].elements.ice>=3)&&["elements_fire:0","elements_ice:1"].every(k=>IC20.labStats[k].elements.fire>=3)'),p.evaluate('IC20.labStats'))
  # Fresh controlled fixtures use real native hit/target/render owners for every mode.
  p.evaluate('TD=null;setState(GS.TITLE)');p.evaluate(old.SETUP,dict(pilot='cole',mode='campaign',clear=True));p.evaluate('startRun(1)');step(p,40);p.evaluate('Input.injectTap("j")');step(p,5)
  p.wait_for_function('BOFINSTRUCTOR.artReady');until(p,lambda m:m['state']=='play',5000)
  p.evaluate('()=>{TD=null;for(const k of Object.keys(Input.keys))Input.keys[k]=false;TUT.i=TUT_LESSONS.findIndex(d=>d.id==="exam")-1;tutNext();TUT.L.wave=2;sg20ExamWave(TUT.L);TUT.typed=10000;}')
  for difficulty in ['easy','normal','hard','furious']:
   out=p.evaluate('''key=>{diffKey=key;DIFF=difficultyForRun('arcade',key);tutClearField();TUT.L.wave=2;sg20ExamWave(TUT.L);const G=TUT.L.bob,core=G.parts.core;_dmgBullet={kind:'mg'};_dmgSrc=null;const h=core.hp;hitEnemy(core,10);const protectedHp=core.hp;killEnemy(G.parts.missile);killEnemy(G.parts.cannon);_dmgBullet={kind:'mg',_inf:'fire'};hitEnemy(core,10);const fire=h-core.hp;_dmgBullet={kind:'mg',_inf:'ice'};const a=core.hp;hitEnemy(core,10);const ice=a-core.hp;_dmgBullet={kind:'missile'};_dmgSrc='missile';const c=core.hp;hitEnemy(core,10);const missile=c-core.hp;_dmgBullet=null;_dmgSrc=null;return{protectedHp,h,fire,ice,missile,hps:Object.values(G.parts).map(e=>e.maxhp),flash:core.flash};}''',difficulty)
   ck(difficulty+' native shield, elements and reactor missile bonus',out['protectedHp']==out['h'] and out['fire']==15 and out['ice']==5 and out['missile']==20 and out['hps']==[90,110,240] and out['flash']>0,out)
   armor=p.evaluate('''()=>{tutClearField();TUT.L.wave=2;sg20ExamWave(TUT.L);for(let i=0;i<30;i++)updatePlay(1/60);const G=TUT.L.bob;return{hps:Object.values(G.parts).map(e=>e.maxhp),extra:eBullets.length};}''')
   ck(difficulty+' modules retain their published armor after native AI updates',armor['hps']==[90,110,240] and armor['extra']==0,armor)
  p.evaluate('()=>{tutClearField();TUT.L.wave=2;sg20ExamWave(TUT.L);TUT.say="";TUT.typed=10000;}')
  fb=p.evaluate('''()=>{const G=TUT.L.bob,paint=()=>{ctx.setTransform(SS,0,0,SS,0,0);ctx.clearRect(0,0,VW,VH);ctx.save();ctx.translate(-camX,0);Object.values(G.parts).forEach(drawEnemy);ctx.restore();return Array.from(ctx.getImageData(0,0,cv.width,cv.height).data);};return Object.values(G.parts).map(e=>{Object.values(G.parts).forEach(q=>q.flash=0);const a=paint();hitEnemy(e,1);const b=paint();e.flash=0;const c=paint();let changed=0,restored=0;for(let i=0;i<a.length;i+=4){if(a[i]!==b[i]||a[i+1]!==b[i+1]||a[i+2]!==b[i+2])changed++;if(a[i]!==c[i]||a[i+1]!==c[i+1]||a[i+2]!==c[i+2])restored++;}return{id:e._bob20.id,changed,restored};});}''')
  ck('Every authored module visibly flashes, including shield absorption, and restores',all(q['changed']>20 and q['restored']==0 for q in fb),fb)
  expiry=p.evaluate('''()=>{markHit(TUT.L.bob.parts.core,.16);for(let i=0;i<24;i++)updatePlay(1/60);return TUT.L.bob.parts.core.flash;}''')
  ck('Module hit flash expires on the native simulation clock',expiry<=0,expiry)
  cancel=p.evaluate('''()=>{const e=TUT.L.bob.parts.missile,q=bob20Ground(e);killEnemy(e);return{dead:q.dead,moduleDead:e.dead};}''')
  ck('Destroying launcher cancels its pending warning',cancel['dead'] and cancel['moduleDead'],cancel)
  for phase,t in [('green',.3),('yellow',1.5),('red',2.8)]:
   p.evaluate('''t=>{const L=TUT.L,G=L.bob;G.cycle={type:'lane',t,x:player.x,fired:0};TUT.say='';TUT.typed=10000;ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);tutOverlayDraw();}''',t);shot(p,'bob-fov-'+phase)
  p.evaluate('()=>{TUT.i=TUT_LESSONS.findIndex(d=>d.id==="bob_card")-1;tutNext();TUT.typed=10000;}');step(p,100);shot(p,'dossier-whole')
  p.evaluate('Input.injectTap("s")');step(p,2);shot(p,'dossier-missile')
  ck('Dossier selects actual authored part',p.evaluate('IC20.cardFrame.part==="missile"'),p.evaluate('IC20.cardFrame'))
  p.evaluate('Input.injectTap("k")');step(p,2);ck('Dossier Back returns to full unit',p.evaluate('TUT.L.sel===0'))
  frozen=p.evaluate('({x:player.x,y:player.y,ammo:run.bombs})');p.evaluate('Input.keys.a=true;Input.keys.j=true');step(p,40)
  ck('Dossier is combat-free and consumes no ammo',p.evaluate('player.x')==frozen['x'] and p.evaluate('run.bombs')==frozen['ammo'])
  p.evaluate('Input.keys.a=false;Input.keys.j=false;Input.injectTap("p")');step(p,50)
  ck('Dossier can pause and expose tutorial skip',p.evaluate('state==="paused"&&PLAY_PAUSE_ROWS[2]==="SKIP TUTORIAL"'))
  p.evaluate('Input.injectTap("p")');step(p,50)
  rotations=p.evaluate('''()=>{const L=TUT.L,all=[];for(let i=0;i<4;i++){L.sel=i;const a=IC20_ART.views[IC20_PARTS[i]],rows=[];for(const yaw of [0,8,16,24]){L.yaw=yaw;const calls=[],draw=ctx.drawImage;ctx.drawImage=function(im,...args){if(args.length===8&&args[2]===a.cell_width&&args[3]===a.cell_height)calls.push(args.slice(0,4));return draw.call(this,im,...args);};try{tutOverlayDraw();}finally{ctx.drawImage=draw;}rows.push({yaw,calls,frame:IC20.cardFrame.frame});}all.push({part:IC20_PARTS[i],frames:a.frames,rows});}return{all,pending:IC20_ART.pending_turntables};}''')
  ck('All four native turntables use distinct authored source rectangles',not rotations['pending'] and all(a['frames']==32 and len({json.dumps(q['calls']) for q in a['rows']})==4 for a in rotations['all']),rotations)
  p.evaluate('TUT.L.sel=0;TUT.L.yaw=0');step(p,1);shot(p,'dossier-whole-final')
  frames=[]
  from PIL import Image
  import io
  for i in range(32):
   p.evaluate('TUT.L.yaw='+str(i)+';ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);tutOverlayDraw();')
   frames.append(Image.open(io.BytesIO(base64.b64decode(p.evaluate('cv.toDataURL().split(",")[1]')))).convert('RGB'))
  frames[0].save(O/'dossier-live.gif',save_all=True,append_images=frames[1:],duration=100,loop=0,optimize=False)
  p.evaluate('Input.keys.a=false;Input.keys.j=false');p.set_viewport_size(dict(width=390,height=844));p.evaluate('__bofFit()');step(p,2);p.screenshot(path=str(O/'dossier-narrow.png'))
  loan=p.evaluate('''()=>{const old=JSON.stringify({w:run.weapon,l:run.wlevel,i:run.infusion});TUT.i=TUT_LESSONS.findIndex(d=>d.id==='elements_ice')-1;tutNext();const changed=!!TUT._icLoan;tutNext();tutNext();return{old,after:JSON.stringify({w:run.weapon,l:run.wlevel,i:run.infusion}),changed};}''')
  ck('Element loans restore equipped gun and infusion',loan['changed'] and loan['old']==loan['after'],loan)
  pilots=p.evaluate('''()=>{const out=[],original=run.pilot;for(const P of PILOTS){run.pilot=P.key;tutClearField();TUT.i=TUT_LESSONS.findIndex(d=>d.id==='elements_ice')-1;tutNext();pBullets=[];pShoot();const kinds=pBullets.map(b=>b.kind),infusable=pBullets.some(b=>infusionCarrier(b));out.push({pilot:P.key,kinds,infusable,primary:ui20Seat(1).primary,secondary:ui20Seat(1).secondary});ic20Return();}run.pilot=original;return out;}''')
  ck('All nine pilots can fire an infusable lab gun and retain their ability descriptions',len(pilots)==9 and all(q['infusable'] and q['primary'] and q['secondary'] for q in pilots),pilots)
  p.keyboard.press('Shift');p.evaluate('Snd.prepare(["enemyMachineGunLight","missileLaunch","expBig","shieldHitHeavy"])')
  p.wait_for_function('()=>["enemyMachineGunLight","missileLaunch","expBig","shieldHitHeavy"].every(k=>Snd.pools[k]?.slots.some(v=>v?.attached&&v.el.readyState>=3))',timeout=20000)
  cue=p.evaluate('''()=>{tutClearField();TUT.L.wave=2;sg20ExamWave(TUT.L);const G=TUT.L.bob,events=[],play=Snd.play;Snd.play=function(k,...a){events.push(k);return play.call(this,k,...a);};try{hitEnemy(G.parts.core,1);tutShoot(G.parts.cannon.x,G.parts.cannon.y,Math.PI/2,3);const q=bob20Ground(G.parts.missile);q.t=q.warn*.53;s6StrikeMissileTick(q);return{events,launch:{x:q._strikeMissile.x,y:q._strikeMissile.y},port:bob20Port(G.parts.missile)};}finally{Snd.play=play;}}''')
  ck('Shield, cannon and missile request decoded approved mixer cues at the actual port',all(k in cue['events'] for k in ['shieldHitHeavy','enemyMachineGunLight','missileLaunch']) and cue['launch']==cue['port'],cue)
  volumes=p.evaluate('''()=>Object.fromEntries(['shieldHitHeavy','enemyMachineGunLight','missileLaunch'].map(k=>[k,Math.max(...Snd.pools[k].slots.filter(v=>v?.attached&&v.el.readyState>=3).map(v=>v.el.volume))]))''')
  ck('Decoded attack voices have finite nonzero audible volume',all(isinstance(v,(int,float)) and v>0 for v in volumes.values()),volumes)
  p.evaluate('tutFinish(false)');step(p,5)
  ck('Skip restores campaign and clears training state',p.evaluate('!TUT&&run.mode==="campaign"&&PLAY_PAUSE_ROWS[2]==="RESTART LEVEL"'))
  ck('No browser, console or asset errors',not errors,errors)
  b.close()
finally:stop()
report=dict(passed=sum(c['passed'] for c in checks),total=len(checks),errors=errors,checks=checks)
(O/'report.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print(json.dumps({k:v for k,v in report.items() if k!='checks'}));raise SystemExit(not all(c['passed'] for c in checks))
