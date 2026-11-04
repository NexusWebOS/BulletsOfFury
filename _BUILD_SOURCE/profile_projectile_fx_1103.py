"""Cost of each PFX13 feature on a real fight, plus the stack of any shadowBlur that still lands.
    python _BUILD_SOURCE/profile_projectile_fx_1103.py"""
from pathlib import Path
import json, sys, http.server
from playwright.sync_api import sync_playwright
R = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(R / '_BUILD_SOURCE')); import shoot
http.server.SimpleHTTPRequestHandler.log_message = lambda *a: None
JS = """([c,mode])=>{
  c.seed=1103;c.pilot='yuri';c.level=4;AP7.begin(c);for(const k of keybindFor(1).fire||[])if(!k.startsWith('pad_'))Input.keys[k]=true;
  for(let f=0;f<240;f++){player.invuln=99999;run.shield=999;updatePlay(1/60);}
  const saved=JSON.parse(JSON.stringify(PFX13.cfg));let leaks=[];
  const own=Object.getOwnPropertyDescriptor(ctx,'shadowBlur');let inB=false;
  Object.defineProperty(ctx,'shadowBlur',{configurable:true,get(){return own.get.call(this);},set(v){own.set.call(this,v);if(inB&&own.get.call(this)>0&&leaks.length<3)leaks.push(JSON.stringify(PFX13._dbg())+' '+new Error().stack.split('\\n').slice(2,10).join(' | '));}});
  const out={};
  for(const m of mode){
    window.PFX13_OFF=m==='off'?1:0;Object.assign(PFX13.cfg,saved);if(m.startsWith('-'))PFX13.cfg[m.slice(1)]=false;
    if(m==='bare')for(const k in PFX13.cfg)PFX13.cfg[k]=false;
    let t=0;for(let i=0;i<120;i++){ctx.setTransform(SS,0,0,SS,0,0);const a=performance.now();inB=true;drawBullets();inB=false;t+=performance.now()-a;}
    out[m]=+(t/120).toFixed(3);
  }
  Object.assign(PFX13.cfg,saved);window.PFX13_OFF=0;Object.defineProperty(ctx,'shadowBlur',own);
  return {ms:out,rounds:eBullets.length+pBullets.length,leaks};
}"""
port, stop = shoot.serve(str(R))
try:
    with sync_playwright() as pw:
        br = pw.chromium.launch(args=['--no-sandbox', '--mute-audio']); cx = br.new_context(viewport={'width': 1100, 'height': 950})
        cx.route('**/*', lambda r: r.continue_() if r.request.url.startswith(('http://127.0.0.1:', 'data:', 'blob:')) else r.abort())
        p = cx.new_page(); p.set_default_timeout(180000)
        p.goto(f'http://127.0.0.1:{port}/index.html'); p.wait_for_function('()=>window.__bofFrames>4'); p.evaluate(shoot.TRAP_RAF)
        for f in ['balance_lab_1007.js', 'projectile_lab_1007.js']: p.add_script_tag(path=str(R / '_BUILD_SOURCE' / f))
        modes = ['off', 'bare', 'on', '-rim', '-trails', '-inner', '-glow', '-pop', '-graze', 'on']
        for c in [dict(stage=1, kind='damkeeper', diff='furious', slice=True), dict(stage=5, kind='xenoregent', diff='furious', slice=True)]:
            p.evaluate(JS, [c, ['on']]); p.wait_for_timeout(1500)
            print(json.dumps(p.evaluate(JS, [c, modes])), flush=True)
        br.close()
finally:
    stop()
