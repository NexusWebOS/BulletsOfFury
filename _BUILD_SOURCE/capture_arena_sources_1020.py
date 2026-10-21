from pathlib import Path
from PIL import Image
from playwright.sync_api import sync_playwright
import ast,base64,json,sys,http.server,io
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
A=R/'_ART_SOURCES/arena_download_1020';A.mkdir(exist_ok=True);(A/'references').mkdir(exist_ok=True)
SETUP=next(ast.literal_eval(n.value) for n in ast.parse((R/'_BUILD_SOURCE/probe_feedback_1002.py').read_text(encoding='utf-8')).body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='SETUP' for t in n.targets))
http.server.ThreadingHTTPServer.request_queue_size=128;port,stop=shoot.serve(str(R));rows=[]
try:
 with sync_playwright() as pw:
  b=pw.chromium.launch(channel='msedge');p=b.new_page(viewport=dict(width=1366,height=768));p.set_default_timeout(180000)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>4');p.evaluate(shoot.TRAP_RAF)
  for name,stage,scroll in [('jungle',1,1500),('lava',2,1500),('space',5,1000),('sky',6,1000)]:
   p.evaluate(SETUP,dict(stage=stage,pilot='cole',diff='normal'))
   p.wait_for_function('()=>{ASSETS.ready=true;stageLoadTick();const c=_levelCfg();return stageLoadReady(run.stage)&&XART.rdy(c.master)}')
   p.evaluate('''s=>{mapScroll=s;shake=0;ctx.setTransform(SS,0,0,SS,0,0);drawBG(0);}''',scroll)
   (A/'references'/(name+'-native.png')).write_bytes(base64.b64decode(p.evaluate('cv.toDataURL().split(",")[1]')))
   row=p.evaluate('({stage:run.stage,cfg:_levelCfg(),world:worldWidth(),view:[viewW(),viewH()],masterPath:XART._src[_levelCfg().master]})');rows.append(row)
   if stage==2:
    p.wait_for_function('()=>_liquidFrames(_levelCfg().liquid).every(f=>ASSETS.rdy(f))')
    for i in range(8):
     d=p.evaluate('''i=>{const f=_liquidFrames(_levelCfg().liquid)[i],c=document.createElement('canvas');c.width=f.naturalWidth;c.height=f.naturalHeight;c.getContext('2d').drawImage(f,0,0);return c.toDataURL().split(',')[1]}''',i)
     (A/'references'/('original-lava-'+str(i)+'.png')).write_bytes(base64.b64decode(d))
  b.close()
finally:stop()
(A/'references/native.json').write_text(json.dumps(rows,indent=2),encoding='utf-8');print(json.dumps(rows))
