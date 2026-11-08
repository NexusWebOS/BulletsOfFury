from pathlib import Path
import sys,json
from playwright.sync_api import sync_playwright
W=Path(__file__).resolve().parent;R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');sys.path.insert(0,str(R/'_BUILD_SOURCE'));from shoot import serve,TRAP_RAF
port,stop=serve(str(R))
try:
 with sync_playwright()as pw:
  b=pw.chromium.launch(channel='msedge',headless=True);p=b.new_page();p.goto(f'http://127.0.0.1:{port}/index.html?quality=high',wait_until='load',timeout=180000);p.wait_for_function('window.__bofFrames>5');p.evaluate(TRAP_RAF);p.add_script_tag(path=str(R/'_BUILD_SOURCE/enemy_behaviour_lab_1011.js'))
  hard=p.evaluate("()=>{EA11.setup(7,'hard');spawnBoss('sludgeemperor');return{kind:boss.kind,hp:boss.hp,maxhp:boss.maxhp,structure:boss._s7mod,keys:Object.keys(boss).filter(k=>k.startsWith('_s7')||k.startsWith('_sew')),attackSpeed:turretInterval15(.2)};}")
  fury=p.evaluate("()=>{EA11.setup(7,'furious');spawnSubBoss('dualscoopdredger');return{hp:subBoss.hp,actors:subBoss._sj98.actors.map(a=>({maxhp:a.maxhp,pools:a.pools.map(p=>p.hp)})),attackSpeed:turretInterval15(.2)};}");print('HARD',json.dumps(hard)[:1900],flush=True);print('FURIOUS',json.dumps(fury),flush=True);(W/'baseline.json').write_text(json.dumps(dict(hard=hard,furious=fury),indent=2));b.close()
finally:stop()
