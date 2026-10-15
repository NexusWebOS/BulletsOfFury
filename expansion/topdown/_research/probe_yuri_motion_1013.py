"""Yuri motion: real Chromium inputs, collision cadence, native pixels and viewer."""
from pathlib import Path
import json,sys
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT/'_BUILD_SOURCE'))
import shoot
OUT=ROOT/'_shots/overdrive_yuri_motion_1013';OUT.mkdir(parents=True,exist_ok=True)
checks=[];errors=[];measurements={}
def check(name,value):
 checks.append({'name':name,'passed':bool(value)});print(('PASS ' if value else 'FAIL ')+name,flush=True)
port,stop=shoot.serve(str(ROOT))
try:
 with sync_playwright() as pw:
  browser=pw.chromium.launch();page=browser.new_page(viewport={'width':1280,'height':960})
  page.on('pageerror',lambda e:errors.append(str(e)));page.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
  page.on('response',lambda r:errors.append(f'HTTP {r.status} {r.url}') if r.status>=400 else None)
  page.add_init_script("window.testPad={id:'Yuri motion standard QA',index:0,connected:true,mapping:'standard',axes:[0,0,0,0],buttons:Array.from({length:24},()=>({pressed:false,value:0}))};Object.defineProperty(navigator,'getGamepads',{value:()=>[testPad]});")
  page.goto(f'http://127.0.0.1:{port}/expansion/topdown/index.html?fullscreen=0&build=overdrive1013-yuri-motion-r1')
  page.wait_for_function('window.TDGAME && TDGAME.G.state==="boot"',timeout=90000);page.evaluate('TDGAME.freeze()')
  page.wait_for_function('Object.keys(TD_YURI_MOTION_ART.assets).every(k=>!!ART.get(k))',timeout=60000)
  page.wait_for_function('document.fonts.check("12px BOFCommand")')
  def ev(s,arg=None):return page.evaluate(s,arg)
  def frames(n=1):
   while n:
    k=min(60,n);ev('n=>TDGAME.step(n)',k);page.wait_for_timeout(1);n-=k
  def release():
   for k in ['w','a','s','d','f','j','r','h','l','Enter']:page.keyboard.up(k)
   page.mouse.up();ev('testPad.axes.fill(0);testPad.buttons.forEach(b=>{b.pressed=false;b.value=0});TD.Input.pointer.active=false');frames()
  def fresh():
   release();ev('TD.pilot="yuri";TD.difficulty="normal";TD.Input.setPadStyle("standard");TDGAME.G.sel=1;TDGAME.start();TD.game.units=[];TD.game.pickups=[];TD.game.player.inv=99999;TD.game.player.x=400;TD.game.player.y=2270;TD.Input.pointer.active=false;TD.Achievements.queue=[]');frames()
  def snap(name):
   ev('TD.game.msgs=[];TD.game.player.inv=0;TDGAME.render()');page.locator('#screen').screenshot(path=str(OUT/(name+'.png')));ev('TD.game.player.inv=99999')
  check('316 authored exports have even 320x320 canvases and one shared pivot',ev('Object.keys(TD_YURI_MOTION_ART.assets).length===316&&Object.values(TD_YURI_MOTION_ART.assets).every(a=>a.size[0]===320&&a.size[1]===320&&a.anchor[0]===160&&a.anchor[1]===256)'))
  check('every walk/run/crawl bank has at least twelve unique authored frames',ev('Object.values(TD_YURI_MOTION_ART.sequences).every(q=>q.frames.length>=12&&new Set(q.frames).size===q.frames.length)'))
  dirs=[('south',['s'],0),('southwest',['s','a'],1),('west',['a'],2),('northwest',['w','a'],3),('north',['w'],4),('northeast',['w','d'],5),('east',['d'],6),('southeast',['s','d'],7)]
  for name,keys,idx in dirs:
   fresh();ev('i=>{const a=i*Math.PI/4,p=TD.game.player;p.x=400;p.y=2270;p.aim=a;p.motionFacing=null;testPad.axes[2]=-Math.sin(a);testPad.axes[3]=Math.cos(a)}',idx)
   for k in keys:page.keyboard.down(k)
   samples=[]
   for _ in range(18):
    frames();samples.append(ev('({pose:TD.footPose(TD.game.player),x:TD.game.player.x,y:TD.game.player.y})'))
   check(name+' walk advances authored poses through real directional input',len(set(s['pose']['key'] for s in samples))>=5 and all(s['pose']['dir']==name and s['pose']['action']=='walk' for s in samples))
  fresh();page.keyboard.down('d');frames(24)
  before=ev('({phase:TD.game.player.gaitPhase,x:TD.game.player.x,pose:TD.footPose(TD.game.player)})')
  page.keyboard.down('j');frames()
  after=ev('({phase:TD.game.player.gaitPhase,x:TD.game.player.x,pose:TD.footPose(TD.game.player)})')
  check('starting fire preserves walking phase and selects matching run-and-gun pose',abs((after['phase']-before['phase'])%1-2.75/96)<1e-6 and after['pose']['action']=='run_fire')
  snap('run_fire');page.keyboard.up('j');frames(10)
  check('releasing fire returns to the walk loop without resetting stride',ev('TD.footPose(TD.game.player).action==="walk"&&Math.abs(TD.game.player.gaitPhase-((35*2.75/96)%1))<1e-6'))
  fresh();page.keyboard.down('f');frames();page.keyboard.up('f');page.keyboard.down('d')
  poses=[]
  for _ in range(60):
   frames();poses.append(ev('TD.footPose(TD.game.player).key'))
  measurements['crawlTransitionsPerSecond']=sum(a!=b for a,b in zip(poses,poses[1:]))
  measurements['crawlDistance']=ev('TD.game.player.x-400')
  check('crawl shows at least fourteen pose changes per second at unchanged 63 px/s',measurements['crawlTransitionsPerSecond']>=14 and abs(measurements['crawlDistance']-63)<1e-6)
  check('crawl remains a low authored pose with no rotated standing billboard',ev('TD.footPose(TD.game.player).action==="crawl"&&TD.footPose(TD.game.player).angle===0'))
  snap('crawl');release();frames(8);rest=ev('TD.footPose(TD.game.player).key');frames(30)
  check('stopping a crawl settles into a planted prone frame',ev('TD.footPose(TD.game.player).key')==rest and ev('!TD.game.player.moving'))
  fresh();ev('TD.game.player.x=355;TD.game.player.y=2103');page.keyboard.down('w');frames(25)
  blocked=ev('({x:TD.game.player.x,y:TD.game.player.y,phase:TD.game.player.gaitPhase,key:TD.footPose(TD.game.player).key})');frames(45)
  check('pushing into a concrete barrier stops the feet after settling',ev('!TD.game.player.moving&&Math.abs(TD.game.player.y-'+str(blocked['y'])+')<.01&&TD.footPose(TD.game.player).key==='+json.dumps(blocked['key'])))
  snap('wall_stop')
  fresh();ev('TD.game.player.gaitPhase=.5;testPad.axes[2]=1;testPad.axes[3]=0');page.keyboard.down('a');frames(5)
  check('backpedaling reverses the gait while keeping independent east aim',ev('TD.footPose(TD.game.player).dir==="east"&&Math.abs(TD.game.player.gaitPhase-(.5-5*2.75/96))<1e-6'))
  fresh();ev('TD.game.player.motionFacing=0;TD.game.player.aim=Math.PI/8+.025')
  check('minor aim jitter near a facing boundary does not flicker the sprite',ev('TD.footPose(TD.game.player).dir==="south"'))
  ev('TD.game.player.aim=Math.PI/8+.1')
  check('deliberate aim change crosses the facing dead band immediately',ev('TD.footPose(TD.game.player).dir==="southwest"'))
  fresh();page.keyboard.down('d');frames(4);page.keyboard.down('Enter');frames();page.keyboard.up('Enter');paused=ev('TD.game.player.gaitPhase');frames(30)
  check('pause freezes movement and animation phase',ev('TD.game.state==="pause"&&TD.game.player.gaitPhase=== '+str(paused)))
  fresh();page.keyboard.down('d');frames(4);page.keyboard.down('r');frames();phase=ev('TD.game.player.gaitPhase');frames(8)
  check('jump holds gait phase and still plays the original jump bank',ev('TD.game.player.gaitPhase=== '+str(phase)+'&&TD.footPose(TD.game.player).action==="jump"'))
  fresh();ev('TD.game.player.gaitPhase=.4;TDGAME.launchBrief()');frames(15);snap('briefing')
  check('normal game render resolves the new Yuri movement art',ev('''(()=>{const old=TD.AssaultArt.draw;let n=0;TD.AssaultArt.draw=function(ctx,k,...args){if(k.startsWith('od_ym_'))n++;return old(ctx,k,...args)};TDGAME.render();TD.AssaultArt.draw=old;return n>0})()'''))
  # Every authored frame through the runtime ART resolver and the actual context
  # drawImage method, followed by pixel inspection of the eight contact sheets.
  ev('const c=document.createElement("canvas");c.id="native-motion";c.width=1280;c.height=720;c.style.cssText="position:absolute;top:0;left:0;width:1280px;height:720px;z-index:9";document.body.append(c)')
  total=0
  for d,_,_ in dirs:
   count=ev('''dir=>{const cv=document.getElementById('native-motion'),c=cv.getContext('2d');c.fillStyle='#17242e';c.fillRect(0,0,1280,720);const old=c.drawImage;let n=0;c.drawImage=function(...args){n++;return old.apply(this,args)};['walk','run_fire','crawl'].forEach((a,j)=>{TD_YURI_MOTION_ART.sequences['yuri_'+dir+'_'+a].frames.forEach((key,i)=>{const x=(i%8)*160,y=(j*2+Math.floor(i/8))*120;TD.AssaultArt.draw(c,key,x+80,y+100,{s:.42});c.fillStyle='#dcebf2';c.font='11px monospace';c.fillText(dir+' '+a+' '+(i+1),x+3,y+114)})});c.drawImage=old;return n}''',d)
   total+=count;page.locator('#native-motion').screenshot(path=str(OUT/('native_'+d+'.png')))
  check('all 316 new frames draw successfully through native ART',total==316)
  page.goto(f'http://127.0.0.1:{port}/expansion/topdown/art/assault_1013/review.html?v=overdrive1013-yuri-motion-r1')
  page.wait_for_function('Object.values(images).every(im=>im.complete&&im.naturalWidth)')
  page.select_option('#action','crawl');page.select_option('#direction','east');page.wait_for_timeout(250);page.screenshot(path=str(OUT/'review_crawl.png'))
  check('review lists every new crawl frame and exposes old/new comparison',page.locator('#strip canvas').count()==12 and page.locator('#compare').is_checked())
  page.click('#pause');page.click('#next');page.select_option('#direction','north')
  check('review dynamically supports sixteen-frame north cycle',page.locator('#strip canvas').count()==16)
  check('no page, console or missing asset errors',not errors)
  browser.close()
finally:stop()
(OUT/'report.json').write_text(json.dumps({'checks':checks,'measurements':measurements,'errors':errors},indent=2),encoding='utf-8')
print(f'SUMMARY {sum(q["passed"] for q in checks)}/{len(checks)} checks; {len(errors)} browser errors',flush=True)
sys.exit(0 if all(q['passed'] for q in checks) and not errors else 1)
