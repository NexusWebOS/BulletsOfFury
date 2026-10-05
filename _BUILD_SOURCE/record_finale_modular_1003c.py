"""Record the actual engine: sequential refill, moving components and knight combo."""
from pathlib import Path
import json,base64,sys,http.server
from playwright.sync_api import sync_playwright
import shoot as sh
R=Path(__file__).resolve().parents[1];O=R/'_shots/finale_modular_1003c';O.mkdir(parents=True,exist_ok=True)
SETUP=(R/'_BUILD_SOURCE/probe_feedback_1002.py').read_text(encoding='utf-8').split('SETUP="""')[1].split('"""')[0]
port,stop=sh.serve(str(R));errors=[];http.server.SimpleHTTPRequestHandler.log_message=lambda *a,**k:None
try:
 with sync_playwright() as pw:
  browser=pw.chromium.launch(args=['--no-sandbox']);p=browser.new_page(viewport={'width':1100,'height':950});p.on('pageerror',lambda e:errors.append(str(e)))
  p.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('()=>window.__bofFrames>4',timeout=120000);p.evaluate(sh.TRAP_RAF);p.wait_for_timeout(60)
  p.evaluate(SETUP,{'stage':8,'kind':'vileexistence','diff':'furious'});p.evaluate('()=>{r30Warm();playerHit=function(){};player.invuln=0;window.chunksFmc=[];window.recFmc=new MediaRecorder(cv.captureStream(30),{mimeType:"video/webm;codecs=vp9",videoBitsPerSecond:1800000});recFmc.ondataavailable=e=>{if(e.data.size)chunksFmc.push(e.data);};}')
  p.wait_for_function('()=>Object.values(FMC_ART).every(a=>XART.rdy(a.key))&&Object.values(S81003_ART).every(a=>XART.rdy(a.key))&&Object.keys(REALM30_ART).every(k=>XART.rdy("r30_"+k))',timeout=120000)
  p.evaluate('()=>{B._r30.mode="takeover";B._r30.t=0;B.enter=true;recFmc.start();}')
  def frames(n):
   for i in range(n//2):
    p.evaluate('()=>{for(let i=0;i<2;i++){updatePlay(1/60);drawWorld(1/60);}}');p.wait_for_timeout(28)
  frames(324)
  for form in [0,1,2,3,4,6,7,5]:
   p.evaluate('(n)=>{r30Clear(B);r30Form(B,n);B._r30.mode="fight";B.enter=false;B._r30.seq=n===4?1:n===6?2:0;player.x=worldWidth()/2;player.y=VH-105;camX=player.x-VW/2;powerups=[];r30Attack(B);}',form)
   frames(800 if form==5 else 234)
  p.evaluate('()=>new Promise(resolve=>{recFmc.onstop=async()=>{const blob=new Blob(chunksFmc,{type:"video/webm"});const r=new FileReader();r.onload=()=>{window.fmcMovie=r.result;resolve();};r.readAsDataURL(blob);};recFmc.stop();})')
  (O/'modular-finale-motion.webm').write_bytes(base64.b64decode(p.evaluate('()=>fmcMovie.split(",")[1]')))
  (O/'motion-errors.json').write_text(json.dumps(errors,indent=2),encoding='utf-8');browser.close();print(json.dumps({'video':str(O/'modular-finale-motion.webm'),'errors':errors}))
finally:stop()
if errors:sys.exit(1)
