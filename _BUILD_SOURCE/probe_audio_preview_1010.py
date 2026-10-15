"""Native QA of the complete authored-frame review page."""
from pathlib import Path
import sys,json
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'_BUILD_SOURCE'));import shoot
OUT=ROOT/'_shots/audio_1010';checks=[];errors=[]
def check(name,value,data=None):checks.append(dict(name=name,passed=bool(value),data=data));print(('PASS ' if value else 'FAIL ')+name,flush=True)
port,stop=shoot.serve(str(ROOT))
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch();p=br.new_page(viewport=dict(width=1280,height=1000));p.set_default_timeout(30000)
  p.on('pageerror',lambda e:errors.append(str(e)))
  p.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
  p.on('response',lambda r:errors.append(str(r.status)+': '+r.url) if r.status>=400 else None)
  p.goto(f'http://127.0.0.1:{port}/docs/previews/audio_1010/index.html');p.wait_for_function('loaded===194&&total===194')
  q=p.evaluate('({cards:reels.length,total,ready:loaded,icons:document.querySelectorAll(".icon").length,plates:document.querySelectorAll(".plates figure").length})')
  check('All 194 displayed authored cells load across nine animation cards, projectile badges, Wind reward and story plates',q==dict(cards=9,total=194,ready=194,icons=10,plates=8),q)
  p.screenshot(path=str(OUT/'preview-desktop.png'))
  p.get_by_role('button',name='Pause animations').click();q=p.evaluate('reels.map(r=>r.time)');p.wait_for_timeout(220)
  check('Pause stops every animation clock',q==p.evaluate('reels.map(r=>r.time)'))
  p.locator('.card select').first.select_option('2');p.locator('.scrub').first.focus();p.keyboard.press('End');p.locator('#anchors').check();p.wait_for_timeout(50)
  q=p.evaluate('({clip:reels[0].clip,frame:Math.floor(reels[0].time*reels[0].clips[2][3]),anchors:showAnchors})')
  check('Clip selector, exact frame scrub and anchor overlay work',q==dict(clip=2,frame=3,anchors=True),q)
  p.locator('#reels').scroll_into_view_if_needed();p.screenshot(path=str(OUT/'preview-reels.png'))
  p.get_by_role('button',name='Play animations').click();p.locator('#speed').select_option('2');p.wait_for_timeout(200)
  check('Playback and speed selection resume the clocks',p.evaluate('playing&&speed===2&&reels[0].time>3/16'))
  p.locator('#windLevel').select_option('5');p.wait_for_function('loaded===total')
  check('Wind level selector displays all nine level-V projectile badges and keeps the separate reward',p.evaluate('Array.from(document.querySelectorAll("#icons img")).every(im=>/_5\\.png/.test(im.src))&&document.querySelectorAll("#icons img").length===9&&document.querySelectorAll("#windSymbol img").length===1'))
  p.locator('#proofs').scroll_into_view_if_needed();p.wait_for_function('Array.from(document.querySelectorAll("#proofs img")).every(i=>i.complete&&i.naturalWidth>0)')
  check('All eight native gameplay captures resolve',p.locator('#proofs img').count()==8)
  p.set_viewport_size(dict(width=480,height=900));p.evaluate('window.scrollTo(0,0)');p.screenshot(path=str(OUT/'preview-narrow.png'))
  check('Narrow review page fits without horizontal overflow',p.evaluate('document.documentElement.scrollWidth<=window.innerWidth+1'))
  check('No page, console or asset errors',not errors,errors);br.close()
finally:stop()
report=dict(passed=sum(q['passed'] for q in checks),failed=sum(not q['passed'] for q in checks),checks=checks,errors=errors)
(OUT/'preview-report.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print(json.dumps(dict(passed=report['passed'],failed=report['failed'],errors=errors)),flush=True)
sys.exit(1 if report['failed'] else 0)
