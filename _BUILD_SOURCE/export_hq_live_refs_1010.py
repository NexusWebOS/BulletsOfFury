"""Export actual game-context ship references for live HQ cinematics."""
from pathlib import Path
import sys,base64,json,hashlib
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'_BUILD_SOURCE'));import shoot
OUT=ROOT/'_ART_SOURCES/hq_live_1010/references';OUT.mkdir(parents=True,exist_ok=True)
port,stop=shoot.serve(str(ROOT));records=[]
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch();p=br.new_page();p.set_default_timeout(120000)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>4');p.evaluate(shoot.TRAP_RAF)
  keys=['ship_'+k for k in ['cole','axel','freezer','yuri','maverick','falva','lizzie','decker','juggernaut']]
  keys+=['fb2_stealth_red','fb2_stealth_green','fb2_stealth_orange','fx_retina_lock_0','hud_radar_bezel_0924']
  for key in keys:
   try:
    p.wait_for_function('k=>XART.rdy(k)',arg=key,polling=50,timeout=15000)
    q=p.evaluate("k=>{const im=XART.get(k),c=document.createElement('canvas');c.width=im.width;c.height=im.height;c.getContext('2d').drawImage(im,0,0);return {w:c.width,h:c.height,data:c.toDataURL('image/png').split(',')[1]};}",key)
    dest=OUT/(key+'.png');dest.write_bytes(base64.b64decode(q.pop('data')))
    records.append(dict(key=key,**q,path=dest.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(dest.read_bytes()).hexdigest()))
    print('Exported '+key,flush=True)
   except Exception as e:print('Unavailable '+key+': '+str(e).splitlines()[0],flush=True)
  br.close()
finally:stop()
(OUT/'manifest.json').write_text(json.dumps(records,indent=2)+'\n',encoding='utf-8')
