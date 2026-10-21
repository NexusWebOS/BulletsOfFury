from pathlib import Path
from playwright.sync_api import sync_playwright
import ast,json,base64
R=Path(__file__).resolve().parents[1];W=R/'_ART_SOURCES/ui_production_1020';O=R/'_shots/ui_production_1020';errors=[];checks=[]
SETUP=next(ast.literal_eval(n.value) for n in ast.parse((R/'_BUILD_SOURCE/probe_feedback_1002.py').read_text(encoding='utf-8')).body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='SETUP' for t in n.targets))
def ck(n,v):checks.append(dict(name=n,passed=bool(v)));print(('PASS ' if v else 'FAIL ')+n,flush=True)
import sys,atexit
sys.path.insert(0,str(R/'_BUILD_SOURCE'))
import shoot
port,stop=shoot.serve(str(R));atexit.register(stop)
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge');p=b.new_page(viewport=dict(width=1920,height=1080));p.set_default_timeout(120000);p.on('pageerror',lambda e:errors.append(str(e)));p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>4');p.evaluate('()=>{window.requestAnimationFrame=()=>0;}');p.wait_for_timeout(60)
 p.evaluate(SETUP,dict(stage=4,kind='stormsovereign',pilot='cole'));p.evaluate('()=>st18Say(boss,"ui20-test","The cores are charging. Keep moving and watch their electrical bursts.",true)');p.wait_for_function('()=>{SC12.refresh();return UI20.radio&&UI20_KEYS.every(k=>XART.rdy(k));}');p.evaluate('()=>{ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);SC12.invalidate();SC12.refresh();}');p.screenshot(path=str(O/'stage4-radio.png'));ck('Stage4 radio stays in HUD and retains secondary status',p.evaluate('()=>UI20.radio.text.includes("cores")&&UI20.last[0].secondary==="NUCLEAR WARHEADS"'))
 p.evaluate('()=>{boss._st18.radio=null;SC12.refresh();}');ck('Clearing radio restores normal secondary instrument',p.evaluate('UI20.radio===null'))
 p.evaluate(SETUP,dict(stage=8,kind='vileexistence',pilot='cole'));p.wait_for_function('()=>{stageLoadTick();dr5Warm();return stageLoadReady(8)&&v18Warm()&&XART.rdy(DP20.key);}');p.evaluate('''()=>{v18Budget(boss);v18Enter(boss,2,0);v18Fight(boss);H3.release=false;H3.ending=null;fb2Talk=fb2Intro=s6Opening=null;BOFCinematicDirector.cancel();AP10_X.intro=null;story=null;boss.x=worldWidth()/2;boss.y=PLAY.y+168;boss._r30.mode='dr5Monologue';boss._r30.t=2;boss._r30.clock=2;boss.enter=boss._noHit=true;dr5Say(boss,'DRACODIA',DR5.intro[0][0],3);dr5State(boss).radio.t=1;ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);}''');p.screenshot(path=str(O/'dracodia-dialogue.png'));ck('Native Dracodia dialogue uses proper dedicated portrait in new frame',p.evaluate('()=>UI20.dialogue.who==="DRACODIA"&&/^dr5_face_/.test(UI20.dialogue.portrait)&&XART.get(UI20.dialogue.portrait)===XART.get(DP20.key)'))
 ck('No extra renderer or radio errors',not errors);b.close()
r=json.loads((O/'report.json').read_text());r['checks']+=checks;r['passed']=sum(c['passed'] for c in r['checks']);r['total']=len(r['checks']);r['errors']+=errors;(O/'report.json').write_text(json.dumps(r,indent=2));print(json.dumps({'passed':r['passed'],'total':r['total'],'errors':errors}));raise SystemExit(not all(c['passed'] for c in checks))
