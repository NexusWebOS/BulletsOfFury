"""Native terrain motion and preserved encounter gates for the flight balance pass."""
from pathlib import Path
import sys,json
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1]
O=R/'_shots/formation_scroll_1013';O.mkdir(exist_ok=True)
sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
rows=[];checks=[];errors=[];port,stop=shoot.serve(str(R))
def check(name,value,details=None):
 checks.append({'name':name,'pass':bool(value),'details':details})
 print(('PASS ' if value else 'FAIL ')+name,flush=True)
def step(p,n):
 while n:
  m=min(30,n);r=p.evaluate(shoot.STEP,m);assert r is None,r;p.wait_for_timeout(15);n-=m
snap='()=>({stage:run.stage,map:mapScroll,src:levelSrcY(),sky:_stage6SkyScroll,airbase:LA1007.scroll,hold:_s1GroundHold,bossHold:_bossHold,live:enemies.filter(e=>!e.dead).length,formations:enemies.filter(e=>e._vp12).length,ambushes:enemies.filter(e=>e._cp12).length,waveIdx,state,story:!!story,bossActive,subBossActive})'
def setup(p,stage,diff):
 p.evaluate('d=>{diffKey=d;DIFF=DIFFS[d]}',diff);p.evaluate(shoot.SETUP,{'state':'PLAY','stage':stage,'pilot':'axel','invuln':True})
 p.wait_for_function('(n)=>{stageLoadTick();return stageLoadReady(n)&&XART.rdy(stageMasterKey(_levelCfg()))&&(!VP12_ART[n]||XART.rdy(VP12_ART[n].key))}',arg=stage,timeout=120000)
 p.evaluate('()=>{story=null;BOFCinematicDirector.cancel();s6Opening=null;s6Wing=null;run._mission29OpeningDone=true;debugFight=null;waveIdx=999;spawnClock=9999;subBossTriggered=true;subBossDone=true;subBossActive=false;bossActive=false;warnT=0;if(wfx)wfx.fseq=null;stageTimer=1;VP12.next=9999;CP12.next=9999;run.shield=5;Input.keys={};Input.mouse.down=false;player.invuln=1e9+2;enemies=[];eBullets=[];pBullets=[];VP12.groups=[];_s1GroundHold=false;_bossHold=0;mapScroll=180;}')
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',args=['--mute-audio']);p=b.new_page(viewport={'width':1440,'height':1000})
 p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text) if m.type=='error' and '404' not in m.text else None)
 p.goto(f'http://127.0.0.1:{port}/index.html',timeout=120000);p.wait_for_function('window.__bofFrames>4');p.evaluate(shoot.TRAP_RAF);p.wait_for_timeout(50)
 for stage in [1,2,4,6,8]:
  for diff in ['easy','normal','hard','furious']:
   setup(p,stage,diff)
   p.evaluate('()=>{if(VP12_ART[run.stage])vp12Spawn("orbit");if([1,2].includes(run.stage))cp12Ambush();}')
   step(p,2);a=p.evaluate(snap);step(p,120);z=p.evaluate(snap)
   row={'kind':'formations_scroll','stage':stage,'difficulty':diff,'start':a,'end':z};rows.append(row)
   check(f'stage{stage} {diff} formations and ambushes retain terrain travel',z['map']-a['map']>79,row)
   if stage==6:check(f'stage6 {diff} sky retains cruise',z['sky']-a['sky']>1470)
   if diff=='furious':p.screenshot(path=str(O/f'stage{stage}-moving.png'))
 for diff in ['easy','normal','hard','furious']:
  setup(p,1,diff)
  meta=p.evaluate('()=>{const idx=stagePlan.findIndex(w=>w.fn?._s1Ground),w=stagePlan[idx],cfg=_levelCfg();waveIdx=idx;mapScroll=Math.max(w.fn._s1MapScroll,(cfg.h||4212)-S1_COAST+100);stageTimer=mapScroll/40;_waveGap=0;vp12Spawn("orbit");cp12Ambush();const pressure=w.fn._s1Pressure||4;const threshold=stageAiProfile(1).cap-pressure;while(enemies.filter(e=>!e.dead).length<=threshold)spawnEnemy("s1jetdelta",camLeftX()+viewW()*.5,PLAY.y+100,{shoots:false,route:"straight"});return {idx,threshold,pressure,sourceBottom:(cfg.h||4212)-mapScroll,landThreshold:S1_COAST-60,live:enemies.length}}')
  a=p.evaluate(snap);step(p,90);z=p.evaluate(snap)
  check(f'{diff} density-blocked ground wave does not stop scroll',z['map']-a['map']>59,{'meta':meta,'start':a,'end':z})
  check(f'{diff} ground wave waits for pressure clearance',z['waveIdx']==meta['idx'],z)
  if diff=='furious':p.screenshot(path=str(O/'ground-queue-moving.png'))
  p.evaluate('()=>{for(const e of enemies)e.dead=true;eBullets=[];VP12.groups=[];_waveGap=0;}');step(p,2)
  dispatch=p.evaluate('()=>({waveIdx,ground:enemies.filter(e=>!e.dead&&e._tank).map(e=>({type:e.type,x:e.x,y:e.y,hp:e.hp})),types:enemies.filter(e=>!e.dead).map(e=>e.type),mapScroll})')
  check(f'{diff} queued ground wave dispatches after pressure clears',dispatch['waveIdx']==meta['idx']+1 and len(dispatch['ground'])>=2,dispatch)
  rows.append({'kind':'ground_queue','difficulty':diff,'before':a,'after':z,'dispatch':dispatch,'meta':meta})
 for role in ['mini','boss']:
  setup(p,1,'normal');p.evaluate('(role)=>{on5LaunchEncounter({stage:1,role});story=null;fb2Talk=null;H3.release=false;}',role);step(p,75)
  a=p.evaluate(snap);step(p,60);z=p.evaluate(snap)
  check(f'actual stage1 {role} encounter still holds its terrain',abs(z['map']-a['map'])<.01 and z['bossHold']==1,{'before':a,'after':z})
  p.screenshot(path=str(O/f'{role}-native-hold.png'));rows.append({'kind':'encounter_hold','role':role,'start':a,'end':z})
 b.close();stop()
report={'checks':checks,'passed':sum(c['pass'] for c in checks),'failed':sum(not c['pass'] for c in checks),'rows':rows,'errors':errors,'scope':'Native Edge render loop; controlled enemy/campaign fixtures; no claims about human survival or complete campaign clear.'}
(O/'report.json').write_text(json.dumps(report,indent=2));assert not errors,errors;assert report['failed']==0,report['failed']
