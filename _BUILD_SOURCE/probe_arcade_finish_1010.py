"""Native pixels, fixed mounts, shieldless dives and sideways volcano vents."""
from pathlib import Path
import sys,json,base64,io,subprocess
import numpy as np
from PIL import Image
from playwright.sync_api import sync_playwright
import imageio_ffmpeg
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'_BUILD_SOURCE'));import shoot
OUT=ROOT/'_shots/arcade_finish_1010';OUT.mkdir(exist_ok=True)
checks=[];errors=[]
def check(name,ok,data=None):
 checks.append({'name':name,'pass':bool(ok),'data':data});print(('PASS ' if ok else 'FAIL ')+name,flush=True)
def capture(p,path):
 data=base64.b64decode(p.evaluate('()=>cv.toDataURL().split(",")[1]'));path.write_bytes(data);return Image.open(io.BytesIO(data)).convert('RGB')
port,stop=shoot.serve(str(ROOT))
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(args=['--autoplay-policy=no-user-gesture-required']);p=br.new_page(viewport={'width':1280,'height':900});p.set_default_timeout(120000)
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:700]) if m.type=='error' or 'draw error' in m.text else None)
  p.on('response',lambda r:errors.append(f'HTTP {r.status} {r.url}') if r.status>=400 else None)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>4');p.evaluate(shoot.TRAP_RAF);p.wait_for_timeout(60)
  p.evaluate('()=>{sm10Warm(Object.keys(SM10_ART));af10Warm();for(const a of Object.values(AC10_JET_ART).flat())XART.rdy(a.key);}')
  p.wait_for_function('()=>Object.values(SM10_ART).flat().every(a=>XART.rdy(a.key))&&af10Ready()&&Object.values(AC10_JET_ART).flat().every(a=>XART.rdy(a.key))',polling=50)
  # Read actual XART pixels with the game's own ctx.drawImage. The canvas is
  # opaque, so occupied RGB pixels define the registration mask, not its alpha.
  metrics={}
  for name,bank in p.evaluate('Object.entries(SM10_ART).filter(([k])=>k!=="electric_ring"&&!k.endsWith("_blue"))'):
   cells=[]
   for a in bank:
    data=p.evaluate('(a)=>{ctx.setTransform(1,0,0,1,0,0);ctx.clearRect(0,0,cv.width,cv.height);ctx.imageSmoothingEnabled=false;ctx.drawImage(XART.get(a.key),0,0,384,384);return cv.toDataURL().split(",")[1];}',a)
    cells.append(np.array(Image.open(io.BytesIO(base64.b64decode(data))).convert('RGB'))[:384,:384].astype(float))
   ref=cells[0];mask=np.max(ref,axis=2)>60;mask[:120]=False;mask[260:]=False;mask[:,:120]=False;mask[:,260:]=False;yy,xx=np.where(mask);shifts=[]
   for im in cells:
    cost=[(float(np.mean((ref[yy,xx]-im[yy+dy,xx+dx])**2)),dx,dy) for dy in range(-5,6) for dx in range(-5,6)]
    _,dx,dy=min(cost);shifts.append([dx,dy])
   metrics[name]=shifts;check(name+' fixed core stays registered',max(abs(v) for s in shifts for v in s)<=2,shifts)
  (OUT/'native-registration.json').write_text(json.dumps(metrics,indent=2)+'\n')
  for name,bank in p.evaluate('Object.entries(AF10_ART)'):
   renders=[]
   for a in bank:
    renders.append(p.evaluate('(a)=>{ctx.setTransform(1,0,0,1,0,0);ctx.clearRect(0,0,cv.width,cv.height);ctx.drawImage(XART.get(a.key),0,0);return cv.toDataURL();}',a))
   check(name+' has 32 distinct native frames',len(bank)==32 and len(set(renders))==32)
  def stage(n):
   p.evaluate('(n)=>{beginStage(n);setState(GS.PLAY);stagePlan=[];spawnClock=9999;waveIdx=999;story=null;BOFCinematicDirector.cancel();enemies=[];eBullets=[];boss=null;bossActive=false;subBoss=null;subBossActive=false;player.reset();player.invuln=1e9;player.x=worldWidth()/2;player.y=VH-100;camX=clamp(player.x-VW/2,0,worldWidth()-VW);}',n)
   for _ in range(2000):
    if p.evaluate('()=>{stageLoadTick();return stageLoadInfo(run.stage).ready;}'):break
    p.wait_for_timeout(20)
   else:raise RuntimeError('Stage load timed out')
  for n,units in [(2,['ash','skim','disc','eye','lance']),(3,['s3mine','s3interceptor'])]:
   stage(n)
   for unit in units:
    q=p.evaluate('(type)=>{enemies=[];eBullets=[];spawnEnemy(type,player.x,PLAY.y+PLAY.h*.25);const e=enemies.at(-1);for(let i=0;i<40;i++){e.t+=1/60;if(run.stage===2)volcTick(e,1/60);else s3IceTick(e,1/60);enemyShieldAutoEquip(e);enemyVolleyTick(e,1/60);}const angle=e._ac10Ram.angle;player.x+=80;for(let i=0;i<25;i++){e.t+=1/60;if(run.stage===2)volcTick(e,1/60);else s3IceTick(e,1/60);}return{shield:!!e._esh,phase:e._ac10Ram.phase,speed:e._ac10Ram.speed,locked:e._ac10Ram.angle===angle,bullets:eBullets.length};}',unit)
    check(unit+' shieldless warned locked dive',not q['shield'] and q['phase']=='ram' and q['locked'] and q['speed']>200 and q['bullets']==0,q)
   check('Stage '+str(n)+' kamikaze contact uses native explosion',p.evaluate('()=>{const e=enemies.at(-1),hit=playerHit;let hits=0;playerHit=()=>hits++;e.x=player.x;e.y=player.y;e._ac10Ram={phase:"ram",t:0,speed:90,angle:Math.PI/2};ac10Ram(e,1/60);playerHit=hit;return hits===1&&e.hp===0&&(e.dead||e._dyingT!=null)&&e.score===0;}'))
   stage(n);p.evaluate('(n)=>{spawnEnemy(n===2?"ac10firejet":"ac10icejet",player.x,190);window.E=enemies.at(-1);}',n)
   hashes=[]
   for f in range(16):
    hashes.append(p.evaluate('(f)=>{E.t=(f+.01)/16;E.flash=0;ctx.setTransform(SS,0,0,SS,0,0);ctx.clearRect(0,0,cv.width,cv.height);drawEnemy(E);return cv.toDataURL();}',f))
   check('Stage '+str(n)+' large jet 16 distinct south-facing frames',len(set(hashes))==16)
   p.evaluate('()=>{E.flash=.12;ctx.clearRect(0,0,cv.width,cv.height);drawEnemy(E);}')
   im=capture(p,OUT/f'stage{n}-jet-white.png');a=np.array(im).astype(int);mask=np.max(a,axis=2)>90
   check('Stage '+str(n)+' large jet visibly flashes white',float(np.mean(np.ptp(a[mask],axis=1)<3))>.95)
   p.evaluate('()=>{E.flash=0;for(let i=0;i<5*60;i++){E.t+=1/60;ac10Jet(E,1/60);}ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);}')
   capture(p,OUT/f'stage{n}-jet-live.png');q=p.evaluate('({shots:eBullets.length,kinds:[...new Set(eBullets.map(b=>b.type||b.kind||b._kind))],hp:E.hp,pattern:E.pattern})')
   check('Stage '+str(n)+' jet uses six-shot gun bursts',q['shots']>=6,q)
   check('Stage '+str(n)+' new jet is an ordinary lock target',p.evaluate('_lockTargets().some(q=>q===E||q.parent===E||q._target===E)'))
   p.evaluate('()=>{beginStage(run.stage);}')
   check('Stage '+str(n)+' queues three jets with finite wave clocks',p.evaluate('stagePlan.filter(q=>[12,25,38].includes(q.t)).length>=3&&stagePlan.every(q=>Number.isFinite(q.t))'))
  stage(2)
  p.evaluate('()=>{s2Vents=[];geysers=[];s2VentT=999;window.V=s2VentSpawn(-1);s2VentTick(S2VENT.warn+.001);window.G=geysers.find(q=>q.horizontal);}')
  check('Volcano vent launches from upper side and faces inward',p.evaluate('!!G&&G.side===-1&&V.y<PLAY.y+PLAY.h*.3&&G.x===camLeftX()+8'))
  p.wait_for_function('XART.rdy("efx_geyser_fire")',polling=50)
  p.evaluate('()=>{G.h=240;G.t=.5;ctx.setTransform(SS,0,0,SS,0,0);ctx.clearRect(0,0,cv.width,cv.height);efxDraw();}')
  a=np.array(capture(p,OUT/'side-geyser.png'));yy,xx=np.where(np.max(a,axis=2)>70)
  check('Geyser native pixels are horizontal',len(xx)>0 and xx.max()-xx.min()>2*(yy.max()-yy.min()),[int(xx.max()-xx.min()),int(yy.max()-yy.min())] if len(xx)>0 else 'missing pixels')
  q=p.evaluate('()=>{const hit=playerHit;let count=0;playerHit=()=>count++;player.dead=false;player.x=G.x+100;player.y=G.y;geyserTick(.01);const inLane=count;player.y=G.y+100;geyserTick(.01);playerHit=hit;return{inLane,outside:count-inLane};}')
  check('Horizontal damage matches rendered lane',q['inLane']==1 and q['outside']==0,q)
  q=p.evaluate('()=>{geysers=[];for(let i=0;i<GEYSER_CAP;i++)geyserSpawn(120+i,300,"fire");s2Vents=[];const v=s2VentSpawn(1);s2VentTick(S2VENT.warn+.001);return geysers.some(g=>g.horizontal&&g.side===1);}')
  check('Horizontal release survives full geyser cap',q)
  # The candidate page runs a real, isolated engine. It is never imported by index.
  page=br.new_page(viewport={'width':1280,'height':1000});page.set_default_timeout(120000);page.on('pageerror',lambda e:errors.append('preview '+str(e)))
  page.on('console',lambda m:errors.append('preview '+m.text[:700]) if m.type=='error' or 'draw error' in m.text else None)
  page.goto(f'http://127.0.0.1:{port}/docs/previews/neo_geo_stage1_1010/index.html');game=page.frame_locator('#game');f=page.frames[1]
  f.wait_for_function('window.PV10&&PV10.ready()',polling=50);f.evaluate(shoot.TRAP_RAF);f.wait_for_timeout(60)
  for unit in ['razorback','furious_razorback','overlord']:
   page.locator('[data-unit="'+unit+'"]').click();f.wait_for_function('PV10.ready()',polling=50);f.evaluate('()=>{ctx.setTransform(SS,0,0,SS,0,0);PV10.t=.5;drawWorld(0);}')
   capture(f,OUT/(unit+'-candidate.png'));check(unit+' keeps separately rendered modules',f.evaluate('PV10.rig().length>=5&&PV10.gone.size===0'))
   cs=[]
   for a in f.evaluate('(u)=>PV10_ART[u+"_hull"]',unit):
    data=f.evaluate('(a)=>{ctx.setTransform(1,0,0,1,0,0);ctx.clearRect(0,0,cv.width,cv.height);ctx.drawImage(XART.get(a.key),0,0);return cv.toDataURL().split(",")[1];}',a)
    cs.append(np.array(Image.open(io.BytesIO(base64.b64decode(data))).convert('RGB'))[:384,:384].astype(float))
   ref=cs[0];mask=np.max(ref,axis=2)>60;mask[:120]=False;mask[260:]=False;mask[:,:120]=False;mask[:,260:]=False;yy,xx=np.where(mask);shifts=[]
   for im in cs:
    _,dx,dy=min((float(np.mean((ref[yy,xx]-im[yy+dy,xx+dx])**2)),dx,dy) for dy in range(-5,6) for dx in range(-5,6));shifts.append([dx,dy])
   check(unit+' sixteen native hull frames keep their fixed mount',max(abs(v) for s in shifts for v in s)<=2,shifts)
   id='rotor' if unit=='overlord' else 'cannon';f.evaluate('(id)=>PV10.break(id)',id);f.evaluate('()=>{for(let i=0;i<30;i++)updatePlay(1/60);ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);}')
   capture(f,OUT/(unit+'-detached.png'));check(unit+' module detaches without hiding hull',f.evaluate('PV10.gone.size===1&&PV10.debris.length===1'))
   f.evaluate('()=>{for(let i=0;i<25;i++)updatePlay(1/60);drawWorld(0);}')
   check(unit+' detached module explodes without fading',f.evaluate('PV10.debris.length===0&&PV10.bursts.some(q=>q.bank==="plasma_blast")'))
  page.screenshot(path=str(OUT/'candidate-page.png'));br.close()
finally:stop()
check('No page, console or asset errors',not errors,errors)
result={'passed':sum(q['pass'] for q in checks),'failed':[q for q in checks if not q['pass']],'errors':errors,'checks':checks};(OUT/'verification.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'passed':result['passed'],'failed':result['failed'],'errors':errors}),flush=True)
if result['failed'] or errors:sys.exit(1)
