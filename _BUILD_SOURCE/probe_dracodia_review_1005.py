"""Exercise review controls in native Chromium; it runs actual engine routes."""
from pathlib import Path
from playwright.sync_api import sync_playwright
import json,sys
sys.path.insert(0,str(Path(__file__).resolve().parent));import shoot as sh
R=Path(__file__).resolve().parents[1];O=R/'_shots/dracodia_1005';report={'checks':[],'errors':[]};port,stop=sh.serve(str(R))
def ck(v,n):
 report['checks'].append({'ok':bool(v),'name':n});print(('PASS ' if v else 'FAIL ')+n,flush=True)
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(args=['--no-sandbox','--autoplay-policy=no-user-gesture-required']);p=br.new_page(viewport={'width':1300,'height':900})
  p.on('pageerror',lambda e:report['errors'].append(str(e)));p.on('console',lambda m:report['errors'].append(m.text[:500]) if m.type=='error' else None)
  p.goto(f'http://127.0.0.1:{port}/_shots/dracodia_1005/review.html',timeout=120000)
  ck(p.locator('#pilot option').count()==9,'review lists exactly nine real pilots')
  for scene in ['host','ghost','speech','combat','death']:
   p.locator('[data-scene="'+scene+'"]').click();p.wait_for_function('()=>document.querySelector("#status").textContent.startsWith("Live ")',timeout=120000)
   f=p.frame_locator('#game').owner.content_frame if False else p.frames[1]
   d=f.evaluate('()=>({mode:boss._r30.mode,phase:j3State(boss).encounter,n:seatList().length,pilot:run.pilot,locked:dr5Locked(),hp:j3State(boss).hp.length,seen:dr5State(boss).introSeen,dead:player.dead})')
   valid={'host':['encounterFall1003j','dr5Reform'],'ghost':['encounterFall1003j','dr5Reform'],'speech':['voidIntro1005','dr5Monologue'],'combat':['fight'],'death':['dr5Death']}[scene]
   ck(d['mode'] in valid and not d['dead'],'review '+scene+' starts actual requested engine sequence')
   ck(d['phase']==({'host':0,'ghost':1}.get(scene,2)),'review '+scene+' retains correct outer encounter')
   ck(f.evaluate('()=>{localStorage.setItem("dr5-review-write-test","blocked");return localStorage.getItem("dr5-review-write-test")===null;}'),'review '+scene+' blocks storage writes')
   if scene=='combat':ck(d['hp']==8 and d['seen'],'live combat retains eight copied health pools without speech replay')
  p.locator('#pilot').select_option('yuri');p.locator('#coop').check();p.locator('[data-scene="death"]').click();p.wait_for_function('()=>document.querySelector("#status").textContent.startsWith("Live ")',timeout=120000)
  f=p.frames[1];ck(f.evaluate('()=>run.pilot==="yuri"&&dr5State(boss).ships.length===2&&withSeat(2,()=>run.pilot)==="decker"'),'Yuri and Decker co-op review has two independently configured seats')
  ck(not report['errors'],'review has zero page or console errors');br.close()
finally:
 stop();(O/'review-verification.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
sys.exit(0 if all(c['ok'] for c in report['checks']) and not report['errors'] else 1)
