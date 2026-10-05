"""Record engine pixels. Hold guard poses only in this inspection fixture."""
from pathlib import Path
import json,base64,sys
from playwright.sync_api import sync_playwright
import shoot as sh
R=Path(__file__).resolve().parents[1];O=R/'_shots/codewall_1003d';O.mkdir(parents=True,exist_ok=True)
SETUP=(R/'_BUILD_SOURCE/probe_feedback_1002.py').read_text(encoding='utf-8').split('SETUP="""')[1].split('"""')[0]
port,stop=sh.serve(str(R));errors=[]
try:
 with sync_playwright() as pw:
  browser=pw.chromium.launch(args=['--no-sandbox','--autoplay-policy=no-user-gesture-required']);p=browser.new_page(viewport={'width':1100,'height':950})
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('()=>window.__bofFrames>4',timeout=120000);p.evaluate(sh.TRAP_RAF);p.wait_for_timeout(60)
  p.evaluate(SETUP,{'stage':8,'kind':'vileexistence','diff':'furious'})
  p.evaluate('()=>{r30Warm();playerHit=function(){};player.invuln=0;window.cwdChunks=[];window.cwdRec=new MediaRecorder(cv.captureStream(30),{mimeType:"video/webm;codecs=vp9",videoBitsPerSecond:1800000});cwdRec.ondataavailable=e=>{if(e.data.size)cwdChunks.push(e.data);};}')
  p.wait_for_function('()=>Object.values(CWD_ART).every(a=>XART.rdy(a.key))&&Object.values(FMC_ART).every(a=>XART.rdy(a.key))&&Object.values(S81003_ART).every(a=>XART.rdy(a.key))',timeout=120000)
  p.evaluate('()=>{B._r30.mode="fight";B.enter=false;B._r30.seq=1;r30Attack(B);B._r30.attack.tell=5;cwdRec.start();}')
  def frames(n,hold=False):
   for i in range(n//2):
    p.evaluate('(hold)=>{for(let i=0;i<2;i++){if(hold&&B._r30.attack?.k1003)B._r30.attack.k1003.age=.30;updatePlay(1/60);drawWorld(1/60);}}',hold);p.wait_for_timeout(28)
  frames(60)
  for i in range(4):
   p.evaluate('(i)=>{const q=r30ShieldBounds(B),x=q.x+(i%2?1:-1)*q.w*.20,y=q.y+(i-1.5)*q.h*.14;B._lastPart=r30At(B,x,y);modularHit(6);}',i);frames(25)
  p.evaluate('()=>{B._lastPart={id:"codeWall1003d"};modularHit(9999);}')
  frames(90)
  p.evaluate('()=>{r30Clear(B);r30Form(B,5);B._r30.mode="fight";B.enter=false;player.x=worldWidth()/2;player.y=VH-110;camX=player.x-VW/2;r30Attack(B);}')
  frames(70,True)
  for i in range(4):
   p.evaluate('()=>{const q=r30ShieldBounds(B);B._lastPart=r30At(B,q.x,q.y);modularHit(5);}')
   frames(24,True)
  p.evaluate('()=>{B._lastPart={id:"codeWall1003d"};modularHit(9999);}')
  frames(90,True)
  frames(190)
  for form in [1,2,4,5]:
   p.evaluate('(n)=>{r30Clear(B);r30Form(B,n);B._r30.mode="fight";B.enter=false;B._lastPart=B.parts[0];modularHit(B.hp+1);}',form)
   frames(176)
  p.evaluate('()=>new Promise(resolve=>{cwdRec.onstop=async()=>{const r=new FileReader();r.onload=()=>{window.cwdMovie=r.result;resolve();};r.readAsDataURL(new Blob(cwdChunks,{type:"video/webm"}));};cwdRec.stop();})')
  (O/'codewall-motion.webm').write_bytes(base64.b64decode(p.evaluate('()=>cwdMovie.split(",")[1]')))
  (O/'motion-errors.json').write_text(json.dumps(errors,indent=2)+'\n',encoding='utf-8');browser.close();print(json.dumps({'video':str(O/'codewall-motion.webm'),'errors':errors}))
finally:stop()
if errors:sys.exit(1)
