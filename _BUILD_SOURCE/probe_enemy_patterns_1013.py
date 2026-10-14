from pathlib import Path
import sys,json,time
from playwright.sync_api import sync_playwright
R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
O=R/'_shots/enemy_patterns_1013';O.mkdir(parents=True,exist_ok=True);errors=[];rows=[];coverage=[]
port,stop=shoot.serve(str(R))
try:
 with sync_playwright() as pw:
  browser=pw.chromium.launch(channel='msedge',args=['--mute-audio']);p=browser.new_page(viewport={'width':1440,'height':1000});p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text) if m.type=='error' and '404' not in m.text else None)
  p.goto(f'http://127.0.0.1:{port}/index.html',timeout=120000);p.wait_for_function('window.__bofFrames>4',timeout=90000);p.evaluate(shoot.TRAP_RAF)
  if not p.evaluate('typeof EP13!=="undefined"'):p.add_script_tag(url=f'http://127.0.0.1:{port}/assets/enemy_patterns_1013.js')
  for stage in [5,7,8,9]:
   p.evaluate(shoot.SETUP,{'state':'PLAY','stage':stage,'pilot':'axel','invuln':True});p.wait_for_function('(n)=>{stageLoadTick();ep13Warm();return stageLoadReady(n)&&ep13ReadyArt()}',arg=stage,timeout=180000)
   p.evaluate('()=>{story=null;debugFight=null;waveIdx=999;spawnClock=9999;subBossTriggered=true;subBossDone=true;subBossActive=false;bossActive=false;warnT=0;if(wfx)wfx.fseq=null;stageTimer=1;VP12.next=9999;CP12.next=9999;EP13.next=0;EP13.clock=2;player.x=camLeftX()+VW*.5;player.y=PLAY.y+PLAY.h*.84;player.invuln=1e9;for(const k in Input.keys)delete Input.keys[k];pBullets=[];eBullets=[];enemies=[];}')
   types=p.evaluate('Object.keys(EP13.families[run.stage])')
   for typ in types:
    c=p.evaluate('type=>{enemies=[];EP13.owner=null;const e=spawnEnemy(type,camLeftX()+VW*.48,PLAY.y+PLAY.h*.24,{});e._ai27={seen:1,visible:true,flinch:0};if(e._mm1003)e._mm1003.phase="rest";e._stagger=0;e._s8Act=null;e._s8Roll=null;return {requested:type,actual:e.type,pattern:e.pattern,eligible:ep13CanStart(e),ground:!!e.ground,dead:!!e.dead};}',typ);coverage.append(c);print('coverage',stage,c,flush=True)
   # One real controller fixture per difficulty, rotating attack families by stage.
   pattern={5:'sweep',7:'rifle',8:'ring',9:'shards'}[stage];typ={5:'s5frigate',7:'mm1003_riflelocust',8:'s8deathorb',9:'s9beacon'}[stage]
   for difficulty in ['easy','normal','hard','furious']:
    p.evaluate('c=>{diffKey=c.d;DIFF=DIFFS[c.d];enemies=[];eBullets=[];pBullets=[];EP13.events=[];EP13.owner=null;EP13.clock=10;EP13.next=0;player.dead=false;player.invuln=1e9;player.x=camLeftX()+VW*.5;player.y=PLAY.y+PLAY.h*.84;window.ep13Fixture=spawnEnemy(c.type,camLeftX()+VW*.48,PLAY.y+PLAY.h*.24,{});const e=ep13Fixture;e.hp=e.maxhp=50000;e._ai27={seen:1,visible:true,flinch:0};if(e._mm1003)e._mm1003.phase="rest";e._stagger=0;e._s8Act=null;e._s8Roll=null;ep13Start(e,c.pattern);}',{'type':typ,'pattern':pattern,'d':difficulty})
    # Native update/draw with invulnerability only for capture. Collision geometry is checked separately.
    frames=[];peak=0
    for i in range(10):
     t=time.perf_counter();err=p.evaluate(shoot.STEP,24);frames.append((time.perf_counter()-t)*1000/24);assert not err,err;p.wait_for_timeout(10);peak=max(peak,p.evaluate('eBullets.filter(b=>b._ep13&&!b.dead).length'))
     if i in [1,3,5] and difficulty in ['normal','furious']:p.screenshot(path=str(O/f's{stage}-{difficulty}-{pattern}-{i}.png'))
    row=p.evaluate('()=>({events:EP13.events,finite:enemies.every(e=>Number.isFinite(e.x)&&Number.isFinite(e.y)),state,beamGone:!ep13Beam(ep13Fixture),owner:!!EP13.owner,frameT:ep13Fixture._ep13?.t})');row.update(stage=stage,difficulty=difficulty,pattern=pattern,peakProjectiles=peak,meanStepMs=sum(frames)/len(frames));rows.append(row);assert row['finite'] and row['state']=='play',row;assert any(e['event']=='release' for e in row['events']),row;print('fixture',stage,difficulty,pattern,peak,round(row['meanStepMs'],2),flush=True)
   # Destroying the actual weapon rig / hull immediately removes owned beam damage.
   clean=p.evaluate('()=>{const e=ep13Fixture;EP13.owner=null;ep13Start(e,"charge");e._ep13.t=e._ep13.profile.tell+.3;e._ep13.phase="fire";const live=ep13Alive(e);e._dyingT=.01;ep13Tick(e,1/60);const gone=!ep13Beam(e)&&!e._ep13;return {live,gone};}');assert clean['live'] and clean['gone'],clean
  # Exhaustive configured geometry: broad safe escape sector and both sweep edges.
  geometry=p.evaluate('()=>{const rows=[];for(const [difficulty,P] of Object.entries(EP13.profiles)){const q={profile:P,beat:0,gap:Math.PI/2};const angles=ep13RingAngles(q);const ringClear=angles.every(a=>Math.abs(Math.atan2(Math.sin(a-q.gap),Math.cos(a-q.gap)))>P.gap*.5);const minPassage=2*Math.sin(P.gap*.5)*100-24;rows.push({difficulty,ringClear,minPassage,sweepSpeed:P.sweep,warning:P.tell,missileFanWidth:(P.missiles-1)*.22});}return rows;}');assert all(r['ringClear'] and r['minPassage']>75 for r in geometry),geometry
  browser.close()
finally:stop()
result={'fixtures':rows,'coverage':coverage,'geometry':geometry,'errors':errors}
(O/'verification.json').write_text(json.dumps(result,indent=2));assert not errors,errors
print('PASS',len(rows),'native difficulty fixtures',len(coverage),'family ownership samples',flush=True)
