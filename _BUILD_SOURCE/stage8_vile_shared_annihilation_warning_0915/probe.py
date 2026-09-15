"""Real Chromium proof for the Stage-8 Vile Existence shared annihilation warning."""
from pathlib import Path
import base64,http.server,json,sys
from PIL import Image
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'_shots'/'stage8_vile_shared_annihilation_warning_0915';OUT.mkdir(parents=True,exist_ok=True)
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
  fight=page.evaluate("()=>window.__fight(8,'boss','yuri')");ok(fight.get('ok'),'native Stage-8 boss route opens in Chromium')
  keys=[f'bmfx_{kind}_{col}_{tail}' for col in ('green','yellow','red') for kind,tail in (('fov','tall'),('alert','danger'))]+['s8symboss_form_3','s8nf_needle_interceptor_projectile_0','s8nf_stealth_crescent_projectile_0','s8nf_stealth_crescent_muzzle_0']
  setup=page.evaluate("""ks=>{__auto=function(){};story=null;dlgBox=function(){};stagePlan=[];waveIdx=0;enemies=[];eBullets=[];pBullets=[];particles=[];powerups=[];playerLocks=[];state=GS.PLAY;stateT=1;run.stage=8;curStage=STAGES[7];camX=0;player.x=360;player.y=400;player.invuln=999;player.dead=false;player.alive=true;diffKey='normal';DIFF=DIFFS.normal;boss=null;bossActive=false;spawnBoss('vileexistence');boss._symEntry=null;boss._morphT=null;boss.enter=false;boss.x=240;boss.y=140;vileBuildForm(boss,3);boss._annihilationUsed=false;bossActive=true;vileAnnihilationStart(boss);window.__annGets=[];const g=XART.get.bind(XART);XART.get=function(k){window.__annGets.push(k);return g(k);};ks.forEach(k=>XART.rdy(k));const A=boss._annihilation;return {name:boss.name,tx:A.tx,ty:A.ty,sources:vileAnnihilationSources(A),world:worldWidth()};}""",keys)
  ok(setup['name']=='FURIOUS DEATH' and len(setup['sources'])==4,'the live final form commits four converging annihilation paths')
  ready=False
  for _ in range(260):
    ready=page.evaluate('ks=>ks.every(k=>XART.rdy(k))',keys)
    if ready:break
    page.wait_for_timeout(35)
  ok(ready,'authored final form, projectiles, muzzle and green/yellow/red warning art decode before capture')
  def set_time(t,x,y):page.evaluate("q=>{player.x=q.x;player.y=q.y;const A=boss._annihilation;A.t=q.t;vileAnnihilationTick(boss,0);boss.flash=0;}",{'t':t,'x':x,'y':y})
  def snap(name):
    page.evaluate('()=>{shake=0;window.__annGets=[];drawWorld(0)}');d=page.evaluate("""()=>{const A=boss._annihilation,B=boss._combatWarnings['stage8-vile-annihilation'];return {t:A.t,wave:A.wave,tx:A.tx,ty:A.ty,sources:vileAnnihilationSources(A),playerX:player.x,playerY:player.y,warn:B&&{t:B.t,warm:B.warm,released:B.released},shots:eBullets.filter(q=>q._bfam==='vile').map(q=>({x:q.x,y:q.y,a:Math.atan2(q.vy,q.vx)})),gets:Array.from(new Set(window.__annGets))}}""");raw=page.evaluate("()=>document.querySelector('#screen').toDataURL('image/png').split(',')[1]");p=OUT/f'{name}.png';p.write_bytes(base64.b64decode(raw));return p,d
  set_time(.13,360,400);greenp,green=snap('vile_annihilation_01_green');ok(green['tx']==setup['tx'] and green['ty']==setup['ty'] and green['sources']==setup['sources'],'green displays the four committed converging paths');ok('bmfx_fov_green_tall' in green['gets'] and 'bmfx_alert_green_danger' in green['gets'],'green draws four shared fields and one matching alert')
  set_time(.39,40,260);yellowp,yellow=snap('vile_annihilation_02_yellow');ok(yellow['tx']==setup['tx'] and yellow['ty']==setup['ty'] and yellow['playerX']!=green['playerX'],'yellow does not chase a late move');ok('bmfx_fov_yellow_tall' in yellow['gets'] and 'bmfx_alert_yellow_danger' in yellow['gets'],'yellow draws the committed shared fields and matching alert')
  set_time(.702,230,450);redp,red=snap('vile_annihilation_03_red');ok(red['tx']==setup['tx'] and red['ty']==setup['ty'],'red preserves the committed cross center');ok('bmfx_fov_red_tall' in red['gets'] and 'bmfx_alert_red_danger' in red['gets'],'red draws the committed shared fields and matching alert')
  set_time(.79,70,260);releasep,release=snap('vile_annihilation_04_release');expected=[]
  for p in setup['sources']: expected.extend([__import__('math').atan2(setup['ty']-p[1],setup['tx']-p[0])]*2)
  actual=[q['a'] for q in release['shots']];ok(release['wave']==1 and len(actual)==8 and release['warn']['released'],'the first eight-shot cross wave releases only after the full warning');ok(all(abs(a-b)<.0001 for a,b in zip(actual,expected)),'all eight rounds follow the four previewed paths')
  shots=[greenp,yellowp,redp,releasep]
  for p in shots:
    im=Image.open(p).convert('RGB');ok(im.size==(960,1024) and im.getbbox() is not None,f'{p.stem} is a non-empty native gameplay frame')
  ok(not errors and not page.evaluate('()=>window.__err||null'),'zero Chromium page, console or game-loop errors');br.close()
stop();result={'checks':checks,'errors':errors,'fight':fight,'setup':setup,'green':green,'yellow':yellow,'red':red,'release':release,'shots':[str(p.relative_to(ROOT)) for p in shots]};(OUT/'results.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8');passed=sum(c['pass'] for c in checks);print(f'{passed} passed / {len(checks)-passed} failed',flush=True)
if passed!=len(checks):raise SystemExit(1)
