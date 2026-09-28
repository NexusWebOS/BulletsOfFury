import json
from pathlib import Path
from playwright.sync_api import sync_playwright
import shoot as sh
root=Path(sh.GAME);out=root/'_shots/furious_0927';release=root.parent/'release_0927/BulletsOfFury';port,stop=sh.serve(str(release))
try:
 with sync_playwright() as pw:
  b=pw.chromium.launch(args=['--no-sandbox','--mute-audio']);p=b.new_page(viewport={'width':1360,'height':960});errs=[];bad=[]
  p.on('pageerror',lambda e:errs.append(str(e)));p.on('response',lambda r:bad.append({'status':r.status,'url':r.url}) if r.status>=400 else None)
  p.goto(f'http://127.0.0.1:{port}/index.html',timeout=120000);p.wait_for_function('()=>window.__bofFrames>4',timeout=120000);p.evaluate(sh.TRAP_RAF)
  assets=p.evaluate('''async()=>{const names=['realm_terrain','realm_fleet','chromium_actions','stagex_card','stagex_terrain','realm_ordnance','realm_boss','rebel_pitch'];return await Promise.all(names.map(async n=>{const im=new Image();im.src='assets/game/furious_review_0927/'+n+'.webp';await im.decode();return {name:n,w:im.width,h:im.height};}));}''')
  p.evaluate("()=>{run.mode='arcade';run.pilot='yuri';for(let s=1;s<=9;s++){run.stage=s;curStage=STAGES[s-1];beginStage(s);}beginStage(8);}");p.wait_for_timeout(2500)
  p.evaluate('()=>{ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);}');p.screenshot(path=str(out/'package-stage8.png'))
  report={'assets':assets,'errors':errs,'failed_http':bad};(out/'package-browser.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print(json.dumps(report));assert not errs and not bad;b.close()
finally:stop()
