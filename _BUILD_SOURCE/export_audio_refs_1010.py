from pathlib import Path
import sys,base64
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'_BUILD_SOURCE'));import shoot
OUT=ROOT/'_ART_SOURCES/audio_1010/references';OUT.mkdir(parents=True,exist_ok=True)
port,stop=shoot.serve(str(ROOT))
try:
 with sync_playwright() as pw:
  b=pw.chromium.launch();p=b.new_page();p.set_default_timeout(120000)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>4');p.evaluate(shoot.TRAP_RAF)
  for key in ['mwfx_fire_shield_0','fzt_chain_link','fzt_chain_edge','ship_voss','r30_dracula_head']:
   try:
    p.wait_for_function('k=>XART.rdy(k)',arg=key,polling=50,timeout=12000)
    data=p.evaluate("k=>{const im=XART.get(k),c=document.createElement('canvas');c.width=im.width;c.height=im.height;c.getContext('2d').drawImage(im,0,0);return c.toDataURL('image/png').split(',')[1];}",key)
    (OUT/(key+'.png')).write_bytes(base64.b64decode(data));print('Exported '+key,flush=True)
   except Exception as e:print('Unavailable '+key+': '+str(e).splitlines()[0],flush=True)
  b.close()
finally:stop()
