from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image,ImageDraw
import sys,base64,json,hashlib
ROOT=Path('D:/BOF-Downloads/2026-11-14/RevG-source');OUT=ROOT/'_shots/prototype_dispatch_1114'
sys.path.insert(0,str(ROOT/'_BUILD_SOURCE'));import shoot
records=[];errors=[]
with sync_playwright()as pw:
 b=pw.chromium.launch(args=['--no-sandbox']);p=b.new_page();p.set_default_timeout(120000)
 p.on('pageerror',lambda e:errors.append(str(e)))
 p.goto('http://127.0.0.1:8765/index.html?kit-reference=1114');p.wait_for_function('window.__bofFrames>6');p.evaluate(shoot.TRAP_RAF)
 for pk in p.evaluate('CP15_ART.pilots'):
  key='ship_'+pk;p.wait_for_function('k=>XART.rdy(k)',arg=key,polling=50)
  q=p.evaluate("k=>{const im=XART.get(k),c=document.createElement('canvas');c.width=im.width;c.height=im.height;c.getContext('2d').drawImage(im,0,0);return{w:c.width,h:c.height,data:c.toDataURL().split(',')[1]};}",key)
  dest=OUT/(key+'.png');dest.write_bytes(base64.b64decode(q.pop('data')));records.append({'pilot':pk,'key':key,**q,'file':dest.name,'sha256':hashlib.sha256(dest.read_bytes()).hexdigest()})
 b.close()
canvas=Image.new('RGB',(960,720),'#0c1726');d=ImageDraw.Draw(canvas)
for i,r in enumerate(records):
 im=Image.open(OUT/r['file']).convert('RGBA');im.thumbnail((260,205),Image.Resampling.NEAREST);x=i%3*320;y=i//3*240;canvas.paste(im,(x+(320-im.width)//2,y),im);d.text((x+12,y+214),r['pilot'].upper(),fill='#e9f1ff')
canvas.save(OUT/'actual-aircraft.jpg',quality=95)
(OUT/'aircraft-refs.json').write_text(json.dumps({'records':records,'errors':errors},indent=2),encoding='utf-8');print('Exported all nine actual unconverted aircraft from native XART.')
assert not errors
