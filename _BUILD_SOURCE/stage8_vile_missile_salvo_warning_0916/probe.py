"""Real Chromium proof for the Stage-8 Vile straight-missile shared warning."""
from pathlib import Path
import base64,json,sys
from PIL import Image
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'_shots'/'stage8_vile_missile_salvo_warning_0916';OUT.mkdir(parents=True,exist_ok=True)
sys.path.insert(0,str(ROOT/'_BUILD_SOURCE'));import shoot
sys.path.insert(0,str(ROOT/'_BUILD_SOURCE'/'trailer_v7'));import capture3
from playwright.sync_api import sync_playwright
checks=[];errors=[]
def ok(v,label):checks.append({'pass':bool(v),'label':label});print(('ok  ' if v else 'FAIL ')+label,flush=True)
port,stop=shoot.serve(str(ROOT))
with sync_playwright() as pw:
  br=pw.chromium.launch(args=['--no-sandbox','--mute-audio']);page=br.new_page(viewport={'width':1100,'height':1200});page.on('pageerror',lambda e:errors.append('page '+str(e)));page.on('console',lambda m:errors.append('console '+m.text) if m.type=='error' else None)
  page.goto(f'http://127.0.0.1:{port}/index.html',wait_until='load',timeout=120000);page.wait_for_function('()=>(window.__bofFrames|0)>4',timeout=120000);page.evaluate(shoot.TRAP_RAF);page.evaluate(capture3.LIB)
  fight=page.evaluate("()=>window.__fight(8,'boss','yuri')");ok(fight.get('ok'),'native Stage-8 boss route opens in Chromium')
  keys=[f'bmfx_{kind}_{col}_{tail}' for col in ('green','yellow','red') for kind,tail in (('fov','tall'),('alert','danger'))]+['s8symboss_form_3','waf_rocket_0','s8nf_armored_gunship_muzzle_0']
  setup=page.evaluate("""ks=>{__auto=function(){};story=null;dlgBox=function(){};stagePlan=[];waveIdx=0;enemies=[];eBullets=[];pBullets=[];particles=[];powerups=[];playerLocks=[];state=GS.PLAY;stateT=1;run.stage=8;curStage=STAGES[7];camX=0;player.x=360;player.y=410;player.invuln=999;player.dead=false;player.alive=true;diffKey='normal';DIFF=DIFFS.normal;_eMslAllow=()=>true;boss=null;bossActive=false;spawnBoss('vileexistence');boss._symEntry=null;boss._morphT=null;boss.enter=false;boss.x=240;boss.y=140;vileBuildForm(boss,3);boss._annihilationUsed=true;boss._vAtk=2;boss._combatWarnings={};bossActive=true;vileAttack(boss);window.__missileGets=[];const g=XART.get.bind(XART);XART.get=function(k){window.__missileGets.push(k);return g(k)};ks.forEach(k=>XART.rdy(k));const V=boss._vileMissiles;return{name:boss.name,offsets:V.offsets,paths:vileMissileSalvoPaths(boss,V),tell:V.tell,cooldown:V.cooldown};}""",keys)
  ok(setup['name']=='FURIOUS DEATH' and len(setup['paths'])==4 and setup['tell']==.58 and setup['cooldown']==.78,'the live final form commits its four straight missile lanes')
  ready=False
  for _ in range(280):
    ready=page.evaluate('ks=>ks.every(k=>XART.rdy(k))',keys)
    if ready:break
    page.wait_for_timeout(35)
  ok(ready,'authored final form, missile, muzzle and warning art decode before capture')
  def set_time(t,x,y):page.evaluate("q=>{player.x=q.x;player.y=q.y;const V=boss._vileMissiles;V.t=q.t;vileMissileSalvoTick(boss,0);boss.flash=0;}",{'t':t,'x':x,'y':y})
  def snap(name):
    page.evaluate('()=>{shake=0;window.__missileGets=[];drawWorld(0)}');d=page.evaluate("""()=>{const V=boss._vileMissiles,B=V&&boss._combatWarnings[V.id];return{name:boss.name,offsets:V&&V.offsets,paths:V&&vileMissileSalvoPaths(boss,V),released:V&&V.released,warn:B&&{t:B.t,warm:B.warm,released:B.released},shots:eBullets.filter(q=>q.kind==='emissile').map(q=>({kind:q.kind,x:q.x,y:q.y,vx:q.vx,vy:q.vy,homing:!!q.homing,lock:!!q._lockId})),locks:playerLocks.length,gets:Array.from(new Set(window.__missileGets))}}""");raw=page.evaluate("()=>document.querySelector('#screen').toDataURL('image/png').split(',')[1]");p=OUT/f'{name}.png';p.write_bytes(base64.b64decode(raw));return p,d
  set_time(.10,360,410);gp,g=snap('vile_missile_01_green');ok(g['offsets']==setup['offsets'] and len(g['shots'])==0,'green previews all four committed missile lanes');ok('bmfx_fov_green_tall' in g['gets'] and 'bmfx_alert_green_danger' in g['gets'],'green uses shared field and alert art')
  set_time(.38,40,250);yp,y=snap('vile_missile_02_yellow');ok(y['offsets']==setup['offsets'] and len(y['shots'])==0,'yellow ignores late player movement');ok('bmfx_fov_yellow_tall' in y['gets'] and 'bmfx_alert_yellow_danger' in y['gets'],'yellow uses shared field and alert art')
  set_time(.53,230,470);rp,r=snap('vile_missile_03_red');ok(r['offsets']==setup['offsets'] and len(r['shots'])==0,'red preserves all four promised lanes');ok('bmfx_fov_red_tall' in r['gets'] and 'bmfx_alert_red_danger' in r['gets'],'red uses shared field and alert art')
  set_time(.59,70,260);relp,rel=snap('vile_missile_04_release');ok(len(rel['shots'])==4,'four authored missiles release only after the full warning');ok(all(q['vx']==0 and q['vy']==2.3 and not q['homing'] and not q['lock'] for q in rel['shots']) and rel['locks']==0,'all four missiles remain straight and Retina-free after Stage 1')
  shots=[gp,yp,rp,relp]
  for p in shots:
    im=Image.open(p).convert('RGB');ok(im.size==(960,1024) and im.getbbox() is not None,f'{p.stem} is a non-empty native gameplay frame')
  ok(not errors and not page.evaluate('()=>window.__err||null'),'zero Chromium page, console or game-loop errors');br.close()
stop();result={'checks':checks,'errors':errors,'fight':fight,'setup':setup,'green':g,'yellow':y,'red':r,'release':rel,'shots':[str(p.relative_to(ROOT)) for p in shots]};(OUT/'results.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8');passed=sum(c['pass'] for c in checks);print(f'{passed} passed / {len(checks)-passed} failed',flush=True)
sys.exit(0 if passed==len(checks) else 1)
