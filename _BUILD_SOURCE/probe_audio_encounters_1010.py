"""Native encounter fixtures; source references use the game's own image cache."""
from pathlib import Path
import sys,json,base64
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'_BUILD_SOURCE'));import shoot
OUT=ROOT/'_shots/audio_1010';OUT.mkdir(parents=True,exist_ok=True)
REF=ROOT/'_ART_SOURCES/audio_1010/references';REF.mkdir(parents=True,exist_ok=True)
checks=[];errors=[]
def check(name,passed,data=None):
 checks.append(dict(name=name,passed=bool(passed),data=data));print(('PASS ' if passed else 'FAIL ')+name,flush=True)
port,stop=shoot.serve(str(ROOT))
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(args=['--autoplay-policy=no-user-gesture-required'])
  p=br.new_page(viewport={'width':1280,'height':900});p.set_default_timeout(120000)
  p.on('pageerror',lambda e:errors.append(str(e)))
  p.on('console',lambda m:errors.append(m.text[:800]) if m.type=='error' or 'draw error' in m.text else None)
  p.on('response',lambda r:errors.append('HTTP '+str(r.status)+': '+r.url) if r.status>=400 else None)
  p.goto(f'http://127.0.0.1:{port}/index.html',timeout=120000)
  p.wait_for_function('window.__bofFrames>4');p.evaluate(shoot.TRAP_RAF);p.mouse.click(650,450)
  def scene(n,pilot='cole'):
   p.evaluate(shoot.SETUP,dict(state='PLAY',stage=n,pilot=pilot,invuln=True))
   p.wait_for_function('n=>{stageLoadTick();return stageLoadInfo(n).ready}',arg=n,polling=50)
   p.evaluate("()=>{BOFCinematicDirector.cancel();story=null;fb2Talk=null;s6Opening=null;H3.release=false;H3.ending=null;stagePlan=[];enemies=[];pBullets=[];eBullets=[];special=null;boss=null;bossActive=false;subBoss=null;subBossActive=false;subBossDone=true;player.invuln=1e9;}")
  def frames(n):
   for start in range(0,n,30):
    r=p.evaluate(shoot.STEP,min(30,n-start))
    if r:errors.append(r);break
    p.wait_for_timeout(2)
  scene(4)
  p.evaluate("spawnBoss('stormsovereign')")
  frames(210)
  p.evaluate("()=>{boss.enter=false;er26Set(boss,'ap10-stormburst');}")
  frames(110);p.screenshot(path=str(OUT/'storm-charge.png'))
  frames(170);p.screenshot(path=str(OUT/'storm-midburst.png'))
  q=p.evaluate("AP10_E.history.filter(q=>q.event.startsWith('sovereign'))")
  check('Sovereign executes charge, vertical release and middle lightning burst',all(any(x['event']==e for x in q) for e in ['sovereign-fusion-charge','sovereign-fusion-release','sovereign-fusion-midburst']),q)
  p.evaluate("()=>{stage4CoreTurretSpawnMissing(boss,.75);}")
  frames(780)
  q=p.evaluate("()=>({shots:boss._s4war.coreShots,barrels:boss._s4war.coreBarrelShots,warnings:boss._er26.warnings})")
  check('Independent core helpers fire from both physical barrels',q['shots']>0 and all(v>0 for v in q['barrels'].values()),q)
  # Copy cache pixels with the game context's own drawImage, never .src tests.
  for key in ['cin_origin_hq_iso','ship_cole_pv2','ship_decker_pv2','ship_cole','whv_closed','vile24_robot_gray']:
   p.wait_for_function('key=>XART.rdy(key)',arg=key,polling=50)
   data=p.evaluate('''key=>{const im=XART.get(key),c=document.createElement('canvas');c.width=im.width;c.height=im.height;
    c.getContext('2d').drawImage(im,0,0);return c.toDataURL('image/png').split(',')[1];}''',key)
   (REF/(key+'.png')).write_bytes(base64.b64decode(data))
  scene(8)
  p.wait_for_function('()=>{r30Warm();furyShipWarm();return furyShipReady()}',polling=50)
  data=p.evaluate("()=>{const im=furyShipCanvas('base','cole'),c=document.createElement('canvas');c.width=im.width;c.height=im.height;c.getContext('2d').drawImage(im,0,0);return c.toDataURL('image/png').split(',')[1];}")
  (REF/'furyship_current.png').write_bytes(base64.b64decode(data))
  p.evaluate("spawnBoss('vileexistence')")
  try:p.wait_for_function("()=>{r30Warm();return r30Parts(boss).every(v=>XART.rdy(REALM30_ART[v.key]?'r30_'+v.key:v.key))}",polling=50,timeout=12000)
  except Exception:
   print(json.dumps(p.evaluate("()=>({mode:boss._r30.mode,encounter:j3State(boss).encounter,parts:r30Parts(boss).map(v=>({key:v.key,path:XART._src[v.key],ready:XART.rdy(v.key)}))})")),flush=True)
  p.evaluate("()=>{boss.x=240;boss.y=225;ctx.setTransform(1,0,0,1,0,0);ctx.clearRect(0,0,cv.width,cv.height);j3Body(boss);}")
  data=p.evaluate("()=>{const c=document.createElement('canvas');c.width=480;c.height=512;c.getContext('2d').drawImage(cv,0,0,480,512,0,0,480,512);return c.toDataURL('image/png').split(',')[1];}")
  (REF/'mutated_drone.png').write_bytes(base64.b64decode(data))
  p.evaluate("()=>{boss._r30.mode='fight';boss.enter=false;boss._r30.cd=.1;}")
  frames(1800)
  q=p.evaluate("()=>({mode:boss._r30.mode,encounter:j3State(boss).encounter,attacks:boss._r30.history.filter(q=>q.event==='attack').map(q=>q.type),bullets:eBullets.length,beams:S81003.beams.length})")
  check('First final encounter actually cycles attacks in live simulation',len(q['attacks'])>=4,q)
  check('No page, console or asset errors',not errors,errors)
  br.close()
finally:stop()
report=dict(passed=sum(q['passed'] for q in checks),failed=sum(not q['passed'] for q in checks),checks=checks,errors=errors)
(OUT/'encounters-report.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(dict(passed=report['passed'],failed=report['failed'],errors=errors)),flush=True)
sys.exit(1 if report['failed'] else 0)
