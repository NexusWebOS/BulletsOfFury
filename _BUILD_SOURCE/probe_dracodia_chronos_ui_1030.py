from pathlib import Path
import sys,json,http.server
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];W=R/'_shots/dracodia_chronos_1030/ui';W.mkdir(parents=True,exist_ok=True);sys.path.insert(0,str(R/'_BUILD_SOURCE'));from shoot import serve,STEP
from barrage_review_common_1025 import boot
http.server.ThreadingHTTPServer.request_queue_size=256;errors=[]
port,stop=serve(str(R))
try:
 with sync_playwright()as pw:
  br=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required']);p=boot(br.new_context(viewport={'width':1280,'height':800}),port,8,errors,'boss');p.evaluate("()=>{window.B=boss;v18Enter(B,2,8);B._r30.mode='fight';B.enter=false;hb20Start(B,'armor');}");p.evaluate(STEP,120);p.evaluate('()=>{drawWorld(0);SC12.refresh();__bofFit()}');p.screenshot(path=str(W/'final-dialogue.png'))
  q=p.evaluate('({panel:CD27.last,content:CD27.history.at(-1),portraitReady:XART.rdy("rd74_portrait"),clock:hb20State(B).action.t,view:[VW,VH]})');checks=[dict(name='Camera-space portrait bay remains fully inside the play view',passed=q['panel']['x']>=0 and q['panel']['x']+q['panel']['w']<=q['view'][0]),dict(name='Actual Dracodia portrait is supplied to the compact bay',passed=q['portraitReady']and q['content']['port']=='rd74_portrait'),dict(name='Combat continues while the portrait announcement types',passed=q['clock']>1.9),dict(name='No UI/browser errors',passed=not errors)];(W/'ui-checks.json').write_text(json.dumps(dict(checks=checks,layout=q,errors=errors),indent=2));print(json.dumps(checks),flush=True);assert all(c['passed']for c in checks);br.close()
finally:stop()
