"""Real Chromium proof for the active Stage-5 Archmage one-hand boomerang."""
from pathlib import Path
import base64,http.server,json,sys
from PIL import Image
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'_shots'/'stage5_archmage_boomerang_0916';OUT.mkdir(parents=True,exist_ok=True)
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
  keys=['arch_twirl_throw','arch_hammer_spin','hammer_reticle']+[f'bmfx_{kind}_{col}_{tail}' for col in ('green','yellow','red') for kind,tail in (('fov','tall'),('alert','danger'))]
  setup=page.evaluate("""ks=>{__auto=function(){};story=null;dlgBox=function(){};stagePlan=[];waveIdx=0;enemies=[];eBullets=[];pBullets=[];particles=[];powerups=[];playerLocks=[];state=GS.PLAY;stateT=1;run.stage=5;curStage=STAGES[4];camX=0;player.x=326;player.y=392;player.invuln=999;player.dead=false;player.alive=true;diffKey='normal';DIFF=DIFFS.normal;boss=null;bossActive=false;spawnBoss('xenoregent');boss.enter=false;boss.x=240;boss.y=168;boss._drawY=boss.y;boss._noHit=false;bossActive=true;boss._combatWarnings={};hammerBoomerangStart(boss);window.__archGets=[];const g=XART.get.bind(XART);XART.get=function(k){window.__archGets.push(k);return g(k)};ks.forEach(k=>XART.rdy(k));const h=boss._hammer;return{name:boss.name,state:h.state,lane:h.throwX,floor:h.throwY,spin:HAMMER_SPIN_TIME,out:HAMMER_OUT_TIME,returnSpeed:HAMMER_RETURN_SPEED,grip:hammerGripPoint(boss),vh:VH};}""",keys)
  ok(setup['name']=='CHROME HAMMER ARCHMAGE' and setup['state']=='spin','active Easy/Normal Stage-5 replacement starts the Archmage one-hand spin')
  ok(setup['spin']==1.55 and setup['out']==.7 and setup['returnSpeed']==315,'spin, vertical throw and medium magnetic return retain approved timing')
  ready=False
  for _ in range(280):
    ready=page.evaluate('ks=>ks.every(k=>XART.rdy(k))',keys)
    if ready:break
    page.wait_for_timeout(35)
  ok(ready,'authored Archmage twirl, detached hammer, reticle and shared warning art decode')
  def spin_time(t):page.evaluate("t=>{const h=boss._hammer;h.t=t;hammerBossTick(boss,0);boss.flash=0;}",t)
  def snap(name):
    page.evaluate('()=>{shake=0;window.__archGets=[];drawWorld(0)}');d=page.evaluate("""()=>{const h=boss._hammer,T=h.throw,W=boss._combatWarnings&&boss._combatWarnings['chrome-hammer-boomerang'];return{state:h.state,t:h.t,lane:h.throwX,floor:h.throwY,throw:T&&{x:T.x,y:T.y,phase:T.phase,t:T.t,angle:T.angle},warning:W&&{t:W.t,warm:W.warm,released:W.released},gets:Array.from(new Set(window.__archGets)),grip:hammerGripPoint(boss)}}""");raw=page.evaluate("()=>document.querySelector('#screen').toDataURL('image/png').split(',')[1]");p=OUT/f'{name}.png';p.write_bytes(base64.b64decode(raw));return p,d
  spin_time(.18);greenp,green=snap('archmage_boomerang_01_green');ok('arch_twirl_throw' in green['gets'] and 'bmfx_fov_green_tall' in green['gets'] and 'bmfx_alert_green_danger' in green['gets'],'green charge shows the authored one-hand twirl and shared lane warning')
  page.evaluate('()=>{player.x=82;player.y=270}');spin_time(.80);yellowp,yellow=snap('archmage_boomerang_02_yellow');ok(yellow['lane']==setup['lane'] and yellow['floor']==setup['floor'] and 'bmfx_fov_yellow_tall' in yellow['gets'],'yellow warning remains committed after the player dodges')
  spin_time(1.40);redp,red=snap('archmage_boomerang_03_red');ok(red['lane']==setup['lane'] and 'bmfx_fov_red_tall' in red['gets'] and 'bmfx_alert_red_danger' in red['gets'],'red warning preserves the promised vertical release lane')
  page.evaluate('()=>{boss._hammer.t=1.54;hammerBossTick(boss,.02);hammerBossTick(boss,.20)}');outp,out=snap('archmage_boomerang_04_outbound');ok(out['state']=='throw' and out['throw']['phase']=='out' and out['throw']['y']>out['grip']['y']+100 and 'arch_hammer_spin' in out['gets'],'detached authored hammer descends rapidly through the warned lane')
  page.evaluate("()=>{let n=0;while(boss._hammer.throw&&boss._hammer.throw.phase==='out'&&n++<30)hammerBossTick(boss,.05)}");turnp,turn=snap('archmage_boomerang_05_bottom_turn');ok(turn['throw'] and turn['throw']['phase']=='return' and turn['throw']['y']>setup['vh'],'the boomerang turns below the playfield instead of vanishing')
  before=page.evaluate("()=>{const T=boss._hammer.throw,g=hammerGripPoint(boss);return{x:T.x,y:T.y,d:Math.hypot(g.x-T.x,g.y-T.y)}}")
  page.evaluate('()=>hammerBossTick(boss,.35)');returnp,ret=snap('archmage_boomerang_06_magnetic_return');after=page.evaluate("()=>{const T=boss._hammer.throw,g=hammerGripPoint(boss);return{x:T.x,y:T.y,d:Math.hypot(g.x-T.x,g.y-T.y)}}")
  moved=((after['x']-before['x'])**2+(after['y']-before['y'])**2)**.5;ok(after['d']<before['d'] and moved<=315*.35+1,'return visibly homes toward the raised hand at the capped medium magnetic speed')
  page.evaluate("()=>{let n=0;while(boss._hammer.state==='throw'&&n++<120)hammerBossTick(boss,.05)}");catchp,catch=snap('archmage_boomerang_07_catch');ok(catch['state']=='hammer' and catch['throw'] is None,'hammer reaches the hand and completes a hard catch without teleport reset')
  shots=[greenp,yellowp,redp,outp,turnp,returnp,catchp]
  for p in shots:
    im=Image.open(p).convert('RGB');ok(im.size==(960,1024) and im.getbbox() is not None,f'{p.stem} is a non-empty native gameplay frame')
  ok(not errors and not page.evaluate('()=>window.__err||null'),'zero Chromium page, console or game-loop errors');br.close()
stop();result={'checks':checks,'errors':errors,'fight':fight,'setup':setup,'green':green,'yellow':yellow,'red':red,'outbound':out,'turn':turn,'return':{'state':ret,'before':before,'after':after,'moved':moved},'catch':catch,'shots':[str(p.relative_to(ROOT)) for p in shots]};(OUT/'results.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8');passed=sum(c['pass'] for c in checks);print(f'{passed} passed / {len(checks)-passed} failed',flush=True)
if passed!=len(checks):raise SystemExit(1)
