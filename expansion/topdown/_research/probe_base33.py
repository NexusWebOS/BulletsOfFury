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



  check('72authoredpiecesdecode',ev('Object.keys(TD_BASE33_ART.assets).length===72&&Object.keys(TD_BASE33_ART.assets).every(k=>ART.get(k))'))
  escape('chute');frames(210);shot('chute');check('chutedronesstillenterfromceiling',ev('TD.game.escape29.spawned>0&&TD.game.escape29.drones.every(u=>u.drone)'))
  def quiet(x=100):
   escape('corridor');ev(f'TD.game.escape29.pending=[];TD.game.escape29.enemies=[];Object.assign(TD.game.player,{{x:{x},y:TD.Escape29.floorAt({x}),inv:0}});');frames(2)
  quiet(193);ev('pad(5);');frames(8);shot('cover_tucked')
  check('recessselectsauthoredbackcover',ev('TD.game.player.hidden33&&TD.game.player.alcove33&&TD.Escape29.pose(TD.game).startsWith("y32_cover_peek")'))
  ev('(()=>{const e=TD.game.escape29,p=TD.game.player;e.enemyShots.push({x:p.x+55,y:p.y-50,px:p.x+55,py:p.y-50,vx:-340,vy:0,life:2,a:Math.PI/2,kind:"mg"});})()');frames(14)
  check('tuckedpierblocksphysicalbulletwithoutinvulnerability',ev('!TD.game.player.dead&&TD.game.player.inv===0&&TD.game.escape29.enemyShots.length===0'))
  ev('TD.Input.pointer.active=true;TD.Input.pointer.x=600;TD.Input.pointer.y=295;pad(5,2);');frames(25);shot('cover_popout')
  check('leanoutfiresfromexistingYuri32pose',ev('!TD.game.player.hidden33&&TD.game.player.peekExposed&&TD.game.escape29.shotCount>0&&TD.Escape29.pose(TD.game).startsWith("y32_cover_peek")'))
  ev('(()=>{const e=TD.game.escape29,p=TD.game.player;e.enemyShots.push({x:p.x+50,y:p.y-50,px:p.x+50,py:p.y-50,vx:-340,vy:0,life:2,a:Math.PI/2,kind:"mg"});p.fireCd=1;})()');frames(12)
  check('exposedYuriremainsonehit',ev('TD.game.player.dead'))
  quiet(800);ev('testPad.axes=[1,0];');frames(30);shot('slide_gap_block')
  check('standingbodycannotwalkthroughlowpipe',ev('TD.game.player.x<=825.1&&TD.game.player.x>810'))
  ev('testPad.axes=[1,1];pad(3);');frames(1);ev('pad();');frames(24);shot('slide_under_pipe')
  check('realflatgroundslidepassesthepipe',ev('TD.game.player.x>960&&TD.game.player.slide29>0&&!TD.game.player.dead&&TD.game.player.rollCd>4'))
  frames(20);check('slidecooldownremainsfiveseconds',ev('TD.game.player.rollCd>4.1&&TD.game.player.rollCd<4.4'))
  quiet(1200);ev('testPad.axes=[1,0];');frames(12);check('crawlcanopyblocksuprightentry',ev('TD.game.player.x<=1218.1'))
  ev('pad(8,3);');frames(1);ev('pad();');frames(25);shot('crawl_under_duct')
  check('modeXpronecanentercrawlspace',ev('TD.game.player.prone&&TD.game.player.x>1230&&TD.game.player.x<1350'))
  ev('pad(8,3);');frames(1);ev('pad();');frames(1)
  check('cannotstandupinsideoverheadduct',ev('TD.game.player.prone&&!TD.game.player.dead'))
  frames(150);ev('testPad.axes=[0,0];pad(8,3);');frames(1);ev('pad();');frames(1)
  check('canstandafterleavingcrawlspace',ev('TD.game.player.x>1382&&!TD.game.player.prone'))
  quiet(1490);ev('TD.Input.pointer.active=true;TD.Input.pointer.x=1540-TD.game.escape29.camX;TD.Input.pointer.y=385;pad(2,4);');frames(1);ev('pad(4);');frames(6);shot('vent_damaged')
  check('ventregisterssweptphysicalprojectiledamage',ev('TD.game.escape29.secrets33[0].hp<6&&TD.game.escape29.secrets33[0].hp>0'))
  ev('pad(2,4);');frames(22);ev('pad();');frames(1);shot('vent_open')
  check('ventopensafterthreeassaultbullets',ev('TD.game.escape29.secrets33[0].open'))
  ev('TD.Input.pointer.active=false;testPad.axes=[1,0];pad(8,3);');frames(1);ev('pad();');frames(50);shot('vent_cache_claim')
  check('crawlingintoventgrantsspreadgunandgrenades',ev('TD.game.escape29.secrets33[0].claimed&&TD.game.player.weapons[TD.game.player.wi].id==="spread_shotgun"&&TD.game.score>=2000'))
  count=ev('({score:TD.game.score,ammo:TD.game.player.weapons[TD.game.player.wi].ammo,grenades:TD.game.player.smoke})');frames(20)
  check('secretrewardcannotbefarmed',count==ev('({score:TD.game.score,ammo:TD.game.player.weapons[TD.game.player.wi].ammo,grenades:TD.game.player.smoke})'))
  ev('testPad.axes=[0,0];TD.Input.pointer.active=true;TD.Input.pointer.x=600;TD.Input.pointer.y=340;pad(2);');frames(1)
  check('secretshotgunactuallyfiresfiveprojectiles',ev('TD.game.escape29.shots.length>=5'))
  pack=json.loads((R/'expansion/topdown/art/base33/manifest.json').read_text(encoding='utf-8'))
  check('allevenexportdimensionsandvalidanchors',all(Image.open(R/m['file']).size==tuple(m['size'])and not(m['size'][0]%2 or m['size'][1]%2)and Image.open(R/m['file']).getbbox()for m in pack['assets'].values()))
  check('effectbanksusefixedgeometry',all(len({tuple(pack['assets'][k]['size'])for k in q['frames']})==1 and len({tuple(pack['assets'][k]['anchor'])for k in q['frames']})==1 for q in pack['sequences'].values()))
  check('820originalartfilespreserved',all(hashlib.sha256((R/k).read_bytes()).hexdigest()==v for k,v in json.loads((R/'_shots/lighting22/retained_art.json').read_text()).items()))
  check('nobrowsererrors',not errors)
  report={'build':'overdrive1015-base33-r1','checks':checks,'passed':sum(x['passed']for x in checks),'failed':sum(not x['passed']for x in checks),'errors':errors,'scope':'Native renderer, actual asset draws, raw-M30 ordinary controls in scoped fixtures. Incoming bullet fixtures use live swept collision and damage. No physical controller test.'}
  (O/'report.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps(report),flush=True);browser.close()
finally:stop()
sys.exit(0 if not report['failed']and not errors else 1)
