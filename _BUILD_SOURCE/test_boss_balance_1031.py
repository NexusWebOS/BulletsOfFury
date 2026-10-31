from pathlib import Path
import sys,json,hashlib
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];W=R/'_shots/boss_balance_normal_1031';W.mkdir(parents=True,exist_ok=True);sys.path.insert(0,str(R/'_BUILD_SOURCE'))
from shoot import serve,STEP
from barrage_review_common_1025 import boot
checks=[];errors=[]
def ck(name,result,data=None):
 checks.append(dict(name=name,passed=bool(result),data=data));(W/'checks.json').write_text(json.dumps(checks,indent=2));print('PASS'if result else'FAIL',name,str(data)[:900]if not result else'',flush=True);assert result,(name,data)
port,stop=serve(str(R))
try:
 with sync_playwright()as pw:
  br=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required']);p=boot(br.new_context(viewport={'width':1280,'height':800}),port,9,errors)
  def step(n):
   for i in range(0,n,12):
    e=p.evaluate(STEP,min(12,n-i));assert not e,e;p.wait_for_timeout(1)
  def shot(n):
   p.evaluate('()=>{drawScene(0);SC12.refresh();__bofFit()}');p.screenshot(path=str(W/(n+'.png')))
  ck('Current game and late owners load without errors',not errors,errors)
  for rank,hp in [('hard',3520),('furious',4160)]:
   q=p.evaluate('''rank=>{diffKey=rank;DIFF=difficultyForRun('campaign',rank);run.ngplus=false;coopOn=false;spawnSubBoss('voidhorizon');window.B=subBoss;window.H=eh57State(B);B.enter=false;H.protected=false;H.mode='recover';eh57Move(B,camLeftX()+240,viewTopY()+180);eh57Set(B,'spiral');return{max:B.maxhp,core:B._s9rift.core.maxhp,on:H.on,gap:H.period-H.on,pulses:H.pulses,warm:H.warm,rest:H.rest};}''',rank)
   ck(rank+' health is one consistent pool with no adaptive double ramp',q['max']==hp and q['core']==hp,q)
   ck(rank+' has a readable tell and at least half a second between laser bursts',q['warm']>=1.3 and q['gap']>=.5,q)
   count=p.evaluate('''()=>{let frames=0,on=0,off=0,last=H.angle,continuous=true;for(let i=0;i<420;i++){s9VoidHorizonTick(B,1/60);if(H.angle<=last)continuous=false;last=H.angle;if(H.phase==='fire'){frames++;if(H.beams.length)on++;else off++;}}return{frames,on,off,continuous,omega:H.omega};}''')
   ck(rank+' rotation never pauses and active lasers leave actual off gaps',count['continuous'] and count['on']>0 and count['off']>0 and count['omega']>3.7,count)
  p.evaluate("()=>{run.ngplus=true;spawnSubBoss('voidhorizon');}");ck('NG+ adds exactly 25% once',p.evaluate('subBoss.maxhp===5200&&subBoss._s9rift.core.maxhp===5200'))
  p.evaluate("()=>{coopOn=true;run.ngplus=false;spawnSubBoss('voidhorizon');}");ck('Co-op retains the native 1.5 health multiplier',p.evaluate('subBoss.maxhp===6240'));p.evaluate('coopOn=false')
  p.evaluate("()=>{run.ngplus=false;spawnSubBoss('voidhorizon');window.B=subBoss;window.H=eh57State(B);B.enter=false;H.protected=false;H.mode='recover';eh57Move(B,camLeftX()+240,180);H.frame=0;window.spot=()=>{const w=B._s9rift.core;for(let y=-60;y<=60;y+=4)for(let x=-60;x<=60;x+=4)if(s9VoidHorizonPart(B,w.x+x,w.y+y))return{x:w.x+x,y:w.y+y};};const q=spot();s9VoidHorizonHit(B,99999,q.x,q.y);}")
  ck('A large hit stops exactly at the half-health transition',p.evaluate('H.half&&H.protected&&B.hp===2080&&B.hp===B._s9rift.core.hp'))
  p.evaluate("()=>{H.protected=false;eh57Set(B,'dash');}");ck('Dash corridor is committed from charge start',p.evaluate('H.start&&H.end&&H.phase==="charge"'))
  p.evaluate("()=>{H.t=H.warm+3.46;s9VoidHorizonTick(B,1/60);}");ck('Offscreen return cannot take hits or Retina locks',p.evaluate('H.phase==="return"&&H.protected&&retinaBossTargets(B).length===0'))
  p.evaluate("()=>{H.t=H.warm+4.87;s9VoidHorizonTick(B,1/60);}");ck('Dash has an actual foreground recovery window',p.evaluate('H.phase==="recover"&&!H.protected&&H.beams.length===0'))
  p.evaluate("()=>{eh57Set(B,'orb');eh57Round(B,1,200,true);}");ck('Horizon ordinary projectiles remain unshootable',p.evaluate('eBullets.filter(q=>q._eh57Owner===B).every(q=>!enemyOrdnanceCanIntercept(q))'))
  # True progression owner and a clean test profile, never a real user profile.
  p.evaluate("()=>{debugFight=null;coopOn=false;run.mode='campaign';run.ngplus=false;diffKey='normal';DIFF=difficultyForRun('campaign',diffKey);run.stage=5;curStage=STAGES[4];campaign.rank={1:'A',2:'A',3:'B',4:'A'};campaign.unlockedMax=5;run.score=50000;spawnBoss('chromehammer');boss.hp=0;bossDie();}")
  snap=p.evaluate('JSON.parse(localStorage.getItem(NF100.key)||"null")')
  ck('Actual Normal Chronos defeat autosaves before results/flight',snap and snap['normalComplete100']['phase']=='defeated' and snap['stage']==5 and snap['completed'],snap)
  ck('Defeat save retains earned chaingun and completed difficulty',snap['diff']=='normal' and snap.get('earnedUnlocks',{}).get('chaingun'),snap.get('earnedUnlocks'))
  p.wait_for_function('()=>nf100Warm()',timeout=180000)
  p.evaluate("()=>{window.score0=run.score;window.res={bonus:1234,rank:'A'};scLeaveStage(res);}")
  ck('Normal results settle once and launch the return flight',p.evaluate('state===NF100.state&&NF100.current.phase==="flight"&&run.score===score0+1234'))
  step(95);shot('normal-earth-return');step(130);shot('normal-hq-return');step(230);shot('normal-hard-choice')
  ck('Flight reaches Hard/Furious choice instead of Stage 6',p.evaluate('state===NF100.state&&NF100.current.phase==="menu"&&run.stage===5'))
  ck('Message and description fit their bitmap text bounds',p.evaluate('NF100.current.copy.rows.length*NF100.current.copy.size*1.45<=85&&NF100.current.detail.rows.length*NF100.current.detail.size*1.45<=94'))
  p.evaluate('NF100.current.sel=1');shot('normal-furious-choice')
  p.evaluate("()=>{window.savedSetter=Storage.prototype.setItem;Storage.prototype.setItem=function(k,v){if(k===NF100.key)throw Error('quota-test');return savedSetter.call(this,k,v)};window.refused=!nf100Choose(1);}")
  ck('Failed autosave is honest and blocks abandoning completion',p.evaluate('refused&&NF100.current.phase==="menu"&&!NF100.current.saved'))
  p.evaluate('()=>{Storage.prototype.setItem=savedSetter;}');p.evaluate('nf100Choose(1)');step(90);shot('furious-pilot-select')
  ck('Furious choice fades into pilot select, resets route, preserves mode',p.evaluate('state===GS.PILOT&&diffKey==="furious"&&run.stage===1&&run.mode==="campaign"&&!run.ngplus'))
  p.evaluate('campBeginFresh()');ck('New run cannot erase archived Normal completion',p.evaluate('JSON.parse(localStorage.getItem(NF100.key)).normalComplete100.phase==="settled"'))
  p.evaluate("()=>{const s=JSON.parse(localStorage.getItem(NF100.key));campApply(s);openStageSelect(run.stage,{});}");step(30)
  ck('Loading completed Normal save reopens the choice, not a locked stage',p.evaluate('state===NF100.state&&NF100.current.phase==="menu"&&diffKey==="normal"'))
  p.evaluate('nf100Choose(0)');step(90)
  ck('Hard choice also routes to pilot select correctly',p.evaluate('state===GS.PILOT&&diffKey==="hard"&&run.stage===1'))
  p.evaluate("()=>{run.mode='arcade';run.stage=5;diffKey='normal';DIFF=difficultyForRun('arcade',diffKey);nf100Open(false,true);nf100Choose(1);}");step(90)
  ck('Arcade mode is retained across the new difficulty choice',p.evaluate('state===GS.PILOT&&run.mode==="arcade"&&diffKey==="furious"'))
  p.evaluate("()=>{debugFight={stage:5,role:'boss'};run.mode='campaign';diffKey='normal';run.stage=5;window.bytes0=localStorage.getItem(NF100.key);spawnBoss('chromehammer');boss.hp=0;bossDie();}");ck('Debug demonstrations never write completion saves',p.evaluate('localStorage.getItem(NF100.key)===bytes0'))
  p.set_viewport_size({'width':390,'height':844});p.evaluate("()=>{debugFight=null;run.pilot='cole';run.mode='campaign';nf100Open(false,true);}");step(35);shot('normal-mobile-choice')
  p.evaluate("()=>{run.ngplus=true;run.stage=5;diffKey='normal';debugFight=null;}");ck('Normal NG+ also ends at Stage 5',p.evaluate('nf100Eligible()'))
  p.evaluate("()=>{run.ngplus=false;run._normalComplete100=null;NF100.resume=null;const s=campSnapshot();delete s.normalComplete100;s.stage=9;s.diff='normal';campApply(s);}");ck('Existing Stage 5 bonus detour saves are not misclassified as completed Normal',p.evaluate('!NF100.resume'))
  p.evaluate("()=>{debugFight=null;coopOn=true;coopPick=2;run.mode='arcade';run.stage=5;diffKey='normal';run2.pilot='decker';run2.score=3210;run2.lives=2;run._normalComplete100=null;nf100Open(true,true);}")
  ck('Co-op return flight includes the actual second pilot',p.evaluate('NF100.current.second==="decker"'))
  p.evaluate("()=>{NF100.current.phase='menu';nf100Choose(1);}");step(90)
  ck('Co-op restart opens player-one selection before player two',p.evaluate('state===GS.PILOT&&coopOn&&coopPick===0&&run.mode==="arcade"'))
  p.evaluate("()=>{run.stage=5;diffKey='normal';nf100Save('settled');const s=JSON.parse(localStorage.getItem(NF100.key));coopOn=false;run2.pilot='axel';run2.score=0;campApply(s);}")
  ck('Completed co-op autosave restores both pilot identity and second score',p.evaluate('coopOn&&run2.pilot==="decker"&&run2.score===3210&&run.mode==="arcade"'))
  ck('No browser/render errors throughout actual state transitions',not errors,errors)
  br.close()
finally:stop()
ck('Core remains byte-for-byte unchanged',hashlib.sha256((R/'assets/game.js').read_bytes()).hexdigest()=='024a0933c5729b6afa2a6e88864574636293bdb535d9f4e5eb91d36bb98509de')
print('RESULT',len(checks),'passed',flush=True)
