from pathlib import Path
import sys,json,hashlib
from PIL import Image,ImageStat
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT/'_BUILD_SOURCE'));import shoot
from serve_bof_1013 import AssetServer
shoot.http.server.ThreadingHTTPServer=AssetServer
OUT=ROOT/'_shots/cover24';OUT.mkdir(parents=True,exist_ok=True);checks=[];errors=[];metrics={}
def check(name,value):checks.append({'name':name,'passed':bool(value)});print(('PASS ' if value else 'FAIL ')+name,flush=True)
port,stop=shoot.serve(str(ROOT))
try:
 with sync_playwright() as pw:
  browser=pw.chromium.launch();p=browser.new_page(viewport={'width':1280,'height':960});p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text) if m.type=='error' else None);p.on('response',lambda r:errors.append(f'HTTP {r.status} {r.url}') if r.status>=400 else None)
  p.goto(f'http://127.0.0.1:{port}/expansion/topdown/index.html?fullscreen=0&build=overdrive1014-cover24-r1',wait_until='domcontentloaded',timeout=90000);p.wait_for_function('window.TDGAME&&TD.game.state==="boot"',timeout=90000);ev=p.evaluate
  ev('TDGAME.freeze();TD.pilot="yuri";TD.difficulty="normal";TD.game.sel=TD.MISSIONS.findIndex(m=>m.id===7);TDGAME.start();TD.Achievements.queue=[];')
  def frames(n):
   while n:
    k=min(40,n);ev(f'TDGAME.step({k})');p.wait_for_timeout(1);n-=k
  def shot(name):
   ev('TD.game.player.inv=0;TDGAME.render()');p.locator('#screen').screenshot(path=str(OUT/(name+'.png')))
  frames(180)
  ev('ART.warm([...Object.keys(TD_GRID21_ART.assets),...Object.keys(TD_BASTION19_ART.assets),...Object.keys(TD_BASTION20_ART.assets)]);')
  p.wait_for_function('ART.progress([...Object.keys(TD_GRID21_ART.assets),...Object.keys(TD_BASTION19_ART.assets),...Object.keys(TD_BASTION20_ART.assets)])===1',timeout=90000)
  ev('TD.game.units=[];TD.game.bastion.enemyCover=[];TD.game.bastion.barrels=[];TD.game.bastion.enemyShots=[];TD.FX.list=[];TD.game.msgs=[];TD.game.player.inv=0;')
  check('level 7 enters intact cover automatically without a held button',ev('TD.game.player.rise===0&&TD.game.player.stance==="crouch"&&TD.Bastion.playerCoverOffset(TD.game)===0'))
  shot('idle_behind_wall')
  check('solid front faces use authored cover art without duplicate low decals',ev('TD.Grid21.lighting.boxes.every(b=>b.visible&&b.material[4].map)&&TD.Grid21.coverPool.every(m=>!m.visible)'))
  check('wall is one aligned 3D body with a thin visible cap',ev('TD.Grid21.lighting.boxes.every(b=>Math.abs(b.scale.z-.10)<.00001&&b.scale.y<1.3&&b.userData.screenTop===336)'))
  check('wall is physically between Yuri and the enemy doorway',ev('TD.Grid21.lighting.coverZ<TD.Grid21.lighting.floorPoint(TD.game.player.x,448).z&&TD.Grid21.lighting.coverZ>-18'))
  check('texture filtering stays crisp without mipmaps or antialiasing',ev('[...TD.Grid21.textures.values()].every(t=>t.magFilter===THREE.NearestFilter&&!t.generateMipmaps)&&!TD.Grid21.renderer.getContext().getContextAttributes().antialias'))
  # Compare the same native render with and without Yuri, keeping lights/shadows fixed.
  ev('''window.cover24Pixels=()=>{const cv=document.createElement('canvas');cv.width=640;cv.height=480;const ctx=cv.getContext('2d');ctx.imageSmoothingEnabled=false;ctx.drawImage(document.querySelector('#screen'),0,0,640,480);return ctx.getImageData(0,0,640,480).data;};
   window.cover24Diff=(y0,y1,withoutWall=false)=>{const grid=TD.Grid21,flat=grid.flat,cover=grid.cover;if(withoutWall)grid.cover=()=>true;TDGAME.render();const a=cover24Pixels();grid.flat=function(ctx,key,...args){return key?.includes('yuri')?true:flat.call(this,ctx,key,...args);};TDGAME.render();const b=cover24Pixels();grid.flat=flat;grid.cover=cover;TDGAME.render();let count=0;for(let y=y0;y<y1;y++)for(let x=250;x<390;x++){const i=(y*640+x)*4;if(Math.abs(a[i]-b[i])+Math.abs(a[i+1]-b[i+1])+Math.abs(a[i+2]-b[i+2])>9)count++;}return count;};void 0;''')
  metrics['idleVisiblePixels']=ev('cover24Diff(300,450)');metrics['idleWithoutWallPixels']=ev('cover24Diff(300,450,true)')
  check('idle crouch is visible on the camera side of the wall',metrics['idleVisiblePixels']>500)
  check('crouched head stays below the wall lip from the enemy side',ev('(()=>{const m=TD_ASSAULT_ART.assets[TD.Bastion.playerPose(TD.game)];return TD.game.player.y+TD.Bastion.playerCoverOffset(TD.game)+(m.bounds[1]-m.anchor[1])*1.3>336;})()'))
  baseline=Image.open(OUT/'before.png').resize((640,480),Image.Resampling.NEAREST).convert('RGB');current=Image.open(OUT/'idle_behind_wall.png').resize((640,480),Image.Resampling.NEAREST).convert('RGB')
  def luma(image,box):
   rgb=ImageStat.Stat(image.crop(box)).mean;return .2126*rgb[0]+.7152*rgb[1]+.0722*rgb[2]
  metrics['luminance']={}
  for name,box in [('leftWall',(25,95,155,235)),('rightWall',(490,95,620,235)),('floor',(110,278,530,350))]:
   a,b=luma(baseline,box),luma(current,box);metrics['luminance'][name]={'before':a,'after':b,'ratio':b/a};check(name+' details are brighter while retaining dark contrast',b>a*1.35 and b<110)
  p.keyboard.down('j');frames(3);shot('rising_to_fire');frames(7)
  check('Fire raises Yuri and emits projectiles within 10 frames',ev('TD.game.player.rise>.94&&TD.game.bastion.bullets.length>0'))
  metrics['firingBodyBelowLip']=ev('cover24Diff(378,445)');metrics['firingBodyAboveLip']=ev('cover24Diff(320,373)')
  check('firing raises Yuri above the wall without hiding his camera-side legs',metrics['firingBodyBelowLip']>50 and metrics['firingBodyAboveLip']>30 and ev('TD.Bastion.playerSocket(TD.game).y<336'))
  shot('firing_behind_wall');p.keyboard.up('j');frames(20)
  check('release Fire returns Yuri to cover',ev('TD.game.player.rise===0&&TD.game.player.stance==="crouch"'))
  count=ev('TD.game.bastion.gunShots.rifle||0');p.keyboard.press('j');frames(10)
  check('a quick Fire tap is buffered through the rise and fires once',ev('TD.game.bastion.gunShots.rifle')==count+1);frames(20)
  check('wall blocks an incoming bullet while Yuri rests on our side',ev('(()=>{const G=TD.game,hp=G.player.hp,stops=G.bastion.coverStops;TD.Bastion.resolveEnemyShot(G,{kind:"mg",tx:G.player.x,damage:1,near:false});return G.player.hp===hp&&G.bastion.coverStops===stops+1;})()'))
  p.keyboard.down('d');frames(12);p.keyboard.up('d');frames(1)
  check('covered sidesteps move Yuri while keeping the lowered wall pose',ev('TD.game.player.x>330&&TD.game.player.rise===0&&TD.Bastion.playerPose(TD.game).startsWith("pb20_yuri_wall_crouch")'))
  p.keyboard.press('f');frames(30);shot('prone_behind_wall')
  check('prone and crawl remain visible on our side of intact cover',ev('TD.game.player.prone&&TD.game.player.rise===0') and ev('cover24Diff(300,450)')>50)
  p.keyboard.press('f');frames(30);p.keyboard.down('c');p.keyboard.down('j');frames(12);shot('blindfire_behind_wall')
  check('Cover + Fire retains blindfire projectiles above the wall',ev('TD.game.player.blindfire&&TD.game.bastion.bullets.length>0&&TD.Bastion.playerSocket(TD.game).y<336'))
  check('blindfire body stays visible on the camera side',ev('cover24Diff(378,445)')>30)
  p.keyboard.up('j');p.keyboard.up('c');frames(20);p.keyboard.down('i');frames(20);shot('freeaim_peek');check('Retina still raises Yuri for free aim',ev('TD.game.player.freeAim&&TD.game.player.rise>.94'));p.keyboard.up('i');frames(20)
  p.keyboard.down('a');p.keyboard.down('k');frames(1)
  check('side fire twists and fires immediately from cover',ev('TD.game.player.quickSide===-1&&TD.game.player.rise===1&&TD.game.bastion.quickShots===1'));shot('quick_sidefire');p.keyboard.up('a');p.keyboard.up('k');frames(20)
  ev('TD.Bastion.damageCover(TD.game,TD.game.player.x,999);');frames(20);shot('destroyed_cover')
  check('destroying a section exposes Yuri and keeps neighboring walls',ev('TD.game.player.rise>.94&&TD.Grid21.lighting.boxes.filter(b=>b.visible).length===3&&TD.Grid21.coverPool.filter(b=>b.visible).length===1'))
  check('Yuri is visible through the destroyed section',ev('cover24Diff(378,445)')>100)
  ev('TD.Bastion.freshCover(TD.game);TD.game.bastion.totalWave=1;TD.game.bastion.turrets=[];TD.game.bastion.wallCore=null;TD.game.bastion.pickups=[];TD.Bastion.beginBreach(TD.game);');frames(85);shot('hop_over_wall')
  check('hop transition releases the lowered cover root',ev('TD.game.bastion.transition.phase==="hop"&&TD.Bastion.playerCoverOffset(TD.game)===0'))
  frames(90);shot('walk_past_wall');check('room traversal still advances the real 3D camera past cover',ev('TD.game.bastion.transition.phase==="walk"&&TD.Grid21.camera.position.z<0'))
  frames(120);check('next room restores an intact cover line',ev('TD.game.bastion.totalWave===2&&TD.game.bastion.cover.every(w=>w.hp===w.max)'))
  ev('TD.Bastion.startBoss(TD.game);TD.game.player.inv=999;');frames(120);shot('brighter_reactor');check('reactor lighting and supplied boss music remain active',ev('TD.game.boss.form==="core"&&TD.Grid21.lighting.core.intensity>60&&TD.Audio.musicKey==="lastHope"'))
  retained=json.loads((ROOT/'_shots/lighting22/retained_art.json').read_text(encoding='utf-8'));check('all 820 existing PNGs remain byte-for-byte unchanged',all(hashlib.sha256((ROOT/k).read_bytes()).hexdigest()==v for k,v in retained.items()))
  check('no native browser, shader, media or asset errors',not errors and ev('TD.Audio.failures.length===0'))
  result={'build':'overdrive1014-cover24-r1','checks':checks,'metrics':metrics,'errors':errors,'passed':sum(c['passed'] for c in checks),'failed':sum(not c['passed'] for c in checks),'scope':'Native Chromium screenshot, pixel-occlusion and actual keyboard checks. Full normal combat route checked separately.'};(OUT/'visual.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8');print(json.dumps(result,indent=2));browser.close()
finally:stop()
sys.exit(0 if all(c['passed'] for c in checks) and not errors else 1)
