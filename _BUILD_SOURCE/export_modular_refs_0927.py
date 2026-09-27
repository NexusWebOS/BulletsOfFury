import sys,base64,json,http.server
from pathlib import Path
import shoot as sh
from playwright.sync_api import sync_playwright
OUT=Path('_shots/modular_roster_0927/references');OUT.mkdir(parents=True,exist_ok=True)
http.server.SimpleHTTPRequestHandler.log_message=lambda *a:None
port,stop=sh.serve(sh.GAME)
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(args=['--no-sandbox','--mute-audio']);p=br.new_page()
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('()=>window.__bofFrames>4');p.evaluate(sh.TRAP_RAF)
  keys=p.evaluate("()=>['nsb_rimewall_intact','s4w_boss_idle','nsb_olivewarden_intact',...Object.keys(XART._src).filter(k=>/^(tlv|tlvb|s4w_).*(body|hull|idle|drone)/.test(k))]")
  print(json.dumps(keys))
  for k in keys[:18]:
   p.evaluate('(k)=>XART.rdy(k)',k);p.wait_for_function('(k)=>XART.rdy(k)',arg=k,timeout=20000)
   data=p.evaluate("k=>{const im=XART.get(k),c=document.createElement('canvas');c.width=im.width;c.height=im.height;c.getContext('2d').drawImage(im,0,0);return c.toDataURL();}",k)
   (OUT/(k+'.png')).write_bytes(base64.b64decode(data.split(',')[1]))
  br.close()
finally:stop()
