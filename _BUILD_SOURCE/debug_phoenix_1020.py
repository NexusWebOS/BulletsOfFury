from pathlib import Path
import ast,json,http.server
from playwright.sync_api import sync_playwright
import shoot
R=Path(__file__).resolve().parents[1];http.server.ThreadingHTTPServer.request_queue_size=128
port,stop=shoot.serve(str(R));errors=[]
SETUP=next(ast.literal_eval(n.value) for n in ast.parse((R/'_BUILD_SOURCE/probe_feedback_1002.py').read_text()).body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='SETUP' for t in n.targets))
try:
 with sync_playwright() as pw:
  b=pw.chromium.launch(channel='msedge',args=['--mute-audio']);p=b.new_page();p.on('pageerror',lambda e:errors.append(str(e)));p.goto(f'http://127.0.0.1:{port}');p.wait_for_timeout(1500);print('errors',errors,flush=True);print(p.evaluate('({frames:window.__bofFrames,ph:typeof PH20,art:typeof PH20_ART})'),flush=True);p.evaluate(shoot.TRAP_RAF);p.evaluate(SETUP,dict(stage=8,kind='vileexistence',diff='normal',pilot='cole'));p.wait_for_timeout(4000);print(p.evaluate('()=>{stageLoadTick();v18Warm();return{ready:stageLoadReady(8),missing:v18Keys().filter(k=>!XART.rdy(k)),errors:[]}}'),flush=True);print('errors',errors,flush=True);b.close()
finally:stop()
