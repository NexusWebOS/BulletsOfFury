"""Native Chromium/rendered-art and real raw-M30 input checks for Escape29."""
from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image
import json,sys,hashlib
R=Path(__file__).resolve().parents[3];sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
from serve_bof_1013 import AssetServer
shoot.http.server.ThreadingHTTPServer=AssetServer
O=R/'_shots/escape29';O.mkdir(parents=True,exist_ok=True);checks=[];errors=[];measured={};cancelledMedia=[]
def check(name,v):checks.append({'name':name,'passed':bool(v)});print(('PASS 'if v else'FAIL ')+name,flush=True)
port,stop=shoot.serve(str(R))
try:
 with sync_playwright()as pw:
  browser=pw.chromium.launch();page=browser.new_page(viewport={'width':1280,'height':960});page.on('pageerror',lambda e:errors.append(str(e)));page.on('console',lambda m:errors.append(m.text)if m.type=='error'else None);page.on('response',lambda r:errors.append(f'HTTP {r.status} {r.url}')if r.status>=400 else None)
  page.on('requestfailed',lambda r:(cancelledMedia if r.failure=='net::ERR_ABORTED' and '/audio/'in r.url else errors).append(f'FAILED {r.url} {r.failure}'))
  page.add_init_script("""window.testPad={id:'6B controller (Vendor: 0ca3 Product: 0024)',mapping:'',index:0,connected:true,axes:[0,0],buttons:Array.from({length:12},()=>({pressed:false,value:0}))};Object.defineProperty(navigator,'getGamepads',{value:()=>[testPad]});window.pad=(...ids)=>testPad.buttons.forEach((b,i)=>{b.pressed=ids.includes(i);b.value=+b.pressed;});""")
  page.goto(f'http://127.0.0.1:{port}/expansion/topdown/index.html?fullscreen=0&build=overdrive1015-escape29-r1',wait_until='domcontentloaded',timeout=90000);page.wait_for_function('window.TDGAME&&TD.game.state==="boot"',timeout=120000);ev=page.evaluate
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
  check('all generated exports decode in native ART',ev('Object.keys(TD_ESCAPE29_ART.assets).every(k=>!!ART.get(k))'))
  check('even frame geometry and uniform unit',ev('Object.values(TD_ESCAPE29_ART.assets).every(m=>m.size[0]%2===0&&m.size[1]%2===0)&&TD_ESCAPE29_ART.unit.cell.join()==="192,224"'))
  check('13 authored aim positions each side',ev('["west","east"].every(s=>TD_ESCAPE29_ART.sequences["e29_aim_"+s].frames.length===13)'))
  fresh();check('stage3 one-hit health and no player health bar',ev('TD.game.player.hp===1&&TD.game.player.max===1&&TD.CornerHUD26.last.healthFillPixels===0'));shot('stage3_new_cover')
  ev('TD.game.player.stance="crouch";');check('new aiming bank preserves crouching',ev('!TD.footPose(TD.game.player).key.startsWith("e29_aim")'));ev('TD.game.player.stance="stand";')
  ev('TD.game.units=[];TD.game.fortress.pending=[];Object.assign(TD.game.player,{x:400,y:2178});testPad.axes=[0,-1];pad(8,2);');frames(1)
  check('rawM30 mode+A vaults toward nearby wall',ev('!!TD.game.player.vault29'));frames(10);shot('topdown_vault');ev('pad(5)');frames(1);ev('pad();');frames(34)
  check('vault crosses the collision footprint and queues landing roll',ev('TD.Combat29.stats.rollLandings>0&&TD.game.player.y<2120&&TD.game.player.roll>0'))
  ev('testPad.axes=[0,0];TD.game.player.roll=0;TD.game.player.jump=0;TD.game.player.vault29=null;TD.game.player.inv=0;TD.game.player.prone=false;TD.hurtPlayer(TD.game,1,0,0);');check('one unprotected hit kills Yuri',ev('TD.game.player.dead&&TD.game.player.hp<=0'));frames(120);check('stage3 retry preserves one-hit rules',ev('!TD.game.player.dead&&TD.game.player.hp===1&&TD.game.player.max===1'))
  fresh();ev('TD.game.units=[];TD.game.fortress.pending=[];TD.game.fortress.relays=3;Object.assign(TD.game.player,{x:400,y:430,inv:9999});TD.game.boss=TD.makeGosfer(TD.game,400,250);');frames(170)
  check('Gosfer has840HP and linked shield',ev('TD.game.boss.max===840&&TD.game.boss.shield'))
  ev('const b=TD.game.boss,s=b.barriers[0];window.shieldBefore=s.hp;TD.hitStructure(TD.game,s,999);');check('player cannot break linked shield barriers',ev('TD.game.boss.barriers[0].hp===shieldBefore'))
  states=set()
  for _ in range(90):frames(15);states.add(ev('TD.game.boss.state'))
  measured['gosferStates']=list(states);check('Gosfer rolls and vaults across the arena',('roll'in states and 'jump'in states)and ev('(TD.game.boss.vaultCount29||0)>0'))
  check('barriers are destroyed by Gosfer projectile ownership',ev('TD.game.boss.barrierLog.length===3&&TD.game.boss.barrierLog.every(q=>q.by==="gosfer")'))
  for _ in range(80):
   if ev('TD.game.boss.phase===2'):break
   frames(30)
  measured['gosferAfterDialogue']=ev('({phase:TD.game.boss.phase,state:TD.game.boss.state,lines:TD.game.boss.dialogueLog,scripted:TD.game.player.scripted})')
  check('dialogue and charged second phase finish',ev('TD.game.boss.phase===2&&!TD.game.boss.shield'));shot('gosfer_second_phase')
  ev('const b=TD.game.boss;b.state="recover";b.hp=2;b.hit(b.x,b.y,100,2);');check('boss defeat opens elevator instead of clearing level',ev('TD.game.fortress.exitReady29&&TD.game.bossDeadT===null'))
  ev('Object.assign(TD.game.player,{x:400,y:165,scripted:false});testPad.axes=[0,-1];pad();');frames(5);ev('testPad.axes=[0,0];');check('walking through north door starts elevator',ev('TD.game.escape29?.phase==="ascent"'));shot('elevator_ascent')
  frames(445);check('power loss and emergency phases reach timed hatch',ev('TD.game.escape29.phase==="hatch"&&["ascent","blackout","emergency","hatch"].every(s=>TD.game.escape29.log.some(q=>q.phase===s))'));shot('elevator_hatch')
  ev('pad(2,4);');frames(1);check('physicalA fires in elevator and Retina raises aim',ev('TD.game.escape29.shotCount>0&&TD.game.player.freeAim'));shot('hatch_aim_down');frames(130);ev('pad();');check('real shots break hatch and enter45degree slide',ev('["hinge","chute"].includes(TD.game.escape29.phase)&&TD.game.escape29.hatchHp<=0'));frames(70);shot('drone_slide')
  ev('pad(1,3,0);testPad.axes=[1,-1];');x=ev('TD.game.player.x');frames(12);check('chute ignores jumping rolling and manual movement',ev(f'TD.game.player.x==={x}&&!TD.game.player.roll&&!TD.game.player.jump&&!TD.game.player.vault29'));ev('pad();testPad.axes=[0,0];');
  ev('pad(9)');frames(1);ev('pad()');frames(1);age=ev('TD.game.escape29.age');frames(10);check('pause freezes escape simulation',ev(f'TD.game.state==="pause"&&TD.game.escape29.age==={age}'));ev('TDGAME.resume()');
  # Reproducible input-only aim assistant for the survival slide: targets bolts,
  # then vulnerable drones, using actual mouse/physicalA. No HP/inv changes.
  escape('chute');ev('pad(2);');
  slideHistory=[]
  for i in range(1800):
   state=ev('''(()=>{const G=TD.game,e=G.escape29,p=G.player;if(!e||e.phase!=='chute')return{done:true,phase:e?.phase,deaths:G.deaths};const bolt=e.enemyShots.filter(s=>!s.dead).sort((a,b)=>Math.hypot(a.x-p.x,a.y-p.y)-Math.hypot(b.x-p.x,b.y-p.y))[0],u=e.drones.filter(u=>!u.dead&&u.phase!=='retreat').sort((a,b)=>a.fireCd-b.fireCd)[0],q=bolt||u;if(q){const last=q._probe29||{x:q.x,y:q.y},vx=(q.x-last.x)*60,vy=(q.y-last.y)*60,lead=Math.hypot(q.x-p.x,q.y-(p.y-45))/900;TD.Input.pointer.active=true;TD.Input.pointer.x=q.x+vx*lead*.65;TD.Input.pointer.y=q.y+vy*lead*.65;q._probe29={x:q.x,y:q.y};}TDGAME.step(1);return{done:false,deaths:G.deaths,kills:e.kills,intercepts:e.intercepts,phase:e.phase};})()''')
   if i%120==0:slideHistory.append(state)
   if state.get('done'):break
  measured['slidePlay']=slideHistory;check('ordinary-input slide can reach corridor',state.get('phase')=='corridor');check('drones visibly take hits and can be destroyed',ev('TD.game.escape29.kills>0'));shot('corridor_entry')
  escape('corridor');ev('TD.game.escape29.pending=[];Object.assign(TD.game.player,{x:370,y:350});testPad.axes=[1,0];pad(1);');frames(1);check('sideview B vaults a crate',ev('!!TD.game.player.vault29'));frames(15);shot('side_vault');frames(30);check('sideview vault lands beyond crate',ev('TD.game.player.x>480&&!TD.game.player.vault29'))
  ev('pad();testPad.axes=[0,1];');frames(2);check('down crouches Yuri',ev('TD.game.player.stance==="crouch"'));ev('pad(8,3)');frames(1);ev('pad();testPad.axes=[0,0];');frames(1);check('mode+X toggles sideview prone',ev('TD.game.player.prone'));shot('side_prone')
  escape('escape');ev('TD.game.escape29.pending=[];Object.assign(TD.game.player,{x:3280,y:410});TD.game.escape29.camX=3030;TD.game.escape29.blastX=2700;TD.game.escape29.cursor={x:3310,y:386};TD.Input.pointer.active=true;TD.Input.pointer.x=280;TD.Input.pointer.y=386;pad(2,4);');frames(100);check('barrel volley blows metal exit door',ev('TD.game.escape29.doorBroken'));shot('barrel_breach');ev('pad(3);testPad.axes=[1,1];TD.game.player.rollCd=0;');frames(1);ev('pad();');frames(28);check('down+roll slides into breached door',ev('["doorSlide","drop"].includes(TD.game.escape29.phase)'));frames(160)
  check('escape enters formerstage7 as visiblelevel4',ev('TD.game.mission===7&&TD.MISSIONS[TD.game.sel].displayNumber===4&&TD.game.bastion&&TD.game.player.hp===1'));shot('level4_arrival')
  check('password pins list new campaign numbering without losing legacy slots',ev('TD.Frontend.pinnedPasswords().find(p=>p.id===4)?.name==="PRISM BASTION"&&TD.stepMission(TD.MISSIONS.findIndex(m=>m.id===3),1)===TD.MISSIONS.findIndex(m=>m.id===7)'))
  escape('chute');frames(80);ev('TD.game.escape29.cursor={x:110,y:150};TD.game.player.aim=TD.M.angTo(285,310,110,150);');shot('slide_back_aim');check('backward slide uses authored reverse-torso pose',ev('TD.Escape29.pose(TD.game)==="e29_slide_back"&&TD.Escape29.socket(TD.game).x<TD.game.player.x'))
  ev('TD.game.player.inv=0;TD.game.escape29.drones[0].flash=0;TDGAME.render();');before=page.locator('#screen').screenshot();ev('TD.game.escape29.drones[0].flash=.1;TDGAME.render();');after=page.locator('#screen').screenshot();check('new drone has visible native hit flash',before!=after);shot('drone_hit_flash');frames(8);check('drone hit flash expires',ev('TD.game.escape29.drones[0].flash===0'))
  fresh(7);frames(120);ev('TD.game.bastion.enemyShots=[];TD.game.bastion.turrets[0].cd=0;');frames(1);check('base turret creates finite-speed projectile instead of immediate damage',ev('TD.game.bastion.enemyShots.some(s=>s.duration>0&&s.duration<.7&&s.t<s.duration)'));frames(12);shot('fast_turret_projectiles')
  ev('TD.Bastion.damageCover(TD.game,TD.game.player.x,2);');check('every cover impact records damage and kicks screen',ev('TD.game.bastion.impactCount29>0&&TD.Cam.shake>0'))
  ev('testPad.axes=[0,-1];pad(1);');frames(1);check('base up+B starts a cover vault',ev('!!TD.game.player.baseVault29'));frames(22);shot('base_vault');frames(23);check('base vault crosses cover and lands',ev('TD.game.player.frontCover29&&TD.game.player.y===360'))
  fresh(7);ev('TD.game.player.inv=0;TD.Bastion.harm(TD.game,1)');check('base section is also one-hit lethal',ev('TD.game.player.dead'));frames(125);check('base respawn stays one-hit',ev('!TD.game.player.dead&&TD.game.player.hp===1'))
  old=json.loads((R/'_shots/lighting22/retained_art.json').read_text());check('all820preexisting graphics retained byte-for-byte',all(hashlib.sha256((R/k).read_bytes()).hexdigest()==h for k,h in old.items()))
  page.goto(f'http://127.0.0.1:{port}/expansion/topdown/art/escape29/preview.html',wait_until='domcontentloaded');page.wait_for_function('document.getElementById("status").textContent.startsWith("Playing")',timeout=60000);ev('paused=true;frame=5;document.getElementById("onion").checked=true;paint();')
  for bank in ['aim','run','vault','roll','cover_peek','slide_motion']:
   page.select_option('#bank',bank);ev('frame=5;paint();');page.locator('#review').screenshot(path=str(O/('onion_'+bank+'.png')))
  check('animation review loads every generated asset',ev('Object.keys(images).length===238'))
  check('no browser or missing asset errors',not errors)
  report={'build':'overdrive1015-escape29-r1','checks':checks,'passed':sum(c['passed']for c in checks),'failed':sum(not c['passed']for c in checks),'errors':errors,'cancelledMedia':cancelledMedia,'measured':measured,'scope':'Native Chromium, synthetic raw M30 input, isolated combat fixtures plus ordinary-input slide survival; not physical controller testing. ERR_ABORTED audio requests on intentional music changes/navigation recorded separately.'};(O/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({'passed':report['passed'],'failed':report['failed'],'errors':errors}));browser.close()
finally:stop()
sys.exit(0 if not report['failed']and not errors else 1)
