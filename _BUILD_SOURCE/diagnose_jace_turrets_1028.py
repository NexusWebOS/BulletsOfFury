from pathlib import Path
import ast,json
from playwright.sync_api import sync_playwright
import shoot
R=Path(__file__).resolve().parents[1]
def strings(f):return[n.value for n in ast.walk(ast.parse((R/f).read_text(encoding='utf8')))if isinstance(n,ast.Constant)and isinstance(n.value,str)]
setup=next(s for s in strings('_BUILD_SOURCE/probe_feedback_1002.py')if s.startswith('c=>{ht27Stop'));init=next(s for s in strings('_BUILD_SOURCE/probe_rebel_balance_1019.py')if s.startswith('gang=>{window.R='));hold=next(s for s in strings('_BUILD_SOURCE/record_jace_turrets_1028.py')if s.startswith('()=>{G.rescueAt='))
port,stop=shoot.serve(str(R))
try:
 with sync_playwright()as pw:
  b=pw.chromium.launch(channel='msedge');p=b.new_page();p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>5');p.evaluate(shoot.TRAP_RAF);p.evaluate('()=>{run.stage=6;stageLoadBegin(6)}');p.evaluate(setup,dict(stage=6,kind='rebelsquad',diff='normal',pilot='cole'));p.evaluate(init,True);p.wait_for_function('()=>{stageLoadTick();rr26Warm();return stageLoadReady(6)&&Object.keys(JR36_TURRETS).every(k=>XART.rdy(k))}');p.evaluate('window.captureStart=performance.now()');p.evaluate(hold)
  data=p.evaluate("""()=>{const rows=[];for(let i=0;i<900;i++){updatePlay(1/60);if(i%15===0){const T=jace.rg4._rbal19Gun;rows.push({t:G.age,n:jace.rg4.gunN,cd:jace.rg4.gunCd,tell:T?.t,alive:ra4Alive(jace),stun:jace.stun,cloak:jace.frCloak,evade:jace.evadeT,scale:jace._rd21Scale,act:jace.rg4.act?.kind,fleet:!!G.rd21.fleet,slots:rbal19Cfg().slots,muzzle:!!jr36Turret(jace,1),hp:jace.hp});}}return{rows,events:RBAL19.events,muzzles:jrMuzzleLog};}""")
  (R/'_shots/jace_turrets_1028/diagnostic.json').write_text(json.dumps(data,indent=2));print(json.dumps(data));b.close()
finally:stop()
