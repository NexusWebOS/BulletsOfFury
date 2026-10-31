"""Runtime registration and visible final 16-bit art checks, after manifest integration."""
from pathlib import Path
import sys,json
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT/'_BUILD_SOURCE'));import shoot
OUT=ROOT/'_shots/bastion16_runtime_1013';OUT.mkdir(parents=True,exist_ok=True);checks=[];errors=[]
def check(name,value):checks.append({'name':name,'passed':bool(value)});print(('PASS ' if value else 'FAIL ')+name,flush=True)
port,stop=shoot.serve(str(ROOT))
try:
 with sync_playwright() as pw:
  browser=pw.chromium.launch();p=browser.new_page(viewport={'width':1280,'height':960});p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
  p.goto(f'http://127.0.0.1:{port}/expansion/topdown/index.html?fullscreen=0',timeout=90000);p.wait_for_function('window.TDGAME&&TD.game.state==="boot"',timeout=90000)
  p.wait_for_function('Object.keys(TD_ASSAULT_ART.assets).filter(k=>k.startsWith("pb16_")).length>200&&Object.keys(TD_ASSAULT_ART.assets).filter(k=>k.startsWith("pb16_")).every(k=>ART.get(k))',timeout=60000)
  ev=p.evaluate
  def frames(n=1):ev(f'TDGAME.step({n})')
  def snap(name):ev('TD.Achievements.queue=[];TD.game.msgs=[];TD.game.player.inv=0;TDGAME.render()');p.locator('#screen').screenshot(path=str(OUT/(name+'.png')))
  def fresh():ev('TDGAME.freeze();TD.pilot="yuri";TD.difficulty="normal";TD.game.sel=TD.MISSIONS.findIndex(m=>m.id===7);TDGAME.start();TD.Input.pointer.active=false;window.fixtureInput={};TD.game.bastion.phase="fixture";')
  ev('window.fixtureInput={};TD.Input.update=function(){this.last=this.state;this.state={...window.fixtureInput};this.raw={};};')
  fresh()
  check('stage and all four main character roles use registered 16-bit art',ev('ART.get("pb16_stage")&&["rifle","heavy","rocket","laser"].every(k=>TD_ASSAULT_ART.sequences["pb16_"+k+"_idle"].frames.every(f=>ART.get(f)))'))
  stand=[]
  for d in range(5):
   ev(f'TD.game.player.aimSector={d};TD.game.player.rise=1;TD.game.player.moving=false;TD.game.player.firing=0');stand.append(ev('TD.Bastion.playerPose(TD.game)'));snap(f'aim_{d}')
  check('five aim directions select five authored torso and gun orientations',stand==[f'pb16_yuri_aim_{i}' for i in range(5)])
  check('native draw uses the new 16-pixel animated gun reticle',ev('(()=>{const seen=[],old=ART.draw;ART.draw=function(...a){seen.push(a[1]);return old.apply(this,a)};TDGAME.render();ART.draw=old;return seen.some(k=>k.startsWith("pb16_reticle_"))&&TD_ASSAULT_ART.assets.pb16_reticle_0.size.every(n=>n<=32)})()'))
  ev('window.geometry=(()=>{const a=TD_ASSAULT_ART.assets,w=a.pb16_wall_0,lip=440+(w.bounds[1]-w.anchor[1])*(w.drawScale||1);const aim=[0,1,2,3,4].map(i=>{const m=a["pb16_yuri_aim_"+i];return 448+(m.muzzle[1]-m.anchor[1])*(m.drawScale||1)}),low=[0,1,2,3,4].map(i=>{const m=a["pb16_yuri_crouch_"+i];return 448+(m.bounds[1]-m.anchor[1])*(m.drawScale||1)});return{lip,aim,low}})()')
  check('standing muzzles clear cover lip while crouched heads remain protected',ev('geometry.aim.every(y=>y<geometry.lip+2)&&geometry.low.every(y=>y>geometry.lip)'))
  ev('window.fixtureInput={cover:true,left:true};TD.game.player.aimSector=0');frames(18)
  check('low lateral movement uses newly authored crouch-step frames',ev('TD.Bastion.playerPose(TD.game).startsWith("pb16_yuri_crouch_strafe")'));snap('crouch_step')
  ev('window.fixtureInput={cover:true,A:true};TD.game.player.aimSector=2;TD.game.bastion.cursor={x:320,y:160}');frames(20)
  check('covered rifle fire uses authored blindfire animation and actual muzzle',ev('TD.Bastion.playerPose(TD.game).startsWith("pb16_yuri_blindfire")&&TD.game.bastion.bullets.some(b=>b.blindfire)'));snap('blindfire')
  ev('window.fixtureInput={};TD.game.player.reviveT=.55');frames()
  check('checkpoint recovery uses rear-view revive bank',ev('TD.Bastion.playerPose(TD.game).startsWith("pb16_yuri_revive")'));snap('revive')
  fresh();ev('TD.game.bastion.totalWave=3;for(const [i,k] of ["rifle","heavy","rocket","laser"].entries()){const u=TD.Bastion.spawn(TD.game,k,100+i*145);u.y=360;u.phase="attack";u.atWall=0;u.canVault=false;u.scale={rifle:.52,heavy:.65,rocket:.54,laser:.53}[k];}');frames()
  check('all live enemies use modern idle/fire/walk frames with real body bounds',ev('TD.game.units.every(u=>TD.Bastion.unitPose(u).startsWith("pb16_")&&TD.Bastion.unitBody(u).ry>25)'));snap('enemy_line')
  for i in range(4):ev(f'TD.game.bastion.cover[2].hp={[52,28,10,0][i]}');snap(f'wall_stage_{i}')
  fresh();ev('TD.Bastion.startBoss(TD.game)');frames(110);snap('prism_heart')
  check('Prism Heart uses modern dimensions for hitbox',ev('(()=>{const q=TD.Bastion.bossBody(TD.game.boss);return q.rx>45&&q.rx<90&&q.ry>45&&q.ry<90})()'))
  ev('TD.Bastion.coreHit(TD.game,999)');frames(120);frames(185);ev('TD.game.boss.state="volley";TD.game.boss.t=.35;TD.game.boss.x=320;TD.game.player.inv=999');snap('helios')
  check('Helios visible body hitbox comes from modern authored bank',ev('(()=>{const q=TD.Bastion.bossBody(TD.game.boss);return q.ry>65&&q.ry<120})()'))
  check('zero browser errors',not errors)
  result={'checks':checks,'errors':errors,'geometry':ev('geometry'),'passed':sum(c['passed'] for c in checks),'total':len(checks)};(OUT/'verification.json').write_text(json.dumps(result,indent=2));print(json.dumps(result));browser.close()
finally:stop()
sys.exit(0 if all(c['passed'] for c in checks) and not errors else 1)
