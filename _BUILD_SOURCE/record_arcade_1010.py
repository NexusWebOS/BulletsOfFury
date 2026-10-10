"""Record actual engine frames at 30 FPS; stream PNGs so no frame folder grows."""
from pathlib import Path
import sys,base64,subprocess,json
from playwright.sync_api import sync_playwright
import imageio_ffmpeg
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'_BUILD_SOURCE'));import shoot
OUT=ROOT/'_shots/arcade_finish_1010';OUT.mkdir(exist_ok=True);port,stop=shoot.serve(str(ROOT));errors=[]
def record(p,name,seconds,tick,shots=()):
 ff=subprocess.Popen([imageio_ffmpeg.get_ffmpeg_exe(),'-v','error','-y','-f','image2pipe','-framerate','30','-i','-','-an','-c:v','libx264','-crf','19','-pix_fmt','yuv420p',str(OUT/(name+'.mp4'))],stdin=subprocess.PIPE)
 try:
  for i in range(round(seconds*30)):
   p.evaluate('(c)=>{for(let i=0;i<2;i++)eval(c);ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);}',tick)
   raw=base64.b64decode(p.evaluate('()=>cv.toDataURL().split(",")[1]'));ff.stdin.write(raw)
   if i in shots:(OUT/(name+'-'+str(i)+'.png')).write_bytes(raw)
   p.wait_for_timeout(2)
 finally:ff.stdin.close();ff.wait()
 if ff.returncode:raise RuntimeError('Encoder failed')
 print('Recorded '+name,flush=True)
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(args=['--autoplay-policy=no-user-gesture-required']);p=br.new_page(viewport={'width':1280,'height':900});p.set_default_timeout(120000)
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:700]) if m.type=='error' or 'draw error' in m.text else None)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>4');p.evaluate(shoot.TRAP_RAF);p.wait_for_timeout(60)
  p.add_script_tag(content=(ROOT/'_BUILD_SOURCE/balance_lab_1007.js').read_text())
  def waitstage(n):
   for _ in range(2000):
    if p.evaluate('(n)=>{stageLoadTick();return stageLoadInfo(n).ready;}',n):return
    p.wait_for_timeout(20)
   raise RuntimeError('stage load timeout')
  for n in [2,3]:
   p.evaluate('(n)=>{diffKey="furious";DIFF=difficultyForRun("arcade",diffKey);run.mode="arcade";beginStage(n);setState(GS.PLAY);stagePlan=[];waveIdx=999;spawnClock=9999;story=null;BOFCinematicDirector.cancel();player.reset();player.invuln=1e9;player.x=worldWidth()/2;player.y=VH-90;camX=clamp(player.x-VW/2,0,worldWidth()-VW);enemies=[];boss=null;bossActive=false;subBoss=null;subBossActive=false;subBossDone=true;subBossTriggered=true;spawnEnemy(n===2?"ac10firejet":"ac10icejet",player.x,-20);for(let i=-1;i<=1;i++)spawnEnemy(n===2?"disc":"s3mine",player.x+i*80,-100-i*25);}',n);waitstage(n)
   record(p,'stage'+str(n)+'-arcade',12,'updatePlay(1/60);BOFCinematicDirector.cancel();story=null;thaw=null;',shots=[70,150,250])
  p.evaluate('()=>BAL7.setup({stage:5,kind:"chromehammer",pilot:"yuri",diff:"furious",fire:false,seconds:60})');waitstage(5)
  p.evaluate('()=>{af10Warm();BOFCinematicDirector.cancel();story=null;B.dead=true;B.dying=0;h3EndingStart(B);}')
  p.wait_for_function('af10Ready()',polling=50);record(p,'hammer-32-frame-farewell',22,'h3EndingTick(1/60);',shots=[320,350,390,420,455])
  page=br.new_page(viewport={'width':1280,'height':1000});page.on('pageerror',lambda e:errors.append('preview '+str(e)));page.goto(f'http://127.0.0.1:{port}/docs/previews/neo_geo_stage1_1010/index.html');f=page.frames[1];f.wait_for_function('window.PV10&&PV10.ready()',polling=50);f.evaluate(shoot.TRAP_RAF);f.wait_for_timeout(60)
  for unit in ['razorback','furious_razorback','overlord']:
   page.locator('[data-unit="'+unit+'"]').click();f.wait_for_function('PV10.ready()',polling=50);record(f,unit+'-modular',4,'updatePlay(1/60);',shots=[15]);
  page.screenshot(path=str(OUT/'preview-ready.png'));br.close()
finally:stop()
(OUT/'recording.json').write_text(json.dumps({'fps':30,'errors':errors},indent=2)+'\n');print(json.dumps({'errors':errors}),flush=True)
if errors:sys.exit(1)
