"""Native keyboard route and relay-fire verification; guards removed to isolate navigation."""
from pathlib import Path
import json,sys
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT/'_BUILD_SOURCE'))
import shoot
OUT=ROOT/'_shots/overdrive_assault_1013';OUT.mkdir(parents=True,exist_ok=True)
checks=[];errors=[]
def check(name,passed):
 checks.append({'name':name,'passed':bool(passed)});print(('PASS ' if passed else 'FAIL ')+name,flush=True)
port,stop=shoot.serve(str(ROOT))
try:
 with sync_playwright() as pw:
  browser=pw.chromium.launch();page=browser.new_page(viewport={'width':1280,'height':960})
  page.on('pageerror',lambda e:errors.append(str(e)))
  page.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
  page.on('response',lambda r:errors.append(f'HTTP {r.status} {r.url}') if r.status>=400 else None)
  page.goto(f'http://127.0.0.1:{port}/expansion/topdown/index.html?fullscreen=0')
  page.wait_for_function('window.TDGAME && TDGAME.G.state==="boot"',timeout=90000)
  page.evaluate('TDGAME.freeze();TD.pilot="yuri";TD.difficulty="normal";TDGAME.G.sel=1;TDGAME.start();TD.game.units=[]')
  def ev(s):return page.evaluate(s)
  def frames(n):
   while n:
    k=min(n,60);page.evaluate('n=>TDGAME.step(n)',k);page.wait_for_timeout(1);n-=k
  def walk(x,y):
   for _ in range(350):
    p=ev('({x:TD.game.player.x,y:TD.game.player.y})');dx=x-p['x'];dy=y-p['y']
    if abs(dx)<5 and abs(dy)<5:break
    for k,on in [('a',dx< -4),('d',dx>4),('w',dy< -4),('s',dy>4)]:
     (page.keyboard.down if on else page.keyboard.up)(k)
    frames(2)
   for k in ['a','d','w','s']:page.keyboard.up(k)
   p=ev('({x:TD.game.player.x,y:TD.game.player.y})')
   ok=abs(p['x']-x)<8 and abs(p['y']-y)<8
   check(f'walk reaches {x},{y} without teleporting',ok)
   if not ok:raise RuntimeError(f'Route blocked at {p}, target {(x,y)}')
  def destroy_relay(x,y):
   # Rifle collision lives at ground level, with a 45px visual muzzle lift.
   target=page.evaluate('([x,y])=>{const r=document.getElementById("screen").getBoundingClientRect();return{x:r.x+(x-TD.Cam.x)*r.width/TD.VW,y:r.y+(y-45-TD.Cam.y)*r.height/TD.VH}}',[x,y])
   page.mouse.move(target['x'],target['y']);page.mouse.down();frames(160);page.mouse.up()
   ok=page.evaluate('([x,y])=>TD.game.structures.some(s=>s.kind==="od_relay"&&s.x===x&&s.y===y&&s.dead)',[x,y])
   check(f'assault rifle destroys relay at {x},{y}',ok)
  for xy in [(330,2240),(175,2140),(175,1900)]:walk(*xy)
  destroy_relay(190,1770)
  for xy in [(175,1660),(220,1430),(220,1340)]:walk(*xy)
  destroy_relay(230,1240)
  for xy in [(395,1340),(450,1100),(585,950)]:walk(*xy)
  destroy_relay(565,800)
  check('all three destroyed relays unlock the data center',ev('TD.game.fortress.relays===3'))
  for xy in [(625,700),(620,570),(400,570)]:walk(*xy)
  page.keyboard.down('w');frames(12);page.keyboard.up('w');frames(100)
  check('normal traversal reaches the open doors and Gosfer introduction',ev('TD.game.boss?.name==="GOSFER"&&TD.game.fortress.doorOpen'))
  ev('TDGAME.render()');page.locator('#screen').screenshot(path=str(OUT/'fortress_route_complete.png'))
  passwords=ev('({fortress:TD.Password.encode(1,"yuri","normal","hotwire"),truck:TD.Password.encode(4,"yuri","normal","hotwire")})')
  print('PASSWORDS',passwords,flush=True)
  # Verify scene-owned state and both briefing layouts after changing stages.
  ev('TDGAME.G.sel=3;TDGAME.start()')
  check('museum setup clears fortress scene state',ev('TD.game.fortress===null&&TD.game.mission===5'))
  check('briefing controls match standard and six-button schemes',ev('TD.Input.setPadStyle("standard");const a=TD.footBriefKeys();TD.Input.setPadStyle("six");const b=TD.footBriefKeys();a.some(k=>k[1]==="JUMP")&&b.some(k=>k[1]==="FIRE NORTH")'))
  ev('TD.pilot="cole";TDGAME.G.sel=4;TDGAME.start();TDGAME.render()')
  page.locator('#screen').screenshot(path=str(OUT/'truck_cole_crew.png'))
  check('no page, console or missing-file errors',not errors)
  (OUT/'route_report.json').write_text(json.dumps({'checks':checks,'passwords':passwords,'fixture':'Guards removed for navigation; real keyboard movement and mouse-fired rifle, no teleports.','errors':errors},indent=2),encoding='utf-8')
  browser.close()
finally:stop()
print(f'SUMMARY {sum(c["passed"] for c in checks)}/{len(checks)} checks; {len(errors)} errors',flush=True)
sys.exit(0 if all(c['passed'] for c in checks) and not errors else 1)
