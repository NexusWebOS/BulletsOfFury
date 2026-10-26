from pathlib import Path
from playwright.sync_api import sync_playwright
from shoot import serve, TRAP_RAF, STEP
import json

R=Path(__file__).resolve().parents[1]
O=R/'_shots/bullethell_1025';O.mkdir(parents=True,exist_ok=True)
port,stop=serve(str(R));out=[]
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(channel='msedge',args=['--autoplay-policy=no-user-gesture-required'])
  p=br.new_page(viewport={'width':1280,'height':800})
  p.goto(f'http://127.0.0.1:{port}/index.html',wait_until='load',timeout=180000)
  p.wait_for_function('window.__bofFrames>5',timeout=180000);p.evaluate(TRAP_RAF)
  print(json.dumps(p.evaluate("debugFightList().filter(f=>f.role==='mini')")),flush=True)
  for stage in range(1,10):
   q=p.evaluate("""stage=>{const E=debugFightFor(stage,'mini');if(!E)return null;debugUnlocked=true;diffKey='furious';debugStartFight(E,{pilot:'cole'});spawnSubBoss(E.kind);debugFight.spawned=true;warnT=0;DBGT.god=true;BOFCinematicDirector.cancel();return{entry:E,keys:Object.keys(subBoss||{}),data:JSON.parse(JSON.stringify(subBoss,(k,v)=>['owner','b','parent','slots','el'].includes(k)?undefined:v))};}""",stage)
   out.append(q);print(json.dumps(q),flush=True)
  br.close()
finally:
 stop();(O/'inventory.json').write_text(json.dumps(out,indent=2),encoding='utf8')
