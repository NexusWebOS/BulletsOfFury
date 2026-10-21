from pathlib import Path
from playwright.sync_api import sync_playwright
import json
R=Path(__file__).resolve().parents[1];O=R/'_shots/cinematic_finish_1020';checks=[];errors=[]
def ck(n,ok):checks.append(dict(name=n,passed=bool(ok)));print(('PASS ' if ok else 'FAIL ')+n,flush=True)
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',args=['--autoplay-policy=no-user-gesture-required']);p=b.new_page(viewport=dict(width=1280,height=1000));p.set_default_timeout(120000);p.on('pageerror',lambda e:errors.append(str(e)))
 p.goto('http://127.0.0.1:8794/docs/previews/cinematic_finish_1020/index.html');p.wait_for_function('ready===true');g=p.frames[1]
 ck('Final cache revision loads both cinematic scripts',g.evaluate('typeof CE20!=="undefined"&&typeof CE20_ART!=="undefined"'))
 p.locator('[data-time="32"]').click();ck('Final scene link reaches the actual pilot epilogue',g.evaluate('CE20.last.scene==="pilot"'))
 p.locator('#play').click();p.wait_for_timeout(600);p.locator('#play').click();t=g.evaluate('drawVictory._t');p.wait_for_timeout(350);ck('Pause holds the native cinematic clock',abs(g.evaluate('drawVictory._t')-t)<.001)
 p.locator('#pilot').select_option('yuri');p.wait_for_function('ready===true');p.locator('#coop').check();p.wait_for_function('ready===true');p.locator('[data-time="9.4"]').click();ck('Yuri co-op uses Cole as the actual second pilot aircraft',g.evaluate('CE20.partnerShip.pilot==="cole"'))
 p.locator('[data-time="38"]').click();p.set_viewport_size(dict(width=390,height=844));p.wait_for_timeout(450)
 lit=g.evaluate('()=>{const a=ctx.getImageData(0,0,cv.width,cv.height).data;let n=0;for(let i=0;i<a.length;i+=4)if(Math.max(a[i],a[i+1],a[i+2])>35)n++;return n;}')
 ck('Paused resize repaints real cinematic pixels',lit>1000);ck('Final narrow preview has no horizontal overflow',p.evaluate('document.documentElement.scrollWidth<=innerWidth'));p.screenshot(path=str(O/'review-final-narrow.png'))
 p.locator('summary').click();p.locator('video').evaluate("v=>{v.preload='metadata';v.load();}");p.wait_for_function('Number.isFinite(document.querySelector("video").duration)');ck('Final review movie exposes a finite seekable duration',p.evaluate('document.querySelector("video").duration>=65'))
 ck('Final UI smoke has no page errors',not errors);b.close()
report=dict(passed=sum(q['passed'] for q in checks),checks=len(checks),errors=errors,results=checks);(O/'ui-smoke.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report));raise SystemExit(not all(q['passed'] for q in checks))
