"""Real Chromium proof for the Chrome Hammer shared leap/slam warning."""
from pathlib import Path
import base64,http.server,json,sys
from PIL import Image
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'_shots'/'hammer_shared_leap_warning_0915';OUT.mkdir(parents=True,exist_ok=True)
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
  fight=page.evaluate("()=>window.__fight(5,'boss','yuri')");ok(fight.get('ok'),'native Stage-5 boss route opens in Chromium')
  keys=[f'bmfx_{kind}_{col}_{tail}' for col in ('green','yellow','red') for kind,tail in (('fov','tall'),('alert','danger'))]+['hammer_charge','hammer_reticle','hammer_leap']
  setup=page.evaluate("""ks=>{__auto=function(){};story=null;dlgBox=function(){};stagePlan=[];waveIdx=0;enemies=[];eBullets=[];pBullets=[];particles=[];powerups=[];playerLocks=[];state=GS.PLAY;stateT=1;run.stage=5;curStage=STAGES[4];camX=0;player.x=326;player.y=392;player.invuln=999;player.dead=false;player.alive=true;diffKey='normal';DIFF=DIFFS.normal;boss=null;bossActive=false;spawnBoss('xenoregent');boss.enter=false;boss.x=240;boss.y=168;boss._drawY=boss.y;boss._noHit=false;bossActive=true;hammerTarget(boss);hammerState(boss,'warn');window.__hammerGets=[];const g=XART.get.bind(XART);XART.get=function(k){window.__hammerGets.push(k);return g(k);};ks.forEach(k=>XART.rdy(k));return {name:boss.name,target:{x:boss._hammer.tx,y:boss._hammer.ty},boomerang:{spin:HAMMER_SPIN_TIME,out:HAMMER_OUT_TIME,returnSpeed:HAMMER_RETURN_SPEED}};}""",keys)
  ok(setup['name']=='CHROME HAMMER','the Easy/Normal Stage-5 replacement is the Chrome Hammer')
  ok(setup['boomerang']=={'spin':1.55,'out':0.7,'returnSpeed':315},'the completed one-hand boomerang timing remains intact')
  ready=False
  for _ in range(260):
    ready=page.evaluate('ks=>ks.every(k=>XART.rdy(k))',keys)
    if ready:break
    page.wait_for_timeout(35)
  ok(ready,'authored Hammer, reticle and green/yellow/red warning art decode before capture')
  def set_time(t,x,y):page.evaluate("q=>{player.x=q.x;player.y=q.y;const h=boss._hammer;h.t=q.t;hammerBossTick(boss,0);}",{'t':t,'x':x,'y':y})
  def snap(name):
    page.evaluate('()=>{shake=0;window.__hammerGets=[];drawWorld(0)}');d=page.evaluate("""()=>{const h=boss._hammer,B=boss._combatWarnings['chrome-hammer-leap'];return {state:h.state,t:h.t,target:{x:h.tx,y:h.ty},player:{x:player.x,y:player.y},warn:B&&{t:B.t,warm:B.warm,released:B.released},gets:Array.from(new Set(window.__hammerGets))}}""");raw=page.evaluate("()=>document.querySelector('#screen').toDataURL('image/png').split(',')[1]");p=OUT/f'{name}.png';p.write_bytes(base64.b64decode(raw));return p,d
  set_time(.20,326,392);greenp,green=snap('hammer_leap_01_green');ok(green['target']==setup['target'],'green begins on the committed player impact point');ok('bmfx_fov_green_tall' in green['gets'] and 'bmfx_alert_green_danger' in green['gets'],'green draws the shared field and matching alert')
  set_time(.60,80,270);yellowp,yellow=snap('hammer_leap_02_yellow');ok(yellow['target']==setup['target'] and yellow['player']!=setup['target'],'yellow preserves the committed point after a late dodge');ok('bmfx_fov_yellow_tall' in yellow['gets'] and 'bmfx_alert_yellow_danger' in yellow['gets'],'yellow draws the shared field and matching alert')
  set_time(1.08,425,300);redp,red=snap('hammer_leap_03_red');ok(red['target']==setup['target'],'red preserves the same leap corridor and landing reticle');ok('bmfx_fov_red_tall' in red['gets'] and 'bmfx_alert_red_danger' in red['gets'],'red draws the shared field and matching alert')
  page.evaluate("()=>{boss._hammer.t=1.2;hammerBossTick(boss,0)}");releasep,release=snap('hammer_leap_04_release');ok(release['state']=='leap' and release['warn']['released'] and release['target']==setup['target'],'release begins the leap only after the complete warning')
  shots=[greenp,yellowp,redp,releasep]
  for p in shots:
    im=Image.open(p).convert('RGB');ok(im.size==(960,1024) and im.getbbox() is not None,f'{p.stem} is a non-empty native gameplay frame')
  ok(not errors and not page.evaluate('()=>window.__err||null'),'zero Chromium page, console or game-loop errors');br.close()
stop();result={'checks':checks,'errors':errors,'fight':fight,'setup':setup,'green':green,'yellow':yellow,'red':red,'release':release,'shots':[str(p.relative_to(ROOT)) for p in shots]};(OUT/'results.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8');passed=sum(c['pass'] for c in checks);print(f'{passed} passed / {len(checks)-passed} failed',flush=True)
if passed!=len(checks):raise SystemExit(1)
