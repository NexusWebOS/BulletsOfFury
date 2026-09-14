"""Real Chromium Frost Cruiser difficulty variant verification."""
from pathlib import Path
import sys,json,base64,hashlib,http.server,subprocess
import imageio_ffmpeg
R=Path(__file__).resolve().parents[2];O=R/'_shots/frost_nose_laser_0914'
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


 fight(3,'mini');step(200)
 pg.evaluate("()=>{XART._touch('fllaser_0');player.invuln=999;}")
 pg.wait_for_function("()=>XART.rdy('fllaser_0')&&XART.rdy('nsb_frost_cruiser')",timeout=120000)
 pg.evaluate("""()=>{window.__sounds={laser:0,missile:0};for(const [k,tag]of [['enemyHeavyLaser','laser'],['missile','missile']]){const f=Audio.SFX[k];Audio.SFX[k]=function(){__sounds[tag]++;if(f)return f.apply(this,arguments);};}window.__draws=[];const old=frostNoseLaserDraw,draw=ctx.drawImage;window.__drawingLaser=false;frostNoseLaserDraw=function(q){__drawingLaser=true;try{return old(q);}finally{__drawingLaser=false;}};ctx.drawImage=function(){if(__drawingLaser)__draws.push(Array.from(arguments).slice(1));return draw.apply(this,arguments);};}""")
 def reset():
  pg.evaluate("""()=>{eBullets=[];pBullets=[];enemies=[];powerups=[];stagePlan=[];story=null;thaw=null;const b=subBoss;b.x=240;b.y=100;b._drawY=100;b._sba=null;b._sbaKick=0;b._sbaHitT=0;b._sbaPhaseT=0;b._jc.rot=0;b._jc.sample=0;b._jc.shot=0;player.x=240;player.y=400;player.invuln=999;shake=0;}""")
 reset()
 origins=pg.evaluate("""()=>{const b=subBoss,C=shipBossMount(b,'C');jungleCruiserNoseRound(b);const q=eBullets[0],a=Math.atan2(q.vy,q.vx);return {C,kind:q.kind,w:q.w,h:q.h,rearX:q.x-Math.cos(a)*q.h/2,rearY:q.y-Math.sin(a)*q.h/2,homing:!!q.homing,shootable:!!q._shootable};}""");details['nose']=origins
 check(origins['kind']=='frostNoseLaser'and origins['w']==24 and origins['h']==112,'nose emits wide 24 x 112 Falva-family laser bolts')
 check(abs(origins['rearX']-origins['C']['x'])<.001 and abs(origins['rearY']-origins['C']['y'])<.001,'the trailing end of the bolt begins at the physical nose mount')
 check(not origins['homing']and not origins['shootable'],'nose laser is committed energy, with no missile homing or interception behavior')
 ports=pg.evaluate("""()=>{eBullets=[];return ['L','R'].map(slot=>{const m=shipBossMount(subBoss,slot),n=eBullets.length;jungleCruiserPodPair(subBoss,slot,false);return {slot,shots:eBullets.slice(n).map(q=>({kind:q.kind,dx:q.x-m.x,dy:q.y-m.y,homing:q.homing}))};});}""");details['ports']=ports
 check(all(len(p['shots'])==2 and all(q['kind']=='emissile'and q['homing']and abs(q['dx'])==4 and q['dy']==2 for q in p['shots'])for p in ports),'both wing turrets retain their physical paired missile launches')
 check(pg.evaluate('()=>__sounds.laser===1&&__sounds.missile===2'),'nose uses the laser sound and wing pods retain missile reports')
 check(pg.evaluate("()=>{const b={_ship:'junglecruiser',x:240,y:100,w:168,h:168,t:0};jungleCruiserInit(b);jungleCruiserNoseRound(b);return eBullets[eBullets.length-1].kind==='mg'&&jungleCruiserNoseGap(b)===JC_GUN_GAP;}"),'shared Jungle Cruiser keeps its existing nose weapon and cadence')
 pixels=pg.evaluate("""()=>{const im=XART.get(FROST_NOSE_LASER.key),v=frostNoseLaserPlate(),c=document.createElement('canvas');c.width=v.width;c.height=v.height;const g=c.getContext('2d');g.drawImage(im,0,0);const a=g.getImageData(0,0,c.width,c.height).data,b=v.getContext('2d').getImageData(0,0,c.width,c.height).data;let alpha=0,blue=0,visible=0,dark=0;for(let i=0;i<a.length;i+=4){if(a[i+3]!==b[i+3])alpha++;if(!a[i+3])continue;visible++;if(b[i+2]>b[i+1]&&b[i+1]>b[i])blue++;if(b[i]+b[i+1]+b[i+2]<100)dark++;}return {alpha,blue,visible,dark};}""");details['palette']=pixels
 check(pixels['alpha']==0 and pixels['blue']==pixels['visible']and pixels['dark']>0,'Falva sprite silhouette survives the black/blue palette with no pink pixels')
 pulse=pg.evaluate("""()=>{const sums=[];__draws=[];for(let n=0;n<4;n++){ctx.save();ctx.setTransform(1,0,0,1,0,0);ctx.clearRect(0,0,960,1024);frostNoseLaserDraw({x:100,y:100,w:24,h:112,vx:0,vy:5.8,t:n/12});const d=ctx.getImageData(75,35,50,130).data;let sum=0;for(let i=0;i<d.length;i+=4)sum+=d[i]+d[i+1]+d[i+2];sums.push(sum);ctx.restore();}return {sums,sizes:[...new Set(__draws.map(d=>d.slice(-2).join(',')))]};}""");details['glow']=pulse
 check(len(set(pulse['sums']))>=3 and pulse['sizes']==['24,112'],'pixel lighting visibly animates while every draw keeps a fixed silhouette and size')
 pg.evaluate("""()=>{ctx.save();ctx.setTransform(2,0,0,2,0,0);ctx.fillStyle='#152336';ctx.fillRect(0,0,VW,VH);for(let n=0;n<4;n++){frostNoseLaserDraw({x:85+n*100,y:195,w:24,h:112,vx:0,vy:5.8,t:n/12});msgText('GLOW '+(n+1),85+n*100,290,12,'#ffffff',1,1);}ctx.restore();}""");shot('beam_glow')
 reset();pg.evaluate("""()=>{jungleCruiserSetState(subBoss,'gunSlide');subBoss.x=120;subBoss.y=shipBossStationY(subBoss);subBoss._jc.slideTarget=380;__noseEmissions=[];const fire=jungleCruiserNoseRound;jungleCruiserNoseRound=function(b){const n=eBullets.length;fire(b);for(const q of eBullets.slice(n))__noseEmissions.push({kind:q.kind,t:b._jc.t});};}""");step(60)
 emissions=pg.evaluate('()=>__noseEmissions');details['oneSecondEmissions']=emissions
 check(2<=len(emissions)<=4 and all(x['kind']=='frostNoseLaser'for x in emissions),'real slide director emits spaced laser bolts instead of the rapid-gun stream')
 shot('normal_slide')
 # Isolate one live projectile to verify its committed trajectory and actual player-hit route.
 pg.evaluate("""()=>{window.__savedBoss=subBoss;subBoss=null;subBossActive=false;eBullets=[{kind:'frostNoseLaser',_frostNoseLaser:true,x:200,y:130,vx:2,vy:4,w:24,h:112,t:0}];player.x=380;player.y=400;window.__q=eBullets[0];}""");step(18)
 check(pg.evaluate('()=>__q.vx===2&&__q.vy===4&&Math.abs(__q.x-236)<.01&&Math.abs(__q.y-202)<.01'),'moving the player never bends or re-homes a released laser')
 hits=[]
 for dx,dy in [(0,40),(38,0)]:
  pg.evaluate("""p=>{window.__hit=0;playerHit=function(){__hit++;};player.x=240+p[0];player.y=300+p[1];player.invuln=0;player.dead=false;eBullets=[{kind:'frostNoseLaser',_frostNoseLaser:true,x:240,y:299,vx:0,vy:1,w:24,h:112,t:0}];}""",[dx,dy]);step(1);hits.append(pg.evaluate('()=>__hit'))
 check(hits[0]>0 and hits[1]==0,'real collision hits the long shaft and leaves a clear lane beside its glow')
 check(pg.evaluate("()=>{const q={x:200,y:200,vx:4,vy:4,w:24,h:112};return frostNoseLaserHit(q,{x:228,y:228},9,10)&&!frostNoseLaserHit(q,{x:228,y:172},9,10);}"),'diagonal collision rotates with the laser rather than using a vertical box')
 pg.evaluate("()=>{player.invuln=999;eBullets=[{kind:'frostNoseLaser',_frostNoseLaser:true,x:240,y:VH+25,vx:0,vy:1,w:24,h:112,t:0}];}");step(1);visible=pg.evaluate('()=>eBullets.length===1');step(40)
 check(visible and pg.evaluate('()=>eBullets.length===0'),'long bolts remain until their tail leaves the screen and are then removed')
 pg.evaluate("()=>{diffKey='hard';}");fight(3,'mini');step(200);reset()
 check(pg.evaluate("()=>subBoss._jc.hardVariant&&Math.abs(subBoss.w-226.8)<.001&&jungleCruiserNoseGap(subBoss)===.34"),'Hard enlarged hull uses the same corrected nose weapon')
 pg.evaluate("""()=>{playerHit=function(){};player.invuln=0;thaw=null;jungleCruiserSetState(subBoss,'missiles');subBoss.x=240;subBoss.y=shipBossStationY(subBoss);player.x=240;player.y=410;}""")
 movie('Frost_Cruiser_Nose_Lasers_0914',9,{35:'wing_missiles',95:'hard_lasers',135:'hard_slide'})
 check(not errors and not pg.evaluate('()=>window.__err||null'),'zero page, console and game-loop errors')
 details['runtimeSha256']=hashlib.sha256((R/'assets/game.js').read_bytes()).hexdigest();(O/'native.json').write_text(json.dumps({'checks':checks,'errors':errors,'details':details,'fixture':'Real stage-3 mini debug fights, controlled phases and player-hit interception. Nine-second silent gameplay recording; decode verified.'},indent=2)+'\n');b.close()
stop();assert all(c['pass']for c in checks)
