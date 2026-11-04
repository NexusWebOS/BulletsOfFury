"""Who holds the wave dispatcher during long quiet stretches? (QA only)

    python _BUILD_SOURCE/probe_wave_holds_1103.py STAGE [DIFF] [SECONDS]

Runs the regular waves with the telemetry novice bot. Every second the screen is quiet while the next
authored wave is already due, it records the live enemies the dispatcher counts (not dead/dying,
not turret/bunker/mini/prop/naval) with their type, position relative to the camera, and age.
"""
from pathlib import Path
import json, sys, collections, http.server
from playwright.sync_api import sync_playwright
R = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(R / '_BUILD_SOURCE')); import shoot
http.server.SimpleHTTPRequestHandler.log_message = lambda *a: None
stage = int(sys.argv[1]); diff = sys.argv[2] if len(sys.argv) > 2 else 'normal'; secs = int(sys.argv[3]) if len(sys.argv) > 3 else 400
JS = r"""n=>{const out=[];for(let i=0;i<n;i++){if(state!==GS.PLAY)break;
  stageLoadTick();WT.F.input(1/60);WT.botInput();stateT+=1/60;updatePlay(1/60);WT.frame++;
  if(WT.frame%3===0){ctx.setTransform(SS,0,0,SS,0,0);drawWorld(3/60);}
  if(WT.frame%60)continue;
  const next=waveIdx<stagePlan.length?stagePlan[waveIdx]:null,due=next&&stageTimer>=next.t;
  const onScreen=e=>e.x>camLeftX()-20&&e.x<camRightX()+20&&e.y>viewTopY()-20&&e.y<VH+20;
  const counted=enemies.filter(e=>!e.dead&&e._dyingT==null&&!e._tur&&!e._bunker&&!e._mini&&!e._prop&&e.pattern!=='naval');
  const vis=counted.filter(onScreen);
  const quiet=vis.length===0&&!eBullets.some(b=>b&&!b.dead&&b.y>viewTopY()&&b.y<VH);
  if(quiet)out.push({q:1,t:+stageTimer.toFixed(1),clock:Math.round(WT.F.clock),wave:waveIdx,nextT:next?next.t:null,due:!!due,gap:+(_waveGap||0).toFixed(2),attempts:(WT.F.attempts||[]).length,live:counted.length,map:Math.round(typeof mapScroll!=='undefined'?mapScroll:-1)});
  if(due&&counted.length>=stageAiProfile(run.stage).cap-1)out.push({t:Math.round(stageTimer),wave:waveIdx,cap:stageAiProfile(run.stage).cap,live:counted.length,
    units:counted.map(e=>({type:e.type,pattern:e.pattern||null,x:Math.round(e.x),y:Math.round(e.y),camL:Math.round(camLeftX()),camR:Math.round(camRightX()),age:+(e.t||e.age||0).toFixed(1),hp:e.hp}))});
 }return out;}"""
port, stop = shoot.serve(str(R))
try:
    with sync_playwright() as pw:
        br = pw.chromium.launch(args=['--no-sandbox', '--mute-audio']); p = br.new_page(viewport={'width': 1100, 'height': 900}); p.set_default_timeout(300000)
        p.goto(f'http://127.0.0.1:{port}/index.html'); p.wait_for_function('()=>window.__bofFrames>4'); p.evaluate(shoot.TRAP_RAF)
        for f in ['enemy_behaviour_lab_1011.js', 'wave_followup_1103/reference_wave_maps.js', 'wave_followup_1103/wave_observe_1102.js', 'wave_telemetry_1103.js']:
            p.add_script_tag(path=str(R / '_BUILD_SOURCE' / f))
        p.evaluate('a=>WT.start(a[0],a[1],"left","novice",3)', [stage, diff])
        for _ in range(1200):
            if p.evaluate('n=>{stageLoadTick();return stageLoadReady(n);}', stage): break
            p.wait_for_timeout(50)
        rows = []
        for _ in range(secs // 10):
            rows += p.evaluate(JS, 600)
        br.close()
finally:
    stop()
q=[r for r in rows if r.get('q')]
print('quiet seconds', len(q))
import itertools
for k, g in itertools.groupby(q, key=lambda r: r['wave']):
    g = list(g)
    if len(g) >= 15: print('   wave', k, 'quiet', len(g), 's', 'stageTimer', g[0]['t'], '->', g[-1]['t'], 'next.t', g[0]['nextT'], 'due', g[-1]['due'], 'attempts', g[0]['attempts'], '->', g[-1]['attempts'], 'map', g[0]['map'], '->', g[-1]['map'])
c = collections.Counter(); where = collections.Counter()
for r in [r for r in rows if not r.get('q')]:
    for u in r['units']:
        c[u['type']] += 1
        side = 'above' if u['y'] < 0 else 'below' if u['y'] > 512 else 'left' if u['x'] < u['camL'] else 'right' if u['x'] > u['camR'] else 'on'
        where[(u['type'], side, u['pattern'])] += 1
print('held seconds (wave due, nothing visible, counted units alive):', len(rows))
for k, n in where.most_common(12): print('  ', n, k)
if False: print('example', json.dumps(rows[len(rows) // 2])[:600])
(R / f'_shots/waves_1103/holds_s{stage}_{diff}.json').write_text(json.dumps(rows))
