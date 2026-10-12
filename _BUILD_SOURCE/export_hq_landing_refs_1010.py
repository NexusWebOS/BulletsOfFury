"""Export the current Furyship and accepted pilot bodies through native XART."""
from pathlib import Path
import sys, base64, json, hashlib
from PIL import Image
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'_BUILD_SOURCE'));import shoot
OUT=ROOT/'_ART_SOURCES/hq_landing_1010/references';OUT.mkdir(parents=True,exist_ok=True)
PILOTS=['cole','axel','freezer','yuri','maverick','falva','lizzie','decker','juggernaut']
records=[];port,stop=shoot.serve(str(ROOT))
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch();p=br.new_page();p.set_default_timeout(120000)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>4');p.evaluate(shoot.TRAP_RAF)
  p.evaluate('furyShipWarm()')
  p.wait_for_function('furyShipReady()',polling=50)
  for pilot in PILOTS:
   key='cole_body_0922' if pilot=='cole' else pilot+'_body_0'
   p.wait_for_function('k=>XART.rdy(k)',arg=key,polling=50)
   for kind in ['ship','body']:
    q=p.evaluate("q=>{const im=q.kind==='ship'?furyShipCanvas('base',q.pilot):XART.get(q.key),c=document.createElement('canvas');c.width=im.width;c.height=im.height;c.getContext('2d').drawImage(im,0,0);return {w:c.width,h:c.height,data:c.toDataURL('image/png').split(',')[1]};}",dict(kind=kind,pilot=pilot,key=key))
    dest=OUT/(pilot+'_'+kind+'.png');dest.write_bytes(base64.b64decode(q.pop('data')))
    records.append(dict(pilot=pilot,role=kind,key='fury_base|'+pilot if kind=='ship' else key,**q,path=dest.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(dest.read_bytes()).hexdigest()))
   # One native reference plate; only a common 1:1 crop and transparent padding.
   ship=Image.open(OUT/(pilot+'_ship.png')).convert('RGBA');body=Image.open(OUT/(pilot+'_body.png')).convert('RGBA')
   ship=ship.crop(ship.getbbox());body=body.crop(body.getbbox())
   w=ship.width+body.width+64;h=max(ship.height,body.height)+48
   w+=w%2;h+=h%2;plate=Image.new('RGBA',(w,h))
   plate.alpha_composite(ship,(16,(h-ship.height)//2));plate.alpha_composite(body,(ship.width+48,(h-body.height)//2))
   plate.save(OUT/(pilot+'_identity.png'))
   print('Exported '+pilot+' current Furyship and accepted pilot body',flush=True)
  br.close()
finally:stop()
(OUT/'manifest.json').write_text(json.dumps(records,indent=2)+'\n',encoding='utf-8')
