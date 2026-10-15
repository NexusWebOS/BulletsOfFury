from pathlib import Path
import sys,json,time
from playwright.sync_api import sync_playwright
R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
O=R/'_shots/enemy_patterns_1013';O.mkdir(parents=True,exist_ok=True);errors=[];rows=[];port,stop=shoot.serve(str(R))
try:
 with sync_playwright() as pw:
  browser=pw.chromium.launch(channel='msedge',args=['--mute-audio']);p=browser.new_page(viewport={'width':1440,'height':1000});p.on('pageerror',lambda e:errors.append(str(e)))
  p.goto(f'http://127.0.0.1:{port}/index.html',timeout=120000);p.wait_for_function('window.__bofFrames>4',timeout=90000);p.evaluate(shoot.TRAP_RAF)
  if not p.evaluate('typeof EP13!=="undefined"'):p.add_script_tag(url=f'http://127.0.0.1:{port}/assets/enemy_patterns_1013.js')
  for stage in [5,7,8,9]:
   for difficulty in ['normal','furious']:
    p.evaluate('d=>{diffKey=d;DIFF=DIFFS[d]}',difficulty);p.evaluate(shoot.SETUP,{'state':'PLAY','stage':stage,'pilot':'cole','invuln':True});p.wait_for_function('(n)=>{stageLoadTick();ep13Warm();return stageLoadReady(n)&&ep13ReadyArt()}',arg=stage,timeout=180000)
    p.evaluate('()=>{story=null;debugFight=null;subBossTriggered=true;subBossDone=true;subBossActive=false;bossActive=false;warnT=0;if(wfx)wfx.fseq=null;player.invuln=1e9;for(const k in Input.keys)delete Input.keys[k];EP13.events=[];}')
    peak=0;ms=[]
    for i in range(45):
     t=time.perf_counter();err=p.evaluate(shoot.STEP,40);ms.append((time.perf_counter()-t)*1000/40);assert not err,err;p.wait_for_timeout(5);peak=max(peak,p.evaluate('eBullets.filter(b=>!b.dead).length'))
    row=p.evaluate('()=>({stage:run.stage,difficulty:diffKey,elapsed:stageTimer,events:EP13.events,finite:enemies.every(e=>Number.isFinite(e.x)&&Number.isFinite(e.y)),state})');row.update(peakBullets=peak,meanFrameMs=sum(ms)/len(ms));rows.append(row);print('live',stage,difficulty,len([e for e in row['events'] if e['event']=='start']),round(row['meanFrameMs'],2),flush=True);assert row['finite'],row
    p.screenshot(path=str(O/f'live-s{stage}-{difficulty}.png'))
  # Specific weapon destruction, recovery and true native co-op seat swapping.
  p.evaluate(shoot.SETUP,{'state':'PLAY','stage':7,'pilot':'cole','invuln':True});p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(7)}',timeout=180000)
  checks=p.evaluate('''()=>{
   story=null;debugFight=null;subBossActive=bossActive=false;warnT=0;enemies=[];pBullets=[];eBullets=[];if(wfx)wfx.fseq=null;EP13.owner=null;EP13.next=0;EP13.clock=3;
   const e=spawnEnemy('mm1003_riflelocust',camLeftX()+VW*.5,PLAY.y+120,{});e._mm1003.phase='rest';e.hp=e.maxhp=50000;e._ai27={seen:1,visible:true,flinch:0};e.shoots=true;player.dead=false;player.x=e.x;player.y=PLAY.y+PLAY.h*.83;player.invuln=1e9;
   ep13Start(e,'rifle');e._ep13.phase='fire';e._ep13.t=e._ep13.profile.tell+.4;const armed=e._ep13.kind==='rifle';e._mm1003.parts.filter(p=>p.kind==='gun').forEach(p=>p.dead=true);const destroyedEmitterSilent=ep13Disarmed(e)&&!ep13Beam(e);ep13Tick(e,.016);const cancelled=!e._ep13,shootsRestored=e.shoots===true;
   e._mm1003.parts.filter(p=>p.kind==='gun').forEach(p=>p.dead=false);ep13Start(e,'rifle');e._ep13.t=20;ep13Tick(e,.016);const recovered=!e._ep13;EP13.next=999;e._ep13Next=999;e._mm1003.cd=0;for(let i=0;i<150;i++){EP13.clock+=1/60;mm1003Tick(e,1/60);}const nativeResumed=e._mm1003.phase!=='rest'||e._mm1003.fired>0;
   const be=spawnEnemy('s5frigate',camLeftX()+VW*.5,PLAY.y+120,{});ep13Start(be,'charge');be._ep13.phase='fire';be._ep13.t=be._ep13.profile.tell+.4;be._ep13.angle=Math.PI/2;const beam=ep13Beam(be);
   coopOn=true;for(const f of SEAT_RUN_FIELDS)run2[f]=run[f];run.shield=2;run2.shield=2;player.dead=false;player.invuln=0;player.x=camLeftX()+35;player.y=PLAY.y+PLAY.h*.8;player2.dead=false;player2.alive=true;player2.invuln=0;player2.x=beam.x;player2.y=player.y;run._megaShield=null;run2._megaShield=null;
   ep13HitSeats();const p2HitOnly=run.shield===2&&run2.shield===1;ep13HitSeats();const invulnRespected=run2.shield===1,seatRestored=_seat===1;coopOn=false;
   warnT=1;ep13Tick(be,.016);const transitionSilent=!ep13Beam(be)&&!be._ep13;warnT=0;
   return {armed,destroyedEmitterSilent,cancelled,shootsRestored,recovered,nativeResumed,p2HitOnly,invulnRespected,seatRestored,transitionSilent};
  }''');print('checks',checks,flush=True);assert all(checks.values()),checks
  browser.close()
finally:stop()
(O/'live-verification.json').write_text(json.dumps({'rows':rows,'checks':checks,'errors':errors},indent=2));assert not errors,errors
assert all(any(e['event']=='start' for e in row['events']) for row in rows),rows
print('PASS native scheduled waves, recovery, weapon destruction, co-op and transition safety',flush=True)
