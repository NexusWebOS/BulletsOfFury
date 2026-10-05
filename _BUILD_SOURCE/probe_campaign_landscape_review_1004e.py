"""Exercise every live map-review button in a normal Chromium animation loop."""
from pathlib import Path
from playwright.sync_api import sync_playwright
import shoot as sh
import json,sys
R=Path(__file__).resolve().parents[1];O=R/'_shots/campaign_landscape_1004e';errors=[];checks=[]
def ck(v,n):checks.append({'ok':bool(v),'name':n});print(('PASS ' if v else 'FAIL ')+n,flush=True)
port,stop=sh.serve(str(R))
try:
 with sync_playwright() as pw:
  b=pw.chromium.launch(args=['--no-sandbox','--autoplay-policy=no-user-gesture-required']);p=b.new_page(viewport={'width':1600,'height':1150})
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
  p.goto(f'http://127.0.0.1:{port}/_shots/campaign_landscape_1004e/review.html',timeout=120000)
  p.wait_for_function('()=>ready',timeout=120000);game=p.frames[1];game.wait_for_function('()=>sselBoot===0&&MAP4E.readiness',timeout=30000)
  for key in ['1','2','3','4','5','6','7','8','9','x','0']:
   p.locator('[data-stage="'+key+'"]').click();p.wait_for_timeout(400)
   if key=='x':v=game.evaluate('()=>CF4.focus&&cf4Pending()')
   elif key=='0':v=game.evaluate('()=>!MAP4E.focus&&!CF4.focus')
   else:v=game.evaluate('(n)=>sselCursor===n&&MAP4E.focus&&campaign.bonusUnlocked===(n===9)',int(key))
   ck(v,'review selects '+('Stage '+key if key!='0' else 'full connected world'))
  p.wait_for_timeout(1700);p.screenshot(path=str(O/'review-screen.png'),full_page=True)
  ck(not errors,'review has zero page and console errors');b.close()
finally:stop()
(O/'review-checks.json').write_text(json.dumps({'checks':checks,'errors':errors},indent=2)+'\n',encoding='utf-8')
print('RESULT',sum(c['ok'] for c in checks),'/',len(checks));sys.exit(bool(errors) or any(not c['ok'] for c in checks))
