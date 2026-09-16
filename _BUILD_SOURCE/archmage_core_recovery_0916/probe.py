"""Real Chromium proof for the Stage-5 Archmage Easy/Normal core recovery."""
from pathlib import Path
import base64,http.server,json,sys
from PIL import Image
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'_shots'/'archmage_core_recovery_0916';OUT.mkdir(parents=True,exist_ok=True)
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
  keys=['arch_chaingun_break_enrage','arch_effects','arch_dual_uzi_assault']+[f'bmfx_{kind}_{col}_{tail}' for col in ('green','yellow','red') for kind,tail in (('fov','tall'),('alert','danger'))]
  setup=page.evaluate("""ks=>{__auto=function(){};story=null;dlgBox=function(){};stagePlan=[];waveIdx=0;enemies=[];eBullets=[];pBullets=[];particles=[];powerups=[];playerLocks=[];state=GS.PLAY;stateT=999;run.stage=5;curStage=STAGES[4];camX=0;player.x=360;player.y=430;player.invuln=999;player.dead=false;player.alive=true;diffKey='normal';DIFF=DIFFS.normal;boss=null;bossActive=false;spawnBoss('xenoregent');boss.enter=false;boss.x=104;boss.y=286;boss._drawY=boss.y;boss._noHit=false;bossActive=true;boss._combatWarnings={};const h=boss._hammer;h.state='chaingun';h.mode='chaingun';h.chainHP=1;boss._hammerModuleHit='chaingun';hammerBossDamage(boss,2);window.__archCoreGets=[];const g=XART.get.bind(XART);XART.get=function(k){window.__archCoreGets.push(k);return g(k)};ks.forEach(k=>XART.rdy(k));return{name:boss.name,state:h.state,mode:h.mode,chainDestroyed:h.chainDestroyed,hammerDestroyed:h.hammerDestroyed,x:boss.x,y:boss.y};}""",keys)
  ok(setup['name']=='CHROME HAMMER ARCHMAGE' and setup['state']=='core_orbit' and setup['mode']=='core' and setup['chainDestroyed'] and setup['hammerDestroyed'],'destroying the Normal chaingun enters the live core-recovery phase and retires obsolete module targets')
  ready=False
  for _ in range(280):
    ready=page.evaluate('ks=>ks.every(k=>XART.rdy(k))',keys)
    if ready:break
    page.wait_for_timeout(35)
  ok(ready,'authored break, core-effect and dual-Uzi art decode before capture')
  def advance(dt):page.evaluate('dt=>{hammerBossTick(boss,dt);boss.flash=0;stateT+=dt;}',dt)
  def snap(name):
    page.evaluate('()=>{shake=0;window.__archCoreGets=[];drawWorld(0)}')
    data=page.evaluate("""()=>{const h=boss._hammer,W=boss._combatWarnings&&boss._combatWarnings['archmage-fused-wave'];return{state:h.state,t:h.t,mode:h.mode,coreAngle:h.coreAngle,x:boss.x,y:boss.y,shotCd:h.shotCd,warn:W&&{t:W.t,warm:W.warm,released:W.released},gets:Array.from(new Set(window.__archCoreGets))}}""")
    raw=page.evaluate("()=>document.querySelector('#screen').toDataURL('image/png').split(',')[1]");p=OUT/f'{name}.png';p.write_bytes(base64.b64decode(raw));return p,data
  advance(.08);p1,d1=snap('archmage_core_01_break')
  ok(d1['state']=='core_orbit' and 'arch_chaingun_break_enrage' in d1['gets'] and 'arch_effects' in d1['gets'],'the break frame uses the authored body reel and core-effect atlas')
  advance(.72);p2,d2=snap('archmage_core_02_orbit')
  ok(d2['state']=='core_orbit' and d2['coreAngle']>d1['coreAngle'] and d2['x']>d1['x'] and d2['y']<d1['y'],'the visible core orbit accelerates while the boss returns to its fighting anchor')
  advance(.78);p3,d3=snap('archmage_core_03_converge')
  ok(d3['state']=='core_orbit' and d3['coreAngle']>d2['coreAngle'],'the authored cores keep orbiting through the late convergence instead of freezing')
  advance(.62);p4,d4=snap('archmage_core_04_uzi_release')
  ok(d4['state']=='uzi' and d4['mode']=='core' and 'arch_dual_uzi_assault' in d4['gets'],'the finite transition releases into the authored dual-Uzi final form')
  page.evaluate("()=>{boss._hammer.t=4.39;boss._hammer.shotCd=.5;hammerBossTick(boss,.02);stateT+=.02}");advance(.25);p5,d5=snap('archmage_core_05_green')
  ok(d5['state']=='mega_charge' and 'bmfx_fov_green_tall' in d5['gets'] and 'bmfx_alert_green_danger' in d5['gets'],'the Normal final-form loop reaches a green shared mega-wave warning')
  advance(.55);p6,d6=snap('archmage_core_06_yellow')
  ok(d6['state']=='mega_charge' and d6['warn'] and not d6['warn']['released'] and 'bmfx_fov_yellow_tall' in d6['gets'],'the mega-wave corridor advances to yellow before release')
  advance(.45);p7,d7=snap('archmage_core_07_red')
  ok(d7['state']=='mega_charge' and not d7['warn']['released'] and 'bmfx_fov_red_tall' in d7['gets'],'the mega-wave corridor reaches red while the attack is still harmless')
  advance(.42);p8,d8=snap('archmage_core_08_mega_beam')
  ok(d8['state']=='mega_beam' and d8['warn']['released'],'the final form releases its mega beam only after the red warning')
  page.evaluate("()=>{boss._hammer.t=6.99;hammerBossTick(boss,.02);stateT+=.02}");p9,d9=snap('archmage_core_09_loop')
  ok(d9['state']=='uzi' and d9['mode']=='core','the Normal final form loops back into dual-Uzi pressure instead of stalling')
  shots=[p1,p2,p3,p4,p5,p6,p7,p8,p9]
  for p in shots:
    im=Image.open(p).convert('RGB');ok(im.size==(960,1024) and im.getbbox() is not None,f'{p.stem} is a non-empty native gameplay frame')
  ok(not errors and not page.evaluate('()=>window.__err||null'),'zero Chromium page, console or game-loop errors');br.close()
stop();result={'checks':checks,'errors':errors,'fight':fight,'setup':setup,'frames':[d1,d2,d3,d4,d5,d6,d7,d8,d9],'shots':[str(p.relative_to(ROOT)) for p in shots]};(OUT/'results.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8');passed=sum(c['pass'] for c in checks);print(f'{passed} passed / {len(checks)-passed} failed',flush=True)
if passed!=len(checks):raise SystemExit(1)
