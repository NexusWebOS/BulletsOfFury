"""Real Chromium proof for the Razorback shared body-ram warning."""
from pathlib import Path
import base64,http.server,json,sys
from PIL import Image
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'_shots'/'razorback_shared_ram_warning_0915';OUT.mkdir(parents=True,exist_ok=True)
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
  fight=page.evaluate("()=>window.__fight(1,'mini','yuri')");ok(fight.get('ok'),'native Stage-1 miniboss route opens in Chromium')
  keys=[f'bmfx_{kind}_{col}_{tail}' for col in ('green','yellow','red') for kind,tail in (('fov','tall'),('alert','danger'))]+['rzb_hull_0','rzb_sonic_charge']
  setup=page.evaluate("""ks=>{__auto=function(){};story=null;dlgBox=function(){};stagePlan=[];waveIdx=0;enemies=[];eBullets=[];pBullets=[];particles=[];powerups=[];playerLocks=[];state=GS.PLAY;stateT=1;run.stage=1;curStage=STAGES[0];camX=100;player.x=350;player.y=VH-68;player.invuln=999;player.dead=false;player.alive=true;diffKey='furious';DIFF=DIFFS.furious;subBoss=null;subBossActive=false;spawnSubBoss('razorback');subBossActive=true;const b=subBoss,R=b._rzb;b.x=(camLeftX()+camRightX())*.5;b.y=165;R.state='guns';R.trans=0;R.attack='ram';R.at=.20;R.beat=-1;R.tgt={x:b.x,y:b.y};R.a=0;R.turret=0;window.__ramGets=[];const g=XART.get.bind(XART);XART.get=function(k){window.__ramGets.push(k);return g(k);};ks.forEach(k=>XART.rdy(k));razorbackCombat(b);return {name:b.name,scale:R.scale,lane:R.ramX};}""",keys)
  ok(setup['name']=='FURIOUS RAZORBACK' and setup['scale']==1.5,'the shared warning runs on the distinct 150-percent Furious tank')
  ready=False
  for _ in range(260):
    ready=page.evaluate('ks=>ks.every(k=>XART.rdy(k))',keys)
    if ready:break
    page.wait_for_timeout(35)
  ok(ready,'authored tank and green/yellow/red warning art decode before capture')
  def snap(name):
    page.evaluate('()=>{shake=0;window.__ramGets=[];drawWorld(0)}');d=page.evaluate("""()=>{const R=subBoss._rzb,B=subBoss._combatWarnings['razorback-body-ram'];return {t:R.at,lane:R.ramX,locked:R.ramLocked,charge:R.charge,target:{x:R.tgt.x,y:R.tgt.y},warn:B&&{t:B.t,warm:B.warm,released:B.released},gets:Array.from(new Set(window.__ramGets))}}""");raw=page.evaluate("()=>document.querySelector('#screen').toDataURL('image/png').split(',')[1]");p=OUT/f'{name}.png';p.write_bytes(base64.b64decode(raw));return p,d
  greenp,green=snap('razorback_ram_01_green');ok(not green['locked'] and green['lane']==setup['lane'],'green tracks the current player lane');ok('bmfx_fov_green_tall' in green['gets'] and 'bmfx_alert_green_danger' in green['gets'],'green uses the shared authored field and alert')
  page.evaluate("()=>{player.x=camLeftX()+60;const R=subBoss._rzb;R.at=.45;razorbackCombat(subBoss)}");yellowp,yellow=snap('razorback_ram_02_yellow');ok(yellow['locked'] and yellow['lane']==green['lane'],'yellow commits instead of following a late player move');ok('bmfx_fov_yellow_tall' in yellow['gets'] and 'bmfx_alert_yellow_danger' in yellow['gets'],'yellow uses the shared authored field and alert')
  page.evaluate("()=>{player.x=camRightX()-40;const R=subBoss._rzb;R.at=.72;razorbackCombat(subBoss)}");redp,red=snap('razorback_ram_03_red');ok(red['lane']==green['lane'],'red retains the committed lane through the opposite dodge');ok('bmfx_fov_red_tall' in red['gets'] and 'bmfx_alert_red_danger' in red['gets'],'red uses the shared authored field and alert')
  page.evaluate("()=>{const R=subBoss._rzb;R.at=1.01;razorbackCombat(subBoss);razorbackMove(subBoss,.18)}");releasep,release=snap('razorback_ram_04_release');ok(release['warn']['released'] and release['charge']==0 and release['target']['x']==green['lane'],'release closes the warning and drives toward the committed lane')
  shots=[greenp,yellowp,redp,releasep]
  for p in shots:
    im=Image.open(p).convert('RGB');ok(im.size==(960,1024) and im.getbbox() is not None,f'{p.stem} is a non-empty native gameplay frame')
  ok(not errors and not page.evaluate('()=>window.__err||null'),'zero Chromium page, console or game-loop errors');br.close()
stop();result={'checks':checks,'errors':errors,'fight':fight,'setup':setup,'green':green,'yellow':yellow,'red':red,'release':release,'shots':[str(p.relative_to(ROOT)) for p in shots]};(OUT/'results.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8');passed=sum(c['pass'] for c in checks);print(f'{passed} passed / {len(checks)-passed} failed',flush=True)
if passed!=len(checks):raise SystemExit(1)
