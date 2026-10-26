from pathlib import Path
from playwright.sync_api import sync_playwright
from shoot import serve, TRAP_RAF
from probe_chronos_glow_1025 import SETUP, READY
R = Path(__file__).resolve().parents[1]; O = R/'_shots/chronos_glow_1025/diag_throw'; O.mkdir(parents=True, exist_ok=True)
port, stop = serve(str(R))
try:
  with sync_playwright() as pw:
    br = pw.chromium.launch(channel='msedge'); p = br.new_page(viewport={'width':1280,'height':800})
    p.goto(f'http://127.0.0.1:{port}/index.html')
    p.wait_for_function("window.__bofFrames>5&&typeof CG!=='undefined'&&typeof c32Warm==='function'", timeout=180000)
    p.mouse.click(3,3); p.evaluate(TRAP_RAF); p.evaluate(SETUP); p.wait_for_function(READY, timeout=180000)
    p.evaluate("()=>{const h=boss._hammer;h.hb20Pickup=null;if(h.frArmor){h.frArmor.activated=false;h.frArmor.hp=0;}h.state='hammer';h._hf22Red=false;h.c27RagePending=true;boss.hp=boss.maxhp*.1;hf22BeginBlueRage(boss);}")
    p.evaluate("()=>{window.__di=ctx.drawImage;}")
    for t in (0.02, 0.09, 0.17, 0.2, 0.3):
      for arm in ('on',):
        info = p.evaluate("""([t,arm])=>{const h=boss._hammer;h._hf22Charge.t=t;boss.x=340;boss.y=260;boss.flash=0;particles.length=0;h._cgPrev={mode:'ragecharge'};
          const f=hammerBossDraw;if(arm==='off')hammerBossDraw=CG.base;
          const log=[];const di=ctx.drawImage;ctx.drawImage=function(im){const a=arguments;if(im&&im.width>=150){const m=ctx.getTransform();log.push([im.__k||('cv'+im.width+'x'+im.height),a.length>=9?[a[5],a[6],a[7],a[8]].map(v=>Math.round(v)):[a[1],a[2],a[3],a[4]].map(v=>Math.round(v)),+m.a.toFixed(2),+m.e.toFixed(0),+m.f.toFixed(0),+ctx.globalAlpha.toFixed(2),ctx.globalCompositeOperation]);}return di.apply(this,arguments);};
          try{drawWorld(0);}finally{ctx.drawImage=di;hammerBossDraw=f;}
          const q=ha21Blue(boss);return {kind:q&&q.kind,k:q&&q.k,log:log.slice(0,14),by:boss.y,bx:boss.x};}""", [t,arm])
        print(t, arm, info['kind'], info['k'], 'by', info['by'])
        for l in info['log']: print('   ', l)
        p.screenshot(path=str(O/f't{t}_{arm}.png'))
    br.close()
finally: stop()
