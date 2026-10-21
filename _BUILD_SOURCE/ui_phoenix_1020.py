from pathlib import Path
import json
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];O=R/'_shots/dracodia_phoenix_1020';errors=[];rows=[]
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge');p=b.new_page(viewport=dict(width=1440,height=1000));p.on('pageerror',lambda e:errors.append(str(e)));p.on('response',lambda r:errors.append(str(r.status)+' '+r.url) if r.status>=400 else None)
 p.goto('http://127.0.0.1:8794/_shots/dracodia_phoenix_1020/review.html');p.wait_for_function('document.fonts.status==="loaded"');p.wait_for_function('document.querySelector("#preview").naturalWidth>0')
 for key in ['cannon','sweep','spin900','ring','coreLaser','rotor','rollerball','eyeSweep','rake']:
  p.locator('[data-attack="'+key+'"]').click();p.wait_for_function('document.querySelector("#preview").complete&&document.querySelector("#preview").naturalWidth>0');rows.append(p.evaluate('({title:document.querySelector("#title").textContent,src:document.querySelector("#preview").getAttribute("src"),width:document.querySelector("#preview").naturalWidth})'))
 p.locator('[data-attack="coreLaser"]').click();p.wait_for_timeout(900);p.screenshot(path=str(O/'review-desktop.png'));p.set_viewport_size(dict(width=540,height=940));p.wait_for_timeout(300);p.screenshot(path=str(O/'review-narrow.png'));overflow=p.evaluate('document.documentElement.scrollWidth>innerWidth');b.close()
(O/'review-ui.json').write_text(json.dumps(dict(rows=rows,overflow=overflow,errors=errors),indent=2));print(json.dumps(dict(previews=len(rows),overflow=overflow,errors=errors)));raise SystemExit(bool(errors) or overflow)
