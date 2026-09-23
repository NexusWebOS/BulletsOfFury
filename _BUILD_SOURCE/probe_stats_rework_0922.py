from pathlib import Path
import sys,json
sys.path.insert(0,str(Path('_BUILD_SOURCE').resolve()))
from shoot import GAME,serve,SETUP,TRAP_RAF
from playwright.sync_api import sync_playwright
O=Path('_shots/stats_rework_0922');O.mkdir(exist_ok=True);errors=[];r={};port,stop=serve(GAME)
try:
 with sync_playwright() as p:
  b=p.chromium.launch(args=['--no-sandbox','--mute-audio']);pg=b.new_page(viewport={'width':1600,'height':900})
  pg.on('pageerror',lambda e:errors.append(str(e)));pg.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
  pg.goto(f'http://127.0.0.1:{port}/index.html');pg.wait_for_function('()=>(window.__bofFrames|0)>4')
  pg.evaluate(SETUP,{'state':'PLAY','stage':1,'pilot':'yuri','invuln':True})
  pg.evaluate("()=>{Object.assign(stageStats,{kills:178,spawned:200,shots:987654,hits:687321,dmgDealt:18000,deaths:1,livesStart:3,missiles:24,mslHits:20,spShots:10,spHits:9,spDmg:2300,pickups:22,pickupsSeen:25,upgrades:1234,wpn:{'THERMOSHOCK BALL':16000}});run.score=231450;stageTimer=247;setState(GS.STAGECLEAR);}")
  pg.wait_for_timeout(2500);pg.evaluate(TRAP_RAF);pg.wait_for_timeout(60)
  pg.evaluate("()=>{computeStageResults();window.statsBeats=[];const tick=Audio.SFX.statTick;Audio.SFX.statTick=()=>{statsBeats.push(stateT);if(tick)tick();};}")
  def frame(t):return pg.evaluate("t=>{stateT=t;ctx.setTransform(SS,0,0,SS,0,0);drawStageClear(1/60);return {row:drawStageClear._row,stamp:drawStageClear._stamp,fast:drawStageClear._fast,score:drawStageClear._scoreShown};}",t)
  for i in range(160):
   q=frame(i/60)
   if i in [30,60,96,156]:
    r[str(i)]=q;pg.screenshot(path=str(O/('stats_'+str(i)+'.png')))
  r['soundTicks']=pg.evaluate('()=>statsBeats.length')
  r['fits']=pg.evaluate("()=>{const art=curFontArt(),P=scPanelRect();return SC_CONCEPT.map((row,i)=>{const b=scBay(P,scSlots().stats[i]),label=row.k,value=String(row.fmt(stageStats)),lh=scFit(art,label,b[2]*.44,b[3]*.43,P[3]*.009,.05),vh=scFit(art,value,b[2]*.46,b[3]*.54,P[3]*.009,.05);return stageWidth(art,label,lh,.05)+stageWidth(art,value,vh,.05)<=b[2]*.92;});}")
  pg.evaluate('()=>{computeStageResults();Input.injectTap("enter");}');frame(.45)
  r['skip']=pg.evaluate("()=>({fast:drawStageClear._fast,stamp:drawStageClear._stamp,state})")
  # Fresh page restores both the engine and independent HUD animation chains.
  pg.reload();pg.wait_for_function('()=>(window.__bofFrames|0)>4')
  pg.evaluate("()=>{run.mode='campaign';run.pilot='yuri';campaign.unlockedMax=8;openStageSelect(4,{});}")
  pg.wait_for_timeout(1400);pg.screenshot(path=str(O/'connected_clock.png'))
  r['clock']=pg.evaluate("()=>{const c=document.getElementById('wide-clock').getBoundingClientRect(),v=cv.getBoundingClientRect();return {top:c.top,height:c.height,barBottom:v.top+(cmap2BarY()+CM2_BAR.h)*v.height/VH};}")
  r['errors']=errors;b.close()
finally:stop()
(O/'results.json').write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2))
assert not errors and all(r['fits'])
assert r['30']['row']<r['60']['row']<r['96']['row']
assert r['156']['stamp']==1 and r['soundTicks']>8
assert r['skip']['fast'] and r['skip']['stamp']==1 and r['skip']['state']=='stageclear'
assert r['clock']['height']>0 and 0<r['clock']['barBottom']-r['clock']['top']<12
