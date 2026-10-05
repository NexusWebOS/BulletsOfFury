"""Record actual host/knight animation in Chromium; no procedural re-render."""
from pathlib import Path
import json,base64,sys
from playwright.sync_api import sync_playwright
import shoot as sh
R=Path(__file__).resolve().parents[1];O=R/'_shots/finale_1003b';O.mkdir(parents=True,exist_ok=True)
SETUP=(R/'_BUILD_SOURCE/probe_feedback_1002.py').read_text().split('SETUP="""')[1].split('"""')[0]
port,stop=sh.serve(str(R));errors=[]
try:
 with sync_playwright() as pw:
  browser=pw.chromium.launch(args=['--no-sandbox']);p=browser.new_page(viewport={'width':1100,'height':950});p.on('pageerror',lambda e:errors.append(str(e)))
  p.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('()=>window.__bofFrames>4',timeout=120000);p.evaluate(sh.TRAP_RAF);p.wait_for_timeout(60)
  p.evaluate(SETUP,{'stage':8,'kind':'vileexistence','diff':'furious'});p.evaluate('()=>{r30Warm();playerHit=function(){};player.invuln=0;window.chunksFinale=[];window.recFinale=new MediaRecorder(cv.captureStream(30),{mimeType:"video/webm;codecs=vp9",videoBitsPerSecond:1800000});recFinale.ondataavailable=e=>{if(e.data.size)chunksFinale.push(e.data);};}')
  p.wait_for_function('()=>Object.values(FINALE1003B_ART).every(a=>XART.rdy(a.key))&&Object.values(S81003_ART).every(a=>XART.rdy(a.key))',timeout=120000)
  p.evaluate('()=>{B._r30.mode="fight";B.enter=false;r30Attack(B);recFinale.start();}')
  for i in range(135):p.evaluate('()=>{updatePlay(1/60);drawWorld(1/60);updatePlay(1/60);drawWorld(1/60);}');p.wait_for_timeout(27)
  p.evaluate('()=>{r30Clear(B);r30Form(B,5);B._r30.mode="fight";B.enter=false;B._r30.seq=1;r30Attack(B);}')
  for i in range(390):p.evaluate('()=>{updatePlay(1/60);drawWorld(1/60);updatePlay(1/60);drawWorld(1/60);}');p.wait_for_timeout(27)
  p.evaluate('()=>new Promise(resolve=>{recFinale.onstop=async()=>{const blob=new Blob(chunksFinale,{type:"video/webm"});const r=new FileReader();r.onload=()=>{window.finalMovie=r.result;resolve();};r.readAsDataURL(blob);};recFinale.stop();})')
  (O/'combat-motion.webm').write_bytes(base64.b64decode(p.evaluate('()=>finalMovie.split(",")[1]')))
  (O/'motion-errors.json').write_text(json.dumps(errors,indent=2));browser.close();print(json.dumps({'video':str(O/'combat-motion.webm'),'errors':errors}))
finally:stop()
if errors:sys.exit(1)
