"""Inspect the remaining Normal miniboss and completion routes in Chromium."""
from pathlib import Path
import sys,json
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'_BUILD_SOURCE'));import shoot
OUT=ROOT/'_shots/audio_1010';checks=[];errors=[]
def check(name,passed,data=None):
 checks.append(dict(name=name,passed=bool(passed),data=data));print(('PASS ' if passed else 'FAIL ')+name,flush=True)
 if not passed:print(json.dumps(data),flush=True)
port,stop=shoot.serve(str(ROOT))
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(args=['--autoplay-policy=no-user-gesture-required']);p=br.new_page(viewport=dict(width=1280,height=900));p.set_default_timeout(120000)
  p.on('pageerror',lambda e:errors.append(str(e)))
  p.on('console',lambda m:errors.append(m.text[:800]) if m.type=='error' or 'draw error' in m.text else None)
  p.on('response',lambda r:errors.append('HTTP '+str(r.status)+': '+r.url) if r.status>=400 else None)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>4');p.evaluate(shoot.TRAP_RAF);p.mouse.click(650,450)
  def frames(n):
   for i in range(0,n,30):
    e=p.evaluate(shoot.STEP,min(30,n-i))
    if e:errors.append(e);break
    p.wait_for_timeout(4)
  def scene(n):
   p.evaluate('()=>{run.mode="arcade";delete run._gp4StageX;}');p.evaluate(shoot.SETUP,dict(state='PLAY',stage=n,pilot='yuri',invuln=True))
   p.wait_for_function('n=>{stageLoadTick();return stageLoadInfo(n).ready}',arg=n,polling=50)
   p.evaluate('()=>{BOFCinematicDirector.cancel();story=null;H3.ending=null;H3.release=false;stagePlan=[];enemies=[];pBullets=[];eBullets=[];subBoss=null;subBossActive=false;subBossDone=true;boss=null;bossActive=false;special=null;fb2Talk=null;s6Opening=null;}')
  scene(2);p.evaluate("spawnSubBoss('magmaward')");frames(240)
  q=p.evaluate('()=>({reaver:av3Reaver(subBoss),book:er26Book(subBoss),parts:subBoss._av3Reaver?.parts.length})')
  check('Healthy twin-turret miniboss favors charged lasers over magma bombardment',q['reaver'] and q['parts']==6 and 'ember-mortar' not in q['book'] and 'ember-bombard' not in q['book'],q)
  p.evaluate("()=>{subBoss.enter=false;er26Set(subBoss,'furnace-lance');}");frames(210)
  q=p.evaluate('()=>({beam:subBoss._l23Beam,draws:AV3?.draws})')
  beam=q['beam']
  check('Normal twin-turret miniboss releases its widened charged beam',beam is not None and beam.get('width',0)>=32 and beam.get('released') and beam['warm']<=beam['t']<beam['warm']+beam['active'],q)
  p.screenshot(path=str(OUT/'stage2-miniboss-beam.png'))
  p.evaluate('()=>{subBoss.hp=subBoss.maxhp*.3;}')
  q=p.evaluate('er26Book(subBoss)');check('Magma bombardment returns in the damaged miniboss state','ember-mortar' in q and 'ember-bombard' in q,q)
  scene(5);p.evaluate("spawnSubBoss('spacebomber')");frames(220)
  p.evaluate('()=>{window.ap10BomberStartX=subBoss.x;}');frames(1800)
  q=p.evaluate('()=>({space:subBoss._bomber.space,parts:siegeBomberParts(subBoss).map(q=>q.id),history:subBoss._bomber.history,x:subBoss.x,start:ap10BomberStartX})')
  check('Existing space miniboss remains modular and cycles pursuit attacks',q['space'] and len(q['parts'])>=5 and {'hc-lances','hc-cross','hc-strafe'}.issubset(set(q['history'])),q)
  p.screenshot(path=str(OUT/'space-miniboss-active.png'))
  scene(6);p.evaluate('()=>{flyoverStartX=player.x;flyoverStartY=player.y;flyoverT=0;setState(GS.FLYOVER);window.ap10ExitStart={x:player.x,y:player.y};}')
  frames(270);q=p.evaluate('()=>({x:player.x,y:player.y,start:ap10ExitStart,state})')
  check('Completion flies the real ship straight north at its normal scale',abs(q['x']-q['start']['x'])<.01 and q['y']<q['start']['y'],q)
  p.screenshot(path=str(OUT/'stage6-completion-flight.png'))
  p.evaluate('()=>{setState(GS.STAGECLEAR);drawStageClear._init=false;}');frames(180)
  p.wait_for_function("()=>XART.rdy('statpanel_full_0916')",polling=50)
  q=p.evaluate("()=>{const a=XART.get('statpanel_full_0916');return{art:a.width/a.height,view:cutsceneViewWidth()/VH};}")
  check('Completion panel uses the authored aspect instead of stretching',abs(q['art']-q['view'])<.005,q)
  p.screenshot(path=str(OUT/'stage6-completion-panel.png'))
  check('No page, console or asset errors',not errors,errors);br.close()
finally:stop()
report=dict(passed=sum(q['passed'] for q in checks),failed=sum(not q['passed'] for q in checks),checks=checks,errors=errors)
(OUT/'finishing-report.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print(json.dumps(dict(passed=report['passed'],failed=report['failed'],errors=errors)),flush=True)
sys.exit(1 if report['failed'] else 0)
