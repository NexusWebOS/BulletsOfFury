"""Real Chromium stage-4 visual audit and Furnace shield lifecycle verification."""
from pathlib import Path
import sys,json,base64,hashlib,http.server,subprocess
import imageio_ffmpeg
R=Path(__file__).resolve().parents[2];O=R/'_shots/razorback_speed_0914'
sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
sys.path.insert(0,str(R/'_BUILD_SOURCE/trailer_v7'));import capture3
from playwright.sync_api import sync_playwright
http.server.SimpleHTTPRequestHandler.log_message=lambda *a:None
port,stop=shoot.serve(str(R));checks=[];errors=[];details={}
def check(v,label):checks.append({'pass':bool(v),'label':label});print(('ok 'if v else'FAIL ')+label,flush=True)
with sync_playwright()as p:
 b=p.chromium.launch(args=['--no-sandbox','--mute-audio','--autoplay-policy=no-user-gesture-required']);pg=b.new_page(viewport={'width':1100,'height':1200})
 pg.on('pageerror',lambda e:errors.append(str(e)));pg.on('console',lambda m:errors.append(m.text)if m.type=='error'else None)
 pg.goto('http://127.0.0.1:%d/index.html'%port,wait_until='load',timeout=120000);pg.wait_for_function('()=>(window.__bofFrames|0)>4',timeout=120000)
 pg.evaluate(shoot.TRAP_RAF);pg.evaluate(capture3.LIB)
 def step(n):
  for i in range(0,n,20):pg.evaluate('n=>__step(n)',min(20,n-i));pg.wait_for_timeout(10)
 def shot(name):
  (O/(name+'.png')).write_bytes(base64.b64decode(pg.evaluate('()=>document.querySelector("#screen").toDataURL().split(",")[1]')))
 def fight(stage,role):
  pg.evaluate('a=>{__auto=function(){};__fight(a[0],a[1],"yuri");stagePlan=[];enemies=[];story=null;playerHit=function(){};Object.keys(Input.keys).forEach(k=>Input.keys[k]=false);}',[stage,role]);step(2)
  for _ in range(240):
   if pg.evaluate('role=>!!(role==="mini"?subBoss:boss)',role):break
   step(4);pg.wait_for_timeout(20)
  assert pg.evaluate('role=>!!(role==="mini"?subBoss:boss)',role), 'fight target did not spawn'
 def movie(name,n,snaps):
  ff=imageio_ffmpeg.get_ffmpeg_exe();path=O/(name+'.mp4');q=subprocess.Popen([ff,'-y','-v','error','-f','image2pipe','-vcodec','mjpeg','-framerate','30','-i','pipe:0','-c:v','libx264','-preset','veryfast','-crf','22','-pix_fmt','yuv420p','-movflags','+faststart',str(path)],stdin=subprocess.PIPE,stderr=subprocess.PIPE)
  for f in range(n*30):
   pg.evaluate('()=>__step(2)')
   q.stdin.write(base64.b64decode(pg.evaluate('()=>document.querySelector("#screen").toDataURL("image/jpeg",.90).split(",")[1]')))
   if f in snaps:shot(snaps[f])
   if f%30==0:pg.wait_for_timeout(10)
  q.stdin.close();err=q.stderr.read();assert q.wait()==0,err;subprocess.run([ff,'-v','error','-i',str(path),'-f','null','-'],check=True)

 fight(1,'mini');pg.wait_for_function('()=>XART.rdy("rzb_sonic_ring")&&XART.rdy("rzb_sonic_bullet")&&XART.rdy("rzb_razor_missile")',timeout=120000)
 for _ in range(180):
  if pg.evaluate('()=>subBoss._rzb.state!=="arrival"&&subBoss.y>70'):break
  step(4)
 tuning=pg.evaluate("""()=>{function travel(attack){const q={x:0,y:0,_rzb:{tgt:{x:1000,y:0},a:0,at:1.5,attack,travel:{left:0,right:0}}};for(let i=0;i<60;i++)razorbackMove(q,1/60);return {distance:q.x,angle:q._rzb.a};}return {cruise:travel('suppression'),ram:travel('ram'),bullet:rzbPxFrame(380),sonic:rzbPxFrame(240),wave:180*RZB_S*RZB_WFAST,nova:200*RZB_S*RZB_WFAST};}""");details['tuning']=tuning
 check(abs(tuning['cruise']['distance']-92*.46*1.3)<.01 and abs(tuning['ram']['distance']-330*.46*1.3)<.01,'native movement covers 30 percent more ground in both cruise and ram')
 check(abs(tuning['bullet']/(380*.46*1.35/60)-1.2)<.001 and abs(tuning['sonic']/(240*.46*1.35/60)-1.2)<.001,'machine and sonic projectile launch speeds are 20 percent faster')
 check(abs(tuning['wave']/(180*.46*1.35)-1.25)<.001 and abs(tuning['nova']/(200*.46*1.35)-1.25)<.001,'directional and nova wave expansion are 25 percent faster')
 pg.evaluate("""()=>{window.__rounds=[];window.__pressure=[];const shot=rzbShot;rzbShot=function(){const n=eBullets.length;shot.apply(this,arguments);for(let i=n;i<eBullets.length;i++)__rounds.push({t:subBoss._rzb.at,kind:eBullets[i].kind,speed:Math.hypot(eBullets[i].vx,eBullets[i].vy)});};const wave=razorbackWaveDraw;razorbackWaveDraw=function(w){__pressure.push({r:w.r,speed:w.speed});return wave.apply(this,arguments);};}""")
 pg.evaluate("()=>{subBoss.x=worldWidth()/2-70;subBoss.y=130;subBoss._rzb.state='guns';subBoss._rzb.trans=0;subBoss._rzb.attack='suppression';subBoss._rzb.at=0;subBoss._rzb.tgt={x:worldWidth()/2+100,y:170};subBoss._rzb.mgBeat=-1;}")
 movie('Razorback_Faster_Guns_0914',6,{30:'moving_gun_burst',105:'sonic_charge',163:'sonic_release'})
 # Controlled sonic attack: compare staying in the lane with a real keyboard sidestep after release.
 def sonic():
  pg.evaluate("""()=>{const b=subBoss,R=b._rzb;b.x=worldWidth()/2;b.y=130;R.state='turret';R.trans=0;R.attack='sonic';R.at=0;R.beat=-1;R.turret=0;R.a=0;R.waves=[];R.tgt={x:b.x,y:b.y};R.pools.left=R.pools.right=0;R.ppx=b.x;R.pvx=0;player.x=b.x;player.y=410;player.invuln=0;player.dead=false;Input.mouse.active=false;Input.mouse.down=false;Object.keys(Input.keys).forEach(k=>Input.keys[k]=false);eBullets=[];pBullets=[];playerLocks=[];window.__hits=0;playerHit=function(){__hits++;};__rounds=[];}""")
 sonic();step(66)
 check(pg.evaluate('()=>!__rounds.length&&!subBoss._rzb.waves.length&&subBoss._rzb.charge>.8'),'the full 1.2-second sonic warning remains before any launch')
 shot('full_sonic_warning');step(8);shot('sonic_fan')
 check(pg.evaluate('()=>__rounds.length===5&&subBoss._rzb.waves.length===1'),'sonic release keeps the five-shot spread and single directional wave')
 radial=pg.evaluate('()=>({r:subBoss._rzb.waves[0].r,v:subBoss._rzb.waves[0].speed})');step(6);radial2=pg.evaluate('()=>subBoss._rzb.waves[0].r')
 check(abs(radial2-radial['r']-radial['v']*.1)<.01,'pressure-wave radius advances at the faster speed through the real update loop')
 step(86);standing=pg.evaluate('()=>__hits');check(standing>0,'standing in the released sonic lane reaches the player-hit route')
 sonic();step(74);pg.evaluate("()=>Input.keys.arrowleft=true");step(40);pg.evaluate("()=>Input.keys.arrowleft=false");step(70)
 dodge=pg.evaluate('()=>({hits:__hits,x:player.x,tankX:subBoss.x})');details['dodge']={'standingHits':standing,**dodge};shot('sonic_sidestep')
 check(dodge['hits']==0 and dodge['x']<dodge['tankX']-90,'a keyboard sidestep after sonic release escapes the faster wave and fan')
 # Record the same reactive sidestep, with capture-only hit counting.
 sonic();pg.evaluate("""()=>{__auto=function(){Input.keys.arrowleft=subBoss._rzb.at>=1.24&&player.x>worldWidth()/2-160;};}""")
 movie('Razorback_Sonic_Dodge_0914',3,{18:'sonic_windup',41:'sonic_committed',78:'sonic_evaded'})
 pg.evaluate("()=>{__auto=function(){};Input.keys.arrowleft=false;eBullets=[];pBullets=[];subBoss._rzb.trans=99;rzbMissile(subBoss,{x:worldWidth()/2,y:100},0);window.__missile=eBullets[eBullets.length-1];window.__launch=__missile.spd;}");step(30)
 missile=pg.evaluate('()=>({start:__launch,speed:__missile.spd,cap:__missile._maxspd,shootable:__missile._shootable,alive:!__missile.dead})');details['missile']=missile
 check(missile['shootable']and abs(missile['start']-160*.46*1.62/60)<.001 and missile['speed']>missile['start']and missile['speed']<=missile['cap'],'Razor rockets stay shootable and accelerate from their faster launch within the new cap')
 check(pg.evaluate('()=>__alog.snd.some(q=>q[1]==="razorbackCharge")&&__alog.snd.some(q=>q[1]==="razorbackPressure")&&__alog.snd.some(q=>q[1]==="razorbackGun")'),'gun, charge and sonic release sounds remain wired during the live fight')
 check(pg.evaluate('()=>__pressure.length>0'),'authored sonic pressure-ring art renders in the real game')
 check(not errors and not pg.evaluate('()=>window.__err||null'),'no page, console or game-loop errors')
 details['runtimeSha256']=hashlib.sha256((R/'assets/game.js').read_bytes()).hexdigest();(O/'native.json').write_text(json.dumps({'checks':checks,'errors':errors,'details':details,'fixture':'Real Chromium debug fight with controlled phases, real keyboard movement and hit-route counting. Silent videos; no claim of a full difficulty balance pass.'},indent=2)+'\n');b.close()
stop();assert all(c['pass']for c in checks)
