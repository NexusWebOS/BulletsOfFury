"""Native Chromium/rendered-art and real raw-M30 input checks for Escape29."""
from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image
import json,sys,hashlib
R=Path(__file__).resolve().parents[3];sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
from serve_bof_1013 import AssetServer
shoot.http.server.ThreadingHTTPServer=AssetServer
O=R/'_shots/yuri30';O.mkdir(parents=True,exist_ok=True);checks=[];errors=[];measured={};cancelledMedia=[]
def check(name,v):checks.append({'name':name,'passed':bool(v)});print(('PASS 'if v else'FAIL ')+name,flush=True)
port,stop=shoot.serve(str(R))
try:
 with sync_playwright()as pw:
  browser=pw.chromium.launch();page=browser.new_page(viewport={'width':1280,'height':960});page.on('pageerror',lambda e:errors.append(str(e)));page.on('console',lambda m:errors.append(m.text)if m.type=='error'else None);page.on('response',lambda r:errors.append(f'HTTP {r.status} {r.url}')if r.status>=400 else None)
  page.on('requestfailed',lambda r:(cancelledMedia if r.failure=='net::ERR_ABORTED' and '/audio/'in r.url else errors).append(f'FAILED {r.url} {r.failure}'))
  page.add_init_script("""window.testPad={id:'6B controller (Vendor: 0ca3 Product: 0024)',mapping:'',index:0,connected:true,axes:[0,0],buttons:Array.from({length:12},()=>({pressed:false,value:0}))};Object.defineProperty(navigator,'getGamepads',{value:()=>[testPad]});window.pad=(...ids)=>testPad.buttons.forEach((b,i)=>{b.pressed=ids.includes(i);b.value=+b.pressed;});""")
  page.goto(f'http://127.0.0.1:{port}/expansion/topdown/index.html?fullscreen=0&build=overdrive1015-yuri30-r1',wait_until='domcontentloaded',timeout=90000);page.wait_for_function('window.TDGAME&&TD.game.state==="boot"',timeout=120000);ev=page.evaluate
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

  check('all213identity frames decoded by native ART',ev('Object.keys(TD_YURI30_ART.assets).length===213&&Object.keys(TD_YURI30_ART.assets).every(k=>!!ART.get(k))'))
  check('runtime owner uses corrected files',ev('Object.entries(TD_YURI30_ART.assets).every(([k,m])=>TD_ESCAPE29_ART.assets[k].file===m.file&&TD_ASSAULT_ART.assets[k].file===m.file)'))
  check('all frame cells and scale retained',ev('Object.values(TD_YURI30_ART.assets).every(m=>m.size.join()===\"192,224\"&&m.anchor.join()===\"96,160\"&&m.drawScale===1)'))
  old=json.loads((R/'expansion/topdown/art/escape29/manifest.json').read_text());new=json.loads((R/'expansion/topdown/art/yuri30/manifest.json').read_text())
  check('action sequences and timing unchanged',old['sequences']==new['sequences'])
  check('all gun sockets preserved',all(m.get('muzzle')==old['assets'][k].get('muzzle')for k,m in new['assets'].items()))
  check('new files contain corrected pixels',all(hashlib.sha256((R/m['file']).read_bytes()).digest()!=hashlib.sha256((R/old['assets'][k]['file']).read_bytes()).digest()for k,m in new['assets'].items()))
  check('original assets and gameplay files unchanged',all(hashlib.sha256((R/k).read_bytes()).hexdigest()==v for k,v in json.loads((O/'before_hashes.json').read_text()).items()))
  check('820 retained graphics still unchanged',all(hashlib.sha256((R/k).read_bytes()).hexdigest()==v for k,v in json.loads((R/'_shots/lighting22/retained_art.json').read_text()).items()))
  fresh();ev('TD.game.units=[];TD.game.fortress.pending=[];TD.game.player.aim=Math.PI/2;TD.game.player.firing=.1;TDGAME.render();');shot('corrected_topdown')
  check('standing sideways uses corrected Yuri',ev('TD.footPose(TD.game.player).key.startsWith("e29_aim")'))
  escape('corridor');ev('TD.game.escape29.pending=[];Object.assign(TD.game.player,{x:270,y:350,inv:999});testPad.axes=[1,0];pad(2);');frames(18);shot('corrected_run')
  check('running selects corrected motion bank',ev('TD.Escape29.pose(TD.game).startsWith("e29_run")'))
  ev('pad(3);');frames(8);shot('corrected_roll');check('rolling selects corrected motion bank',ev('TD.Escape29.pose(TD.game).startsWith("e29_roll")'))
  escape('corridor');ev('TD.game.escape29.pending=[];Object.assign(TD.game.player,{x:370,y:350});testPad.axes=[1,0];pad(1);');frames(18);shot('corrected_vault');check('vault selects corrected motion bank',ev('TD.Escape29.pose(TD.game).startsWith("e29_vault")'))
  escape('chute');frames(80);ev('TD.game.escape29.cursor={x:110,y:150};TD.game.player.aim=TD.M.angTo(285,310,110,150);');shot('corrected_reverse_slide');check('reverse slide has corrected authored sprite',ev('TD.Escape29.pose(TD.game)==="e29_slide_back"'))
  # Whole images drawn through the actual in-game ART/AssaultArt renderer.
  ev("""(()=>{const c=document.createElement('canvas');c.id='identityReview';c.style.cssText='position:fixed;left:0;top:0;width:1200px;height:460px;z-index:999;image-rendering:pixelated';c.width=1200;c.height=460;document.body.appendChild(c);const ctx=c.getContext('2d');ctx.imageSmoothingEnabled=false;ctx.fillStyle='#172631';ctx.fillRect(0,0,c.width,c.height);[['y28_west_setup','Established Yuri'],['e29_aim_west_6','Corrected aim'],['e29_run_west_6','Corrected run'],['e29_slide_back','Corrected slide']].forEach(([k,label],i)=>{TD.AssaultArt.draw(ctx,k,120+i*300,365,{s:3});ctx.fillStyle='#e6f2fc';ctx.font='18px monospace';ctx.fillText(label,25+i*300,410);});})()""")
  page.locator('#identityReview').screenshot(path=str(O/'identity_comparison.png'))
  ev('document.getElementById("identityReview").remove()')
  page.goto(f'http://127.0.0.1:{port}/expansion/topdown/art/yuri30/preview.html',wait_until='domcontentloaded');page.wait_for_function('document.getElementById("status").textContent.startsWith("Playing")',timeout=60000)
  for bank in ['aim','run','vault','roll','crouch','prone','cover_peek','slide_motion','slide_aim']:
   page.select_option('#bank',bank);ev('paused=true;frame=5;document.getElementById("onion").checked=true;paint();');page.locator('#review').screenshot(path=str(O/('onion_'+bank+'.png')))
  check('all corrected frames load in review',ev('Object.keys(images).length===213'))
  check('no browser errors or missing images',not errors)
  report={'build':'overdrive1015-yuri30-r1','checks':checks,'passed':sum(c['passed']for c in checks),'failed':sum(not c['passed']for c in checks),'errors':errors,'scope':'Identity/art correction. Existing movement controls exercised with synthetic M30 input; native renderer and onion views inspected. No physical-controller test or gameplay rebalance.'};(O/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({'passed':report['passed'],'failed':report['failed'],'errors':errors}));browser.close()
finally:stop()
sys.exit(0 if not report['failed']and not errors else 1)
