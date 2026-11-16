from pathlib import Path
from playwright.sync_api import sync_playwright
import sys,json
R=Path(__file__).resolve().parents[1];O=R/'_shots/release_qa_1116/followup';O.mkdir(parents=True,exist_ok=True);sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
checks=[];errors=[]
def ck(n,v,d=None):checks.append({'name':n,'ok':bool(v),'data':d});print(('PASS 'if v else'FAIL ')+n+(' '+str(d)if not v else''),flush=True)
with sync_playwright()as w:
 b=w.chromium.launch(args=['--no-sandbox','--autoplay-policy=no-user-gesture-required']);p=b.new_page(viewport={'width':1440,'height':1000});p.set_default_timeout(150000)
 p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text)if m.type=='error'else None);p.on('response',lambda r:errors.append(str(r.status)+' '+r.url)if r.status>=400 else None)
 p.goto('http://127.0.0.1:8765/index.html?release-followup=1116');p.wait_for_function('window.__bofFrames>6');p.evaluate(shoot.TRAP_RAF);p.evaluate('()=>{BOFOnline.submitScore=()=>{};}')
 def step(n):
  for i in range(0,n,12):p.evaluate(shoot.STEP,min(12,n-i));p.wait_for_timeout(1)
 for diff in ['hard','furious']:
  for role in ['mini','boss']:
   p.evaluate("q=>{BOSSMODE.start(6,q.role,'cole',false,q.diff);player.invuln=1e8;player._spawnClearT=1e8;}",{'role':role,'diff':diff});p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(6)}',polling=50);step(720)
   q=p.evaluate("role=>{const b=role==='boss'?boss:subBoss;return{state,kind:b?.kind,hp:b?.hp,enter:b?.enter,live:BOFCinematicDirector.live,opening:!!s6Opening,warn:warnT,entry:ENTRY16.events.at(-1)};}",role)
   ck(diff+' Stage6 '+role+' standalone native warning reaches the intended live actor',q.get('hp',0)>0 and q['entry']['role']==role,q);p.evaluate('()=>SC12.refresh()');p.screenshot(path=str(O/(diff+'-s6-'+role+'.jpg')),type='jpeg',quality=86)
 # Prepared earned mode checkpoint: the actual gauntlet route owner chooses each fight.
 p.evaluate("()=>{debugFight=null;P2M.active='bossrush';P2M.pending=null;diffKey='hard';run.mode='arcade';}")
 for idx in [5,6,7,8]:
  p.evaluate('i=>{P2M.index=i;p2RushLaunch();player.invuln=1e8;player._spawnClearT=1e8;}',idx);p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(run.stage)}',polling=50);step(420)
  q=p.evaluate('({index:P2M.index,state,stage:run.stage,kind:boss?.kind,hp:boss?.hp,active:P2M.active})');ck('Boss Rush native checkpoint '+str(idx+1)+' has a live intended boss',q.get('hp',0)>0 and q['active']=='bossrush',q)
 p.evaluate("()=>{P2M.active=null;P2M.receipt={version:2,mode:'campaign',stages:[1,2,3,4,5,6,7,8]};P2M.choice='arcade';P2M.row=1;p2ChoiceConfirm();}")
 ck('earned Arcade New Game+ menu retains its flag into difficulty selection',p.evaluate('state===GS.DIFF&&run.ngplus&&P2M.ngplus'))
 # Retest the older co-op fixture only after terrain/camera have settled.
 p.evaluate("()=>{BOSSMODE.start(7,'mini','cole',false,'hard');boss=subBoss=null;bossActive=subBossActive=false;debugFight=null;stagePlan=[];spawnClock=1e9;enemies=[];eBullets=[];player.invuln=1e8;player._spawnClearT=1e8;setState(GS.PLAY);}");step(30)
 p.evaluate("()=>{enemies=[];spawnEnemy('s7tank',worldWidth()/2,130,{});window.QTank=enemies.at(-1);}");step(20)
 p.evaluate("()=>{coopOn=true;for(const f of SEAT_RUN_FIELDS)run2[f]=run[f];run2.pilot='decker';p2Index=PILOTS.findIndex(p=>p.key==='decker');PILOTMOD2={...PILOTS[p2Index]};player2.reset();player2.invuln=1e8;player2._spawnClearT=1e8;window.QTankHP=QTank.hp;pBullets=[];withSeat(2,()=>{run.weapon=0;run.wlevel=0;run._primary1003b='mg';player.x=QTank.x;player.y=QTank.y+80;player.fireCd=0;pShoot();});for(const b of pBullets){b.x=QTank.x;b.y=QTank.y+6;b.vx=0;b.vy=-1;b.dmg=.25;}}")
 step(1);q=p.evaluate('({loss:QTankHP-QTank.hp,flash:QTank.flash,x:QTank.x,y:QTank.y,seat:_seat})');ck('settled Stage7 tank takes native Player2 projectile damage and flashes',q['loss']>0 and q['flash']>0 and q['seat']==1,q);p.evaluate('()=>SC12.refresh()');p.screenshot(path=str(O/'s7tank-p2-hit.png'))
 # Current Stage8 native solo/party health, without the obsolete LC19_OFF comparison.
 for diff in ['hard','furious']:
  p.evaluate("d=>{coopOn=false;BOSSMODE.start(8,'mini','cole',false,d);boss=subBoss=null;bossActive=subBossActive=false;debugFight=null;stagePlan=[];enemies=[];spawnClock=1e9;}",diff);step(30)
  q=p.evaluate("()=>{const out=[];for(const kind of ['s8deathorb','s8carrier','s8bomber','s8tentacle']){enemies=[];coopOn=false;const a=spawnEnemy(kind,worldWidth()/2,150,{});const solo=enemies.at(-1).hp;enemies=[];coopOn=true;spawnEnemy(kind,worldWidth()/2,150,{});const party=enemies.at(-1).hp;out.push({kind,solo,party,ratio:party/solo});}return out;}")
  ck(diff+' Stage8 current native party scaling is preserved for all four restored hulls',all(abs(r['ratio']-1.25)<.02 for r in q),q)
 ck('no page console or asset errors',not errors,errors);b.close()
(O/'report.json').write_text(json.dumps({'scope':'Native standalone encounter/mode checkpoints and settled physical projectile retests. No full campaign/Boss Rush win claim. Stage8 health ratios compare real native solo and co-op builds, not a removed historical test switch.','checks':checks,'errors':errors},indent=2),encoding='utf8');sys.exit(any(not q['ok']for q in checks))
