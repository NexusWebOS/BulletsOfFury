"""Current Breaker in the real Stage9 wave book and native encounter handoff."""
from pathlib import Path
import json,sys
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'_BUILD_SOURCE'));from shoot import TRAP_RAF
O=R/'_shots/current_breaker_1102';rows=[];errors=[]
with sync_playwright()as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required']);p=b.new_page(viewport={'width':1280,'height':800});p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:500])if m.type=='error'or'draw error'in m.text else None);p.goto('http://127.0.0.1:8805/game/index.html',wait_until='load',timeout=180000);p.wait_for_function('window.__bofFrames>5');p.mouse.click(3,3);p.evaluate(TRAP_RAF);p.add_script_tag(path=str(R/'_BUILD_SOURCE/enemy_behaviour_lab_1011.js'))
 p.evaluate('''()=>{EA11.setup(9,'furious');subBossTriggered=subBossDone=aminiTriggered=bossWarned=false;debugUnlocked=true;DBGT.god=true;player.invuln=0;window.currentCampaign=null;const old=spawnEnemy;spawnEnemy=function(){const e=old.apply(this,arguments);if(cb112Own(e))window.currentCampaign=e;return e;};}''');p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(9)}',timeout=180000)
 for j in range(100):
  q=p.evaluate('''()=>{for(let i=0;i<60;i++){Input.clearTaps();updatePlay(1/60);if(i%2===0){ctx.setTransform(SS,0,0,SS,0,0);window.__bofFrames++;drawWorld(1/30);drawEncounterClocks();}}const e=currentCampaign;return{stageTimer,waveIdx,mini:subBossActive,miniWarning:subBossTriggered,boss:bossActive,bossWarning:bossWarned,current:e?{phase:e._cb112.phase,age:e._cb112.age,hp:e.hp,max:e.maxhp,dead:e.dead}:null,complete:CB112.events.some(e=>e.event==='arsenal-complete')};}''');rows.append(q);p.wait_for_timeout(3)
  if j%15==0:print(j,q,flush=True)
  if q['mini']or errors:break
 p.screenshot(path=str(O/'native-campaign-handoff.png'));b.close()
ok=not errors and any(x['current']for x in rows)and any(x['complete']for x in rows)and rows[-1]['mini']and not rows[-1]['bossWarning']and rows[-1]['stageTimer']<42;(O/'campaign.json').write_text(json.dumps(dict(passed=ok,rows=rows,errors=errors),indent=2));print('PASS'if ok else'FAIL','Native campaign Current arsenal and miniboss handoff',rows[-1]);sys.exit(0 if ok else 1)
