"""Native integration proof: flight, evasion, launch, palettes, death and legacy."""
from pathlib import Path
import base64,json,sys,http.server,threading,hashlib
R=Path(__file__).resolve().parents[2];O=R/'_shots/furyship_live_0914'
sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
sys.path.insert(0,str(R/'_BUILD_SOURCE/trailer_v7'));import capture3
from playwright.sync_api import sync_playwright
from PIL import Image,ImageDraw
checks=[];errors=[];details={};shots=[]
def ok(v,n):checks.append({'pass':bool(v),'label':n});print(('ok  'if v else'FAIL ')+n,flush=True)
class Quiet(http.server.SimpleHTTPRequestHandler):
 def __init__(self,*a,**kw):super().__init__(*a,directory=str(R),**kw)
 def log_message(self,*a):pass
srv=http.server.ThreadingHTTPServer(('127.0.0.1',0),Quiet);threading.Thread(target=srv.serve_forever,daemon=True).start()
with sync_playwright() as p:
 b=p.chromium.launch(args=['--no-sandbox','--mute-audio','--autoplay-policy=no-user-gesture-required']);pg=b.new_page(viewport={'width':1100,'height':1200})
 pg.on('pageerror',lambda e:errors.append(str(e)));pg.on('console',lambda m:errors.append(m.text)if m.type=='error'else None)
 pg.goto('http://127.0.0.1:%d/index.html'%srv.server_port,wait_until='load',timeout=120000);pg.wait_for_function('()=>(window.__bofFrames|0)>4',timeout=120000)
 pg.evaluate(shoot.TRAP_RAF);pg.evaluate(capture3.LIB)
 pg.evaluate('''()=>{__auto=function(){};window.__newKeys=[];window.__oldKeys=[];window.__deathCount=0;
 const blit=furyShipBlit;furyShipBlit=function(k){__newKeys.push(k);return blit.apply(this,arguments);};
 const old=spaceAtlasDraw;spaceAtlasDraw=function(g,k){__oldKeys.push(k);return old.apply(this,arguments);};
 const death=gravityDeathSpinDraw;gravityDeathSpinDraw=function(){__deathCount++;return death.apply(this,arguments);};}''')
 def step(n,visible=False):
  for i in range(0,n,6):
   pg.evaluate('(a)=>{if(a[1])player.invuln=0;__step(a[0]);}',[min(6,n-i),visible]);pg.wait_for_timeout(12)
 def shot(n):
  path=O/(n+'.png');path.write_bytes(base64.b64decode(pg.evaluate('()=>document.querySelector("#screen").toDataURL().split(",")[1]')));shots.append(path)
 def prep(stage=5,pilot='cole'):
  pg.evaluate('''a=>{run.mode='arcade';run.pilot=a[1];pilotIndex=PILOTS.findIndex(p=>p.key===a[1]);run.stage=a[0];curStage=STAGES[a[0]-1];furyLegacyShip=false;beginStage(a[0]);setState(GS.PLAY);player.reset();player.x=worldWidth()/2;player.y=410;player.invuln=0;story=null;special=null;stagePlan=[];waveIdx=0;boss=null;bossActive=false;bossTriggered=true;subBoss=null;subBossActive=false;subBossTriggered=true;aminiTriggered=true;enemies=[];pBullets=[];eBullets=[];particles=[];powerups=[];playerHit=function(){};for(const k of Object.keys(Input.keys))Input.keys[k]=false;warmPlayerAtlases();furyShipWarm();__newKeys=[];__oldKeys=[];}''',[stage,pilot])
  pg.wait_for_function('()=>furyShipReady()',timeout=120000);step(2)
 prep();ok(pg.evaluate('()=>furyShipReady()&&FURY_KIT.length===6'),'new frame family and all masks decode; six independent parts registered')
 for pilot in ['axel','cole','maverick','decker','yuri','freezer','juggernaut','lizzie','falva']:
  pg.evaluate('p=>{pilotIndex=PILOTS.findIndex(q=>q.key===p);run.pilot=p;__newKeys=[];}',pilot);step(2)
  ok(pg.evaluate('()=>__newKeys.includes("base")'),'actual Stage 5 flight renders '+pilot+' new hull')
  shot('flight_'+pilot)
 prep();pg.evaluate('()=>{__newKeys=[];startSomersault();}');ok(pg.evaluate('()=>!!player.somer'),'real somersault entry succeeds in space')
 for _ in range(42):step(1,True)
 pitch=pg.evaluate('()=>[...new Set(__newKeys.filter(k=>k.startsWith("somersault_")))]');details['pitchKeys']=pitch
 ok(len(pitch)==12,'all twelve pitch frames reach the native drawing path')
 for direction in [-1,1]:
  pg.evaluate('d=>{player._rollCool=0;__newKeys=[];startRoll(d);}',direction)
  for i in range(38):
   step(1,True)
   if i==10:shot('roll_'+str(direction))
  keys=pg.evaluate('()=>[...new Set(__newKeys.filter(k=>k.startsWith("roll_")))]');ok(len(keys)==8,'all eight roll frames render, direction '+str(direction))
 pg.evaluate('()=>{player._somerCool=0;player.roll=null;startSomersault();}');step(13,True);shot('pitch_end_on')
 pg.evaluate('()=>setState("paused")');clock=pg.evaluate('()=>furyFlightTime');step(30)
 ok(pg.evaluate('t=>furyFlightTime===t',clock),'pause freezes the new animation clock')
 pg.evaluate('()=>setState(GS.PLAY)');step(45,True)
 pg.evaluate('()=>{pwInput="SPCBOY";submitPassword();__newKeys=[];__oldKeys=[];player._bank=0;}');step(2)
 ok(pg.evaluate('()=>furyLegacyShip&&!furyShipReady()&&__oldKeys.includes("ship_base")&&!__newKeys.includes("base")'),'SPCBOY selects the intact original fighter')
 ok(pg.evaluate('()=>campSnapshot().unlocks.legacySpaceShip===true'),'campaign snapshot records the legacy selection')
 ok(pg.evaluate('()=>{const s=campSnapshot();furyLegacyShip=false;campApply(s);return furyLegacyShip===true;}'),'loading a campaign snapshot restores the legacy selection')
 shot('legacy_ship')
 pg.evaluate('()=>{pwInput="SPCBOY";submitPassword();}');step(2)
 ok(pg.evaluate('()=>!furyLegacyShip&&furyShipReady()'),'SPCBOY again restores the new fighter')
 prep();pg.evaluate('()=>{__deathCount=0;player.invuln=0;player.shield=0;special=null;__realHit();}');step(15)
 ok(pg.evaluate('()=>player.dead&&__deathCount>0'),'real death enters the new spaceship burning-spin draw path');shot('death_spin')
 prep(9,'yuri');step(150);ok(pg.evaluate('()=>gravityMode.phase==="active"&&run.gravityShipReady&&__newKeys.includes("base")'),'Stage 9 retains and renders the new spaceship');shot('stage9')
 prep();pg.evaluate('''()=>{run.gravityShipReady=false;setState(GS.LAUNCH);drawLaunch._phase=undefined;drawLaunch(0);gravityModeStart();drawLaunch._phase='gravity';drawLaunch._dist=SEG_B3+SEG_B1+240;gravityMode.dialogueDone=true;gravityMode.dialogueT=100;gravityModeBeginCharge();__newKeys=[];}''')
 phases=set();glow_checked=False
 for i in range(95):
  step(6)
  phase=pg.evaluate('()=>gravityMode.phase');phases.add(phase)
  if phase=='pixelglow' and not glow_checked:
   glow_ok=pg.evaluate('()=>{const saved=__newKeys;__newKeys=[];gravityModeDrawShip(240,290,90,70);const ok=__newKeys.includes("base")&&!__newKeys.some(k=>FURY_KIT.some(q=>k.startsWith(q.key+"_")));__newKeys=saved;return ok;}');glow_checked=True
   ok(glow_ok,'pixel-glow starts with the complete approved hull and no loose parts')
  if i in [12,43,49,57,62,72]:shot('assembly_%02d_%s'%(i,phase))
 details['phases']=sorted(phases)
 ok({'charge','scatter','snap','pixelglow','whiteout','reveal','active'}<=phases,'launch traverses every transformation phase into active flight')
 ok(pg.evaluate('()=>FURY_KIT.every(q=>__newKeys.some(k=>k.startsWith(q.key+"_")))&&__newKeys.some(k=>k.startsWith("assembly_"))&&__newKeys.some(k=>k.startsWith("veil_"))'),'all six parts, fusion energy and transition curtain reach the renderer')
 ok(pg.evaluate('()=>run.gravityShipReady'),'finished transformation earns the ship')
 details['loopError']=pg.evaluate('()=>window.__err||null');ok(not errors and not details['loopError'],'zero page, console and loop errors')
 b.close()
srv.shutdown()
sheet=Image.new('RGB',(960,((len(shots)+3)//4)*278),(16,23,32));d=ImageDraw.Draw(sheet)
for i,path in enumerate(shots):
 im=Image.open(path).convert('RGB');im.thumbnail((240,256));x=i%4*240;y=i//4*278;sheet.paste(im,(x,y));d.text((x+4,y+258),path.stem,fill='white')
sheet.save(O/'contact.png')
(O/'native.json').write_text(json.dumps({'checks':checks,'errors':errors,'details':details,'runtimeSha256':hashlib.sha256((R/'assets/game.js').read_bytes()).hexdigest()},indent=2)+'\n')
print(str(sum(c['pass'] for c in checks))+' passed / '+str(sum(not c['pass'] for c in checks))+' failed')
if any(not c['pass']for c in checks):raise SystemExit(1)
