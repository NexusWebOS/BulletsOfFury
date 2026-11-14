from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image
import sys,json,hashlib,numpy as np
W=Path(__file__).resolve().parent;R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');O=W.parents[1]/'outputs/Stage5-bomber-assault';O.mkdir(exist_ok=True);sys.path.insert(0,str(R/'_BUILD_SOURCE'))
from shoot import serve,STEP
from barrage_review_common_1025 import boot
errors=[];checks=[];port,stop=serve(str(R));traces={}
def ck(name,ok,data=None):
 checks.append(dict(name=name,passed=bool(ok),data=data));(O/'checks.json').write_text(json.dumps(dict(checks=checks,errors=errors),indent=2));print(('PASS 'if ok else'FAIL ')+name, str(data)[:400]if not ok else'',flush=True)
def shot(p,name):p.evaluate('()=>{drawWorld(0);SC12.refresh();__bofFit()}');p.screenshot(path=str(O/(name+'.png')))
setup="""d=>{diffKey=d;run.ngplus=false;spawnSubBoss('siegebomber');subBossActive=true;subBossDone=false;window.B=subBoss;B.enter=false;B.y=B.ty;B.x=worldWidth()/2;B._bomber.mode='recover';s5b14Init(B);window.M=B._s5b14;S5B14.events=[];boss=null;bossActive=false;enemies=[];l5Rocks=[];eBullets=[];pBullets=[];groundTargetingFx=[];player.dead=player.out=false;player.invuln=1e9;player.x=worldWidth()/2;player.y=VH-65;for(const k of Object.keys(Input.keys))Input.keys[k]=false;Input.mouse.active=false;setState(GS.PLAY);}"""
try:
 with sync_playwright()as pw:
  br=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required','--js-flags=--expose-gc']);ctxb=br.new_context(viewport={'width':1280,'height':800});p=boot(ctxb,port,5,errors,'mini');p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(5)&&s5b14Warm()}',timeout=180000)
  (W/'setup.js').write_text(setup)
  for diff in ['easy','normal','hard','furious']:
   p.evaluate(setup,diff);initial=p.evaluate('({hp:B.hp,max:B.maxhp,pool:B._bomber.core+B._bomber.parts.reduce((n,q)=>n+q.hp,0),parts:B._bomber.parts.map(q=>[q.id,q.hp])})');rows=[];saved=set();done=False
   for batch in range(160):
    q=p.evaluate("""()=>{for(let i=0;i<45;i++)updatePlay(1/60);return{phase:M.phase,t:M.t,cycle:M.cycle,depth:M.depth,head:M.head,air:M.air,fore:M.fore,hp:B.hp,pool:B._bomber.core+B._bomber.parts.reduce((n,q)=>n+Math.max(0,q.hp),0),rounds:s5b14Owned(B),bombs:groundTargetingFx.filter(q=>q._s5b14Owner===B&&!q.dead).length,locked:M.locked,target:M.target,serial:M.serial,events:S5B14.events.length};}""");rows.append(q)
    if diff=='furious'and q['phase']not in saved and(q['phase']!='lock'or q['locked']):shot(p,'furious-'+q['phase']);saved.add(q['phase'])
    if q['cycle']>=2:done=True;break
    if batch%8==0:p.wait_for_timeout(1);p.evaluate('()=>{if(window.gc)window.gc()}')
   events=p.evaluate('S5B14.events');phases=list(dict.fromkeys(e['to']for e in events if e['event']=='phase'));traces[diff]=dict(rows=rows,events=events,initial=initial)
   ck(diff+': complete burst/cool/burst, retreat/turn/bomb charge/overflight/return/catch-up loops',done and all(s in phases for s in ['lock','burst','cool','spool','boost','turn-in','charge','pass','turnback','return','catch','stalk']),phases)
   ck(diff+': original full module/core health stays unchanged through two flight cycles',all(abs(q['hp']-initial['hp'])<.01 and abs(q['pool']-initial['pool'])<.01 for q in rows),initial)
   laser=[e for e in events if e['event']=='laser-round'];drops=[e for e in events if e['event']=='bomb-drop'and e['raid']];cool=[e for e in events if e['event']=='cannons-cooling']
   ck(diff+': real cannon bursts and repeated cooling alternate with a dense warned bombing run',len(laser)>=32 and len(drops)>=(8 if diff=='easy'else 24)and len(cool)>=4,dict(lasers=len(laser),raidBombs=len(drops),cooldowns=len(cool)))
   ck(diff+': bounded projectile and bomb populations',max(q['rounds']for q in rows)<=128 and max(q['bombs']for q in rows)<=24,dict(rounds=max(q['rounds']for q in rows),bombs=max(q['bombs']for q in rows)))
  p.evaluate(setup,'furious');p.evaluate("s5b14Mode(B,'lock')");p.evaluate('()=>{for(let i=0;i<55;i++)updatePlay(1/60)}');a=p.evaluate('({locked:M.locked,target:{...M.target},origin:{x:B.x,y:B.y}})');p.evaluate('()=>{player.x+=100;player.y-=60;for(let i=0;i<12;i++)updatePlay(1/60)}');z=p.evaluate('({target:M.target,root:M.fireRoot,x:B.x,y:B.y})')
  ck('Committed optics freeze the aim and firing hull instead of snapping after the player',a['locked']and z['target']==a['target']and z['root']==a['origin']and abs(z['x']-a['origin']['x'])<.01 and abs(z['y']-a['origin']['y'])<.01,dict(before=a,after=z));shot(p,'optic-committed')
  p.evaluate('()=>{for(let i=0;i<20;i++)updatePlay(1/60)}');q=p.evaluate("""()=>{const q=eBullets.find(q=>q._s5b14Laser),e=S5B14.events.find(q=>q.event==='laser-round'),p=e&&s5b14Mount(B,e.part,true);return{shot:!!q,intercept:q&&enemyOrdnanceCanIntercept(q),element:q&&enemyOrdnanceElement(q),hp:q?.hp,shootable:q?._shootable,sourceError:p&&Math.hypot(e.x-p.x,e.y-p.y)};}""")
  ck('Laser rounds originate at the actual live cannon bore and are ordinary unshootable ordnance',q['shot']and q['intercept']==False and q['element']is None and not q['shootable']and q['sourceError']<.01,q)
  # Destroy one real cannon while a committed burst is queued.
  q=p.evaluate("""()=>{const part=siegeBomberParts(B).find(q=>q.id==='laserL');siegeBomberHit(B,99999,part.x,part.y,part.id);const mark=S5B14.events.length;for(let i=0;i<180;i++)updatePlay(1/60);return{left:B._bomber.parts.find(q=>q.id==='laserL').hp,queued:M.plan.some(q=>q.id==='laserL'),released:eBullets.some(q=>q._s5b14Owner===B&&q._s5b14Part==='laserL'),newLeft:S5B14.events.slice(mark).filter(q=>q.event==='laser-round'&&q.part==='laserL').length};}""")
  ck('Breaking a cannon cancels its queued and released fire and prevents new optics/fire',q['left']==0 and not q['queued']and not q['released']and q['newLeft']==0,q)
  # Verify native damage and visible white pixels on the actual prepared module.
  p.evaluate(setup,'normal');p.evaluate("s5b14Mode(B,'lock');M.warn=999;M.lockAt=998;M.target={x:player.x,y:player.y};M.fireRoot={x:B.x,y:B.y};M.locked=true");shot(p,'before-module-hit')
  q=p.evaluate("""()=>{const p=siegeBomberParts(B).find(p=>p.id==='laserR'),m=B._bomber.parts.find(q=>q.id===p.id),old=m.hp;siegeBomberHit(B,17,p.x,p.y,p.id);return{old,hp:m.hp,flash:m.flash};}""");shot(p,'module-white-hit')
  before=np.array(Image.open(O/'before-module-hit.png').convert('RGB'));after=np.array(Image.open(O/'module-white-hit.png').convert('RGB'));white=(after.min(axis=2)>235)&(np.max(abs(after.astype(int)-before.astype(int)),axis=2)>30)
  ck('Actual native module damage produces changed white sprite pixels',q['old']-q['hp']==17 and q['flash']>0 and int(white.sum())>100,dict(**q,changedWhitePixels=int(white.sum())));p.evaluate('()=>{for(let i=0;i<25;i++)updatePlay(1/60)}');ck('Native module hit flash expires normally',p.evaluate('B._bomber.parts.find(q=>q.id==="laserR").flash===0'))
  # Native core protection and source-alpha flight gating are kept separate.
  q=p.evaluate("""()=>{const hp=B._bomber.core;const closed=sb28Closed(B);siegeBomberHit(B,99999,B.x,B.y,'core');return{closed,before:hp,after:B._bomber.core,ids:siegeBomberTargets(B).map(q=>q._retinaId)}}""");ck('All four original modules still gate the intact core',q['closed']and q['before']==q['after']and'bomber-core'not in q['ids'],q)
  q=p.evaluate("""()=>{s5b14Mode(B,'spool');const hp=B.hp;const p=siegeBomberParts(B).find(q=>q.id==='laserR');siegeBomberHit(B,20,p.x,p.y,p.id);return{same:B.hp===hp,at:siegeBomberAt(B,p.x,p.y),beam:siegeBomberBeam(B,{x:p.x,w:8,top:0,bot:VH}),targets:siegeBomberTargets(B).length}}""");ck('Upper-plane overflight cannot collide, absorb shots or remain a shootable Retina target',q['same']and q['at']is None and q['beam']is None and q['targets']==0,q)
  # Moving forward shortens a finite catch-up; neither path heals or recreates parts.
  times=[]
  for forward in [False,True]:
   p.evaluate(setup,'normal');p.evaluate('f=>{s5b14Mode(B,"catch");player.y=f?PLAY.y+70:VH-60;}',forward)
   q=p.evaluate('()=>{const hp=B.hp;let n=0;while(M.phase===\'catch\'&&n++<400)siegeBomberTick(B,1/60);return{n,hp,after:B.hp,phase:M.phase,depth:M.depth}}');times.append(q)
  ck('Catch-up responds to forward flight and always returns to the damage plane finitely',times[1]['n']<times[0]['n']and all(q['n']<=221 and q['hp']==q['after']and q['phase']=='stalk'and q['depth']==1 for q in times),times)
  p.evaluate(setup,'normal');q=p.evaluate("""()=>{const part=siegeBomberParts(B).find(q=>q.id==='engineL');siegeBomberHit(B,99999,part.x,part.y,part.id);s5b14Mode(B,'spool');for(let i=0;i<40;i++)updatePlay(1/60);for(let i=0;i<81;i++)updatePlay(1/60);const slower=M.phase==='boost',hp=B.hp;for(let i=0;i<18;i++)updatePlay(1/60);return{slower,next:M.phase,engines:M.engines,broken:B._bomber.parts.find(q=>q.id==='engineL').hp,hp,after:B.hp};}""")
  ck('Destroying an engine slows the retreat without healing or recreating it',q['slower']and q['next']=='turn-in'and q['engines']==1 and q['broken']==0 and q['hp']==q['after'],q)
  p.evaluate(setup,'normal');q=p.evaluate("""()=>{player.invuln=0;DBGT.god=false;s5b14Mode(B,'charge');M.diveX=player.x;M.t=Math.sqrt((player.y-(viewTopY()+65))/(VH+230-(viewTopY()+65)))*2.45-1/60;M.dropCd=999;let calls=0;const saved=playerHit;playerHit=function(){calls++;};try{updatePlay(1/60);const safe=calls===0&&Math.abs(B.y-player.y)<2&&B._s4MiniSafe;M.air=false;B._s4MiniSafe=false;M.phase='lock';M.warn=999;M.locked=true;M.fireRoot={x:player.x,y:player.y};M.target={x:player.x,y:player.y};updatePlay(1/60);return{safe,controlContact:calls>0};}finally{playerHit=saved;}}""")
  ck('Native player collision ignores the overhead hull but still contacts a same-plane hull',q['safe']and q['controlContact'],q)
  p.evaluate(setup,'furious');q=p.evaluate("""()=>{s5b14Mode(B,'lock');const clock=M.clock;player.dead=true;const n=S5B14.events.length;for(let i=0;i<200;i++)siegeBomberTick(B,1/60);return{frozen:M.clock===clock,newFire:S5B14.events.slice(n).some(q=>q.event==='laser-round'||q.event==='bomb-drop'),plan:M.plan.length};}""")
  ck('No new targeting or attacks continue after the last live pilot dies',q['frozen']and not q['newFire']and q['plan']==0,q)
  # Native pause, score, all-module exhaustion and death owner.
  p.evaluate(setup,'normal');t=p.evaluate('()=>{setState(GS.PAUSED);return M.clock}');p.evaluate(STEP,60);q=p.evaluate('t=>{const same=M.clock===t;setState(GS.PLAY);return same}',t);ck('Pause preserves flight/optics clocks',q)
  q=p.evaluate("""()=>{for(const m of B._bomber.parts.slice()){const p=siegeBomberParts(B).find(q=>q.id===m.id);siegeBomberHit(B,m.hp+1,p.x,p.y,m.id);}const core=B._bomber.core,score=run.score;siegeBomberHit(B,core+1,B.x,B.y,'core');for(let i=0;i<220;i++)updatePlay(1/60);const first=run.score;for(let i=0;i<150;i++)updatePlay(1/60);return{hp:B.hp,dead:B.dead,done:subBossDone,score:run.score,first,prior:score,shots:eBullets.filter(q=>q._s5b14Owner===B).length,bombs:groundTargetingFx.filter(q=>q._s5b14Owner===B&&!q.dead).length}}""")
  ck('Full native module/core exhaustion cleans attacks and completes defeat/reward once',q['dead']and q['hp']==0 and(q['done']or q['first']>q['prior'])and q['score']==q['first']and q['shots']==0 and q['bombs']==0,q)
  q=p.evaluate("""()=>{run.stage=6;spawnSubBoss('siegebomber');const b=subBoss;return{own:s5b14Own(b),state:!!b._s5b14,stage:run.stage}}""");ck('Stage6 and its original bomber owner remain outside this rewrite',not q['own']and not q['state'],q)
  ck('No native page, update or draw errors',not errors,errors);br.close()
finally:stop()
I=json.loads((W/'installation.json').read_text());ck('Stage5 boss, Draconus work, other stages and native source owners stay byte-identical',all(hashlib.sha256((R/n).read_bytes()).hexdigest()==h for n,h in I['protected'].items()))
(O/'native-traces.json').write_text(json.dumps(traces,separators=(',',':')));(O/'checks.json').write_text(json.dumps(dict(checks=checks,errors=errors,runtimeHash=hashlib.sha256((R/'assets/stage5_bomber_assault_1114.js').read_bytes()).hexdigest()),indent=2));assert all(q['passed']for q in checks)and not errors
