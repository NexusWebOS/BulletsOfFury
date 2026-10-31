from pathlib import Path
import sys,json,http.server
from playwright.sync_api import sync_playwright
R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');W=Path(__file__).resolve().parent;sys.path.insert(0,str(R/'_BUILD_SOURCE'));from shoot import serve,STEP
from barrage_review_common_1025 import boot,advance
http.server.ThreadingHTTPServer.request_queue_size=256;checks=[];errors=[]
def ck(n,v,d=None):
 checks.append(dict(name=n,passed=bool(v),data=d));(W/'checks.json').write_text(json.dumps(checks,indent=2));print('PASS'if v else'FAIL',n,flush=True);assert v,(n,d)
port,stop=serve(str(R))
try:
 with sync_playwright()as pw:
  br=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required']);bc=br.new_context(viewport={'width':1280,'height':800});p=boot(bc,port,8,errors)
  p.evaluate('()=>{run.stage=8;stageLoadBegin(8)}');p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(8)}',timeout=180000)
  p.evaluate("()=>{beginStage(8);BOFCinematicDirector.cancel();story=null;diffKey='furious';debugStartFight({stage:8,role:'mini',kind:'heralddeath'},{pilot:'cole',record:false});spawnSubBoss('heralddeath');debugFight.spawned=true;subBossActive=true;warnT=0;DBGT.god=true;player.invuln=1e9;BOFCinematicDirector.cancel();setState(GS.PLAY);window.B=subBoss;HB25.events=[];HL51.events=[];pBullets=[];eBullets=[];hb25Flight(B,'bomber')}")
  ck('Native bomber reaches its pre-drop tell',advance(p,"B._hd1003._hb25?.phase==='tell'",500,1),p.evaluate('({stage:run.stage,state,active:subBossActive,mode:B._hd1003.mode,phase:B._hd1003._hb25?.phase,clock:B._hd1003.clock})'))
  before=p.evaluate("""()=>{const ret=groundTargetReticleDraw,fov=combatWarningDraw,rows=[],marks=[];groundTargetReticleDraw=function(...a){marks.push(a);return ret.apply(this,a)};combatWarningDraw=function(o,a){rows.push(a);return fov.apply(this,arguments)};try{heraldDeathDraw(B)}finally{groundTargetReticleDraw=ret;combatWarningDraw=fov}return{marks,rows};}""")
  ck('No ground retinas appear before an explosive bomb releases',len(before['marks'])==0,before['marks'])
  ck('Pre-drop carpet has no vertical FOV columns',all(abs(q['ey']-q['y'])<1 for q in before['rows']),before['rows'])
  p.evaluate('drawWorld(0)');p.screenshot(path=str(W/'before-drop.png'))
  ck('Native explosive release occurs',advance(p,"HL51.events.some(e=>e.event==='drop')",180,1))
  during=p.evaluate("""()=>{const r=groundTargetReticleDraw,f=combatWarningDraw,marks=[],lanes=[];groundTargetReticleDraw=function(...a){marks.push(a);return r.apply(this,a)};combatWarningDraw=function(o,a){lanes.push(a);return f.apply(this,arguments)};try{heraldDeathDraw(B)}finally{groundTargetReticleDraw=r;combatWarningDraw=f}return{marks,lanes,bombs:eBullets.filter(q=>q._hl51&&!q.dead).map(q=>({id:q._hl51,x:q.x,y:q.y,target:q._hb25Bomb.target}))};}""")
  ck('Each live explosive drop has one reticle at its committed landing point',len(during['marks'])==len(during['bombs'])>0 and all(any(abs(m[0]-q['target']['x'])<1e-8 and abs(m[1]-q['target']['y'])<1e-8 for m in during['marks'])for q in during['bombs']),during)
  ck('Falling bombs do not draw vertical or radial FOV rays',len(during['lanes'])==0,during['lanes'])
  p.evaluate('drawWorld(0)');p.screenshot(path=str(W/'after-drop.png'))
  ck('Live bomber crosses the visible center for hit verification',advance(p,"B._hd1003._hb25?.phase==='strike'&&B.x>camLeftX()+viewW()*.35&&B.x<camLeftX()+viewW()*.65",240,1))
  pixels=p.evaluate("""()=>{drawWorld(0);const a=ctx.getImageData(0,0,cv.width,cv.height).data;window.hitBefore=hd1003Part(B,'gunR').hp;hd1003Hit(B,10,0,0,'gunR');drawWorld(0);const d=ctx.getImageData(0,0,cv.width,cv.height).data;let white=0;for(let i=0;i<d.length;i+=4)if(d[i]>240&&d[i+1]>240&&d[i+2]>240&&a[i]+a[i+1]+a[i+2]<650)white++;return{white,flash:hd1003Part(B,'gunR').flash,hp:hd1003Part(B,'gunR').hp,before:hitBefore};}""")
  ck('Real claw damage still renders white damaged pixels',pixels['white']>4 and pixels['hp']<pixels['before']and pixels['flash']>0,pixels)
  p.screenshot(path=str(W/'claw-hit.png'));p.evaluate(STEP,20)
  ck('Native claw hit flash expires normally',p.evaluate("hd1003Part(B,'gunR').flash===0"))
  # Follow real drops through both Furious passes; only the labelled prior 10HP damage fixture differs.
  for i in range(450):
   p.evaluate(STEP,1)
   if i%60==0:p.wait_for_timeout(1)
  e=p.evaluate('HL51.events');drops=[q for q in e if q['event']=='drop'];impacts=[q for q in e if q['event']=='impact']
  ck('Native passes use all four upper/middle/lower/bottom bands',set(q['band']for q in drops)=={0,1,2,3},drops)
  ck('All observed velocity vectors end at the marked point after the native fuse',all(abs(q['x']+q['vx']*60*.68-q['target']['x'])<1e-6 and abs(q['y']+q['vy']*60*.68-q['target']['y'])<1e-6 for q in drops))
  ck('Each native impact is at its own reticle position',len(impacts)>0 and all(any(d['id']==q['id']and d['target']['x']==q['x']and d['target']['y']==q['y']for d in drops)for q in impacts),impacts)
  ck('Native 128-round budget remains bounded',p.evaluate('eBullets.filter(q=>q._hb25Chaos&&!q.dead).length<=128'))
  p.evaluate("()=>{eBullets=[];const Q={escapeX:player.x,rank:3,drops:0},m=hd1003Muzzle(B,'gunL');window.dropQ=Q;window.plan={id:'gunL',burst:true,target:{x:camLeftX()+200,y:220},seed:99,wave:1};hb25BombDrop(B,Q,plan);window.testBomb=eBullets.find(q=>q._hl51)}")
  ck('Explosive bombs remain ordinary unshootable chaos ordnance',p.evaluate('testBomb&&!enemyOrdnanceCanIntercept(testBomb)&&!testBomb._shootable&&!testBomb.hp'))
  target=p.evaluate('({...testBomb._hb25Bomb.target})');p.evaluate('()=>{player.x+=100;camX=Math.max(0,camX-40)}');ck('Player and camera motion cannot retarget a released bomb',p.evaluate('({...testBomb._hb25Bomb.target})')==target)
  p.evaluate("()=>{window.blasts=[];window.expOld=explode;explode=function(x,y){blasts.push({x,y});return expOld.apply(this,arguments)};for(let i=0;i<128;i++)eBullets.push({_hb25Chaos:true,x:100,y:100,dead:false});hb25Burst(testBomb);explode=expOld;}")
  ck('Landing still explodes exactly on the reticle with a full projectile budget',p.evaluate('blasts.some(q=>q.x===testBomb._hb25Bomb.target.x&&q.y===testBomb._hb25Bomb.target.y)&&testBomb.x===testBomb._hb25Bomb.target.x&&testBomb.y===testBomb._hb25Bomb.target.y'))
  p.evaluate("()=>{eBullets=[];hb25BombDrop(B,dropQ,plan);window.cancelBomb=eBullets.find(q=>q._hl51);window.gun=hd1003Part(B,'gunL');window.oldHp=gun.hp;gun.hp=0;hb25Prune();gun.hp=oldHp;}")
  ck('A destroyed claw cancels its in-flight bomb and marker',p.evaluate('cancelBomb.dead'))
  p.evaluate("()=>{eBullets=[];hb25BombDrop(B,dropQ,plan);window.exitBomb=eBullets.find(q=>q._hl51);run.stage=7;hb25Prune();run.stage=8;}")
  ck('Stage exit cancels remaining bombs',p.evaluate('exitBomb.dead'))
  ck('No native page/console errors',not errors,errors);(W/'landing-events.json').write_text(json.dumps(e,indent=2));br.close()
finally:stop()
