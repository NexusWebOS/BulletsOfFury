from pathlib import Path
import sys,json
from playwright.sync_api import sync_playwright
R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
O=R/'_shots/enemy_patterns_1013';port,stop=shoot.serve(str(R));errors=[]
try:
 with sync_playwright() as pw:
  b=pw.chromium.launch(channel='msedge',args=['--mute-audio']);p=b.new_page(viewport={'width':1280,'height':900});p.on('pageerror',lambda e:errors.append(str(e)));p.goto(f'http://127.0.0.1:{port}/index.html',timeout=120000);p.wait_for_function('window.__bofFrames>4',timeout=90000);p.evaluate(shoot.TRAP_RAF)
  if not p.evaluate('typeof EP13!=="undefined"'):p.add_script_tag(url=f'http://127.0.0.1:{port}/assets/enemy_patterns_1013.js')
  p.evaluate(shoot.SETUP,{'state':'PLAY','stage':5,'pilot':'cole','invuln':False});p.wait_for_function('()=>{stageLoadTick();ep13Warm();return stageLoadReady(5)&&ep13ReadyArt()}',timeout=180000)
  checks=p.evaluate('''()=>{
   story=null;debugFight=null;waveIdx=999;spawnClock=9999;subBossTriggered=true;subBossDone=true;subBossActive=false;bossActive=false;warnT=0;if(wfx)wfx.fseq=null;stageTimer=1;VP12.next=9999;CP12.next=9999;EP13.next=0;EP13.clock=4;enemies=[];eBullets=[];pBullets=[];l5Rocks=[];l5RockT=9999;
   coopOn=true;for(const f of SEAT_RUN_FIELDS)run2[f]=run[f];run2.lives=3;run2.shield=3;player2.reset();player2.dead=false;player2.out=false;player2.x=camLeftX()+VW*.65;player2.y=PLAY.y+PLAY.h*.84;player2.invuln=1e9;
   player.dead=false;player.out=false;player.invuln=0;run._megaShield=null;run.shield=0;run.lives=3;playerHit();
   const e=spawnEnemy('s5frigate',camLeftX()+VW*.48,PLAY.y+PLAY.h*.24,{});e.hp=e.maxhp=50000;e._ai27={seen:1,visible:true,flinch:0};e._stagger=0;
   const p1Dead=player.dead,p2Alive=!player2.dead,eligible=ep13CanStart(e);ep13Tick(e,.016);const started=!!e._ep13;updatePlay(1/60);const continued=!!e._ep13&&EP13.owner===e;
   player2.dead=true;ep13Tick(e,.016);const allDeadCancels=!e._ep13&&!EP13.owner;coopOn=false;
   return {p1Dead,p2Alive,eligible,started,continued,allDeadCancels,seatRestored:_seat===1};
  }''');print(checks,flush=True);assert all(checks.values()),checks;b.close()
finally:stop()
(O/'coop-verification.json').write_text(json.dumps({'checks':checks,'errors':errors},indent=2));assert not errors,errors;print('PASS surviving co-op pilot retains complex attacks')
