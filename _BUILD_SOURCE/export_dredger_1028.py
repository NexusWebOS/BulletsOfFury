from pathlib import Path
import json,base64
from playwright.sync_api import sync_playwright
from shoot import serve
from barrage_review_common_1025 import boot
R=Path(__file__).resolve().parents[1];O=R/'_ART_SOURCES/dredger_1028';O.mkdir(parents=True,exist_ok=True)
port,stop=serve(str(R));errors=[]
try:
 with sync_playwright()as pw:
  br=pw.chromium.launch(channel='msedge');p=boot(br.new_context(viewport={'width':1280,'height':800}),port,7,errors,'mini')
  p.wait_for_function("()=>{s7mWarm();return XART.rdy('s7m_tank')&&XART.rdy('er28_tank_gun')}")
  for name,cell,w,h in [('body',0,176,192),('top',2,76,68)]:
   data=p.evaluate("([cell,w,h])=>{const c=document.createElement('canvas');c.width=w;c.height=h;c.getContext('2d').drawImage(s7mCell('tank',cell,true),0,0,w,h);return c.toDataURL().split(',')[1]}",[cell,w,h]);(O/(name+'.png')).write_bytes(base64.b64decode(data))
  for f in [0,64,128,192]:
   data=p.evaluate("f=>{const a=ER28_ART.tank_gun,c=document.createElement('canvas');c.width=a.cw;c.height=a.ch;c.getContext('2d').drawImage(XART.get(a.key),f%a.cols*a.cw,Math.floor(f/a.cols)*a.ch,a.cw,a.ch,0,0,a.cw,a.ch);return c.toDataURL().split(',')[1]}",f);(O/f'gun-{f}.png').write_bytes(base64.b64decode(data))
  p.evaluate("()=>{s7mSet(reviewActor,'er28-guns');reviewActor.enter=false;reviewActor.x=worldWidth()/2;reviewActor.y=205;}");p.evaluate('drawWorld(0)');p.screenshot(path=str(O/'native.png'))
  print(p.evaluate("()=>({kind:reviewActor.kind,ship:reviewActor._ship,pose:s7mPose(reviewActor),rect:{w:reviewActor.w,h:reviewActor.h},VH,viewW:viewW(),top:s7mMuzzle(reviewActor,'dorsal')})"));print(errors);br.close()
finally:stop()
