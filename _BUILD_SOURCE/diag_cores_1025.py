from pathlib import Path
from playwright.sync_api import sync_playwright
from shoot import serve, TRAP_RAF
from probe_chronos_glow_1025 import SETUP, READY, STATES
from PIL import Image
R = Path(__file__).resolve().parents[1]; O = R/'_shots/chronos_glow_1025/cores'; O.mkdir(parents=True, exist_ok=True)
port, stop = serve(str(R)); errs=[]
try:
  with sync_playwright() as pw:
    br = pw.chromium.launch(channel='msedge'); p = br.new_page(viewport={'width':1280,'height':800})
    p.on('pageerror', lambda e: errs.append(str(e)))
    p.goto(f'http://127.0.0.1:{port}/index.html')
    p.wait_for_function("window.__bofFrames>5&&typeof CG!=='undefined'&&typeof c32Warm==='function'", timeout=180000)
    p.mouse.click(3,3); p.evaluate(TRAP_RAF); p.evaluate(SETUP); p.wait_for_function(READY, timeout=180000)
    for st in ('chrome','regular','rage'):
      p.evaluate(STATES[st]); tiles=[]
      for i in range(8):
        p.evaluate("i=>{efxClock=20+i/9+.01;boss.x=340;boss.y=260;boss.flash=0;particles.length=0;boss._hammer._cgPrev={mode:cgMode(boss).mode};shake=0;flashScreen=0;drawWorld(0);}", i)
        f=O/f'{st}_{i}.png'; p.screenshot(path=str(f)); tiles.append(Image.open(f).crop((420,120,860,560)))
      sh=Image.new('RGB',(440*3,440*2)); [sh.paste(t,((i%3)*440,(i//3)*440)) for i,t in enumerate(tiles)]; sh.save(O/f'{st}_frames.png')
    print('errors', errs, p.evaluate("CG.events.filter(e=>e.type.includes('error'))"))
    br.close()
finally: stop()
