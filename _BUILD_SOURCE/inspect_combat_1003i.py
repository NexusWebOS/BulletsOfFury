from pathlib import Path
import json,base64,sys
from playwright.sync_api import sync_playwright
import shoot as sh
R=Path(__file__).resolve().parents[1];O=R/'_shots/combat_1003i';O.mkdir(parents=True,exist_ok=True)
port,stop=sh.serve(str(R))
try:
 with sync_playwright() as pw:
  b=pw.chromium.launch(args=['--no-sandbox','--autoplay-policy=no-user-gesture-required']);p=b.new_page(viewport={'width':1100,'height':960})
  p.goto(f'http://127.0.0.1:{port}/index.html',timeout=120000);p.wait_for_function('()=>window.__bofFrames>4',timeout=120000);p.evaluate(sh.TRAP_RAF)
  p.wait_for_function('()=>XART.rdy("nsb_inferno_reaver")',timeout=60000)
  data=p.evaluate('''()=>{const im=XART.get('nsb_inferno_reaver'),c=document.createElement('canvas');c.width=im.width;c.height=im.height;c.getContext('2d').drawImage(im,0,0);return c.toDataURL().split(',')[1]}''')
  (O/'inferno-reference.png').write_bytes(base64.b64decode(data))
  print(p.evaluate('()=>JSON.stringify({sub:SUBBOSS,bosses:STAGES.map(s=>s.boss),sfx:Object.keys(Audio.SFX),source:XART._src.nsb_inferno_reaver})'))
  b.close()
finally:stop()
