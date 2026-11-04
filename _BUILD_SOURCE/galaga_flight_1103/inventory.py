from pathlib import Path
import sys,ast,json
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[2];W=Path(__file__).parent
sys.path.insert(0,str(R/'_BUILD_SOURCE'));from shoot import TRAP_RAF
t=ast.parse((R/'_BUILD_SOURCE/probe_feedback_1002.py').read_text(encoding='utf8'))
SETUP=next(ast.literal_eval(n.value)for n in t.body if isinstance(n,ast.Assign)and any(isinstance(x,ast.Name)and x.id=='SETUP'for x in n.targets))
sets={1:['s1jetdelta','s1jetdelta_b'],2:['skim','cinderwasp','lance','ac10firejet','basaltbomber','v31elite_balls'],3:['frost','ac10icejet'],4:['s4interceptor','s4rocket','s4command','s4heavyjet'],5:['s5interceptor','s5skimmer','s5frigate'],6:['l6v_s0','l6v_s1','l6v_s2','l6v_r0','l6v_r1','l6v_r2','s6dart','s6skimmer','s6bomber'],7:['cp22slime','s7missilejet','s8crescent'],8:['s8interceptor','s8needlejet','s8voidjet','s8hellwing','s8laserharrier'],9:['s9comet','wskim','echof','tsplit','s9gunship']}
rows=[];errors=[]
with sync_playwright()as pw:
 b=pw.chromium.launch(channel='msedge',headless=True);p=b.new_page()
 p.route('**/assets/online-config.js',lambda r:r.fulfill(status=200,body='window.BOF_ONLINE_CONFIG={};',content_type='application/javascript'))
 p.on('pageerror',lambda e:errors.append(str(e)));p.goto('http://127.0.0.1:65041/game/index.html',wait_until='load',timeout=180000);p.wait_for_function('window.__bofFrames>4',timeout=60000);p.evaluate(TRAP_RAF)
 for stage,types in sets.items():
  p.evaluate(SETUP,{'stage':stage,'diff':'furious'})
  for typ in types:
   rows.append(p.evaluate('''t=>{const e=spawnEnemy(t,worldWidth()*.3,-180,{});if(!e)return{request:t,stage:run.stage,empty:true};return{stage:run.stage,request:t,type:e.type,pattern:e.pattern,w:e.w,h:e.h,draw:[e._drawW,e._drawH],model:e._v31?.model||e._i31?.model||e._s411?.model||e._s511?.model||e._s611?.model||e._s711?.model||e._s811?.model||e._s911?.model||e._r46?.model,hp:e.hp,flags:{entry:!!e._entrySweep,flight:!!e._cp22Flight,stealth:!!e._fb2Stealth,jet:!!e._jetManeuver},artDirs:e._s611?s611M(e)?.bank.dirs:e._s811?s811M(e)?.bank.dirs:e._s911?s911M(e)?.bank.dirs:e._s711?s711M(e)?.bank.dirs:e._s511?s511M(e)?.bank.dirs:null};}''',typ))
 b.close()
(W/'inventory.json').write_text(json.dumps({'rows':rows,'errors':errors},indent=2),encoding='utf8')
for r in rows:print(r['stage'],r['request'],r.get('type'),r.get('pattern'),r.get('model'),r.get('draw'),r.get('artDirs'),flush=True)
