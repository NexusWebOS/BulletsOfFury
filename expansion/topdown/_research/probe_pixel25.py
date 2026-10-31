from pathlib import Path
from playwright.sync_api import sync_playwright
import sys,json,hashlib
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT/'_BUILD_SOURCE'));import shoot
from serve_bof_1013 import AssetServer
shoot.http.server.ThreadingHTTPServer=AssetServer
OUT=ROOT/'_shots/pixel25';OUT.mkdir(exist_ok=True,parents=True);errors=[];checks=[]
def check(n,v):checks.append({'name':n,'passed':bool(v)});print(('PASS 'if v else'FAIL ')+n,flush=True)
port,stop=shoot.serve(str(ROOT))
try:
 with sync_playwright()as pw:
  b=pw.chromium.launch();p=b.new_page(viewport={'width':1280,'height':960});p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text)if m.type=='error'else None);p.on('response',lambda r:errors.append(f'HTTP {r.status} {r.url}')if r.status>=400 else None)
  p.goto(f'http://127.0.0.1:{port}/expansion/topdown/index.html?fullscreen=0&build=overdrive1014-pixel25-r1',wait_until='domcontentloaded',timeout=90000);p.wait_for_function('window.TDGAME&&TD.game.state==="boot"',timeout=90000);ev=p.evaluate
  ev('TDGAME.freeze();TD.pilot="yuri";TD.difficulty="normal";ART.warm(Object.keys(TD_PIXEL25_ART.assets));')
  p.keyboard.press('Shift')
  p.wait_for_function('ART.progress(Object.keys(TD_PIXEL25_ART.assets))===1',timeout=120000)
  def frames(n):
   while n:k=min(40,n);ev(f'TDGAME.step({k})');p.wait_for_timeout(1);n-=k
  def fresh(level):ev(f'TD.game.sel=TD.MISSIONS.findIndex(m=>m.id==={level});TDGAME.start();TD.Achievements.queue=[];')
  def shot(name):ev('TD.game.player.inv=0;TDGAME.render()');p.locator('#screen').screenshot(path=str(OUT/(name+'.png')))
  check('all PixelLab frames decode through the real ART loader',ev('Object.keys(TD_PIXEL25_ART.assets).length>=500&&ART.progress(Object.keys(TD_PIXEL25_ART.assets))===1'))
  check('every exported frame is even with a common 256px character canvas',ev('Object.entries(TD_PIXEL25_ART.assets).every(([k,m])=>m.size.every(n=>n%2===0)&&(!m.role||(m.size[0]===256&&m.size[1]===256&&m.anchor[0]===128&&m.anchor[1]===224)))'))
  check('four enemy classes have walk, fire, crouch and death banks',ev('["rifle","heavy","rocket","laser"].every(k=>["walk","fire","crouch","death"].every(a=>TD.Pixel25.seq(k,a)?.frames.length>=12))'))
  check('rifle and heavy have four-direction walking and firing',ev('["rifle","heavy"].every(k=>["walk","fire"].every(a=>["south","east","north","west"].every(d=>TD.Pixel25.seq(k,a,d)?.frames.length>=12)))'))
  check('dedicated sidesteps and vault keep full animation banks',ev('["rifle","heavy"].every(k=>TD.Pixel25.seq(k,"strafe").frames.length===16)&&TD.Pixel25.seq("rifle","vault").frames.length===17'))
  draws=ev('''()=>{const cv=document.createElement('canvas');cv.width=cv.height=256;const ctx=cv.getContext('2d');let count=0,empty=[];for(const [key,m] of Object.entries(TD_PIXEL25_ART.assets)){if(!m.role)continue;ctx.clearRect(0,0,256,256);const g=ART.get(key);ctx.drawImage(g.im,g.sx,g.sy,g.sw,g.sh,0,0,256,256);const d=ctx.getImageData(0,0,256,256).data;let pixels=0;for(let i=3;i<d.length;i+=4)if(d[i])pixels++;if(pixels<30)empty.push(key);count++;}return{count,empty};}''')
  check('every character frame draws nonempty native pixels',draws['count']>400 and not draws['empty'])
  fresh(3);frames(3);shot('stage3_courtyard')
  check('stage 3 uses the composed PixelLab floor and generated HUD',ev('TD_ASSAULT_ART.assets.od_fortress_ground.file.includes("pixel25")&&TD_ASSAULT_ART.assets.pb20_hud_top.file.includes("pixel25")'))
  ev('TD.game.fortress.pending=[];TD.game.units=[];TD.game.player.x=400;TD.game.player.y=2160;TD.game.player.inv=999;TD.game.units=[TD.makeUnit("odRobot",300,1990,{a:0}),TD.makeUnit("odElite",530,2010,{a:0})];TD.Cam.x=80;TD.Cam.y=1840;');frames(30);shot('stage3_new_troops')
  check('stage 3 draws the actual new soldiers',ev('TD.Pixel25.stats.stage3>0&&TD.game.units.every(u=>TD.Pixel25.stage3Pose(u,u.type==="odElite").key.startsWith("px25_"))'))
  key1=ev('TD.Pixel25.stage3Pose(TD.game.units[0],false).key');frames(12);key2=ev('TD.Pixel25.stage3Pose(TD.game.units[0],false).key');check('stage 3 locomotion advances through new gait drawings',key1!=key2)
  ev('TD.game.units[0].fireCd=0;TD.game.player.inv=999;');frames(1)
  check('stage 3 gunfire retains a live measured weapon socket',ev('(()=>{const u=TD.game.units[0],s=TD.Pixel25.stage3Socket(u,false);return Number.isFinite(s.x)&&s.y<u.y&&s.y>u.y-100;})()'))
  check('stage 3 bullets originate at the rendered gun barrel',ev('(()=>{const G=TD.game,u=G.units[0];G.eshots=[];Object.assign(u,{x:300,y:2260,vx:0,vy:0,fireCd:0});Object.assign(G.player,{x:400,y:2260});TD.unitTick(u,G,1/60);const s=G.eshots[0],m=TD.Pixel25.stage3Socket(u,false);return s&&Math.hypot(s.x-m.x,s.y-s.drawLift-m.y)<.01;})()'))
  check('stage 3 native damage flashes expire without changing the armor palette',ev("(()=>{const G=TD.game,u=G.units[0],c=document.createElement('canvas');c.width=c.height=256;const ctx=c.getContext('2d'),snap=()=>{ctx.clearRect(0,0,256,256);TD.drawAssaultRobot(ctx,{...u,x:128,y:224},false);return ctx.getImageData(0,0,256,256).data;};u.flash=0;const a=snap(),hp=u.hp;TD.hitUnit(G,u,1,u.x,u.y);const timer=u.flash,b=snap();let changed=0;for(let i=0;i<a.length;i+=4)if(a[i+3]&&b[i+3]&&(a[i]!==b[i]||a[i+1]!==b[i+1]||a[i+2]!==b[i+2]))changed++;TD.unitTick(u,G,.3);return u.hp<hp&&timer>0&&u.flash===0&&changed>100;})()"))
  ev('TD.hitUnit(TD.game,TD.game.units[0],999,300,1990)');frames(25);shot('stage3_knockdown')
  check('stage 3 death retains the new falling body after enemy removal',ev('TD.Pixel25.corpses.length===1&&TD.Pixel25.stats.corpses>0'))
  ev('TD.game.fortress.pending=[];TD.game.units=[];TD.game.player.x=400;TD.game.player.y=428;TD.game.player.inv=999;TD.game.fortress.relays=3;TD.game.boss=TD.makeGosfer(TD.game,400,195);TD.Cam.x=80;TD.Cam.y=0;');frames(165);shot('stage3_data_center')
  check('Gosfer identity and protected barrier encounter remain intact',ev('TD.game.boss.name==="GOSFER"&&TD.game.boss.shield&&TD.game.boss.remaining().length===3'))
  fresh(7);frames(180);shot('stage7_room')
  check('three-dimensional room surfaces use separate native PixelLab textures',ev('["grid21_wall","grid21_floor","grid21_ceiling","grid21_rearwall","grid21_door_0"].every(k=>TD_ASSAULT_ART.assets[k].file.includes("pixel25"))&&TD.Grid21.stats.gridCells>=275'))
  check('Yuri still waits on the camera side of cover with readable lighting',ev('TD.game.player.rise===0&&TD.Grid21.lighting.coverZ<TD.Grid21.lighting.floorPoint(TD.game.player.x,448).z&&TD.Grid21.lighting.ambient.intensity===1.3'))
  check('nearest texture filtering remains sharp',ev('[...TD.Grid21.textures.values()].every(t=>t.magFilter===THREE.NearestFilter&&!t.generateMipmaps)'))
  ev('TD.game.units=[];TD.game.bastion.enemyCover=[];TD.game.bastion.barrels=[];TD.game.bastion.turrets=[];TD.game.bastion.wallCore=null;for(const [i,k]of ["rifle","heavy","rocket","laser"].entries()){const u=TD.Bastion.spawn(TD.game,k,105+i*142,0);Object.assign(u,{x:105+i*142,y:315,phase:"peek",scale:.7,duck:0,cd:9,phaseT:0});}void 0;')
  frames(1);shot('stage7_weapon_classes')
  check('stage 7 selects all four new enemy identities',ev('new Set(TD.game.units.map(u=>TD.Bastion.unitPose(u).split("_")[1])).size===4&&TD.game.units.every(u=>TD.Bastion.unitPose(u).startsWith("px25_"))'))
  ev('TD.game.units.forEach(u=>{u.phase="enter";u.enterT=.6;u.gait=.2;});TDGAME.render()');shot('stage7_walking')
  ev('TD.game.units.forEach(u=>Object.assign(u,{phase:"peek",duck:0,enterT:2,firing:.3,fireT:.4,warn:0,velocity:0,y:330}));TDGAME.render()');shot('stage7_firing')
  check('lateral stage 7 entrances use the dedicated sidestep bank',ev("TD.Pixel25.pose({...TD.game.units[0],kind:'rifle',phase:'enter',homeX:100,targetY:338,duck:0,firing:0,warn:0,gait:.3}).startsWith('px25_rifle_strafe_south_')"))
  check('new firing bodies have stable hit volumes and matching gun sockets',ev('TD.game.units.every(u=>{const key=TD.Bastion.unitPose(u),m=TD_ASSAULT_ART.assets[key],s=TD.Bastion.unitSocket(u),b=TD.Bastion.unitBody(u);return m.action==="fire"&&m.hitBounds&&Number.isFinite(s.x)&&Number.isFinite(s.y)&&b.rx>=16&&b.ry>=24;})'))
  check('all four new stage 7 enemies retain actual hit flashes and expiry',ev("(()=>{const G=TD.game,ctx=document.getElementById('screen').getContext('2d');TDGAME.render();const a=ctx.getImageData(0,0,640,480).data;const results=G.units.map(u=>{const hp=u.hp,q=TD.Bastion.unitBody(u);TD.Bastion.fireHits(G,{oldX:q.x,oldY:q.y,x:q.x,y:q.y,ty:q.y,r:3,damage:1,gun:'rifle'});return u.hp<hp&&u.flash>0;});TDGAME.render();const b=ctx.getImageData(0,0,640,480).data;let changed=0;for(let i=0;i<a.length;i+=4)if(b[i]>240&&b[i+1]>240&&b[i+2]>240&&(a[i]<230||a[i+1]<230||a[i+2]<230))changed++;window.px25HitPixelCount=changed;return results.every(Boolean)&&changed>100;})()"))
  frames(15)
  check('stage 7 hit tint clears on the normal enemy clock',ev('TD.game.units.every(u=>u.flash===0)'))
  ev('TD.game.units.forEach(u=>{u.phase="hide";u.firing=0;u.duck=1;});TDGAME.render()');shot('stage7_crouching')
  ev('TD.game.units.forEach(u=>{u.dead=true;u.deathT=.5;});TDGAME.render()');shot('stage7_falling')
  check('falling troops use their generated death drawings',ev('TD.game.units.every(u=>TD_ASSAULT_ART.assets[TD.Bastion.unitPose(u)].action==="death")'))
  ev('TD.Bastion.startBoss(TD.game);TD.game.player.inv=999;');frames(120);shot('stage7_reactor')
  check('reactor encounter retains lighting and boss track',ev('TD.game.boss.form==="core"&&TD.Audio.musicKey==="lastHope"&&TD.Grid21.lighting.core.intensity>60'))
  check('existing cover/character source art remains byte-for-byte unchanged',all(hashlib.sha256((ROOT/k).read_bytes()).hexdigest()==v for k,v in json.loads((ROOT/'_shots/lighting22/retained_art.json').read_text(encoding='utf-8')).items()))
  p.goto(f'http://127.0.0.1:{port}/expansion/topdown/art/pixel25/preview.html',wait_until='domcontentloaded');p.wait_for_function('typeof data!=="undefined"&&data&&Object.keys(images).length>450',timeout=120000);p.wait_for_timeout(250);p.locator('#review').screenshot(path=str(OUT/'animation_review.png'))
  check('interactive review plays the complete new frame set',p.evaluate('data.sequences.px25_rifle_walk_south.frames.length===16&&Object.keys(images).length>450'))
  p.locator('#action').select_option('fire');p.locator('#onion').check();p.locator('#slow').check();p.wait_for_timeout(400);p.locator('#review').screenshot(path=str(OUT/'onion_review.png'))
  check('half-speed onion review is available',p.evaluate('document.getElementById("onion").checked&&document.getElementById("slow").checked'))
  check('zero browser, shader and missing-asset errors',not errors)
  result={'checks':checks,'passed':sum(q['passed']for q in checks),'failed':sum(not q['passed']for q in checks),'errors':errors,'nativeDraws':draws,'build':'overdrive1014-pixel25-r1','scope':'Native rendered fixtures and complete image decoding; ordinary-input normal combat routes are separate.'};(OUT/'visual.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8');print(json.dumps({'passed':result['passed'],'failed':result['failed'],'errors':errors,'nativeDraws':draws}));b.close()
finally:stop()
sys.exit(0 if all(q['passed']for q in checks)and not errors else 1)

