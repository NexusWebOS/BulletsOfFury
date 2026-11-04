from pathlib import Path
import sys,base64,json
from playwright.sync_api import sync_playwright
W=Path(__file__).resolve().parent;O=W/'revision-refs';O.mkdir(exist_ok=True)
R=Path(r'C:\Users\Mike\Desktop\Github Coding\BulletsOfFury');sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
port,stop=shoot.serve(str(R))
try:
 with sync_playwright()as pw:
  br=pw.chromium.launch(channel='msedge');p=br.new_page();p.set_default_timeout(90000)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>4');p.evaluate(shoot.TRAP_RAF)
  for name in ['interceptor','drone','blue']:
   a=p.evaluate('n=>S811_ART.models[n]?.full',name)
   if not a:continue
   p.wait_for_function('a=>XART.rdy(a.key)',arg=a)
   data=p.evaluate('''a=>{const im=XART.get(a.key),c=document.createElement('canvas');c.width=a.cell*3;c.height=a.cell;const d=c.getContext('2d');[0,8,16].forEach((f,i)=>d.drawImage(im,f%a.cols*a.cell,Math.floor(f/a.cols)*a.cell,a.cell,a.cell,i*a.cell,0,a.cell,a.cell));return c.toDataURL().split(',')[1]}''',a)
   (O/(name+'.png')).write_bytes(base64.b64decode(data));print('Exported current alien '+name,flush=True)
  br.close()
finally:stop()
