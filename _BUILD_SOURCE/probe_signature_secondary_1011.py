"""Focused native check of the final secondary-attack label correction."""
from pathlib import Path
from playwright.sync_api import sync_playwright
import sys,json
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'_BUILD_SOURCE'));import shoot
OUT=ROOT/'_shots/signature_specials_1011';checks=[];errors=[]
def check(name,yes,data=None):checks.append(dict(name=name,passed=bool(yes),data=data));print(('PASS ' if yes else 'FAIL ')+name,flush=True)
port,stop=shoot.serve(str(ROOT))
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch();p=br.new_page(viewport=dict(width=1100,height=950));p.set_default_timeout(120000)
  p.on('pageerror',lambda e:errors.append(str(e)))
  p.on('console',lambda m:errors.append(m.text) if m.type=='error' or 'draw error' in m.text else None)
  p.on('response',lambda r:errors.append('HTTP '+str(r.status)+': '+r.url) if r.status>=400 else None)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>4');p.evaluate(shoot.TRAP_RAF)
  def frames(n):
   for i in range(0,n,30):
    result=p.evaluate(shoot.STEP,min(30,n-i))
    if result:raise RuntimeError(result)
    p.wait_for_timeout(3)
  p.evaluate(shoot.SETUP,dict(state='PLAY',stage=6,pilot='cole',invuln=True))
  p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(6)}',polling=50)
  p.evaluate('()=>{BOFCinematicDirector.cancel();story=fb2Talk=s6Opening=null;H3.release=false;AP10_X.intro=null;stagePlan=[];enemies=[];spawnClock=9999;subBoss=null;subBossActive=false;subBossDone=true;spawnBoss("rebelsquad");const R=boss._rebels;R.frIntro={done:true};R.h3Intro=null;boss.enter=false;boss._noHit=false;rg4Init(boss);s6WingInit();s6Wing.all=true;s6Wing.supplyIndex=3;player.invuln=1e9;}')
  p.wait_for_function('()=>{rg4Warm();return XART.rdy("ra4_ui")&&XART.rdy("ra7_air")}',polling=50);frames(90)
  p.evaluate('()=>{const R=boss._rebels,G=R.gang1004;for(const q of R.ships){q.rg4.act=null;q.rg4.cd=99;}G.rebelBoxes=[];R.rf.callouts=[];R.rf.comm=null;R.frRadio=null;const v=R.ships.find(q=>q.key==="voss");rg4Attack(v,R,G,"fusion");window.__secondaryPaint=0;const original=campText;campText=function(text){if(text==="FUSION CANNON")window.__secondaryPaint++;return original.apply(this,arguments)};}')
  frames(25)
  q=p.evaluate('()=>({name:boss._rebels.ships[0].rg4.act?._fs11Name,labels:boss._rebels.rf.callouts.map(c=>c.text),paint:window.__secondaryPaint})')
  check('Voss secondary Fusion retains exactly one correct callout',q['name']=='FUSION CANNON' and q['labels'].count('FUSION CANNON')==1 and 'ROOKHOOK' not in q['labels'],q)
  check('The actual campaign font painter renders the Fusion callout without browser errors',q['paint']>0 and not errors,q)
  p.screenshot(path=str(OUT/'rebel-voss-fusion.png'))
  p.evaluate('()=>{coopOn=true;pilotIndex=PILOTS.findIndex(q=>q.key==="cole");p2Index=PILOTS.findIndex(q=>q.key==="falva");run.mode="arcade";startRun(1);BOFCinematicDirector.cancel();story=fb2Talk=s6Opening=null;H3.release=false;stagePlan=[];enemies=[];spawnClock=9999;setState(GS.PLAY);player.invuln=player2.invuln=1e9;}')
  p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(1)&&fs11ArtReady("cole")&&fs11ArtReady("falva")}',polling=50);frames(540)
  p.wait_for_function('()=>Array.from({length:8},(_,i)=>XART.rdy("florb_"+i)).every(Boolean)',polling=50)
  p.evaluate('()=>{window.__seat2BallDraws=0;const get=XART.get,draw=ctx.drawImage;let key;XART.get=function(k){key=k;return get.apply(this,arguments)};ctx.drawImage=function(){if(_seat===2&&key?.startsWith("florb_"))window.__seat2BallDraws++;return draw.apply(this,arguments)};player.invuln=player2.invuln=40002;}');frames(2)
  q=p.evaluate('()=>({p1:special?.pilot,p2:FS11.seat2.special?.pilot,helpers:FS11.seat2.falva.length,draws:window.__seat2BallDraws,dx:Math.abs(FS11.seat2.falva[0]?.x-(player2.x+18)),dy:Math.abs(FS11.seat2.falva[0]?.y-player2.y)})')
  check('P2 Falva keeps her helper alongside P1 Cole after real opening deliveries',q['p1']=='cole' and q['p2']=='falva' and q['helpers']==1,q)
  check('The real world pass paints the authored orbiting ball in P2 seat context',q['draws']>0,q)
  p.screenshot(path=str(OUT/'coop-falva-helper.png'));br.close()
except Exception as e:errors.append(type(e).__name__+': '+str(e));print(errors[-1],flush=True)
finally:
 stop();report=dict(passed=sum(q['passed'] for q in checks),failed=sum(not q['passed'] for q in checks),checks=checks,errors=errors)
 (OUT/'secondary-report.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print(json.dumps(report),flush=True)
sys.exit(1 if errors or report['failed'] else 0)
