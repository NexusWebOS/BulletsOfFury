"""Small real-engine preview of the restored modular Herald."""
from pathlib import Path
import json,base64,http.server
from playwright.sync_api import sync_playwright
import shoot as sh
R=Path(__file__).resolve().parents[1];O=R/'_shots/herald_1003f';O.mkdir(parents=True,exist_ok=True)
SETUP=(R/'_BUILD_SOURCE/probe_feedback_1002.py').read_text(encoding='utf-8').split('SETUP="""')[1].split('"""')[0]
port,stop=sh.serve(str(R));errors=[];http.server.SimpleHTTPRequestHandler.log_message=lambda *a,**k:None
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(args=['--no-sandbox']);p=br.new_page(viewport={'width':1100,'height':950})
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('()=>window.__bofFrames>4',timeout=120000);p.evaluate(sh.TRAP_RAF);p.wait_for_timeout(60)
  p.evaluate(SETUP,{'stage':8,'kind':'heralddeath','mini':True,'diff':'furious'})
  p.wait_for_function('()=>XART.rdy(HD1003_ART.key)&&Object.values(S81003_ART).every(a=>XART.rdy(a.key))',timeout=120000,polling=60)
  p.evaluate('()=>{playerHit=function(){};player.invuln=0;powerups=[];_mc1=_mc2=_sc1=_sc2=true;window.hdMovieChunks=[];window.hdRecorder=new MediaRecorder(cv.captureStream(30),{mimeType:"video/webm;codecs=vp9",videoBitsPerSecond:1800000});hdRecorder.ondataavailable=e=>{if(e.data.size)hdMovieChunks.push(e.data);};hdRecorder.start();}')
  for i in range(630):
   if i in [270,405]:
    p.evaluate('(id)=>{const q=hd1003Part(B,id);hd1003Hit(B,q.hp+1,0,0,id);}', 'gunL' if i==270 else 'wingR')
   if i==555:p.evaluate('()=>hitSubBoss(B.hp+1)')
   p.evaluate('(i)=>{for(let j=0;j<2;j++){player.x=worldWidth()/2+Math.sin(i/90)*65;player.y=VH-95;camX=worldWidth()/2-VW/2;updatePlay(1/60);drawWorld(1/60);}}',i);p.wait_for_timeout(27)
  p.evaluate('()=>new Promise(resolve=>{hdRecorder.onstop=()=>{const f=new FileReader();f.onload=()=>{window.hdMovie=f.result;resolve();};f.readAsDataURL(new Blob(hdMovieChunks,{type:"video/webm"}));};hdRecorder.stop();})')
  (O/'herald-motion.webm').write_bytes(base64.b64decode(p.evaluate('()=>hdMovie.split(",")[1]')))
  (O/'motion-errors.json').write_text(json.dumps(errors),encoding='utf-8');br.close()
finally:stop()
print(json.dumps({'video':str(O/'herald-motion.webm'),'errors':errors}))
if errors:raise SystemExit(1)
