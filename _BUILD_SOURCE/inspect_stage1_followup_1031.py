from pathlib import Path
import json,sys,base64,http.server
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'_BUILD_SOURCE'));from shoot import serve,STEP,TRAP_RAF
W=R/'_shots/stage1_followup_1031';W.mkdir(exist_ok=True);http.server.ThreadingHTTPServer.request_queue_size=256;port,stop=serve(str(R));errors=[]
try:
 with sync_playwright()as pw:
  b=pw.chromium.launch(channel='msedge',headless=True);p=b.new_page(viewport={'width':1280,'height':800});p.on('pageerror',lambda e:errors.append(str(e)));p.goto(f'http://127.0.0.1:{port}/index.html',wait_until='load',timeout=180000);p.wait_for_function('window.__bofFrames>5');p.evaluate(TRAP_RAF);p.wait_for_timeout(50)
  p.evaluate("()=>{debugStartFight(debugFightFor(1,'boss'),{pilot:'cole'});spawnBoss(debugFightFor(1,'boss').kind);debugFight.spawned=true;warnT=0;DBGT.god=true;BOFCinematicDirector.cancel();setState(GS.PLAY);stagePlan=[];waveIdx=999;_adaptiveSpawnT=9999;spawnClock=9999;subBossDone=true;bossWarned=true;stageTimer=0;boss=null;subBoss=null;enemies=[];eBullets=[];pBullets=[];powerups=[];player.invuln=1e9;s1mWarm();}")
  p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(1)&&s1mKeys().every(k=>XART.rdy(k));}',timeout=180000)
  keys=p.evaluate("""()=>{const types=['s1boatpatrol','s1corvette','s1tankapc','s1tanklight','s1truckmissile','s1jetdelta_b'];const info=types.map(type=>{const e=spawnEnemy(type,340,160,{});return{type,art:e.art,key:ENEMY_ART[e.art],w:e.w,h:e.h,mod:e._modTank,truck:!!e._mt18}});const keys=['furyboat_1_0','furyboat_turret_0_2','overhaul_ground_base_1','overhaul_ground_head_mg','overhaul_ground_head_missile',...info.flatMap(e=>[e.key+'_intact',e.key+'_idle'])];keys.push(...Object.keys(XART._src).filter(k=>/nef_s1_jungle_(mini_tank|apc)|nef_s1_river_corvette/.test(k)&&/idle|intact/.test(k)));return{info,keys:[...new Set(keys)]};}""");print(keys,flush=True)
  p.wait_for_function('(keys)=>keys.filter(k=>XART._src[k]).every(k=>XART.rdy(k))',arg=keys['keys'],timeout=180000)
  for key in keys['keys']:
   v=p.evaluate("k=>{if(!XART.rdy(k))return null;const im=XART.get(k),c=document.createElement('canvas');c.width=im.naturalWidth||im.width;c.height=im.naturalHeight||im.height;c.getContext('2d').drawImage(im,0,0);return{png:c.toDataURL().split(',')[1],w:c.width,h:c.height,src:XART._src[k]};}",key)
   if v:(W/(key+'.png')).write_bytes(base64.b64decode(v.pop('png')));print(key,v,flush=True)
  (W/'inspection.json').write_text(json.dumps(dict(info=keys,errors=errors),indent=2));b.close()
finally:stop()
