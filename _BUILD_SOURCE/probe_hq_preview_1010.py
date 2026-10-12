"""Browser QA for the real-game HQ cinematic review page."""
from pathlib import Path
import sys,json
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'_BUILD_SOURCE'));import shoot
OUT=ROOT/'_shots/hq_live_1010';checks=[];errors=[]
def check(name,value,data=None):
 checks.append(dict(name=name,passed=bool(value),data=data));print(('PASS ' if value else 'FAIL ')+name,flush=True)
 if not value:print(json.dumps(data),flush=True)
port,stop=shoot.serve(str(ROOT))
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(args=['--autoplay-policy=no-user-gesture-required']);p=br.new_page(viewport=dict(width=1440,height=1040));p.set_default_timeout(120000)
  p.on('pageerror',lambda e:errors.append(str(e)))
  p.on('console',lambda m:errors.append(m.text[:800]) if m.type=='error' or 'draw error' in m.text else None)
  p.on('response',lambda r:errors.append('HTTP '+str(r.status)+': '+r.url) if r.status>=400 else None)
  p.goto(f'http://127.0.0.1:{port}/docs/previews/hq_live_1010/index.html')
  p.wait_for_function("ready&&document.getElementById('status').textContent.includes('Radar is live')")
  game=p.frames[1];game.evaluate(shoot.TRAP_RAF);game.wait_for_function('()=>hq10Warm()',polling=50)
  def frames(n):
   for i in range(0,n,30):
    e=game.evaluate(shoot.STEP,min(30,n-i))
    if e:errors.append(e);break
    p.wait_for_timeout(4)
  frames(225);p.screenshot(path=str(OUT/'preview-desktop.png'))
  check('Preview embeds the actual live interactive radar',game.evaluate('hq10MapActive()&&HQ10.draws.map>0'))
  p.get_by_role('button',name='Play sequence + sound').click();frames(20)
  q=game.evaluate('({beats:BOFCinematicDirector.current.beats.length,first:BOFCinematicDirector.current.beats[0].bg})')
  check('Play button runs the full four-shot cinematic',q['beats']==4 and q['first']=='hq10_background_00',q)
  p.get_by_role('button',name='Live radar',exact=True).click();frames(225)
  p.keyboard.press('ArrowRight');frames(1);p.keyboard.press('j');frames(1)
  q=game.evaluate('({selected:BOFCinematicDirector.current._hq10.selected,scan:BOFCinematicDirector.current._hq10.scan})')
  check('Preview transfers keyboard focus into the real radar controls',q['selected']!=0 and q['scan'] is not None,q)
  p.locator('#pilot').select_option('freezer');frames(30);game.wait_for_function("()=>XART.rdy('ship_freezer')",polling=50)
  p.get_by_role('button',name='Landing',exact=True).click();frames(110);p.screenshot(path=str(OUT/'preview-freezer-landing.png'))
  check('Pilot selector uses the actual selected ship in the landing',game.evaluate("run.pilot==='freezer'&&(HQ10.draws.ship_freezer||0)>0"))
  for name,index in [('Attack',1),('Scramble',3)]:
   p.get_by_role('button',name=name,exact=True).click();frames(140)
   check(name+' button opens its real authored cinematic shot',game.evaluate('hq10Shot().index')==index)
  p.set_viewport_size(dict(width=480,height=1000));p.get_by_role('button',name='Live radar',exact=True).click();frames(200);p.screenshot(path=str(OUT/'preview-narrow.png'))
  q=p.evaluate('({width:innerWidth,scroll:document.documentElement.scrollWidth})')
  check('Narrow review controls fit without horizontal overflow',q['scroll']<=q['width'],q)
  check('Narrow embedded cinematic preserves physical proportions',game.evaluate("(()=>{const r=cv.getBoundingClientRect();return Math.abs((r.width/cutsceneViewWidth())/(r.height/VH)-1)<.005;})()"))
  check('No page, console or asset errors',not errors,errors);br.close()
finally:stop()
report=dict(passed=sum(q['passed'] for q in checks),failed=sum(not q['passed'] for q in checks),checks=checks,errors=errors)
(OUT/'preview-report.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps(dict(passed=report['passed'],failed=report['failed'],errors=errors)),flush=True)
sys.exit(1 if report['failed'] else 0)
