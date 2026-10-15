"""Render the five review-only side HUDs in Chromium and verify their controls."""
from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image
import shoot,json,base64
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'_shots/side_hud_1012';WEB=ROOT/'docs/previews/side_hud_1012'
checks=[];errors=[]
def check(name,ok,detail=None):
 checks.append(dict(name=name,passed=bool(ok),detail=detail));print(('PASS ' if ok else 'FAIL ')+name,flush=True)
port,stop=shoot.serve(str(ROOT))
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(args=['--mute-audio']);p=br.new_page(viewport=dict(width=1920,height=1080),reduced_motion='reduce');p.set_default_timeout(90000)
  p.on('pageerror',lambda e:errors.append(str(e)))
  p.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
  p.on('response',lambda r:errors.append(str(r.status)+' '+r.url) if r.status>=400 else None)
  p.goto(f'http://127.0.0.1:{port}/docs/previews/side_hud_1012/index.html');p.wait_for_function('SIDE_HUD_REVIEW.state.ready')
  check('All five concepts load with native references and reduced-motion default',p.locator('#concepts button').count()==5 and not p.evaluate('SIDE_HUD_REVIEW.state.motion'))
  for q in p.evaluate('SIDE_HUD_REVIEW.snapshots()'):
   (WEB/(q['id']+'-mockup.png')).write_bytes(base64.b64decode(q['url'].split(',')[1]))
  for i in range(5):
   p.locator('#concepts button').nth(i).click()
   check('Concept '+str(i+1)+' selector updates its title and highlighted choice',p.evaluate('SIDE_HUD_REVIEW.state.selected')==i and p.locator('#concepts [aria-pressed=true]').count()==1)
   p.locator('#stocks').select_option('low');p.screenshot(path=str(OUT/f'concept-{i+1}-low.png'))
  p.locator('#stocks').select_option('normal');p.locator('#concepts button').nth(0).click()
  boxes=[]
  for name in ['gameplay','fly-in','continue']:
   p.locator(f'[data-scene="{name}"]').click();boxes.append(p.locator('#preview').bounding_box());p.screenshot(path=str(OUT/(name+'-review.png')))
   check(name+' displays a valid native reference inside the same full-height field',p.evaluate('SIDE_HUD_REVIEW.state.scene')==name and Image.open(WEB/(name+'.png')).size==(960,1024))
  check('Switching scene never resizes the visible preview or logical playfield',all(b==boxes[0] for b in boxes) and p.evaluate('SIDE_HUD_REVIEW.field()')==[484,0,1080,1152],boxes)
  p.locator('[data-scene="gameplay"]').click();p.locator('#stocks').select_option('empty');p.screenshot(path=str(OUT/'empty-stocks.png'))
  check('Empty stock state remains selectable and visible',p.evaluate('SIDE_HUD_REVIEW.state.stocks')=='empty')
  p.locator('#stocks').select_option('normal');p.locator('#motion').check();p.wait_for_timeout(100)
  check('Radar sweep can animate independently of scene geometry',p.evaluate('SIDE_HUD_REVIEW.state.time')>0);p.locator('#motion').uncheck()
  p.locator('#full').click();p.wait_for_function('document.fullscreenElement!==null');p.wait_for_timeout(120);p.screenshot(path=str(OUT/'fullscreen.png'))
  rect=p.locator('#preview').bounding_box();check('Fullscreen uses the complete 16:9 display without top or bottom HUD bands',abs(rect['height']-1080)<2 and abs(rect['width']-1920)<2,rect)
  p.evaluate('document.exitFullscreen()');p.wait_for_timeout(100)
  with p.expect_download() as download:p.locator('#download').click()
  check('Save mockup downloads the selected PNG',download.value.suggested_filename=='command-bastion-gameplay.png')
  p.screenshot(path=str(OUT/'review-desktop.png'),full_page=True)
  p.set_viewport_size(dict(width=390,height=844));p.screenshot(path=str(OUT/'review-mobile.png'),full_page=True)
  check('Mobile review fits without horizontal overflow',p.evaluate('document.documentElement.scrollWidth<=innerWidth'))
  check('No browser or missing-asset errors',not errors,errors);br.close()
finally:stop()
report=dict(passed=sum(q['passed'] for q in checks),failed=sum(not q['passed'] for q in checks),errors=errors,checks=checks)
(ROOT/'docs/qa/side_hud_1012.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
(OUT/'verification.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(passed=report['passed'],failed=report['failed'],errors=errors)),flush=True)
raise SystemExit(bool(report['failed']))
