from pathlib import Path
from playwright.sync_api import sync_playwright
import json,sys
R=Path('C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');O=R/'_shots/tactics36';O.mkdir(parents=True,exist_ok=True)
checks=[];errors=[];data={}
def check(name,value):
 checks.append({'name':name,'passed':bool(value)});print(('PASS 'if value else 'FAIL ')+name,flush=True)
with sync_playwright() as pw:
 b=pw.chromium.launch(args=['--autoplay-policy=no-user-gesture-required']);p=b.new_page(viewport={'width':1280,'height':960});p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text)if m.type=='error'else None)
 p.goto('http://127.0.0.1:8781/expansion/topdown/index.html?fullscreen=0&build=tactics36-test',wait_until='domcontentloaded');p.wait_for_function('window.TDGAME&&TD.game.state==="boot"',timeout=120000)
 ev=p.evaluate;ev('TDGAME.freeze()')
 if not ev('!!TD.Tactics36'):p.add_script_tag(url='js/tactics36.js?qa=1')
 ev('ART.warm([...Object.keys(TD_DEPTH35_ART.assets),...Object.keys(TD_CONTRA34_ART.assets)])');p.wait_for_function('[...Object.keys(TD_DEPTH35_ART.assets),...Object.keys(TD_CONTRA34_ART.assets)].every(k=>ART.get(k))',timeout=120000)
 def fresh(id=3):ev(f'TD.pilot="yuri";TD.game.sel=TD.MISSIONS.findIndex(m=>m.id==={id});TDGAME.start();TD.game.player.inv=999;TD.Achievements.queue=[];TD.game.msgs=[];')
 def snap(name):ev('TDGAME.render()');p.locator('#screen').screenshot(path=str(O/(name+'.png')))
 def setup(kind):
  fresh();ev(f'''TD.game.fortress.pending=[];TD.World.load(800,2400,[]);TD.game.structures=[TD.makeStructure({{kind:'od_barrier',x:310,y:2010}}),TD.makeStructure({{kind:'od_bunker',x:540,y:2030}}),TD.makeStructure({{kind:'od_barrier',x:410,y:1780}})];TD.Nav.build();Object.assign(TD.game.player,{{x:400,y:2240}});TD.game.units=[window.u=TD.makeUnit('c35_{kind}',310,1880,{{a:0}})];TD.Cam.y=1820;TD.Cam.x=0;TD.Cam.zoom=1;window.history36=[];''')
 def tick(n):
  while n:
   q=min(30,n);ev('''n=>{for(let i=0;i<n;i++){TD.game.t++;TD.unitTick(u,TD.game,1/60);history36.push({x:u.x,y:u.y,state:u.tactic36?.state,cover:u.tactic36?.cover?.x,phase:u.attack35?.phase,roll:u.rollState35,key:TD.Depth35.groundPose(u).key,hidden:u.tactic36?.cover&&!TD.Tactics36.clearSegment(u,TD.game.player),inside:TD.World.solidAt(u.x,u.y)});}}''',q);p.wait_for_timeout(1);n-=q
 setup('shotgun');tick(900);data['shotgun']=ev('history36');snap('ground_shotgun')
 check('shotgun chooses actual cover',any(x['cover']for x in data['shotgun']))
 check('shotgun advances and peeks before firing',any(x['state']=='attack'for x in data['shotgun']) and ev('(TD.Depth35.attacks.shotgun||0)>0'))
 check('shotgun does not walk through cover',not any(x['inside']for x in data['shotgun']))
 setup('double');tick(1100);data['double']=ev('history36');snap('ground_double')
 check('double barrel retreats into physical blocked line during reload',any(x['state']=='hidden'and x['phase']=='recover'and x['hidden']for x in data['double']))
 check('double barrel uses authored full reload frames',len({x['key']for x in data['double']if 'reload_break_action'in x['key']})>=20)
 check('double barrel resumes attacks after reload',ev('(TD.Depth35.attacks.double||0)>=4'))
 ev('TD.hitStructure(TD.game,u.tactic36.cover,999)');tick(150);check('destroyed cover cannot remain assigned',ev('!u.tactic36.cover||!u.tactic36.cover.dead'))
 setup('roller');tick(1000);data['roller']=ev('history36');snap('ground_roller')
 check('rolling alien transfers between real objects',len({x['cover']for x in data['roller']if x['cover']})>=2 and ev('TD.Tactics36.stats.rollTransfers>0'))
 check('full folding and unfolding banks are played',all(len({x['key']for x in data['roller']if x['roll']==s})>=16 for s in ['fold','unfold']))
 check('rolling alien cannot tunnel through walls',not any(x['inside']for x in data['roller']))
 fresh(7);ev("TD.game.bastion.phase='fight';TD.game.bastion.totalWave=1;TD.game.bastion.turrets=[];TD.game.units=[];window.u=TD.Bastion.spawn(TD.game,'double',250,0);Object.assign(u,{phase:'peek',phaseT:0,x:250,y:338,duck:0});window.front36=[];")
 for _ in range(20):ev("TDGAME.step(30);front36.push({phase:u.phase,duck:u.duck,attack:u.attack35?.phase,key:TD.Bastion.unitPose(u)})");p.wait_for_timeout(1)
 data['frontDouble']=ev('front36');check('Bastion double barrel ducks for reload',any(x['phase']=='hide'and x['duck']>.8 and x['attack']=='recover'for x in data['frontDouble']));snap('front_double')
 fresh(7);ev("TD.game.bastion.phase='fight';TD.game.bastion.totalWave=1;TD.game.bastion.turrets=[];TD.game.units=[];window.u=TD.Bastion.spawn(TD.game,'roller',160,0);Object.assign(u,{phase:'peek',phaseT:0,x:160,y:338,duck:0,rollCd35:0});TD.game.bastion.enemyCover.push({x:440,y:350,hp:18,max:18,kind:'crate',flash:0});window.original36=u.cover;")
 for _ in range(10):ev('TDGAME.step(30)');p.wait_for_timeout(1)
 check('Bastion roller acquires surviving destination cover',ev('u.cover!==original36&&TD.game.bastion.enemyCover.includes(u.cover)&&u.cover.hp>0'));snap('front_roller')
 fresh();ev("TD.Escape29.begin(TD.game);TD.Escape29.setPhase(TD.game,'corridor');TD.game.escape29.pending=[];TD.Base33.ensure(TD.game);TD.game.escape29.solids=[{x:430,y:350,w:62,h:40,hp:200,max:200,flash:0,dead:false,key33:'b33_barrier',scale33:.7},{x:690,y:350,w:68,h:40,hp:200,max:200,flash:0,dead:false,key33:'b33_barrier',scale33:.7}];TD.game.escape29.base33Solids=TD.game.escape29.solids;Object.assign(TD.game.player,{x:240,y:350,inv:999});TD.game.escape29.enemies=[window.u={kind:'double',x:490,y:350,homeX:490,hp:99,max:99,phase:'fight',age:0,flash:0,walk:0,fireCd:.1}];window.side36=[];TD.Depth35.attacks.double=0;")
 for _ in range(24):ev("TDGAME.step(30);side36.push({x:u.x,state:u.tactic36?.state,cover:u.tactic36?.cover?.x,phase:u.attack35?.phase,low:u.coverBlend36})");p.wait_for_timeout(1)
 data['sideDouble']=ev('side36');snap('side_double');check('side double barrel uses real object cover',any(x['cover']for x in data['sideDouble']))
 check('side double barrel still attacks',ev('(TD.Depth35.attacks.double||0)>0'))
 check('side double barrel returns to far side and crouches during reload',any(x['state']=='hidden'and x['phase']=='recover'and x['x']>x['cover']and x['low']>.8 for x in data['sideDouble']))
 check('cover really intercepts projectile before hidden enemy',ev('''(()=>{const c=TD.game.escape29.solids[0],hp=c.hp,s={px:390,py:335,x:440,y:335,vx:500,vy:0,damage:2};const result=TD.Base33.hitProp(TD.game,s,()=>{},false);return result&&s.dead&&c.hp===hp-2})()'''))
 ev("TD.game.escape29.enemies=[window.u={kind:'roller',x:481,y:350,homeX:481,hp:99,max:99,phase:'fight',age:0,flash:0,walk:0,fireCd:.1,rollCd35:0}];window.sideRoll36=[];")
 for _ in range(12):ev("TDGAME.step(30);sideRoll36.push({x:u.x,cover:u.tactic36?.cover?.x,roll:u.rollState35,key:TD.Contra34.sidePose(u,TD.game).key})");p.wait_for_timeout(1)
 data['sideRoller']=ev('sideRoll36');check('side roller travels through gap to a different actual object',any(x['cover']==690 for x in data['sideRoller'])and any(x['roll']=='rolling'for x in data['sideRoller']));snap('side_roller')
 check('native browser has no errors',not errors)
 (O/'report.json').write_text(json.dumps({'checks':checks,'errors':errors,'data':data,'stats':ev('TD.Tactics36.stats')},indent=2));print(json.dumps({'passed':sum(x['passed']for x in checks),'total':len(checks),'errors':errors}),flush=True);b.close()
sys.exit(0 if all(x['passed']for x in checks)and not errors else 1)
