"""Real Chromium proof for the Stage-8 Vile aimed-fan shared warnings."""
from pathlib import Path
import base64,http.server,json,math,sys
from PIL import Image
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'_shots'/'stage8_vile_aimed_fan_warning_0916';OUT.mkdir(parents=True,exist_ok=True)
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
  keys=[f'bmfx_{kind}_{col}_{tail}' for col in ('green','yellow','red') for kind,tail in (('fov','tall'),('alert','danger'))]+['s8symboss_form_1','s8symboss_form_3','s8nf_needle_interceptor_projectile_0','s8nf_armored_gunship_projectile_0','s8nf_needle_interceptor_muzzle_0','s8nf_armored_gunship_muzzle_0']
  setup=page.evaluate("""ks=>{__auto=function(){};story=null;dlgBox=function(){};stagePlan=[];waveIdx=0;enemies=[];eBullets=[];pBullets=[];particles=[];powerups=[];playerLocks=[];state=GS.PLAY;stateT=1;run.stage=8;curStage=STAGES[7];camX=0;player.x=360;player.y=410;player.invuln=999;player.dead=false;player.alive=true;diffKey='normal';DIFF=DIFFS.normal;boss=null;bossActive=false;spawnBoss('vileexistence');boss._symEntry=null;boss._morphT=null;boss.enter=false;boss.x=240;boss.y=140;vileBuildForm(boss,1);boss._vAtk=0;boss._combatWarnings={};bossActive=true;vileAttack(boss);window.__fanGets=[];const g=XART.get.bind(XART);XART.get=function(k){window.__fanGets.push(k);return g(k)};ks.forEach(k=>XART.rdy(k));const V=boss._vileFan;return{name:boss.name,kind:V.kind,aims:V.entries.map(e=>e.a),paths:vileAimedFanPaths(boss,V)};}""",keys)
  ok(setup['name']=='RAVENOUS ASCENDANT' and setup['kind']=='needle' and len(setup['paths'])==5,'the live second form commits its five needle paths')
  ready=False
  for _ in range(280):
    ready=page.evaluate('ks=>ks.every(k=>XART.rdy(k))',keys)
    if ready:break
    page.wait_for_timeout(35)
  ok(ready,'both authored forms, projectiles, muzzles and warning art decode before capture')
  def set_time(t,x,y):page.evaluate("q=>{player.x=q.x;player.y=q.y;const V=boss._vileFan;V.t=q.t;vileAimedFanTick(boss,0);boss.flash=0;}",{'t':t,'x':x,'y':y})
  def snap(name):
    page.evaluate('()=>{shake=0;window.__fanGets=[];drawWorld(0)}');d=page.evaluate("""()=>{const V=boss._vileFan,B=V&&boss._combatWarnings[V.id];return{name:boss.name,kind:V&&V.kind,aims:V&&V.entries.map(e=>e.a),paths:V&&vileAimedFanPaths(boss,V),released:V&&V.released,warn:B&&{t:B.t,warm:B.warm,released:B.released},shots:eBullets.filter(q=>q._bfam==='vile').map(q=>({kind:q.kind,x:q.x,y:q.y,a:Math.atan2(q.vy,q.vx)})),locks:(boss._enemyLocks||[]).length,gets:Array.from(new Set(window.__fanGets))}}""");raw=page.evaluate("()=>document.querySelector('#screen').toDataURL('image/png').split(',')[1]");p=OUT/f'{name}.png';p.write_bytes(base64.b64decode(raw));return p,d
  set_time(.10,360,410);ngp,ng=snap('vile_needle_01_green');ok(ng['aims']==setup['aims'] and len(ng['shots'])==0,'green previews all five committed needle lanes');ok('bmfx_fov_green_tall' in ng['gets'] and 'bmfx_alert_green_danger' in ng['gets'],'needle green uses shared field and alert art')
  set_time(.40,40,250);nyp,ny=snap('vile_needle_02_yellow');ok(ny['aims']==setup['aims'] and len(ny['shots'])==0,'yellow ignores a late player move');ok('bmfx_fov_yellow_tall' in ny['gets'] and 'bmfx_alert_yellow_danger' in ny['gets'],'needle yellow uses shared field and alert art')
  set_time(.57,230,470);nrp,nr=snap('vile_needle_03_red');ok(nr['aims']==setup['aims'] and len(nr['shots'])==0,'red preserves the five promised needle paths');ok('bmfx_fov_red_tall' in nr['gets'] and 'bmfx_alert_red_danger' in nr['gets'],'needle red uses shared field and alert art')
  set_time(.63,70,260);nrelp,nrel=snap('vile_needle_04_release');ok(len(nrel['shots'])==5 and [q['kind'] for q in nrel['shots']]==['s8nf_needle']*5,'five authored needles release only after the full warning');ok(all(abs(q['a']-setup['aims'][i])<1e-7 for i,q in enumerate(nrel['shots'])),'all five needles follow their previewed paths')
  gun=page.evaluate("""()=>{eBullets=[];playerLocks=[];player.x=330;player.y=420;vileBuildForm(boss,3);boss._annihilationUsed=true;boss._vAtk=0;boss._combatWarnings={};vileAttack(boss);const V=boss._vileFan;return{name:boss.name,kind:V.kind,aims:V.entries.map(e=>e.a),paths:vileAimedFanPaths(boss,V)};}""");ok(gun['name']=='FURIOUS DEATH' and gun['kind']=='gunship' and len(gun['paths'])==7,'the live final form commits its seven gunship paths')
  set_time(.30,40,280);gyp,gy=snap('vile_gunship_05_yellow');ok(gy['aims']==gun['aims'] and len(gy['shots'])==0,'final-form yellow previews seven committed lanes');ok('bmfx_fov_yellow_tall' in gy['gets'] and 'bmfx_alert_yellow_danger' in gy['gets'],'gunship yellow uses shared field and alert art')
  set_time(.59,210,460);grelp,grel=snap('vile_gunship_06_release');ok(len(grel['shots'])==7 and [q['kind'] for q in grel['shots']]==['s8nf_gunship']*7,'seven authored gunship rounds release only after warning');ok(all(abs(q['a']-gun['aims'][i])<1e-7 for i,q in enumerate(grel['shots'])),'all seven gunship rounds follow their previewed paths')
  shots=[ngp,nyp,nrp,nrelp,gyp,grelp]
  for p in shots:
    im=Image.open(p).convert('RGB');ok(im.size==(960,1024) and im.getbbox() is not None,f'{p.stem} is a non-empty native gameplay frame')
  ok(not errors and not page.evaluate('()=>window.__err||null'),'zero Chromium page, console or game-loop errors');br.close()
stop();result={'checks':checks,'errors':errors,'fight':fight,'needleSetup':setup,'needleGreen':ng,'needleYellow':ny,'needleRed':nr,'needleRelease':nrel,'gunSetup':gun,'gunYellow':gy,'gunRelease':grel,'shots':[str(p.relative_to(ROOT)) for p in shots]};(OUT/'results.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8');passed=sum(c['pass'] for c in checks);print(f'{passed} passed / {len(checks)-passed} failed',flush=True)
if passed!=len(checks):raise SystemExit(1)
