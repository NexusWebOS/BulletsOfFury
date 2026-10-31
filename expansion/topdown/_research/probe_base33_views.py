"""Native Chromium/rendered-art and real raw-M30 input checks for Escape29."""
from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image
import json,sys,hashlib
R=Path(__file__).resolve().parents[3];sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
from serve_bof_1013 import AssetServer
shoot.http.server.ThreadingHTTPServer=AssetServer
O=R/'_shots/base33';O.mkdir(parents=True,exist_ok=True);checks=[];errors=[];measured={};cancelledMedia=[]
def check(name,v):checks.append({'name':name,'passed':bool(v)});print(('PASS 'if v else'FAIL ')+name,flush=True)
port,stop=shoot.serve(str(R))
try:
 with sync_playwright()as pw:
  browser=pw.chromium.launch();page=browser.new_page(viewport={'width':1280,'height':960});page.on('pageerror',lambda e:errors.append(str(e)));page.on('console',lambda m:errors.append(m.text)if m.type=='error'else None);page.on('response',lambda r:errors.append(f'HTTP {r.status} {r.url}')if r.status>=400 else None)
  page.on('requestfailed',lambda r:(cancelledMedia if r.failure=='net::ERR_ABORTED' and '/audio/'in r.url else errors).append(f'FAILED {r.url} {r.failure}'))
  page.add_init_script("""window.testPad={id:'6B controller (Vendor: 0ca3 Product: 0024)',mapping:'',index:0,connected:true,axes:[0,0],buttons:Array.from({length:12},()=>({pressed:false,value:0}))};Object.defineProperty(navigator,'getGamepads',{value:()=>[testPad]});window.pad=(...ids)=>testPad.buttons.forEach((b,i)=>{b.pressed=ids.includes(i);b.value=+b.pressed;});""")
  page.goto(f'http://127.0.0.1:{port}/expansion/topdown/index.html?fullscreen=0&build=overdrive1015-base33-r1',wait_until='domcontentloaded',timeout=90000);page.wait_for_function('window.TDGAME&&TD.game.state==="boot"',timeout=120000);ev=page.evaluate
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



  check('all72newassetsload',ev('Object.keys(TD_BASE33_ART.assets).length===72&&Object.keys(TD_BASE33_ART.assets).every(k=>ART.get(k))'))
  escape('chute');frames(210);shot('chute')
  escape('corridor');frames(30);shot('base_start')
  for x,name in [(193,'cover'),(790,'slide_passage'),(1190,'crawl_passage'),(1480,'secret_vent'),(3110,'escape_exit')]:
   escape('corridor');ev(f'Object.assign(TD.game.player,{{x:{x},y:TD.Escape29.floorAt({x}),inv:0}});TD.game.escape29.enemies=[];TD.game.escape29.pending=[];');frames(2)
   if name=='cover':ev('pad(5);');frames(8)
   shot(name)
  print('ERRORS',errors,flush=True);browser.close()
finally:stop()
