from pathlib import Path
import json
from playwright.sync_api import sync_playwright
from shoot import serve,TRAP_RAF,STEP
R=Path(__file__).resolve().parents[1];O=R/'_shots/chronos_contract_1025';O.mkdir(exist_ok=True)
port,stop=serve(str(R))
try:
 with sync_playwright() as pw:
  b=pw.chromium.launch(channel='msedge',args=['--autoplay-policy=no-user-gesture-required']);p=b.new_page(viewport={'width':1280,'height':800})
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>5',timeout=180000);p.mouse.click(3,3);p.evaluate(TRAP_RAF);p.wait_for_timeout(30)
  p.evaluate("()=>{diffKey='furious';debugStartFight({stage:5,role:'boss',kind:'chromehammer'},{pilot:'cole'});bi24Warm();}")
  p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(5)&&bi24Warm()&&ht23Warm()}',timeout=180000)
  for i in range(170):
   p.evaluate('player.invuln=999');p.evaluate(STEP,12);p.wait_for_timeout(2)
  r=p.evaluate("""()=>{const images=[],d=ctx.drawImage;ctx.drawImage=function(im,...args){const key=HA21.tags.get(im)||FV21.tags.get(im)||'';if(/portal|gate|warp/i.test(key))images.push({key,args});return d.call(this,im,...args)};try{drawWorld(0)}finally{ctx.drawImage=d}return {images,state:boss?._hammer?.state,s5run,s5GateOut,warp:run._s5GateOut,armor:fr27Armor(boss)};}""");print(json.dumps(r),flush=True);p.screenshot(path=str(O/'before.png'))
  for bank in ['chronos_kneel','chronos_kneel_armor','chronos_hold_armor']:
   r=p.evaluate("""name=>{const q=bi24Sample(name,.5);if(!q)return null;const a=q.a,im=XART.get(a.key);return {a,url:im?.toDataURL?.()};}""",bank)
   # BI banks are sheets; metadata enough for local crop.
   if r:(O/(bank+'.json')).write_text(json.dumps(r))
  b.close()
finally:stop()
