from pathlib import Path
import json,sys
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT/'_BUILD_SOURCE'));import shoot;from serve_bof_1013 import AssetServer;shoot.http.server.ThreadingHTTPServer=AssetServer
OUT=ROOT/'_shots/bastion18_runtime';OUT.mkdir(parents=True,exist_ok=True);checks=[];errors=[]
def check(n,v):checks.append({'name':n,'passed':bool(v)});print(('PASS 'if v else'FAIL ')+n,flush=True)
port,stop=shoot.serve(str(ROOT))
try:
 with sync_playwright()as pw:
  b=pw.chromium.launch();p=b.new_page(viewport={'width':1280,'height':960});p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text)if m.type=='error'else None)
  p.goto(f'http://127.0.0.1:{port}/expansion/topdown/index.html?fullscreen=0',wait_until='domcontentloaded',timeout=90000);p.wait_for_function('window.TDGAME&&TD.game.state==="boot"',timeout=90000);ev=p.evaluate;ev('TDGAME.freeze();TD.pilot="yuri";TD.difficulty="normal"')
  def frames(n):
   while n:
    k=min(45,n);ev(f'TDGAME.step({k})');p.wait_for_timeout(1);n-=k
  ev('TD.game.sel=TD.MISSIONS.findIndex(m=>m.id===7);TDGAME.start();TD.game.bastion.totalWave=6;TD.game.units=[];TD.Bastion.wave(TD.game);TD.game.player.hp=1;TD.game.player.inv=0;TD.Bastion.harm(TD.game,2)');frames(230)
  check('death in room seven revives into room seven rather than jumping to the boss',ev('TD.game.bastion.totalWave===7&&TD.game.bastion.phase==="fight"&&!TD.game.boss&&TD.game.lives===1'))
  ev('TD.Bastion.startBoss(TD.game);Object.assign(TD.game.boss,{form:"helios",name:"HELIOS / PRISM ENTITY",state:"fight",hp:360,max:360,y:320,pattern:0});TD.game.bastion.turrets=[];TD.game.player.hp=1;TD.game.player.inv=0;TD.Bastion.harm(TD.game,2)');frames(124)
  check('Helios death checkpoint restores Helios without resurrecting the computer or corner turrets',ev('TD.game.boss.form==="helios"&&TD.game.boss.hp===360&&!TD.game.bastion.turrets.length&&!TD.game.bastion.coreRays.length'))
  ev('TD.game.sel=TD.MISSIONS.findIndex(m=>m.id===3);TDGAME.start();TD.game.fortress.pending=[];TD.game.units=[];TD.game.structures=[];TD.World.load(800,2400,[]);TD.game.player.y=428;TD.game.boss=TD.makeGosfer(TD.game,400,195)');frames(185)
  ev('window.g=TD.game.boss;Object.assign(g,{firing:0,fireAge:0,evade:0,burst:1,burstT:0,cd:999,dodgeCd:999});TD.game.eshots=[];g.tick(1/60);const pose=TD.gosferPose(g),m=TD_ASSAULT_ART.assets[pose.key],s=TD.game.eshots.at(-1);window.socketMatch=Math.abs(s.x-(g.x+(m.muzzle[0]-m.anchor[0])*(pose.flip?-1:1)))<.1&&Math.abs((s.y-s.drawLift)-(g.y+m.muzzle[1]-m.anchor[1]))<.1;TDGAME.render()')
  check('Gosfer laser starts exactly at the actual firing-frame muzzle',ev('socketMatch'));p.locator('#screen').screenshot(path=str(OUT/'gosfer_firing_socket.png'))
  p.mouse.move(600,500);p.mouse.down();ev('TD.game.player.inv=999;g.cd=999;g.dodgeCd=999;TD.Input.pointer.buttons[0]=true;window.oldHP=g.hp')
  for i in range(360):
   if ev('TD.game.boss.dead'):break
   ev('TD.Input.pointer.active=true;TD.Input.pointer.x=(g.x-TD.Cam.x)*TD.Cam.zoom;TD.Input.pointer.y=(g.y-65-TD.Cam.y)*TD.Cam.zoom;TD.Input.pointer.buttons[0]=true');frames(8)
  print(ev('({hp:g.hp,shots:TD.game.shots.length,time:TD.game.time})'));check('actual native rifle projectiles hit and defeat the animated Gosfer',ev('g.dead&&g.hp<=0'))
  check('recovery and firing fixtures have no browser errors',not errors)
  result={'checks':checks,'passed':sum(c['passed']for c in checks),'failed':sum(not c['passed']for c in checks),'errors':errors,'scope':'Protected native recovery/muzzle/damage fixtures; not a Normal balance route.'};(OUT/'recovery.json').write_text(json.dumps(result,indent=2));print(json.dumps({'passed':result['passed'],'failed':result['failed'],'errors':errors}));b.close()
finally:stop()
sys.exit(0 if all(c['passed']for c in checks)and not errors else 1)
