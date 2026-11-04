"""Frame-exact capture of the Stage 5 Fury-ship forming sequence (QA / review).
    python _BUILD_SOURCE/capture_ship_forming_1104.py TAG [pilot] [init-js]
Drives the real loop() at a fixed 60 fps under TRAP_RAF from setState(GS.LAUNCH) until the ship is active,
saving every 2nd frame from the kit's first part until 1 s after 'active' to _shots/ship_forming_1104/TAG/,
with the gravityMode phase/t of each saved frame in frames.json. Also writes an MP4 (ffmpeg via imageio).
"""
from pathlib import Path
import json, sys, base64, http.server
from playwright.sync_api import sync_playwright
R = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(R / '_BUILD_SOURCE')); import shoot
http.server.SimpleHTTPRequestHandler.log_message = lambda *a: None
tag = sys.argv[1]; pilot = sys.argv[2] if len(sys.argv) > 2 else 'axel'; init = sys.argv[3] if len(sys.argv) > 3 else ''
O = R / '_shots/ship_forming_1104' / tag; O.mkdir(parents=True, exist_ok=True)
for f in O.glob('f_*.png'): f.unlink()
FRAME = r"""t=>{const cb=window.__bofPendingRAF;window.__bofPendingRAF=null;if(cb)cb(t);
 const G=typeof gravityMode!=='undefined'?gravityMode:null;
 return {state:state,phase:G?G.phase:null,t:G?+G.t.toFixed(3):0,age:G?+(G.age||0).toFixed(3):0,parts:G?(G.partStartAge!=null):false,
  intro:drawLaunch._furyIntro?drawLaunch._furyIntro.phase:null};}"""
port, stop = shoot.serve(str(R))
try:
    with sync_playwright() as pw:
        br = pw.chromium.launch(args=['--no-sandbox', '--mute-audio']); p = br.new_page(viewport={'width': 1100, 'height': 1100}); p.set_default_timeout(300000)
        errs = []; p.on('pageerror', lambda e: errs.append(str(e)[:200]))
        p.add_init_script("Object.defineProperty(navigator,'getGamepads',{value:()=>[]});" + init)
        p.goto(f'http://127.0.0.1:{port}/index.html'); p.wait_for_function('()=>window.__bofFrames>4')
        p.evaluate('()=>{furyShipWarm();XART._touch("ngm_space_atlas");for(let i=0;i<7;i++)XART._touch("cm2_cloud_"+i);}')
        p.wait_for_function('()=>furyShipReady()&&XART.rdy("ngm_space_atlas")', timeout=120000)
        p.evaluate(shoot.TRAP_RAF)
        p.evaluate('k=>{const i=PILOTS.findIndex(q=>q.key===k);if(i>=0)pilotIndex=i;run.mode="campaign";beginStage(5);run.pilot=k;player.reset();player.invuln=999999;snapCamToPlayer();setState(GS.LAUNCH);gravityModeReset();drawLaunch._phase=undefined;drawLaunch._furyIntro=null;}', pilot)
        t = 1000.0; frames = []; rec = False; after = None; n = 0
        for i in range(60 * 60):
            t += 1000 / 60; s = p.evaluate(FRAME, t)
            if i % 20 == 0: p.wait_for_timeout(15)   # let lazy images decode on real time
            if s['parts'] and not rec: rec = True
            if s['phase'] == 'active' and after is None: after = i
            if rec and i % 2 == 0:
                png = base64.b64decode(p.evaluate("()=>document.getElementById('screen').toDataURL('image/png').split(',')[1]"))
                (O / f'f_{n:04d}.png').write_bytes(png); s['i'] = i; s['n'] = n; frames.append(s); n += 1
            if after is not None and i - after > 60: break
        (O / 'frames.json').write_text(json.dumps(frames))
        print('saved', n, 'frames; phases', sorted({f['phase'] for f in frames if f['phase']}), 'errors', errs[:3])
        br.close()
finally:
    stop()
try:
    import imageio.v2 as iio
    w = iio.get_writer(str(O / f'{tag}.mp4'), fps=30, codec='libx264', quality=8, macro_block_size=1)
    for f in sorted(O.glob('f_*.png')): w.append_data(iio.imread(f))
    w.close(); print('mp4', O / f'{tag}.mp4')
except Exception as e:
    print('mp4 skipped', e)
