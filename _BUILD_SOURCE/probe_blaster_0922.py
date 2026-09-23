import sys,json,base64
from pathlib import Path
sys.path.insert(0,str(Path('_BUILD_SOURCE').resolve()))
from shoot import GAME,serve,SETUP,STEP,TRAP_RAF
from playwright.sync_api import sync_playwright
O=Path('_shots/blaster_0922');O.mkdir(exist_ok=True);errors=[];r={};port,stop=serve(GAME)
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(args=['--no-sandbox','--mute-audio']);pg=br.new_page(viewport={'width':1440,'height':1000})
  pg.on('pageerror',lambda e:errors.append(str(e)));pg.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
  pg.goto(f'http://127.0.0.1:{port}/index.html');pg.wait_for_function('()=>(window.__bofFrames|0)>4');pg.evaluate(TRAP_RAF)
  def ev(s,a=None):return pg.evaluate(s,a)
  def step(n):
   while n>0:
    v=ev(STEP,min(n,60));assert not v,v;n-=60;pg.wait_for_timeout(30)
  def cap(n):
   step(1);(O/(n+'.png')).write_bytes(base64.b64decode(ev("()=>cv.toDataURL().split(',')[1]")))
  ev(SETUP,{'state':'PLAY','stage':5,'pilot':'cole','invuln':True})
  ev("()=>{diffKey='furious';DIFF=DIFFS.furious;stagePlan=[];waveIdx=999;_adaptiveSpawnT=999;spawnClock=9999;enemies=[];eBullets=[];pBullets=[];powerups=[];spawnBoss('chromehammer');boss.enter=false;boss._noHit=false;boss.x=worldWidth()/2;boss.y=175;boss._hammer.balance0922=true;boss._hammer.mode='chaingun';hammerState(boss,'chaingun_draw');}")
  pg.wait_for_function("()=>['body','gun','fx'].every(f=>Array.from({length:8},(_,i)=>XART.rdy('arch_blaster_'+f+'_'+i)).every(Boolean))")
  for t,n in [(.15,'transform_start'),(.8,'transform_expand'),(1.85,'assembled')]:
   ev('(t)=>{boss._hammer.state="chaingun_draw";boss._hammer.t=t;}',t);cap(n)
  r['south']=ev("()=>{boss._hammer.state='chaingun';boss._hammer.t=0;boss._hammer.chainHeat=.3;player.x=camLeftX()+30;eBullets=[];let m=hammerBlasterMount(boss);hammerBossChaingunFire(boss);return {n:eBullets.length,vertical:eBullets.every(q=>q.vx===0&&q.vy>0&&q._archBlaster),muzzle:eBullets.every(q=>Math.abs(q.y-m.muzzleY)<.01)};}")
  cap('firing');step(100);cap('sweep_fire')
  r['heat']=ev("()=>{let h=boss._hammer;h.chainHeat=.99;hammerBossChaingunFire(boss);return {state:h.state,heat:h.chainHeat};}")
  cap('overheat');step(40);cap('steam')
  r['cool']=ev("()=>{let h=boss._hammer;h.state='chain_cool';h.t=2.31;diffKey='normal';hammerBossTick(boss,.01);return {state:h.state,heat:h.chainHeat};}")
  r['noGhostHammer']=ev("()=>{bossHitTest(boss.x-48,boss.y+18);return boss._hammerModuleHit!=='hammer';}")
  r['module']=ev("()=>{let h=boss._hammer;h.state='chaingun';let before=boss.hp;let m=hammerBlasterMount(boss);let hit=bossHitTest(m.x,m.muzzleY-20);let damage=hammerBossDamage(boss,10);return {hit,weapon:h.chainHP<h.chainMax,hull:boss.hp===before,damage};}")
  ev("()=>{boss._hammer.chainHP=1;diffKey='furious';const m=hammerBlasterMount(boss);bossHitTest(m.x,m.muzzleY-20);hammerBossDamage(boss,10);}");cap('destroyed')
  r['destroy']=ev("()=>{eBullets=[];hammerBossChaingunFire(boss);return {destroyed:boss._hammer.chainDestroyed,state:boss._hammer.state,shots:eBullets.length};}")
  r['errors']=errors;br.close()
finally:stop()
(O/'results.json').write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2))
assert not errors
assert r['noGhostHammer']
assert r['south']=={'n':2,'vertical':True,'muzzle':True}
assert r['heat']['state']=='chain_cool' and r['heat']['heat']==1
assert r['cool']=={'state':'chaingun','heat':0}
assert r['module']=={'hit':True,'weapon':True,'hull':True,'damage':0}
assert r['destroy']=={'destroyed':True,'state':'enrage','shots':0}
