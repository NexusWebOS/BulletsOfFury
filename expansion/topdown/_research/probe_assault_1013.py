"""Native Chromium input, rendering, combat and complete 150-second pursuit QA."""
from pathlib import Path
import json,sys
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT/'_BUILD_SOURCE'))
import shoot
OUT=ROOT/'_shots/overdrive_assault_1013';OUT.mkdir(parents=True,exist_ok=True)
checks=[];errors=[]
def check(name,value):
 checks.append(dict(name=name,passed=bool(value)));print(('PASS ' if value else 'FAIL ')+name,flush=True)
port,stop=shoot.serve(str(ROOT))
try:
 with sync_playwright() as pw:
  browser=pw.chromium.launch();page=browser.new_page(viewport={'width':1280,'height':960})
  page.on('pageerror',lambda e:errors.append(str(e)));page.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
  page.on('response',lambda r:errors.append(f'HTTP {r.status} {r.url}') if r.status>=400 else None)
  page.add_init_script("window.testPad={id:'Assault QA standard controller',index:0,connected:true,mapping:'standard',axes:[0,0,0,0],buttons:Array.from({length:24},()=>({pressed:false,value:0}))};Object.defineProperty(navigator,'getGamepads',{value:()=>[testPad]});")
  page.goto(f'http://127.0.0.1:{port}/expansion/topdown/index.html?fullscreen=0&build=overdrive1013-assault-r1')
  page.wait_for_function('window.TDGAME && TDGAME.G.state==="boot"',timeout=90000);page.evaluate('TDGAME.freeze()')
  page.wait_for_function('Object.keys(TD_ASSAULT_ART.assets).every(k=>!!ART.get(k))',timeout=60000)
  page.wait_for_function('document.fonts.check("12px BOFCommand")')
  def frames(n=1):
   while n:
    k=min(60,n);page.evaluate('n=>TDGAME.step(n)',k);page.wait_for_timeout(1);n-=k
  def ev(s):return page.evaluate(s)
  def pad(*ids):page.evaluate('ids=>testPad.buttons.forEach((b,i)=>{b.pressed=ids.includes(i);b.value=+b.pressed})',list(ids))
  def fresh(sel=1):
   for k in ['w','a','s','d','r','f','c','j','h','u','i','Tab']:page.keyboard.up(k)
   page.mouse.up();pad();page.evaluate('sel=>{TD.pilot="yuri";TD.difficulty="normal";TD.Input.update();TD.Input.setPadStyle("standard");TDGAME.G.sel=sel;TDGAME.start();TDGAME.G.player.inv=99999;TD.Input.pointer.active=false;TD.Achievements.queue=[];}',sel);frames(2)
  def aim(dx,dy):
   pos=page.evaluate('([dx,dy])=>{const p=TD.game.player,r=document.getElementById("screen").getBoundingClientRect();return{x:r.x+(p.x+dx-TD.Cam.x)*r.width/TD.VW,y:r.y+(p.y+dy-(p.onfoot?TD.footLift(p):0)-TD.Cam.y)*r.height/TD.VH}}',[dx,dy]);page.mouse.move(pos['x'],pos['y']);frames(1)
  def snap(name):
   ev('TD.game.msgs=[];TD.game.player.inv=0;TD.game.player.flash=0;TDGAME.render()');page.locator('#screen').screenshot(path=str(OUT/(name+'.png')));ev('TD.game.player.inv=99999')
  check('all 518 authored exports resolve with even frame sizes',ev('Object.values(TD_ASSAULT_ART.assets).every(a=>a.size.every(n=>n%2===0))'))
  check('fortress restored into normal campaign; no boss in pursuit',ev('!TD.MISSIONS[1].hidden && TD.MISSIONS[4].id===6 && !TD.MISSIONS[4].boss && TD.stepMission(0,1)===1'))
  check('new truck password round-trips across every pilot/difficulty/partner',ev('TD.PILOTS.every(p=>["easy","normal","hard","furious","insanity"].every(d=>TD.COMPANIONS.every(c=>{const q=TD.Password.decode(TD.Password.encode(4,p,d,c));return q?.sel===4&&q.pilot===p&&q.difficulty===d&&q.companion===c})))'))
  fresh();check('fortress uses close 640x480 playfield and three armor points',ev('TD.VW===640&&TD.VH===480&&TD.game.player.max===3'))
  snap('fortress_start');page.keyboard.down('w');frames(25);check('walking advances feet with the north authored walk bank',ev('TD.game.player.y<2240&&TD.footPose(TD.game.player).dir==="north"&&TD.footPose(TD.game.player).action==="walk"'));page.keyboard.up('w')
  aim(180,0);page.mouse.down();frames(15);check('mouse aims and fires east while the body uses east artwork',ev('TD.footPose(TD.game.player).dir==="east"&&TD.game.shots.some(s=>s.vx>9&&Math.abs(s.vy)<.2)'));snap('yuri_run_fire');page.mouse.up()
  check('base rifle retains unlimited ammunition',ev('TD.game.player.weapons[0].id==="assault_rifle"&&TD.game.player.weapons[0].ammo===Infinity'))
  page.keyboard.down('r');frames(10);check('jump raises the authored jump sprite',ev('TD.game.player.jump>0&&TD.game.player.jumpZ>10&&TD.footPose(TD.game.player).action==="jump"'));snap('yuri_jump');page.keyboard.up('r');frames(70)
  page.keyboard.down('h');frames(9);check('roll uses the drawn tumble sequence',ev('TD.game.player.roll>0&&TD.footPose(TD.game.player).action==="roll"'));snap('yuri_roll');page.keyboard.up('h');frames(35)
  page.keyboard.down('f');frames();page.keyboard.up('f');frames(5);check('prone remains latched after release',ev('TD.game.player.prone&&TD.footPose(TD.game.player).action==="prone_fire"'));page.keyboard.down('w');frames(12);check('prone movement uses crawling artwork',ev('TD.footPose(TD.game.player).action==="crawl"'));snap('yuri_prone');page.keyboard.up('w')
  fresh();ev('TD.game.units=[];const p=TD.game.player;p.x=365;p.y=2110;TD.Cam.follow(p.x,p.y,1)');aim(0,-160);pad(4);frames(20);check('L shoulder crouches into real cover',ev('TD.game.player.cover?.kind==="od_barrier"&&TD.game.player.stance==="crouch"'));snap('cover_low');pad(4,0);frames(18);check('holding fire pops up and shoots beyond own cover',ev('TD.game.player.peekExposed&&TD.game.shots.length>0&&TD.game.shots.every(s=>s.y<2065)'));snap('cover_peek');pad(4);frames(4);check('releasing fire returns behind cover immediately',ev('!TD.game.player.peekExposed&&TD.game.player.hidden'));pad()
  pad(4);frames(1);ev('const G=TD.game,p=G.player;p.inv=0;G.eshots=[{k:"mg",x:365,y:2060,vx:0,vy:6,a:0,dmg:1,life:40,r:4,t:0}]');frames(2);check('cover absorbs enemy fire while crouched',ev('TD.game.player.hp===3&&TD.game.structures[0].hp<30'))
  pad(4,0);frames(18);ev('const G=TD.game;G.player.inv=0;G.eshots=[{k:"mg",x:365,y:2060,vx:0,vy:6,a:0,dmg:1,life:40,r:4,t:0}]');frames(2);check('exposed peek can be hit by enemy rounds',ev('TD.game.player.hp===2'));pad(4);frames(3)
  ev('const G=TD.game,p=G.player;p.x=265;p.y=1840;p.inv=99999;p.prone=true;p.aim=Math.PI;TD.Input.pointer.active=false;G.shots=[];G.eshots=[];G.units=[TD.makeUnit("odRobot",200,1630,{a:0})];G.units[0].hp=10000;G.units[0].fireCd=999;TD.Cam.follow(p.x,p.y,1)');frames(2);pad(4,5);frames(32);check('Retina can acquire the firing lane from a prone wall corner',ev('TD.game.player.retina?.locked'));pad(4,0);frames(20);check('prone wall peek physically moves around the wall end',ev('TD.game.player.cover?.kind==="od_wall"&&TD.game.player.y<1760'));snap('wall_prone_peek');pad(4);frames(2);check('releasing wall fire returns to the protected anchor',ev('Math.abs(TD.game.player.y-1840)<1&&TD.game.player.prone'));pad()
  ev('const G=TD.game,s=G.structures.find(s=>s.kind==="od_barrier");TD.hitStructure(G,s,100);');check('destroyed concrete cover removes the collision slab and emits effects',ev('TD.game.structures[0].dead&&TD.game.structures[0].rect.dead&&TD.FX.list.length>5'))
  ev('const G=TD.game;G.player.x=400;G.player.y=2230;G.player.aim=Math.PI;G.player.prone=false;G.player.cover=null;G.player.coverAnchor=null;G.player.peek=0;G.units=[TD.makeUnit("odRobot",540,2180,{a:0})];G.units[0].hp=10000;TD.Cam.follow(400,2230,1)');pad(5);frames(32);check('R shoulder acquires original BOF Retina on foot without missiles',ev('TD.game.player.retina?.locked'));snap('foot_retina');pad()
  ev('const p=TD.game.player;p.weapons.push({id:"minigun",lv:1,ammo:1,reserve:0});p.wi=1;p.fireCd=0');page.keyboard.down('j');frames(1);page.keyboard.up('j');check('exhausted upgrade returns to unlimited assault rifle',ev('TD.game.player.wi===0&&TD.game.player.weapons.length===1'))
  fresh();ev('const G=TD.game;G.units=[];for(const s of G.structures)if(s.kind==="od_relay")TD.hitStructure(G,s,100);G.player.y=550');frames(2);check('north doors trigger Gosfer entry and explosions',ev('TD.game.boss?.name==="GOSFER"&&TD.game.boss.state==="enter"&&TD.game.fortress.doorOpen'));frames(100);snap('gosfer_entry');frames(100)
  for _ in range(60):
   if ev('TD.game.eshots.some(s=>s.k==="laser")'):break
   frames(5)
  check('Gosfer fires actual laser volleys',ev('TD.game.boss.state==="fight"&&TD.game.eshots.some(s=>s.k==="laser")'));snap('gosfer_fight')
  ev('const b=TD.game.boss;b.dodgeCd=0;TD.game.shots.push({x:b.x,y:b.y+80,vx:0,vy:-4,k:"vulcan",a:Math.PI,dmg:2,r:3,t:0,life:40,lv:1});');frames(1);check('Gosfer reflex dodge has a cooldown',ev('TD.game.boss.evade>0&&TD.game.boss.dodgeCd>1'))
  pad(0,5)
  for _ in range(50):
   if ev('TD.game.boss.dead'):break
   frames(60)
  pad();check('aimed rifle fire defeats the moving and dodging Gosfer',ev('TD.game.boss.dead'));frames(190);check('defeating Gosfer advances to Machinists with a save password',ev('TD.game.state==="clear"&&TD.Password.decode(TD.game.results.password)?.sel===2'))
  fresh(0);check('four new armor families occur in existing tank stages',ev('["jackal","lancer","manticore","bastion"].every(k=>TD.MISSIONS.filter(m=>m.mode==="tank").some(m=>m.data.units.some(u=>u.type===k)))'))
  ev('const G=TD.game;G.units=["jackal","lancer","manticore","bastion"].map((k,i)=>TD.makeUnit(k,200+i*130,2100,{a:Math.PI}));G.player.y=2280;TD.Cam.follow(400,2180,1)');snap('new_armor')
  fresh(4);snap('night_searchlights');frames(520);check('searchlight opening transitions into pursuit',ev('TD.game.convoy.phase==="pursuit"&&TD.game.units.length>0'));frames(230);snap('night_pursuit')
  ev('const G=TD.game,p=G.player;G.eshots=[{k:"missile",x:p.x,y:p.y-80,vx:0,vy:1,a:0,r:10,shootable:true,life:90,t:0,dmg:9}];G.shots=[{k:"vulcan",x:p.x,y:p.y-60,vx:0,vy:-12,a:Math.PI,dmg:2,r:5,life:40,t:0,lv:1}]');frames(2);check('turret bullets intercept incoming rockets before hull impact',ev('TD.game.convoy.intercepts===1'))
  ev('TD.Convoy.damage(TD.game,1000)');check('hull zero explodes into a wreck',ev('TD.game.player.dead&&TD.game.convoy.phase==="wreck"'));snap('truck_destroyed');frames(182);check('hull loss restarts searchlight opening with full hull and zero combat time',ev('TD.game.convoy.phase==="search"&&TD.game.convoy.combat===0&&TD.game.player.hp===100&&TD.game.convoy.restarts===1'))
  frames(460);ev('TD.game.player.hp=1e8');frames(7300);check('red hyper-elite robots spawn in the final stretch',ev('TD.game.convoy.eliteSpawned>0'));snap('red_elite_pursuit');frames(2400);check('complete 150-second simulation reaches clear without a boss',ev('TD.game.state==="clear"&&TD.game.convoy.combat>=150&&!TD.game.boss'))
  # Feasibility run: standard pad aiming and fire only. Normal HP, no invulnerability,
  # and a 250 ms targeting cadence. This is a bot, not a claim of human play skill.
  fresh(4);pad(0)
  for _ in range(660):
   if ev('TD.game.state==="clear"||TD.game.convoy.restarts>0'):break
   ev('''const G=TD.game,p=G.player;const threat=G.eshots.filter(e=>e.shootable&&e.y>0&&e.y<470).sort((a,b)=>Math.hypot(a.x-p.x,a.y-p.y)-Math.hypot(b.x-p.x,b.y-p.y))[0];const target=threat||G.units.filter(u=>!u.dead&&u.y>30&&u.y<480).sort((a,b)=>Math.hypot(a.x-p.x,a.y-p.y)-Math.hypot(b.x-p.x,b.y-p.y))[0];if(target){const dx=target.x-p.x,dy=target.y-(p.y+24),d=Math.hypot(dx,dy)||1;testPad.axes[2]=dx/d;testPad.axes[3]=dy/d;}''');frames(15)
  check('normal-hull pursuit is survivable using turret aim and fire',ev('TD.game.state==="clear"&&TD.game.convoy.restarts===0&&TD.game.player.hp>0'))
  hull_result=ev('({state:TD.game.state,hull:TD.game.player.hp,elapsed:TD.game.convoy.combat,kills:TD.game.kills,intercepts:TD.game.convoy.intercepts,restarts:TD.game.convoy.restarts})')
  print('NORMAL HULL RESULT',hull_result,flush=True);pad()
  check('searchlight pursuit does not award an undetected ghost clear',ev('TD.Stealth.alerts===1&&!TD.game.results.ghost'))
  # Inspect every one of Yuri's 384 core pose frames in the owning game renderer.
  ev('const cv=document.createElement("canvas");cv.id="pose-review";cv.width=cv.height=1024;cv.style.cssText="position:absolute;top:0;left:0;width:1024px;height:1024px;z-index:5";document.body.append(cv)')
  draws=[]
  for frame in range(6):
   draws.append(page.evaluate('''f=>{const cv=document.getElementById('pose-review'),c=cv.getContext('2d');c.imageSmoothingEnabled=false;c.fillStyle='#17242e';c.fillRect(0,0,1024,1024);const original=c.drawImage;let count=0;c.drawImage=function(...args){count++;return original.apply(this,args)};const dirs=['south','southwest','west','northwest','north','northeast','east','southeast'],actions=['walk','run_fire','jump','crouch','roll','prone_fire','crawl','peek'];actions.forEach((a,r)=>dirs.forEach((d,col)=>{const key=TD_ASSAULT_ART.sequences['yuri_'+d+'_'+a].frames[f];TD.AssaultArt.draw(c,key,col*128+64,r*128+104,{s:.42});c.fillStyle='#dde9ef';c.font='10px monospace';c.fillText(d+' / '+a,col*128+2,r*128+119)}));c.drawImage=original;return count;}''',frame))
   page.locator('#pose-review').screenshot(path=str(OUT/f'all_yuri_frame_{frame}.png'))
  check('every core pose renders through the game ART context',draws==[64]*6)
  check('no page, console or missing-file errors',not errors)
  (OUT/'report.json').write_text(json.dumps({'checks':checks,'normalHullResult':hull_result,'errors':errors},indent=2),encoding='utf-8');browser.close()
finally:stop()
print(f'SUMMARY {sum(c["passed"] for c in checks)}/{len(checks)} checks; {len(errors)} errors',flush=True)
for error in errors[:12]:print(error,flush=True)
sys.exit(0 if all(c['passed'] for c in checks) and not errors else 1)
