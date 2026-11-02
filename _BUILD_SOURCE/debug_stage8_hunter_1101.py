from pathlib import Path
import json,sys
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'_BUILD_SOURCE'));from shoot import TRAP_RAF
from probe_stage8_cases_1101 import CASES,SETUP
O=R/'_shots/stage8_amplify_1101';checks=[];errors=[]
def ck(n,ok,d=None):
 checks.append(dict(name=n,passed=bool(ok),data=d));print('PASS'if ok else'FAIL',n,flush=True);(O/'edge-checks.json').write_text(json.dumps(checks,indent=2))
with sync_playwright()as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required']);p=b.new_page(viewport=dict(width=1280,height=800));p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text)if m.type=='error'or'draw error'in m.text else None)
 p.add_init_script("Object.defineProperty(navigator,'getGamepads',{value:()=>[]});");p.goto('http://127.0.0.1:8805/game/index.html',wait_until='load',timeout=180000);p.wait_for_function('window.__bofFrames>5');p.mouse.click(3,3);p.evaluate(TRAP_RAF);p.add_script_tag(path=str(R/'_BUILD_SOURCE/enemy_behaviour_lab_1011.js'));p.evaluate('EA11.setup(8,"furious")');p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(8)&&s811Keys().every(k=>XART.rdy(k))}',timeout=180000)
 p.evaluate(SETUP,'s8hunter');q=p.evaluate("""()=>{player.x=worldWidth()/2+85;player.y=VH-80;let hits=0,turns=new Set(),peak=0,closest=999,snapshot=null;const hit=playerHit;playerHit=function(why){if(why==='alien lash')hits++;};for(let i=0;i<900;i++){player.invuln=0;updatePlay(1/60);if(E._s811.attack==='lash'){turns.add(v31Dir(E._s811.head));peak=Math.max(peak,E.y);for(const arm of s811M(E).arms)for(const seg of s811Arm(E,arm)){const d=s81003Distance(player.x,player.y,{x:seg.p.x,y:seg.p.y,ex:seg.tip.x,ey:seg.tip.y});if(d<closest){closest=d;snapshot={player:{x:player.x,y:player.y},enemy:{x:E.x,y:E.y},seg,phase:E._s811.phase,t:E._s811.t,VH,PLAY};}}}}playerHit=hit;return{hits,turns:[...turns],peak,closest,snapshot};}""");ck('Hunter turns and its committed lashes can actually reach the pilot',q['hits']>0 and len(q['turns'])>1,q)

 print(json.dumps(checks,indent=2));p.screenshot(path=str(O/'hunter-lunge-debug.png'));b.close()
