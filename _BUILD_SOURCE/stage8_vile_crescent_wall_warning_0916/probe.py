"""Real Chromium proof for the Stage-8 BLACK COCOON crescent-wall warning."""
from pathlib import Path
import base64,http.server,json,sys
from PIL import Image
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'_shots'/'stage8_vile_crescent_wall_warning_0916';OUT.mkdir(parents=True,exist_ok=True)
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
  keys=[f'bmfx_{kind}_{col}_{tail}' for col in ('green','yellow','red') for kind,tail in (('fov','tall'),('alert','danger'))]+['s8symboss_form_0','s8nf_stealth_crescent_projectile_0','s8nf_stealth_crescent_muzzle_0']
  setup=page.evaluate("""ks=>{__auto=function(){};story=null;dlgBox=function(){};stagePlan=[];waveIdx=0;enemies=[];eBullets=[];pBullets=[];particles=[];powerups=[];playerLocks=[];state=GS.PLAY;stateT=1;run.stage=8;curStage=STAGES[7];camX=0;player.x=360;player.y=410;player.invuln=999;player.dead=false;player.alive=true;diffKey='normal';DIFF=DIFFS.normal;boss=null;bossActive=false;spawnBoss('vileexistence');boss._symEntry=null;boss._morphT=null;boss.enter=false;boss.x=240;boss.y=140;boss.t=0;vileBuildForm(boss,0);boss._combatWarnings={};bossActive=true;vileAttack(boss);window.__wallGets=[];const g=XART.get.bind(XART);XART.get=function(k){window.__wallGets.push(k);return g(k)};ks.forEach(k=>XART.rdy(k));const V=boss._vileWall;return{name:boss.name,gap:V.gap,columns:V.columns,warn:V.tell,world:worldWidth()};}""",keys)
  ok(setup['name']=='BLACK COCOON' and setup['warn']==.72 and len(setup['columns'])>=6,'the live first form commits its original crescent columns and safe opening')
  ready=False
  for _ in range(260):
    ready=page.evaluate('ks=>ks.every(k=>XART.rdy(k))',keys)
    if ready:break
    page.wait_for_timeout(35)
  ok(ready,'authored first form, crescent projectile, muzzle and warning art decode before capture')
  def set_time(t,boss_t,x):page.evaluate("q=>{boss.t=q.bt;player.x=q.x;const V=boss._vileWall;V.t=q.t;vileCrescentWallTick(boss,0);boss.flash=0;}",{'t':t,'bt':boss_t,'x':x})
  def snap(name):
    page.evaluate('()=>{shake=0;window.__wallGets=[];drawWorld(0)}');d=page.evaluate("""()=>{const V=boss._vileWall,B=boss._combatWarnings['stage8-vile-crescent-wall'];return{gap:V&&V.gap,columns:V&&V.columns,released:V&&V.released,warn:B&&{t:B.t,warm:B.warm,released:B.released},shots:eBullets.filter(q=>q._bfam==='vile').map(q=>({kind:q.kind,x:q.x,y:q.y,vx:q.vx,vy:q.vy})),gets:Array.from(new Set(window.__wallGets))}}""");raw=page.evaluate("()=>document.querySelector('#screen').toDataURL('image/png').split(',')[1]");p=OUT/f'{name}.png';p.write_bytes(base64.b64decode(raw));return p,d
  set_time(.10,0,360);greenp,green=snap('vile_wall_01_green');ok(green['gap']==setup['gap'] and green['columns']==setup['columns'] and len(green['shots'])==0,'green previews every dangerous column and the original safe opening');ok('bmfx_fov_green_tall' in green['gets'] and 'bmfx_alert_green_danger' in green['gets'],'green uses shared field and alert art')
  set_time(.37,9,40);yellowp,yellow=snap('vile_wall_02_yellow');ok(yellow['gap']==setup['gap'] and yellow['columns']==setup['columns'],'yellow ignores later boss-clock and player movement');ok('bmfx_fov_yellow_tall' in yellow['gets'] and 'bmfx_alert_yellow_danger' in yellow['gets'],'yellow uses shared field and alert art')
  set_time(.64,18,230);redp,red=snap('vile_wall_03_red');ok(red['gap']==setup['gap'] and len(red['shots'])==0,'red preserves the promised opening until release');ok('bmfx_fov_red_tall' in red['gets'] and 'bmfx_alert_red_danger' in red['gets'],'red uses shared field and alert art')
  set_time(.73,24,70);releasep,release=snap('vile_wall_04_release');ok(len(release['shots'])==len(setup['columns']) and [q['x'] for q in release['shots']]==setup['columns'],'the unchanged crescent wall releases only from the previewed columns');ok(all(q['kind']=='s8nf_crescent' and abs(q['vx'])<1e-8 and q['vy']>0 for q in release['shots']) and release['warn']['released'],'every released crescent follows its exact vertical preview')
  shots=[greenp,yellowp,redp,releasep]
  for p in shots:
    im=Image.open(p).convert('RGB');ok(im.size==(960,1024) and im.getbbox() is not None,f'{p.stem} is a non-empty native gameplay frame')
  ok(not errors and not page.evaluate('()=>window.__err||null'),'zero Chromium page, console or game-loop errors');br.close()
stop();result={'checks':checks,'errors':errors,'fight':fight,'setup':setup,'green':green,'yellow':yellow,'red':red,'release':release,'shots':[str(p.relative_to(ROOT)) for p in shots]};(OUT/'results.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8');passed=sum(c['pass'] for c in checks);print(f'{passed} passed / {len(checks)-passed} failed',flush=True)
if passed!=len(checks):raise SystemExit(1)
