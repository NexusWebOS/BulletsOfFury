"""Real-browser truck steering/aim regression; fake hardware, production input."""
from pathlib import Path
import json, sys
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT/'_BUILD_SOURCE'))
import shoot
OUT=ROOT/'_shots/convoy_controls_1013';OUT.mkdir(parents=True,exist_ok=True)
checks=[];errors=[]
def check(name,value):
 checks.append({'name':name,'passed':bool(value)});print(('PASS ' if value else 'FAIL ')+name,flush=True)
port,stop=shoot.serve(str(ROOT))
try:
 with sync_playwright() as pw:
  b=pw.chromium.launch();p=b.new_page(viewport={'width':1280,'height':960});p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda e:errors.append(e.text) if e.type=='error' else None)
  p.add_init_script("window.testPad={id:'Convoy regression pad',index:0,connected:true,mapping:'standard',axes:[0,0,0,0],buttons:Array.from({length:24},()=>({pressed:false,value:0}))};Object.defineProperty(navigator,'getGamepads',{value:()=>[testPad]});")
  p.goto(f'http://127.0.0.1:{port}/expansion/topdown/index.html?fullscreen=0',wait_until='domcontentloaded',timeout=120000);p.wait_for_function('window.TDGAME&&TD.game.state==="boot"',timeout=120000);p.evaluate('TDGAME.freeze()');p.wait_for_function('ART.get("od_silverado_0")&&ART.get("od_gunner_0")&&ART.get("od_night_road")',timeout=60000)
  def ev(s):return p.evaluate(s)
  def step(n=1):
   while n:
    z=min(60,n);p.evaluate('n=>TDGAME.step(n)',z);p.wait_for_timeout(1);n-=z
  def neutral():ev('testPad.buttons.forEach(b=>{b.pressed=false;b.value=0});testPad.axes.fill(0);TD.Input.pointer.active=false;');step(1)
  def buttons(*names):
   ev('testPad.buttons.forEach(b=>{b.pressed=false;b.value=0});')
   for name in names:
    p.evaluate("name=>{const direction={up:12,down:13,left:14,right:15},n=direction[name]??TD.Input.padProfile()[name];if(typeof n!=='number')throw new Error('unexpected binding '+name);testPad.buttons[n].pressed=true;testPad.buttons[n].value=1}",name)
  def fresh(style='six',pursuit=True):
   neutral();ev(f'TD.Input.setPadStyle({json.dumps(style)});TD.pilot="yuri";TD.difficulty="normal";TD.game.sel=TD.MISSIONS.findIndex(m=>m.id===6);TDGAME.start();TD.Achievements.queue=[];')
   if pursuit:ev('TD.game.convoy.phase="pursuit";TD.game.convoy.nextWave=999;TD.game.units=[];TD.game.shots=[];TD.game.eshots=[];')
  def snap(name):ev('TDGAME.render()');p.locator('#screen').screenshot(path=str(OUT/(name+'.png')))
  fresh(pursuit=False);buttons('left');step(60)
  check('D-pad already steers during the searchlight opening without rotating the turret',ev('TD.game.player.x<170&&Math.abs(TD.M.wrap(TD.game.player.aim-Math.PI))<.001&&TD.game.shots.length===0'))
  neutral();step(60);ev('window.stoppedX=TD.game.player.x');step(60)
  check('released steering settles without lane oscillation or recentering',ev('Math.abs(TD.game.player.x-stoppedX)<.01'))
  fresh();buttons('right','X');step(65)
  check('D-pad right steers while north face-button fire stays north',ev('TD.game.player.x>480&&Math.abs(TD.M.wrap(TD.game.player.aim-Math.PI))<.001&&TD.game.shots.length>0&&TD.game.shots.every(s=>Math.abs(s.vx)<.001&&s.vy<0)'))
  check('gunner mount stays a fixed bed offset as the hull turns',ev('(()=>{const p=TD.game.player,q=TD.Convoy.bed(p);return Math.abs(Math.hypot(q.x-p.x,q.y-p.y)-24)<.001&&q.x<p.x-10})()'))
  check('hull leans into a gradual turn independently of turret direction',ev('Math.abs(TD.M.wrap(TD.game.player.a-Math.PI))>.4&&Math.abs(TD.M.wrap(TD.game.player.a-TD.game.player.aim))>.4'));snap('steer_right_fire_north')
  for direction,expression in [('up','p.y<225'),('down','p.y===380'),('left','p.x<175'),('right','p.x>465')]:
   fresh();ev('TD.game.player.aim=.72');buttons(direction);step(60)
   check('D-pad '+direction+' moves the truck and retains turret bearing',ev('(()=>{const p=TD.game.player;return '+expression+'&&Math.abs(p.aim-.72)<.001&&TD.game.shots.length===0})()'))
  buttons('right','down');step(300)
  check('truck stays inside visible road bounds',ev('TD.game.player.x<=548&&TD.game.player.y<=380&&Number.isFinite(TD.game.player.a)'))
  fresh();buttons('L','left','A');step(60)
  check('explicit free-aim shoulder gives D-pad the turret while Hotwire holds the lane',ev('Math.abs(TD.game.player.x-320)<.001&&Math.abs(TD.game.player.y-345)<.001&&Math.abs(TD.M.wrap(TD.game.player.aim-Math.PI/2))<.001&&TD.game.shots.some(s=>s.vx<0)'))
  fresh();ev('const u=TD.Convoy.spawn(TD.game,"jet",480,0);u.y=180;u.fireCd=999');buttons('Z');step(35)
  check('Retina still acquires a visible pursuing aircraft',ev('TD.game.player.retina?.locked&&Math.abs(TD.M.wrap(TD.game.player.aim-TD.M.angTo(TD.Convoy.bed(TD.game.player).x,TD.Convoy.bed(TD.game.player).y,TD.game.units[0].x,TD.game.units[0].y)))<.02'))
  neutral();buttons('B');step(1)
  check('fresh face-direction fire overrides a released Retina lock',ev('Math.abs(TD.M.wrap(TD.game.player.aim+Math.PI/2))<.001'))
  fresh('standard');buttons('right','A');ev('testPad.axes[2]=-1;testPad.axes[3]=0');step(60)
  check('standard-pad steering and right-stick aim remain independent',ev('TD.game.player.x>465&&Math.abs(TD.M.wrap(TD.game.player.aim-Math.PI/2))<.001'))
  fresh();box=p.locator('#screen').bounding_box();p.mouse.move(box['x']+box['width']*.3,box['y']+box['height']*.2);p.mouse.down();buttons('right');step(45)
  check('mouse aim continues tracking its pointer while D-pad steers',ev('TD.game.player.x>430&&Math.abs(TD.M.wrap(TD.game.player.aim-TD.M.angTo(TD.Convoy.bed(TD.game.player).x,TD.Convoy.bed(TD.game.player).y,TD.Input.pointer.x,TD.Input.pointer.y)))<.001&&TD.game.shots.length>0'));snap('mouse_aim_while_steering');p.mouse.up()
  fresh();buttons('left');step(20);neutral();ev('TD.game.player.damageCd=0;TD.Convoy.damage(TD.game,1000)');step(185)
  check('wreck restart restores center position and zero steering momentum',ev('TD.game.convoy.phase==="search"&&TD.game.player.x===320&&TD.game.player.y===345&&TD.game.player.steerVX===0&&TD.game.player.steerVY===0&&TD.game.player.hp===100'))
  # Full ordinary normal-hull pursuit: no target HP edits or damage suppression.
  fresh('standard',False);buttons('A')
  for _ in range(660):
   if ev('TD.game.state==="clear"||TD.game.convoy.phase==="wreck"||TD.game.convoy.restarts>0'):break
   ev('''const G=TD.game,p=G.player;const threat=G.eshots.filter(e=>e.shootable&&e.y>0&&e.y<470).sort((a,b)=>Math.hypot(a.x-p.x,a.y-p.y)-Math.hypot(b.x-p.x,b.y-p.y))[0];const target=threat||G.units.filter(u=>!u.dead&&u.y>30&&u.y<480).sort((a,b)=>Math.hypot(a.x-p.x,a.y-p.y)-Math.hypot(b.x-p.x,b.y-p.y))[0];if(target){const mount=TD.Convoy.bed(p),dx=target.x-mount.x,dy=target.y-mount.y,d=Math.hypot(dx,dy)||1;testPad.axes[2]=dx/d;testPad.axes[3]=dy/d;}''');step(15)
  full=ev('({state:TD.game.state,hull:TD.game.player.hp,kills:TD.game.kills,intercepts:TD.game.convoy.intercepts,restarts:TD.game.convoy.restarts,combat:TD.game.convoy.combat})')
  check('full normal-hull pursuit remains clearable using real input',full['state']=='clear' and full['restarts']==0 and full['hull']>0)
  check('no page or console errors',not errors)
  report={'checks':checks,'fullRun':full,'errors':errors,'passed':sum(c['passed'] for c in checks),'total':len(checks),'scope':'Simulated gamepad hardware through unchanged production Input.update and mission simulation. No physical M30 claim. Focused fixtures suppress wave scheduling; full run uses normal health, damage and all waves.'}
  (OUT/'verification.json').write_text(json.dumps(report,indent=2));(ROOT/'docs/qa/overdrive_convoy_controls_1013.json').write_text(json.dumps(report,indent=2));print(json.dumps(report),flush=True);b.close()
finally:stop()
sys.exit(0 if all(c['passed'] for c in checks) and not errors else 1)
