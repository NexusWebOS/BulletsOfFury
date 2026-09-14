"""Native Furyship launch and combat demo, with frame-aligned game sound effects.

Uses the existing shoot/capture3 fixture. HQ reading and boss entrance are skipped;
capture-only playerHit prevents a death from cutting off the animation demonstration.
"""
from pathlib import Path
import base64,json,sys,http.server,threading,subprocess,hashlib,array
R=Path(__file__).resolve().parents[2];O=R/'_shots/furyship_live_0914/video';O.mkdir(parents=True,exist_ok=True)
sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
sys.path.insert(0,str(R/'_BUILD_SOURCE/trailer_v7'));import capture3
sys.path.insert(0,str(R/'_BUILD_SOURCE/stage_1_5_0914'));import audio_export
import imageio_ffmpeg
from playwright.sync_api import sync_playwright

class Quiet(http.server.SimpleHTTPRequestHandler):
 def __init__(self,*a,**kw):super().__init__(*a,directory=str(R),**kw)
 def log_message(self,*a):pass
srv=http.server.ThreadingHTTPServer(('127.0.0.1',0),Quiet);threading.Thread(target=srv.serve_forever,daemon=True).start()
ff=imageio_ffmpeg.get_ffmpeg_exe();reports=[];errors=[]
with sync_playwright() as p:
 b=p.chromium.launch(args=['--no-sandbox','--mute-audio','--autoplay-policy=no-user-gesture-required'])
 for name,seconds in [('transformation',12),('flight',14)]:
  pg=b.new_page(viewport={'width':1100,'height':1200})
  pg.on('pageerror',lambda e:errors.append(str(e)));pg.on('console',lambda m:errors.append(m.text)if m.type=='error'else None)
  pg.goto('http://127.0.0.1:%d/index.html'%srv.server_port,wait_until='load',timeout=120000)
  pg.wait_for_function('()=>(window.__bofFrames|0)>4',timeout=120000)
  pg.evaluate(shoot.TRAP_RAF);pg.evaluate(capture3.LIB);pg.evaluate('()=>{__auto=function(){};furyLegacyShip=false;furyShipWarm();Audio.resume();}')
  pg.wait_for_function('()=>furyShipReady()',timeout=120000)
  if name=='transformation':
   pg.evaluate('''()=>{run.mode='arcade';run.pilot='cole';pilotIndex=PILOTS.findIndex(p=>p.key==='cole');run.stage=5;curStage=STAGES[4];beginStage(5);player.reset();player.invuln=0;story=null;special=null;stagePlan=[];waveIdx=0;boss=null;bossActive=false;bossTriggered=true;subBoss=null;subBossActive=false;subBossTriggered=true;aminiTriggered=true;enemies=[];pBullets=[];eBullets=[];particles=[];powerups=[];warmPlayerAtlases();run.gravityShipReady=false;setState(GS.LAUNCH);drawLaunch._phase=undefined;drawLaunch(0);gravityModeStart();drawLaunch._phase='gravity';drawLaunch._dist=SEG_B3+SEG_B1+240;gravityMode.dialogueDone=true;gravityMode.dialogueT=100;}''')
  else:
   result=pg.evaluate('()=>__fight(5,"mini","cole")');assert result['ok'],result
   for _ in range(200):
    ready=pg.evaluate('()=>{const T=__tgt();return T&&!T.dead&&!T.enter&&T.y>0;}')
    if ready:break
    pg.evaluate('()=>__step(6)');pg.wait_for_timeout(8)
   assert ready,'miniboss entrance failed'
   pg.evaluate('''()=>{story=null;dlgBox=function(){};floaters.length=0;player.x=worldWidth()/2;player.y=PLAY.y+PLAY.h*.77;player.invuln=0;run.weapon=0;run.wlevel=1;warmPlayerAtlases();}''')
  pg.wait_for_timeout(500)
  pg.evaluate('''()=>{__auto=function(){};playerHit=function(){};for(const k of Object.keys(Input.keys))Input.keys[k]=false;
   __i=1;const L=__alog;L.snd.length=0;L.syn.length=0;L.warp.length=0;L.restarts.length=0;L.loops={};
   window.__poseLog=[];const draw=furyShipDrawFlight;furyShipDrawFlight=function(x,y,s,p,pose,t){__poseLog.push(pose.key);return draw.apply(this,arguments);};}''')
  if name=='transformation':pg.evaluate('()=>gravityModeBeginCharge()')
  rec0=pg.evaluate('()=>__i');picture=O/(name+'_picture.mp4');movie=O/(name+'.mp4')
  enc=subprocess.Popen([ff,'-y','-v','error','-f','image2pipe','-vcodec','mjpeg','-framerate','30','-i','pipe:0','-c:v','libx264','-preset','veryfast','-crf','19','-pix_fmt','yuv420p','-movflags','+faststart',str(picture)],stdin=subprocess.PIPE,stderr=subprocess.PIPE)
  timeline=[]
  for frame in range(seconds*30):
   if name=='flight':
    pg.evaluate('''f=>{const K=Input.keys;const tx=worldWidth()/2+Math.sin(f/30*.75)*95;
     K.a=player.x>tx+5;K.d=player.x<tx-5;K.j=f>15&&f<390;
     if([45,210,345].includes(f)){player._somerCool=0;startSomersault();}
     if(f===105||f===285){player._rollCool=0;startRoll(-1);}
     if(f===155){player._rollCool=0;startRoll(1);}
    }''',frame)
   pg.evaluate('()=>__step(2)')
   enc.stdin.write(base64.b64decode(pg.evaluate('()=>document.querySelector("#screen").toDataURL("image/jpeg",.94).split(",")[1]')))
   err=pg.evaluate('()=>window.__err||null');assert not err,err
   if frame%60==0:
    metrics=pg.evaluate('()=>({state,phase:gravityMode.phase,dead:player.dead,pose:furyShipPose(player).key})');timeline.append({'s':frame/30,**metrics});print(name,frame/30,metrics,flush=True)
   if frame in [38,130,153,180,215,275]:
    (O/(name+'_%03d.png'%frame)).write_bytes(base64.b64decode(pg.evaluate('()=>document.querySelector("#screen").toDataURL().split(",")[1]')))
  enc.stdin.close();encerr=enc.stderr.read();assert enc.wait()==0,encerr
  ev=pg.evaluate('()=>__audioDump()');ev.update(rec0=rec0,frames=seconds*60)
  (O/(name+'_events.json')).write_text(json.dumps(ev),encoding='utf-8')
  res=pg.evaluate(audio_export.RENDER,{'ev':ev,'iife':audio_export.audio_module_source(),'tail':0,'exclude':[]})
  assert not res['errs'] and res['rms']>0,{k:res[k]for k in ['errs','rms','peak']}
  gain=min(1,.85/res['peak']);samples=array.array('f');samples.frombytes(base64.b64decode(res['b64']))
  raw=array.array('f',(v*gain for v in samples)).tobytes()
  wav=O/(name+'_sfx.wav');audio_export.write_wav_float(str(wav),raw)
  subprocess.run([ff,'-y','-v','error','-i',str(picture),'-i',str(wav),'-map','0:v','-map','1:a','-c:v','copy','-c:a','aac','-b:a','192k','-shortest','-movflags','+faststart',str(movie)],check=True)
  report={'name':name,'seconds':seconds,'timeline':timeline,'poses':pg.evaluate('()=>[...new Set(__poseLog)]'),'audio':{**{k:res[k]for k in ['peak','rms','counts','errs']},'exportGain':gain,'exportPeak':res['peak']*gain},'sounds':sorted(set(e[1]for e in ev['snd']))}
  reports.append(report);(O/'report.json').write_text(json.dumps({'runtimeSha256':hashlib.sha256((R/'assets/game.js').read_bytes()).hexdigest(),'takes':reports,'errors':errors,'fixture':'Native game rendering; completed HQ dialogue and miniboss entrance skipped; capture-only invincibility. Sound effects reconstructed from frame-stamped game audio calls; no added soundtrack.'},indent=2)+'\n')
  pg.close();print('DONE',name,flush=True)
 b.close()
srv.shutdown();assert not errors,errors
concat=O/'concat.txt';concat.write_text(''.join("file '%s'\n"%(O/(r['name']+'.mp4')).as_posix()for r in reports))
final=O/'BulletsOfFury_Furyship_0914.mp4'
subprocess.run([ff,'-y','-v','error','-f','concat','-safe','0','-i',str(concat),'-c','copy','-movflags','+faststart',str(final)],check=True)
subprocess.run([ff,'-v','error','-i',str(final),'-f','null','-'],check=True)
print('VIDEO',str(final),flush=True)
