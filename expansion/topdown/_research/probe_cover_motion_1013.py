"""Real Chromium coverage for cover controls, visible body hits and entrances."""
from pathlib import Path
import json,sys
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT/'_BUILD_SOURCE'));import shoot
OUT=ROOT/'_shots/cover_motion_1013';OUT.mkdir(parents=True,exist_ok=True)
checks=[];errors=[]
def check(name,value):
 checks.append({'name':name,'passed':bool(value)});print(('PASS ' if value else 'FAIL ')+name,flush=True)
port,stop=shoot.serve(str(ROOT))
try:
 with sync_playwright() as pw:
  browser=pw.chromium.launch();page=browser.new_page(viewport={'width':1280,'height':960})
  page.on('pageerror',lambda e:errors.append(str(e)));page.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
  page.on('response',lambda r:errors.append('HTTP '+str(r.status)+' '+r.url) if r.status>=400 else None)
  page.goto(f'http://127.0.0.1:{port}/expansion/topdown/index.html?fullscreen=0&build=cover-motion-qa')
  page.wait_for_function('window.TDGAME&&TDGAME.G.state==="boot"',timeout=90000);page.evaluate('TDGAME.freeze()')
  if not page.evaluate('!!window.TD_COVER_MOTION_ART'):page.add_script_tag(url=f'http://127.0.0.1:{port}/expansion/topdown/art/cover_motion_1013/manifest.js')
  page.wait_for_function('Object.keys(TD_COVER_MOTION_ART.assets).every(k=>ART.get(k))',timeout=60000)
  def ev(s):return page.evaluate(s)
  def frames(n=1):
   while n:
    k=min(n,60);page.evaluate('n=>TDGAME.step(n)',k);page.wait_for_timeout(1);n-=k
  def snap(name):
   ev('TD.game.msgs=[];TD.game.player.inv=0;TD.game.player.flash=0;TDGAME.render()');page.locator('#screen').screenshot(path=str(OUT/(name+'.png')));ev('TD.game.player.inv=9999')
  def fresh():
   for k in ['w','a','s','d','j','i','f','c','Tab']:page.keyboard.up(k)
   page.mouse.up();ev('TD.pilot="yuri";TD.difficulty="normal";TDGAME.G.sel=1;TDGAME.start();TD.Input.pointer.active=false;TD.game.player.inv=9999;TD.Achievements.queue=[]');frames(2)
  fresh()
  check('55 complete even-canvas art frames decode',ev('Object.keys(TD_COVER_MOTION_ART.assets).length===55&&Object.values(TD_COVER_MOTION_ART.assets).every(m=>m.size.every(n=>n%2===0)&&m.bounds[0]>0&&m.bounds[1]>0&&m.bounds[2]<m.size[0]&&m.bounds[3]<m.size[1])'))
  check('fortress arrivals originate above camera top',ev('TD.game.fortress.arrivals.length>0&&TD.game.fortress.arrivals.every(a=>a.y<a.cameraY-60)'))
  ev('TD.game.fortress.pending=[];TD.game.units=[];TD.game.player.x=400;TD.game.player.y=2166;TD.game.player.aim=Math.PI;TD.Cam.follow(400,2166,1)');page.keyboard.down('f');frames();page.keyboard.up('f');frames(2)
  check('F latches prone and anchors to indestructible wall',ev('TD.game.player.prone&&TD.game.player.stance==="prone"&&TD.game.player.cover.kind==="od_bunker"'))
  ev('const G=TD.game,s=G.player.cover;window.wallY=G.player.y;TD.hitStructure(G,s,1e12,true);TD.blastStructures(G,s.x,s.y,100,1e12)')
  check('concrete bunker survives ram and blast damage',ev('!TD.game.player.cover.dead&&TD.game.player.cover.hp===Infinity&&!TD.game.player.cover.rect.dead'))
  page.keyboard.down('j');frames(16)
  check('peek rises without teleporting through the wall',ev('TD.game.player.peekExposed&&Math.abs(TD.game.player.y-wallY)<.1&&TD.game.shots.length>0&&TD.footPose(TD.game.player).key.startsWith("od_cm_yuri_north_peek")'));snap('cover_peek_live')
  page.keyboard.down('i');frames(14)
  check('Retina plus fire keeps blindfire protected',ev('TD.game.player.blindfire&&!TD.game.player.peekExposed&&TD.game.player.hidden&&TD.game.player.firing>0&&TD.footPose(TD.game.player).action==="blindfire"'));snap('cover_blindfire_live')
  ev('const G=TD.game,p=G.player;p.inv=0;G.eshots=[{k:"mg",x:400,y:2105,vx:0,vy:8,a:0,dmg:1,life:40,r:4,t:0,drawLift:35}];window.armor=p.hp');frames(6)
  check('enemy fire cannot damage concealed blindfire body',ev('TD.game.player.hp===armor'))
  page.keyboard.up('j');page.keyboard.up('i');frames(12);snap('cover_prone_live')
  page.keyboard.down('f');frames();page.keyboard.up('f');frames(2)
  ev('const p=TD.game.player;p.x=480;p.y=2260;p.aim=Math.PI;p.manualAim=900;TD.Cam.follow(p.x,p.y,1)');page.keyboard.down('d');frames(22)
  check('aim north plus move east selects true sidestep bank',ev('TD.footPose(TD.game.player).action==="sidestep"&&TD.footPose(TD.game.player).key.startsWith("od_cm_yuri_north_sidestep")'));snap('yuri_sidestep_live');page.keyboard.up('d')
  ev('const p=TD.game.player;p.weapons=[{id:"assault_rifle",ammo:Infinity,lv:1},{id:"minigun",ammo:30,lv:1}];p.wi=1');page.keyboard.down('Tab');frames();page.keyboard.up('Tab');page.mouse.wheel(0,200);frames()
  check('Tab and wheel cannot swap equipped weapon',ev('TD.game.player.wi===1'))
  ev('const p=TD.game.player;TD.game.pickups=[{kind:"fusion_beam",x:p.x,y:p.y,t:0}];TD.footPickups(TD.game,1/60)')
  check('pickup replaces upgrade and keeps unlimited fallback',ev('TD.game.player.weapons.length===2&&TD.game.player.weapons[1].id==="fusion_beam"&&TD.game.player.weapons[0].id==="assault_rifle"'))
  check('swept shots hit visible torso and reject empty flank',ev('(()=>{const u={type:"odRobot",x:400,y:400};return TD.infantryShotHit(u,{x:400,y:378,vx:0,vy:-20,drawLift:0,r:3})&&!TD.infantryShotHit(u,{x:470,y:378,vx:0,vy:-20,drawLift:0,r:3})&&TD.infantryShotHit({type:"light",x:400,y:400},{x:400,y:400})===null})()'))
  ev('const G=TD.game,p=G.player;p.x=400;p.y=2200;p.cover=null;p.prone=false;p.stance="stand";G.shots=[];G.units=[TD.makeUnit("odRobot",400,2050,{a:0})];G.units[0].fireCd=999;window.uv=[]');
  for _ in range(24):frames();ev('uv.push([TD.game.units[0].vx,TD.game.units[0].vy])')
  check('enemy direction changes use bounded acceleration',ev('uv.slice(1).every((v,i)=>Math.hypot(v[0]-uv[i][0],v[1]-uv[i][1])<.5)'))
  ev('const G=TD.game;G.units=[];G.player.dead=true;G.player.deadT=.48;TD.Cam.follow(G.player.x,G.player.y,1)');snap('yuri_knockback_live')
  check('death uses rear knockback frames instead of front pose',ev('TD.footPose(TD.game.player).key.startsWith("od_cm_yuri_north_knockback")&&TD.footPose(TD.game.player).dir==="north"'))
  fresh();ev('const G=TD.game;G.fortress.pending=[];G.units=[];G.player.y=430;G.boss=TD.makeGosfer(G,400,195);G.boss.state="fight";G.boss.y=195;G.boss.hp=130;TD.Cam.follow(400,240,1)');frames(4);snap('gosfer_bar_live')
  check('Gosfer body hit accepts torso-level projectile',ev('const b=TD.game.boss;const h=b.hp; b.hit(b.x,b.y-15,3,2,{x:b.x,y:b.y-15,vx:0,vy:-10,drawLift:0,r:3})&&b.hp===h-2'))
  check('zero page, console or missing asset errors',not errors)
  result={'checks':checks,'errors':errors,'passed':sum(c['passed'] for c in checks),'failed':sum(not c['passed'] for c in checks)};(OUT/'verification.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2));browser.close()
finally:stop()
sys.exit(0 if not errors and all(c['passed'] for c in checks) else 1)
