from pathlib import Path
from playwright.sync_api import sync_playwright
import json,sys
R=Path(__file__).resolve().parents[3] if Path(__file__).parent.name=='_research' else Path('C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');O=R/'_shots/yuri36';O.mkdir(exist_ok=True);errors=[];checks=[]
def check(n,v):checks.append({'name':n,'passed':bool(v)});print(('PASS 'if v else'FAIL ')+n,flush=True)
with sync_playwright() as pw:
 b=pw.chromium.launch();p=b.new_page(viewport={'width':1280,'height':960});p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text)if m.type=='error'else None)
 p.goto('http://127.0.0.1:8781/expansion/topdown/index.html?fullscreen=0',wait_until='domcontentloaded');p.wait_for_function('window.TDGAME&&TD.game.state==="boot"',timeout=120000);ev=p.evaluate;ev('TDGAME.freeze();TD.Input.pointer.active=false;TD.pilot="yuri";TD.game.sel=TD.MISSIONS.findIndex(m=>m.id===3);TDGAME.start();TD.game.fortress.pending=[];TD.game.units=[];TD.game.msgs=[];TD.Achievements.queue=[];ART.warm(Object.keys(TD_YURI32_ART.assets).concat(Object.keys(TD_LEVEL36_ART.assets)))');p.wait_for_function('Object.keys(TD_YURI32_ART.assets).concat(Object.keys(TD_LEVEL36_ART.assets)).every(k=>ART.get(k))',timeout=120000)
 def frames(n):
  for i in range(n):ev('TDGAME.step(1)');p.wait_for_timeout(1)
 def snap(n):ev('TD.game.msgs=[];TDGAME.render()');p.locator('#screen').screenshot(path=str(O/(n+'.png')))
 check('normal index loaded Level36 and Yuri36 exactly once',ev('!!TD.Level36&&!!TD.Yuri36&&document.querySelectorAll("script[src*=yuri36]").length===1'))
 ev('window.column36=TD.game.structures.find(s=>s.kind==="od_column36"&&s.x===170&&s.y===2310);Object.assign(TD.game.player,{x:210,y:2310,aim:-Math.PI/2,manualAim:999});TD.Cam.y=2100;TD.Cam.x=0;');p.keyboard.down('c');frames(120);snap('real_column_hold')
 check('C takes back cover on the real 170,2310 beam column',ev('TD.game.player.cover===column36&&TD.footPose(TD.game.player).key==="y32_cover_peek_east_0"'))
 p.keyboard.down('z');frames(35);snap('real_column_fire');check('real column exposes and fires the authored extended gun',ev('TD.game.player.peekExposed&&TD.footPose(TD.game.player).key==="y32_cover_peek_east_18"&&TD.game.shots.length>0'));p.keyboard.up('z');frames(35);p.keyboard.up('c');frames(1)
 ev('window.wall36=TD.game.structures.find(s=>s.kind==="od_barrier"&&s.x===415&&s.y===1515);Object.assign(TD.game.player,{x:415,y:1542,aim:Math.PI,manualAim:999});TD.Cam.y=1300;TD.Cam.x=0;');p.keyboard.down('c');frames(20);snap('real_wall_hold');check('C takes low cover at the real 415,1515 wall',ev('TD.game.player.cover===wall36&&TD.footPose(TD.game.player).key==="pb19_yuri_north_peek_0"'))
 p.keyboard.down('z');frames(28);snap('real_wall_fire');check('real wall pop-out keeps its full-height endpoint during firing',ev('TD.game.player.peekExposed&&TD.footPose(TD.game.player).key==="pb19_yuri_north_peek_7"'));p.keyboard.up('z');frames(25);p.keyboard.up('c');frames(1)
 check('one-hit and prone/roll controls retained',ev('TD.game.player.max===1&&TD.Input.keyLabel("prone")==="F"'))
 check('integrated native scene has no page or console errors',not errors);b.close()
(O/'scene_report.json').write_text(json.dumps({'checks':checks,'errors':errors},indent=2));print(json.dumps({'passed':sum(c['passed']for c in checks),'total':len(checks),'errors':errors}),flush=True);sys.exit(0 if all(c['passed']for c in checks)and not errors else 1)
