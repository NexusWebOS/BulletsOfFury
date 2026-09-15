"""Chromium proof for Stage-9 Event Horizon and Warp Sentinel volley warnings."""
from pathlib import Path
import base64,http.server,json,sys
from PIL import Image
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'_shots'/'stage9_horizon_shared_volley_warning_0915';OUT.mkdir(parents=True,exist_ok=True)
sys.path.insert(0,str(ROOT/'_BUILD_SOURCE'));import shoot
sys.path.insert(0,str(ROOT/'_BUILD_SOURCE'/'trailer_v7'));import capture3
from playwright.sync_api import sync_playwright
checks=[];errors=[]
def ok(v,label):checks.append({'pass':bool(v),'label':label});print(('ok  ' if v else 'FAIL ')+label,flush=True)
http.server.SimpleHTTPRequestHandler.log_message=lambda *a:None
port,stop=shoot.serve(str(ROOT))
with sync_playwright() as pw:
 br=pw.chromium.launch(args=['--no-sandbox','--mute-audio']);page=br.new_page(viewport={'width':1100,'height':1200});page.on('pageerror',lambda e:errors.append('page '+str(e)));page.on('console',lambda m:errors.append('console '+m.text) if m.type=='error' else None)
 page.goto(f'http://127.0.0.1:{port}/index.html',wait_until='load',timeout=120000);page.wait_for_function('()=>(window.__bofFrames|0)>4',timeout=120000);page.evaluate(shoot.TRAP_RAF);page.evaluate(capture3.LIB)
 fight=page.evaluate("()=>window.__fight(9,'boss','yuri')");ok(fight.get('ok'),'native Stage-9 route opens in Chromium')
 keys=[f'bmfx_{k}_{c}_{t}' for c in ('green','yellow','red') for k,t in (('fov','tall'),('alert','danger'))]+['ns9x_horizon_0','ns9_warpsen_intact']
 setup=page.evaluate("""ks=>{__auto=function(){};story=null;dlgBox=function(){};stagePlan=[];waveIdx=0;enemies=[];eBullets=[];pBullets=[];particles=[];powerups=[];playerLocks=[];state=GS.PLAY;run.stage=9;curStage=STAGES[8];camX=0;player.x=360;player.y=400;player.invuln=999;player.dead=false;diffKey='normal';DIFF=DIFFS.normal;subBoss=null;subBossActive=false;spawnSubBoss('voidhorizon');subBoss.enter=false;const w=subBoss._s9rift.core;w.x=240;w.y=138;subBoss.x=w.x;subBoss.y=w.y;s9FusionWardenWarningStart(subBoss,w,.1,'stage9-event-horizon');window.__s9Gets=[];const g=XART.get.bind(XART);XART.get=function(k){__s9Gets.push(k);return g(k)};ks.forEach(k=>XART.rdy(k));return{name:subBoss.name,angles:s9FusionWardenWarningAngles(w)}}""",keys);ok(setup['name']=='EVENT HORIZON' and len(setup['angles'])==8,'Event Horizon commits an eight-lane wheel')
 for _ in range(260):
  if page.evaluate('ks=>ks.every(k=>XART.rdy(k))',keys):break
  page.wait_for_timeout(35)
 ok(page.evaluate('ks=>ks.every(k=>XART.rdy(k))',keys),'boss and shared warning art decode')
 def snap(name):
  page.evaluate('()=>{shake=0;__s9Gets=[];drawWorld(0)}');raw=page.evaluate("()=>document.querySelector('#screen').toDataURL('image/png').split(',')[1]");p=OUT/f'{name}.png';p.write_bytes(base64.b64decode(raw));return p,page.evaluate("()=>({eb:eBullets.length,gets:Array.from(new Set(__s9Gets))})")
 page.evaluate("()=>{const A=subBoss._s9rift.core._s9VolleyWarn;A.t=.1;s9FusionWardenWarningTick(subBoss,subBoss._s9rift.core,0)}");g,gd=snap('horizon_01_green');ok('bmfx_fov_green_tall' in gd['gets'],'radial green warning renders')
 page.evaluate("()=>{const A=subBoss._s9rift.core._s9VolleyWarn;A.t=.558;s9FusionWardenWarningTick(subBoss,subBoss._s9rift.core,0)}");r,rd=snap('horizon_02_red');ok('bmfx_fov_red_tall' in rd['gets'],'radial red warning renders')
 page.evaluate("()=>{const w=subBoss._s9rift.core,A=w._s9VolleyWarn;A.t=.63;s9FusionWardenWarningTick(subBoss,w,0)}");rr,rrd=snap('horizon_03_radial_release');ok(rrd['eb']==8,'eight radial rounds release after warning')
 aimed=page.evaluate("()=>{eBullets=[];const w=subBoss._s9rift.core;player.x=360;player.y=400;s9FusionWardenWarningStart(subBoss,w,.6,'stage9-event-horizon');const a=w._s9VolleyWarn.aim;player.x=40;player.y=260;w._s9VolleyWarn.t=.31;s9FusionWardenWarningTick(subBoss,w,0);return{aim:a,now:w._s9VolleyWarn.aim,angles:s9FusionWardenWarningAngles(w)}}");y,yd=snap('horizon_04_aimed_yellow');ok(aimed['aim']==aimed['now'] and len(aimed['angles'])==5 and 'bmfx_fov_yellow_tall' in yd['gets'],'aimed fan stays committed after player movement')
 pair=page.evaluate("()=>{subBoss=null;subBossActive=false;boss=null;bossActive=false;eBullets=[];spawnBoss('tidalfusion');boss.enter=false;boss._s9fusion.t=2;boss._s9fusion.phase='twins';const L=boss._s9fusion.left,R=boss._s9fusion.right;L.y=R.y=138;s9FusionWardenWarningStart(boss,L,.1,'stage9-warp-sentinel-L');s9FusionWardenWarningStart(boss,R,.6,'stage9-warp-sentinel-R');L._s9VolleyWarn.t=R._s9VolleyWarn.t=.558;s9FusionWardenWarningTick(boss,L,0);s9FusionWardenWarningTick(boss,R,0);bossActive=true;return{L:s9FusionWardenWarningAngles(L).length,R:s9FusionWardenWarningAngles(R).length}} ");p5,p5d=snap('sentinels_05_independent_red');ok(pair['L']==8 and pair['R']==5 and 'bmfx_fov_red_tall' in p5d['gets'],'two Sentinels preview independent radial and aimed volleys')
 shots=[g,r,rr,y,p5]
 for p in shots:
  im=Image.open(p).convert('RGB');ok(im.size==(960,1024) and im.getbbox() is not None,p.stem+' is a non-empty native frame')
 ok(not errors and not page.evaluate('()=>window.__err||null'),'zero Chromium page, console or game-loop errors');br.close()
stop();result={'checks':checks,'errors':errors,'fight':fight,'setup':setup,'aimed':aimed,'pair':pair,'shots':[str(p.relative_to(ROOT)) for p in shots]};(OUT/'results.json').write_text(json.dumps(result,indent=2)+'\n');passed=sum(c['pass'] for c in checks);print(f'{passed} passed / {len(checks)-passed} failed');raise SystemExit(0 if passed==len(checks) else 1)
