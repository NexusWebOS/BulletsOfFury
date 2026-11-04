"""Which large effects cover the playfield during regular waves? (QA only)

    python _BUILD_SOURCE/probe_big_flash_1103.py STAGE [SECONDS]

Tags every XART image with its key and, while drawEffects and drawWorld run, records image draws
larger than 110x110 game px and arc/fill discs over 55 px radius: key or source, size, and the
calling function. Prints the biggest offenders by frames x area.
"""
from pathlib import Path
import json, sys, http.server
from playwright.sync_api import sync_playwright
R = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(R / '_BUILD_SOURCE')); import shoot
http.server.SimpleHTTPRequestHandler.log_message = lambda *a: None
stage = int(sys.argv[1]); secs = int(sys.argv[2]) if len(sys.argv) > 2 else 240
SETUP = r"""()=>{
 const tags=new WeakMap(),g=XART.get,raw=XART.raw;XART.get=function(k){const im=g.apply(this,arguments);if(im&&typeof im==='object')tags.set(im,k);return im;};
 XART.raw=function(k){const im=raw.apply(this,arguments);if(im&&typeof im==='object')tags.set(im,k);return im;};
 window.BF={rows:{},on:false};const d=ctx.drawImage,arc=ctx.arc;
 const who=()=>{const s=String(new Error().stack).split(String.fromCharCode(10)).map(l=>l.trim()).filter(l=>l.startsWith('at ')&&!/BF|probe|eval/.test(l));return (s[1]||'').replace(/^at /,'').replace(/ \(.*/,'').slice(0,40);};
 ctx.drawImage=function(im,...a){if(BF.on){const dw=a.length>=8?a[6]:a[2],dh=a.length>=8?a[7]:a[3];if(Math.abs(dw)>110&&Math.abs(dh)>110&&this.globalAlpha>.25){const k=(tags.get(im)||String(im.src||'canvas').split('/').pop()).replace(/_\d+$/,'')+' <- '+who();const r=BF.rows[k]||(BF.rows[k]={n:0,area:0,maxW:0});r.n++;r.area+=Math.abs(dw*dh);r.maxW=Math.max(r.maxW,Math.round(Math.abs(dw)));}}return d.call(this,im,...a);};
 ctx.arc=function(x,y,r,...rest){if(BF.on&&r>55&&this.globalAlpha>.25){const k='arc r>55 '+String(this.fillStyle).slice(0,9)+' <- '+who();const q=BF.rows[k]||(BF.rows[k]={n:0,area:0,maxW:0});q.n++;q.area+=Math.PI*r*r;q.maxW=Math.max(q.maxW,Math.round(r*2));}return arc.call(this,x,y,r,...rest);};
 const fx=drawEffects;drawEffects=function(){BF.on=true;try{return fx.apply(this,arguments);}finally{BF.on=false;}};
}"""
STEP = r"""n=>{for(let i=0;i<n;i++){if(state!==GS.PLAY||WT.F.done)break;stageLoadTick();WT.F.input(1/60);WT.botInput();stateT+=1/60;updatePlay(1/60);WT.frame++;
 if(WT.frame%3===0){ctx.setTransform(SS,0,0,SS,0,0);drawWorld(3/60);}}return WT.F.clock;}"""
port, stop = shoot.serve(str(R))
try:
    with sync_playwright() as pw:
        br = pw.chromium.launch(args=['--no-sandbox', '--mute-audio']); p = br.new_page(viewport={'width': 1100, 'height': 900}); p.set_default_timeout(300000)
        p.goto(f'http://127.0.0.1:{port}/index.html'); p.wait_for_function('()=>window.__bofFrames>4'); p.evaluate(shoot.TRAP_RAF)
        for f in ['enemy_behaviour_lab_1011.js', 'wave_followup_1103/reference_wave_maps.js', 'wave_followup_1103/wave_observe_1102.js', 'wave_telemetry_1103.js']:
            p.add_script_tag(path=str(R / '_BUILD_SOURCE' / f))
        p.evaluate(SETUP)
        p.evaluate('a=>WT.start(a[0],a[1],"left","novice",5)', [stage, 'furious'])
        for _ in range(1200):
            if p.evaluate('n=>{stageLoadTick();return stageLoadReady(n);}', stage): break
            p.wait_for_timeout(50)
        for _ in range(secs // 10): p.evaluate(STEP, 600)
        rows = p.evaluate('()=>BF.rows')
        br.close()
finally:
    stop()
for k, v in sorted(rows.items(), key=lambda kv: -kv[1]['area'])[:15]:
    print(f"{v['n']:6} draws  max {v['maxW']:4}px  area {v['area']/1e6:8.1f}M  {k}")
