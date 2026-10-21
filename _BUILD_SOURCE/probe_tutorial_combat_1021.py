"""Native tutorial release timing, mode pressure, correct portraits and credits."""
from pathlib import Path
import sys,json,http.server
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'_BUILD_SOURCE'))
import shoot,probe_tutorial_1015 as old
O=R/'_shots/tutorial_combat_1021';O.mkdir(parents=True,exist_ok=True)
checks=[];errors=[];modes=[]
def ck(name,ok,data=None):
 checks.append(dict(name=name,passed=bool(ok),data=data));print(('PASS ' if ok else 'FAIL ')+name,flush=True)
http.server.ThreadingHTTPServer.request_queue_size=128
port,stop=shoot.serve(str(R))
try:
 with sync_playwright() as pw:
  b=pw.chromium.launch(channel='msedge',args=['--mute-audio','--autoplay-policy=no-user-gesture-required'])
  p=b.new_page(viewport=dict(width=1366,height=768));p.set_default_timeout(120000)
  p.on('pageerror',lambda e:errors.append(str(e)))
  p.on('console',lambda m:errors.append(m.text[:600]) if m.type=='error' or 'draw error' in m.text else None)
  p.on('response',lambda r:errors.append(str(r.status)+' '+r.url.split('?')[0]) if r.status>=400 else None)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>4&&ASSETS.ready')
  p.evaluate(shoot.TRAP_RAF);p.evaluate(old.SETUP,dict(pilot='cole',mode='arcade',clear=True))
  p.evaluate('startRun(1)');p.evaluate(old.STEPN,30);p.evaluate('Input.injectTap("j")');p.evaluate(old.STEPN,5)
  p.wait_for_function('BOFINSTRUCTOR.artReady')
  p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(1)}')
  for i in range(40):
   m=p.evaluate(old.STEPN,30)
   if m['state']=='play' and m['lesson']:break
   p.wait_for_timeout(20)
  p.evaluate('''()=>{for(const B of Object.values(AF21_ART.models.s1jetdelta.banks))XART.rdy(B.key);}''')
  p.wait_for_function('Object.values(AF21_ART.models.s1jetdelta.banks).every(B=>XART.rdy(B.key))')
  p.evaluate('''()=>{window.tc21={shots:[],flashes:[],badAnim:[],draws:[]};
   const shoot=tutShoot,emit=wm26Emit,get=XART.get,draw=ctx.drawImage,tags=new WeakMap();
   tutShoot=function(x,y,a,s){const first=eBullets.length,r=shoot.apply(this,arguments),newborn=eBullets.slice(first);
    tc21.shots.push({t:TUT?.t,x,y,n:newborn.length,speeds:newborn.map(b=>Math.hypot(b.vx,b.vy)),tagged:newborn.every(b=>b._tut)});return r;};
   wm26Emit=function(owner,x,y,a,f,c,o){const r=emit.apply(this,arguments);
    if(owner?._ic21Escort&&!o?.fallback)tc21.flashes.push({t:TUT.t,x,y,owner:owner.type});return r;};
   XART.get=function(k){const im=get.apply(this,arguments);if(im)tags.set(im,k);return im;};
   ctx.drawImage=function(im){const k=tags.get(im);if(k)tc21.draws.push(k);return draw.apply(this,arguments);};
   window.tc21Step=n=>{for(let i=0;i<n;i++){
    tc21.draws=[];window.__now+=1000/60;loop(window.__now);
    for(const e of enemies)if(e._tut&&e._af21Rendered?.kind==='attack'&&efxClock-(e._af21FireAt??-999)>.401)tc21.badAnim.push(e.type);
   }};
   window.tc21Lesson=id=>{TUT.i=TUT_LESSONS.findIndex(d=>d.id===id)-1;tutNext();TUT.typed=10000;Input.clearTaps();};
  }''')
  p.evaluate('tc21Lesson("fire");tc21.shots=[];tc21Step(600)')
  quiet=p.evaluate('({shots:tc21.shots.length,phantom:enemies.filter(e=>e._tut&&e._af21Rendered?.kind==="attack").length,bad:tc21.badAnim})')
  ck('Non-firing lesson jets never mime native shooting or emit hidden rounds',quiet['shots']==0 and quiet['phantom']==0 and not quiet['bad'],quiet)
  for mode in ['normal','hard','furious']:
   p.evaluate('''mode=>{diffKey=mode;DIFF=difficultyForRun('arcade',mode);tc21Lesson('exam');tc21.shots=[];tc21.flashes=[];tc21.badAnim=[];window.tc21Start=TUT.t;}''',mode)
   jets=p.evaluate('TUT.L.units.length')
   for i in range(20):
    p.evaluate('tc21Step(30)');p.wait_for_timeout(10)
    if i==3:p.screenshot(path=str(O/(mode+'-escorts.png')))
   escort=p.evaluate('''()=>({jets:TUT.L.units.length,shots:tc21.shots,flashes:tc21.flashes,bad:tc21.badAnim,start:tc21Start,
    releases:TUT.L.units.map(e=>e._ic21Escort.releases),errors:window.__perr||null})''')
   ck(mode+' every escort fires promptly through its own controller',all(n>0 for n in escort['releases']) and 0<escort['shots'][0]['t']-escort['start']<2 and not escort['errors'],escort)
   ck(mode+' every visible barrel flash has a simultaneous real tagged bullet',len(escort['shots'])==len(escort['flashes']) and all(s['n']==1 and s['tagged'] and any(abs(s['t']-f['t'])<.0001 and abs(s['x']-f['x'])<.01 and abs(s['y']-f['y'])<.01 for f in escort['flashes']) for s in escort['shots']) and not escort['bad'],dict(bullets=len(escort['shots']),flashes=len(escort['flashes']),bad=escort['bad']))
   p.evaluate('''()=>{tutClearField();TUT.L.wave=2;sg20ExamWave(TUT.L);tc21.shots=[];window.tc21Start=TUT.t;window.tc21Motion=[];window.tc21Strikes=new Set();window.tc21Split=false;}''')
   for i in range(40):
    p.evaluate('''()=>{tc21Step(30);const G=TUT.L.bob;tc21Motion.push(G.x);
     for(const q of groundTargetingFx)if(q.owner?._bob20)tc21Strikes.add(q);
     const c=Object.values(G.parts).map(e=>e.x-e._bob20.off.x);if(Math.max(...c)-Math.min(...c)>.01)tc21Split=true;}''')
    p.wait_for_timeout(10)
    if i==2:p.screenshot(path=str(O/(mode+'-bob.png')))
   bob=p.evaluate('''()=>({hp:Object.values(TUT.L.bob.parts).map(e=>e.maxhp),rounds:tc21.shots.reduce((s,q)=>s+q.n,0),
    first:tc21.shots[0]?.t-tc21Start,speed:tc21.shots[0]?.speeds[0],strikes:tc21Strikes.size,
    travel:Math.max(...tc21Motion)-Math.min(...tc21Motion),split:tc21Split,
    portrait:UI20.dialogue?.portrait,draws:tc21.draws.filter(k=>k.startsWith('bob20_')),errors:window.__perr||null})''')
   ck(mode+' B.O.B. moves, fires promptly and operates both pods independently',bob['first']<2.5 and bob['rounds']>60 and bob['strikes']>=3 and bob['travel']>60 and not bob['split'] and not bob['errors'],bob)
   ck(mode+' B.O.B. retains actual modular art and green Cole instructor',set(['bob20_missile','bob20_cannon','bob20_core']).issubset(bob['draws']) and bob['portrait'].startswith('comm_cole_'),bob)
   p.evaluate('''()=>{killEnemy(TUT.L.bob.parts.missile);killEnemy(TUT.L.bob.parts.cannon);tc21.shots=[];}''')
   for i in range(6):p.evaluate('tc21Step(30)');p.wait_for_timeout(10)
   core=p.evaluate('({rounds:tc21.shots.reduce((s,q)=>s+q.n,0),active:TUT.L.bob.cycle?.type,draws:tc21.draws.filter(k=>k.startsWith("bob20_"))})')
   ck(mode+' exposed reactor immediately keeps attacking after pods are destroyed',core['rounds']>=20 and core['draws']==['bob20_core'],core)
   modes.append(dict(mode=mode,jets=jets,escortShots=len(escort['shots']),**bob))
  ck('Normal, Hard and Furious increase pressure, speed and module health',all(modes[i+1]['rounds']>modes[i]['rounds'] and modes[i+1]['speed']>modes[i]['speed'] and sum(modes[i+1]['hp'])>sum(modes[i]['hp']) and modes[i+1]['first']<modes[i]['first'] and modes[i+1]['escortShots']>modes[i]['escortShots'] for i in range(2)),modes)
  driver=old.DRIVER.replace('K.j = true;',"""K.j=true;
    if(id==='exam'&&L.wave===3){const e=['missile','cannon','core'].map(k=>L.bob.parts[k]).find(e=>e&&!e.dead&&e.hp>0);if(e)steer(e.x,low);else stop();return;}
  """)
  for mode in ['hard','furious']:
   p.evaluate('''mode=>{diffKey=mode;DIFF=difficultyForRun('arcade',mode);run.weapon=0;run.wlevel=1;run.infusion=null;tc21Lesson('exam');window.tc21WinStart=TUT.t;window.tc21HitStart=TUT.hits;}''',mode)
   p.evaluate(driver)
   for batch in range(120):
    m=p.evaluate(old.STEPN,60);p.wait_for_timeout(10)
    if m['lesson']!='exam' or m['done']>0:break
   result=p.evaluate('({lesson:TUT.L.def.id,done:TUT.done,seconds:TUT.t-tc21WinStart,hits:TUT.hits-tc21HitStart,dead:player.dead})')
   ck(mode+' graduation clears with the actual starter gun and native aiming controls',result['lesson']!='exam' or result['done']>0,result)
   p.evaluate('window.TD=null;for(const k of Object.keys(Input.keys))Input.keys[k]=false;Input.clearTaps();')
  for width,height in [(1366,768),(390,844)]:
   p.set_viewport_size(dict(width=width,height=height));p.evaluate('__bofFit();tc21Step(2)')
   p.screenshot(path=str(O/('green-cole-'+str(width)+'.png')))
   p.evaluate('tutFinish(false);Input.clearTaps();setState(GS.CREDITS);')
   p.wait_for_function('XART.rdy("ic20_neutral")')
   p.evaluate('tc21.draws=[];ctx.setTransform(SS,0,0,SS,0,0);drawCredits(0)')
   ck(str(width)+' credits use the red/black author portrait',p.evaluate('tc21.draws.includes("ic20_neutral")&&!tc21.draws.some(k=>k.startsWith("comm_cole_"))'))
   ck(str(width)+' credits text stays within its authored apertures',p.evaluate('IC20.creditsLayout.every(r=>r.layout.height<=r.h+.1&&r.layout.lines.every(s=>msgMeasure(s,r.layout.H)<=r.w+.1))'))
   p.screenshot(path=str(O/('credits-'+str(width)+'.png')))
  p.keyboard.press('k');p.evaluate(old.STEPN,2)
  ck('Credits retain the native Back control',p.evaluate('state===GS.TITLE'))
  ck('No page, console, asset or draw errors',not errors and not p.evaluate('window.__perr'),errors)
  b.close()
finally:stop()
q=dict(passed=sum(c['passed'] for c in checks),failed=sum(not c['passed'] for c in checks),checks=checks,modes=modes,errors=errors)
(O/'native-report.json').write_text(json.dumps(q,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:v for k,v in q.items() if k not in ['checks','modes']}));sys.exit(bool(q['failed']))
