from pathlib import Path
import json,http.server,sys
from playwright.sync_api import sync_playwright
import shoot as sh
R=Path(__file__).resolve().parents[1];O=R/'_shots/campaign_focus_1004b';errors=[];checks=[]
port,stop=sh.serve(str(R));http.server.SimpleHTTPRequestHandler.log_message=lambda *a,**k:None
try:
 with sync_playwright() as pw:
  browser=pw.chromium.launch(args=['--no-sandbox','--autoplay-policy=no-user-gesture-required']);p=browser.new_page(viewport={'width':1440,'height':1000})
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:500]) if m.type=='error' else None)
  p.goto(f'http://127.0.0.1:{port}/_shots/campaign_focus_1004b/review.html',timeout=120000)
  p.evaluate('()=>localStorage.setItem("cf4-practice-marker","preserved")')
  p.screenshot(path=str(O/'review-page.png'),full_page=False)
  for mode in ['rebels','gang','finale','dracula','knight','harrier-map','rebels-map','portal']:
   p.locator('[data-mode="'+mode+'"]').click();p.wait_for_function('()=>document.querySelector("#status").textContent.includes("ready.")',timeout=120000)
   f=p.frame_locator('#arena');game=p.frames[-1];game.wait_for_function('()=>window.__bofFrames>8',timeout=120000);p.wait_for_timeout(1600)
   row=game.evaluate('()=>({stage:run.stage,state,kind:boss?.kind,encounter:j3State(boss)?.encounter,mimic:j3State(boss)?.mimic,allies:s6Wing?.ships.length,gang:boss?._rebels?.gang1004?.gang,pending:campaign.stageX1004?.route})')
   good=(row.get('allies')==4 and row.get('kind')=='rebelsquad') if mode in ['rebels','gang'] else (row.get('encounter')==0) if mode=='finale' else (row.get('encounter')==2) if mode=='dracula' else (row.get('mimic')==5) if mode=='knight' else (row.get('state')=='stagesel' and row.get('pending')==('left' if mode=='harrier-map' else 'right')) if mode.endswith('-map') else row.get('state')=='warpentry'
   game.evaluate('()=>localStorage.setItem("cf4-practice-marker","overwritten")');safe=p.evaluate('()=>localStorage.getItem("cf4-practice-marker")==="preserved"')
   checks.append({'mode':mode,'ok':bool(good and safe),'state':row,'saveWritesBlocked':safe});print(mode,good,safe,flush=True)
   if mode in ['rebels','knight']:p.locator('#arena').screenshot(path=str(O/('review-'+mode+'.png')))
  browser.close()
finally:stop()
data={'checks':checks,'errors':errors};(O/'review-report.json').write_text(json.dumps(data,indent=2),encoding='utf-8');print(json.dumps(data))
sys.exit(bool(errors) or any(not c['ok'] for c in checks))
