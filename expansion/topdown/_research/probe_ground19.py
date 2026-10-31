from pathlib import Path
import sys,json,time
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[3];sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot;from serve_bof_1013 import AssetServer;shoot.http.server.ThreadingHTTPServer=AssetServer
O=R/'_shots/bastion19/runtime';O.mkdir(parents=True,exist_ok=True);checks=[];errors=[]
def check(n,v):checks.append({'name':n,'passed':bool(v)});print(('PASS 'if v else'FAIL ')+n,flush=True)
port,stop=shoot.serve(str(R))
try:
 with sync_playwright()as pw:
  b=pw.chromium.launch();p=b.new_page(viewport={'width':1280,'height':960});p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text)if m.type=='error'else None)
  p.goto(f'http://127.0.0.1:{port}/expansion/topdown/index.html?fullscreen=0',wait_until='domcontentloaded',timeout=90000);p.wait_for_function('window.TDGAME&&TD.game.state==="boot"',timeout=90000);ev=p.evaluate;ev('TDGAME.freeze();TD.pilot="yuri";TD.difficulty="normal"')
  def frames(n):
   while n:
    k=min(45,n);ev(f'TDGAME.step({k})');p.wait_for_timeout(2);n-=k
  def shot(n):
   old=ev('({inv:TD.game.player.inv,flash:TD.game.player.flash})');ev('TD.game.player.inv=0;TD.game.player.flash=0;TDGAME.render()');p.locator('#screen').screenshot(path=str(O/(n+'.png')));p.evaluate('q=>Object.assign(TD.game.player,q)',old)
  ev('TD.game.sel=TD.MISSIONS.findIndex(m=>m.id===7);TDGAME.start()');frames(100)
  check('Bastion19 art loads into current game',ev('!!TD_BASTION19_ART&&TD_ASSAULT_ART.assets.pb18_room.file.includes("bastion19")'))
  check('rear door has an integrated core and corner sockets',ev('TD.game.bastion.wallCore.x===320&&TD.game.bastion.turrets[0].x===254&&TD.game.bastion.turrets[1].x===386'))
  shot('room_standing');p.keyboard.down('l');frames(35);check('cover lowers Yuri behind foreground wall',ev('TD.game.player.rise<.1'));shot('room_cover');p.keyboard.down('j');frames(20);check('blindfire shoots from cover',ev('TD.game.player.blindfire&&TD.game.bastion.gunShots.rifle>0'));shot('room_blindfire');p.keyboard.up('j');p.keyboard.up('l');frames(30)
  ev('TD.Bastion.startBoss(TD.game)');frames(110);shot('reactor');check('new cylindrical reactor has rotating and cracked/shattered banks',ev('TD_BASTION19_ART.sequences.pb19_reactor.frames.length===16&&TD.game.boss.name.includes("REACTOR")'))
  ev('TD.Bastion.coreHit(TD.game,999)');frames(45);shot('reactor_shatter');frames(95);shot('white_transform');frames(175);shot('helios_reveal');check('containment destruction reveals authored Helios',ev('TD.game.boss.form==="helios"'))
  for state,sec in [('run',.32),('volley',.63),('lightning',1.1),('jump',.55)]:
   ev(f'Object.assign(TD.game.boss,{{state:"{state}",t:{sec},x:320,y:320,gait:.36,toX:735,jumpZ:{130 if state=="jump" else 0}}})');shot('helios_'+state)
  ev('TD.game.sel=TD.MISSIONS.findIndex(m=>m.id===3);TDGAME.start();TD.game.fortress.pending=[];TD.game.units=[];TD.game.player.inv=999;TD.game.structures=[];TD.World.load(800,2400,[]);TD.game.player.y=800;TD.game.player.x=400;TD.Cam.x=80;TD.Cam.y=560');frames(2)
  p.keyboard.press('f');frames(40);check('F toggles actual prone state',ev('TD.game.player.prone&&TD.game.player.stance==="prone"'));shot('foot_prone');y=ev('TD.game.player.y');p.keyboard.down('w');frames(40);p.keyboard.up('w');check('WASD crawls while remaining prone',ev(f'TD.game.player.prone&&TD.game.player.y<{y}-20'));shot('foot_crawl');p.keyboard.press('f');frames(30);check('F restores authored standing suit without a black silhouette',ev('!TD.game.player.prone&&TD.footPose(TD.game.player).key.startsWith("pb19_yuri")'));shot('foot_stand')
  ev('TD.game.player.aim=Math.PI;TD.game.player.manualAim=999;TD.game.player.motionFacing=4');p.keyboard.press('u');frames(7);check('grenade throw preserves north facing',ev('TD.footPose(TD.game.player).dir==="north"&&TD.footPose(TD.game.player).key.includes("north_grenade")'));shot('foot_grenade');frames(35)
  p.mouse.move(630,120);p.mouse.down();p.keyboard.down('d');frames(12);p.keyboard.up('d');check('moving muzzle effect is attached to the actor socket',ev('TD.FX.list.some(f=>f.k==="attached"&&f.actor===TD.game.player&&Math.hypot(f.socket(f.actor).x-TD.footVisualSocket(TD.game.player).x,f.socket(f.actor).y-TD.footVisualSocket(TD.game.player).y)<.01)'));shot('foot_fire');p.mouse.up();frames(10)
  ev('TD.game.player.y=428;TD.game.player.x=400;TD.game.boss=TD.makeGosfer(TD.game,400,195);TD.game.fortress.relays=3;TD.game.structures.push(TD.makeStructure({kind:"od_bosswall",x:400,y:365}));TD.Cam.x=80;TD.Cam.y=0');frames(190);shot('gosfer_patrol')
  ev('Object.assign(TD.game.boss,{state:"windup",attack:"breaker",attackT:.7,sent:0,volleyTarget:{x:400,y:428}});TDGAME.render()');shot('gosfer_charge');frames(45);check('Gosfer releases cover-breaker lasers after telegraph',ev('TD.game.eshots.some(s=>s.dmg===5)||TD.game.boss.sent>0'));shot('gosfer_fire')
  ev('const w=TD.game.structures.find(w=>w.kind==="od_bosswall");TD.hitStructure(TD.game,w,27,false);window.wall=w');check('Gosfer cover has real damage states',ev('wall.hp>0&&wall.hp<48&&!wall.dead'));shot('gosfer_damaged_cover');ev('TD.hitStructure(TD.game,wall,30,false)');check('Gosfer wall breaks and removes collision',ev('wall.dead&&wall.rect.dead&&!TD.World.solidAt(wall.x,wall.y)'));shot('gosfer_broken_cover')
  check('no browser/page/asset errors',not errors);result={'checks':checks,'passed':sum(c['passed']for c in checks),'failed':sum(not c['passed']for c in checks),'errors':errors};(O/'focused.json').write_text(json.dumps(result,indent=2));print(json.dumps(result));b.close()
finally:stop()
sys.exit(0 if all(c['passed']for c in checks)and not errors else 1)
