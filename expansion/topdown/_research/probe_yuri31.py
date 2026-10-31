"""Native Chromium/rendered-art and real raw-M30 input checks for Escape29."""
from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image
import json,sys,hashlib
R=Path(__file__).resolve().parents[3];sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
from serve_bof_1013 import AssetServer
shoot.http.server.ThreadingHTTPServer=AssetServer
O=R/'_shots/yuri31';O.mkdir(parents=True,exist_ok=True);checks=[];errors=[];measured={};cancelledMedia=[]
def check(name,v):checks.append({'name':name,'passed':bool(v)});print(('PASS 'if v else'FAIL ')+name,flush=True)
port,stop=shoot.serve(str(R))
try:
 with sync_playwright()as pw:
  browser=pw.chromium.launch();page=browser.new_page(viewport={'width':1280,'height':960});page.on('pageerror',lambda e:errors.append(str(e)));page.on('console',lambda m:errors.append(m.text)if m.type=='error'else None);page.on('response',lambda r:errors.append(f'HTTP {r.status} {r.url}')if r.status>=400 else None)
  page.on('requestfailed',lambda r:(cancelledMedia if r.failure=='net::ERR_ABORTED' and '/audio/'in r.url else errors).append(f'FAILED {r.url} {r.failure}'))
  page.add_init_script("""window.testPad={id:'6B controller (Vendor: 0ca3 Product: 0024)',mapping:'',index:0,connected:true,axes:[0,0],buttons:Array.from({length:12},()=>({pressed:false,value:0}))};Object.defineProperty(navigator,'getGamepads',{value:()=>[testPad]});window.pad=(...ids)=>testPad.buttons.forEach((b,i)=>{b.pressed=ids.includes(i);b.value=+b.pressed;});""")
  page.goto(f'http://127.0.0.1:{port}/expansion/topdown/index.html?fullscreen=0&build=overdrive1015-yuri31-r1',wait_until='domcontentloaded',timeout=90000);page.wait_for_function('window.TDGAME&&TD.game.state==="boot"',timeout=120000);ev=page.evaluate
  ev('TDGAME.freeze();TD.Input.setPadPreset("m30");ART.warm(Object.keys(TD_ESCAPE29_ART.assets));');page.wait_for_function('Object.keys(TD_ESCAPE29_ART.assets).every(k=>!!ART.get(k))',timeout=90000)
  def frames(n):
   while n:k=min(30,n);ev(f'TDGAME.step({k})');page.wait_for_timeout(1);n-=k
  def shot(name):ev('TD.Achievements.queue=[];TDGAME.render()');page.locator('#screen').screenshot(path=str(O/(name+'.png')))
  def fresh(id=3):
   ev(f'pad();testPad.axes=[0,0];TD.Input.pointer.active=false;TD.Input.update();TD.pilot="yuri";TD.difficulty="normal";TD.game.sel=TD.MISSIONS.findIndex(m=>m.id==={id});TDGAME.start();TD.Achievements.queue=[];TD.game.msgs=[];');frames(1)
  def escape(phase):
   fresh();ev('TD.Escape29.begin(TD.game);')
   if phase=='escape':ev('TD.Escape29.setPhase(TD.game,"corridor");')
   ev(f'TD.Escape29.setPhase(TD.game,"{phase}");');frames(1)


  check('145 authored frames decoded',ev('Object.keys(TD_YURI31_ART.assets).length===145&&Object.keys(TD_YURI31_ART.assets).every(k=>ART.get(k))'))
  check('new poses retain even uniform cells and root',ev('Object.values(TD_YURI31_ART.assets).every(m=>m.size.join()==="192,224"&&m.anchor.join()==="96,160"&&m.drawScale===1)'))
  escape('corridor');ev('TD.game.escape29.pending=[];TD.game.escape29.enemies=[];testPad.axes=[1,0];pad(3);');frames(1);ev('pad();');seen=[]
  for n in range(30):
   seen.append(ev('TD.Escape29.pose(TD.game)'))
   if n in [7,12,20,28]:shot('roll_'+str(n))
   frames(1)
  measured['rollFrames']=seen
  check('roll reaches inverted and recovery drawings',any(k.endswith('_7')for k in seen)and'y31_roll_east_23'in seen)
  check('roll plays all24 frames over movement duration',len(set(k for k in seen if k.startswith('y31_roll_')))==24)
  measured['rollLanding']=ev('({roll:TD.game.player.roll,prone:TD.game.player.prone,cooldown:TD.game.player.rollCd})')
  check('roll completes standing with five second cooldown',ev('TD.game.player.roll===0&&!TD.game.player.prone&&TD.game.player.rollCd>4.4&&TD.game.player.rollCd<4.6'))
  escape('corridor');ev('TD.game.escape29.pending=[];testPad.axes=[1,0];pad(3);');frames(3);ev('pad(1);');frames(2);check('jump does not cut the roll short',ev('TD.game.player.roll>0&&!TD.game.player.jump&&!TD.game.player.vault29'))
  ev('pad();');frames(1);ev('pad(8,3);');frames(1);ev('pad();');check('mode+roll queues prone landing',ev('TD.game.player.rollProne'));frames(25);check('complete roll lands prone',ev('TD.game.player.prone&&TD.game.player.roll===0'));check('prone landing stays down while moving',ev('Number(TD.Escape29.pose(TD.game).split("_").at(-1))>=11'));shot('roll_prone_landing')
  fresh();ev('TD.game.units=[];TD.game.fortress.pending=[];testPad.axes=[1,0];pad(5);');frames(9);check('horizontal topdown roll uses full authored rotation',ev('TD.footPose(TD.game.player).key.startsWith("y31_roll_east")'));shot('topdown_complete_roll')
  escape('chute');ev('TD.game.escape29.drones=[];TD.game.escape29.nextDrone=999;TD.Input.pointer.active=true;TD.Input.pointer.x=520;TD.Input.pointer.y=150;');frames(1);shot('slide_front');ev('TD.Input.pointer.x=80;');seen=[]
  for n in range(23):
   frames(1);seen.append(ev('TD.Escape29.pose(TD.game)'))
   if n in [4,9,19]:shot('slide_turn_'+str(n))
  measured['slideTurn']=seen
  check('slide turn visits authored intermediate angles',len(set(seen))>=13 and ev('TD.game.escape29.slideTurn31===1'))
  v=ev('TD.game.escape29.slideTurn31');ev('TDGAME.render();TDGAME.render();TDGAME.render()');check('drawing does not advance animation',ev(f'TD.game.escape29.slideTurn31==={v}'))
  ev('pad(2);');frames(1);check('projectiles originate at current turned barrel',ev('(()=>{const s=TD.game.escape29.shots.at(-1),q=TD.Escape29.socket(TD.game);return s&&Math.hypot(s.px-q.x,s.py-q.y)<.01;})()'))
  ev('pad();TD.Input.pointer.x=520;');frames(5);check('aim reversal unwinds instead of snapping',ev('TD.game.escape29.slideTurn31>0&&TD.game.escape29.slideTurn31<1'));shot('slide_unwind');frames(18);check('turn returns to forward slide',ev('TD.game.escape29.slideTurn31===0&&TD.Escape29.pose(TD.game)==="y31_slide_turn_east_0"'))
  escape('hatch');ev('pad(4);');frames(1);check('Retina stands Yuri over hatch facing forward/down',ev('TD.game.player.x===374&&TD.game.player.stance==="stand"&&TD.Escape29.pose(TD.game)==="y31_down_idle"&&TD.game.player.aim===0'))
  check('floor muzzle lies directly below center',ev('(()=>{const p=TD.game.player,q=TD.Escape29.socket(TD.game);return Math.abs(q.x-p.x)<2&&q.y>p.y-20&&q.y<p.y;})()'))
  shot('floor_aim');hp=ev('TD.game.escape29.hatchHp');ev('pad(4,2);');frames(1);check('M30A fires into hatch from front-facing stance',ev(f'TD.game.escape29.hatchHp<{hp}&&TD.Escape29.pose(TD.game).startsWith("y31_down_fire")'));shot('floor_fire');frames(140);check('floor shooting still breaches hatch',ev('["hinge","chute"].includes(TD.game.escape29.phase)'))
  check('820 retained art files unchanged',all(hashlib.sha256((R/k).read_bytes()).hexdigest()==v for k,v in json.loads((R/'_shots/lighting22/retained_art.json').read_text()).items()))
  page.goto(f'http://127.0.0.1:{port}/expansion/topdown/art/yuri31/preview.html',wait_until='domcontentloaded');page.wait_for_function('document.getElementById("status").textContent.startsWith("Playing")',timeout=60000)
  for bank,n in [('slide_turn',7),('roll',8),('roll_prone',24),('down_fire',4)]:
   page.select_option('#bank',bank);ev(f'paused=true;frame={n};document.getElementById("onion").checked=true;paint();');page.locator('#review').screenshot(path=str(O/('onion_'+bank+'.png')))
  ev('document.getElementById("onion").checked=false;paint()');page.locator('#review').screenshot(path=str(O/'standing_floor_fire.png'))
  check('review loads every selected frame',ev('Object.keys(images).length===145'))
  check('no browser errors',not errors)
  report={'build':'overdrive1015-yuri31-r1','checks':checks,'passed':sum(c['passed']for c in checks),'failed':sum(not c['passed']for c in checks),'errors':errors,'measured':measured,'scope':'Native Chromium with raw-M30 input simulation; real-time roll progression, reversible slide aim, and actual hatch impacts. No physical controller test.'};(O/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({'passed':report['passed'],'failed':report['failed'],'errors':errors}));browser.close()
finally:stop()
sys.exit(0 if not report['failed']and not errors else 1)
