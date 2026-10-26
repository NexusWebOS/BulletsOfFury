from pathlib import Path
from playwright.sync_api import sync_playwright
from shoot import serve
import base64,json
R=Path(__file__).resolve().parents[1];O=R/'_ART_SOURCES/boss_integrity_1024/reference';O.mkdir(parents=True,exist_ok=True);port,stop=serve(str(R))
with sync_playwright()as pw:
 b=pw.chromium.launch(channel='msedge');p=b.new_page(viewport={'width':1280,'height':800});p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>5',timeout=180000);p.evaluate("()=>{diffKey='furious';debugStartFight({stage:8,role:'boss',kind:'vileexistence',name:'Dracodia'},{pilot:'cole'});}");p.wait_for_function('boss?._r30?.v18',timeout=180000)
 for n,f,name in [(0,0,'dracodia'),(2,2,'phoenix'),(2,8,'corrupt_hammer')]:
  p.evaluate('([n,f])=>{v18Enter(boss,n,f);v18Fight(boss);v18Warm();}',[n,f]);p.wait_for_function('v18Warm()',timeout=180000)
  raw=p.evaluate("""()=>{const b=boss;b.x=256;b.y=256;b._r30.clock=8/12;b._r30.v18.attack=null;ctx.save();ctx.setTransform(1,0,0,1,0,0);ctx.clearRect(0,0,cv.width,cv.height);if(v19Native(b))v19Body(b);else v18Body(b);ctx.restore();const out=document.createElement('canvas');out.width=512;out.height=512;out.getContext('2d').drawImage(cv,0,0,512,512,0,0,512,512);return out.toDataURL().split(',')[1];}""")
  (O/(name+'.png')).write_bytes(base64.b64decode(raw))
 b.close()
stop()
