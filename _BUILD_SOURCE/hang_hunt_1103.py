"""Catch the JavaScript stack of a hung wave run (QA only).

    python _BUILD_SOURCE/hang_hunt_1103.py STAGE DIFF [tries]

Runs the wave telemetry in 60-frame chunks with Chrome's remote-debugging port open. A watchdog
subprocess attaches over CDP when a chunk has not returned for 45 s, pauses the debugger, and
writes the call stack to _shots/waves_1103/hang_<stage>_<diff>.json.
"""
from pathlib import Path
import json, sys, time, subprocess, http.server, threading
R = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(R / '_BUILD_SOURCE')); import shoot
OUT = R / '_shots/waves_1103'
WATCH = r'''
import sys,json,time
from playwright.sync_api import sync_playwright
port,out=int(sys.argv[1]),sys.argv[2]
with sync_playwright() as pw:
  br=pw.chromium.connect_over_cdp(f"http://127.0.0.1:{port}")
  pages=[p for c in br.contexts for p in c.pages]
  pg=[p for p in pages if 'index.html' in p.url][0]
  s=pg.context.new_cdp_session(pg);frames=[]
  s.on('Debugger.paused',lambda e:frames.extend(e['callFrames']))
  s.send('Debugger.enable');s.send('Debugger.pause')
  for _ in range(100):
    if frames:break
    time.sleep(.1)
  rows=[{'fn':f['functionName'],'url':f['url'].split('/')[-1],'line':f['location']['lineNumber']+1,'col':f['location'].get('columnNumber',0)} for f in frames]
  # local scope summary of the top frame
  open(out,'w').write(json.dumps({'stack':rows},indent=1))
  s.send('Debugger.resume')
'''
stage, diff = int(sys.argv[1]), sys.argv[2]; tries = int(sys.argv[3]) if len(sys.argv) > 3 else 3
http.server.SimpleHTTPRequestHandler.log_message = lambda *a: None
port, stop = shoot.serve(str(R)); dbg = 9300 + stage
from playwright.sync_api import sync_playwright
try:
    with sync_playwright() as pw:
        for k in range(tries):
            br = pw.chromium.launch(args=['--no-sandbox', '--mute-audio', f'--remote-debugging-port={dbg}'])
            p = br.new_page(viewport={'width': 1100, 'height': 900}); p.set_default_timeout(300000)
            p.goto(f'http://127.0.0.1:{port}/index.html'); p.wait_for_function('()=>window.__bofFrames>4'); p.evaluate(shoot.TRAP_RAF)
            for f in ['enemy_behaviour_lab_1011.js', 'wave_followup_1103/reference_wave_maps.js', 'wave_followup_1103/wave_observe_1102.js', 'wave_telemetry_1103.js']:
                p.add_script_tag(path=str(R / '_BUILD_SOURCE' / f))
            p.evaluate('a=>WT.start(a[0],a[1],"left","novice",3)', [stage, diff])
            for _ in range(1200):
                if p.evaluate('n=>{stageLoadTick();return stageLoadReady(n);}', stage): break
                p.wait_for_timeout(50)
            last = [time.time()]; hung = [False]; out = OUT / f'hang_{stage}_{diff}.json'
            def watchdog():
                while not hung[0]:
                    time.sleep(5)
                    if time.time() - last[0] > 45:
                        hung[0] = True
                        subprocess.run([sys.executable, '-c', WATCH, str(dbg), str(out)], timeout=120)
                        print('HUNG: stack written', out, flush=True)
            threading.Thread(target=watchdog, daemon=True).start()
            clock = 0
            while clock < 1000 and not hung[0]:
                s = p.evaluate('()=>WT.steps(60)'); last[0] = time.time(); clock = s['clock']
                if s['done'] or s['state'] != 'play': break
            print('try', k, 'ended clock', round(clock), 'hung', hung[0], flush=True)
            if hung[0]:
                time.sleep(130); break
            hung[0] = True; br.close()
finally:
    stop()
