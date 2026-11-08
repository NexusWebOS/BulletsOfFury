"""Native collision boundary fixtures for the faster diagonal passes."""
from pathlib import Path
import json,sys
from playwright.sync_api import sync_playwright
W=Path(__file__).resolve().parent;R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');sys.path.insert(0,str(R/'_BUILD_SOURCE'));from shoot import serve,TRAP_RAF
port,stop=serve(str(R));checks=[];errors=[]
try:
 with sync_playwright()as pw:
  b=pw.chromium.launch(channel='msedge',headless=True);p=b.new_page(viewport={'width':1280,'height':800});p.on('pageerror',lambda e:errors.append(str(e)));p.goto(f'http://127.0.0.1:{port}/index.html?quality=high',wait_until='load',timeout=180000);p.wait_for_function('window.__bofFrames>5');p.evaluate(TRAP_RAF);p.add_script_tag(path=str(R/'_BUILD_SOURCE/enemy_behaviour_lab_1011.js'))
  p.evaluate("()=>{EA11.setup(6,'furious');debugUnlocked=true;DBGT.god=true;spawnSubBoss('razorwake');window.B=subBoss;window.T=B._rw118;window.Q=B._fb112;}");p.wait_for_function('()=>{stageLoadTick();return fb112Ready()&&stageLoadReady(6)}',timeout=180000)
  d=p.evaluate('''()=>{B.enter=false;T.state='throttle-run';T.t=.2;T.hitAt=new Map();Q.heading=Math.PI/4;player.invuln=0;player.dead=false;player.x=worldWidth()/2;player.y=VH*.6;const at={x:player.x,y:player.y};B.x=at.x+500;B.y=at.y+500;T.sweep={x:at.x-500,y:at.y-500};RW118.events=[];rw118Contact(B);const hit=RW118.events.filter(e=>e.event==='contact').length;T.hitAt=new Map();player.invuln=0;player.x=at.x+200;player.y=at.y-200;rw118Contact(B);return{hit,afterMiss:RW118.events.filter(e=>e.event==='contact').length,protected:!player.dead,hp:B.hp};}''')
  checks.append(dict(name='Swept contact catches a crossed pilot when both sampled hull positions are offscreen',passed=d['hit']==1,data=d));checks.append(dict(name='A pilot outside the actual swept lane is safe',passed=d['afterMiss']==1));checks.append(dict(name='Fast-pass contact retains native GOD protection and boss health',passed=d['protected']and d['hp']==1785));checks.append(dict(name='No browser errors',passed=not errors,data=errors));b.close()
finally:stop()
(W/'sweep-checks.json').write_text(json.dumps(dict(checks=checks,errors=errors),indent=2));print(json.dumps(checks));raise SystemExit(0 if all(c['passed']for c in checks)else 1)
