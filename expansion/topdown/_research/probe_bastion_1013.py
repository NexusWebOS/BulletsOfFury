"""Real browser mechanics, input, art and boss-stage regression checks.

Boss setup shortcuts below isolate mechanics; difficulty/playthrough evidence is
separate in probe_bastion_balance_1013.py with live incoming damage.
"""
from pathlib import Path
import sys,json
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT/'_BUILD_SOURCE'));import shoot
OUT=ROOT/'_shots/bastion_1013';OUT.mkdir(parents=True,exist_ok=True);checks=[];errors=[]
def check(name,value):checks.append({'name':name,'passed':bool(value)});print(('PASS ' if value else 'FAIL ')+name,flush=True)
port,stop=shoot.serve(str(ROOT))
try:
 with sync_playwright() as pw:
  browser=pw.chromium.launch();p=browser.new_page(viewport={'width':1280,'height':960})
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text) if m.type=='error' else None);p.on('response',lambda r:errors.append(f'HTTP {r.status}: {r.url}') if r.status>=400 else None)
  p.goto(f'http://127.0.0.1:{port}/expansion/topdown/index.html?fullscreen=0&build=bastion-qa',timeout=90000);p.wait_for_function('window.TDGAME&&TDGAME.G.state==="boot"',timeout=90000)
  def ev(s):return p.evaluate(s)
  def frames(n=1):ev(f'TDGAME.step({n})')
  def snap(name):ev('TD.Achievements.queue=[];TD.game.msgs=[];TDGAME.render()');p.locator('#screen').screenshot(path=str(OUT/(name+'.png')))
  def mouse(x,y):
   q=p.locator('#screen').bounding_box();p.mouse.move(q['x']+x*q['width']/640,q['y']+y*q['height']/480)
  def fresh():
   for k in ['a','d','s','w','j','i','f','c','k',' ']:p.keyboard.up(k)
   p.mouse.up();ev('TDGAME.freeze();TD.pilot="yuri";TD.difficulty="normal";TDGAME.G.sel=5;TDGAME.start();TD.Achievements.queue=[];TD.Input.pointer.active=false')
  fresh()
  check('real mission seven uses fixed 640x480 camera',ev('TD.game.mission===7&&TD.VW===640&&TD.VH===480&&TD.Cam.zoom===1'))
  check('all authored assets load with even dimensions and safe gutters',ev('Object.entries(TD_BASTION_ART.assets).every(([k,m])=>ART.get(k)&&m.size.every(n=>n%2===0)&&(k==="pb_stage"||(m.bounds[0]>0&&m.bounds[1]>0&&m.bounds[2]<m.size[0]&&m.bounds[3]<m.size[1])))'))
  p.keyboard.down('f');frames();p.keyboard.up('f');frames(15)
  check('F latches cover and transitions fully down',ev('TD.game.player.prone&&TD.game.player.rise===0'))
  ev('window.oldX=TD.game.player.x');p.keyboard.down('d');frames(12);p.keyboard.up('d')
  check('side step works while behind cover',ev('TD.game.player.x>oldX+20&&TD.game.player.x<oldX+30&&TD.game.player.rise===0'));snap('cover_down')
  ev('window.oldX=TD.game.player.x;window.oldCursor={...TD.game.bastion.cursor}');p.keyboard.down('i');p.keyboard.down('a');p.keyboard.down('w');frames(12);p.keyboard.up('a');p.keyboard.up('w')
  check('held Retina stands and moves cursor independently of body',ev('TD.game.player.rise===1&&TD.game.player.x===oldX&&TD.game.bastion.cursor.x<oldCursor.x&&TD.game.bastion.cursor.y<oldCursor.y'));snap('retina_free_aim')
  p.keyboard.up('i');p.keyboard.down('f');frames();p.keyboard.up('f');frames(15)
  p.keyboard.down('k');p.keyboard.down(' ');frames(20);p.keyboard.up('k');p.keyboard.up(' ')
  check('base stage has no jump shooting',ev('!TD.game.player.jump&&TD.game.player.y===448'))
  # Core and turrets now belong to the third clear-gated line of each corridor.
  ev("TD.game.bastion.totalWave=2;TD.game.units=[];TD.Bastion.wave(TD.game)")
  frames(120);mouse(320,150);p.mouse.down();frames(45);p.mouse.up()
  check('mouse aim and visible projectiles damage wall core',ev('TD.game.bastion.wallCore.hp<40'));snap('first_breach_live')
  ev('TD.game.player.fireCd=0');p.mouse.down();frames();p.mouse.up()
  check('bullets begin at the rendered rifle socket',ev('(()=>{const s=TD.game.bastion.bullets.at(-1),q=TD.Bastion.playerSocket(TD.game);return s&&Math.hypot(s.sx-q.x,s.sy-q.y)<.01})()'));snap('registered_rifle_muzzle')
  check('wave enemies enter above the screen',ev('TD.game.bastion.entryLog.length>=3&&TD.game.bastion.entryLog.every(q=>q.y<0)'))
  ev('TD.game.units=[];TD.game.bastion.next=999;TD.game.bastion.turrets=[];TD.game.player.hp=6;TD.game.player.inv=0');p.keyboard.down('c');frames(15)
  ev('const p=TD.game.player,c=TD.game.bastion;c.enemyShots=[{sx:p.x,sy:160,x:p.x,y:160,tx:p.x,ty:405,t:0,duration:.1,kind:"mg",damage:1}];window.blocks=c.coverStops');frames(10)
  check('solid cover blocks real incoming bullets',ev('TD.game.player.hp===6&&TD.game.bastion.coverStops===blocks+1'));p.keyboard.up('c');frames(15)
  ev('const p=TD.game.player,c=TD.game.bastion;c.enemyShots=[{sx:p.x,sy:160,x:p.x,y:160,tx:p.x,ty:405,t:0,duration:.1,kind:"mg",damage:1}]');frames(10)
  check('exposed player takes damage',ev('TD.game.player.hp===5'))
  check('swept ellipses hit visible enemy bodies and reject empty space',ev('TD.Bastion.intersects({oldX:320,oldY:300,x:320,y:200},320,250,30,50)&&!TD.Bastion.intersects({oldX:420,oldY:300,x:420,y:200},320,250,30,50)'))
  fresh();ev('TD.Bastion.startBoss(TD.game)');frames(40);snap('core_orange_fill')
  check('Prism Heart bar fills orange before combat',ev('TD.game.boss.state==="enter"&&TD.game.boss.gauge>0&&TD.game.boss.gauge<1'));frames(235)
  check('core warns before prism beam discharge',ev('TD.game.bastion.hazards.length===2&&TD.game.bastion.hazards.every(h=>h.kind==="beam"&&h.t<h.delay)'))
  ev('TD.Bastion.coreHit(TD.game,999)');frames(62)
  check('core destruction produces full white transformation flash',ev('TD.game.bastion.flash===1'));snap('transformation_white');frames(48)
  check('white flash reveals living Helios form',ev('TD.game.boss.form==="helios"&&TD.game.boss.hp===360&&TD.game.boss.state==="enter"'))
  frames(40);snap('helios_orange_fill');frames(66);snap('helios_red_fill')
  check('Helios double-fill progresses orange then red',ev('TD.game.boss.t>1.3&&TD.game.boss.t<2.6&&TD.game.boss.gauge>.5'))
  frames(85);ev('TD.game.player.inv=999');snap('helios_live')
  ev('const b=TD.game.boss;b.state="volley";b.t=0;b.volley=0;const q=TD.Bastion.bossBody(b);window.oldBossHP=b.hp;TD.game.bastion.bullets=[{x:q.x,y:q.y-q.ry*.83,oldX:q.x,oldY:q.y-q.ry*.83,sx:q.x,sy:q.y-q.ry*.83,tx:q.x,ty:q.y-q.ry*.83,t:0,duration:.16,damage:2}]');frames()
  check('Helios upper body takes actual projectile damage',ev('TD.game.boss.hp===oldBossHP-2'))
  ev('window.states=new Set();window.minBossX=999;window.maxBossX=-999;window.patterns=new Set();window.orbs=false;window.geyser=false;window.beams=false;for(let n=0;n<2200;n++){TDGAME.step();const b=TD.game.boss,c=TD.game.bastion;states.add(b.state);patterns.add(b.pattern);minBossX=Math.min(minBossX,b.x);maxBossX=Math.max(maxBossX,b.x);orbs ||= c.enemyShots.some(e=>e.kind==="orb");geyser ||= c.hazards.some(h=>h.kind==="geyser");beams ||= c.hazards.some(h=>h.kind==="beam");}')
  check('Helios runs offscreen and returns',ev('(minBossX<0||maxBossX>640)&&states.has("return")'))
  check('Helios uses fire volleys lightning and jump geysers',ev('orbs&&geyser&&beams&&states.has("volley")&&states.has("lightning")&&states.has("jump")'))
  ev('const b=TD.game.boss;b.state="fight";b.pattern=3;TDGAME.step(82)');snap('helios_geyser_live')
  ev('TD.game.boss.state="fight";TD.game.player.inv=0;TD.Bastion.harm(TD.game,999)');frames(35);snap('backward_knockdown')
  check('death remains rear-facing authored knockback',ev('TD.game.player.dead&&TD_BASTION_ART.sequences.pb_yuri_death.frames.length===8'))
  ev('window.stageTime=TD.game.time');frames(95)
  check('boss death restarts current boss checkpoint without extra breach',ev('TD.game.boss.form==="helios"&&TD.game.boss.state==="enter"&&TD.game.bastion.room===2&&TD.game.time>=stageTime'))
  # Native gamepad mapping; no analogue axes needed.
  fresh();ev('window.padButtons=Array.from({length:16},()=>({pressed:false,value:0}));Object.defineProperty(navigator,"getGamepads",{configurable:true,value:()=>[{id:"QA six-button",connected:true,buttons:padButtons,axes:[]}]});TD.Input.setPadStyle("six")');frames()
  ev('padButtons[4]={pressed:true,value:1};padButtons[15]={pressed:true,value:1};window.px=TD.game.player.x;window.cx=TD.game.bastion.cursor.x');frames(12)
  check('six-button Z plus dpad free-aims without moving body',ev('TD.game.player.freeAim&&TD.game.player.x===px&&TD.game.bastion.cursor.x>cx'))
  ev('padButtons.forEach(b=>{b.pressed=false;b.value=0});padButtons[8]={pressed:true,value:1}');frames(15)
  check('Genesis Mode alone ducks behind base wall',ev('TD.game.player.rise===0'))
  ev('padButtons.forEach(b=>{b.pressed=false;b.value=0});TDGAME.G.sel=1;TDGAME.start();padButtons[8]={pressed:true,value:1};padButtons[4]={pressed:true,value:1}');frames()
  check('Genesis Mode plus Z maps covered blindfire on foot',ev('TD.Input.down("cover")&&TD.Input.down("retina")&&TD.Input.down("A")'))
  fresh();ev('TD.difficulty="easy";TD.game.player.inv=0;TD.Bastion.harm(TD.game,1)')
  check('new stage inherits selected damage difficulty',ev('TD.game.player.hp===5.35'))
  check('zero missing assets or browser errors',not errors)
  result={'checks':checks,'errors':errors,'passed':sum(q['passed'] for q in checks),'failed':sum(not q['passed'] for q in checks)}
  (OUT/'verification.json').write_text(json.dumps(result,indent=2));(ROOT/'docs/qa/overdrive_bastion_1013.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2));browser.close()
finally:stop()
sys.exit(0 if not errors and all(q['passed'] for q in checks) else 1)
