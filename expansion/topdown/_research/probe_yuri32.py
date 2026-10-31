"""Native Chromium/rendered-art and real raw-M30 input checks for Escape29."""
from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image
import json,sys,hashlib
R=Path(__file__).resolve().parents[3];sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
from serve_bof_1013 import AssetServer
shoot.http.server.ThreadingHTTPServer=AssetServer
O=R/'_shots/yuri32';O.mkdir(parents=True,exist_ok=True);checks=[];errors=[];measured={};cancelledMedia=[]
def check(name,v):checks.append({'name':name,'passed':bool(v)});print(('PASS 'if v else'FAIL ')+name,flush=True)
port,stop=shoot.serve(str(R))
try:
 with sync_playwright()as pw:
  browser=pw.chromium.launch();page=browser.new_page(viewport={'width':1280,'height':960});page.on('pageerror',lambda e:errors.append(str(e)));page.on('console',lambda m:errors.append(m.text)if m.type=='error'else None);page.on('response',lambda r:errors.append(f'HTTP {r.status} {r.url}')if r.status>=400 else None)
  page.on('requestfailed',lambda r:(cancelledMedia if r.failure=='net::ERR_ABORTED' and '/audio/'in r.url else errors).append(f'FAILED {r.url} {r.failure}'))
  page.add_init_script("""window.testPad={id:'6B controller (Vendor: 0ca3 Product: 0024)',mapping:'',index:0,connected:true,axes:[0,0],buttons:Array.from({length:12},()=>({pressed:false,value:0}))};Object.defineProperty(navigator,'getGamepads',{value:()=>[testPad]});window.pad=(...ids)=>testPad.buttons.forEach((b,i)=>{b.pressed=ids.includes(i);b.value=+b.pressed;});""")
  page.goto(f'http://127.0.0.1:{port}/expansion/topdown/index.html?fullscreen=0&build=overdrive1015-yuri32-r1',wait_until='domcontentloaded',timeout=90000);page.wait_for_function('window.TDGAME&&TD.game.state==="boot"',timeout=120000);ev=page.evaluate
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



  check('all215framesload',ev('Object.keys(TD_YURI32_ART.assets).length===215&&Object.keys(TD_YURI32_ART.assets).every(k=>ART.get(k))'))
  escape('corridor');ev('TD.game.escape29.enemies=[];TD.game.escape29.pending=[];TD.game.player.inv=0;TD.Input.pointer.active=true;TD.Input.pointer.x=TD.game.player.x;TD.Input.pointer.y=150;pad(4);');frames(1)
  check('uprightfrontupstance',ev('TD.Escape29.pose(TD.game)==="y32_up_idle"'));shot('standing_up')
  ev('pad(4,2);');frames(1)
  check('upwardfireusesnewrecoil',ev('TD.Escape29.pose(TD.game).startsWith("y32_up_fire")'))
  check('upwardprojectilesstartatraisedbarrel',ev('(()=>{const p=TD.game.player,s=TD.game.escape29.shots.at(-1),q=TD.Escape29.socket(TD.game);return s&&Math.hypot(s.px-q.x,s.py-q.y)<.01&&s.vy<0&&q.y<p.y-100;})()'));shot('up_fire')
  for name in ['walk','run']:
   escape('corridor');ev('TD.game.escape29.enemies=[];TD.game.escape29.pending=[];TD.game.player.inv=0;')
   if name=='run':ev('testPad.axes=[1,0];');frames(3)
   ev('testPad.axes=[1,1];pad(3);');frames(1);ev('pad();');seen=[]
   for i in range(41):
    state=ev('({key:TD.Escape29.pose(TD.game),y:TD.game.player.y,x:TD.game.player.x,remaining:TD.game.player.slide29,bank:TD.game.player.slideEntry32})');seen.append(state)
    if i in [0,8,18,27,36]:shot(name+'_slide_'+str(i))
    frames(1)
   measured[name+'Slide']=seen
   check(name+'entryselected',seen[0]['bank']==name and seen[0]['key'].startswith('y32_'+name+'_slide'))
   check(name+'slideholdsandrecovers',any(v['key'].startswith('y32_slide_hold')for v in seen)and any(v['key'].startswith('y32_slide_exit')for v in seen)and seen[-1]['remaining']==0)
   check(name+'slideisflat',all(abs(v['y']-350)<.01 for v in seen))
  escape('corridor');ev('TD.game.escape29.pending=[];TD.game.escape29.enemies=[];Object.assign(TD.game.player,{x:473,y:350,inv:0});TD.Input.pointer.active=true;TD.Input.pointer.x=600;TD.Input.pointer.y=292;testPad.axes=[0,1];pad();');frames(2)
  check('backcoverusescrouchedobjectfreepose',ev('!!TD.game.player.sideCover29&&TD.Escape29.pose(TD.game)==="y32_crouch_peek_east_0"'));shot('back_cover_low')
  ev('pad(2);');seen=[]
  for i in range(18):frames(1);seen.append(ev('TD.Escape29.pose(TD.game)'))
  measured['popout']=seen;check('partialpopoutusesintermediateposes',len(set(seen))>=10 and seen[-1].startswith('y32_crouch_peek_east'));shot('back_cover_peek')
  ev('pad();');seen=[]
  for i in range(12):frames(1);seen.append(ev('TD.Escape29.pose(TD.game)'))
  check('returntucksthroughsameauthoredposes',len(set(seen))>=7 and seen[-1]=='y32_crouch_peek_east_0');shot('back_cover_return')
  ev('TD.game.player.sideCover29.h=100;');frames(1);check('tallbackcoverusesstandingpose',ev('TD.Escape29.pose(TD.game)==="y32_cover_peek_east_0"'));shot('back_cover_tall');ev('pad(2);');frames(18);shot('back_cover_tall_peek')
  escape('corridor');ev('TD.game.escape29.pending=[];TD.game.escape29.enemies=[];Object.assign(TD.game.player,{x:387,y:350,inv:0});testPad.axes=[1,1];');frames(2);check('forwardobjectkeepscompatiblefrontcover',ev('!!TD.game.player.sideCover29&&!TD.Escape29.pose(TD.game).startsWith("y32_")'))
  retained=json.loads((R/'expansion/topdown/art/yuri32/source/retained.json').read_text(encoding='utf-8'));check('priorgameplayandYuri31filespreserved',all(hashlib.sha256((R/k).read_bytes()).hexdigest()==v for k,v in retained.items()))
  check('820retainedartunchanged',all(hashlib.sha256((R/k).read_bytes()).hexdigest()==v for k,v in json.loads((R/'_shots/lighting22/retained_art.json').read_text()).items()))
  pack=json.loads((R/'expansion/topdown/art/yuri32/manifest.json').read_text(encoding='utf-8'));valid=True
  for k,m in pack['assets'].items():
   im=Image.open(R/m['file']).convert('RGBA');b=im.getbbox();valid &= im.size==(192,224)and set(im.getchannel('A').get_flattened_data())=={0,255}and min(b[:2])>0 and b[2]<192 and b[3]<224
  check('uniformcellsbinaryalphaandunclippedbounds',valid)
  page.goto(f'http://127.0.0.1:{port}/expansion/topdown/art/yuri32/preview.html',wait_until='domcontentloaded');page.wait_for_function('document.getElementById("status").textContent.startsWith("Playing")',timeout=60000)
  for bank,n in [('up_fire',3),('walk_slide',8),('run_slide',12),('slide_exit',5),('cover_enter',9),('cover_crouch',8),('cover_peek',7),('cover_return',10),('crouch_peek',8),('crouch_return',10)]:
   page.select_option('#bank',bank);ev(f'paused=true;frame={n};document.getElementById("onion").checked=true;paint();');page.locator('#review').screenshot(path=str(O/('onion_'+bank+'.png')))
   ev('document.getElementById("onion").checked=false;paint()');page.locator('#review').screenshot(path=str(O/('review_'+bank+'.png')))
  check('reviewloadsallnewframes',ev('Object.keys(images).length===215'))
  check('nobrowsererrors',not errors)
  report={'build':'overdrive1015-yuri32-r1','checks':checks,'passed':sum(c['passed']for c in checks),'failed':sum(not c['passed']for c in checks),'errors':errors,'measured':measured,'scope':'Native Chromium, actual asset draws, simulated M30 plus pointer aiming; scoped upfire/flat-slide/cover checks. No physical-controller test.'};(O/'report.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps({'passed':report['passed'],'failed':report['failed'],'errors':errors}));browser.close()
finally:stop()
sys.exit(0 if not report['failed']and not errors else 1)
