from pathlib import Path
import ast,base64,json,http.server
import shoot as sh
from playwright.sync_api import sync_playwright
OUT=Path('_shots/overnight_0927/entry');OUT.mkdir(parents=True,exist_ok=True)
tree=ast.parse(Path('_BUILD_SOURCE/probe_polish_0927b.py').read_text(encoding='utf-8'))
SETUP=next(ast.literal_eval(n.value) for n in tree.body if isinstance(n,ast.Assign) and isinstance(n.targets[0],ast.Name) and n.targets[0].id=='SETUP')
http.server.SimpleHTTPRequestHandler.log_message=lambda *a:None
port,stop=sh.serve(sh.GAME);errors=[];out=[]
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(args=['--no-sandbox','--mute-audio']);p=br.new_page(viewport={'width':1100,'height':1100})
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('()=>window.__bofFrames>5');p.evaluate(sh.TRAP_RAF)
  for stage,kind,mini in [(2,'magmaward',True),(3,'frostcruiser',True),(3,'cryospear',False),(4,'stormsovereign',False),(9,'voidhorizon',True)]:
   c={'stage':stage,'kind':kind,'mini':mini,'diff':'normal'};p.evaluate(SETUP,c)
   p.evaluate("()=>{timeScale=1;special=null;run.sonicT=run.dkT=0;s6Opening=null;window.motion={activeMax:0,arrival:[],entered:false};}")
   for sec in range(8):
    p.evaluate("""()=>{for(let i=0;i<60;i++){const was=B.enter,x=B.x,y=B.y;updatePlay(1/60);const d=Math.hypot(B.x-x,B.y-y);if(!was&&!B.enter)motion.activeMax=Math.max(motion.activeMax,d);if(was&&!B.enter){motion.entered=true;motion.arrival.push({x:B.x,y:B.y,step:d});}if(i%6===0){ctx.setTransform(SS,0,0,SS,0,0);drawWorld(.1);}}}""")
    p.wait_for_timeout(25)
    if sec in [1,2,3]: (OUT/f'{kind}-{sec}.png').write_bytes(base64.b64decode(p.evaluate('()=>ctx.canvas.toDataURL()').split(',')[1]))
   out.append(p.evaluate('c=>({...c,...motion})',c))
  br.close()
finally:stop()
(OUT/'report.json').write_text(json.dumps({'cases':out,'errors':errors},indent=2),encoding='utf-8');print(json.dumps(out,indent=2));assert not errors,errors
assert all(c['activeMax']<12 and c['entered'] for c in out)
