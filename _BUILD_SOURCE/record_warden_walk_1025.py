"""45-second audible native Warden checkpoint. No enemy HP or phase writes.
The native loop reaches its first chase, then runs on real RAF with GOD and inputs.
The bot withholds weapons to keep all live limbs visible for movement review.
"""
from pathlib import Path
from playwright.sync_api import sync_playwright
from shoot import serve,TRAP_RAF,STEP
from record_furious_789_1025 import CAPTURE
import base64,json,http.server,time,subprocess,re
import imageio_ffmpeg
R=Path(__file__).resolve().parents[1];O=R/'_shots/warden_tidal_1025/walk';O.mkdir(parents=True,exist_ok=True)
folder=O/time.strftime('%H%M%S');folder.mkdir();errors=[];timeline=[];FF=imageio_ffmpeg.get_ffmpeg_exe()
http.server.SimpleHTTPRequestHandler.protocol_version='HTTP/1.1';http.server.ThreadingHTTPServer.request_queue_size=128
port,stop=serve(str(R));cap=CAPTURE.replace("debugStartFight(entry,{pilot:'cole',record:false});DBGT.god=true;DBGT.speed=1;player.invuln=0;","DBGT.god=true;DBGT.speed=1;player.invuln=0;")
cap=cap.replace('A.tick++;',r'''A.tick++;
  for(const k of ['a','d','w','s','j','k','c'])K[k]=false;
  const walkX=worldWidth()/2+Math.sin(elapsed*.31)*115,walkY=VH-65;
  K.a=player.x>walkX+6;K.d=player.x<walkX-6;K.w=player.y>walkY+6;K.s=player.y<walkY-6;return;
''').replace('COLE / INVULNERABLE INPUT BOT / NATIVE HP & PHASES','NATIVE WALK CHECKPOINT / INVULNERABLE INPUT BOT')
try:
 with sync_playwright()as pw:
  br=pw.chromium.launch(channel='msedge',args=['--autoplay-policy=no-user-gesture-required','--disable-background-timer-throttling','--disable-renderer-backgrounding']);p=br.new_page(viewport={'width':1280,'height':800})
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text)if m.type=='error'or'draw error'in m.text else None)
  p.on('response',lambda r:errors.append('HTTP '+str(r.status)+' '+r.url.split('/')[-1])if r.status>=400 else None)
  p.goto(f'http://127.0.0.1:{port}/index.html',wait_until='load',timeout=180000);p.wait_for_function('window.__bofFrames>5',timeout=180000);p.mouse.click(3,3);p.evaluate(TRAP_RAF)
  p.evaluate("()=>{debugUnlocked=true;diffKey='furious';debugStartFight(debugFightFor(7,'boss'),{pilot:'cole'});spawnBoss('sludgeemperor');debugFight.spawned=true;warnT=0;DBGT.god=true;player.x=worldWidth()/2;player.y=VH-65;BOFCinematicDirector.cancel();setState(GS.PLAY);for(const k of Object.keys(Input.keys))Input.keys[k]=false;}")
  p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(7)&&r25Warm(7)}',timeout=180000)
  found=False
  for i in range(2000):
   p.evaluate(STEP,5)
   if p.evaluate("boss._s7mod?.mode==='chase'"):found=True;break
   if i%12==0:p.wait_for_timeout(1)
  if not found:raise RuntimeError('Native chase checkpoint not reached')
  initial=p.evaluate('({hp:boss.hp,maxhp:boss.maxhp,mode:boss._s7mod.mode,clock:boss._s7mod.clock})')
  with(folder/'capture.webm').open('wb')as raw:
   p.expose_function('saveCaptureChunk',lambda b:raw.write(base64.b64decode(b)))
   p.evaluate('()=>{window.requestAnimationFrame=window.__bofRealRAF;last=performance.now();requestAnimationFrame(loop);}')
   p.evaluate(cap,{'stage':7});print('RECORD Warden walking checkpoint',flush=True)
   while True:
    p.wait_for_timeout(350);q=p.evaluate("()=>({seconds:(performance.now()-captureStart)/1000,hp:boss.hp,mode:boss._s7mod.mode,clock:boss._s7mod.clock,rate:s7WardenReverseScroll(),speed:boss._s7mod.r25Gait?.speed,frames:captureStats.frames,audio:captureStats.peak})");timeline.append(q)
    if q['seconds']>45 or errors:break
   sound=p.evaluate("async()=>{reviewBot.enabled=false;for(const k of ['a','d','w','s','j','c'])Input.keys[k]=false;await new Promise(r=>{reviewRecorder.onstop=r;reviewRecorder.stop();});await capturePending;captureLive=false;return captureStats;}")
   p.screenshot(path=str(folder/'final.png'))
  br.close()
finally:stop()
video=folder/'warden-walking.mp4'
subprocess.run([FF,'-v','error','-y','-threads','2','-i',str(folder/'capture.webm'),'-vf','fps=30','-c:v','libx264','-preset','fast','-crf','20','-c:a','aac','-b:a','160k','-pix_fmt','yuv420p','-movflags','+faststart',str(video)],check=True)
dec=subprocess.run([FF,'-hide_banner','-nostats','-threads','2','-i',str(video),'-af','volumedetect','-f','null','-'],capture_output=True,text=True);(folder/'decode.log').write_text(dec.stderr,encoding='utf8');pk=re.search(r'max_volume: ([\-\d.inf]+) dB',dec.stderr);peak=float(pk[1])if pk else-999
for i,at in enumerate([.8,4,8,12,20,30,40]):subprocess.run([FF,'-v','error','-y','-ss',str(at),'-i',str(video),'-frames:v','1',str(folder/f'decoded-{i}.png')],check=True)
modes=sorted(set(t['mode']for t in timeline));checks={'noErrors':not errors,'audible':peak>-60,'fullDecode':dec.returncode==0,'realTime':sound['frames']/timeline[-1]['seconds']>45,'nativeChase':any(t['rate']>0 and t.get('speed',0)>0 for t in timeline),'nativeSwipe':any(t['mode'].startswith('swipe')for t in timeline),'nativeBattery':'battery1009'in modes}
report={'video':video.relative_to(R).as_posix(),'method':__doc__,'initial':initial,'timeline':timeline,'sound':sound,'errors':errors,'modes':modes,'decodedPeakDb':peak,'checks':checks};(folder/'report.json').write_text(json.dumps(report,indent=2),encoding='utf8');(O/'latest.json').write_text(json.dumps({'folder':str(folder.relative_to(R))},indent=2),encoding='utf8')
print(json.dumps({'video':str(video),'checks':checks,'modes':modes}),flush=True)
raise SystemExit(0 if all(checks.values())else 1)
