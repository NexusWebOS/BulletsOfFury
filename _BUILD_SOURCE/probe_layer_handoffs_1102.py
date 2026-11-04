from pathlib import Path
import json,sys,math
from playwright.sync_api import sync_playwright
R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');W=Path(__file__).parent
sys.path.insert(0,str(R/'_BUILD_SOURCE'));from shoot import serve,TRAP_RAF
checks=[];errors=[]
def ck(n,v,d=None):
 checks.append({'name':n,'passed':bool(v),'data':d});(W/'handoff-checks.json').write_text(json.dumps(checks,indent=2));print('PASS' if v else 'FAIL',n,str(d)[:900] if not v else '',flush=True);assert v,(n,d)
setup='''n=>{EA11.setup(n,'furious');stagePlan=[];waveIdx=0;subBossTriggered=subBossDone=aminiTriggered=true;bossWarned=true;boss=null;subBoss=null;bossActive=subBossActive=false;DBGT.god=true;player.invuln=1e9;stageTimer=0;_adaptiveSpawnT=99999;CP12.next=VP12.next=CP22.nextWave=CP22.nextFlyby=99999;enemies=[];eBullets=[];pBullets=[];powerups=[];player.x=worldWidth()/2;player.y=VH-65;camX=Math.max(0,player.x-VW/2);}'''
port,stop=serve(str(R))
try:
 with sync_playwright() as pw:
  b=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required']);p=b.new_page(viewport={'width':1280,'height':900});p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:500]) if m.type=='error' or 'draw error' in m.text else None)
  p.goto(f'http://127.0.0.1:{port}/index.html',wait_until='load',timeout=180000);p.wait_for_function('window.__bofFrames>4');p.mouse.click(3,3);p.evaluate(TRAP_RAF);p.add_script_tag(path=str(R/'_BUILD_SOURCE/enemy_behaviour_lab_1011.js'))
  p.evaluate(setup,4);p.wait_for_function('()=>{stageLoadTick();hm17Warm();return stageLoadReady(4)&&ls112Keys(4).every(k=>XART.rdy(k))}',timeout=180000)
  q=p.evaluate('''()=>{let drift=0;for(let i=0;i<600;i++){updatePlay(1/60);ctx.setTransform(SS,0,0,SS,0,0);window.__bofFrames++;drawWorld(1/60);for(const e of enemies)if(e._hm17?.phase==='loaded')drift=Math.max(drift,Math.abs(e.y+46-e._hm17.anchor-LA1007.scroll));}return {map:mapScroll,visual:LA1007.scroll,spawns:HM17.events.filter(e=>e.event==='pad-spawn'),next:HM17.next,drift};}''')
  ck('Stage4 native roadside weapon director still launches its original cadence',len(q['spawns'])>=1 and len(q['spawns'])<=3 and q['next']>q['map'],q)
  ck('Roadside weapons remain exactly anchored to the new terrain',q['drift']<.01,q)
  q=p.evaluate('''()=>{mapScroll=levelScrollRange();LS112.chaseTravel=0;boss={dead:false,_s4war:{mode:'swerve'}};bossActive=true;const sources=[],deltas=[];for(let i=0;i<400;i++){ls112Road(1/60);sources.push(_masterSrcY);deltas.push(_groundDy);}return {source:sources.at(-1),monotonic:sources.every((s,i)=>!i||s<sources[i-1]),maxDelta:Math.max(...deltas.slice(1)),drive:tankDrivable(340,-100,false),blocked:tankDrivable(20,-100,false)};}''')
  ck('Highway chase continues forward through repeated source boundaries',q['monotonic'] and q['source']<-2000 and q['maxDelta']<12,q)
  ck('Chase road remains navigable without opening desert shoulders',q['drive'] and not q['blocked'],q)
  p.locator('#screen').screenshot(path=str(W/'stage4-highway-live.png'))
  p.evaluate(setup,6);p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(6)}',timeout=180000)
  q=p.evaluate('''()=>{const map=mapScroll,draws=LS112.draws['city-transition']||0;ctx.setTransform(SS,0,0,SS,0,0);stage6TransitionBackgroundDraw(220);return {map,after:mapScroll,draws:(LS112.draws['city-transition']||0)-draws};}''');ck('Stage6 arrival uses the new city without advancing encounter distance',q['draws']==1 and q['map']==q['after'],q)
  p.evaluate('()=>{run._gp4StageX={review:true};ls112Warm("X")}');p.wait_for_function('()=>ls112Keys("X").every(k=>XART.rdy(k))',timeout=180000)
  q=p.evaluate('''()=>{const draws=LS112.draws['stage-X']||0;ctx.setTransform(SS,0,0,SS,0,0);drawBG(1/60);return (LS112.draws['stage-X']||0)>draws;}''');ck('Actual alternate-route background dispatch reaches Stage X layers',q)
  p.locator('#screen').screenshot(path=str(W/'stage-X-live.png'))
  p.evaluate(setup,8);p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(8)}',timeout=180000)
  q=p.evaluate('''()=>{const d=LS112.draws['stage-8']||0;l78EntryStart();ctx.setTransform(SS,0,0,SS,0,0);drawL78Entry(0);return {draws:(LS112.draws['stage-8']||0)-d,material:LS112.clock.bed?.name};}''');ck('Stage8 portal arrival shows the same new biome and biofluid',q['draws']>0 and q['material']=='biofluid',q)
  for n in [5,9]:
   p.evaluate(setup,n);p.wait_for_function('n=>{stageLoadTick();return stageLoadReady(n)}',arg=n,timeout=180000)
   q=p.evaluate('''()=>{const list=enemies.slice(),targets=retinaBossTargets(boss)||[];for(let i=0;i<60;i++)drawBG(1/60);return {same:enemies.length===list.length&&enemies.every((e,i)=>e===list[i]),objects:LS112_ART.levels[String(run.stage)].passive};}''');ck('Stage'+str(n)+' scenery remains passive and untargetable',q['same'] and q['objects'],q)
  p.evaluate(setup,3);p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(3)}',timeout=180000)
  q=p.evaluate('''()=>{const cfg=_levelCfg(),a=LS112_ART.materials[cfg.liquid.slice(6)];for(let i=0;i<45;i++)updatePlay(1/60);const t=efxClock;setState(GS.PAUSE);for(let i=0;i<10;i++)drawWorld(0);return {same:efxClock===t,frame:LS112.clock.bed?.frame,expected:Math.floor(t*a.fps)%a.frames};}''');ck('Pause holds the authored liquid animation phase',q['same'] and q['frame']==q['expected'],q)
  ck('No native browser/render exceptions during handoffs',not errors,errors);b.close()
 print('RESULT',len(checks),'passed',flush=True)
finally:stop()
