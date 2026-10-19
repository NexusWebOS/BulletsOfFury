"""Real review iframe: native launch, button-driven gunfire and isolated saves."""
from pathlib import Path
import json,sys
from playwright.sync_api import sync_playwright
import shoot
R=Path(__file__).resolve().parents[1];O=R/'_shots/highway_missiles_1017';checks=[];errors=[]
def check(name,ok,data=None):
 checks.append(dict(name=name,passed=bool(ok),data=data));print(('PASS ' if ok else 'FAIL ')+name,flush=True)
port,stop=shoot.serve(str(R))
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(channel='msedge',args=['--mute-audio']);p=br.new_page(viewport=dict(width=1920,height=1080));p.set_default_timeout(180000)
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:500]) if m.type=='error' or 'draw error' in m.text else None)
  p.on('response',lambda r:errors.append(str(r.status)+' '+r.url) if r.status>=400 else None)
  p.goto(f'http://127.0.0.1:{port}/docs/previews/highway_missiles_1017/index.html')
  p.wait_for_function('ready&&!busy&&game.contentWindow.eval("HM17.serial===2")')
  g=p.frames[1];g.evaluate(shoot.TRAP_RAF)
  check('Review boots two actual native shoulder missiles with the regular HUD',g.evaluate('enemies.filter(e=>e._hm17).length===2&&state===GS.PLAY&&SC12.enabled!==false'))
  p.screenshot(path=str(O/'review-ready.png'))
  p.get_by_role('button',name='Fire at rocket',exact=True).click()
  for i in range(20):
   error=g.evaluate(shoot.STEP,8)
   if error:errors.append(error)
   p.wait_for_timeout(5)
  check('Review fire button uses native gunfire to intercept the real rocket',g.evaluate('HM17.events.some(q=>q.event==="intercepted")&&!HM17.events.some(q=>q.event==="escaped-return-locked")'))
  p.get_by_role('button',name='Replay launch',exact=True).click();p.wait_for_function('''!busy&&game.contentWindow.eval("HM17.serial===2&&HM17.events.every(q=>q.event!=='intercepted')")''')
  for i in range(50):
   error=g.evaluate(shoot.STEP,8)
   if error:errors.append(error)
   p.wait_for_timeout(5)
  check('Replay runs the actual launch and atomic-return owners',g.evaluate('HM17.events.some(q=>q.event==="launch"||q.event==="escaped-return-locked")'))
  isolated=g.evaluate('''()=>{localStorage.setItem('probe','review-only');return window.__highwayMissileReviewStorage&&localStorage.getItem('probe')==='review-only';}''')
  protected=p.evaluate("localStorage.getItem('probe')===null&&localStorage.getItem('BOF_HIGHWAY_MISSILE_REVIEW_1017_probe')==='review-only'")
  check('Review storage is namespaced before the game boots',isolated and protected)
  p.get_by_role('button',name='Play highway',exact=True).click();p.wait_for_function('!busy&&game.contentWindow.eval("stagePlan.length>0&&HM17.next===180")')
  check('Play-highway mode retains the authored Stage4 plan and the installed director',g.evaluate('run.stage===4&&stagePlan.length>0&&!subBossTriggered&&HM17.next===180'))
  br.close()
finally:stop()
check('Review has no page, console, drawing or missing-asset errors',not errors,errors)
report={'passed':sum(c['passed'] for c in checks),'failed':[c for c in checks if not c['passed']],'errors':errors,'checks':checks}
O.mkdir(parents=True,exist_ok=True);(O/'review-verification.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report),flush=True)
if report['failed'] or errors:sys.exit(1)
