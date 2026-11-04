"""Native smoke checks for the new motion owner, without replacing game logic."""
import json,base64
from playwright.sync_api import sync_playwright
from native_flight import *
checks=[];errors=[];samples=[]
def check(value,name):
 checks.append({'ok':bool(value),'name':name});print(('OK 'if value else 'FAIL ')+name,flush=True)
with sync_playwright()as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required','--disk-cache-size=1','--media-cache-size=1'])
 p=b.new_page(viewport={'width':1280,'height':800});p.on('pageerror',lambda e:errors.append(str(e)));boot(p);setup(p)
 check(p.evaluate('SS===2&&cv.width===960&&!ctx.imageSmoothingEnabled'),'high quality native backing retained')
 for rate in [30,60,120]:
  setup(p);p.evaluate('()=>{enemies=[];eBullets=[];window.E=spawnEnemy("l6v_s0",worldWidth()*.28,-190,{});}')
  result=p.evaluate('''hz=>{for(let i=0;i<hz*12;i++){stateT+=1/hz;updatePlay(1/hz);}return{hz,x:E.x,y:E.y,phase:E._gf113.phase,age:E._gf113.age,hp:E.hp,finite:Number.isFinite(E.x+E.y+gf113Head(E))};}''',rate)
  samples.append(result);check(result['finite']and result['phase']in ['dive','exit'],'finite native flight at '+str(rate)+'Hz')
 # Pause uses the real state owner. No manual advancement during pause.
 setup(p);p.evaluate('()=>{window.E=spawnEnemy("l6v_s0",worldWidth()*.28,-190,{});for(let i=0;i<240;i++)updatePlay(1/60);window.pauseBefore={x:E.x,y:E.y,age:E._gf113.age};setState("paused");}')
 p.evaluate('()=>{for(let i=0;i<60;i++){const cb=window.__bofPendingRAF;if(cb)cb(performance.now()+i*16.667);}}')
 check(p.evaluate('state==="paused"&&E.x===pauseBefore.x&&E.y===pauseBefore.y&&E._gf113.age===pauseBefore.age'),'real pause freezes routed aircraft')
 p.evaluate('()=>{setState(GS.PLAY);updatePlay(1/60);}')
 check(p.evaluate('E._gf113.age>pauseBefore.age'),'real play resume advances flight')
 # Preserve native HP/damage and actual renderer feedback on the same actor.
 setup(p);p.evaluate('()=>{window.E=spawnEnemy("l6v_s0",worldWidth()/2,150,{});window.hpBefore=E.hp;hitEnemy(E,1);ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);}')
 check(p.evaluate('E.hp<hpBefore&&E.flash>0&&!E.dead'),'native hit damage and flash retained')
 (W/'native-hit.png').write_bytes(base64.b64decode(p.evaluate('cv.toDataURL().split(",")[1]')))
 # The motion owner must let the original encounter cancellation take over.
 p.evaluate('()=>{subBossActive=true;const before=ai27Begin(E,1/60);ai27End(E,before);}')
 check(p.evaluate('E._gf113.released&&!gf113Own(E)'),'miniboss handoff releases motion')
 check(p.evaluate('spawnEnemy("l6v_s0",worldWidth()/2,-190,{})?._gf113==null'),'boss helpers excluded during active encounter')
 p.evaluate('()=>{subBossActive=false;window.ground={dead:false,hp:10,ground:true,type:"l6v_s0"};}')
 check(p.evaluate('!gf113Eligible(ground)'),'ground enemies excluded')
 # Native Stage8 launched children keep their launch/scaling owner.
 setup(p,8);p.evaluate('()=>{window.E=spawnEnemy("s8interceptor",worldWidth()/2,-190,{});E._s811.launchOwner={};E._s811.phase="launch";const old=ai27Begin(E,1/60);ai27End(E,old);}')
 check(p.evaluate('E._gf113.released&&!gf113Own(E)'),'carrier child launch releases route')
 setup(p,7);p.evaluate('()=>{window.E=spawnEnemy("s7missilejet",worldWidth()/2,200,{});window.port=s711Part(E,0).tip;window.slug=s711Shot(E,port,"slug",4);window.rocket=s711Shot(E,port,"missile",4);}')
 check(p.evaluate('!enemyOrdnanceCanIntercept(slug)&&enemyOrdnanceCanIntercept(rocket)'),'ordinary slugs remain unshootable; missiles retain interception')
 check(p.evaluate('slug._s711Owner===E&&Math.abs(slug.x-port.x)<.01&&Math.abs(slug.y-port.y)<.01'),'native turret socket and projectile owner retained')
 b.close()
result={'checks':checks,'rateSamples':samples,'errors':errors}
(W/'invariant-checks.json').write_text(json.dumps(result,indent=2),encoding='utf8')
assert not errors and all(c['ok']for c in checks)
