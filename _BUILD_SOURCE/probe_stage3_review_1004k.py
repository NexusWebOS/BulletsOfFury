from pathlib import Path
from playwright.sync_api import sync_playwright
import shoot as sh
import json,base64,sys
R=Path(__file__).resolve().parents[1];O=R/'_shots/stage3_combat_1004k';port,stop=sh.serve(str(R));checks=[];errors=[]
try:
 with sync_playwright() as pw:
  b=pw.chromium.launch(args=['--no-sandbox','--autoplay-policy=no-user-gesture-required']);p=b.new_page(viewport={'width':1200,'height':900})
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:500]) if m.type=='error' or 'draw error' in m.text else None)
  p.goto(f'http://127.0.0.1:{port}/_shots/stage3_combat_1004k/review.html');p.locator('#safe').check()
  for kind in ['frostcruiser','cryospear','stage']:
   p.locator('button[data-kind="'+kind+'"]').click();p.wait_for_function('()=>document.querySelector("#status").textContent==="Furious encounter ready."',timeout=90000)
   f=p.frame_locator('#arena');fr=p.frames[-1];fr.wait_for_function('()=>window.__bofFrames>10',timeout=90000)
   fr.evaluate(sh.TRAP_RAF);fr.evaluate('()=>{ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);}')
   s=fr.evaluate('()=>({stage:run.stage,pilot:run.pilot,state,play:GS.PLAY,preview:!!window.__map4hPreviewStorage,ship:(boss||subBoss)?._ship,lives:run.lives,frames:window.__bofFrames})')
   ok=s['stage']==3 and s['state']==s['play'] and s['preview'] and isinstance(s['lives'],(int,float)) and s['lives']>0 and (kind=='stage' or s['ship']==kind)
   checks.append({'name':kind+' playable review button','ok':ok,'state':s});print(('OK ' if ok else 'FAIL ')+kind,flush=True)
   (O/('review-'+kind+'.png')).write_bytes(base64.b64decode(fr.evaluate('()=>cv.toDataURL().split(",")[1]')))
  checks.append({'name':'review zero browser errors','ok':not errors});b.close()
finally:stop();(O/'review-verification.json').write_text(json.dumps({'checks':checks,'errors':errors},indent=2),encoding='utf-8')
sys.exit(0 if all(q['ok'] for q in checks) and not errors else 1)
