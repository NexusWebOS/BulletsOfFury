from pathlib import Path
from playwright.sync_api import sync_playwright
from shoot import serve, TRAP_RAF
import probe_chronos_glow_1025 as P
R=Path(__file__).resolve().parents[1]; O=R/'_shots/chronos_glow_1025/diag_release'; O.mkdir(parents=True,exist_ok=True)
port,stop=serve(str(R))
try:
  with sync_playwright() as pw:
    br=pw.chromium.launch(channel='msedge'); p=br.new_page(viewport={'width':1280,'height':800})
    p.goto(f'http://127.0.0.1:{port}/index.html')
    p.wait_for_function("window.__bofFrames>5&&typeof CG!=='undefined'&&typeof c32Warm==='function'",timeout=180000)
    p.mouse.click(3,3);p.evaluate(TRAP_RAF);p.evaluate(P.SETUP);p.wait_for_function(P.READY,timeout=180000)
    p.evaluate("()=>{const h=boss._hammer;h.hb20Pickup=null;if(h.frArmor){h.frArmor.activated=false;h.frArmor.hp=0;}h.state='hammer';h._hf22Red=false;h.c27RagePending=true;boss.hp=boss.maxhp*.1;hf22BeginBlueRage(boss);}")
    for name,js in (('as_is',''),('noflash','C.c45Flash=0;'),('noparticles','particles.length=0;'),('noscreen','flashScreen=0;')):
      p.evaluate("""js=>{const h=boss._hammer,C=h._hf22Charge;for(let i=0;i<8;i++){C.t=1.8*(.90+i*.004);boss.x=340;boss.y=260;efxClock+=1/30;drawWorld(0);}
        eval(js);boss.x=340;boss.y=260;C.t=1.8*.935;drawWorld(0);}""", js)
      p.screenshot(path=str(O/f'{name}.png'),clip={'x':380,'y':160,'width':520,'height':520})
      p.evaluate("()=>{const h=boss._hammer,C=h._hf22Charge;C.c45Final=false;C.c45N=0;C.c45Live=[];}")
    br.close()
finally: stop()
