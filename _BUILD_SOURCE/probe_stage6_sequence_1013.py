"""Native Stage 6 route introduction and solo miniboss regression fixtures."""
from pathlib import Path
import sys,json,base64
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1]
if not (R/'assets/game.js').exists():R=Path('C:/Users/Mike/Desktop/Github Coding/BulletsOfFury')
sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
O=R/'_shots/stage6_sequence_1013';O.mkdir(parents=True,exist_ok=True)
checks=[];rows=[];errors=[]
def check(name,value,data=None):
 checks.append({'name':name,'pass':bool(value),'details':data});print(('PASS ' if value else 'FAIL ')+name,flush=True)
def step(p,n):
 while n:
  count=min(30,n);v=p.evaluate(shoot.STEP,count);assert v is None,v;p.wait_for_timeout(12);n-=count
def capture(p,name):
 p.evaluate('drawWorld(1/60)');raw=p.evaluate('ctx.canvas.toDataURL("image/png")').split(',')[1];(O/(name+'.png')).write_bytes(base64.b64decode(raw))
def setup(p,diff):
 p.evaluate('d=>{diffKey=d;DIFF=DIFFS[d]}',diff)
 assert p.evaluate(shoot.SETUP,{'state':'PLAY','stage':6,'pilot':'axel','invuln':True})['ok']
 p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(6)&&XART.rdy(VP12_ART[6].key)}',timeout=180000)
 p.evaluate('''()=>{story=null;BOFCinematicDirector.cancel();s6Opening=null;fb2Talk=null;run._mission29OpeningDone=true;
  debugFight=null;stagePlan=[];spawnClock=99999;waveIdx=999;warnT=0;run._gp4StageX=null;
  enemies=[];pBullets=[];eBullets=[];boss=null;bossActive=false;bossDefeated=false;bossWarned=false;
  subBoss=null;subBossActive=false;subBossTriggered=true;subBossDone=true;Input.keys={};Input.mouse.down=false;
  stageTimer=curStage.length+.1;mapScroll=2200;player.invuln=1e9+2;player.x=240;player.y=410;H3.release=false;
  s6WingInit();s6WingLaunch(4,true);s6Wing.all=true;s6Wing.beats=3;s6Wing.fakeDone=true;s6Wing.supplyIndex=3;
  s6Wing.postMiniT=4;s6Wing.reinforce=999;s6Wing.choice=true;s6Wing.choiceT=0;VP12.age=11;VP12.next=10;
 }''')
snap='''()=>({scene:!!s6q13Scene(),introDone:!!boss?._rebels?.frIntro?.done,stageTimer,waveIdx,
 vpAge:VP12.age,cpAge:CP12.age,live:enemies.filter(e=>!e.dead).length,shots:eBullets.length,
 allyShots:pBullets.filter(b=>b.ally||b._wingKey).length,wing:s6Wing?.ships.length||0,
 held:!!S6Q13.held,release:H3.release,sub:!!subBossActive,hp:subBoss?.hp,
 forms:VP12.groups.length, introAge:boss?._rebels?.h3Intro?.age||0, route:s6Wing?.route})'''
port,stop=shoot.serve(str(R))
try:
 with sync_playwright() as pw:
  b=pw.chromium.launch(channel='msedge',args=['--mute-audio']);p=b.new_page(viewport={'width':1440,'height':1000})
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text) if m.type=='error' and not m.location.get('url','').endswith('/favicon.ico') else None)
  p.goto(f'http://127.0.0.1:{port}/index.html',timeout=120000);p.wait_for_function('window.__bofFrames>4');p.evaluate(shoot.TRAP_RAF);p.wait_for_timeout(50)
  if not p.evaluate('!!window.BOF_STAGE6_SEQUENCE'):p.add_script_tag(url=f'http://127.0.0.1:{port}/assets/stage6_sequence_1013.js')
  for diff in ['easy','normal','hard','furious']:
   setup(p,diff)
   # The regular campaign route selector receives the real keyboard right action.
   p.keyboard.down('ArrowRight');step(p,4);p.keyboard.up('ArrowRight')
   step(p,18);p.keyboard.down('Enter');step(p,3);p.keyboard.up('Enter')
   selected=p.evaluate('s6Wing.route');check(diff+' native right route selected',selected=='right',selected)
   if selected!='right':
    print(p.evaluate('()=>({state,stage:run.stage,locked:h3Locked(),keybind,story:!!story,opening:!!s6Opening,choice:s6Wing.choice,choiceT:s6Wing.choiceT,t:stageTimer,loop:window.__bofFrames,errors:window.__bofLastError,clock:BOF_COMBAT_CLOCK,cin:BOFCinematicDirector.live,seq:!!wfx?.fseq})'));print(errors)
    raise AssertionError('Keyboard choice failed')
   p.evaluate('s6Wing.routeFightT=32')
   for _ in range(30):
    step(p,15)
    if p.evaluate('!!boss?._rebels'):break
   check(diff+' native route spawns rebel boss',p.evaluate('!!boss?._rebels'))
   # Recreate a formation on screen from the outgoing flight and an overdue queue.
   p.evaluate('''()=>{vp12Spawn('corner');VP12.age=19;VP12.next=10;S6Q13.scene=null;
    eShoot(player.x,80,Math.PI/2,3,'missile');pBullets.push({ally:true,_wingKey:'cole',x:240,y:300,kind:'mg',vx:0,vy:-10});}''')
   step(p,1);initial=p.evaluate(snap);peakEnemies=peakShots=0
   p.evaluate('''()=>{window.__s6qIntro={timer:stageTimer,vp:VP12.age,frames:0,maxEnemies:0,maxShots:0,drift:0};window.__qaTick=()=>{
    if(!s6q13Scene())return;const q=window.__s6qIntro;q.frames++;q.maxEnemies=Math.max(q.maxEnemies,enemies.filter(e=>!e.dead).length);
    q.maxShots=Math.max(q.maxShots,eBullets.length);q.drift=Math.max(q.drift,Math.abs(stageTimer-q.timer),Math.abs(VP12.age-q.vp));};}''')
   check(diff+' outgoing wave and threats cleared immediately',initial['live']==0 and initial['shots']==0 and initial['forms']==0,initial)
   for second in range(75):
    step(p,60);q=p.evaluate(snap)
    if not q['scene']:break
    peakEnemies=max(peakEnemies,q['live']);peakShots=max(peakShots,q['shots'])
    if second==8:capture(p,diff+'-rebel-intro')
   finish=p.evaluate(snap);audit=p.evaluate('window.__s6qIntro');p.evaluate('window.__qaTick=null');rows.append({'difficulty':diff,'introStart':initial,'introEnd':finish,'audit':audit})
   check(diff+' every intro frame free of enemies and live hostile shots',audit['frames']>1500 and audit['maxEnemies']==0 and audit['maxShots']==0,audit)
   check(diff+' intro naturally completes',finish['introDone'] and not finish['scene'],finish)
   check(diff+' stage and formation clocks frozen during intro',audit['drift']<.0001,audit)
   check(diff+' player trigger latch released',not finish['release'])
   p.evaluate('''()=>{window.__s6qFire=pBullets.length;pShoot();window.__s6qPlayable=pBullets.length>window.__s6qFire;}''')
   check(diff+' native player fire resumes',p.evaluate('window.__s6qPlayable'))
   step(p,240);capture(p,diff+'-rebel-combat')
   check(diff+' rebel native combat attacks resume',p.evaluate('!!boss._rebels.gang1004&&boss._rebels.gang1004.age>2'))
   # Native miniboss encounter, retaining the same approach allies and stale shots.
   setup(p,diff)
   p.evaluate('''()=>{s6Wing.choice=false;s6Wing.route=null;stageTimer=25;subBossDone=false;subBossTriggered=true;
    for(const q of s6Wing.ships){q.phase='fight';q.y=VH*.70;q.fcd=0;q.specialCd=0;q.missileCd=0;}
    pBullets.push({ally:true,_wingKey:'cole',kind:'mg',x:240,y:100,vx:0,vy:-10,dmg:99999});
    spawnSubBoss(SUBBOSS[6].kind);window.__miniHP=subBoss.hp;window.__wingDraws=0;window.__wingOld=S6Q13.base.draw;
    S6Q13.base.draw=function(){window.__wingDraws++;return window.__wingOld.apply(this,arguments)};
   }''')
   start=p.evaluate(snap);check(diff+' miniboss removes wing and existing allied shots at spawn',start['held'] and start['wing']==0 and start['allyShots']==0,start)
   for _ in range(10):step(p,60)
   mid=p.evaluate(snap);capture(p,diff+'-solo-miniboss')
   check(diff+' no helper fire or damage throughout miniboss',mid['allyShots']==0 and abs(mid['hp']-start['hp'])<.01,mid)
   check(diff+' no helper sprites rendered during miniboss',p.evaluate('window.__wingDraws===0'))
   check(diff+' solo fight uses neutral ally pressure',p.evaluate('s6PressureMultiplier()===1'))
   # Damage through the native hit owner and advance the full death lifecycle.
   p.evaluate('''()=>{S6Q13.base.draw=window.__wingOld;_dmgBullet=null;for(let i=0;i<40&&!subBoss.dead;i++)hitSubBoss(1e7,subBoss.x,subBoss.y);}''')
   for _ in range(25):
    step(p,30)
    if p.evaluate('subBossDone&&!S6Q13.held'):break
   end=p.evaluate(snap);check(diff+' allies return after actual miniboss defeat',end['wing']>=4 and not end['held'] and not end['sub'],end)
   step(p,120);capture(p,diff+'-wing-return')
   rows[-1]['miniboss']={'start':start,'middle':mid,'end':end}
  b.close()
finally:stop()
report={'checks':checks,'passed':sum(c['pass'] for c in checks),'failed':sum(not c['pass'] for c in checks),'rows':rows,'errors':errors,'scope':'Native Edge frame loop and authored renderer; actual Stage 6 keyboard route choice, complete rebel intro, actual miniboss spawn/hit/death. Controlled invulnerable observation fixtures, not human playthrough.'}
(O/'report.json').write_text(json.dumps(report,indent=2));print(json.dumps({'passed':report['passed'],'failed':report['failed'],'errors':errors}),flush=True)
assert not errors,errors
assert report['failed']==0,report['failed']
