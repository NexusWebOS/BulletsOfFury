"""Native movement, offscreen entry, Retina and pursuit regression checks."""
from pathlib import Path
import json,sys
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT/'_BUILD_SOURCE'))
import shoot
OUT=ROOT/'_shots/desert_breaker_1013';OUT.mkdir(parents=True,exist_ok=True)
checks=[];errors=[]
def check(n,v):
 checks.append({'name':n,'passed':bool(v)});print(('PASS ' if v else 'FAIL ')+n,flush=True)
port,stop=shoot.serve(str(ROOT))
try:
 with sync_playwright() as pw:
  b=pw.chromium.launch();p=b.new_page(viewport={'width':1280,'height':960});p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda e:errors.append(e.text) if e.type=='error' else None)
  p.add_init_script("window.testPad={id:'Desert QA pad',index:0,connected:true,mapping:'standard',axes:[0,0,0,0],buttons:Array.from({length:24},()=>({pressed:false,value:0}))};Object.defineProperty(navigator,'getGamepads',{value:()=>[testPad]});")
  p.goto(f'http://127.0.0.1:{port}/expansion/topdown/index.html?fullscreen=0',wait_until='domcontentloaded',timeout=120000);p.wait_for_function('window.TDGAME && TD.game.state==="boot"',timeout=90000);p.evaluate('TDGAME.freeze()')
  assert p.evaluate('!!TD.Desert'),'desert module must be loaded by production index'
  p.wait_for_function('ART.get("od_desert_ground")&&ART.get("of_scout_air_idle")&&ART.get("od_jackal_0")',timeout=30000)
  def ev(s):return p.evaluate(s)
  def step(n=1):
   while n:
    z=min(60,n);p.evaluate('n=>TDGAME.step(n)',z);p.wait_for_timeout(1);n-=z
  def fresh(mid=5):
   for key in ['w','a','s','d','j','i','k','r']:p.keyboard.up(key)
   p.mouse.up();ev(f'TD.pilot="yuri";TD.difficulty="normal";TD.game.sel=TD.MISSIONS.findIndex(m=>m.id==={mid});TDGAME.start();TD.game.player.inv=999999;TD.Input.pointer.active=false;TD.Achievements.queue=[]');step(2)
  def snap(name):
   ev('TD.game.player.flash=0;TD.game.player.inv=0;TD.game.msgs=[];TDGAME.render()');p.locator('#screen').screenshot(path=str(OUT/(name+'.png')));ev('TD.game.player.inv=999999')
  check('museum campaign slot is a tank desert and old password slot still resolves',ev('TD.MISSIONS.find(m=>m.id===5).mode==="tank"&&TD.MISSIONS.find(m=>m.id===5).data.name==="DESERT BREAKER"&&TD.Password.decode("OD-237D-5JXP").sel===TD.MISSIONS.findIndex(m=>m.id===5)'))
  fresh();step(270);check('mixed tanks and aircraft enter beyond north viewport before travelling in',ev('TD.game.desert.entries.length===3&&TD.game.desert.entries.every(e=>e.y+90<e.top)&&TD.game.units.some(u=>u.type==="desertAir")'))
  snap('desert_first_formation')
  ev('TD.game.units=[];TD.game.desert.pending=[];TD.game.desert.next=999;TD.game.player.x=400;TD.game.player.y=870;TD.game.player.a=Math.PI')
  p.keyboard.down('s');step(60);p.keyboard.up('s');check('player smoothly makes a full reversal instead of refusing 180 degree input',ev('Math.abs(TD.M.wrap(TD.game.player.a))<.1&&TD.game.player.y>960'))
  fresh();ev('TD.game.units=[TD.makeUnit("jackal",400,900,{a:0,mode:"alert",ramCd:0,fireCd:999})];TD.game.desert.pending=[];TD.game.desert.next=999;TD.game.player.x=400;TD.game.player.y=1080;TD.Cam.follow(400,995,1)');step(1)
  check('ram gives a .9 second stationary warning',ev('TD.game.units[0].ramState==="warn"&&TD.game.units[0].ramT>.8'));snap('desert_ram_warning');step(60)
  check('ram accelerates along the announced heading',ev('TD.game.units[0].ramState==="charge"&&TD.game.units[0].armorSpeed>3&&Math.abs(TD.game.units[0].a)<.001'))
  p.keyboard.down('d');step(40);p.keyboard.up('d');check('moving aside evades the committed ram without homing',ev('TD.game.player.x>470&&Math.abs(TD.game.units[0].x-400)<8'))
  check('cannon hit query catches hull between prior and current projectile position',ev('TD.vehicleShotHit({x:20,y:0,r:8},{x:40,y:0,vx:40,vy:0,r:2})&&!TD.vehicleShotHit({x:20,y:20,r:8},{x:40,y:0,vx:40,vy:0,r:2})'))
  fresh();ev('TD.game.desert.next=999;TD.game.desert.pending=[];TD.game.units=[TD.makeUnit("desertAir",400,860,{a:0,fireCd:999})];TD.game.player.x=400;TD.game.player.y=985;TD.Cam.follow(400,850,1)');p.keyboard.down('i');step(35);p.keyboard.up('i')
  check('Retina acquires the actual flying unit',ev('TD.game.player.retina?.locked&&TD.game.player.retina.target.id===TD.game.units[0]'));p.keyboard.down('k');step(1);p.keyboard.up('k');check('locked cannon fires a missile that retains the aircraft target',ev('TD.game.shots.some(s=>s.retinaTarget?.id===TD.game.units[0])&&TD.game.player.missiles===11'));snap('desert_retina_air');step(90)
  check('guided missile damages or destroys the moving aircraft',ev('TD.game.units[0].hp<9'))
  # Full wave progression through real hit/death accounting; player weapon
  # behavior and missile flight are tested independently above.
  fresh();ev('TD.game.player.inv=999999')
  for _ in range(70):
   step(60);ev('for(const u of TD.game.units)if(!u.dead&&!u.entering)TD.hitUnit(TD.game,u,100,u.x,u.y)')
   if ev('TD.game.state==="clear"'):break
  check('all four formations complete into the next mission',ev('TD.game.state==="clear"&&TD.game.desert.defeated===16&&TD.Password.decode(TD.game.results.password).sel===TD.MISSIONS.findIndex(m=>m.id===6)'))
  fresh();check('all mobile armor families keep finite continuous positions through turns and braking',ev('''(()=>{const G=TD.game,types=Object.entries(TD.ET).filter(([k,d])=>!d.still&&!d.foot&&(d.odTank||d.et||d.mod)).map(([k])=>k);G.props=[];G.units=[];G.player.x=400;G.player.y=960;return types.every(type=>{const u=TD.makeUnit(type,420,800,{a:Math.PI/2,mode:'alert',ramCd:99});G.units=[u];let prev=u.a;for(let i=0;i<160;i++){TD.unitTick(u,G,1/60);if(!Number.isFinite(u.x+u.y+u.a+u.armorSpeed)||Math.abs(TD.M.wrap(u.a-prev))>.051)return false;prev=u.a;}return true;});})()'''))
  fresh(6);step(650);check('pursuit reinforcements all begin above the visible north edge',ev('TD.game.units.length>0&&TD.game.units.every(u=>u.y<480)'))
  ev('TD.Convoy.wave(TD.game);TD.Convoy.wave(TD.game)');check('truck and runner spawn helpers normalize south spawns to north approach',ev('TD.game.units.filter(u=>u.t===0).every(u=>u.y< -100)'));step(320);snap('pursuit_smooth_convoy')
  check('gun trucks have a drive state and larger hittable hull',ev('TD.game.units.some(u=>u.kind==="truck"&&u.r===43&&Number.isFinite(u.vx)&&u.driveState)'))
  ev('TD.game.player.damageCd=0;TD.Convoy.damage(TD.game,1000)');step(185);check('pursuit wreck still resets opening and full hull',ev('TD.game.convoy.phase==="search"&&TD.game.player.hp===100&&TD.game.convoy.restarts===1'))
  fresh(6);ev('TD.Input.setPadStyle("standard");testPad.buttons[0].pressed=true;testPad.buttons[0].value=1;TD.game.player.inv=0')
  for _ in range(660):
   if ev('TD.game.state==="clear"||TD.game.convoy.phase==="wreck"||TD.game.convoy.restarts>0'):break
   ev('''const G=TD.game,p=G.player;const threat=G.eshots.filter(e=>e.shootable&&e.y>0&&e.y<470).sort((a,b)=>Math.hypot(a.x-p.x,a.y-p.y)-Math.hypot(b.x-p.x,b.y-p.y))[0];const target=threat||G.units.filter(u=>!u.dead&&u.y>30&&u.y<480).sort((a,b)=>Math.hypot(a.x-p.x,a.y-p.y)-Math.hypot(b.x-p.x,b.y-p.y))[0];if(target){const dx=target.x-p.x,dy=target.y-(p.y+24),d=Math.hypot(dx,dy)||1;testPad.axes[2]=dx/d;testPad.axes[3]=dy/d;}''');step(15)
  check('normal-hull full pursuit remains survivable with aim and fire',ev('TD.game.state==="clear"&&TD.game.convoy.restarts===0&&TD.game.player.hp>0'))
  print('PURSUIT BOT',ev('({combat:TD.game.convoy.combat,input:TD.Input.state,state:TD.game.state,hull:TD.game.player.hp,kills:TD.game.kills,intercepts:TD.game.convoy.intercepts,restarts:TD.game.convoy.restarts})'),flush=True)
  check('zero browser errors',not errors)
  (OUT/'verification.json').write_text(json.dumps({'checks':checks,'errors':errors,'passed':sum(c['passed'] for c in checks),'total':len(checks)},indent=2));print(json.dumps({'passed':sum(c['passed'] for c in checks),'total':len(checks),'errors':errors}),flush=True);b.close()
finally:stop()
sys.exit(0 if all(c['passed'] for c in checks) and not errors else 1)
