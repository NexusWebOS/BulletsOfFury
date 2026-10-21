from pathlib import Path
import ast,json,http.server,base64
from playwright.sync_api import sync_playwright
import shoot
R=Path(__file__).resolve().parents[1];O=R/'_shots/boss_redesign_1020';port,stop=shoot.serve(str(R))
tree=ast.parse((R/'_BUILD_SOURCE/probe_boss_redesign_1020.py').read_text());BOOT=next(ast.literal_eval(n.value) for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='BOOT' for t in n.targets));t=ast.parse((R/'_BUILD_SOURCE/probe_feedback_1002.py').read_text());SETUP=next(ast.literal_eval(n.value) for n in t.body if isinstance(n,ast.Assign) and any(isinstance(x,ast.Name) and x.id=='SETUP' for x in n.targets))
http.server.ThreadingHTTPServer.request_queue_size=128
try:
 with sync_playwright() as pw:
  b=pw.chromium.launch(channel='msedge',args=['--mute-audio']);p=b.new_page();p.set_default_timeout(180000);p.goto(f'http://127.0.0.1:{port}');p.wait_for_function('window.__bofFrames>4');p.evaluate(shoot.TRAP_RAF);p.evaluate(SETUP,dict(stage=8,kind='vileexistence',pilot='cole'));p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(8)&&v18Warm();}');p.evaluate(BOOT)
  for form in [2,1,8]:
   p.evaluate('f=>setup20(f)',form);print('FORM',form,p.evaluate('()=>({parts:B.parts.map(p=>[p.id,p.hp,p.destroyed]),rig:v18Rig(B).map(v=>({id:v.p.id,key:v.key,anchor:v.anchor,belongs:B.parts.includes(v.p),flash:v.p.flash})),mode:B._r30.mode,cam:camX,state})'),flush=True)
   if form==2:
    print('WING',p.evaluate('()=>{Q.stage="swoon";const id="wingL",part=B.parts.find(p=>p.id===id),before=capturePart20(id);B._lastPart=part;modularHit(1);const after=capturePart20(id);let changed=0;for(let i=0;i<after.length;i++)if(before[i]!==after[i])changed++;return{changed,flash:part.flash,owner:B.flash,draw:B20.draws,rig:v18Rig(B).map(v=>[v.p.id,v.p===part,v.key]),rdy:XART.rdy("ph21_wingL")};}'),flush=True)
   p.evaluate('()=>{ctx.setTransform(1,0,0,1,0,0);ctx.clearRect(0,0,cv.width,cv.height);ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);drawHUD();}');(O/f'diag-{form}.png').write_bytes(base64.b64decode(p.evaluate('()=>cv.toDataURL().split(",")[1]')))
  b.close()
finally:stop()
