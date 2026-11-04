"""Enemy fire per type and difficulty (QA only).

    python _BUILD_SOURCE/probe_fire_by_type_1103.py STAGE DIFF[,DIFF...] [SECONDS]

Credits each new enemy round to the nearest live enemy at birth (within 90 px) and reports, per
enemy type: on-screen seconds, rounds fired, rounds per on-screen second. Writes
_shots/waves_1103/fire_s<stage>_<diff>.json
"""
from pathlib import Path
import json, sys, http.server
from playwright.sync_api import sync_playwright
R = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(R / '_BUILD_SOURCE')); import shoot
http.server.SimpleHTTPRequestHandler.log_message = lambda *a: None
stage = int(sys.argv[1]); diffs = sys.argv[2].split(','); secs = int(sys.argv[3]) if len(sys.argv) > 3 else 500
JS = r"""n=>{const F=window.FT||(window.FT={seen:new WeakSet(),types:{}});
 for(let i=0;i<n;i++){if(state!==GS.PLAY||WT.F.done)break;
  stageLoadTick();WT.F.input(1/60);WT.botInput();stateT+=1/60;updatePlay(1/60);WT.frame++;
  if(WT.frame%3===0){ctx.setTransform(SS,0,0,SS,0,0);drawWorld(3/60);}
  const live=enemies.filter(e=>!e.dead&&e._dyingT==null&&!e._prop);
  for(const e of live){if(e.x>camLeftX()-10&&e.x<camRightX()+10&&e.y>viewTopY()&&e.y<VH){const T=F.types[e.type]||(F.types[e.type]={sec:0,rounds:0,units:new Set()});T.sec+=1/60;}}
  for(const b of eBullets){if(!b||F.seen.has(b))continue;F.seen.add(b);let best=null,bd=90;for(const e of live){const d=Math.hypot(e.x-b.x,e.y-b.y);if(d<bd){bd=d;best=e;}}
   const k=best?best.type:'(unattributed)';const T=F.types[k]||(F.types[k]={sec:0,rounds:0});T.rounds++;}
 }
 return {clock:WT.F.clock,done:WT.F.done};}"""
port, stop = shoot.serve(str(R))
try:
    with sync_playwright() as pw:
        br = pw.chromium.launch(args=['--no-sandbox', '--mute-audio'])
        for diff in diffs:
            p = br.new_page(viewport={'width': 1100, 'height': 900}); p.set_default_timeout(300000)
            p.goto(f'http://127.0.0.1:{port}/index.html'); p.wait_for_function('()=>window.__bofFrames>4'); p.evaluate(shoot.TRAP_RAF)
            for f in ['enemy_behaviour_lab_1011.js', 'wave_followup_1103/reference_wave_maps.js', 'wave_followup_1103/wave_observe_1102.js', 'wave_telemetry_1103.js']:
                p.add_script_tag(path=str(R / '_BUILD_SOURCE' / f))
            p.evaluate('a=>WT.start(a[0],a[1],"left","novice",3)', [stage, diff])
            for _ in range(1200):
                if p.evaluate('n=>{stageLoadTick();return stageLoadReady(n);}', stage): break
                p.wait_for_timeout(50)
            for _ in range(secs // 10):
                s = p.evaluate(JS, 600)
                if s['done']: break
            types = p.evaluate('()=>Object.fromEntries(Object.entries(FT.types).map(([k,v])=>[k,{sec:+v.sec.toFixed(1),rounds:v.rounds,rate:v.sec>1?+(v.rounds/v.sec).toFixed(2):null}]))')
            (R / f'_shots/waves_1103/fire_s{stage}_{diff}.json').write_text(json.dumps(types))
            print('DONE', stage, diff, 'clock', round(s['clock']), flush=True)
            p.close()
        br.close()
finally:
    stop()
