"""Render-only scene hygiene and the neighboring Stage 6 native radio scenes."""
from pathlib import Path
import sys,json,base64
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1]
if not (R/'assets/game.js').exists():R=Path('C:/Users/Mike/Desktop/Github Coding/BulletsOfFury')
sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
O=R/'_shots/stage6_sequence_1013';O.mkdir(parents=True,exist_ok=True)
checks=[];errors=[];rows=[]
def check(name,value,data=None):
 checks.append({'name':name,'pass':bool(value),'details':data});print(('PASS ' if value else 'FAIL ')+name,flush=True)
def step(p,n):
 while n:
  m=min(30,n);v=p.evaluate(shoot.STEP,m);assert v is None,v;p.wait_for_timeout(12);n-=m
def capture(p,name):
 p.evaluate('drawWorld(1/60)');raw=p.evaluate('ctx.canvas.toDataURL("image/png")').split(',')[1];(O/(name+'.png')).write_bytes(base64.b64decode(raw))
def seed(p):
 p.evaluate('''()=>{S6Q13.scene=null;spawnEnemy('s6dart',240,100,{});vp12Spawn('corner');
  eShoot(240,110,Math.PI/2,3,'missile');explode(70,120,40,'red');powerups.push({kind:'shield',x:60,y:180,w:24,h:24,t:0});
  window.__s6qLoot=powerups.length;VP12.age=20;VP12.next=10;}''')
def snapshot(p):return p.evaluate('''()=>({scene:!!s6q13Scene(),enemies:enemies.length,shots:eBullets.length,
 frames:VP12.groups.length,fx:explosions.length+particles.length+sprAnims.length,loot:powerups.length,
 introAge:boss?._rebels?.h3Intro?.age,gangAge:boss?._rebels?.gang1004?.age,clock:AV3.clock})''')
port,stop=shoot.serve(str(R))
try:
 with sync_playwright() as pw:
  for browser in ['chrome','firefox']:
   b=pw.firefox.launch() if browser=='firefox' else pw.chromium.launch(channel=browser,args=['--mute-audio'])
   p=b.new_page(viewport={'width':1440,'height':1000});p.on('pageerror',lambda e:errors.append(str(e)))
   p.on('console',lambda m:errors.append(m.text) if m.type=='error' and not m.location.get('url','').endswith('/favicon.ico') else None)
   p.goto(f'http://127.0.0.1:{port}/index.html',timeout=120000);p.wait_for_function('window.__bofFrames>4');p.evaluate(shoot.TRAP_RAF);p.wait_for_timeout(50)
   assert p.evaluate(shoot.SETUP,{'state':'PLAY','stage':6,'pilot':'axel','invuln':True})['ok']
   p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(6)&&XART.rdy(VP12_ART[6].key)}',timeout=180000)
   p.evaluate('''()=>{story=null;BOFCinematicDirector.cancel();s6Opening=null;fb2Talk=null;run._mission29OpeningDone=true;debugFight=null;
    stagePlan=[];spawnClock=9999;waveIdx=999;warnT=0;run._gp4StageX=null;subBoss=null;subBossActive=false;subBossDone=true;
    subBossTriggered=true;stageTimer=60;s6WingInit();s6Wing.all=true;s6Wing.beats=3;s6Wing.fakeDone=true;s6Wing.route='right';s6Wing.supplyIndex=3;
    s6WingLaunch(4,true);s6Wing.line=null;bossDefeated=false;player.invuln=1e9+2;spawnBoss('rebelsquad');}''')
   seed(p);step(p,180);q=snapshot(p);capture(p,browser+'-clean-intro');rows.append({'browser':browser,'scene':'intro','state':q})
   check(browser+' outgoing actors and hazard queue removed',q['enemies']==0 and q['shots']==0 and q['frames']==0,q)
   check(browser+' no frozen outgoing combat FX',q['fx']==0,q)
   check(browser+' hidden cinematic pickups remain preserved',p.evaluate('powerups.length===window.__s6qLoot'))
   clock=q['clock'];step(p,60);check(browser+' scene sound cue clock keeps advancing',snapshot(p)['clock']-clock>.95)
   # Private authored demonstrations remain alive; no real projectile emitter runs.
   p.evaluate('''()=>{const R=boss._rebels,I=R.h3Intro;I.i=I.rows.findIndex(l=>l.demo==='slug');I.t=1;I.shown=0;}''')
   step(p,30);check(browser+' native noncolliding weapon demonstration remains animated',p.evaluate('boss._rebels.h3Intro.showcase.fx.some(f=>f.kind==="slug")&&eBullets.length===0'))
   capture(p,browser+'-native-weapon-demo')
   p.evaluate('''()=>{const R=boss._rebels;R.frIntro.done=true;R.h3Intro=null;boss._noHit=false;H3.release=false;const G=rg4Init(boss);rg4GangStart(boss,G);}''')
   seed(p);step(p,80);q=snapshot(p);capture(p,browser+'-gang-scene')
   # The current overnight controller deliberately makes GANG a live callout,
   # unlike the subsequent locked rescue. Preserve that native distinction.
   check(browser+' live gang callout keeps combat enabled',not q['scene'] and p.evaluate('rg4State().gang&&!h3Locked()'),q)
   step(p,140);check(browser+' live gang combat continues',p.evaluate('!rg4State().scene&&rg4State().releaseAt>0'))
   p.evaluate('''()=>{rg4RescueStart(boss,rg4State());}''');seed(p);step(p,360);q=snapshot(p);capture(p,browser+'-rescue-scene')
   check(browser+' rescue scene suppresses ordinary enemies and attacks',q['scene'] and q['enemies']==0 and q['shots']==0,q)
   # The approach's original pre-choice radio uses its own native dialogue owner.
   p.evaluate('''()=>{boss=null;bossActive=false;bossDefeated=false;S6Q13.scene=null;s6Wing.fake={t:5.5};s6Wing._fb2Talked=false;fb2TalkStart();}''')
   seed(p);step(p,360);q=snapshot(p);capture(p,browser+'-prechoice-radio')
   check(browser+' pre-choice radio advances safely without background enemies',q['scene'] and q['enemies']==0 and q['shots']==0 and p.evaluate('fb2Talk.age>5'),q)
   # Cole's native pre-choice demonstration owns real temporary player rounds.
   # Its visual clocks must age while the ordinary input/attack owners stay off.
   p.evaluate('''()=>{run.pilot='cole';fb2Talk=null;fb2TalkStart();fb2Talk.i=fb2Talk.beats.findIndex(b=>b.kind==='demo');
    fb2Talk.t=0;fb2Talk.shown=0;fb2Talk.demo=null;S6Q13.scene=null;
    window.__cfInputOld=cf1004Input;window.__cfInputs=0;cf1004Input=function(){window.__cfInputs++;return window.__cfInputOld.apply(this,arguments)};
    window.__coleDemoAudit={clock:CF1004.clock,maxMuzzle:0,maxRelease:0,shots:0,afterFrames:0,stale:0,enemies:0,hostile:0};
    window.__qaTick=()=>{const a=window.__coleDemoAudit,demo=fb2Talk?.beats?.[fb2Talk.i]?.kind==='demo';
     a.maxMuzzle=Math.max(a.maxMuzzle,player._cfMuzzle?.t||0);a.maxRelease=Math.max(a.maxRelease,...wm26Releases.map(f=>f.age),0);
     a.shots=Math.max(a.shots,pBullets.length);a.enemies=Math.max(a.enemies,enemies.length);a.hostile=Math.max(a.hostile,eBullets.length);
     if(!demo){a.afterFrames++;a.stale=Math.max(a.stale,pBullets.length);}};
   }''')
   step(p,1)
   p.evaluate('''()=>{CF1004.effects.push({kind:'colefusionfx',x:player.x,y:player.y,w:60,h:60,t:0,life:.32,_qaDemo:true});}''')
   cole=[]
   for label,frames in [('charge',63),('release',23),('expired-flash',24),('laser',69),('after-volley',90),('next-caption',78)]:
    step(p,frames)
    cole.append(p.evaluate('''label=>({label,clock:CF1004.clock,demo:fb2Talk?.beats?.[fb2Talk.i]?.kind==='demo',demoTime:fb2Talk?.demo?.t||0,
      muzzle:player._cfMuzzle?{t:player._cfMuzzle.t,life:player._cfMuzzle.life}:null,releases:wm26Releases.map(f=>({age:f.age,life:f.life})),
      impact:CF1004.effects.some(f=>f._qaDemo),shots:pBullets.length})''',label))
    if label in ['charge','release','laser','next-caption']:capture(p,browser+'-cole-demo-'+label)
   audit=p.evaluate('window.__coleDemoAudit');p.evaluate('window.__qaTick=null;cf1004Input=window.__cfInputOld')
   rows.append({'browser':browser,'scene':'cole-demo','samples':cole,'audit':audit})
   check(browser+' Cole charge and projectile reel clock advances throughout demo',cole[-1]['clock']-audit['clock']>5.6,audit)
   check(browser+' native Cole fusion muzzle animates then expires',audit['maxMuzzle']>.12 and cole[1]['muzzle'] is not None and cole[2]['muzzle'] is None,cole)
   check(browser+' native weapon release reels advance then expire',audit['maxRelease']>.07 and len(cole[-1]['releases'])==0,audit)
   check(browser+' authored Cole impact effect expires',not cole[2]['impact'])
   check(browser+' demo fires but no rounds leak into the next caption',audit['shots']>0 and audit['afterFrames']>30 and audit['stale']==0,audit)
   check(browser+' demo never resumes normal input or hostile combat',p.evaluate('window.__cfInputs===0') and audit['enemies']==0 and audit['hostile']==0,audit)
   b.close()
finally:stop()
report={'checks':checks,'passed':sum(q['pass'] for q in checks),'failed':sum(not q['pass'] for q in checks),'errors':errors,'rows':rows,'scope':'Real Chrome/Firefox scene rendering and controller fixtures. Full natural intro/miniboss lifecycle is covered by the companion all-difficulty Edge probe.'}
(O/'cinematics-report.json').write_text(json.dumps(report,indent=2));print(json.dumps({'passed':report['passed'],'failed':report['failed'],'errors':errors}),flush=True)
assert not errors,errors
assert not report['failed'],report['failed']
