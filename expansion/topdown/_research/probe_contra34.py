"""Native Chromium/rendered-art and real raw-M30 input checks for Escape29."""
from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image
import json,sys,hashlib
R=Path(__file__).resolve().parents[3];sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
from serve_bof_1013 import AssetServer
shoot.http.server.ThreadingHTTPServer=AssetServer
O=R/'_shots/contra34';O.mkdir(parents=True,exist_ok=True);checks=[];errors=[];measured={};cancelledMedia=[]
def check(name,v):checks.append({'name':name,'passed':bool(v)});print(('PASS 'if v else'FAIL ')+name,flush=True)
port,stop=shoot.serve(str(R))
try:
 with sync_playwright()as pw:
  browser=pw.chromium.launch();page=browser.new_page(viewport={'width':1280,'height':960});page.on('pageerror',lambda e:errors.append(str(e)));page.on('console',lambda m:errors.append(m.text)if m.type=='error'else None);page.on('response',lambda r:errors.append(f'HTTP {r.status} {r.url}')if r.status>=400 else None)
  page.on('requestfailed',lambda r:(cancelledMedia if r.failure=='net::ERR_ABORTED' and '/audio/'in r.url else errors).append(f'FAILED {r.url} {r.failure}'))
  page.add_init_script("""window.testPad={id:'6B controller (Vendor: 0ca3 Product: 0024)',mapping:'',index:0,connected:true,axes:[0,0],buttons:Array.from({length:12},()=>({pressed:false,value:0}))};Object.defineProperty(navigator,'getGamepads',{value:()=>[testPad]});window.pad=(...ids)=>testPad.buttons.forEach((b,i)=>{b.pressed=ids.includes(i);b.value=+b.pressed;});""")
  page.goto(f'http://127.0.0.1:{port}/expansion/topdown/index.html?fullscreen=0&build=overdrive1016-contra34-r1',wait_until='domcontentloaded',timeout=90000);page.wait_for_function('window.TDGAME&&TD.game.state==="boot"',timeout=120000);ev=page.evaluate
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



  ev('ART.warm(Object.keys(TD_CONTRA34_ART.assets))');page.wait_for_function('Object.keys(TD_CONTRA34_ART.assets).every(k=>ART.get(k))',timeout=90000)
  check('new exported sheets decode',ev('Object.keys(TD_CONTRA34_ART.assets).length===2595'))
  escape('corridor');ev("TD.game.escape29.pending=[];TD.game.escape29.enemies=[{kind:'rifle',x:400,y:350,phase:'enter',walk:.3,age:1,homeX:360,hp:10,flash:0},{kind:'heavy',x:520,y:350,phase:'enter',walk:.4,age:1,homeX:450,hp:24,flash:0}];");shot('corridor')
  check('side sprite bank used',ev('TD.Contra34.stats.side>0&&TD.Contra34.sidePose(TD.game.escape29.enemies[0],TD.game).key.startsWith("c34_side_machine_gunner_walk")'))
  ev('TD.Input.pointer.active=true;TD.Input.pointer.x=430;TD.Input.pointer.y=240;pad(2);');frames(1)
  measured['aim']=ev('({cursor:TD.game.escape29.cursor,screen:TD.Contra34.toScreen(TD.game,TD.game.escape29.cursor.x,TD.game.escape29.cursor.y)})')
  check('zoom mouse aim inverse matches screen',abs(measured['aim']['screen']['x']-430)<.01 and abs(measured['aim']['screen']['y']-240)<.01)
  ev('pad();TD.Input.pointer.active=false;testPad.axes=[1,-1];pad(4);');frames(90)
  check('controller retina remains visible',ev('(()=>{const e=TD.game.escape29,q=TD.Contra34.toScreen(TD.game,e.cursor.x,e.cursor.y);return q.x>=9&&q.x<=631&&q.y>=89&&q.y<=466})()'))
  escape('chute');frames(160);shot('chute');check('chute uses flying alien animation',ev('TD.Contra34.stats.drone>0'))
  escape('corridor');ev('TD.game.escape29.pending=[];TD.game.player.x=191;pad(5);');frames(15);shot('cover');check('closer view keeps cover',ev('TD.game.player.hidden33'))
  fresh(7);frames(130);shot('bastion');check('Bastion uses imported enemy identity',ev('TD.game.units.every(u=>TD.Bastion.unitPose(u).startsWith("c34_"))'))
  ev('TD.Input.pointer.active=true;TD.Input.pointer.x=384;TD.Input.pointer.y=229;pad(4,2);');frames(1)
  measured['frontAim']=ev('TD.Contra34.toScreen(TD.game,TD.game.bastion.cursor.x,TD.game.bastion.cursor.y)');check('Bastion zoom mouse aim inverse matches screen',abs(measured['frontAim']['x']-384)<.01 and abs(measured['frontAim']['y']-229)<.01)
  ev('pad();TD.Input.pointer.active=false;TD.Bastion.startBoss(TD.game);TD.game.boss.form="helios";TD.game.boss.state="run";TD.game.boss.x=320;TD.game.boss.y=340;TD.game.boss.toX=560;TD.game.boss.t=.2;TD.game.boss.gait=.3;');shot('helios');check('new Helios walking bank selected',ev('TD.Bastion.heliosPose(TD.game.boss).key.startsWith("c34_motion_fire_prism_run")'))
  # Render hit flash on the exact same pose, then verify it expires through gameplay.
  from PIL import ImageChops
  escape('corridor');ev("TD.game.escape29.pending=[];TD.game.escape29.enemies=[{kind:'rifle',x:300,y:350,phase:'fight',walk:0,age:1,homeX:300,hp:10,max:10,flash:0,fireCd:5}];TD.game.escape29.message='';TD.game.escape29.cursor={x:490,y:150};")
  shot('side_unhit');ev('TD.game.escape29.enemies[0].flash=.10');shot('side_hit')
  check('actual side sprite pixels flash on hit',ImageChops.difference(Image.open(O/'side_unhit.png').convert('RGB'),Image.open(O/'side_hit.png').convert('RGB')).getbbox() is not None)
  frames(10);check('side hit flash expires',ev('TD.game.escape29.enemies[0].flash===0'))
  # A live burst emits from the selected, registered gun tip.
  ev('TD.game.escape29.enemies[0].fireCd=0;TD.game.player.inv=2;');frames(1)
  measured['socket']=ev('(()=>{const e=TD.game.escape29,u=e.enemies[0],s=e.enemyShots[0],q=TD.Contra34.sideSocket(u,TD.game);return {shot:s&&{x:s.px,y:s.py},socket:q}})()')
  check('enemy shot originates at the visible muzzle',measured['socket']['shot'] and abs(measured['socket']['shot']['x']-measured['socket']['socket']['x'])<.01 and abs(measured['socket']['shot']['y']-measured['socket']['socket']['y'])<.01)
  escape('hatch');shot('hatch');check('elevator hatch stays above dialogue box',ev('TD.Contra34.toScreen(TD.game,374,405).y<419'));ev('pad(4,2);');frames(140);check('hatch remains shootable at close zoom',ev('TD.game.escape29.phase!=="hatch"'))
  fresh(7);ev("TD.game.bastion.t=7;TD.game.msgs=[];const u=TD.Bastion.spawn(TD.game,'heavy',320,0);Object.assign(u,{phase:'peek',x:320,y:338,duck:0,scale:.65,phaseT:.5,firing:1,fireT:.12,flash:0});TD.game.units=[u];");shot('front_unhit');ev('TD.game.units[0].flash=.12');shot('front_hit')
  check('front sprite pixels flash through ThreeJS',ImageChops.difference(Image.open(O/'front_unhit.png').convert('RGB'),Image.open(O/'front_hit.png').convert('RGB')).getbbox() is not None)
  frames(12);check('front hit flash expires',ev('TD.game.units[0].flash===0'))
  check('all four front firing families use new sheets',ev('["rifle","heavy","rocket","laser"].every(kind=>TD.Contra34.frontPose({kind,phase:"peek",firing:1,fireT:.1}).startsWith("c34_front_"))'))
  fresh(3);frames(3);check('top down on foot view is 25 percent closer',ev('TD.Cam.zoom===1.25'));shot('topdown')
  fresh(7);ev('TD.Bastion.startBoss(TD.game);Object.assign(TD.game.boss,{form:"helios",name:"HELIOS / FIRE PRISM",state:"run",x:320,y:340,toX:560,fromX:320,runT:0,pattern:0,hitAge:99,gauge:1,t:.2,gait:.3,flash:0});TD.game.bastion.phase="helios";TD.game.msgs=[];');shot('boss_unhit');ev('TD.game.boss.flash=.12');shot('boss_hit')
  check('imported boss pixels flash on hit',ImageChops.difference(Image.open(O/'boss_unhit.png').convert('RGB'),Image.open(O/'boss_hit.png').convert('RGB')).getbbox() is not None)
  frames(12);check('boss flash expires',ev('TD.game.boss.flash===0'))
  measured['zoom']=ev('TD.Contra34.view(TD.game).z');check('boss keeps closer camera',measured['zoom']==1.15)
  ev('Object.assign(TD.game.boss,{state:"volley",t:.59,volley:0});TD.game.bastion.enemyShots=[];');frames(2)
  measured['bossEmitter']=ev('(()=>{const G=TD.game,b=G.boss,z=TD.Bastion.heliosPose(b),m=TD_ASSAULT_ART.assets[z.key],q=m.emitter,shots=G.bastion.enemyShots;return {n:shots.length,expected:{x:b.x+(q[0]-m.anchor[0])*m.drawScale,y:b.y+(q[1]-m.anchor[1])*m.drawScale},shot:shots[0]&&{x:shots[0].sx,y:shots[0].sy}}})()')
  e=measured['bossEmitter'];check('new boss volley uses scaled hand emitter',e['n']>=3 and abs(e['expected']['x']-e['shot']['x'])<.01 and abs(e['expected']['y']-e['shot']['y'])<.01)
  shot('boss_volley')
  check('browser has no errors',not errors)
  report={'checks':checks,'errors':errors,'measured':measured};(O/'report.json').write_text(json.dumps(report,indent=2));print(json.dumps(report));browser.close()
finally:stop()
sys.exit(0 if all(c['passed']for c in checks)and not errors else 1)
