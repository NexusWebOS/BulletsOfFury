"""Native Chromium pixels and timed attack checks for Mike's filmed boss motion.
Uses the real engine via shoot.py. Saves clips at normal simulated speed (15 FPS).
"""
from pathlib import Path
import sys,json,base64,subprocess
from PIL import Image,ImageDraw
from playwright.sync_api import sync_playwright
import imageio_ffmpeg

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'_BUILD_SOURCE'))
import shoot
OUT=ROOT/'_shots/boss_motion_1009';OUT.mkdir(parents=True,exist_ok=True)
checks=[];errors=[];shots=[];videos=[]
def check(name,ok,data=None):
 checks.append({'name':name,'pass':bool(ok),'data':data});print(('PASS ' if ok else 'FAIL ')+name,flush=True)
port,stop=shoot.serve(str(ROOT))
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(args=['--autoplay-policy=no-user-gesture-required'])
  p=br.new_page(viewport={'width':1280,'height':900});p.set_default_timeout(120000)
  p.on('pageerror',lambda e:errors.append(str(e)))
  p.on('console',lambda m:errors.append(m.text[:700]) if m.type=='error' or 'draw error' in m.text else None)
  p.on('response',lambda r:errors.append(f'HTTP {r.status} {r.url}') if r.status>=400 else None)
  p.goto(f'http://127.0.0.1:{port}/index.html',timeout=120000)
  p.wait_for_function('window.__bofFrames>4');p.evaluate(shoot.TRAP_RAF);p.mouse.click(700,500)
  p.add_script_tag(content=(ROOT/'_BUILD_SOURCE/balance_lab_1007.js').read_text())
  p.evaluate('()=>{bm9Warm(Object.keys(BM9_ART));fb1002Warm();r30Warm();av3Warm();s7mWarm();for(const k of Object.keys(MR27_ART))XART.rdy("mr27_"+k);}')
  p.wait_for_function('()=>Object.values(BM9_ART).flat().every(a=>XART.rdy(a.key))&&XART.rdy("r30_colossus_body")&&XART.rdy("s7m_body")',polling=50)
  def setup(c):
   p.evaluate('(c)=>BAL7.setup(c)',dict(pilot='yuri',diff='furious',seconds=60,fire=False,**c))
   for _ in range(1600):
    if p.evaluate('()=>{stageLoadTick();return stageLoadInfo(run.stage).ready;}'):break
    p.wait_for_timeout(25)
   else:raise RuntimeError('Stage loading did not finish')
   p.evaluate('()=>{BOFCinematicDirector.cancel();story=null;fb2Talk=null;player.invuln=1e9;shake=whiteBlast=0;enemies=[];eBullets=[];}')
  def shot(name,expr=None):
   if expr:p.evaluate(expr)
   p.evaluate('()=>{ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);}')
   q=base64.b64decode(p.evaluate('()=>cv.toDataURL().split(",")[1]'))
   (OUT/(name+'.png')).write_bytes(q);shots.append(name+'.png')
  def clip(name,seconds,expr):
   folder=OUT/name;folder.mkdir(exist_ok=True)
   for i in range(round(seconds*15)):
    p.evaluate('(code)=>{for(let i=0;i<4;i++){eval(code)}ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);}',expr)
    (folder/f'{i:04d}.png').write_bytes(base64.b64decode(p.evaluate('()=>cv.toDataURL().split(",")[1]')))
    p.wait_for_timeout(5)
   ff=imageio_ffmpeg.get_ffmpeg_exe()
   subprocess.run([ff,'-v','error','-y','-framerate','15','-i',str(folder/'%04d.png'),'-c:v','libx264','-crf','19','-pix_fmt','yuv420p',str(OUT/(name+'.mp4'))],check=True)
   videos.append(name+'.mp4')
  # Render all authored frames through the game's own drawImage context.
  p.evaluate('()=>{ctx.setTransform(1,0,0,1,0,0);ctx.fillStyle="#121925";ctx.fillRect(0,0,cv.width,cv.height);let i=0;for(const [name,frames] of Object.entries(BM9_ART)){for(const a of frames){const col=i%8,row=Math.floor(i/8),w=cv.width/8,h=cv.height/Object.keys(BM9_ART).length,k=Math.min((w-7)/a.w,(h-7)/a.h);ctx.drawImage(XART.get(a.key),col*w+(w-a.w*k)/2,row*h+(h-a.h*k)/2,a.w*k,a.h*k);i++;}}}')
  (OUT/'native-art-contact.png').write_bytes(base64.b64decode(p.evaluate('()=>cv.toDataURL().split(",")[1]')))
  check('64 authored cells load through XART',p.evaluate('Object.values(BM9_ART).flat().length===64'))
  check('Every affected boss stage queues its new frames before play',p.evaluate('()=>[3,4,5,7,8].every(n=>{stageLoadBegin(n,[]);return bm9StageNames(n).flatMap(name=>BM9_ART[name].map(a=>a.key)).every(k=>_stageLoads[n].keys.includes(k));})'))
  setup({'stage':5,'kind':'chromehammer'})
  p.evaluate('()=>{B.dead=true;B.dying=0;h3EndingStart(B);}')
  clip('hammer-death',18.0,'h3EndingTick(1/60);')
  check('Hammer acts and ruptures before cutaways',p.evaluate('()=>B._hammer.bm9Rupture&&H3.ending?.phase==="overhead"'),p.evaluate('BM9.events'))
  for f,t in enumerate([.2,.8,1.4,1.9,2.5,3.2,4.2,5.0]):
   p.evaluate('(t)=>{B.dying=t;H3.ending.engineDeath=t;H3.ending.phase="engineDeath";whiteBlast=0;}',t);shot('hammer-death-'+str(f))
  setup({'stage':5,'kind':'chromehammer'})
  p.evaluate('()=>{const h=B._hammer;h.mode="storm";h.charged=true;h.hammerDestroyed=false;h.stormHome={x:B.x,y:175};hammerStormTarget(B);hammerStormImpact(B);player.y=200;h.t=1;B.y=220;}')
  check('Spike preview and target stay at bottom',p.evaluate('()=>B._hammer.stormTarget.y===hammerStormFloorY()-12&&B._hammer.stormWaves.every(q=>q.height<PLAY.h*.4&&q.y===hammerStormFloorY())'))
  clip('hammer-counter',4.3,'updatePlay(1/60);')
  check('Escaping upward triggers authored counter',p.evaluate('()=>BM9.events.some(q=>q.event==="hammer-upper-counter")'))
  setup({'stage':8,'kind':'vileexistence','form':'home'})
  p.evaluate('()=>{B._r30.cd=0;B._r30.attack=null;j3State(B).attacks=0;B._r30.hf7=null;}')
  clip('dracodia-claws',5.1,'updatePlay(1/60);')
  check('Dracodia physical pattern emits no replacement volleys',p.evaluate('()=>eBullets.length===0&&BM9.events.some(q=>q.event==="dracodia-claw-combo"&&!q.low)'))
  check('Every Dracodia acting pose retains its attached head',p.evaluate('()=>{const old=B._r30.attack;const P={bm9:true,type:"bm9Swipe",ids:["left","right"],count:2,cycle:2.33,tell:1.30,t:0};B._r30.attack=P;let ok=true;try{for(const time of [.1,.3,.7,1.1,1.4,1.8,2.0]){P.t=time;ok=ok&&r30Parts(B).some(v=>v.p.id==="core"&&v.key.startsWith("bm9_dracodia_core_"));}}finally{B._r30.attack=old;}return ok;}'))
  p.evaluate('()=>{B._r30.attack=null;B._r30.cd=0;j3State(B).attacks=0;B.hp=B.maxhp*.45;}')
  p.evaluate('()=>aa5DraculaTick(B,1/60)')
  check('Below half of active form adds four warned strikes',p.evaluate('()=>B._r30.attack?.low&&B._r30.attack.count===4'))
  clip('dracodia-enraged',8.4,'updatePlay(1/60);')
  p.evaluate('()=>{B._r30.attack=null;B._r30.cd=0;j3State(B).attacks=0;aa5DraculaTick(B,1/60);const arm=B.parts.find(q=>q.id==="left");arm.destroyed=true;arm.hp=0;}')
  check('Broken Dracodia arm removed from physical rig',p.evaluate('()=>!r30Parts(B).some(v=>v.p.id==="left")'))
  setup({'stage':7,'kind':'sludgeemperor'})
  p.evaluate('()=>{s7mInit(B);B._s7mod._mission29IntroDone=true;B.x=worldWidth()/2;B.y=235;s7mSet(B,"swipeX");}')
  clip('warden-claws',2.0,'updatePlay(1/60);')
  check('Warden uses generated claw cells',p.evaluate('()=>s7mPose(B).filter(q=>q.id.startsWith("front")).every(q=>typeof q.cell==="string"&&q.cell.startsWith("bm9_spider_claws"))'))
  p.evaluate('()=>{s7mSet(B,"swipeL");B._s7mod.parts.find(q=>q.id==="frontL").hp=0;s7mTick(B,1/60);}')
  check('Destroyed Warden claw cancels its pending strike',p.evaluate('()=>B._s7mod.mode==="recover"'))
  setup({'stage':7,'kind':'sludgeemperor'})
  p.evaluate('()=>{s7mInit(B);B._s7mod._mission29IntroDone=true;B.x=worldWidth()/2;B.y=235;s7mSet(B,"jump");}')
  clip('warden-leap',3.8,'updatePlay(1/60);')
  check('Warden landing uses new gravel reel',p.evaluate('()=>BM9.events.some(q=>q.event==="warden-gravel-landing")&&BM9.draws.landing>0'))
  p.evaluate('()=>{B.y=190;eBullets=[];window.bm9BatteryRounds=0;s7mSet(B,"battery1009");}')
  clip('warden-battery',5.1,'updatePlay(1/60);bm9BatteryRounds=Math.max(bm9BatteryRounds,eBullets.filter(q=>q._s7modOwner===B).length);')
  check('Warden converges guns and alternates owned rounds',p.evaluate('()=>bm9BatteryRounds>0&&B._s7mod.mode!=="battery1009"'))
  for stage,kind,mini,mode in [(3,'cryospear',False,'rime-orbit1004k'),(3,'frostcruiser',True,'cryo-crosscut'),(4,'stormsovereign',False,'hc-relay1007')]:
   setup({'stage':stage,'kind':kind,'mini':mini})
   p.evaluate('(mode)=>{er26Init(B);mr27Init(B);if(B._s3Nuclear){B._s3Nuclear.introDone=true;B._er26.neutralOpening=false;B._er26.nuclearRevealed=true;}er26Set(B,mode);}',mode)
   start=p.evaluate('BM9.draws.turret_charge||0')
   clip('turrets-'+kind,4.3,'updatePlay(1/60);')
   check(kind+' turret charge renders',p.evaluate('(n)=>(BM9.draws.turret_charge||0)>n',start))
  check('Ordinary pellets stay non-interceptable',p.evaluate('()=>!enemyOrdnanceCanIntercept({kind:"mg"})&&!enemyOrdnanceCanIntercept({kind:"shell"})&&enemyOrdnanceCanIntercept({kind:"magma"})&&enemyOrdnanceCanIntercept({kind:"emissile"})'))
  br.close()
finally:stop()
check('No page, console or asset errors',not errors,errors)
result={'passed':sum(c['pass'] for c in checks),'failed':[c for c in checks if not c['pass']],'errors':errors,'checks':checks,'shots':shots,'videos':videos}
(OUT/'verification.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in result.items() if k not in ('checks','shots','videos')}),flush=True)
if result['failed'] or errors:sys.exit(1)
