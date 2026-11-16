from pathlib import Path
from playwright.sync_api import sync_playwright
import sys,json
R=Path(__file__).resolve().parents[1];O=R/'_shots/cinema_overnight_1116/boss-loading';sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
checks=[];errors=[]
with sync_playwright()as w:
 b=w.chromium.launch(args=['--no-sandbox','--autoplay-policy=no-user-gesture-required']);p=b.new_page(viewport={'width':1440,'height':1000});p.set_default_timeout(180000)
 p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text)if m.type=='error'else None)
 p.goto('http://127.0.0.1:8765/index.html?night-boss-controls=1116');p.wait_for_function('window.__bofFrames>6');p.evaluate(shoot.TRAP_RAF);p.evaluate('()=>BOFOnline.submitScore=()=>{}')
 p.evaluate("()=>{run.mode='campaign';run.pilot='cole';pilotIndex=PILOTS.findIndex(p=>p.key==='cole');diffKey='furious';coopOn=true;p2Index=PILOTS.findIndex(p=>p.key==='decker');startRun(1);BOFCinematicDirector.cancel();campaign.unlockedMax=9;campaign.rank={1:'A',2:'A',3:'A',4:'A',5:'A',6:'A',7:'A'};beginStage(8);warmStage(8);debugFight=null;stagePlan=[];waveIdx=999;spawnClock=99999;subBossDone=true;bossWarned=true;}");p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(8)&&Object.values(RD71_ART).every(a=>XART.rdy(a.key))&&Object.values(RD94_ART).every(a=>XART.rdy(a.key))}',polling=50)
 p.evaluate("()=>{window.NightOriginalReady=XART.rdy;window.NightGate=RD71_ART.drone_charge.key;XART.rdy=function(k){return k===NightGate?false:NightOriginalReady.call(this,k)};spawnBoss('vileexistence');warnT=0;setState(GS.PLAY);DBGT.god=false;Input.clearTaps();window.Held1=keybindFor(1).right.find(k=>!k.startsWith('mouse'));window.Held2=keybindFor(2).left.find(k=>!k.startsWith('mouse'));Input.keys[Held1]=Input.keys[Held2]=true;}")
 p.evaluate(shoot.STEP,1);q=p.evaluate('({coop:coopOn,p1:[player.x,player.y],p2:[player2.x,player2.y],t:boss._r30.t,clock:stageTimer,distance:run.distance})');start=q
 for i in range(30):
  e=p.evaluate(shoot.STEP,6)
  if e:raise RuntimeError(e)
 q=p.evaluate('({coop:coopOn,p1:[player.x,player.y],p2:[player2.x,player2.y],t:boss._r30.t,clock:stageTimer,distance:run.distance,immunity:[player.invuln,player2.invuln]})')
 checks.append({'name':'Both native co-op ships and simulation clocks stay anchored under held movement while art waits','ok':q['coop']and q['p1']==start['p1']and q['p2']==start['p2']and q['t']==start['t']==0 and abs(q['clock']-start['clock'])<1e-7 and abs(q['distance']-start['distance'])<1e-7,'data':{'start':start,'end':q}})
 p.evaluate("()=>{Input.keys[Held1]=Input.keys[Held2]=false;Input.injectTap('pad_b9')}");p.evaluate(shoot.STEP,1);q=p.evaluate('({state,menu:playPause?.mode,t:boss._r30.t,clock:stageTimer})');checks.append({'name':'Logical gamepad Start opens the native pause menu during missing boss art','ok':q['state']=='paused'and q['menu']=='root','data':q})
 before=q
 for i in range(12):p.evaluate(shoot.STEP,6)
 q=p.evaluate('({state,t:boss._r30.t,clock:stageTimer})');checks.append({'name':'Pause freezes the waiting introduction and clock','ok':q['state']=='paused'and q['t']==before['t']and q['clock']==before['clock'],'data':q})
 p.evaluate("()=>Input.injectTap('pad_b9')");p.evaluate(shoot.STEP,1);q=p.evaluate('({state,t:boss._r30.t,clock:stageTimer})');checks.append({'name':'Logical gamepad Start resumes the same native waiting introduction','ok':q['state']=='play'and q['t']==0,'data':q})
 p.evaluate('()=>NightGate=null')
 for i in range(240):
  e=p.evaluate(shoot.STEP,6)
  if e:raise RuntimeError(e)
  if p.evaluate("boss._r30.mode==='fight'"):break
 q=p.evaluate('({mode:boss._r30.mode,noHit:boss._noHit,hp:boss.hp,max:boss.maxhp,immunity:[player.invuln,player2.invuln],p1:[player.x,player.y],p2:[player2.x,player2.y]})');checks.append({'name':'Co-op decode release completes intact and releases temporary protection for both seats','ok':q['mode']=='fight'and not q['noHit']and q['hp']==q['max']and all(v<=.5 for v in q['immunity']),'data':q});p.evaluate('()=>{drawWorld(0);SC12.refresh()}');p.screenshot(path=str(O/'coop-resumed.png'))
 # Fresh missing-art boss; native pause quit must remain a usable escape route.
 p.evaluate("()=>{NightGate=RD71_ART.drone_charge.key;spawnBoss('vileexistence');warnT=0;setState(GS.PLAY);Input.clearTaps();}");p.evaluate(shoot.STEP,90);p.evaluate("()=>Input.injectTap('pad_b9')");p.evaluate(shoot.STEP,1);p.evaluate('()=>playPauseChoose(5)')
 for i in range(100):
  e=p.evaluate(shoot.STEP,6)
  if e:raise RuntimeError(e)
  if p.evaluate("state==='gameover'||state===GS.TITLE"):break
 q=p.evaluate('({state,blocked:!!NightGate,exit:playPause?.mode})');checks.append({'name':'Native pause quit can leave a permanently missing-art encounter','ok':q['state']in['gameover','title']and q['blocked'],'data':q})
 p.evaluate('()=>{XART.rdy=NightOriginalReady;NightGate=null}');checks.append({'name':'No page or console errors','ok':not errors,'data':errors});b.close()
(O/'controls-current.json').write_text(json.dumps({'checks':checks,'errors':errors,'scope':'Fresh native startRun co-op initialization and prepared unlocked Stage8 profile with controlled art delay. Actual logical Start edge, native pause/resume/quit callback and normal reveal. No physical-controller, combat-win or WAN claim.'},indent=2),encoding='utf8');print(json.dumps(checks,indent=2));assert all(q['ok']for q in checks)
