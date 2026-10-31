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

  fresh();measured['startingPickups']=ev('TD.game.pickups.map(k=>({kind:k.kind,x:k.x,y:k.y}))')
  escape('corridor');history=[];seen=set()
  for i in range(2600):
   state=ev("""(()=>{const G=TD.game,e=G.escape29,p=G.player;if(!e||e.finished||G.state==='gameover')return{done:true,mission:G.mission,state:G.state};
    const ids=[2];let dx=1,dy=0;
    const solid=e.solids.filter(s=>!s.dead&&s.x>p.x&&s.x-p.x<s.w/2+44).sort((a,b)=>a.x-b.x)[0];
    const enemy=e.enemies.filter(u=>!u.dead&&u.x>p.x).sort((a,b)=>a.x-b.x)[0];
    let target=enemy?{x:enemy.x,y:enemy.y-45}:{x:p.x+220,y:p.y-50};
    if(enemy&&enemy.kind==='heavy'&&enemy.x-p.x<330)dx=0;
    const bolt=e.enemyShots.filter(s=>!s.dead&&Math.hypot(s.x-p.x,s.y-(p.y-40))<230).sort((a,b)=>Math.hypot(a.x-p.x,a.y-p.y)-Math.hypot(b.x-p.x,b.y-p.y))[0];
    if(bolt){const lead=Math.hypot(bolt.x-p.x,bolt.y-(p.y-50))/1200;target={x:bolt.x+bolt.vx*lead,y:bolt.y+bolt.vy*lead};}
    if(solid&&!p.vault29&&p.y>=TD.Escape29.floorAt(p.x)-.5)ids.push(1);
    if(p.x>3170&&!e.doorBroken){dx=0;ids.push(4);target={x:3310,y:386};}
    if(e.doorBroken&&p.x>3220&&p.rollCd<=0){dy=1;ids.push(3);}
    pad(...ids);testPad.axes=[dx,dy];TD.Input.pointer.active=true;TD.Input.pointer.x=target.x-e.camX;TD.Input.pointer.y=target.y;
    TDGAME.step(1);return{done:false,phase:e.phase,x:p.x,y:p.y,dead:p.dead,deaths:G.deaths,lives:G.lives,kills:e.kills,blast:e.blastX,door:e.doorBroken,projectiles:e.enemyShots.length,cover:!!p.sideCover29};
   })()""")
   if i%120==0:history.append(state);print(i,state,flush=True)
   phase=state.get('phase')
   if phase and phase not in seen:seen.add(phase);shot('route_'+phase)
   if i%600==0:shot('route_at_'+str(i))
   if state.get('done'):break
  measured['corridorPlay']=history;measured['end']=state
  check('ordinary inputs clear corridor and self-destruct into level4',state.get('mission')==7)
  shot('route_end')
  # Cover must remain engaged even after movement is released.
  escape('corridor');ev('TD.game.escape29.pending=[];TD.game.escape29.enemies=[];Object.assign(TD.game.player,{x:387,y:350,inv:0});testPad.axes=[1,1];pad();');frames(2);ev('testPad.axes=[0,1];');frames(30)
  check('holding crouch maintains stationary cover',ev('!!TD.game.player.sideCover29'));shot('side_cover_hold');ev('pad(2);');frames(25);check('cover smoothly exposes authored shooting pose',ev('TD.game.player.peekExposed&&TD.game.escape29.shotCount>0'));shot('side_cover_fire')
  check('no browser errors',not errors)
  report={'checks':checks,'errors':errors,'measured':measured,'scope':'Continuous ordinary-input corridor run; no health, invulnerability, enemy or geometry changes during the run. Separate stationary-cover fixture.'};(O/'route_report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report),flush=True);browser.close()
finally:stop()
sys.exit(0 if all(c['passed']for c in checks)and not errors else 1)
