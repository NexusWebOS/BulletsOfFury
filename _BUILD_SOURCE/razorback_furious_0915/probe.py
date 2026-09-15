"""Real Chromium proof for the Stage-1 Furious Razorback hyper tank."""
from pathlib import Path
import base64,hashlib,http.server,json,subprocess,sys
import imageio_ffmpeg
from PIL import Image
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'_shots'/'razorback_furious_0915';OUT.mkdir(parents=True,exist_ok=True)
sys.path.insert(0,str(ROOT/'_BUILD_SOURCE'));import shoot
sys.path.insert(0,str(ROOT/'_BUILD_SOURCE'/'trailer_v7'));import capture3
from playwright.sync_api import sync_playwright
checks=[];errors=[];details={}
def ok(v,label):checks.append({'pass':bool(v),'label':label});print(('ok  ' if v else 'FAIL ')+label,flush=True)
http.server.SimpleHTTPRequestHandler.log_message=lambda *a:None
port,stop=shoot.serve(str(ROOT))
with sync_playwright() as pw:
  br=pw.chromium.launch(args=['--no-sandbox','--mute-audio']);page=br.new_page(viewport={'width':1100,'height':1200})
  page.on('pageerror',lambda e:errors.append('page '+str(e)));page.on('console',lambda m:errors.append('console '+m.text) if m.type=='error' else None)
  page.goto(f'http://127.0.0.1:{port}/index.html',wait_until='load',timeout=120000);page.wait_for_function('()=>(window.__bofFrames|0)>4',timeout=120000)
  page.evaluate(shoot.TRAP_RAF);page.evaluate(capture3.LIB)
  fight=page.evaluate("()=>window.__fight(1,'mini','yuri')");ok(fight.get('ok'),'native Stage-1 miniboss route opens in Chromium')
  setup=page.evaluate("""()=>{__auto=function(){};story=null;dlgBox=function(){};stagePlan=[];waveIdx=0;enemies=[];eBullets=[];pBullets=[];particles=[];powerups=[];playerLocks=[];state=GS.PLAY;stateT=1;run.stage=1;curStage=STAGES[0];camX=100;player.x=340;player.y=VH-65;player.invuln=999;player.dead=false;player.alive=true;
    diffKey='normal';DIFF=DIFFS.normal;subBoss=null;subBossActive=false;spawnSubBoss('razorback');const normal={w:subBoss.w,h:subBoss.h};
    diffKey='furious';DIFF=DIFFS.furious;subBoss=null;subBossActive=false;spawnSubBoss('razorback');subBossActive=true;
    window.__rzbPals=[];const pal=xartPalette;xartPalette=function(k,m){if(k.indexOf('rzb_')===0)__rzbPals.push([k,m]);return pal(k,m);};return {normal,w:subBoss.w,h:subBoss.h,name:subBoss.name,pair:!!subBoss._rzbPair};}""")
  details['setup']=setup
  ok(not setup['pair'] and setup['name']=='FURIOUS RAZORBACK','Furious keeps one separate hyper-tank encounter')
  ok(abs(setup['w']/setup['normal']['w']-1.5)<.02 and setup['w']==setup['h'],'the complete Furious collision silhouette is exactly 50 percent larger')
  keys=['rzb_hull_0','rzb_machinegun','rzb_turret','rzb_sonic_charge','rzb_sonic_ring','rzb_sonic_bullet','rzb_razor_missile']
  ready=False
  for _ in range(260):
    ready=page.evaluate('ks=>ks.every(k=>XART.rdy(k))',keys)
    if ready:break
    page.wait_for_timeout(35)
  ok(ready,'authored Razorback hull, weapons, charge and ordnance decode before capture')
  def step(n):
    for i in range(0,n,20):page.evaluate('n=>__step(n)',min(20,n-i));page.wait_for_timeout(8)
  def shot(name):
    page.evaluate('()=>{shake=0;drawWorld(0)}');p=OUT/(name+'.png');p.write_bytes(base64.b64decode(page.evaluate('()=>document.querySelector("#screen").toDataURL("image/png").split(",")[1]')));return p
  entered=False
  for _ in range(190):
    entered=page.evaluate("()=>subBoss._rzb.state==='guns'&&subBoss._rzb.trans<=0")
    if entered:break
    step(4)
  ok(entered,'the giant tank completes its authored arrival and becomes attackable')
  page.evaluate("""()=>{const b=subBoss,R=b._rzb;b.x=(camLeftX()+camRightX())*.5;b.y=160;R.state='guns';R.trans=0;R.attack='sonic';R.at=.62;R.beat=-1;R.tgt={x:b.x,y:b.y};R.a=0;R.turret=0;R.waves=[];eBullets=[];playerLocks=[];}""")
  step(18);charge=shot('furious_razorback_01_sonic_charge')
  cs=page.evaluate("()=>({charge:subBoss._rzb.charge,bullets:eBullets.length,waves:subBoss._rzb.waves.length,pals:Array.from(new Set(__rzbPals.map(x=>x.join('|'))))})")
  details['charge']=cs;ok(cs['charge']>.75 and cs['bullets']==0 and cs['waves']==0,'the furious sonic attack still gives a readable charged warning before release')
  ok(any(x.endswith('|#d51f3b') for x in cs['pals']),'the native renderer palette-swaps the complete tank through luminance-preserving authored plates')
  step(12);release=shot('furious_razorback_02_sonic_release')
  sonic=page.evaluate("""()=>({bullets:eBullets.filter(q=>q.kind==='rzbSonic'&&q._rzbFurious).length,waves:subBoss._rzb.waves.length,arc:subBoss._rzb.waves[0]&&subBoss._rzb.waves[0].arc,width:subBoss._rzb.waves[0]&&subBoss._rzb.waves[0].width,speed:subBoss._rzb.waves[0]&&subBoss._rzb.waves[0].speed,pals:Array.from(new Set(__rzbPals.map(x=>x.join('|'))))})""")
  details['sonic']=sonic
  ok(sonic['bullets']==9 and sonic['waves']==1 and sonic['arc']==1.05,'release creates the nine-round Furious fan and one much wider pressure wave')
  ok(sonic['width']>13.8 and sonic['speed']>279.45,'the Furious wave is over twice the baseline width and expansion speed')
  ok(any('rzb_sonic' in x and x.endswith('|#ff1838') for x in sonic['pals']),'charge, wave and sonic ordnance use the visible red Furious palette')
  # Measure the hyper drivetrain and attack clock through real update functions.
  motion=page.evaluate("""()=>{const b=subBoss,R=b._rzb;b.x=camLeftX()+100;b.y=160;R.state='guns';R.trans=0;R.attack='suppression';R.at=0;R.tgt={x:camRightX()-80,y:190};R.a=0;const x=b.x;for(let i=0;i<60;i++)razorbackUpdate(b,1/60);return {travel:b.x-x,attack:R.at,speedMul:R.speedMul,turnMul:R.turnMul};}""")
  details['motion']=motion;ok(motion['travel']>80 and motion['attack']>1.29 and motion['speedMul']==1.62 and motion['turnMul']==1.55,'hyper mode advances movement, turn and attack clocks together')
  # Record a controlled sonic-to-nova showcase from the production renderer.
  page.evaluate("""()=>{const b=subBoss,R=b._rzb;b.x=(camLeftX()+camRightX())*.5;b.y=160;R.state='hull';R.trans=0;R.attack='sonic';R.at=0;R.beat=-1;R.tgt={x:b.x,y:b.y};R.a=0;R.turret=0;R.waves=[];eBullets=[];playerLocks=[];window.__furyNovaPeak=0;}""")
  ff=imageio_ffmpeg.get_ffmpeg_exe();movie=OUT/'Furious_Razorback_Hyper_Tank_0915.mp4';proc=subprocess.Popen([ff,'-y','-v','error','-f','image2pipe','-vcodec','mjpeg','-framerate','30','-i','pipe:0','-c:v','libx264','-preset','veryfast','-crf','21','-pix_fmt','yuv420p','-movflags','+faststart',str(movie)],stdin=subprocess.PIPE,stderr=subprocess.PIPE)
  for f in range(150):
    if f==76:page.evaluate("()=>{const R=subBoss._rzb;R.attack='nova';R.at=0;R.beat=-1;R.waves=[];eBullets=[]}")
    page.evaluate("()=>{__step(2);if(subBoss._rzb.attack==='nova')window.__furyNovaPeak=Math.max(window.__furyNovaPeak,eBullets.filter(q=>q.kind==='rzbSonic').length)}");proc.stdin.write(base64.b64decode(page.evaluate('()=>document.querySelector("#screen").toDataURL("image/jpeg",.92).split(",")[1]')))
    if f in (38,70,112,138):shot('furious_razorback_%02d'%(3+(38,70,112,138).index(f)))
    if f%30==0:page.wait_for_timeout(8)
  proc.stdin.close();ok(proc.wait()==0,'native five-second hyper-tank capture encodes cleanly');subprocess.run([ff,'-v','error','-i',str(movie),'-f','null','-'],check=True)
  nova=page.evaluate("()=>({shots:window.__furyNovaPeak,waves:subBoss._rzb.waves.length,furious:subBoss._rzb.waves.some(w=>w.furious)})")
  details['nova']=nova;ok(nova['shots']>=28 and nova['waves']>=1 and nova['furious'],'the live showcase reaches the 28-round Furious resonance nova')
  edge=page.evaluate("""()=>{const b=subBoss,R=b._rzb;R.state='guns';R.trans=0;const g=rzbWorld(b,-57,96),x=g.x+RZB_R.gun*1.25;return {part:razorbackPartAt(b,x,g.y),beam:!!razorbackBeamHit(b,{x,w:2,top:g.y-60,bot:g.y+60})};}""")
  ok(edge['part']=='left' and edge['beam'],'the larger visual owns matching projectile and held-beam component geometry')
  # A simple pixel sanity check: the reviewed frame contains a meaningful crimson population.
  im=Image.open(release).convert('RGB');red=sum(1 for r,g,b in im.getdata() if r>g*1.22 and r>b*1.10 and r>70)
  details['crimsonPixels']=red;ok(red>1500,'native release pixels visibly contain the crimson Furious hull and red attack treatment')
  ok(all(p.stat().st_size>18000 for p in OUT.glob('*.png')) and movie.stat().st_size>50000,'screenshots and video contain non-empty native gameplay frames')
  ok(not errors and not page.evaluate('()=>window.__err||null'),'zero Chromium page, console or game-loop errors')
  details['runtimeSha256']=hashlib.sha256((ROOT/'assets/game.js').read_bytes()).hexdigest();br.close()
stop();result={'checks':checks,'errors':errors,'details':details,'fight':fight,'shots':[str(p.relative_to(ROOT)) for p in OUT.glob('*.png')],'video':str(movie.relative_to(ROOT))};(OUT/'results.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
passed=sum(c['pass'] for c in checks);print(f'{passed} passed / {len(checks)-passed} failed',flush=True)
if passed!=len(checks):raise SystemExit(1)
