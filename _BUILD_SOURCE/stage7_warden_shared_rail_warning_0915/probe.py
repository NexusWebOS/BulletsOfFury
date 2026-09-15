"""Real Chromium proof for the Toxic Portal Warden shared rail-fan warning."""
from pathlib import Path
import base64,http.server,json,sys
from PIL import Image
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'_shots'/'stage7_warden_shared_rail_warning_0915';OUT.mkdir(parents=True,exist_ok=True)
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
  fight=page.evaluate("()=>window.__fight(7,'boss','yuri')");ok(fight.get('ok'),'native Stage-7 boss route opens in Chromium')
  keys=[f'bmfx_{kind}_{col}_{tail}' for col in ('green','yellow','red') for kind,tail in (('fov','tall'),('alert','danger'))]+['cfx_stage7_warden_rail','cfx_stage7_warden_spear']
  setup=page.evaluate("""ks=>{__auto=function(){};story=null;dlgBox=function(){};stagePlan=[];waveIdx=0;enemies=[];eBullets=[];pBullets=[];particles=[];powerups=[];playerLocks=[];state=GS.PLAY;stateT=1;run.stage=7;curStage=STAGES[6];camX=0;player.x=360;player.y=400;player.invuln=999;player.dead=false;player.alive=true;diffKey='normal';DIFF=DIFFS.normal;boss=null;bossActive=false;spawnBoss('sludgeemperor');boss.enter=false;boss.x=240;boss.y=178;boss._drawY=boss.y;boss._s7FinalNoBar=false;boss._s7warden.final.phase='fight';boss._s7warden.noHit=false;bossActive=true;s7WardenMode(boss,'rail');window.__railGets=[];const g=XART.get.bind(XART);XART.get=function(k){window.__railGets.push(k);return g(k);};ks.forEach(k=>XART.rdy(k));return {name:boss.name,aim:boss._s7warden.railAim,safe:boss._s7warden.railSafe,angles:s7WardenRailAngles(boss._s7warden)};}""",keys)
  ok(setup['name']=='TOXIC PORTAL WARDEN' and len(setup['angles'])==5,'the live Warden commits the five actual rail lanes and a safe-side gap')
  ready=False
  for _ in range(260):
    ready=page.evaluate('ks=>ks.every(k=>XART.rdy(k))',keys)
    if ready:break
    page.wait_for_timeout(35)
  ok(ready,'authored Warden, spear and green/yellow/red warning art decode before capture')
  def set_time(t,x):page.evaluate("q=>{player.x=q.x;const S=boss._s7warden;S.mt=q.t;s7WardenTick(boss,0);}",{'t':t,'x':x})
  def snap(name):
    page.evaluate('()=>{shake=0;window.__railGets=[];drawWorld(0)}');d=page.evaluate("""()=>{const S=boss._s7warden,B=boss._combatWarnings['stage7-warden-rail'];return {mode:S.mode,t:S.mt,event:S.event,aim:S.railAim,safe:S.railSafe,angles:s7WardenRailAngles(S),playerX:player.x,warn:B&&{t:B.t,warm:B.warm,released:B.released},shots:eBullets.filter(q=>q._s7warden==='rail').length,gets:Array.from(new Set(window.__railGets))}}""");raw=page.evaluate("()=>document.querySelector('#screen').toDataURL('image/png').split(',')[1]");p=OUT/f'{name}.png';p.write_bytes(base64.b64decode(raw));return p,d
  set_time(.15,360);greenp,green=snap('warden_rail_01_green');ok(green['angles']==setup['angles'],'green displays the lanes committed when charge starts');ok('bmfx_fov_green_tall' in green['gets'] and 'bmfx_alert_green_danger' in green['gets'],'green draws the five shared fields and one matching alert')
  set_time(.43,55);yellowp,yellow=snap('warden_rail_02_yellow');ok(yellow['angles']==setup['angles'] and yellow['playerX']!=green['playerX'],'yellow does not chase a late move across the arena');ok('bmfx_fov_yellow_tall' in yellow['gets'] and 'bmfx_alert_yellow_danger' in yellow['gets'],'yellow draws the committed shared fields and matching alert')
  set_time(.774,430);redp,red=snap('warden_rail_03_red');ok(red['angles']==setup['angles'],'red preserves every committed rail lane and the safe-side gap');ok('bmfx_fov_red_tall' in red['gets'] and 'bmfx_alert_red_danger' in red['gets'],'red draws the committed shared fields and matching alert')
  set_time(.87,70);releasep,release=snap('warden_rail_04_release');ok(release['event']==1 and release['shots']==5 and release['warn']['released'],'five rail spears release only after the full warning')
  shots=[greenp,yellowp,redp,releasep]
  for p in shots:
    im=Image.open(p).convert('RGB');ok(im.size==(960,1024) and im.getbbox() is not None,f'{p.stem} is a non-empty native gameplay frame')
  ok(not errors and not page.evaluate('()=>window.__err||null'),'zero Chromium page, console or game-loop errors');br.close()
stop();result={'checks':checks,'errors':errors,'fight':fight,'setup':setup,'green':green,'yellow':yellow,'red':red,'release':release,'shots':[str(p.relative_to(ROOT)) for p in shots]};(OUT/'results.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8');passed=sum(c['pass'] for c in checks);print(f'{passed} passed / {len(checks)-passed} failed',flush=True)
if passed!=len(checks):raise SystemExit(1)
