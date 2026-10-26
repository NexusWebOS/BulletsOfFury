from barrage_review_common_1025 import ROOT,OUT,boot,advance
from shoot import serve
from playwright.sync_api import sync_playwright
from pathlib import Path
import base64,json

port,stop=serve(str(ROOT));errors=[];folder=OUT/'art';folder.mkdir(exist_ok=True)
try:
 with sync_playwright() as pw:
  b=pw.chromium.launch(channel='msedge',args=['--autoplay-policy=no-user-gesture-required'])
  context=b.new_context(viewport={'width':1280,'height':800})
  p=boot(context,port,8,errors)
  keys=['nhd_primary_projectile_0','nhd_special_projectile_0','bpfx_muzzle_void_2','weapon_muzzle_toxic_1']
  for key in keys:
   p.wait_for_function('k=>XART.rdy(k)',arg=key,timeout=180000)
   payload=p.evaluate("""k=>{const im=XART.get(k),c=document.createElement('canvas');c.width=im.width;c.height=im.height;c.getContext('2d').drawImage(im,0,0);return c.toDataURL().split(',')[1];}""",key)
   (folder/(key+'.png')).write_bytes(base64.b64decode(payload))
  advance(p,'!reviewActor.enter&&reviewActor.y>100',100)
  p.evaluate('drawWorld(0)');p.screenshot(path=str(folder/'herald-native.png'))
  print(json.dumps({'errors':errors,'files':[str(v)for v in folder.glob('*.png')]}),flush=True)
  b.close()
finally:stop()
