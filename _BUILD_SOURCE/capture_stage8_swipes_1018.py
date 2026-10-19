"""Capture the delivered native preview, including both real arm sweeps."""
from pathlib import Path
from io import BytesIO
import http.server
from PIL import Image
from playwright.sync_api import sync_playwright
import shoot
R=Path(__file__).resolve().parents[1];O=R/'_shots/stage8_swipes_1018';http.server.ThreadingHTTPServer.request_queue_size=128
port,stop=shoot.serve(str(R))
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(channel='msedge',args=['--mute-audio']);p=br.new_page(viewport=dict(width=1280,height=900));p.set_default_timeout(180000)
  p.add_init_script("Object.defineProperty(navigator,'getGamepads',{value:()=>[]});")
  p.goto(f'http://127.0.0.1:{port}/docs/previews/stage8_pixellab_1018/index.html?scene=swipes&difficulty=normal&revision=stage8-swipes-1018')
  p.wait_for_function('!document.querySelector("#replay").disabled');f=p.frames[1];f.evaluate(shoot.TRAP_RAF);p.wait_for_timeout(40)
  for scene in ['swipes','ghostswipes','scythes','volcanoswipes']:
   if p.input_value('#scene')!=scene:p.select_option('#scene',scene)
   else:p.click('#replay')
   p.wait_for_function('!document.querySelector("#replay").disabled');shots=[]
   for i in range(58):
    f.evaluate('()=>{for(let i=0;i<5;i++){updatePlay(1/60);drawWorld(1/60);}SC12.refresh();__bofFit();}');p.wait_for_timeout(5)
    im=Image.open(BytesIO(p.screenshot(type='png'))).convert('RGB');shots.append(im)
    if i in [13,18,35,39]:im.save(O/(scene+'-actual-'+str(i)+'.png'))
   shots[0].save(O/(scene+'.gif'),save_all=True,append_images=shots[1:],duration=83,loop=0,optimize=False)
   print(scene+' captured through the real game and side HUD',flush=True)
  br.close()
finally:stop()
