"""Film Stage 6 new-fighter rounds (_s611Ammo) in game: full frames + 4x crops around rounds.
    python _BUILD_SOURCE/shots_s6_rounds_1104.py TAG [diff] [off-flag]
"""
from pathlib import Path
import json, sys, base64, io, http.server
from playwright.sync_api import sync_playwright
from PIL import Image
R = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(R / '_BUILD_SOURCE')); import shoot
http.server.SimpleHTTPRequestHandler.log_message = lambda *a: None
tag = sys.argv[1]; diff = sys.argv[2] if len(sys.argv) > 2 else 'hard'; off = sys.argv[3] if len(sys.argv) > 3 else ''
O = R / '_shots/s6_rounds_1104' / tag; O.mkdir(parents=True, exist_ok=True)
STEP = r"""n=>{for(let i=0;i<n;i++){if(state!==GS.PLAY||WT.F.done)break;stageLoadTick();WT.F.input(1/60);WT.botInput();stateT+=1/60;updatePlay(1/60);WT.frame++;
 if(WT.frame%3===0){ctx.setTransform(SS,0,0,SS,0,0);drawWorld(3/60);}}
 const r=eBullets.filter(b=>b&&!b.dead&&b._s611Ammo&&b.x>camLeftX()+20&&b.x<camRightX()-20&&b.y>20&&b.y<VH-20);
 return {s6r:window.S6R14?{...S6R14.stat}:null,n:r.length,clock:WT.F.clock,pts:r.slice(0,6).map(b=>[b.x-camLeftX(),b.y,b.kind])};}"""
port, stop = shoot.serve(str(R))
try:
    with sync_playwright() as pw:
        br = pw.chromium.launch(args=['--no-sandbox', '--mute-audio']); p = br.new_page(viewport={'width': 1100, 'height': 900}); p.set_default_timeout(300000)
        errs = []; p.on('pageerror', lambda e: errs.append(str(e)[:200]))
        p.add_init_script("Object.defineProperty(navigator,'getGamepads',{value:()=>[]});" + (f"window.{off}=1;" if off else ""))
        p.goto(f'http://127.0.0.1:{port}/index.html'); p.wait_for_function('()=>window.__bofFrames>4'); p.evaluate(shoot.TRAP_RAF)
        for f in ['enemy_behaviour_lab_1011.js', 'wave_followup_1103/reference_wave_maps.js', 'wave_followup_1103/wave_observe_1102.js', 'wave_telemetry_1103.js']:
            p.add_script_tag(path=str(R / '_BUILD_SOURCE' / f))
        p.evaluate('d=>WT.start(6,d,"left","still",3)', diff)
        for _ in range(1200):
            if p.evaluate('()=>{stageLoadTick();return stageLoadReady(6);}'): break
            p.wait_for_timeout(50)
        got = 0; meta = []
        for i in range(900):
            r = p.evaluate(STEP, 3)
            if i % 20 == 0:
                p.evaluate('()=>{const cb=window.__bofPendingRAF;window.__bofPendingRAF=null;if(cb)cb(performance.now());}')
            if r['n'] >= 2 and (i % 4 == 0):
                p.evaluate('()=>{ctx.setTransform(SS,0,0,SS,0,0);drawWorld(1/60);}')
                png = base64.b64decode(p.evaluate("()=>cv.toDataURL('image/png').split(',')[1]"))
                im = Image.open(io.BytesIO(png)).convert('RGB'); sx = im.width / 480 if im.width < 1400 else None
                # canvas maps the 480-wide playfield with HUD offsets; find scale from canvas vs VW
                info = p.evaluate('()=>({w:cv.width,h:cv.height,ox:(typeof playX==="number"?playX:0)})')
                im.save(O / f'frame_{got:02d}.png'); meta.append({'i': got, 'clock': r['clock'], 'pts': r['pts'], 'canvas': info})
                got += 1
                if got >= 8: break
        (O / 'meta.json').write_text(json.dumps(meta, indent=1)); print('frames', got, 'S6R14', r.get('s6r'), 'errors', errs[:3]); br.close()
finally:
    stop()
