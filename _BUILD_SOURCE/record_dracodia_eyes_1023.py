from pathlib import Path
from playwright.sync_api import sync_playwright
import json,sys,base64,subprocess,imageio_ffmpeg
R=Path(__file__).resolve().parents[1];W=R/'_ART_SOURCES/dracodia_eyes_1023';O=R/'_shots/dracodia_eyes_1023';O.mkdir(exist_ok=True);sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
port,stop=shoot.serve(str(R));errors=[]
try:
 with sync_playwright()as pw:
  br=pw.chromium.launch(channel='msedge',args=['--autoplay-policy=no-user-gesture-required']);p=br.new_page();p.on('pageerror',lambda e:errors.append(str(e)));p.goto(f'http://127.0.0.1:{port}');p.wait_for_function('window.__bofFrames>4');p.evaluate(shoot.TRAP_RAF)
  for f in ['balance_lab_1007.js','animation_audit_1023/hammer_review_lab_1023.js']:p.add_script_tag(path=str(R/'_BUILD_SOURCE'/f))
  ev=p.evaluate;ev('BAL7.setup({stage:8,kind:"vileexistence",pilot:"cole",diff:"normal",fire:false,seconds:60})');p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(8)&&nb23Warm();}')
  ev('''()=>{window.EYE23={reset(){HR23.clean();v18Budget(B);v18Enter(B,2,6);v18Fight(B);B._r30.cd=999;dr5State(B).radio=null;playerHit=()=>{};},step(dt){player.invuln=0;player.dead=player.out=false;player.fireCd=9999;pBullets=[];updatePlay(dt);ctx.setTransform(SS,0,0,SS,0,0);drawWorld(dt);}};EYE23.reset();}''')
  video=ev('''async()=>{const cs=cv.captureStream(30),as=await HR23.audio(),rec=new MediaRecorder(new MediaStream([...cs.getVideoTracks(),...as.getAudioTracks()]),{mimeType:'video/webm;codecs=vp8,opus',videoBitsPerSecond:2600000}),chunks=[];rec.ondataavailable=e=>e.data.size&&chunks.push(e.data);const end=new Promise(resolve=>rec.onstop=()=>{const f=new FileReader();f.onload=()=>resolve(f.result);f.readAsDataURL(new Blob(chunks,{type:'video/webm'}));});rec.start();let last=performance.now(),start=last,pass=0;await new Promise(resolve=>{const timer=setInterval(()=>{const now=performance.now(),t=(now-start)/1000;if(pass===0&&t>2){nb23Start(B,'eyeExpansion');pass=1;}if(pass===1&&t>7.5){EYE23.reset();nb23Start(B,'eyeExpansion');pass=2;}EYE23.step(Math.min(.035,(now-last)/1000));last=now;if(t>12.5){clearInterval(timer);resolve();}},1000/60);});rec.stop();const data=await end;HR23.audioRestore();cs.getTracks().forEach(t=>t.stop());return data;}''');(O/'moving-eyes-laser.webm').write_bytes(base64.b64decode(video.split(',')[1]));br.close()
finally:stop()
subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(),'-y','-loglevel','error','-i',str(O/'moving-eyes-laser.webm'),'-c:v','libx264','-preset','fast','-crf','20','-pix_fmt','yuv420p','-c:a','aac','-movflags','+faststart',str(O/'moving-eyes-laser.mp4')],check=True)
(O/'record-errors.json').write_text(json.dumps(errors));print(json.dumps({'videoBytes':(O/'moving-eyes-laser.mp4').stat().st_size,'errors':errors}));sys.exit(bool(errors))
