from pathlib import Path
from playwright.sync_api import sync_playwright
import json,sys
R=Path('C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');O=R/'_shots/tactics36';O.mkdir(parents=True,exist_ok=True);checks=[];errors=[];data={}
def check(n,v):checks.append({'name':n,'passed':bool(v)});print(('PASS 'if v else'FAIL ')+n,flush=True)
with sync_playwright() as pw:
 b=pw.chromium.launch(args=['--autoplay-policy=no-user-gesture-required']);p=b.new_page(viewport={'width':1280,'height':960});p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text)if m.type=='error'else None)
 p.goto('http://127.0.0.1:8781/expansion/topdown/index.html?fullscreen=0&build=tactics36-map',wait_until='domcontentloaded');p.wait_for_function('window.TDGAME&&TD.game.state==="boot"',timeout=120000);ev=p.evaluate;ev('TDGAME.freeze();ART.warm([...Object.keys(TD_LEVEL36_ART.assets),...Object.keys(TD_CONTRA34_ART.assets)])');p.wait_for_function('[...Object.keys(TD_LEVEL36_ART.assets),...Object.keys(TD_CONTRA34_ART.assets)].every(k=>ART.get(k))',timeout=120000)
 for kind,ux,uy,px,py in [('shotgun',350,2450,400,2720),('double',210,2210,400,2450),('roller',550,2120,400,2400)]:
  ev(f'''TD.pilot='yuri';TD.game.sel=TD.MISSIONS.findIndex(m=>m.id===3);TDGAME.start();TD.game.fortress.pending=[];TD.game.units=[window.u=TD.makeUnit('c35_{kind}',{ux},{uy},{{a:0}})];Object.assign(TD.game.player,{{x:{px},y:{py},inv:0}});TD.Depth35.attacks['{kind}']=0;window.history36=[];TD.Achievements.queue=[];TD.game.msgs=[];TD.Cam.y={max(0,py-420)};TD.Cam.x=0;TD.Cam.zoom=1;''')
  saved=set()
  for i in range(50):
   ev("for(let j=0;j<30;j++){TD.game.t++;TD.unitTick(u,TD.game,1/60);history36.push({state:u.tactic36?.state,phase:u.attack35?.phase,x:u.x,y:u.y,cover:u.tactic36?.cover?.x,coverY:u.tactic36?.cover?.y,roll:u.rollState35,inside:TD.World.solidAt(u.x,u.y),blocked:!TD.Tactics36.clearSegment(u,TD.game.player),key:TD.Depth35.groundPose(u).key});}");p.wait_for_timeout(1)
   state=ev('u.rollState35||u.tactic36?.state')
   if state in ['hidden','attack','rolling']and state not in saved:
    ev('TDGAME.render()');p.locator('#screen').screenshot(path=str(O/f'map_{kind}_{state}.png'));saved.add(state)
  history=ev('history36');data[kind]={'history':history,'attacks':ev(f'TD.Depth35.attacks.{kind}'),'distance':ev('Math.hypot(u.x-TD.game.player.x,u.y-TD.game.player.y)')}
  check(kind+' attacks in the actual level 3 layout',data[kind]['attacks']>0)
  check(kind+' never enters a solid footprint',not any(x['inside']for x in history))
  if kind=='shotgun':check('shotgun closes from spawn to effective range',any(((x['x']-px)**2+(x['y']-py)**2)**.5<220 for x in history))
  if kind=='double':check('double barrel reloads behind actual beam column',any(x['state']=='hidden'and x['phase']=='recover'and x['blocked']for x in history))
  if kind=='roller':check('roller rolls between different actual level objects',len({(x['cover'],x['coverY'])for x in history if x['cover']})>=2 and any(x['roll']=='rolling'for x in history))
 # Real renderer, authored current plate, existing owner flash and expiry.
 flashed=ev('''()=>{const c=document.createElement('canvas');c.width=c.height=256;const x=c.getContext('2d');const v=TD.makeUnit('c35_double',128,210,{a:0});TD.drawAssaultRobot(x,v);const a=x.getImageData(0,0,256,256).data.slice();x.clearRect(0,0,256,256);v.flash=.1;TD.drawAssaultRobot(x,v);const z=x.getImageData(0,0,256,256).data;let n=0;for(let i=0;i<a.length;i+=4)if(a[i+3]&&z[i]+z[i+1]+z[i+2]>a[i]+a[i+1]+a[i+2])n++;TD.unitTick(v,TD.game,.2);return {pixels:n,expired:v.flash===0}}''')
 check('cover tactics retain visible enemy hit flash and expiry',flashed['pixels']>20 and flashed['expired'])
 check('actual map native browser has no errors',not errors)
 (O/'map_report.json').write_text(json.dumps({'checks':checks,'errors':errors,'data':data,'flash':flashed,'stats':ev('TD.Tactics36.stats')},indent=2));print(json.dumps({'passed':sum(x['passed']for x in checks),'total':len(checks),'errors':errors}),flush=True);b.close()
sys.exit(0 if all(x['passed']for x in checks)and not errors else 1)
