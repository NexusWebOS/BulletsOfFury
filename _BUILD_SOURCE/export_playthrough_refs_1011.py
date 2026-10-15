"""Export live XART references and encounter descriptors for the October 11 review."""
from pathlib import Path
import base64,json
from playwright.sync_api import sync_playwright
import shoot
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'_ART_SOURCES/playthrough_1011/references';OUT.mkdir(parents=True,exist_ok=True)
port,stop=shoot.serve(str(ROOT))
try:
 with sync_playwright() as pw:
  b=pw.chromium.launch(args=['--mute-audio']);p=b.new_page();p.set_default_timeout(120000)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>4');p.evaluate(shoot.TRAP_RAF)
  desc=p.evaluate('''()=>{const ships=Object.fromEntries(['frostcruiser','rimewall','olivewarden','stormsovereign','infernoreaver'].map(k=>[k,SHIPBOSS[k]]));
   return {ships,rigs:typeof FMC_RIGS==='undefined'?{}:FMC_RIGS,keys:Object.keys(XART._src).filter(k=>/furnace|av3|ghost|r30_|logo|credits|difficulty/.test(k)).slice(0,350)};}''')
  (OUT/'native-descriptors.json').write_text(json.dumps(desc,indent=2),encoding='utf-8')
  keys=p.evaluate('''()=>['aa5_ghost_0','fzt_overload_wave','vile24_robot_gray'];''')
  for key in keys:
   p.wait_for_function('k=>XART.rdy(k)',arg=key,polling=50)
   data=p.evaluate('''k=>{const im=XART.get(k),c=document.createElement('canvas');c.width=im.width;c.height=im.height;c.getContext('2d').drawImage(im,0,0);return c.toDataURL('image/png').split(',')[1];}''',key)
   (OUT/(key+'.png')).write_bytes(base64.b64decode(data));print(key,flush=True)
  b.close()
finally:stop()
