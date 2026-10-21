from pathlib import Path
from PIL import Image
import ast,base64,http.server,json
from playwright.sync_api import sync_playwright
import shoot
R=Path(__file__).resolve().parents[1];O=R/'_ART_SOURCES/dracodia_phoenix_1020'
SETUP=next(ast.literal_eval(n.value) for n in ast.parse((R/'_BUILD_SOURCE/probe_feedback_1002.py').read_text()).body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='SETUP' for t in n.targets))
http.server.ThreadingHTTPServer.request_queue_size=128;port,stop=shoot.serve(str(R));errors=[]
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(channel='msedge',args=['--mute-audio']);p=br.new_page(viewport=dict(width=1400,height=1000));p.set_default_timeout(180000);p.on('pageerror',lambda e:errors.append(str(e)))
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>4');p.evaluate(shoot.TRAP_RAF);p.evaluate(SETUP,dict(stage=8,kind='vileexistence',diff='normal',pilot='cole'));p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(8)&&v18Warm()}',polling=80)
  p.evaluate('()=>{B=boss;v18Budget(B);v18Enter(B,2,2);B._r30.mode="v18formIn";B.parts.forEach(q=>{q.destroyed=false;q.flash=0});B.flash=0;}')
  row=p.evaluate('''()=>{const c=document.createElement('canvas');c.width=c.height=256;const g=c.getContext('2d'),names=['save','restore','translate','rotate','scale','drawImage'],props=['globalAlpha','globalCompositeOperation','imageSmoothingEnabled'],saved={},pd={};g.translate(128,128);g.scale(.5,.5);g.translate(-B.x,-B.y);g.imageSmoothingEnabled=false;try{for(const name of props){pd[name]=Object.getOwnPropertyDescriptor(ctx,name);Object.defineProperty(ctx,name,{configurable:true,get:()=>g[name],set:v=>g[name]=v});}for(const n of names){saved[n]=ctx[n];ctx[n]=(...args)=>g[n](...args);}v19Body(B);}finally{for(const n of names)ctx[n]=saved[n];for(const name of props){delete ctx[name];if(pd[name])Object.defineProperty(ctx,name,pd[name]);}}return{png:c.toDataURL().split(',')[1],size:v18Size(B),parts:v18Rig(B).map(v=>v.key)};}''')
  (O/'native-reference.png').write_bytes(base64.b64decode(row.pop('png')));(O/'native-reference.json').write_text(json.dumps(dict(**row,errors=errors),indent=2));print(json.dumps(dict(parts=len(row['parts']),errors=errors)),flush=True);br.close()
finally:stop()
