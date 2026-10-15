"""Part-two feedback: native pixels, real damage routes, mode/input transitions.

Uses shoot.py's real Chromium loop. Invulnerable fixtures inspect encounters;
they do not establish human win rate or a complete unassisted campaign clear.
"""
from pathlib import Path
import sys,json,time
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'_BUILD_SOURCE'));import shoot
OUT=ROOT/'_shots/part2_1010/verified';OUT.mkdir(parents=True,exist_ok=True)
checks=[];errors=[];shots=[]
def check(name,value,data=None):
 checks.append(dict(name=name,passed=bool(value),data=data));print(('PASS ' if value else 'FAIL ')+name,flush=True)
 if not value:print(json.dumps(data),flush=True)
port,stop=shoot.serve(str(ROOT))
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(args=['--autoplay-policy=no-user-gesture-required'])
  p=br.new_page(viewport=dict(width=1280,height=900));p.set_default_timeout(120000)
  p.on('pageerror',lambda e:errors.append(str(e)))
  p.on('console',lambda m:errors.append(m.text[:1000]) if m.type=='error' or 'draw error' in m.text else None)
  p.on('response',lambda r:errors.append('HTTP '+str(r.status)+': '+r.url.split('?')[0]) if r.status>=400 else None)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>3');p.evaluate(shoot.TRAP_RAF)
  def frames(n):
   for i in range(0,n,15):
    e=p.evaluate(shoot.STEP,min(15,n-i))
    if e:errors.append(e)
    p.wait_for_timeout(3)
  def snap(name):
   p.screenshot(path=str(OUT/(name+'.png')));shots.append(name+'.png')
  def scene(n,pk='lizzie',diff='furious'):
   p.evaluate('()=>{P2M.active=null;P2M.pending=null;run.mode="arcade";coopOn=false;delete run._gp4StageX;}')
   p.evaluate(shoot.SETUP,dict(state='PLAY',stage=n,pilot=pk,invuln=True))
   p.wait_for_function('n=>{stageLoadTick();return stageLoadInfo(n).ready}',arg=n,polling=50)
   p.evaluate('''d=>{diffKey=d;DIFF=DIFFS[d];BOFCinematicDirector.cancel();story=null;fb2Talk=null;s6Opening=null;H3.release=false;H3.ending=null;
    stagePlan=[];enemies=[];powerups=[];pBullets=[];eBullets=[];boss=null;bossActive=false;subBoss=null;subBossActive=false;subBossDone=true;
    player.invuln=1e9;player._spawnClearT=1e9;special=null;lzMount=null;atomBooms=[];atomFlash=0;run.dkT=0;run.sonicT=0;
    run.forge={};run.forgeForms={};run.infusion=null;run._spaceShadowHeld=false;_cinematicHidePlayer=false;}''',diff)
  # Nine independent shells, with no leftover atom/beam covering the hull.
  scene(2)
  for pk in ['yuri','falva','cole','maverick','axel','juggernaut','lizzie','decker','freezer']:
   p.evaluate('(k)=>{run.pilot=k;run.shield=2;XART.rdy("ship_"+k);}',pk)
   p.wait_for_function('k=>XART.rdy("ship_"+k)&&XART.rdy("p2_shield_"+k)',arg=pk)
   frames(3);snap('shield-'+pk)
   q=p.evaluate('k=>({hull:P2.hulls.get(k),draws:P2.draws.shield})',pk)
   check(pk+' shield draws against its actual opaque hull',q.get('hull',{}).get('w',0)>0,q)
  p.evaluate('()=>{run.pilot="lizzie";run.shield=0;run.weapon=3;run.wlevel=3;run.forge={3:{elem:"ice",lv:1}};forgeApply();pShoot();updatePlay(.016);}');frames(1)
  q=p.evaluate('()=>({bullets:pBullets.filter(q=>q.kind==="beam").map(q=>({inf:q._inf,w:q.w,top:q.top,bot:q.bot})),draws:P2.draws.ice})')
  check('Forged Ice Laser creates and automatically stamps a continuous damaging beam',len(q['bullets'])==1 and q['bullets'][0]['inf']=='ice' and q['bullets'][0]['w']>0 and q['draws']>0,q);snap('ice-laser')
  p.evaluate('()=>{pBullets=[];special={pilot:"lizzie",t:15,dur:15};run.weapon=0;run.wlevel=3;atomBooms=[{x:player.x,y:player.y-8,t:.65,dur:1.9}];atomFlash=0;}');frames(1);snap('atomic-cloud')
  q=p.evaluate('()=>{pBullets=[];pShoot();const muted=pBullets.length===0;atomBooms=[];pShoot();return{muted,restored:pBullets.some(q=>q.kind==="mg")};}')
  check('Atomic impact owns the trigger, then immediately restores the normal gun',q['muted'] and q['restored'],q)
  # Do not bypass the approved nuclear reveal or its invulnerability.
  scene(3);p.evaluate('on5LaunchEncounter({stage:3,role:"mini",code:"MINI3"})');frames(650)
  q=p.evaluate('()=>({noHit:subBoss._noHit,revealed:subBoss._s3Nuclear?.introDone,mode:subBoss._er26.mode})')
  check('Frost Cruiser nuclear reveal naturally returns to a hittable actor',q['revealed'] and not q['noHit'],q)
  p.evaluate('()=>{for(const q of subBoss._mr27.parts)if(q.id.startsWith("gun")){const z=mr27Shape(subBoss,q.id);hitSubBoss(q.hp+5,z.x,z.y);}}')
  frames(700);q=p.evaluate('()=>({guns:subBoss._mr27.parts.filter(q=>q.id.startsWith("gun")).map(q=>q.dead),history:subBoss._er26.history.map(q=>q.mode),events:P2E.events.slice(-10)})')
  check('Real hits dismantle both Frost guns and leave three physical core attacks',all(q['guns']) and {'p2-core-balls','p2-core-laser','p2-core-charge'}.issubset(set(q['history'])),q);snap('frost-core')
  # Damage each generator through the real hit path, including its rearm cycles.
  scene(4);p.evaluate('on5LaunchEncounter({stage:4,role:"boss",code:"BOSS4"})');frames(180)
  q=p.evaluate('()=>({shield:boss._s4war.shield.active,ram:boss._mr27.ram1002,mode:boss._er26.mode})');check('Storm Sovereign has one attack owner and retains its generator objectives',q['ram'] is None and q['mode'].startswith('p2-') and q['shield'],q);snap('storm-warning')
  for i in range(18):
   p.evaluate('''()=>{if(!boss||boss.dead)return;const H=boss._s4war.shield;
    const points=H.active?H.nodes.filter(q=>!q.dead):[mr27Shape(boss,'core')];
    for(const z of points){if(!z||boss.dead)continue;_lastHitX=z.x;_lastHitY=z.y;_dmgBullet={kind:'beam',dmg:1e5,_stage4WideBeam:true};
     if(bossHitTest(z.x,z.y))hitBoss(1e5);_dmgBullet=null;}}''');frames(95)
   if p.evaluate('!!boss?.dead'):break
  q=p.evaluate('()=>({dead:boss?.dead,hp:boss?.hp,defeated:bossDefeated,cycles:boss?._s4war.shield.cycle,threshold:boss?._s4war.shieldThresholdIndex})')
  check('Storm Sovereign can be completed through generators, rearm cycles and core damage',q['dead'] and q['defeated'] and q['threshold']>=2,q);snap('storm-defeated')
  # Stage 5 authored formation weapons now announce and release from hardpoints.
  scene(5,'cole');p.evaluate('()=>{for(const [i,k] of ["s5frigate","s5gravity","s5station"].entries())spawnEnemy(k,camLeftX()+100+i*140,180,{});}')
  frames(420);q=p.evaluate('()=>({events:P2E.events.filter(q=>q.event==="space-salvo"),shots:eBullets.filter(q=>q._p2Emitter).length})')
  check('Three space hulls execute actual ranged salvos',len({q['ship'] for q in q['events'] if q['shots']})>=3,q);snap('space-formations')
  # Last words and one destruction: no second dying close-up in the cutaways.
  scene(5,'lizzie','normal');p.evaluate('on5LaunchEncounter({stage:5,role:"boss",code:"BOSS5"})');frames(220)
  p.evaluate('()=>{boss.hp=0;bossDie();}');frames(1)
  q=p.evaluate('()=>({hold:H3.ending.sm10.hold,core:sm10Core(H3.ending.boss),phase:H3.ending.sm10.phase})')
  check('Hammer retains his entire current combat pose for his last words',not q['hold']['dead'] and q['phase']=='words',dict(core=q['core'],phase=q['phase']));snap('hammer-last-words')
  p.evaluate('()=>{const Q=H3.ending.sm10;Q.line=1;Q.shown=SM10_LAST_WORDS[1].length;Q.t=20;}')
  for i in range(150):
   frames(1)
   if p.evaluate('H3.ending.sm10.phase==="lock"'):break
  frames(15);snap('hammer-core-lock')
  for i in range(100):
   frames(1)
   if p.evaluate('H3.ending.sm10.phase==="missile"'):break
  frames(18);snap('hammer-missile');frames(350);snap('hammer-rupture')
  faces=[]
  for i in range(60):
   frames(15);faces.append(p.evaluate('H3.ending.phase'))
  q=p.evaluate('()=>({phase:H3.ending.phase,t:H3.ending.t,events:SM10.events.slice(-15)})')
  check('After the in-game rupture the repeated dying close-up is skipped','face' not in faces and q['t']>=17.5,q)
  # Real visible mode cards and confirmation input, not direct launch alone.
  p.evaluate('()=>{P2M.receipt=null;bonusModesUnlocked=true;setState(GS.MODESEL);}')
  q=p.evaluate('modeList().map(q=>({mode:q.mode,open:modeItemOpen(q)}))');check('A stale bonus boolean cannot open bonus modes without completion evidence',all(not x['open'] for x in q if x['mode'] in ['bossrush','timeattack']) and all(x['mode']!='ngplus' for x in q),q)
  p.evaluate('()=>{P2M.receipt={version:2,mode:"campaign",stages:[1,2,3,4,5,6,7,8]};modeIndex=modeList().findIndex(q=>q.mode==="bossrush");setState(GS.MODESEL);}')
  frames(40);snap('unlocked-modes');q=p.evaluate('modeList().filter(q=>["bossrush","timeattack"].includes(q.mode)).map(q=>modeItemOpen(q))');check('Valid completion enables both visible playable cards',q==[True,True],q)
  p.evaluate('Input.injectTap("pad_b0")');frames(45);q=p.evaluate('({state,pending:P2M.pending})');check('Boss Rush starts from the actual menu confirm action',q['pending']=='bossrush' and q['state']=='diff',q)
  p.evaluate('()=>{pilotIndex=6;startRun(1);player.invuln=1e9;player._spawnClearT=1e9;}');frames(140)
  q=p.evaluate('()=>({active:P2M.active,boss:boss.kind,stage:run.stage,score:run.score})');check('Boss Rush loads its real first boss',q['active']=='bossrush' and q['boss']=='damkeeper',q);snap('boss-rush-first')
  routes=[]
  for i in range(9):
   q=p.evaluate('()=>({index:P2M.index,stage:run.stage,boss:boss?.kind,code:P2M.events.at(-1).code})');routes.append(q)
   p.evaluate('scLeaveStage({bonus:50,rank:"A"})')
   if i<8:p.evaluate('()=>{stateT=1;Input.injectTap("pad_b0");p2ModeResultDraw();player.invuln=1e9;}');frames(5)
  q=p.evaluate('()=>({state,result:P2M.result,record:localStorage.getItem("bof_bossrush_"+run.pilot+"_"+diffKey)})')
  check('Rush result/confirm traverses all nine encounters and stores its own completed record',len(routes)==9 and len(set(r['code'] for r in routes))==9 and q['result']['complete'] and q['record'],dict(routes=routes,result=q));snap('boss-rush-result')
  p.evaluate('()=>{p2ModeChoose("timeattack");startRun(1);BOFCinematicDirector.cancel();story=null;setState(GS.PLAY);stagePlan=[];enemies=[];}');frames(65)
  before=p.evaluate('P2M.elapsed');p.evaluate('setState(GS.PAUSE)');frames(65);after=p.evaluate('P2M.elapsed')
  check('Time Attack advances during play and holds during Pause',before>0 and before==after,dict(before=before,after=after))
  p.evaluate('()=>{setState(GS.PLAY);triggerGameOver();}');q=p.evaluate('({state,result:P2M.result})');check('Time Attack has a distinct loss result',q['state']=='p2result' and q['result']['success'] is False,q);snap('time-attack-result')
  p.evaluate('()=>{p2ModeChoose("coop");P2M.row=0;p2ChoiceConfirm();pilotIndex=6;p2Index=1;startRun(1);BOFCinematicDirector.cancel();story=null;setState(GS.PLAY);stagePlan=[];enemies=[];pBullets=[];window.p2CoopShots=[1,2].map(n=>withSeat(n,()=>{const first=pBullets.length;pShoot();return pBullets.slice(first).map(q=>({x:q.x,y:q.y,kind:q.kind}));}));}')
  q=p.evaluate('()=>({seats:seatList(),shots:p2CoopShots.map(q=>q.length),lives:[run.lives,run2.lives],pilots:[run.pilot,run2.pilot],born:p2CoopShots})')
  check('Local co-op fires independently for two selected pilots',q['seats']==[1,2] and all(n>0 for n in q['shots']) and all(n>0 for n in q['lives']),q);frames(3);snap('local-coop')
  check('No page, console, renderer or asset errors',not errors,errors);br.close()
except Exception as e:errors.append(type(e).__name__+': '+str(e));print(errors[-1],flush=True)
finally:
 stop();r=dict(passed=sum(q['passed'] for q in checks),failed=sum(not q['passed'] for q in checks),checks=checks,errors=errors,shots=shots)
 (OUT/'report.json').write_text(json.dumps(r,indent=2),encoding='utf-8');print(json.dumps(dict(passed=r['passed'],failed=r['failed'],errors=errors)),flush=True)
sys.exit(1 if errors or r['failed'] else 0)
