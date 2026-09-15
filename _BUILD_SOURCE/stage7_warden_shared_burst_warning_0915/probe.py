"""Real Chromium proof for the Toxic Portal Warden shared cannon-burst warning."""
from pathlib import Path
import base64,http.server,json,sys
from PIL import Image
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'_shots'/'stage7_warden_shared_burst_warning_0915';OUT.mkdir(parents=True,exist_ok=True)
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
  keys=[f'bmfx_{kind}_{col}_{tail}' for col in ('green','yellow','red') for kind,tail in (('fov','tall'),('alert','danger'))]+['cfx_stage7_warden_cannon','cfx_stage7_warden_shell']
  setup=page.evaluate("""ks=>{__auto=function(){};story=null;dlgBox=function(){};stagePlan=[];waveIdx=0;enemies=[];eBullets=[];pBullets=[];particles=[];powerups=[];playerLocks=[];state=GS.PLAY;stateT=1;run.stage=7;curStage=STAGES[6];camX=0;player.x=360;player.y=400;player.invuln=999;player.dead=false;player.alive=true;diffKey='normal';DIFF=DIFFS.normal;boss=null;bossActive=false;spawnBoss('sludgeemperor');boss.enter=false;boss.x=240;boss.y=178;boss._drawY=boss.y;boss._s7FinalNoBar=false;boss._s7warden.final.phase='fight';boss._s7warden.noHit=false;bossActive=true;s7WardenMode(boss,'burst');window.__burstGets=[];const g=XART.get.bind(XART);XART.get=function(k){window.__burstGets.push(k);return g(k);};ks.forEach(k=>XART.rdy(k));const S=boss._s7warden;return {name:boss.name,aim:S.aim,angles:s7WardenBurstAngles(S)};}""",keys)
  ok(setup['name']=='TOXIC PORTAL WARDEN' and len(setup['angles'])==5,'the live Warden commits the five-lane toxic burst at charge start')
  ready=False
  for _ in range(260):
    ready=page.evaluate('ks=>ks.every(k=>XART.rdy(k))',keys)
    if ready:break
    page.wait_for_timeout(35)
  ok(ready,'authored cannon, shell and green/yellow/red warning art decode before capture')
  def set_time(t,x):page.evaluate("q=>{player.x=q.x;const S=boss._s7warden;S.mt=q.t;s7WardenTick(boss,0);}",{'t':t,'x':x})
  def snap(name):
    page.evaluate('()=>{shake=0;window.__burstGets=[];drawWorld(0)}');d=page.evaluate("""()=>{const S=boss._s7warden,B=boss._combatWarnings['stage7-warden-burst'];return {mode:S.mode,t:S.mt,shot:S.shot,aim:S.aim,angles:s7WardenBurstAngles(S),playerX:player.x,warn:B&&{t:B.t,warm:B.warm,released:B.released},shells:eBullets.filter(q=>q._s7warden==='shell').map(q=>({x:q.x,y:q.y,a:Math.atan2(q.vy,q.vx)})),gets:Array.from(new Set(window.__burstGets))}}""");raw=page.evaluate("()=>document.querySelector('#screen').toDataURL('image/png').split(',')[1]");p=OUT/f'{name}.png';p.write_bytes(base64.b64decode(raw));return p,d
  set_time(.08,360);greenp,green=snap('warden_burst_01_green');ok(green['angles']==setup['angles'],'green displays the five lanes committed when charge starts');ok('bmfx_fov_green_tall' in green['gets'] and 'bmfx_alert_green_danger' in green['gets'],'green draws the shared fields and matching alert')
  set_time(.24,40);yellowp,yellow=snap('warden_burst_02_yellow');ok(yellow['angles']==setup['angles'] and yellow['playerX']!=green['playerX'],'yellow does not chase a late move across the arena');ok('bmfx_fov_yellow_tall' in yellow['gets'] and 'bmfx_alert_yellow_danger' in yellow['gets'],'yellow draws the committed shared fields and matching alert')
  set_time(.432,230);redp,red=snap('warden_burst_03_red');ok(red['angles']==setup['angles'],'red preserves all five committed cannon lanes');ok('bmfx_fov_red_tall' in red['gets'] and 'bmfx_alert_red_danger' in red['gets'],'red draws the committed shared fields and matching alert')
  set_time(.49,70);first=page.evaluate("""()=>{const S=boss._s7warden,B=boss._combatWarnings['stage7-warden-burst'];return {shot:S.shot,released:B.released,shells:eBullets.filter(q=>q._s7warden==='shell').length}}""");ok(first['shot']==1 and first['released'] and first['shells']==1,'the first shell releases only after the full warning')
  page.evaluate("()=>{for(let i=0;i<57;i++){shake=0;updatePlay(1/60);}}")
  releasep,release=snap('warden_burst_04_release');expected=setup['angles']*2;actual=[q['a'] for q in release['shells']];ok(release['shot']==10 and len(actual)>=8 and all(any(abs(a-b)<.0001 for b in expected) for a in actual),'the original ten-round two-cannon burst keeps its exact five-lane cadence while its leading round exits normally')
  shots=[greenp,yellowp,redp,releasep]
  for p in shots:
    im=Image.open(p).convert('RGB');ok(im.size==(960,1024) and im.getbbox() is not None,f'{p.stem} is a non-empty native gameplay frame')
  ok(not errors and not page.evaluate('()=>window.__err||null'),'zero Chromium page, console or game-loop errors');br.close()
stop();result={'checks':checks,'errors':errors,'fight':fight,'setup':setup,'green':green,'yellow':yellow,'red':red,'firstRelease':first,'release':release,'shots':[str(p.relative_to(ROOT)) for p in shots]};(OUT/'results.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8');passed=sum(c['pass'] for c in checks);print(f'{passed} passed / {len(checks)-passed} failed',flush=True)
if passed!=len(checks):raise SystemExit(1)
