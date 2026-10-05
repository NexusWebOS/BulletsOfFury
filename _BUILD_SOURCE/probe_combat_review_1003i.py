"""Smoke test the review controls and its real playable encounter."""
from pathlib import Path
import json,http.server,sys
from playwright.sync_api import sync_playwright
import shoot as sh
R=Path(__file__).resolve().parents[1];O=R/'_shots/combat_1003i';errors=[];checks=[]
port,stop=sh.serve(str(R));http.server.SimpleHTTPRequestHandler.log_message=lambda *a,**k:None
def ck(v,n):checks.append({'ok':bool(v),'name':n});print(('PASS ' if v else 'FAIL ')+n,flush=True)
try:
 with sync_playwright() as pw:
  b=pw.chromium.launch(args=['--no-sandbox','--autoplay-policy=no-user-gesture-required']);p=b.new_page(viewport={'width':1280,'height':920})
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:500]) if m.type=='error' else None)
  p.goto(f'http://127.0.0.1:{port}/_shots/combat_1003i/review.html');p.wait_for_function('()=>document.images[0].complete')
  ck(p.locator('audio').count()==20,'twenty sound previews available')
  p.screenshot(path=str(O/'review-page.png'))
  p.locator('#launch').click();p.wait_for_function('()=>document.querySelector("#launch").textContent.includes("Restart")',timeout=120000)
  f=p.frames[-1];f.wait_for_function('()=>subBoss?._av3Reaver?.parts.length===6',timeout=60000)
  ck(f.evaluate('()=>state===GS.PLAY&&run.stage===2&&subBoss._ship==="magmaward"'),'review launches the actual modular Stage 2 fight')
  ck(f.evaluate('()=>diffKey==="furious"&&BOFA.music.mini2.endsWith("Level2mb.mp3")'),'selected difficulty and Stage 2 miniboss music resolve')
  f.wait_for_timeout(2000);p.screenshot(path=str(O/'review-playable.png'))
  p.locator('#launch').click();p.wait_for_function('()=>document.querySelector("#launch").textContent.includes("Restart")',timeout=120000)
  ck(not errors,'review and restart have no page/console errors');b.close()
finally:stop();(O/'review-checks.json').write_text(json.dumps({'checks':checks,'errors':errors},indent=2)+'\n')
sys.exit(0 if all(q['ok'] for q in checks) and not errors else 1)
