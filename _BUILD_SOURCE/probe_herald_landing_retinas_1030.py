from pathlib import Path
import sys,json,http.server,numpy as np,math
from PIL import Image
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];W=R/'_shots/herald_landing_retinas_1030/probe';W.mkdir(parents=True,exist_ok=True);sys.path.insert(0,str(R/'_BUILD_SOURCE'))
from shoot import serve,STEP
from barrage_review_common_1025 import boot,advance
http.server.ThreadingHTTPServer.request_queue_size=256;checks=[];errors=[]
def ck(n,v,d=None):
 checks.append(dict(name=n,passed=bool(v),data=d));(W/'checks.json').write_text(json.dumps(checks,indent=2));assert v,(n,d)
im=np.asarray(Image.open(R/'assets/game/levels/stage_08/miniboss/herald_landing_retinas_1030/retina.png').convert('RGBA'))
ck('Retina atlas contains24 fixed64x32 colour/fade frames',im.shape==(96,512,4))
for c in range(3):
 a=[int(im[c*32:(c+1)*32,f*64:(f+1)*64,3].sum())for f in range(8)]
 ck(['Green','Yellow','Red'][c]+' fade is authored into increasing pixel alpha',all(b>a for a,b in zip(a,a[1:])),a)
port,stop=serve(str(R))
try:
 with sync_playwright()as pw:
  br=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required']);bc=br.new_context(viewport={'width':1280,'height':800});p=boot(bc,port,8,errors)
  p.evaluate('()=>{run.stage=8;stageLoadBegin(8)}');p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(8)}',timeout=180000)
  p.evaluate("()=>{beginStage(8);BOFCinematicDirector.cancel();story=null;diffKey='furious';debugStartFight({stage:8,role:'mini',kind:'heralddeath'},{pilot:'cole',record:false});spawnSubBoss('heralddeath');debugFight.spawned=true;subBossActive=true;warnT=0;DBGT.god=true;player.invuln=1e9;BOFCinematicDirector.cancel();setState(GS.PLAY);window.B=subBoss;HB25.events=[];HL51.events=[];pBullets=[];eBullets=[];hb25Flight(B,'bomber')}")
  ck('Retina frames are preloaded before the bomber attack',p.evaluate('XART.rdy(HL51_ART.key)'))
  ck('Native bomber reaches its pre-drop tell',advance(p,"B._hd1003._hb25?.phase==='tell'",500,1))
  ck('No acquisition marks exist before a physical drop releases',p.evaluate('eBullets.filter(q=>q._hl51&&!q.dead).length===0'))
  ck('Native drop releases a landing mark',advance(p,"HL51.events.some(e=>e.event==='drop')",180,1))
  p.evaluate('()=>{window.firstBomb=eBullets.find(q=>q._hl51&&!q.dead);window.markTrace=[];}')
  for i in range(14):
   q=p.evaluate('''()=>{const m=hl51Mark(firstBomb);if(m)markTrace.push({...m,target:{...m.target}});drawWorld(0);SC12.refresh();__bofFit();return m;}''')
   if i in [0,4,12]:p.screenshot(path=str(W/f'retina-arrival-{i}.png'))
   p.evaluate(STEP,1)
  trace=p.evaluate('markTrace');dist=[math.hypot(t['x']-t['target']['x'],t['y']-t['target']['y'])for t in trace]
  ck('Mark starts faint and in motion, then rapidly locks onto the impact',trace[0]['frame']%8<7 and not trace[0]['settled']and trace[-1]['settled']and dist[0]>25 and dist[-1]<1e-8 and all(b<=a+1e-6 for a,b in zip(dist,dist[1:])),dict(distances=dist,frames=[q['frame']for q in trace]))
  ck('Fade and movement finish within first quarter of actual bomb flight',p.evaluate('firstBomb._hl51Reveal<=.18&&firstBomb._hl51Reveal<=(firstBomb._hb25Bomb.at-firstBomb._hb25Born)*.25+.0001'))
  q=p.evaluate('''()=>{const art=ctx.drawImage,native=groundTargetReticleDraw,calls=[],legacy=[];ctx.drawImage=function(im,...a){if(im===XART.get(HL51_ART.key))calls.push(a);return art.apply(this,[im,...a])};groundTargetReticleDraw=function(...a){legacy.push(a);return native.apply(this,a)};try{heraldDeathDraw(B)}finally{ctx.drawImage=art;groundTargetReticleDraw=native}return{calls,legacy,live:eBullets.filter(q=>q._hl51&&!q.dead).length};}''')
  ck('Every falling drop has one real authored Retina blit and no old popping marker',q['live']>0 and len(q['calls'])==q['live']and not q['legacy']and all(c[-2:]==[64,32]for c in q['calls']),q)
  ck('Released targets sit at the bottom of the current arena',p.evaluate('eBullets.filter(q=>q._hl51&&!q.dead).every(q=>q._hb25Bomb.target.y===VH-36)'))
  target=p.evaluate('({...firstBomb._hb25Bomb.target})');p.evaluate('()=>{player.x+=50;camX=Math.max(0,camX-12)}');ck('Player/camera motion cannot drag a committed target',p.evaluate('({...firstBomb._hb25Bomb.target})')==target)
  for i in range(450):
   p.evaluate(STEP,1)
   if i%60==0:p.wait_for_timeout(1)
  e=p.evaluate('HL51.events');drops=[q for q in e if q['event']=='drop'];hits=[q for q in e if q['event']=='impact']
  ck('Both native ordinary and radial-explosive drops receive cues',any(q['simple']for q in drops)and any(not q['simple']for q in drops),dict(drops=len(drops),impacts=len(hits)))
  ck('Every released velocity/fuse ends on its marked bottom point',all(abs(q['x']+q['vx']*60*(q['at']-q['time'])-q['target']['x'])<1e-6 and abs(q['y']+q['vy']*60*(q['at']-q['time'])-q['target']['y'])<1e-6 for q in drops))
  ck('Actual ordinary and radial impacts match their locked Retina coordinates',hits and all(any(d['id']==h['id']and d['target']['x']==h['x']and d['target']['y']==h['y']for d in drops)for h in hits),hits[:3])
  ck('Projectile pressure remains inside the native128-round cap',p.evaluate('eBullets.filter(q=>q._hb25Chaos&&!q.dead).length<=128'))
  p.evaluate("()=>{eBullets=[];const Q={escapeX:player.x,rank:3,drops:0},m=hd1003Muzzle(B,'gunL');window.Q=Q;window.P={id:'gunL',burst:false,target:{x:m.x,y:300},seed:99,wave:1};hb25BombDrop(B,Q,P);window.cancelBomb=eBullets.find(q=>q._hl51)}")
  ck('Ordinary marked drops remain unshootable',p.evaluate('cancelBomb&&!enemyOrdnanceCanIntercept(cancelBomb)&&!cancelBomb._shootable'))
  p.evaluate("()=>{const gun=hd1003Part(B,'gunL');window.gunHp=gun.hp;gun.hp=0;hb25Prune();}");ck('Broken claw cancels its in-flight drop and animated mark',p.evaluate('cancelBomb.dead&&hl51Mark(cancelBomb)===null'))
  p.evaluate("()=>{hd1003Part(B,'gunL').hp=gunHp;eBullets=[];hb25BombDrop(B,Q,P);window.exitBomb=eBullets.find(q=>q._hl51);run.stage=7;hb25Prune();}");ck('Stage exit clears drops and marks',p.evaluate('exitBomb.dead&&hl51Mark(exitBomb)===null'))
  ck('Dual-red claw laser asset owner remains loaded',p.evaluate('typeof HL67!=="undefined"&&XART.rdy(HL67_ART.projectile.key)'))
  ck('No native page/console errors',not errors,errors);(W/'landing-events.json').write_text(json.dumps(e,indent=2));br.close()
finally:stop()
print(len(checks),'Herald landing Retina checks passed')
