from pathlib import Path
from playwright.sync_api import sync_playwright
import sys,json
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
rows=[];errors=[]
with sync_playwright()as w:
 b=w.chromium.launch(channel='msedge');p=b.new_page();p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text)if m.type=='error'else None)
 p.add_init_script('Object.defineProperty(navigator,"getGamepads",{value:()=>[]})')
 try:
  p.goto('http://127.0.0.1:8765/index.html',wait_until='load',timeout=180000);p.wait_for_function('window.__bofFrames>6');p.evaluate(shoot.TRAP_RAF)
  for label,js in [('before','()=>PF16_IDLE_BASE'),('helper',None),('setup',"()=>EA11.setup(6,'furious')"),('draw','()=>drawWorld(0)')]:
   if label=='helper':p.add_script_tag(path=str(R/'_BUILD_SOURCE/enemy_behaviour_lab_1011.js'))
   else:p.evaluate(js)
   q=p.evaluate('({idle:PF16_IDLE_BASE,state,stage:run.stage})');rows.append({'step':label,**q});print(rows[-1],flush=True)
 except Exception as e:errors.append(str(e));print(str(e),flush=True)
 b.close()
(R/'_shots/release_qa_1116/edge-isolate.json').write_text(json.dumps({'rows':rows,'errors':errors},indent=2),encoding='utf8')
