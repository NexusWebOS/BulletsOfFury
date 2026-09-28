import json,http.server
http.server.SimpleHTTPRequestHandler.log_message=lambda *a:None
from pathlib import Path
from playwright.sync_api import sync_playwright
import shoot as sh
out=Path(sh.GAME)/'_shots/hammer_fix_0928';out.mkdir(exist_ok=True)
port,stop=sh.serve(sh.GAME)
try:
 with sync_playwright() as pw:
  b=pw.chromium.launch(args=['--no-sandbox','--mute-audio']);p=b.new_page(viewport={'width':1360,'height':960});p.set_default_timeout(120000);errors=[];p.on('pageerror',lambda e:errors.append(str(e)))
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('()=>window.__bofFrames>4');p.evaluate(sh.TRAP_RAF);p.wait_for_timeout(50)
  report=p.evaluate("""()=>{diffKey='furious';DIFF=DIFFS.furious;run.pilot='yuri';beginStage(5);setState(GS.PLAY);story=null;spawnBoss('chromehammer');bossActive=true;boss.enter=false;boss._noHit=false;boss.x=worldWidth()/2;boss.y=VH*.34;boss._hammer.balance0922=true;hammerState(boss,'hammer');hammerBossTick(boss,.01);hammerBossTick(boss,3.5);boss.hp=boss.maxhp*.5;fr27Restore(boss,.1,false,true);const target=retinaBossTargets(boss).find(t=>t._retinaId==='hammer'),before=boss._hammer.recovery.coreHP;retinaMissileDamage(target,24,{kind:'gmiss',x:target.x,y:target.y});return{before,after:boss._hammer.recovery.coreHP,status:boss._hammer.recovery.status,state:boss._hammer.state};}""")
  report['cue']=p.evaluate("""()=>{ht27Pending=true;startRun(5);const b=boss,d=b._hammerTime;d.mode='attack';d.locked=false;d.shield=false;d.musicStarted=true;d.clock=15.9;Snd.music.hammerTime.pause();b._noHit=false;hammerState(b,'warn');hammerBossTick(b,.01);hammerBossTick(b,1.2);const before={state:b._hammer.state,t:b._hammer.t};ht27LockStart(b,d);return {before,after:{state:b._hammer.state,t:b._hammer.t},armor:!!fr27Armor(b)};}""")
  print(json.dumps(report));(out/'before.json').write_text(json.dumps(report,indent=2));b.close()
finally:stop()
