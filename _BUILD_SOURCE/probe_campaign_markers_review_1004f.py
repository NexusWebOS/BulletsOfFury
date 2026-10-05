"""Verify marker review buttons in the actual uninterrupted Chromium game."""
from pathlib import Path
from playwright.sync_api import sync_playwright
import shoot as sh
import json,sys
R=Path(__file__).resolve().parents[1];O=R/'_shots/campaign_markers_1004f';checks=[];errors=[]
def ck(v,n):checks.append({'ok':bool(v),'name':n});print(('PASS ' if v else 'FAIL ')+n,flush=True)
port,stop=sh.serve(str(R))
try:
 with sync_playwright() as pw:
  b=pw.chromium.launch(args=['--no-sandbox','--autoplay-policy=no-user-gesture-required']);p=b.new_page(viewport={'width':1600,'height':1150})
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
  p.goto(f'http://127.0.0.1:{port}/_shots/campaign_markers_1004f/review.html',timeout=120000);p.wait_for_function('()=>ready',timeout=120000)
  g=p.frames[1];g.wait_for_function('()=>sselBoot===0&&MAP4E.readiness&&XART.rdy("map4f_flagx")',timeout=120000)
  for k in ['4','5','7','8','1','xl','xh','x','hq','0']:
   p.locator('[data-stage="'+k+'"]').click();p.wait_for_timeout(600)
   if k=='xl':v=g.evaluate('()=>MAP4E.xPreview&&!Rival24.mapAvailable')
   elif k in ['x','xh']:v=g.evaluate('(r)=>CF4.focus&&campaign.stageX1004.route===r','right' if k=='x' else 'left')
   elif k=='hq':v=g.evaluate('()=>cmap2.cam.z===.55&&cmap2.cam.x===MAP4E.hq[0]&&XART.rdy("map4e_region_hq")')
   elif k=='0':v=g.evaluate('()=>!MAP4E.focus&&!MAP4E.xPreview&&!CF4.focus')
   else:v=g.evaluate('(k)=>sselCursor===k&&MAP4E.focus',int(k))
   ck(v,'live review selects '+k)
  p.wait_for_timeout(1700);p.screenshot(path=str(O/'review-screen.png'),full_page=True)
  ck(not errors,'review has zero page and console errors');b.close()
finally:stop()
(O/'review-checks.json').write_text(json.dumps({'checks':checks,'errors':errors},indent=2)+'\n',encoding='utf-8')
print('RESULT',sum(c['ok'] for c in checks),'/',len(checks));sys.exit(bool(errors) or any(not c['ok'] for c in checks))
