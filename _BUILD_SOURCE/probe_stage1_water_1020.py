from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image
import ast,base64,json,sys,io,argparse,http.server
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
O=R/'_shots/stage1_water_1020';O.mkdir(exist_ok=True)
SETUP=next(ast.literal_eval(n.value) for n in ast.parse((R/'_BUILD_SOURCE/probe_feedback_1002.py').read_text(encoding='utf-8')).body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='SETUP' for t in n.targets))
ap=argparse.ArgumentParser();ap.add_argument('--before',action='store_true');a=ap.parse_args()
http.server.ThreadingHTTPServer.request_queue_size=128
port,stop=shoot.serve(str(R));errors=[]
try:
 with sync_playwright() as pw:
  b=pw.chromium.launch(channel='msedge');p=b.new_page(viewport=dict(width=1366,height=768));p.set_default_timeout(120000)
  p.route('**/favicon.ico',lambda r:r.fulfill(status=204,body=''))
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:500]) if m.type=='error' else None)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>4&&typeof ht27Stop==="function"');p.evaluate(shoot.TRAP_RAF)
  p.evaluate(SETUP,dict(stage=1,pilot='cole',diff='normal'))
  p.wait_for_function('()=>{const c=_levelCfg(1);_liquidFrames(c.liquid);return XART.rdy(c.master)&&_legacyWater()?.some(f=>ASSETS.rdy(f))}')
  p.evaluate('()=>{mapScroll=0;shake=0;ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);SC12.refresh();}')
  label='before' if a.before else 'after'
  (O/(label+'.png')).write_bytes(base64.b64decode(p.evaluate('cv.toDataURL().split(",")[1]')));p.screenshot(path=str(O/(label+'-desktop.png')))
  data=p.evaluate('''()=>{const f=_legacyWater().find(f=>ASSETS.rdy(f)),c=document.createElement('canvas');c.width=f.naturalWidth;c.height=f.naturalHeight;c.getContext('2d').drawImage(f,0,0);return {png:c.toDataURL().split(',')[1],width:c.width,height:c.height,cfg:_levelCfg(1),map:mapScroll,world:worldWidth()};}''')
  (O/(label+'-native-tile.png')).write_bytes(base64.b64decode(data.pop('png')))
  (O/(label+'-reference.json')).write_text(json.dumps(data,indent=2),encoding='utf-8')
  print(json.dumps({'reference':data,'errors':errors}),flush=True);b.close()
finally:stop()
