"""Does the core pixel glow land in every state the live fight draws? Runs the real fight."""
import json
from pathlib import Path
from playwright.sync_api import sync_playwright
from shoot import serve, TRAP_RAF
from probe_chronos_glow_1025 import SETUP, READY
R=Path(__file__).resolve().parents[1]; port,stop=serve(str(R)); errs=[]
try:
  with sync_playwright() as pw:
    br=pw.chromium.launch(channel='msedge'); p=br.new_page(viewport={'width':1280,'height':800})
    p.on('pageerror',lambda e:errs.append(str(e)))
    p.goto(f'http://127.0.0.1:{port}/index.html')
    p.wait_for_function("window.__bofFrames>5&&typeof CG!=='undefined'&&typeof c32Warm==='function'",timeout=180000)
    p.mouse.click(3,3);p.evaluate(TRAP_RAF);p.evaluate(SETUP);p.wait_for_function(READY,timeout=180000)
    p.evaluate("""()=>{window.__cs={};const g=cgCoreGlow;cgCoreGlow=function(b,M,B){window.__cg={k:B.im.__k||('cv'+B.im.width+'x'+B.im.height),mode:M.mode};return g.apply(this,arguments);};
      const d=hammerBossDraw;hammerBossDraw=function(b){window.__cg=null;window.__pl=[];const di=ctx.drawImage;ctx.drawImage=function(im){if(im&&im.width>=120)__pl.push((im.__k||'cv'+im.width+'x'+im.height)+'@'+ctx.globalAlpha.toFixed(2)+ctx.globalCompositeOperation[0]);return di.apply(this,arguments);};
        try{return d.apply(this,arguments);}finally{ctx.drawImage=di;const s=(b._hammer&&b._hammer.state)||'?';const e=__cs[s]||(__cs[s]={n:0,glow:0,keys:{},miss:[]});e.n++;if(__cg){e.glow++;e.keys[__cg.k]=1;}else if(e.miss.length<2)e.miss.push(__pl.slice(0,8));}};
      playerHit=function(){};}""")
    O=R/'_shots/chronos_glow_1025/core_states'; O.mkdir(parents=True,exist_ok=True); shot=set()
    WANT={'hammer','giant_idle','throw','whirlwind','giant_dive','c27_depth_combo','spin','giant_bg_drop','hammer_catch','return','nova_release','ball'}
    for chunk in range(140*4):   # ~140 s of the live fight, 15-frame chunks so states can be photographed
      st=p.evaluate("()=>{for(let i=0;i<15;i++){player.x=340+Math.sin(efxClock)*120;player.y=430;if(boss&&boss.hp<boss.maxhp*.2&&!boss._hammer._hf22Red)boss.hp=boss.maxhp*.6;updatePlay(1/60);drawWorld(1/60);}return boss&&boss._hammer&&boss._hammer.state;}")
      if st in WANT and st not in shot and chunk%3==0:
        shot.add(st); p.screenshot(path=str(O/f'{st}.png'))
      if chunk%4==0: p.wait_for_timeout(20)
    print('tool glows', p.evaluate("CG.toolGlows||0"), 'shots', sorted(shot))
    r=p.evaluate("__cs")
    for s,e in sorted(r.items(),key=lambda x:-x[1]['n']):
      print(f"{s:28s} frames {e['n']:5d} glow {e['glow']:5d}", list(e['keys'])[:3], '' if e['glow']==e['n'] else e['miss'][:1])
    print('errors',errs[:3])
    br.close()
finally: stop()
