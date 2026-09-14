"""Native Chromium pixels and real damage paths; no mock assets/context."""
from pathlib import Path
import sys,json,base64,hashlib,http.server,subprocess
import imageio_ffmpeg
http.server.SimpleHTTPRequestHandler.log_message=lambda *a:None
R=Path(__file__).resolve().parents[2];O=R/'_shots/dialogue_hazards_0914'
sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
sys.path.insert(0,str(R/'_BUILD_SOURCE/trailer_v7'));import capture3
from playwright.sync_api import sync_playwright
port,stop=shoot.serve(str(R));errors=[];checks=[]
def ok(v,n):
 checks.append({'pass':bool(v),'label':n});print(('ok 'if v else'FAIL ')+n,flush=True)
with sync_playwright()as p:
 b=p.chromium.launch(args=['--no-sandbox','--mute-audio']);pg=b.new_page(viewport={'width':1100,'height':1200})
 pg.on('pageerror',lambda e:errors.append(str(e)));pg.on('console',lambda m:errors.append(m.text)if m.type=='error'else None)
 pg.goto('http://127.0.0.1:%d/index.html'%port,wait_until='load',timeout=120000);pg.wait_for_function('()=>(window.__bofFrames|0)>4',timeout=120000)
 pg.evaluate(shoot.TRAP_RAF);pg.evaluate(capture3.LIB)
 pg.evaluate('''()=>{__auto=function(){};run.mode='arcade';run.pilot='cole';pilotIndex=PILOTS.findIndex(p=>p.key==='cole');beginStage(5);furyShipWarm();XART._touch('dlg_rect_0914');for(let i=0;i<6;i++)XART.rdy('np5_ast_'+i);for(const st of ['idle','damaged','critical'])XART.rdy('ns9c_sm_'+st);msgFaceUse('dialogue');for(const p of PILOTS)pilotPortrait(p.key,'idle');}''')
 pg.wait_for_function('()=>XART.rdy("dlg_rect_0914")&&furyShipReady()&&Array.from({length:6},(_,i)=>XART.rdy("np5_ast_"+i)).every(Boolean)',timeout=120000)
 for _ in range(10):pg.evaluate('()=>__step(3)');pg.wait_for_timeout(20)
 def shot(name):
  (O/(name+'.png')).write_bytes(base64.b64decode(pg.evaluate('()=>document.querySelector("#screen").toDataURL().split(",")[1]')))
 pg.evaluate('''()=>{ctx.save();ctx.setTransform(document.querySelector('#screen').width/VW,0,0,document.querySelector('#screen').height/VH,0,0);ctx.fillStyle='#172031';ctx.fillRect(0,0,VW,VH);for(let i=0;i<6;i++){const im=XART.get('np5_ast_'+i);ctx.drawImage(im,15+i%3*155,12+Math.floor(i/3)*180,140,140);}ctx.restore();}''');shot('asteroid_art')
 palettes=pg.evaluate('''()=>PILOTS.map(p=>{const c=dialogueFrame(p.key,p.tint);const d=c.getContext('2d').getImageData(50,8,1,1).data;return {pilot:p.key,tint:p.tint,pixel:Array.from(d)};})''')
 for key in pg.evaluate('()=>PILOTS.map(p=>p.key)'):
  pg.evaluate('''key=>{run.pilot=key;ctx.save();ctx.setTransform(document.querySelector('#screen').width/VW,0,0,document.querySelector('#screen').height/VH,0,0);ctx.fillStyle='#16212d';ctx.fillRect(0,0,VW,VH);dlgBox({who:key.toUpperCase(),full:'FIGHTER ONLINE. CLEAR THE ASTEROIDS AND KEEP MOVING!',tint:dialogueNameColor(key),screenSpace:false,y:200});ctx.restore();}''',key);shot('dialogue_'+key)
 ok(len(palettes)==9,'all nine pilot frame variants render')
 # Draw real launch with its actual long HQ message.
 pg.evaluate('''()=>{run.pilot='cole';pilotIndex=PILOTS.findIndex(p=>p.key==='cole');run.gravityShipReady=false;furyLegacyShip=false;setState(GS.LAUNCH);drawLaunch._phase=undefined;drawLaunch._furyIntro=null;}''')
 for _ in range(160):pg.evaluate('()=>__step(3)')
 shot('hq_in_game')
 # Measure final-line centering and reveal stability using the actual font renderer.
 layout=pg.evaluate('''()=>{const calls=[],orig=msgTextLeft;msgTextLeft=function(t,x,y,h){calls.push({t,x,y,h,w:msgMeasure(t,h)});return orig.apply(this,arguments);};msgFaceUse('dialogue');const o={text:'KEEP MOVING THROUGH THE CLOUDS.',x:60,y:100,w:350,h:75,maxH:16,minH:8,align:'center',stableCenter:true,valign:'middle'};const q=msgDrawBlock({...o,budget:1}),first=calls[0];calls.length=0;msgDrawBlock(o);const full=calls.slice();msgTextLeft=orig;msgFaceUse(null);return {first,full,layout:q};}''')
 ok(abs(layout['first']['x']-layout['full'][0]['x'])<.01,'typed characters keep their final centered positions')
 ok(all(abs(c['x']+c['w']/2-235)<.01 for c in layout['full']),'completed lines center inside the text window')
 # Real asteroid damage and collision, without invoking capture3 invincibility.
 result=pg.evaluate('''()=>{run.stage=5;l5FieldReset();enemies=[];boss=null;subBoss=null;powerups=[];pBullets=[];l5Rocks=[];l5RockT=100;player.reset();player.x=400;player.y=440;player.invuln=0;const r=l5RockSpawn(160,false);r.y=200;r.vx=r.vy=0;const hp=r.hp;const hit=spaceBulletHit({x:r.x+r.rad*.5,y:r.y,w:5,h:26,dmg:4},false);const damaged=r.hp===hp-4;spaceDamageTarget(r,100,{x:r.x,y:r.y});const broken=r._dieT===0;const q=l5RockSpawn(player.x,false);q.y=player.y;q.vx=q.vy=0;playerHit=__realHit;const before=run.lives;l5RocksUpdate(1/60);return {damaged,broken,target:hit===r,collision:q._dieT===0&&(player.dead||player.invuln>0||run.lives<before),decor:l5Field.length,radius:r.rad};}''')
 for k in ['damaged','broken','target','collision']:ok(result[k],'asteroid '+k+' through live weapon/player paths')
 ok(result['decor']==0,'no decorative asteroid pool remains')
 # Existing comet units are real targets, never additive background reels.
 comet=pg.evaluate('''()=>{enemies=[];pBullets=[];const e=spawnEnemy('cometsm',240,140,{pattern:'straight'});const hp=e.hp;spaceDamageTarget(e,3,{x:e.x,y:e.y});const damaged=e.hp===hp-3;spaceDamageTarget(e,9999,{x:e.x,y:e.y});return {damaged,dead:e.hp<=0&&(e.dead||e._dyingT!=null),art:e.art||e.type,base:S9_UNITS.cometsm};}''')
 ok(comet['damaged']and comet['dead'],'authored comet accepts space fire and is destroyed')
 # Verify comet contact in the actual PLAY collision pass, not an isolated distance formula.
 comet_contact=pg.evaluate("""()=>{run.stage=5;curStage=STAGES[4];run.gravityShipReady=true;gravityMode.phase='active';setState(GS.PLAY);enemies=[];pBullets=[];eBullets=[];l5Rocks=[];boss=null;subBoss=null;player.reset();player.invuln=0;player.x=240;player.y=410;playerHit=__realHit;const e=spawnEnemy('cometsm',240,410,{pattern:'straight'});updatePlay(0);return player.dead||player.invuln>0;}""")
 ok(comet_contact,'comet contact damages the player through updatePlay')
 # Render exact hazard bodies through the game's draw calls and record their real alpha.
 audit=pg.evaluate("""()=>{ctx.save();ctx.setTransform(2,0,0,2,0,0);ctx.fillStyle='#12354a';ctx.fillRect(0,0,VW,VH);l5Rocks=[];const r=l5RockSpawn(150,true);r.y=180;r.rot=0;const e=spawnEnemy('cometsm',320,180,{pattern:'straight'});e.flash=0;const d=ctx.drawImage,seen=[];ctx.drawImage=function(){seen.push([ctx.globalAlpha,ctx.globalCompositeOperation]);return d.apply(this,arguments);};l5RocksDraw();drawEnemy(e);ctx.drawImage=d;ctx.restore();return {seen,key:ENEMY_ART[e.art]+'_idle',solid:e._environmentBody,shoots:e.shoots};}""")
 shot('solid_hazards')
 ok(audit['solid']and not audit['shoots']and bool(audit['seen'])and all(a==[1,'source-over']for a in audit['seen']),'actual asteroid and comet bodies draw opaque with normal compositing')
 # Small in-game preview. Scripted firing/steering; damage was tested separately above.
 pg.evaluate("""()=>{beginStage(5);setState(GS.PLAY);story=null;run.pilot='cole';pilotIndex=PILOTS.findIndex(p=>p.key==='cole');run.gravityShipReady=true;gravityMode.phase='active';player.reset();player.x=240;player.y=425;player.invuln=0;playerHit=function(){};l5Rocks=[];l5RockT=100;enemies=[];pBullets=[];eBullets=[];for(const x of [120,240,350]){const r=l5RockSpawn(x,true);r.y=80+Math.abs(x-240)*.4;r.vx=0;}spawnEnemy('cometsm',240,200,{pattern:'straight'});run.spaceWeapon=0;}""")
 ff=imageio_ffmpeg.get_ffmpeg_exe();movie=O/'Solid_Hazards_0914.mp4'
 enc=subprocess.Popen([ff,'-y','-v','error','-f','image2pipe','-vcodec','mjpeg','-framerate','30','-i','pipe:0','-c:v','libx264','-preset','veryfast','-crf','20','-pix_fmt','yuv420p','-movflags','+faststart',str(movie)],stdin=subprocess.PIPE,stderr=subprocess.PIPE)
 for f in range(180):
  pg.evaluate("""f=>{player.x=240+Math.sin(f/35)*75;if(f%5===0)spaceLaserFire();__step(2);}""",f)
  enc.stdin.write(base64.b64decode(pg.evaluate('()=>document.querySelector("#screen").toDataURL("image/jpeg",.9).split(",")[1]')))
  if f==24:shot('hazards_in_game')
 enc.stdin.close();err=enc.stderr.read();assert enc.wait()==0,err
 subprocess.run([ff,'-v','error','-i',str(movie),'-f','null','-'],check=True)
 ok(not errors and not pg.evaluate('()=>window.__err||null'),'no page, console or game-loop errors')
 data={'checks':checks,'errors':errors,'palettes':palettes,'layout':layout,'rock':result,'comet':comet,'cometContact':comet_contact,'drawAudit':audit,'preview':str(movie),'runtimeSha256':hashlib.sha256((R/'assets/game.js').read_bytes()).hexdigest()}
 (O/'native.json').write_text(json.dumps(data,indent=2)+'\n');b.close()
stop()
assert all(c['pass']for c in checks)
