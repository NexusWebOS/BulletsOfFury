from pathlib import Path
import sys,json
from playwright.sync_api import sync_playwright
W=Path(__file__).resolve().parent;R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');sys.path.insert(0,str(R/'_BUILD_SOURCE'));from shoot import serve,TRAP_RAF
checks=[];errors=[]
def ck(n,ok,d=None):checks.append(dict(name=n,passed=bool(ok),data=d));print('PASS'if ok else'FAIL',n,flush=True)
port,stop=serve(str(R))
try:
 with sync_playwright()as pw:
  b=pw.chromium.launch(channel='msedge',headless=True);p=b.new_page(viewport={'width':1280,'height':800});p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:500])if m.type=='error'or'draw error'in m.text else None)
  p.goto(f'http://127.0.0.1:{port}/index.html?quality=high',wait_until='load',timeout=180000);p.wait_for_function('window.__bofFrames>5');p.evaluate(TRAP_RAF);p.add_script_tag(path=str(R/'_BUILD_SOURCE/enemy_behaviour_lab_1011.js'))
  p.evaluate("()=>{EA11.setup(5,'normal');}");ck('Normal cannot select the Furious Stage 6 alternate',p.evaluate('()=>!fb112Rank()'))
  for diff in ['hard']:
   d=p.evaluate("d=>{EA11.setup(6,d);spawnSubBoss('siegefortress17');return{kind:subBoss.kind,alternate:!!subBoss._rw118,cargo:!!subBoss._cargo13,hp:subBoss.hp};}",diff);ck(diff+' keeps native fortress miniboss',d['cargo']and not d['alternate'],d)
  d=p.evaluate("()=>{EA11.setup(6,'furious');run._gp4StageX=true;return{rank:fb112Rank()};}");ck('Stage X is excluded from the Furious alternate selector',not d['rank'])
  p.evaluate("()=>{EA11.setup(6,'furious');run._gp4StageX=false;DBGT.god=true;spawnBoss('thunderhead');}");p.wait_for_function('()=>{stageLoadTick();return fb112Ready()&&stageLoadReady(6)}',timeout=180000)
  d=p.evaluate("()=>{const b=boss,q=b._fb112;for(let i=0;i<3600;i++){updatePlay(1/60);if(i%12===0){ctx.setTransform(SS,0,0,SS,0,0);drawWorld(1/60);}}return{modular:tm115Own(b),razor:!!b._rw118,parts:q.parts.length,core:q.core.hp,events:TM115.events.length};}");ck('Furious Thunderhead retains six modules, storm controller and reachable assets',d['modular']and not d['razor']and d['parts']==6 and d['events']>0,d)
  d=p.evaluate("()=>{const keys=fb112Keys();return{old:keys.filter(k=>k.startsWith('fb114_razor_')||k.startsWith('fb114_shadow_')),thunder:TM115.keys.every(k=>keys.includes(k)&&XART.rdy(k)),new:RW118.keys.every(k=>XART.rdy(k))};}");ck('Obsolete Razorwake pages are excluded while current boss pages stay ready',not d['old']and d['thunder']and d['new'],d)
  ck('No compatibility browser/render errors',not errors,errors);b.close()
finally:stop()
(W/'compat-report.json').write_text(json.dumps(dict(checks=checks,errors=errors),indent=2));raise SystemExit(0 if all(c['passed']for c in checks)else 1)
