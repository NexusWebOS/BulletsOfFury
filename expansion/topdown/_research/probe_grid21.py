from pathlib import Path
import sys,json,time
from playwright.sync_api import sync_playwright
ROOT=Path(r'C:\Users\Mike\Desktop\Github Coding\BulletsOfFury');sys.path.insert(0,str(ROOT/'_BUILD_SOURCE'));import shoot;from serve_bof_1013 import AssetServer;shoot.http.server.ThreadingHTTPServer=AssetServer
OUT=ROOT/'_shots/grid21';OUT.mkdir(parents=True,exist_ok=True);errors=[];checks=[]
def check(name,v):checks.append({'name':name,'passed':bool(v)});print(('PASS ' if v else 'FAIL ')+name,flush=True)
port,stop=shoot.serve(str(ROOT))
try:
 with sync_playwright() as pw:
  b=pw.chromium.launch();p=b.new_page(viewport={'width':1280,'height':960});p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text) if m.type=='error' else None);p.on('response',lambda r:errors.append(f'HTTP {r.status} {r.url}') if r.status>=400 else None)
  p.goto(f'http://127.0.0.1:{port}/expansion/topdown/index.html?fullscreen=0&build=overdrive1014-grid21-r1',wait_until='domcontentloaded',timeout=90000);p.wait_for_function('window.TDGAME&&TD.game.state==="boot"',timeout=90000)
  p.evaluate('TDGAME.freeze();TD.pilot="yuri";TD.difficulty="normal";TD.game.sel=TD.MISSIONS.findIndex(m=>m.id===7);TDGAME.start();TD.Achievements.queue=[];')
  for i in range(3):p.evaluate('TDGAME.step(60)');p.wait_for_timeout(1)
  p.evaluate('TDGAME.render()');p.locator('#screen').screenshot(path=str(OUT/'corridor.png'))
  check('actual Three.js WebGL2 renderer initialized',p.evaluate('!!TD.Grid21.renderer&&TD.Grid21.renderer.getContext() instanceof WebGL2RenderingContext&&!TD.Grid21.error'))
  check('independent tiled corridor has over 200 grid cells',p.evaluate('TD.Grid21.stats.gridCells>200&&TD.Grid21.scene.children.length>=7'))
  check('native 640x480 output no antialiasing or pixel-ratio inflation',p.evaluate('TD.Grid21.renderer.domElement.width===640&&TD.Grid21.renderer.domElement.height===480&&TD.Grid21.renderer.getPixelRatio()===1&&!TD.Grid21.renderer.getContext().getContextAttributes().antialias'))
  check('every live texture uses nearest sampling without mipmaps',p.evaluate('[...TD.Grid21.textures.values()].every(t=>t.magFilter===THREE.NearestFilter&&t.minFilter===THREE.NearestFilter&&!t.generateMipmaps&&t.anisotropy===1)'))
  check('player and enemy art are real individually textured flats',p.evaluate('TD.Grid21.stats.flatDraws>20&&TD.Grid21.pool.length>=6&&TD.Grid21.pool.some(m=>m.material.uniforms.image.value.image.width>=100)'))
  check('perspective corridor and independent cover layers both render',p.evaluate('TD.Grid21.stats.environmentDraws>=6&&TD.Grid21.coverPool.length===4'))
  p.evaluate('TD.Input.state={prone:true};TD.Input.last={};TD.Input.update=function(){this.last=this.state;this.state={prone:true};};TD.game.player.prone=true;TD.game.player.stance="prone";TD.game.player.rise=0;TD.game.player.inv=0;TDGAME.render()');p.locator('#screen').screenshot(path=str(OUT/'wall_prone.png'))
  p.evaluate('TD.Input.update=function(){this.last=this.state;this.state={};};TD.Bastion.beginBreach(TD.game);');
  for phase,n in [('hop',75),('walk_early',55),('walk_late',42),('next_room',120)]:
   for i in range(0,n,30):p.evaluate(f'TDGAME.step({min(30,n-i)})');p.wait_for_timeout(1)
   p.evaluate('TDGAME.render()');p.locator('#screen').screenshot(path=str(OUT/f'{phase}.png'))
   print(phase,p.evaluate('({phase:TD.game.bastion.transition?.phase,z:TD.Grid21.stats.cameraZ,wave:TD.game.bastion.totalWave})'),flush=True)
  check('traversal returns to fixed combat camera in next room',p.evaluate('TD.game.bastion.totalWave===2&&TD.Grid21.stats.cameraZ===4&&TD.Cam.zoom===1'))
  p.evaluate('TD.Bastion.startBoss(TD.game);TD.game.player.prone=false;TD.game.player.rise=1;TD.game.player.inv=0;TDGAME.render()');p.locator('#screen').screenshot(path=str(OUT/'reactor.png'))
  check('room eight uses separate generated glass reactor',p.evaluate('TD.Bastion.masterPose(TD.game.boss).startsWith("grid21_reactor_")'))
  p.evaluate('Object.assign(TD.game.boss,{name:"HELIOS / PRISM ENTITY",form:"helios",state:"run",hp:360,max:360,y:320,x:420,toX:735,fromX:190,gait:0.25});TD.game.msgs=[];TDGAME.render()');p.locator('#screen').screenshot(path=str(OUT/'helios.png'))
  check('Helios retains previous authored run bank',p.evaluate('TD.Bastion.heliosPose(TD.game.boss).key.startsWith("pb20_helios_run")'))
  pixels=p.evaluate('''() => {const reports=[];const a=document.createElement('canvas'),b=document.createElement('canvas');a.width=b.width=640;a.height=b.height=480;const ac=a.getContext('2d'),bc=b.getContext('2d');ac.imageSmoothingEnabled=bc.imageSmoothingEnabled=false;
   for(const key of [...Object.keys(TD_GRID21_ART.assets),TD.Bastion.playerPose(TD.game),TD.Bastion.heliosPose(TD.game.boss).key]){const m=TD_ASSAULT_ART.assets[key];ac.clearRect(0,0,640,480);bc.clearRect(0,0,640,480);TD.Grid21.begin(ac,TD.game);TD.Grid21.renderer.setClearColor(0,0);TD.Grid21.renderer.clear();TD.Grid21.flat(ac,key,320,240,1,{});TD.Grid21.end(ac);TD.AssaultArt.draw(bc,key,320,240,{s:1});const aa=ac.getImageData(0,0,640,480).data,bb=bc.getImageData(0,0,640,480).data;let opaque=0,max=0,bad=0;for(let i=0;i<aa.length;i+=4){if(aa[i+3]===255&&bb[i+3]===255){opaque++;for(let j=0;j<3;j++)max=Math.max(max,Math.abs(aa[i+j]-bb[i+j]));}if(aa[i+3]!==bb[i+3])bad++;}reports.push({key,opaque,maxChannelDifference:max,alphaMismatches:bad});}return reports;}''')
  check('all new assets and retained actors match native pixels through Three.js flats',all(q['opaque']>0 and q['maxChannelDifference']<=1 and q['alphaMismatches']==0 for q in pixels))
  (OUT/'pixel_comparison.json').write_text(json.dumps(pixels,indent=2),encoding='utf-8')
  p.evaluate('TDGAME.render()');perf=p.evaluate('''async()=>{const samples=[];for(let i=0;i<10;i++){const t=performance.now();for(let j=0;j<6;j++)TDGAME.render();await new Promise(r=>requestAnimationFrame(r));samples.push((performance.now()-t)/6);}return samples;}''');print('RENDER_MS',perf,flush=True)
  (OUT/'render_timing.json').write_text(json.dumps({'batchFrameMilliseconds':perf,'scope':'Real Chromium, headless GPU software/hardware dependent; six-frame batches, actual game renderer including canvas composite.'},indent=2),encoding='utf-8')
  result={'checks':checks,'errors':errors,'stats':p.evaluate('TD.Grid21.stats'),'scope':'Native Chromium rendering; dedicated isolated scene/transition fixtures. Full Normal input-only route tested separately.'};(OUT/'visual.json').write_text(json.dumps(result,indent=2),encoding='utf-8');print(json.dumps(result,indent=2));b.close()
finally:stop()
sys.exit(0 if all(c['passed'] for c in checks) and not errors else 1)
