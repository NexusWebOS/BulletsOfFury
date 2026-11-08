"""Scoped native route and NG+ compatibility for the SJ120 owner."""
from pathlib import Path
import sys,json
from playwright.sync_api import sync_playwright
W=Path(__file__).resolve().parent;R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');sys.path.insert(0,str(R/'_BUILD_SOURCE'));from shoot import serve,TRAP_RAF
checks=[];errors=[]
def ck(n,ok,data=None):checks.append(dict(name=n,passed=bool(ok),data=data));print('PASS'if ok else'FAIL',n,flush=True)
port,stop=serve(str(R))
try:
 with sync_playwright()as pw:
  b=pw.chromium.launch(channel='msedge',headless=True);p=b.new_page(viewport={'width':1280,'height':800});p.on('pageerror',lambda e:errors.append(str(e)))
  p.goto(f'http://127.0.0.1:{port}/index.html?quality=high',wait_until='load',timeout=180000);p.wait_for_function('window.__bofFrames>5');p.evaluate(TRAP_RAF);p.add_script_tag(path=str(R/'_BUILD_SOURCE/enemy_behaviour_lab_1011.js'))
  d=p.evaluate("()=>{EA11.setup(7,'hard');spawnBoss('sludgeemperor');return{hp:boss.maxhp,tandem:!!boss._sj120,warden:!!boss._s7warden};}");ck('Hard Stage 7 boss keeps its 12,466 HP and original owner',d['hp']==12466 and d['warden']and not d['tandem'],d)
  d=p.evaluate("()=>{EA11.setup(7,'hard');run.ngplus=false;spawnSubBoss('dualscoopdredger');return{kind:subBoss.kind,tandem:!!subBoss._sj120,old:subBoss._ship==='dualscoopdredger'&&!subBoss._sj98};}");ck('Hard Stage 7 retains its original Dredger miniboss',not d['tandem']and d['old'],d)
  d=p.evaluate("()=>{EA11.setup(6,'furious');spawnSubBoss('siegefortress17');return{razor:!!subBoss._rw118,sump:!!subBoss._sj120};}");ck('Furious Stage 6 still selects Razorwake',d['razor']and not d['sump'],d)
  d=p.evaluate("()=>{EA11.setup(6,'furious');spawnBoss('thunderhead');return{reactor:!!boss._tc119,sump:!!boss._sj120};}");ck('Furious Stage 6 still selects the Thunderhead reactor',d['reactor']and not d['sump'],d)
  d=p.evaluate("()=>{EA11.setup(7,'furious');run.ngplus=true;spawnSubBoss('dualscoopdredger');const b=subBoss;return{hp:b.maxhp,actors:b._sj98.actors.map(a=>({hp:a.maxhp,pools:a.pools.reduce((s,p)=>s+p.hp,0)}))};}");ck('NG+ keeps the native 25 percent health increase and equal pool shares',d['hp']==17500 and all(a['hp']==8750 and a['pools']==8750 for a in d['actors']),d)
  ck('No compatibility browser errors',not errors,errors);b.close()
finally:stop()
(W/'compat-report.json').write_text(json.dumps(dict(checks=checks,errors=errors),indent=2));raise SystemExit(0 if all(c['passed']for c in checks)else 1)
