"""Input-driven quick tutorial, native drawing and campaign/skip handoffs."""
from pathlib import Path
import json,sys,http.server
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];O=R/'_shots/tutorial_showcase_1109';O.mkdir(exist_ok=True)
sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot,probe_tutorial_1015 as old
checks=[];errors=[];runs=[]
def ck(name,ok,data=None):checks.append(dict(name=name,passed=bool(ok),data=data));print('PASS'if ok else'FAIL',name,flush=True)
DRIVER=old.DRIVER.replace("if (id === 'warn') {", """if(id==='multi'){
      K.j=false;steer((camLeftX()+camRightX())/2,low);K.y=true;
      if((player._retinaScan?.marks||[]).filter(m=>m.phase==='locked').length>=2&&age%15===0)tap('k');return;
    }
    if (id === 'warn') {
      K.j=false;const q=L.strike;
      steer(q&&q.t>.9?camLeftX()+65:camRightX()-65,low);return;
    }
    if (id === 'old-warn') {""").replace("TD.lastLesson = T.i; TD.t0", "TD.lastLesson = T.i; K.y=false; TD.t0").replace("if (id === 'retina') {","if (id === 'retina') { K.j=false;")
TRACE=r'''()=>{window.TSQA={draws:{},bob:0,boss:0,foreign:0,unsafe:0,shots:[]};const get=XART.get,draw=ctx.drawImage,keys=new WeakMap();
 XART.get=function(k){const im=get.apply(this,arguments);if(im)keys.set(im,k);return im;};
 ctx.drawImage=function(im){const k=keys.get(im);if(k)TSQA.draws[k]=(TSQA.draws[k]||0)+1;return draw.apply(this,arguments);};
 const spawn=bob20Spawn;bob20Spawn=function(){TSQA.bob++;return spawn.apply(this,arguments);};
 const shot=tutShoot;tutShoot=function(x,y,a,s){const first=eBullets.length,r=shot.apply(this,arguments);
  if(TUT?.L?.def.id==='warn'){const e=TUT.L.gun,ports=[-1,1].map(s=>s1aPlaneMuzzle(e,s));
   TSQA.shots.push({mouth:Math.min(...ports.map(p=>Math.hypot(p.x-x,p.y-y))),heading:s1aPlaneHead(e),frame:e._air13Frame,rounds:eBullets.slice(first).map(b=>({vx:b.vx,vy:b.vy}))});}return r;};
 window.tsqaCheck=()=>{if(!tutLive())return;TSQA.boss+=!!(bossActive||subBossActive||boss||subBoss);TSQA.foreign=Math.max(TSQA.foreign,enemies.filter(e=>!e._tut&&!e.dead).length);
  for(const b of eBullets)if(b._tut&&enemyOrdnanceCanIntercept(b))TSQA.unsafe++;};}'''
http.server.ThreadingHTTPServer.request_queue_size=128
port,stop=shoot.serve(str(R))
try:
 with sync_playwright()as pw:
  b=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required'])
  def page(pilot='cole',mode='arcade',diff='normal'):
   p=b.new_page(viewport={'width':1280,'height':800});p.set_default_timeout(180000)
   p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:400])if m.type=='error'or'draw error'in m.text.lower()else None)
   p.goto(f'http://127.0.0.1:{port}/index.html?showcase=1109',wait_until='load',timeout=180000);p.wait_for_function('window.__bofFrames>4&&typeof TS109!=="undefined"');p.evaluate(shoot.TRAP_RAF);p.evaluate(old.SETUP,dict(pilot=pilot,mode=mode,clear=True));p.evaluate('d=>{diffKey=d;DIFF=difficultyForRun(run.mode,d);}',diff);return p
  def step(p,n):
   r=p.evaluate(old.STEPN,n);p.evaluate('window.tsqaCheck?.()');return r
  def enter(p):
   p.evaluate('startRun(1)');step(p,30);p.wait_for_function('Object.values(MW21_ART).every(a=>XART.rdy(a.key))');step(p,2);p.screenshot(path=str(O/'ask.png'))
   p.evaluate('Input.injectTap("j")');step(p,2);p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(1)&&sg20LayersReady();}')
   for _ in range(150):
    r=step(p,15);p.wait_for_timeout(10)
    if r['state']=='play'and r['lesson']:return r
   raise RuntimeError('Tutorial did not enter play '+str(r))
  for pilot,mode,diff in [('cole','arcade','normal'),('juggernaut','campaign','furious')]:
   p=page(pilot,mode,diff);p.evaluate(TRACE);r=enter(p);p.evaluate(DRIVER);initial=p.evaluate('({lives:run.lives,mode:TUT.mode,coop:TUT.coop})');seen=[];shots=set();last=r
   for batch in range(300):
    last=step(p,30);p.wait_for_timeout(8)
    if last['lesson']and last['lesson']not in seen:seen.append(last['lesson']);print('LESSON',pilot,last['lesson'],flush=True)
    if last['lesson']and last['lesson']not in shots and p.evaluate('TUT.lt')>1.1:
     shots.add(last['lesson']);p.screenshot(path=str(O/f'{pilot}-{last["lesson"]}.png'))
    if not last['tut']:break
   data=p.evaluate('({state,mode:run.mode,coop:coopOn,lives:run.lives,dead:player.dead,trace:TSQA,steps:TS109.completed,store:tutStoreRead(),pause:PLAY_PAUSE_ROWS[2]})');runs.append(dict(pilot=pilot,requestedMode=mode,difficulty=diff,seen=seen,**data))
   ck(pilot+' completes all nine mechanics through native inputs',len(seen)==9 and not last['tut'],dict(seen=seen,last=last,steps=data['steps']))
   ck(pilot+' tutorial is a short showcase without combat exams',sum(s['seconds']for s in data['steps'])<100 and len(data['steps'])==9,data['steps'])
   ck(pilot+' has no BOB, boss or unrelated waves',data['trace']['bob']==0 and data['trace']['boss']==0 and data['trace']['foreign']==0,data['trace'])
   drawn=data['trace']['draws'];ck(pilot+' draws animated water without academy or BOB art',drawn.get(SGKEY:='sgw20_ocean',0)>50 and not any(k.startswith('bob20_')or k=='sg20_stormglass'for k in drawn),dict(water=drawn.get(SGKEY),forbidden=[k for k in drawn if k.startswith('bob20_')or k=='sg20_stormglass']))
   ck(pilot+' warning rounds remain unshootable',data['trace']['unsafe']==0,data['trace']['unsafe'])
   shots=data['trace']['shots'];ck(pilot+' warning fire leaves actual south-facing twin gun mouths',len(shots)==6 and all(s['mouth']<.01 and abs(s['heading']-1.57079632679)<.01 and s['frame']==0 and len(s['rounds'])==1 and abs(s['rounds'][0]['vx'])<.01 and s['rounds'][0]['vy']>0 for s in shots),shots)
   ck(pilot+' restores requested mode and native pause/completion owners',not last['tut']and data['mode']==mode and data['coop']==initial['coop']and data['store'].get('done')and data['pause']=='RESTART LEVEL',dict(mode=data['mode'],state=data['state'],store=data['store']))
   ck(pilot+' protected practice never loses a life',data['lives']==initial['lives']and not data['dead'],dict(before=initial['lives'],after=data['lives']))
   p.close()
  for mode in ['arcade','campaign']:
   p=page(mode=mode);p.evaluate('startRun(1)');step(p,30);p.evaluate('Input.injectTap("arrowdown")');step(p,2);p.evaluate('Input.injectTap("j")');r=step(p,2)
   ck(mode+' can decline the tutorial',not r['tut']and not r['ask']and p.evaluate('run.mode')==mode,r);p.close()
  p=page();p.evaluate('coopOn=true;setState(GS.COOPROSTER)');enter(p);p.evaluate('Input.injectTap("p")');step(p,2);p.evaluate('playPauseChoose(2)');r=step(p,2)
  ck('Pause skip restores co-op and starts the requested run',not r['tut']and p.evaluate('coopOn&&run.mode==="arcade"&&PLAY_PAUSE_ROWS[2]==="RESTART LEVEL"'),r);p.close()
  p=page();enter(p);p.evaluate('TUT.i=TUT_LESSONS.findIndex(d=>d.id==="fire")-1;tutNext();window.pixelEnemy=TUT.L.units[0]');step(p,5);p.wait_for_function('XART.rdy(S1A_ART.delta_heading.key)')
  q=p.evaluate('''()=>{window.tsqaPixels=()=>{ctx.save();ctx.setTransform(1,0,0,1,0,0);ctx.clearRect(0,0,cv.width,cv.height);drawEnemy(pixelEnemy);ctx.restore();const d=ctx.getImageData(0,0,cv.width,cv.height).data;let white=0;for(let i=0;i<d.length;i+=4)if(d[i]>235&&d[i+1]>235&&d[i+2]>235)white++;return white;};const clean=tsqaPixels(),old=_dmgBullet;_dmgBullet={kind:'mg',x:pixelEnemy.x,y:pixelEnemy.y,lv:1};hitEnemy(pixelEnemy,.01);_dmgBullet=old;return {clean,hit:tsqaPixels()};}''');step(p,45);q.update(p.evaluate('({expired:tsqaPixels(),flash:pixelEnemy.flash})'));ck('Actual target pixels flash white on damage and expire',q['hit']>q['clean']+20 and q['expired']<q['hit']*.5 and q['flash']<=0,q)
  p.set_viewport_size({'width':390,'height':844});step(p,5);p.screenshot(path=str(O/'mobile.png'));ck('Mobile tutorial retains a compact 84px dialogue panel',p.evaluate('UI20.dialogue.h===84'));p.close()
  ck('No page or console errors',not errors,errors);b.close()
finally:stop()
(O/'checks.json').write_text(json.dumps(dict(checks=checks,runs=runs,errors=errors),indent=2));print('SUMMARY',sum(c['passed']for c in checks),'/',len(checks));sys.exit(0 if all(c['passed']for c in checks)else 1)
