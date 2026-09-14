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


 pg.evaluate("()=>{for(let i=0;i<8;i++)XART._touch('fllaser_'+i);}")
 pg.wait_for_function("()=>Array.from({length:8},(_,i)=>XART.rdy('fllaser_'+i)).every(Boolean)",timeout=120000)
 pg.evaluate("()=>{ctx.save();ctx.setTransform(2,0,0,2,0,0);ctx.fillStyle='#172333';ctx.fillRect(0,0,VW,VH);for(let i=0;i<8;i++){const im=XART.get('fllaser_'+i);ctx.drawImage(im,20+i*58,100,48,250);msgText(String(i),44+i*58,380,16,'#ffffff',1,1);}ctx.restore();}")
 shot('falva_source');print(pg.evaluate("()=>Array.from({length:8},(_,i)=>{const im=XART.get('fllaser_'+i);return {key:'fllaser_'+i,w:im.naturalWidth||im.width,h:im.naturalHeight||im.height};})"));b.close()
stop()
