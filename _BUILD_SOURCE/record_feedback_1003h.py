"""Record the real ending, and the shared static-frame monochrome draw function."""
from pathlib import Path
import base64,json,sys
from playwright.sync_api import sync_playwright
import shoot as sh
R=Path(__file__).resolve().parents[1];O=R/'_shots/feedback_1003h';O.mkdir(parents=True,exist_ok=True)
SETUP=(R/'_BUILD_SOURCE/probe_feedback_1002.py').read_text(encoding='utf-8').split('SETUP="""')[1].split('"""')[0]
errors=[];port,stop=sh.serve(str(R))
def start(p,canvas='cv',audio=False):
 p.evaluate('''([canvas,audio])=>{window.movieChunks=[];const stream=window[canvas].captureStream(30);
 if(audio&&Snd.cur?.captureStream)for(const t of Snd.cur.captureStream().getAudioTracks())stream.addTrack(t);
 window.movieRecorder=new MediaRecorder(stream,{mimeType:'video/webm;codecs=vp9',videoBitsPerSecond:2400000});
 movieRecorder.ondataavailable=e=>{if(e.data.size)movieChunks.push(e.data);};movieRecorder.start();}''',[canvas,audio])
def finish(p,name,dest=O):
 data=p.evaluate('''()=>new Promise(resolve=>{movieRecorder.onstop=()=>{const f=new FileReader();f.onload=()=>resolve(f.result.split(',')[1]);f.readAsDataURL(new Blob(movieChunks,{type:'video/webm'}));};movieRecorder.stop();})''')
 (dest/name).write_bytes(base64.b64decode(data))
try:
 with sync_playwright() as pw:
  b=pw.chromium.launch(args=['--no-sandbox','--autoplay-policy=no-user-gesture-required']);p=b.new_page(viewport={'width':1280,'height':900})
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
  p.goto(f'http://127.0.0.1:{port}/index.html',timeout=120000);p.wait_for_function('()=>window.__bofFrames>4',timeout=120000);p.evaluate(sh.TRAP_RAF);p.mouse.click(500,500)
  p.wait_for_function('()=>{h3Warm();return H3_ART.every(k=>XART.rdy("h3_"+k))&&furyShipReady();}',timeout=120000)
  if '--ending-only' not in sys.argv:
   # This uses the same renderer/timing as the in-game still, at its wide aspect.
   p.evaluate('()=>{window.fadeCanvas=document.createElement("canvas");fadeCanvas.width=1280;fadeCanvas.height=720;window.fadeContext=fadeCanvas.getContext("2d");h3AftermathDraw(fadeContext,0,0,1280,720,0);}')
   start(p,'fadeCanvas')
   for i in range(181):
    p.evaluate('(t)=>h3AftermathDraw(fadeContext,0,0,1280,720,t)',i/30);p.wait_for_timeout(33)
   finish(p,'orbital-aftermath-monochrome.webm',R/'assets/game/feedback_1003h')
  # Record the full native timeline with live MP3 music and authored explosion cues.
  p.evaluate(SETUP,{'stage':5,'pilot':'axel','diff':'furious'})
  p.evaluate('()=>{Audio.init();Audio.resume();spawnBoss(curStage.boss);boss._be=null;boss.enter=false;fb2Intro=null;boss.hp=0;bossDie();window.movieCanvas=cv;}')
  p.wait_for_function('()=>Snd.cur&&!Snd.cur.paused&&Snd.cur.readyState>=3',timeout=30000)
  start(p,'movieCanvas',True)
  for i in range(1920):
   p.evaluate('()=>{updatePlay(1/30);ctx.setTransform(SS,0,0,SS,0,0);drawWorld(1/30);}')
   p.wait_for_timeout(28)
   if p.evaluate('()=>state===GS.STAGECLEAR'):break
  finish(p,'hammer-homecoming.webm')
  # A second native clip shows each rebel's portrait, entry spacing and protected dialogue.
  if '--ending-only' not in sys.argv:
   p.evaluate(SETUP,{'stage':6,'pilot':'yuri','diff':'furious'})
   p.evaluate('()=>{spawnBoss("rebelsquad");boss._be=null;boss.enter=false;window.movieCanvas=cv;}')
   start(p,'movieCanvas')
   for i in range(1300):
    p.evaluate('()=>{updatePlay(1/30);ctx.setTransform(SS,0,0,SS,0,0);drawWorld(1/30);}')
    p.wait_for_timeout(28)
    if p.evaluate('()=>boss?._rebels?.frIntro?.done'):break
   finish(p,'rebel-introductions.webm')
  b.close()
finally:
 stop();(O/'motion-errors.json').write_text(json.dumps(errors),encoding='utf-8')
print(json.dumps({'errors':errors,'videos':['assets/game/shared/combat/feedback_1003h/orbital-aftermath-monochrome.webm','_shots/feedback_1003h/hammer-homecoming.webm','_shots/feedback_1003h/rebel-introductions.webm']}),flush=True)
raise SystemExit(1 if errors else 0)
