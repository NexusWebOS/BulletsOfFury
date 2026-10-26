from playwright.sync_api import sync_playwright
from pathlib import Path
from shoot import serve
import base64,json
R=Path(__file__).resolve().parents[1];port,stop=serve(str(R))
with sync_playwright()as pw:
 b=pw.chromium.launch(channel='msedge');p=b.new_page();p.goto(f'http://127.0.0.1:{port}/docs/previews/opening_storyboard_1024/video.html');p.wait_for_function('document.querySelector("video").readyState>=2')
 for t in [2,6,11,18]:
  data=p.evaluate('''async t=>{const v=document.querySelector('video');v.pause();v.currentTime=t;await new Promise(r=>v.addEventListener('seeked',r,{once:true}));await new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)));const c=document.createElement('canvas');c.width=v.videoWidth;c.height=v.videoHeight;c.getContext('2d').drawImage(v,0,0);return c.toDataURL().split(',')[1];}''',t)
  (R/f'_shots/intro_order_1024/video-{t}.png').write_bytes(base64.b64decode(data))
 print(p.evaluate('({width:document.querySelector("video").videoWidth,height:document.querySelector("video").videoHeight,error:document.querySelector("video").error})'));b.close()
stop()
