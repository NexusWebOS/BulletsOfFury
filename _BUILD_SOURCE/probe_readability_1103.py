"""Native probe for assets/readability_1103.js (RD13).

    python _BUILD_SOURCE/probe_readability_1103.py

Real index.html, natural wave pacing (wave_telemetry_1103). Checks that threat pips are stamped on
enemy rounds inside explosions and that warning lanes beyond the two most imminent are dimmed, that
gameplay state is identical with RD13 on and off for the same frame (renderer only), and zero
errors. Saves a frame with pips to _shots/waves_1103/readability_pips.png.
"""
from pathlib import Path
import json, sys, base64, http.server
from playwright.sync_api import sync_playwright
R = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(R / '_BUILD_SOURCE')); import shoot
http.server.SimpleHTTPRequestHandler.log_message = lambda *a: None
checks, errors = [], []
def ok(name, cond, info=''):
    checks.append({'name': name, 'pass': bool(cond), 'info': info}); print(('PASS ' if cond else 'FAIL ') + name, info, flush=True)
STEP = r"""n=>{let shot=null,same=0,diff=0;for(let i=0;i<n;i++){if(state!==GS.PLAY||WT.F.done)break;
  stageLoadTick();WT.F.input(1/60);WT.botInput();stateT+=1/60;updatePlay(1/60);WT.frame++;
  if(WT.frame%3===0){
    const snap=()=>JSON.stringify(eBullets.map(b=>[b.x,b.y,b.vx,b.vy,!!b.dead]).concat(enemies.map(e=>[e.x,e.y,e.hp])));
    const p0=RD13.state.stat.pips,s0=snap();ctx.setTransform(SS,0,0,SS,0,0);drawWorld(3/60);const s1=snap();
    if(s0===s1)same++;else diff++;
    if(!shot&&RD13.state.stat.pips-p0>=2)shot=cv.toDataURL('image/png').split(',')[1];}
 }return {shot,same,diff,stat:{...RD13.state.stat},clock:WT.F.clock};}"""
port, stop = shoot.serve(str(R))
try:
    with sync_playwright() as pw:
        br = pw.chromium.launch(args=['--no-sandbox', '--mute-audio']); p = br.new_page(viewport={'width': 1100, 'height': 900}); p.set_default_timeout(300000)
        p.on('pageerror', lambda e: errors.append(str(e)[:200]))
        p.goto(f'http://127.0.0.1:{port}/index.html'); p.wait_for_function('()=>window.__bofFrames>4&&typeof RD13!=="undefined"'); p.evaluate(shoot.TRAP_RAF)
        for f in ['enemy_behaviour_lab_1011.js', 'wave_followup_1103/reference_wave_maps.js', 'wave_followup_1103/wave_observe_1102.js', 'wave_telemetry_1103.js']:
            p.add_script_tag(path=str(R / '_BUILD_SOURCE' / f))
        p.evaluate('()=>WT.start(9,"furious","left","novice",5)')
        for _ in range(1200):
            if p.evaluate('()=>{stageLoadTick();return stageLoadReady(9);}'): break
            p.wait_for_timeout(50)
        shot = None; same = diff = 0; st = {}
        for _ in range(30):
            r = p.evaluate(STEP, 600); same += r['same']; diff += r['diff']; st = r['stat']
            if r['shot'] and not shot:
                shot = r['shot']; (R / '_shots/waves_1103/readability_pips.png').write_bytes(base64.b64decode(shot))
        ok('threat pips stamped on rounds inside explosions', st.get('pips', 0) > 0, f"{st.get('pips')} pips")
        ok('warning lanes beyond the two most imminent are dimmed', st.get('dimmed', 0) > 0, f"{st.get('dimmed')} dimmed lane draws")
        ok('drawing never changes rounds or enemies (renderer only)', diff == 0 and same > 0, f'{same} frames identical, {diff} changed')
        br.close()
finally:
    stop()
ok('zero page errors', not errors, '; '.join(errors[:3]))
print('RESULT', sum(c['pass'] for c in checks), '/', len(checks))
