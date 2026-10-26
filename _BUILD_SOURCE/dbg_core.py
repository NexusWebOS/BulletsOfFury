from playwright.sync_api import sync_playwright
from shoot import serve, TRAP_RAF
from pathlib import Path
import probe_chronos_glow_1025 as P
R=Path(__file__).resolve().parents[1]; port,stop=serve(str(R))
try:
  with sync_playwright() as pw:
    br=pw.chromium.launch(channel='msedge'); p=br.new_page(viewport={'width':1280,'height':800})
    p.goto(f'http://127.0.0.1:{port}/index.html')
    p.wait_for_function("window.__bofFrames>5&&typeof CG!=='undefined'&&typeof c32Warm==='function'",timeout=180000)
    p.mouse.click(3,3);p.evaluate(TRAP_RAF);p.evaluate(P.SETUP);p.wait_for_function(P.READY,timeout=180000);p.evaluate(P.STATES['chrome'])
    print(p.evaluate("""()=>{boss.x=340;boss.y=260;const o=[];const g=cgCoreGlow;cgCoreGlow=function(b,M,B){o.push({k:B.im.__k||('cv'+B.im.width),dx:B.dx,dy:B.dy,ky:B.ky,mode:M.mode});return g.apply(this,arguments);};
      const L=[];const di=ctx.drawImage;ctx.drawImage=function(im){if(im&&im.width>=150){L.push((im.__k||'cv'+im.width+'x'+im.height)+' a'+ctx.globalAlpha.toFixed(2)+' '+ctx.globalCompositeOperation);}return di.apply(this,arguments);};
      for(let i=0;i<3;i++){efxClock+=1/9;drawWorld(0);} ctx.drawImage=di;cgCoreGlow=g;return {o:o.slice(0,3),L:L.slice(0,40),body:CG.body&&{k:CG.body.im.__k}};}"""))
    br.close()
finally: stop()
