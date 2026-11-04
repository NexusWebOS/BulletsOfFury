"""Wave pressure telemetry across stages and difficulties (QA only).

    python _BUILD_SOURCE/measure_waves_1103.py [--stages 1,2,6r] [--diffs normal,hard,furious] [--bots novice] [--tag x]

Each run: one fresh page, the stage's authored regular-wave book (wave_review_1101 fixture: encounters
suppressed, adaptive extras held), the chosen difficulty, a dodge bot (wave_telemetry_1103), level-3
weapons, invulnerable with every playerHit call counted. Writes _shots/waves_1103/<tag>/<stage>-<diff>-<bot>.json
"""
from pathlib import Path
import json, sys, time, argparse, http.server
from playwright.sync_api import sync_playwright
R = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(R / '_BUILD_SOURCE')); import shoot
A = argparse.ArgumentParser()
A.add_argument('--stages', default='1,2,3,4,5,6,6r,7,8,9'); A.add_argument('--diffs', default='normal,hard,furious')
A.add_argument('--bots', default='novice'); A.add_argument('--tag', default='run'); A.add_argument('--cap', type=float, default=480); A.add_argument('--see', action='store_true'); A.add_argument('--off', default='', help='window flag set before boot, e.g. DA13_OFF')
args = A.parse_args()
O = R / '_shots/waves_1103' / args.tag; O.mkdir(parents=True, exist_ok=True)
http.server.SimpleHTTPRequestHandler.log_message = lambda *a: None
port, stop = shoot.serve(str(R))
try:
    with sync_playwright() as pw:
        br = pw.chromium.launch(args=['--no-sandbox', '--mute-audio'])
        for st in args.stages.split(','):
            stage, route = int(st.rstrip('r')), ('right' if st.endswith('r') else 'left')
            for diff in args.diffs.split(','):
                if diff in ('normal', 'easy') and stage >= 6: continue   # Easy/Normal campaigns end at Stage 5 (normal_finale_1031)
                for bot in args.bots.split(','):
                    out = O / f'{st}-{diff}-{bot}.json'
                    if out.exists(): continue
                    p = br.new_page(viewport={'width': 1100, 'height': 900}); p.set_default_timeout(300000); errs = []
                    p.on('pageerror', lambda e: errs.append(str(e)[:200]))
                    p.add_init_script("Object.defineProperty(navigator,'getGamepads',{value:()=>[]});" + ("window.WT_SEE_HAZARDS=1;" if args.see else "") + (f"window.{args.off}=1;" if args.off else ""))
                    p.goto(f'http://127.0.0.1:{port}/index.html'); p.wait_for_function('()=>window.__bofFrames>4'); p.evaluate(shoot.TRAP_RAF)
                    for f in ['enemy_behaviour_lab_1011.js', 'wave_followup_1103/reference_wave_maps.js', 'wave_followup_1103/wave_observe_1102.js', 'wave_telemetry_1103.js']:
                        p.add_script_tag(path=str(R / '_BUILD_SOURCE' / f))
                    t0 = time.time()
                    try:
                        p.evaluate('a=>WT.start(a[0],a[1],a[2],a[3],3)', [stage, diff, route, bot])
                        # the stage loader decodes a few images at a time on real time; waves wait for it
                        for _ in range(1200):
                            if p.evaluate('n=>{stageLoadTick();return stageLoadReady(n);}', stage): break
                            p.wait_for_timeout(50)
                        load = p.evaluate('n=>stageLoadInfo(n)', stage)
                        while True:
                            s = p.evaluate('()=>WT.steps(600)')
                            if int(s['clock']) % 60 < 10: print('  ..', st, diff, bot, 'clock', int(s['clock']), 'events', s['events'], flush=True)
                            # the image queue advances inside loop(), held by TRAP_RAF: give it real frames
                            for _ in range(3):
                                p.evaluate('()=>{const cb=window.__bofPendingRAF;window.__bofPendingRAF=null;if(cb)cb(performance.now());}'); p.wait_for_timeout(10)
                            if s['done'] or s['state'] != 'play' or s['clock'] > args.cap: break
                        res = p.evaluate('()=>WT.result()'); res.update(route=route, end=s, errors=errs[:5], wall=round(time.time() - t0), load=load)
                        out.write_text(json.dumps(res))
                        print('DONE', st, diff, bot, 'sec', res['seconds'], 'hits', res['hits'], 'shots/s', res['shotsPerSec'], 'events', s['events'], '/', s['expected'], 'wall', res['wall'], flush=True)
                    except Exception as e:
                        print('ERR', st, diff, bot, str(e)[:300], flush=True)
                    p.close()
        br.close()
finally:
    stop()
