"""Native Chromium pixels and real damage paths; no mock assets/context."""
from pathlib import Path
import sys,json,base64,hashlib,http.server,subprocess
import imageio_ffmpeg
http.server.SimpleHTTPRequestHandler.log_message=lambda *a:None
R=Path(__file__).resolve().parents[2];O=R/'_shots/projectile_glow_0914'
sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
sys.path.insert(0,str(R/'_BUILD_SOURCE/trailer_v7'));import capture3
from playwright.sync_api import sync_playwright
port,stop=shoot.serve(str(R));errors=[];checks=[]
def ok(v,n):
 checks.append({'pass':bool(v),'label':n});print(('ok 'if v else'FAIL ')+n,flush=True)
with sync_playwright()as p:
 b=p.chromium.launch(args=['--no-sandbox','--mute-audio']);pg=b.new_page(viewport={'width':1100,'height':1200})
 pg.on('pageerror',lambda e:errors.append(str(e)));pg.on('console',lambda m:errors.append(m.text)if m.type=='error'else None)
 pg.goto('http://127.0.0.1:%d/index.html'%port,wait_until='load',timeout=120000);pg.wait_for_function('()=>(window.__bofFrames|0)>4',timeout=120000)
 pg.evaluate(shoot.TRAP_RAF);pg.evaluate(capture3.LIB)
 pg.evaluate('''()=>{__auto=function(){};run.mode='arcade';run.pilot='cole';pilotIndex=PILOTS.findIndex(p=>p.key==='cole');beginStage(5);furyShipWarm();XART._touch('dlg_rect_0914');for(let i=0;i<6;i++)XART.rdy('np5_ast_'+i);for(const st of ['idle','damaged','critical'])XART.rdy('ns9c_sm_'+st);msgFaceUse('dialogue');for(const p of PILOTS)pilotPortrait(p.key,'idle');}''')
 pg.wait_for_function('()=>XART.rdy("dlg_rect_0914")&&furyShipReady()&&Array.from({length:6},(_,i)=>XART.rdy("np5_ast_"+i)).every(Boolean)',timeout=120000)
 for _ in range(10):pg.evaluate('()=>__step(3)');pg.wait_for_timeout(20)
 def shot(name):
  (O/(name+'.png')).write_bytes(base64.b64decode(pg.evaluate('()=>document.querySelector("#screen").toDataURL().split(",")[1]')))
 pg.evaluate('''()=>{ctx.save();ctx.setTransform(document.querySelector('#screen').width/VW,0,0,document.querySelector('#screen').height/VH,0,0);ctx.fillStyle='#172031';ctx.fillRect(0,0,VW,VH);for(let i=0;i<6;i++){const im=XART.get('np5_ast_'+i);ctx.drawImage(im,15+i%3*155,12+Math.floor(i/3)*180,140,140);}ctx.restore();}''');shot('asteroid_art')
 pg.evaluate("""()=>{for(const k of ['cfx_stage5_alien_projectiles_v2','cfx_stage2_volcanic_projectiles'])XART.rdy(k);}""")
 pg.wait_for_function("()=>XART.rdy('cfx_stage5_alien_projectiles_v2')&&XART.rdy('cfx_stage2_volcanic_projectiles')",timeout=120000)
 kinds=pg.evaluate("()=>Object.keys(CFX_STAGE_PROJECTILE).filter(k=>/^s5/.test(k)||k==='s2slag'||k==='s2mine')")
 results=pg.evaluate("""kinds=>{const out=[];for(const kind of kinds){const indices=[],base=[],pixels=[];const saved=combatAtlasDraw;for(const t of [0,.09,.18,.27,.36,.45,.54,.63]){ctx.save();ctx.setTransform(1,0,0,1,0,0);ctx.clearRect(0,0,960,1024);combatAtlasDraw=function(k,c,r,i,x,y,w,h,o){indices.push(i);if(!o||!o.blend)base.push([i,w,h]);return saved.apply(this,arguments);};drawCfxStageProjectile({kind,x:240,y:240,vx:0,vy:3,t});combatAtlasDraw=saved;const d=ctx.getImageData(185,185,110,110).data;let sum=0;for(let i=0;i<d.length;i+=4)sum+=d[i]+d[i+1]+d[i+2];pixels.push(sum);ctx.restore();}out.push({kind,indices:[...new Set(indices)],sizes:[...new Set(base.map(q=>q.slice(1).join(',')))],pixelSums:pixels});}return out;}""",kinds)
 for r in results:
  ok(len(r['indices'])==1 and len(r['sizes'])==1,r['kind']+' uses one source cell and constant size')
  ok(len(set(r['pixelSums']))>=3,r['kind']+' has visible stepped pixel lighting')
 # Full-source native draw comparison; all columns here use the SAME sprite and changing glow.
 pg.evaluate("""kinds=>{ctx.save();ctx.setTransform(2,0,0,2,0,0);ctx.fillStyle='#142335';ctx.fillRect(0,0,VW,VH);for(let row=0;row<kinds.length;row++){const kind=kinds[row];for(let col=0;col<4;col++)drawCfxStageProjectile({kind,x:155+col*82,y:40+row*53,vx:0,vy:3,t:col/12});ctx.fillStyle='#ffffff';ctx.font='11px monospace';ctx.fillText(kind,12,44+row*53);}ctx.restore();}""",kinds);shot('fixed_frame_glow')
 # Recreate the screenshot's diagonal three-shot volley in the actual stage renderer.
 pg.evaluate("""()=>{run.pilot='cole';pilotIndex=PILOTS.findIndex(p=>p.key==='cole');beginStage(5);setState(GS.PLAY);run.gravityShipReady=true;gravityMode.phase='active';player.reset();player.invuln=0;playerHit=function(){};story=null;l5Rocks=[];l5RockT=100;enemies=[];eBullets=[];pBullets=[];__auto=function(){};}""")
 ff=imageio_ffmpeg.get_ffmpeg_exe();movie=O/'Static_Projectile_Glow_0914.mp4'
 enc=subprocess.Popen([ff,'-y','-v','error','-f','image2pipe','-vcodec','mjpeg','-framerate','30','-i','pipe:0','-c:v','libx264','-preset','veryfast','-crf','19','-pix_fmt','yuv420p','-movflags','+faststart',str(movie)],stdin=subprocess.PIPE,stderr=subprocess.PIPE)
 for f in range(180):
  pg.evaluate("""f=>{if(f%60===0){for(let i=0;i<3;i++)spaceBossShot(300+i*44,70+i*15,Math.PI*.70,2.3,'s5fracture',{silent:true});for(let i=0;i<2;i++)spaceBossShot(75+i*42,65,Math.PI/2,2.0,'s5null',{silent:true});}__step(2);}""",f)
  enc.stdin.write(base64.b64decode(pg.evaluate('()=>document.querySelector("#screen").toDataURL("image/jpeg",.92).split(",")[1]')))
  if f==45:shot('space_in_game')
 enc.stdin.close();err=enc.stderr.read();assert enc.wait()==0,err
 subprocess.run([ff,'-v','error','-i',str(movie),'-f','null','-'],check=True)
 pg.evaluate("""()=>{beginStage(2);setState(GS.PLAY);player.reset();playerHit=function(){};story=null;enemies=[];eBullets=[];pBullets=[];for(let i=0;i<3;i++)eBullets.push({kind:'s2slag',x:125+i*110,y:160+i*40,vx:0,vy:2,w:18,h:18,t:0});}""")
 for _ in range(12):pg.evaluate('()=>__step(3)');pg.wait_for_timeout(10)
 shot('lava_saws_in_game')
 ok(not errors and not pg.evaluate('()=>window.__err||null'),'zero page, console and game-loop errors')
 data={'checks':checks,'errors':errors,'projectiles':results,'runtimeSha256':hashlib.sha256((R/'assets/game.js').read_bytes()).hexdigest(),'video':str(movie),'videoSeconds':6,'videoDecodeExitCode':0,'fixture':'Actual game renderer and update loop, scripted projectile spawns and capture-only invincibility; silent video.'}
 (O/'native.json').write_text(json.dumps(data,indent=2)+'\n');b.close()
stop()
assert all(c['pass']for c in checks)
