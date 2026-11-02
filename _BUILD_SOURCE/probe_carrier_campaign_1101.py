"""Exercise all four real stage-plan wave callbacks with native firing inputs.
Regular pressure/crew isolated in this QA fixture; no enemy pool/phase/timer writes.
"""
from pathlib import Path
import sys,json
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'_BUILD_SOURCE'));from shoot import TRAP_RAF
O=R/'_shots/carrier_assault_1101';errors=[];trace=[]
with sync_playwright()as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required']);p=b.new_page(viewport={'width':1280,'height':800});p.add_init_script("Object.defineProperty(navigator,'getGamepads',{value:()=>[]});");p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:400])if m.type=='error'or'draw error'in m.text else None)
 p.goto('http://127.0.0.1:8805/game/index.html',wait_until='load',timeout=180000);p.wait_for_function('window.__bofFrames>5');p.mouse.click(3,3);p.evaluate(TRAP_RAF);p.add_script_tag(path=str(R/'_BUILD_SOURCE/enemy_behaviour_lab_1011.js'));p.evaluate('''()=>{EA11.setup(6,'furious');bossWarned=false;story=thaw=fb2Talk=fb2Intro=null;CP12.next=VP12.next=CP22.nextWave=CP22.nextFlyby=99999;_adaptiveSpawnT=99999;stagePlan=buildStagePlan(6).filter(w=>w._ca111);waveIdx=0;playerLocks=[];aiQueue=[];fb2Flights=[];s6WingTick=()=>{};s6WingDraw=()=>{};s6Wing=null;ally=null;run.weapon=3;run.wlevel=5;run.wlevels=WEAPONS.map(()=>5);run.bombs=40;DBGT.god=true;DBGT.speed=1;player.invuln=40002;}''');p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(6)&&Object.values(CA111_ART.banks).every(b=>XART.rdy(b.key))}',timeout=180000)
 for j in range(300):
  q=p.evaluate('''()=>{for(let i=0;i<60;i++){
   Input.clearTaps();for(const k of Object.keys(Input.keys))Input.keys[k]=false;
   const target=_lockTargets().filter(e=>(e._sc12||e._ca111)&&sc12Alive(e)&&e.y>PLAY.y+20&&e.y<VH-65).sort((a,b)=>b.y-a.y)[0];
   const tx=target?.x??worldWidth()/2,ty=VH-55;
   Input.keys.a=player.x>tx+3;Input.keys.d=player.x<tx-3;Input.keys.w=player.y>ty+4;Input.keys.s=player.y<ty-4;Input.keys.j=true;Input.keys.c=!!target;
   if(target&&run.bombs>0&&Math.floor(CA111.clock*60)%100===0)Input.injectTap('k');updatePlay(1/60);
  }drawWorld(0);return{t:CA111.clock,stageTimer,waveIdx,completed:[...CA111.completed],active:CA111.active?.key||null,pending:carrierAssaultPending111(),hold:carrierAssaultHold111(),enemyCount:enemies.length,state,dead:player.dead};}''');trace.append(q);p.wait_for_timeout(3)
  if j%25==0:print('Campaign',round(q['t'],1),'stage',round(q['stageTimer'],1),'completed',q['completed'],flush=True)
  if len(q['completed'])==4 and not q['hold']:break
  if errors:break
 q=p.evaluate('()=>({completed:[...CA111.completed],pending:carrierAssaultPending111(),hold:carrierAssaultHold111(),waves:waveIdx,pairedDefeats:CC111.events.filter(e=>e.event==="complete-defeat").length,strategicDefeats:CA111.events.filter(e=>e.event==="strategic-defeat").length,source:CA111.events})');p.screenshot(path=str(O/'campaign-complete.png'));b.close()
checks=[dict(name='All four native scheduled callbacks run in order',passed=q['completed']==['pair-top','pair-bottom','nuclear','laser']and q['waves']==4),dict(name='Four paired hulls and two strategic hulls genuinely defeated',passed=q['pairedDefeats']==4 and q['strategicDefeats']==2),dict(name='Campaign hold and boss gate release after the final wave',passed=not q['hold']and not q['pending']),dict(name='Native simulation stays live with no browser errors',passed=all(t['state']=='play'and not t['dead']for t in trace)and not errors)]
(O/'campaign-checks.json').write_text(json.dumps(dict(checks=checks,trace=trace,result=q,errors=errors),indent=2));print('SUMMARY',sum(q['passed']for q in checks),'/',len(checks));assert all(q['passed']for q in checks),(checks,q)
