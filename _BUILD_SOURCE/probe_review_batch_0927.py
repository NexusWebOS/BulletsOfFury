import json,http.server
http.server.SimpleHTTPRequestHandler.log_message=lambda *a:None
from pathlib import Path
from playwright.sync_api import sync_playwright
import shoot as sh
out=Path(sh.GAME)/'_shots/furious_0927';out.mkdir(exist_ok=True)
port,stop=sh.serve(sh.GAME)
try:
 with sync_playwright() as pw:
  b=pw.chromium.launch(args=['--no-sandbox','--mute-audio']);p=b.new_page(viewport={'width':1360,'height':960});p.set_default_timeout(120000);errors=[];p.on('pageerror',lambda e:errors.append(str(e)))
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('()=>window.__bofFrames>4');p.evaluate(sh.TRAP_RAF);p.wait_for_timeout(50)
  p.evaluate("()=>{diffKey='furious';DIFF=DIFFS.furious;run.mode='arcade';run.pilot='yuri';beginStage(5);setState(GS.PLAY);story=null;player.invuln=99999;spawnBoss(curStage.boss);bossActive=true;boss._noHit=false;boss.enter=false;boss.x=worldWidth()/2;boss.y=VH*.32;boss._hammer.state='hammer';boss._hammer.balance0922=true;hammerBossTick(boss,.016);}")
  p.wait_for_function("()=>XART.rdy('fr27_chromium_actions')&&XART.rdy('bmbar_fill_grey')")
  report=p.evaluate("()=>{for(let i=0;i<130;i++)hammerBossTick(boss,1/60);drawWorld(0);return {armor:boss._hammer.frArmor,state:boss._hammer.state,hp:boss.hp,max:boss.maxhp};}")
  p.screenshot(path=str(out/'chromium-activation.png'))
  report['hammer']=p.evaluate("()=>{for(let i=0;i<100;i++)hammerBossTick(boss,1/60);const hp=boss.hp,a=boss._hammer.frArmor.hp;const dealt=hammerBossDamage(boss,100);boss.hp-=dealt;const armorDamage=a-boss._hammer.frArmor.hp,hpUnchanged=hp===boss.hp;boss._hammer.frArmor.hp=0;boss.hp=boss.maxhp*.14;hammerState(boss,'hammer');hammerBossTick(boss,.01);const checkpoints=[];for(let i=0;i<4;i++){if(boss._hammer.state==='fr_twirl')break;if(boss._hammer.recovery)boss._hammer.recovery.status='complete';boss._hammer.frRecovery=false;boss._hammer.frArmor.barrier=0;hammerState(boss,'hammer');hammerBossTick(boss,.01);checkpoints.push(boss._hammer.state);}return {armorDamage,hpUnchanged,checkpoints,state:boss._hammer.state};}")
  p.evaluate("()=>{boss._hammer.t=.7;drawWorld(0);}");p.screenshot(path=str(out/'chromium-twirl.png'))
  p.evaluate("()=>{beginStage(6);setState(GS.PLAY);story=null;s6Opening=null;s6Wing.choice=true;s6Wing.route=null;}")
  p.evaluate('()=>drawWorld(0)');p.wait_for_timeout(1600)
  report['choice']=p.evaluate("()=>{const before={timer:stageTimer,x:player.x,y:player.y,scroll:mapScroll};for(let i=0;i<120;i++)updatePlay(1/60);drawWorld(0);return{before,after:{timer:stageTimer,x:player.x,y:player.y,scroll:mapScroll}};}");p.screenshot(path=str(out/'route-choice.png'))
  p.evaluate("()=>{s6Wing.choice=false;s6Wing.route='right';spawnBoss('rebelsquad');bossActive=true;rebelSquadTick(boss,11);drawWorld(0);}");p.wait_for_timeout(1500);p.evaluate('()=>drawWorld(0)');p.screenshot(path=str(out/'rebel-parley.png'))
  report['hammerContinue']=p.evaluate("()=>{ht27Pending=true;pilotIndex=PILOTS.findIndex(p=>p.key==='yuri');startRun(5);const B=boss,D=B._hammerTime;D.mode='attack';D.locked=false;D.shield=false;D.clock=25;D.musicStarted=true;Snd.music.hammerTime.currentTime=25;player.dead=true;run.lives=0;run.contUsed=0;setState(GS.CONTINUE);const entered=state;stateT=1;Input.injectTap('enter');drawContinue(.01);return{entered,state,active:ht27Active,sameBoss:boss===B,lives:run.lives,used:run.contUsed};}")
  report['errors']=errors;(out/'review-probe.json').write_text(json.dumps(report,indent=2));print(json.dumps(report));b.close()
finally:stop()
