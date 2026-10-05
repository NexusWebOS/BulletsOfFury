from pathlib import Path
import json,base64,sys
from playwright.sync_api import sync_playwright
import shoot as sh
R=Path(__file__).resolve().parents[1];O=R/'_shots/finale_structure_1003j';O.mkdir(parents=True,exist_ok=True)
port,stop=sh.serve(str(R))
try:
 with sync_playwright() as pw:
  b=pw.chromium.launch(args=['--no-sandbox','--autoplay-policy=no-user-gesture-required']);p=b.new_page(viewport={'width':1100,'height':960})
  p.goto(f'http://127.0.0.1:{port}/index.html',timeout=120000);p.wait_for_function('()=>window.__bofFrames>4',timeout=120000);p.evaluate(sh.TRAP_RAF)
  setup=(R/'_BUILD_SOURCE/probe_feedback_1002.py').read_text().split('SETUP="""')[1].split('"""')[0]
  rows=[]
  for diff in ['easy','normal','hard','furious','insanity']:
   for stage,kind in [(1,'damkeeper'),(2,'infernoreaver'),(3,'cryospear'),(4,'stormsovereign'),(5,'chromehammer'),(6,'chaosharrier'),(7,'sludgeemperor'),(8,'vileexistence')]:
    p.evaluate(setup,{'stage':stage,'kind':kind,'diff':diff})
    p.evaluate('()=>{updateBoss(1/60);updateBoss(1/60);}')
    rows.append(p.evaluate('()=>({stage:run.stage,diff:diffKey,kind:B._ship||B.kind,name:B.name,hp:B.maxhp,armor:B._frArmor?.max,flags:Object.keys(B).filter(k=>k.startsWith("_"))})'))
  (O/'source-bosses-live.json').write_text(json.dumps(rows,indent=2))
  p.wait_for_function('()=>{r30Warm();return ["r30_possessed_body","r30_colossus_body","vile25_ghost_claw","vile24_alien_final","vile24_robot_gray"].every(k=>XART.rdy(k));}',timeout=60000)
  p.evaluate('()=>{ctx.setTransform(SS,0,0,SS,0,0);ctx.fillStyle="#102030";ctx.fillRect(0,0,VW,VH);for(const [i,k] of ["vile24_robot_gray","r30_possessed_body","vile25_ghost_claw","r30_colossus_body","vile24_alien_final"].entries()){ctx.drawImage(XART.get(k),20+(i%3)*155,35+Math.floor(i/3)*230,130,180);ctx.fillStyle="white";ctx.font="9px sans-serif";ctx.fillText(k,15+(i%3)*155,225+Math.floor(i/3)*230);}}')
  (O/'approved-art.png').write_bytes(base64.b64decode(p.evaluate('()=>cv.toDataURL().split(",")[1]')))
  print(json.dumps([{k:v for k,v in r.items() if k!='flags'} for r in rows]))
  b.close()
finally:stop()
