"""Check late helper pools and ensure the native cannon solver scales once."""
from pathlib import Path
import sys,json
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'_BUILD_SOURCE'));from shoot import TRAP_RAF
O=R/'_shots/waves_all_1101';checks=[];errors=[]
def ck(name,passed,data=None):
 checks.append(dict(name=name,passed=bool(passed),data=data));print('PASS' if passed else 'FAIL',name,flush=True)
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required']);p=b.new_page(viewport={'width':1280,'height':800});p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
 p.goto('http://127.0.0.1:8805/game/index.html',wait_until='load',timeout=180000);p.wait_for_function('window.__bofFrames>5');p.mouse.click(3,3);p.evaluate(TRAP_RAF);p.add_script_tag(path=str(R/'_BUILD_SOURCE/enemy_behaviour_lab_1011.js'))
 q=p.evaluate('''()=>{const tag=Object.keys(BOFX.mechboss).find(k=>_mechMeta(k));player.x=700;player.y=650;return Object.fromEntries(DR15.keys.map(k=>{diffKey=k;const b={x:300,y:100,w:352,_mech:{tag,phase:'fight',parts:{'left-cannon':{state:'live',_aim:0},'right-cannon':{state:'live',_aim:0}}}};mechAimCannons(b,1/60);return[k,b._mech.parts['left-cannon']._aim];}));}''')
 ck('Native mech cannon angular solver receives exactly one difficulty scale',abs(q['hard']/q['normal']-1.15)<1e-8 and abs(q['furious']/q['hard']-1.15)<1e-8,q)
 rows={}
 for diff in ['normal','hard','furious']:
  rows[diff]=p.evaluate('''d=>{EA11.setup(4,d);bossWarned=false;spawnBoss(curStage.boss);const b=boss;b._s4war.coreTurrets=[];b._s4war.coreGeneration=0;stage4CoreTurretSpawnMissing(b,1);return{turrets:b._s4war.coreTurrets.map(t=>({hp:t.maxhp,shield:t.maxShield})),config:stage4CoreDifficulty()};}''',diff)
 for key in ['hp','shield']:
  ck('Native Stage4 late helper '+key+' pool follows the shared curve',all(abs(rows[d]['turrets'][0][key]-rows['normal']['turrets'][0][key]*f)<=1 for d,f in [('hard',1.15),('furious',1.3225)]),{d:v['turrets'] for d,v in rows.items()})
 ck('Native Stage4 aim and diagonal fire cadence use compound15%',all(abs(rows[d]['config']['aimGain']/rows['normal']['config']['aimGain']-f)<1e-8 and abs(rows['normal']['config']['diagBeat']/rows[d]['config']['diagBeat']-f)<1e-8 for d,f in [('hard',1.15),('furious',1.3225)]))
 q=p.evaluate('()=>({copies:DR15.keys.map(k=>J3_SOURCE_HP[k]),training:DR15.keys.map(k=>IC21_TUNING[k].hp)})')
 for key in ['copies','training']:
  ck(key+' persistent health rows derive from the Normal source',all(abs(hp-q[key][0][i]*f)<=.51 for row,f in [(1,1.15),(2,1.3225)] for i,hp in enumerate(q[key][row])),q[key])
 ck('No runtime or console errors',not errors,errors);b.close()
(O/'difficulty-followups.json').write_text(json.dumps(checks,indent=2));print('SUMMARY',sum(x['passed'] for x in checks),'/',len(checks));sys.exit(0 if all(x['passed'] for x in checks) else 1)
