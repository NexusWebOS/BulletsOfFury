"""Export current native encounter pixels before designing preview candidates."""
from pathlib import Path
import sys,base64,json
from playwright.sync_api import sync_playwright
from PIL import Image
import io
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'_BUILD_SOURCE'));import shoot
OUT=ROOT/'_ART_SOURCES/arcade_candidates_1010/reference';OUT.mkdir(parents=True,exist_ok=True)
port,stop=shoot.serve(str(ROOT));errors=[];meta={}
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(args=['--autoplay-policy=no-user-gesture-required']);p=br.new_page(viewport={'width':1280,'height':900});p.set_default_timeout(120000)
  p.on('pageerror',lambda e:errors.append(str(e)));p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>4');p.evaluate(shoot.TRAP_RAF);p.wait_for_timeout(60)
  p.add_script_tag(content=(ROOT/'_BUILD_SOURCE/balance_lab_1007.js').read_text())
  bosskind=p.evaluate('STAGES[0].boss')
  for name,c in [('razorback',{'stage':1,'kind':'razorback','mini':True,'diff':'normal'}),('furious_razorback',{'stage':1,'kind':'razorback','mini':True,'diff':'furious'}),('stage1_boss',{'stage':1,'kind':bosskind,'diff':'furious'})]:
   p.evaluate('(c)=>BAL7.setup({...c,pilot:"yuri",fire:false,seconds:60})',c)
   for _ in range(1800):
    if p.evaluate('()=>{stageLoadTick();return stageLoadInfo(1).ready;}'):break
    p.wait_for_timeout(20)
   p.evaluate('()=>{B.x=worldWidth()/2;B.y=220;B._drawY=220;B.enter=false;B._ovAirborne=false;if(B._ovIntro)B._ovIntro.done=true;if(B._rzb)B._rzb.a=Math.PI;ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);}')
   (OUT/(name+'-ingame.png')).write_bytes(base64.b64decode(p.evaluate('()=>cv.toDataURL().split(",")[1]')))
   data=p.evaluate('()=>{const x=B.x,y=B.y;ctx.setTransform(1,0,0,1,0,0);ctx.clearRect(0,0,cv.width,cv.height);B.x=384;B.y=384;B._drawY=384;if(B._rzb)razorbackDraw(B);else drawBoss();B.x=x;B.y=y;B._drawY=y;return cv.toDataURL().split(",")[1];}')
   Image.open(io.BytesIO(base64.b64decode(data))).crop((0,0,768,768)).save(OUT/(name+'.png'));meta[name]=p.evaluate('({kind:B.kind,w:B.w,h:B.h,parts:B._rzb?.pools||null})')
  br.close()
finally:stop()
(OUT/'runtime.json').write_text(json.dumps({'encounters':meta,'errors':errors},indent=2)+'\n')
print(json.dumps({'encounters':meta,'errors':errors}),flush=True)
if errors:sys.exit(1)
