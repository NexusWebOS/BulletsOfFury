"""Native clock, render interpolation and exact simulation-state verification."""
from pathlib import Path
import json,sys
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[3] if 'expansion' in str(Path(__file__)) else Path('C:/Users/Mike/Desktop/Github Coding/BulletsOfFury')
sys.path.insert(0,str(ROOT/'_BUILD_SOURCE'));import shoot
OUT=ROOT/'_shots/overdrive_pacing_1013';OUT.mkdir(parents=True,exist_ok=True)
checks=[];errors=[]
def check(name,value):
 checks.append({'name':name,'passed':bool(value)});print(('PASS ' if value else 'FAIL ')+name,flush=True)
port,stop=shoot.serve(str(ROOT))
try:
 with sync_playwright() as pw:
  browser=pw.chromium.launch();page=browser.new_page(viewport={'width':1280,'height':960})
  page.on('pageerror',lambda e:errors.append(str(e)));page.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
  page.on('response',lambda r:errors.append(f'HTTP {r.status} {r.url}') if r.status>=400 else None)
  page.goto(f'http://127.0.0.1:{port}/expansion/topdown/index.html?fullscreen=0',wait_until='domcontentloaded',timeout=90000)
  page.wait_for_function('window.TDGAME&&TDGAME.G.state==="boot"',timeout=90000);page.evaluate('TDGAME.freeze()')
  page.wait_for_function('TD.FRONT_WARM.every(k=>!!ART.get(k))',timeout=60000)
  cadence={}
  for name,times in {'60Hz':[1/60]*60,'120Hz':[1/120]*120,'144Hz':[1/144]*144,'240Hz':[1/240]*240,'alternating25ms_8ms':[.025,1/120]*30}.items():
   cadence[name]=page.evaluate("times=>{TDGAME.freeze();TD.Frontend.go('title');const start=TD.game.t;let last;for(const s of times)last=TDGAME.advanceFrame(s);return{ticks:TD.game.t-start,alpha:last.alpha}}",times)
   check(f'{name} advances exactly 60 simulation ticks in one second',cadence[name]['ticks']==60)
  check('long stalls catch up by at most six ticks',page.evaluate('(()=>{TDGAME.freeze();return TDGAME.advanceFrame(1).ticks===6})()'))
  check('negative and nonfinite frame intervals do not advance simulation',page.evaluate('(()=>{TDGAME.freeze();const t=TD.game.t;TDGAME.advanceFrame(-1);TDGAME.advanceFrame(NaN);return TD.game.t===t})()'))
  page.evaluate("TD.pilot='yuri';TD.game.sel=0;TDGAME.start();TDGAME.freeze();TD.game.units=[];TD.game.player.inv=999999;TD.game.msgs=[];TD.Achievements.queue=[];TD.Input.pointer.active=false;window.drawSamples=[];window.savedTankDraw=TD.drawPlayerTank;TD.drawPlayerTank=function(ctx,p,o){if(p===TD.game.player)drawSamples.push({x:p.x,y:p.y,a:p.a,aim:p.aim,cx:TD.Cam.x,cy:TD.Cam.y});return savedTankDraw(ctx,p,o)};0")
  page.keyboard.down('d')
  pair=page.evaluate('(()=>{const p=TD.game.player,before={x:p.x,y:p.y,a:p.a,cx:TD.Cam.x,cy:TD.Cam.y};const clock=TDGAME.advanceFrame(1/60);const after={x:p.x,y:p.y,a:p.a,cx:TD.Cam.x,cy:TD.Cam.y};return{before,after,clock,draw:drawSamples.at(-1)}})()')
  check('actual keyboard movement advances the tank simulation',pair['after']['x']>pair['before']['x'])
  check('a fixed-step boundary draws the previous position',abs(pair['draw']['x']-pair['before']['x'])<1e-7)
  samples=[]
  for ratio in (.25,.5,.75):
   got=page.evaluate('(()=>{const state=TD.game.player.x,clock=TDGAME.advanceFrame(1/240);return{state,after:TD.game.player.x,draw:drawSamples.at(-1),clock}})()');samples.append(got)
   target=pair['before']['x']+(pair['after']['x']-pair['before']['x'])*ratio
   check(f'240Hz tank render advances to {ratio:g} of its fixed-step movement',got['clock']['ticks']==0 and abs(got['draw']['x']-target)<1e-7 and got['after']==got['state'])
  check('camera interpolation stays synchronized with the moving tank',all(abs(got['draw']['cx']-(pair['before']['cx']+(pair['after']['cx']-pair['before']['cx'])*ratio))<1e-7 for got,ratio in zip(samples,(.25,.5,.75))))
  check('exact render reads the restored current simulation position',page.evaluate('(()=>{TDGAME.render();return drawSamples.at(-1).x===TD.game.player.x})()'))
  page.keyboard.up('d');page.evaluate('TD.drawPlayerTank=savedTankDraw;TDGAME.step(1);TD.game.player.inv=0;TDGAME.render();0')
  page.locator('#screen').screenshot(path=str(OUT/'tank_native.png'))
  # A mission-owned fixture drives every render-owned collection through the
  # real main clock. No gameplay numbers or draw functions are changed on disk.
  result=page.evaluate('''(()=>{
   TDGAME.G.sel=5;TDGAME.start();TDGAME.freeze();const m=TD.MISSIONS[5],oldStep=m.exclusiveStep,oldDraw=m.drawWorld,oldHud=m.hud,G=TD.game;
   const p=G.player,u={x:100,y:100,a:3.13},boss={x:300,y:100,a:3.13},shot={x:400,y:100,a:0};
   G.units=[u];G.boss=boss;G.shots=[shot];G.eshots=[];G.bastion.bullets=[{x:10,y:10}];G.bastion.enemyShots=[{x:20,y:20}];G.bastion.hazards=[{x:30,y:30}];G.bastion.cursor={x:40,y:40};
   const objects=[p,u,boss,shot,...G.bastion.bullets,...G.bastion.enemyShots,...G.bastion.hazards,G.bastion.cursor,TD.Cam];
   const from=objects.map(o=>[o.x,o.y]);let seen;
   m.exclusiveStep=()=>{for(const o of objects){o.x+=4;o.y+=2;if(Number.isFinite(o.a))o.a=TD.M.wrap(o.a+.04);}G.time+=1/60;};
   m.drawWorld=()=>{seen=objects.map(o=>[o.x,o.y,o.a]);};m.hud=()=>true;
   try{
    TDGAME.advanceFrame(1/60);const exact=objects.map(o=>[o.x,o.y,o.a]);TDGAME.advanceFrame(1/120);
    const halfway=seen.every((v,i)=>Math.abs(v[0]-from[i][0]-2)<1e-7&&Math.abs(v[1]-from[i][1]-1)<1e-7);
    const restored=objects.every((o,i)=>o.x===exact[i][0]&&o.y===exact[i][1]&&o.a===exact[i][2]);
    const shortest=Math.abs(TD.M.wrap(seen[1][2]-3.15))<1e-7;
    const origX=p.x;m.drawWorld=()=>{throw Error('expected render fixture');};let threw=false;try{TDGAME.advanceFrame(0)}catch(e){threw=e.message==='expected render fixture'}
    return{halfway,restored,shortest,exceptionRestored:threw&&p.x===origX};
   }finally{m.exclusiveStep=oldStep;m.drawWorld=oldDraw;m.hud=oldHud;TDGAME.G.sel=0;TDGAME.start();TDGAME.freeze();}
  })()''')
  check('120Hz interpolates enemies, boss, camera, shots and Bastion reticle/projectiles/hazards',result['halfway'])
  check('all interpolated coordinates and angles restore after drawing',result['restored'])
  check('rotations cross the plus/minus PI boundary by the shortest path',result['shortest'])
  check('render exceptions still restore exact gameplay state',result['exceptionRestored'])
  page.evaluate("TD.Frontend.returnTo='pause';TD.Frontend.go('pause');TDGAME.freeze()")
  check('pause holds gameplay time and position while menus tick',page.evaluate('(()=>{const p=TD.game.player,x=p.x,t=TD.game.time;TDGAME.advanceFrame(.1);return p.x===x&&TD.game.time===t&&TD.game.state==="pause"})()'))
  before=page.evaluate('TD.game.t');page.wait_for_timeout(100);check('freeze suppresses automatic RAF stepping',page.evaluate('TD.game.t')==before)
  check('manual step remains exact while frozen',page.evaluate('(()=>{const before=TD.game.t;TDGAME.step(3);return TD.game.t===before+3})()'))
  reset=page.evaluate('(()=>{TDGAME.G.sel=5;TDGAME.start();const seven=TD.VW===640&&TD.VH===480&&!!TD.game.bastion;TDGAME.G.sel=3;TDGAME.start();const five=TD.VW===640&&TD.VH===480&&!TD.game.bastion&&!!TD.game.desert;TDGAME.G.sel=0;TDGAME.start();return{seven,five,cleared:TD.game.bastion===null&&TD.game.desert===null}})()')
  check('Levels 5 and 7 retain a close 640 by 480 viewport',reset['seven'] and reset['five'])
  check('mission starts clear prior Bastion and desert state',reset['cleared'])
  check('no page console or asset errors',not errors)
  (OUT/'report.json').write_text(json.dumps({'checks':checks,'cadence':cadence,'interpolation':samples,'errors':errors},indent=2)+'\n')
  browser.close()
finally:stop()
print(f'{sum(c["passed"] for c in checks)}/{len(checks)} checks passed');sys.exit(0 if all(c['passed'] for c in checks) else 1)
