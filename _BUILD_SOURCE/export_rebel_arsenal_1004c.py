"""Export resolved, authored Maverick cells through the game's own canvas."""
from pathlib import Path
import base64, sys
from playwright.sync_api import sync_playwright
import shoot
R=Path(__file__).resolve().parents[1]
O=R/'_ART_SOURCES/rebel_arsenal_1004c/authored';O.mkdir(parents=True,exist_ok=True)
keys=[f'nhxsb_g_{i}' for i in range(3)]+[f'fchgc_{i}' for i in range(4)]+[f'nhxb_g_{i}' for i in range(5)]
port,stop=shoot.serve(str(R))
try:
 with sync_playwright() as pw:
  b=pw.chromium.launch(args=['--no-sandbox']);p=b.new_page()
  p.goto(f'http://127.0.0.1:{port}/index.html',timeout=120000)
  p.wait_for_function('()=>window.__bofFrames>4',timeout=120000);p.evaluate(shoot.TRAP_RAF)
  p.evaluate('(keys)=>keys.forEach(k=>XART.rdy(k))',keys)
  p.wait_for_function('(keys)=>keys.every(k=>XART.rdy(k))',arg=keys,timeout=120000)
  for key in keys:
   png=p.evaluate('''k=>{const im=XART.get(k),c=document.createElement('canvas');c.width=im.width;c.height=im.height;
    const g=c.getContext('2d');g.drawImage(im,0,0);return c.toDataURL().split(',')[1];}''',key)
   (O/(key+'.png')).write_bytes(base64.b64decode(png))
  b.close()
finally:stop()
print(f'Exported {len(keys)} authored source cells.')
