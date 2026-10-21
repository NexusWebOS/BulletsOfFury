from pathlib import Path
import ast,base64,json,http.server
from playwright.sync_api import sync_playwright
import shoot
R=Path(__file__).resolve().parents[1];O=R/'_ART_SOURCES/boss_redesign_1020';http.server.ThreadingHTTPServer.request_queue_size=128;port,stop=shoot.serve(str(R));errors=[]
t=ast.parse((R/'_BUILD_SOURCE/probe_feedback_1002.py').read_text());SETUP=next(ast.literal_eval(n.value) for n in t.body if isinstance(n,ast.Assign) and any(isinstance(x,ast.Name) and x.id=='SETUP' for x in n.targets))
t=ast.parse((R/'_BUILD_SOURCE/export_phoenix_1020.py').read_text());CAPTURE=next(n.args[0].value for n in ast.walk(t) if isinstance(n,ast.Call) and n.args and isinstance(n.args[0],ast.Constant) and isinstance(n.args[0].value,str) and 'const c=document.createElement' in n.args[0].value)
try:
 with sync_playwright() as pw:
  b=pw.chromium.launch(channel='msedge',args=['--mute-audio']);p=b.new_page();p.set_default_timeout(180000);p.on('pageerror',lambda e:errors.append(str(e)));p.goto(f'http://127.0.0.1:{port}');p.wait_for_function('window.__bofFrames>4');p.evaluate(shoot.TRAP_RAF);p.evaluate(SETUP,dict(stage=8,kind='vileexistence',pilot='cole'));p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(8)&&v18Warm();}')
  for form,name in [(2,'volcano'),(8,'hammer')]:
   p.evaluate('form=>{B=boss;v18Clear(B);v18Budget(B);v18Enter(B,2,form);B._r30.mode="v18formIn";B.flash=0;B.parts.forEach(p=>p.flash=0);}',form);row=p.evaluate(CAPTURE);(O/(name+'-native.png')).write_bytes(base64.b64decode(row.pop('png')));(O/(name+'-native.json')).write_text(json.dumps(row,indent=2));print(name,len(row['parts']),errors,flush=True)
  b.close()
finally:stop()
