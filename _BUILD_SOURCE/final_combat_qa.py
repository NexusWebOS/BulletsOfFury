from pathlib import Path
import sys,json
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
O=R/'_shots/combat_pressure_1012';port,stop=shoot.serve(str(R));out={};errors=[]
try:
 with sync_playwright() as pw:
  b=pw.chromium.launch(channel='msedge');p=b.new_page(viewport={'width':1440,'height':1000});p.on('pageerror',lambda e:errors.append(str(e)));p.goto(f'http://localhost:{port}/index.html');p.wait_for_function('window.__bofFrames>4');p.evaluate(shoot.TRAP_RAF)
  out['audio']=p.evaluate('()=>{const w={t:0};const v=BOF_CHIP_PASS.firewall(w);const r={url:v.el.src,loop:v.el.loop};BOF_CHIP_PASS.stop(w);return r;}');assert out['audio']['url'].endswith('firewall_flamethrower_1012.mp3') and out['audio']['loop']
  p.evaluate('()=>{const root=document.createElement("div");root.style="position:fixed;inset:0;z-index:99999;overflow:auto;background:#10212d;color:white;padding:20px";document.body.append(root);for(const [n,a] of Object.entries(SPREAD1001_ART)){const h=document.createElement("h3");h.textContent=n+" / "+a.size.join(" × ");root.append(h);const im=document.createElement("img");im.src=a.path;im.style="max-width:95%;image-rendering:pixelated";root.append(im);}window.gallery=root;}');p.wait_for_function('Array.from(gallery.querySelectorAll("img")).every(i=>i.complete&&i.naturalWidth)');p.screenshot(path=str(O/'spread-bank-review.png'),full_page=True)
  out['spread']=p.evaluate('()=>Object.entries(SPREAD1001_ART).map(([name,a])=>({name,even:a.size.every(n=>n%2===0),frames:a.frames.length,consistent:a.frames.every(r=>r[2]===a.size[0]&&r[3]===a.size[1])}))');assert all(x['even'] and x['consistent'] for x in out['spread'])
  p.evaluate('gallery.remove()');b.close()
finally:stop()
out['errors']=errors;(O/'art-audio-verification.json').write_text(json.dumps(out,indent=2));assert not errors;print(json.dumps(out,indent=2))
