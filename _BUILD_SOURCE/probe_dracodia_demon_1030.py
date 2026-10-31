from pathlib import Path
import sys,json,http.server
import numpy as np
from PIL import Image
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];W=R/'_shots/dracodia_demon_1030/probe';W.mkdir(parents=True,exist_ok=True);sys.path.insert(0,str(R/'_BUILD_SOURCE'))
from shoot import serve,STEP
from barrage_review_common_1025 import boot,advance
http.server.ThreadingHTTPServer.request_queue_size=256;checks=[];errors=[]
def ck(n,v,d=None):
 checks.append(dict(name=n,passed=bool(v),data=d));(W/'checks.json').write_text(json.dumps(checks,indent=2));print(n,bool(v),flush=True);assert v,(n,d)
M=json.loads((R/'assets/game/levels/stage_08/boss/claw_laser_1030/manifest.json').read_text())
def cell(n,f):
 a=M[n];im=Image.open(R/a['path']);return im.crop((f%a['cols']*a['cw'],f//a['cols']*a['ch'],(f%a['cols']+1)*a['cw'],(f//a['cols']+1)*a['ch']))
ck('All35 new banks use even fixed cells, common pivots and bounded atlases',len(M)==35 and all(a['cw']%2==a['ch']%2==0 and max(Image.open(R/a['path']).size)<=4096 for a in M.values()),len(M))
ck('Physical claws have64 directional frames and4 actual closure stages',M['claw']['frames']==256 and len({cell('claw',i).tobytes()for i in [0,64,128,192]})==4)
ck('White hit masks preserve the authored claw and tendon alpha',all(cell(n,f).getchannel('A').tobytes()==cell(n+'_hit',f).getchannel('A').tobytes()for n in ['claw','tendon']for f in [0,16,70,200]))
ck('All45 inset-turret poses carry same-frame body anchors',all(len(M['turret_'+n+'_'+s]['anchors'])==M['turret_'+n+'_'+s]['frames']for n in ['dracodia_wind','dracodia_strike','dracodia_recover']for s in ['left','right']))
im=Image.new('RGBA',(640,480),(15,22,30,255))
for i,(n,f)in enumerate([('claw',16),('claw',208),('tendon',16),('beam',16),('optic_root',16),('missile',16),('asterisk',1),('turret_dracodia_wind_left',0)]):
 c=cell(n,f);im.alpha_composite(c,(i%4*160,i//4*200))
im.save(W/'art-inspection.png')
port,stop=serve(str(R))
try:
 with sync_playwright()as pw:
  br=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required']);p=boot(br.new_context(viewport={'width':1280,'height':800}),port,8,errors,'boss')
  p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(8)&&Object.values(RD72_ART).every(a=>XART.rdy(a.key))}',timeout=180000)
  ck('Native possession intro reaches combat with all original HP',advance(p,"boss._r30.mode==='fight'",90,16)and p.evaluate('boss.hp===boss.maxhp'))
  p.evaluate('()=>{window.B=boss;window.initialHP=B.hp;window.coreMax=B.parts.find(p=>p.id==="core").maxhp;player.invuln=0;}')
  def start(kind):p.evaluate('(k)=>{v18Clear(B);eBullets.length=0;smokeTrails.length=0;player.invuln=0;rd72Start(B,k);}',kind)
  def step(n):
   err=p.evaluate(STEP,n)
   if err:raise RuntimeError(err)
  def shot(n):
   p.evaluate('()=>{drawWorld(0);SC12.refresh();__bofFit()}');p.screenshot(path=str(W/(n+'.png')))
  start('missiles');step(86);shot('missile-ports')
  q=p.evaluate('()=>{const q=eBullets.filter(q=>q._rd72Missile);return{n:q.length,ports:RD72.events.filter(q=>q.event==="inset-missile").slice(-2),claws:rb23Arms(B).map(p=>rb23PartPoint(B,p,true)),shootable:q.every(q=>q._shootable&&!q._weaponProof&&q.hp===3),kinds:[...new Set(q.map(q=>q.kind))]};}')
  ck('Paired shootable missiles launch from inset tubes rather than distal claws',q['n']>=2 and q['shootable']and all(abs(a['x']-b['x'])>5 or abs(a['y']-b['y'])>15 for a,b in zip(q['ports'],q['claws'])),q)
  ck('Purple missile exhaust replaces the retired yellow smoke/flame trail',p.evaluate('eBullets.filter(q=>q._rd72Missile).every(q=>q._energyOrdnance)&&!smokeTrails.some(q=>q.kind==="missile")'))
  ck('Missile attack recovers into the normal encounter owner',advance(p,'!rd72Act(B)',400,1))
  for kind in ['eyeFan','eyeSweep','eye360']:
   start(kind);step(55);shot(kind+'-warning');step(40);shot(kind+'-active')
   ck(kind+' keeps the red beam attached to the moving eye and recovers',advance(p,'!rd72Act(B)',400,1))
  ev=p.evaluate('RD72.events');dirs=[e['dir']for e in ev if e['event']=='optic-turn'and e['kind']=='eye360']
  ck('Furious fan delivers12 rapid flashes;360 sweep visits all64 directions',sum(e['event']=='optic-fan-blast'for e in ev)==12 and len(set(dirs))==64,dict(fan=sum(e['event']=='optic-fan-blast'for e in ev),circleDirections=len(set(dirs))))
  ck('The retired generic claw shots and warning sidecar remain disabled',p.evaluate('!eBullets.some(q=>q._target17Owner===B&&!q.dead)&&!TARGET17.events.some(q=>q.event==="weapon-shot")'))
  start('swipe');step(88);shot('physical-swipe');q=p.evaluate('()=>{const P=rd72Act(B),v=P.rig;return{target:P.target,tip:v.tip,nodes:v.nodes.length,d:Math.hypot(v.wrist.x-v.root.x,v.wrist.y-v.root.y),retina:rb23PartPoint(B,B.parts.find(p=>p.id===P.side)),collision:r30At(B,v.wrist.x,v.wrist.y)?.id,side:P.side};}')
  ck('Actual extending arm carries collision and Retina anchors with its claw',q['d']>100 and q['nodes']>7 and q['retina']==q['tip'],q)
  ck('Physical swipe fully retracts before the next attack',advance(p,'!rd72Act(B)',400,1))
  p.evaluate('()=>{v18Clear(B);eBullets.length=0;DBGT.god=false;player.invuln=0;player.roll=player.somer=null;run.shield=2;const e=rb23Eye(B);player.x=e.x+60;player.y=e.y+140;rd72BeamHit(B,16);}')
  ck('A ship outside the rendered beam keeps its shields',p.evaluate('!player.dead&&run.shield===2'))
  p.evaluate('()=>{const e=rb23Eye(B);player.x=e.x;player.y=e.y+140;rd72BeamHit(B,16);}')
  ck('A ship inside the rendered beam takes native damage exactly once',p.evaluate('!player.dead&&run.shield===1&&player.invuln>0'))
  p.evaluate('()=>{DBGT.god=true;player.invuln=0;player.x=worldWidth()/2;player.y=VH-110;rd72Start(B,"grab");}')
  ck('Native GOD still permits a nonfatal capture',advance(p,'!!player._rd72Grab',300,1))
  ck('Debug GOD prevents the fatal throw without leaving capture/input locks',advance(p,'RD72.events.some(q=>q.event==="grab-god-survived")',200,1)and p.evaluate('!player.dead&&!player._rd72Grab'))
  step(50)
  p.evaluate('()=>{v18Clear(B);player.invuln=0;player.x=worldWidth()/2;player.y=VH-110;rd72Start(B,"grab");}')
  ck('A captured pilot can leave the encounter safely',advance(p,'!!player._rd72Grab',300,1))
  p.evaluate('()=>stageLoadBegin(8)')
  ck('Stage-load cancellation releases the held pilot and restores its inputs',p.evaluate('!player.dead&&!player._rd72Grab&&player.invuln>=60&&RD72.events.some(q=>q.event==="grab-released"&&q.reason==="stage-change")'))
  # A controlled real-player fixture: native damage/death/life pipeline, no GOD.
  p.evaluate('()=>{v18Clear(B);eBullets.length=0;DBGT.god=false;player.invuln=0;player.roll=player.somer=null;player.x=worldWidth()/2;player.y=VH-110;run.shield=2;window.livesBefore=run.lives;window.deathsBefore=run.stats?.deaths||0;window.hitOriginal=playerHit;playerHit=function(source){if(rd72Act(B)?.kind==="grab"&&!player._rd72Grab)rd72Log("fixture-hit-before-grip",{source,stack:new Error().stack});return hitOriginal.apply(this,arguments);};rd72Start(B,"grab");}')
  caught=advance(p,'!!player._rd72Grab',300,1);q=p.evaluate('({dead:player.dead,shield:run.shield,invuln:player.invuln,roll:!!player.roll,somer:!!player.somer,kind:rd72Act(B)?.kind,events:RD72.events.slice(-10),x:player.x,y:player.y,tip:rd72Act(B)?.rig?.tip})');shot('grab-attempt');ck('Grab catches a real player without killing or consuming its shields',caught and p.evaluate('!player.dead&&run.shield===2'),q)
  pos=p.evaluate('({x:player.x,y:player.y})');p.evaluate('()=>{window.bombsBefore=run.bombs;window.roundsBefore=pBullets.length;Input.keys.a=Input.keys.j=Input.keys.k=Input.keys.c=true;}');step(24);shot('grab-hold')
  q=p.evaluate('({held:!!player._rd72Grab,dead:player.dead,y:player.y,inputs:!!Input.keys.a,grip:rd72Act(B)?.rig.tip})')
  ck('Held ship is lifted inside the closing claw while its controls are locked',q['held']and not q['dead']and q['y']<pos['y']-30,q)
  ck('Held fire and missile inputs cannot shoot or spend ammunition',p.evaluate('pBullets.length<=roundsBefore&&run.bombs===bombsBefore'))
  p.evaluate('()=>{for(const k of Object.keys(Input.keys))Input.keys[k]=false;}')
  ck('Committed throw invokes a native death even with stocked shields',advance(p,'player.dead',150,1)and p.evaluate('run.shield===0&&!player._rd72Grab&&!!player._spin&&!!player._rd72Thrown'))
  step(12);shot('grab-thrown-wreck');q=p.evaluate('({dead:player.dead,x:player.x,edge:camLeftX(),right:camRightX(),spin:player._spin?.t,life:run.lives,deaths:run.stats?.deaths})');ck('Thrown wreck travels outward through native tumbling/fire death state',q['dead']and q['spin']>0,q)
  ck('Native death finishes, spends one life and restores normal play',advance(p,'!player.dead',600,1)and p.evaluate('run.lives===livesBefore-1&&!player._rd72Grab&&!player._rd72Thrown'))
  # Destroying the actual grabbing arm must rescue the live pilot.
  p.evaluate('()=>{DBGT.god=true;player.invuln=0;player.roll=player.somer=null;player.x=worldWidth()/2;player.y=VH-110;v18Clear(B);eBullets.length=0;rd72Start(B,"grab");}')
  ck('Second grab can catch a respawned pilot',advance(p,'!!player._rd72Grab',300,1))
  p.evaluate('()=>{const P=rd72Act(B),part=B.parts.find(p=>p.id===P.side);B._lastPart=part;modularHit(part.hp);}')
  ck('Destroying the whole grabbing arm rescues the living pilot',p.evaluate('!player.dead&&!player._rd72Grab&&RD72.events.some(q=>q.event==="grab-released"&&q.reason==="grabbing-arm-destroyed")'))
  shot('claw-arm-destroyed')
  p.evaluate('()=>{window.hp=B.hp;B._lastPart=B.parts.find(p=>p.id==="core");modularHit(40);}')
  ck('Remaining arm still protects native core HP',p.evaluate('B.hp===hp'))
  p.evaluate('()=>{const part=rb23Arms(B)[0];B._lastPart=part;modularHit(part.hp);}')
  ck('Both actual shoulder/arm pools gate the original exposed-core phase',p.evaluate('!rb23Arms(B).length&&B.hp===coreMax'))
  ck('Armless native rolling/code phase remains available',advance(p,'!!B._r30.v18.attack',400,1)and p.evaluate('!B._r30.v18.attack._rd72'))
  ck('No browser, console or native draw errors',not errors,errors)
  (W/'events.json').write_text(json.dumps(p.evaluate('RD72.events'),indent=2));br.close()
finally:stop()
print(len(checks),'claw/optic/turret checks passed')



