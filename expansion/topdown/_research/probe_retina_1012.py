"""Native BOF Retina, shoulder aim, menu A and smaller Warrior regression.

Isolated saves, actual keyboard/pointer events and synthetic Gamepad reports.
Protected combat fixtures run the owning gameplay code and authored renderer.
"""
from pathlib import Path
import json,sys
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT/'_BUILD_SOURCE'))
import shoot
OUT=ROOT/'_shots/overdrive_retina_1012';OUT.mkdir(parents=True,exist_ok=True)
checks=[];errors=[];observations={}
def check(name,value):
 checks.append({'name':name,'passed':bool(value)});print(('PASS ' if value else 'FAIL ')+name,flush=True)
port,stop=shoot.serve(str(ROOT))
try:
 with sync_playwright() as pw:
  browser=pw.chromium.launch();page=browser.new_page(viewport={'width':1600,'height':1200})
  page.on('pageerror',lambda e:errors.append(str(e)));page.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
  page.on('response',lambda r:errors.append(f'HTTP {r.status} {r.url}') if r.status>=400 else None)
  page.add_init_script("""window.testPad={id:'Overdrive Retina and shoulder fixture',index:0,connected:true,mapping:'standard',axes:[0,0,0,0],buttons:Array.from({length:24},()=>({pressed:false,value:0}))};Object.defineProperty(navigator,'getGamepads',{configurable:true,value:()=>[testPad]});""")
  page.goto(f'http://127.0.0.1:{port}/expansion/topdown/index.html?fullscreen=0&build=overdrive1012-retina-r1')
  page.wait_for_function('window.TDGAME && TDGAME.G.state==="boot"',timeout=60000);page.evaluate('TDGAME.freeze()')
  page.wait_for_function('TD.Retina.warm.every(k=>!!ART.get(k)) && TD.FRONT_WARM.every(k=>!!ART.get(k))',timeout=30000)
  page.wait_for_function('document.fonts.check("11px BOFCommand")')
  def frames(n=1):
   while n:
    k=min(n,30);page.evaluate('n=>TDGAME.step(n)',k);page.wait_for_timeout(1);n-=k
  def pad(*ids):page.evaluate('ids=>testPad.buttons.forEach((b,i)=>{b.pressed=ids.includes(i);b.value=+b.pressed})',list(ids))
  def tap(i):pad(i);frames();pad();frames(26)
  def go(s):pad();page.evaluate("s=>{TD.Frontend.returnTo='title';TD.Frontend.pending=null;TD.Frontend.go(s)}",s);frames(18)
  def fresh(style='six'):
   pad();page.keyboard.up('w');page.mouse.up()
   page.evaluate("""style=>{testPad.axes=[0,0,0,0];TD.Input.update();TD.Input.setPadStyle(style);TDGAME.G.sel=0;TDGAME.start();const G=TDGAME.G,p=G.player;G.units=[];G.props=[];G.structures=[];G.pickups=[];G.msgs=[];TD.Achievements.queue=[];TD.World.load(800,4000,[]);p.x=400;p.y=2200;p.inv=99999;p.a=p.aim=Math.PI;TD.Input.pointer.active=false;TD.Cam.follow(p.x,p.y,1);}""",style);frames(2)
  def point(dx,dy):
   pos=page.evaluate("""([dx,dy])=>{const p=TDGAME.G.player,r=document.getElementById('screen').getBoundingClientRect(),v=TD.Display;return{x:r.x+(p.x+dx-TD.Cam.x)*TD.Cam.zoom*r.width/v.w,y:r.y+(p.y+dy-TD.Cam.y)*TD.Cam.zoom*r.height/v.h}}""",[dx,dy]);page.mouse.move(pos['x'],pos['y'])
  def snap(name):page.evaluate('TDGAME.G.msgs=[];TDGAME.G.player.inv=0;TDGAME.render();TDGAME.G.player.inv=99999');page.locator('#screen').screenshot(path=str(OUT/(name+'.png')))
  def targets():
   page.evaluate("""const G=TDGAME.G;G.units=[[570,2140],[260,2090]].map(([x,y])=>{const u=TD.makeUnit('camera',x,y,{a:0});u.hp=u.max=10000;return u});""")
  frames(18);tap(5)
  check('nonstandard printed A on browser button 5 starts the game like Start',page.evaluate('TDGAME.G.state==="intro"'))
  tap(5);check('the same face button can skip the opening into the title',page.evaluate('TDGAME.G.state==="title"'))
  tap(5);check('A selects New Game from the title',page.evaluate('TDGAME.G.state==="difficulty"'))
  tap(5);check('A selects difficulty',page.evaluate('TDGAME.G.state==="pilot"'))
  tap(5);check('A launches the actual pilot briefing',page.evaluate('TDGAME.G.state==="brief"'))
  frames(40);tap(5);check('A confirms the briefing into gameplay',page.evaluate('TDGAME.G.state==="play"'))
  go('pause');tap(5);check('A selects Resume in the pause menu',page.evaluate('TDGAME.G.state==="play"'))
  go('password');tap(5);check('A selects the highlighted password keypad character',page.evaluate('TD.Frontend.pw==="OD-A"'))
  go('options');page.evaluate("TD.OriginalOptions.select(TD.OriginalOptions.rows().filter(r=>r.t!=='head').findIndex(r=>r.who===1&&r.act==='aimLeft'))");frames();tap(5)
  check('A arms a binding through the exact original Options renderer',page.evaluate('TD.OriginalOptions.snapshot().capture==="aimLeft"'))
  page.keyboard.down('Escape');frames();page.keyboard.up('Escape');frames(18);tap(1)
  check('B remains Back and cancels Options without selecting',page.evaluate('TDGAME.G.state==="title"'))
  go('padsetup');page.evaluate('TD.Input.beginSetup();TD.Input.setup.done=true');frames(18);tap(5)
  check('A completes controller setup just like Start',page.evaluate('TDGAME.G.state!=="padsetup" && !TD.Input.setup'))

  fresh();point(175,0);frames(20);pad(12);frames(18);pad(6,12);frames();pad(6,14);frames(20)
  check('L shoulder captures existing northward travel and D-pad aims west despite an idle mouse',page.evaluate('TDGAME.G.player.cruising && TDGAME.G.player.vy< -2 && Math.abs(TDGAME.G.player.vx)<.1 && Math.abs(TD.M.wrap(TDGAME.G.player.aim-Math.PI/2))<.05'))
  pad(6,14,0);frames(8)
  check('A fires west along shoulder-controlled turret aim while the tank still cruises north',page.evaluate('(()=>{const s=TDGAME.G.shots.at(-1);return TDGAME.G.player.vy<0&&s&&s.vx< -7&&Math.abs(s.vy)<.4})()'))
  pad(6,14)
  snap('shoulder_aim_west')
  point(170,0);frames(20)
  check('new mouse movement can still aim east while shoulder cruise continues north',page.evaluate('TDGAME.G.player.vy< -2 && Math.abs(TD.M.wrap(TDGAME.G.player.aim+Math.PI/2))<.15'))
  pad(6,15);frames(20)
  check('a fresh D-pad direction takes shoulder aim back from the mouse',page.evaluate('TD.Input.state.aimSource==="cruise" && Math.abs(TD.M.wrap(TDGAME.G.player.aim+Math.PI/2))<.05'))
  fresh();page.evaluate("TD.Input.setPadBinding('L',10);TD.Input.setPadBinding('R',11)");point(175,0);frames(20);pad(12);frames(12);pad(10,12);frames();pad(10,14);frames(20)
  check('a saved nondefault L shoulder controls free aim and continued travel',page.evaluate('TDGAME.G.player.cruising && TDGAME.G.player.vy<0 && Math.abs(TD.M.wrap(TDGAME.G.player.aim-Math.PI/2))<.05'))
  fresh('standard');point(175,0);frames(20);pad(12);frames(12);page.evaluate('testPad.axes[2]=-1');pad(4,12);frames(20)
  check('standard right-stick aim remains independent when L and drive are held together',page.evaluate('TDGAME.G.player.cruising && Math.abs(TD.M.wrap(TDGAME.G.player.aim-Math.PI/2))<.05'))

  fresh();targets();point(-170,0);frames(20);pad(7);frames();pad();frames(8)
  r=page.evaluate('({phase:TDGAME.G.player.retina.phase,x:TDGAME.G.player.retina.x,y:TDGAME.G.player.retina.y,scale:TDGAME.G.player.retina.scale,origin:TDGAME.G.player.retina.ox,target:TDGAME.G.player.retina.target?.point().x})');observations['seeker']=r
  check('one R tap launches a travelling, shrinking BOF seeker after release',r['phase']=='seek' and abs(r['x']-r['target'])>1 and 1<r['scale']<2.2)
  page.evaluate("()=>{window.drawn=[];const draw=ART.draw;ART.draw=function(c,k,...args){drawn.push(k);return draw.call(this,c,k,...args)}}");snap('retina_seeking')
  check('actual seeker rendering uses the original retm animation master',page.evaluate('drawn.some(k=>/^retm_[0-3]$/.test(k)) && !drawn.includes("target_retina")'))
  frames(22)
  check('R tap acquires without keeping the shoulder held and without a forward-cone restriction',page.evaluate('TDGAME.G.player.retina.locked && TDGAME.G.player.retina.lockT>4.8'))
  page.evaluate('window.firstTarget=TDGAME.G.player.retina.target.id;drawn=[]');snap('retina_locked')
  check('actual ordinary lock rendering uses BOF retmb animation with Cole neon green',page.evaluate('drawn.some(k=>/^retmb_[0-3]$/.test(k)) && TD.Retina.colors.cole==="#39ff5a"'))
  tap(7);frames(14)
  check('a second R tap cycles to the next visible enemy',page.evaluate('TDGAME.G.player.retina.locked && TDGAME.G.player.retina.target.id!==firstTarget'))
  page.evaluate('TDGAME.G.player.retina.lockT=.06');frames(6)
  check('a released lock expires without an automatic target replacement',page.evaluate('!TDGAME.G.player.retina.target && !TDGAME.G.player.retina.locked'))
  pad(7);frames(34);page.evaluate('TDGAME.G.player.retina.lockT=.02');frames(10)
  check('holding R maintains the lock window',page.evaluate('TDGAME.G.player.retina.locked && TDGAME.G.player.retina.lockT===5'))
  before=page.evaluate('TDGAME.G.player.missiles');pad(7,0);frames()
  check('holding R and A launches a real guided tank missile at the acquired target',page.evaluate('(before)=>TDGAME.G.player.missiles===before-1 && TDGAME.G.shots.some(s=>s.retinaTarget?.id===TDGAME.G.player.retina.target.id)',before))
  pad();frames(12);page.keyboard.down('k');frames();page.keyboard.up('k')
  frames(34);page.keyboard.down('k');frames();page.keyboard.up('k')
  check('the released BOF lock is also usable by the normal cannon binding',page.evaluate('TDGAME.G.player.missiles<5 && TDGAME.G.player.retina.locked'))
  page.evaluate('TDGAME.G.player.retina.target.id.dead=true');frames()
  check('destroying a marked target invalidates its lock',page.evaluate('!TDGAME.G.player.retina.target'))
  fresh();targets();page.evaluate("TD.World.load(800,4000,[[450,2000,480,2250,'b']])");tap(7);frames(15)
  check('solid buildings prevent Retina from selecting a concealed enemy',page.evaluate('TDGAME.G.player.retina.target?.point().x===260'))
  fresh();targets();page.evaluate("TD.Input.setPadBinding('R',11)");tap(11);frames(15)
  check('the remapped R shoulder acquires a live lock',page.evaluate('TDGAME.G.player.retina.locked'))
  check('all seventeen original BOF Retina cells decode with even dimensions',page.evaluate('TD.Retina.warm.length===17 && TD.Retina.warm.every(k=>{const g=ART.get(k);return g&&g.sw%2===0&&g.sh%2===0})'))

  fresh();page.evaluate('TDGAME.G.player.x=400;TDGAME.G.player.y=650');frames(260)
  check('real arena entry still rolls the smaller Warrior into the dossier',page.evaluate('TDGAME.G.bossIntro?.phase==="card" && TDGAME.G.boss.scale===.85'))
  frames(235);snap('card_centered')
  boxes=page.evaluate('TDGAME.G.bossIntro.textLayouts');observations['cardText']=boxes
  check('every dossier text run is fitted and centered inside its assigned frame',len(boxes)>=20 and all(v['width']<=v['box'][2]-3.9 and abs(v['center'][0]-v['box'][0]-v['box'][2]/2)<.01 and abs(v['center'][1]-v['box'][1]-v['box'][3]/2)<.01 for v in boxes))
  check('Continue A/Start prompts remain inside the generated outer card frame',all(v['box'][1]+v['box'][3]<=444 for v in boxes))
  pad(5);frames();pad();frames(18)
  check('printed A selects Continue on the boss dossier exactly as Start does',page.evaluate('TDGAME.G.bossIntro.phase==="slide"'))
  frames(110);page.evaluate("const B=TDGAME.G.boss;B.state='recover';B.cooldown=999;B.a=B.upper=0;B.x=400;B.y=B.homeY;TDGAME.G.units=[];TDGAME.G.player.x=400;TDGAME.G.player.y=635;TDGAME.G.player.vx=TDGAME.G.player.vy=0;TDGAME.G.shots=[];TDGAME.G.eshots=[];TD.Achievements.queue=[];TDGAME.G.msgs=[]");frames(25);snap('warrior_arena_smaller')
  r=page.evaluate('({scale:TDGAME.G.boss.scale,bounds:TDGAME.G.boss.bounds(),cam:{x:TD.Cam.x,y:TD.Cam.y},zoom:TD.Cam.zoom,view:[TD.VW,TD.VH]})');observations['arena']=r
  check('smaller Warrior and escape area use the existing 640x480 view at normal zoom',r['scale']==.85 and r['view']==[640,480] and r['zoom']==1 and r['bounds']['left']>r['cam']['x'] and r['bounds']['right']<r['cam']['x']+640)
  tap(7);frames(15);page.evaluate('drawn=[]');snap('warrior_bof_retina')
  check('boss parts acquire after an R tap and draw the actual BOF boss Retina',page.evaluate('TDGAME.G.player.retina.locked && String(TDGAME.G.player.retina.target.id).startsWith("warrior:") && drawn.includes("nbret_cole")'))
  page.evaluate("const B=TDGAME.G.boss,d=TD.WARRIOR_PARTS.armL;window.mount=B.world(d.x,d.y);window.angle=B.upper;B.damage('armL',999)")
  check('smaller detached arms preserve the scaled mounted sprite, pivot and rotation',page.evaluate('(()=>{const f=TD.FX.list.find(q=>q.k==="fragment"&&q.key==="warrior_arm_l");return f&&Math.abs(f.x-mount.x)<.01&&Math.abs(f.y-mount.y)<.01&&f.a===angle&&f.s===TD.WARRIOR_PARTS.armL.scale*.85})()'))
  go('pilot');page.evaluate("TD.pilot='hotwire';TD.Frontend.pilotAge=8;TD.Frontend.pilotSpin=0");snap('hotwire_text_fitted')
  check('the expansion pilot screen retains two rows of six within its frame',page.evaluate('TD.pilotRects.length===12 && new Set(TD.pilotRects.map(r=>r[1])).size===2 && TD.pilotRects.every(r=>r[0]+r[2]<=640)'))
  go('help');snap('shoulder_help_fitted')
  check('Help shows the restored Retina and shoulder-fire scheme',page.evaluate('TD.Frontend.helpTab===0 && TD.Display.w===640 && TD.Display.h===512'))
  check('browser has no page, console, asset or audio errors',not errors and page.evaluate('!TD.Audio.failures.length'))
  browser.close()
finally:stop()
report={'date':'2026-10-12','build':'overdrive1012-retina-r1','checks':checks,'passed':sum(c['passed'] for c in checks),'failed':sum(not c['passed'] for c in checks),'errors':errors,'observations':observations,'scope':__doc__}
(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:report[k] for k in ['passed','failed','errors']}),flush=True)
sys.exit(0 if not report['failed'] and not errors else 1)
