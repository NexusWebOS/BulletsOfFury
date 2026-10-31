from pathlib import Path
from playwright.sync_api import sync_playwright
import json,sys
R=Path(__file__).resolve().parents[3];sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
from serve_bof_1013 import AssetServer
shoot.http.server.ThreadingHTTPServer=AssetServer
O=R/'_shots/base33';errors=[];checks=[];port,stop=shoot.serve(str(R))
def check(n,v):checks.append({'name':n,'passed':bool(v)});print(n,bool(v),flush=True)
try:
 with sync_playwright()as pw:
  b=pw.chromium.launch();p=b.new_page(viewport={'width':1440,'height':1100});p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda e:errors.append(e.text)if e.type=='error'else None)
  p.goto(f'http://127.0.0.1:{port}/expansion/topdown/art/base33/preview.html',wait_until='domcontentloaded');p.wait_for_function('ready&&pack',timeout=120000)
  check('previewloads16props',p.locator('#gallery .card').count()==16)
  p.wait_for_timeout(400)
  check('pausedpreviewhasactualrenderedpixels',p.evaluate('(()=>{const q=frame.contentWindow.document.getElementById("screen"),d=q.getContext("2d").getImageData(0,0,q.width,q.height).data;let n=0;for(let i=0;i<d.length;i+=400)if(d[i]+d[i+1]+d[i+2]>60)n++;return n>100;})()'))
  p.screenshot(path=str(O/'preview_page.png'),full_page=True)
  for section in ['chute','cover','low','vent','exit']:
   p.click(f'[data-section="{section}"]');p.wait_for_timeout(50);check(section+'sectionready',p.evaluate("frame.contentWindow.TD.game.state==='play'"))
  p.click('[data-section="chute"]');p.click('#play');p.wait_for_timeout(1000);check('previewplaysrealgameclock',p.evaluate('frame.contentWindow.TD.game.escape29.t>.7'));p.click('#play');check('previewcanpause',p.locator('#state').inner_text()=='Paused')
  for group,count in [('walls',12),('recess',4),('icons',16),('fx',4)]:p.click(f'[data-group="{group}"]');check(group+'gallery',p.locator('#gallery .card').count()==count)
  p.locator('#gallery').screenshot(path=str(O/'preview_effects.png'));check('nobrowsererrors',not errors)
  (O/'preview_report.json').write_text(json.dumps({'checks':checks,'errors':errors},indent=2),encoding='utf-8');b.close()
finally:stop()
sys.exit(0 if all(c['passed']for c in checks)and not errors else 1)
