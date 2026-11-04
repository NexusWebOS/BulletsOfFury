"""Native probe for assets/wave_followups_1104.js (WF14).
    python _BUILD_SOURCE/probe_wave_followups_1104.py
Stage 6 scene: time to finish with no input vs pressing confirm every 0.5 s, the demo still fires.
Stage 5 rammer: tell length, blinks, lurch returns to the warned start, charge speed and lane fidelity on
Normal/Hard, and Hard unchanged vs WF14_RAM_OFF. Zero page errors.
"""
from pathlib import Path
import json, sys, math, http.server
from playwright.sync_api import sync_playwright
R = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(R / '_BUILD_SOURCE')); import shoot
http.server.SimpleHTTPRequestHandler.log_message = lambda *a: None
checks, errors = [], []
def ok(name, cond, info=''):
    checks.append({'name': name, 'pass': bool(cond), 'info': info}); print(('PASS ' if cond else 'FAIL ') + name, info, flush=True)
STEP = r"""n=>{for(let i=0;i<n;i++){if(state!==GS.PLAY||WT.F.done)break;stageLoadTick();WT.F.input(1/60);WT.botInput();stateT+=1/60;updatePlay(1/60);WT.frame++;
 if(WT.frame%3===0){ctx.setTransform(SS,0,0,SS,0,0);drawWorld(3/60);}}return {talk:typeof fb2TalkActive==='function'&&fb2TalkActive(),clock:WT.F.clock};}"""
def page(br, port, init=''):
    p = br.new_page(viewport={'width': 1100, 'height': 900}); p.set_default_timeout(300000)
    p.on('pageerror', lambda e: errors.append(str(e)[:200]))
    p.add_init_script("Object.defineProperty(navigator,'getGamepads',{value:()=>[]});" + init)
    p.goto(f'http://127.0.0.1:{port}/index.html'); p.wait_for_function('()=>window.__bofFrames>4&&typeof WF14!=="undefined"||window.WF14_RAM_OFF||window.WF14_OFF'); p.evaluate(shoot.TRAP_RAF)
    for f in ['enemy_behaviour_lab_1011.js', 'wave_followup_1103/reference_wave_maps.js', 'wave_followup_1103/wave_observe_1102.js', 'wave_telemetry_1103.js']:
        p.add_script_tag(path=str(R / '_BUILD_SOURCE' / f))
    return p
def start(p, stage, diff):
    p.evaluate('a=>WT.start(a[0],a[1],"left","still",3)', [stage, diff])
    for _ in range(1200):
        if p.evaluate('n=>{stageLoadTick();return stageLoadReady(n);}', stage): break
        p.wait_for_timeout(50)
def scene(br, port, press):
    p = page(br, port); start(p, 6, 'hard'); p.evaluate('()=>{run.pilot="cole";}')
    for _ in range(400):
        if p.evaluate(STEP, 30)['talk']: break
    p.evaluate('()=>{WT.F.input=()=>{};WT.botInput=()=>{};}')   # the harness taps fire itself; only our presses count
    t0 = p.evaluate('()=>WT.F.clock'); demo = 0
    for i in range(6000):
        if press and i % 30 == 0:
            p.keyboard.down(' '); r = p.evaluate(STEP, 1); p.keyboard.up(' ')
        else:
            r = p.evaluate(STEP, 1)
        d = p.evaluate('()=>fb2Talk?.demo?.fired||0'); demo = max(demo, d)
        if not r['talk']: break
    res = {'secs': round((i + 1) / 60, 1), 'demo': demo, 'stat': p.evaluate('()=>({...WF14.stat})'), 'pilot': p.evaluate('()=>run.pilot')}
    p.close(); return res
RAM = r"""a=>{const [x]=a;const e=spawnEnemy('s5rammer',camLeftX()+x,-90,{});e.hp=e.maxhp=99999;
 const L={warm:null,tellT:0,blinks:0,start:null,ramStart:null,maxSp:0,off:0,lurch:0};let prev=null,ph=null,px=0,py=0;
 for(let i=0;i<600;i++){if(e.dead)break;player.invuln=9;stageLoadTick();stateT+=1/60;updatePlay(1/60);
  const A=e._s511;if(!A)continue;
  if(A.phase==='tell'){if(ph!=='tell'){L.warm=A.warm;L.start={x:e.x,y:e.y};}L.tellT+=1/60;if(e.flash>0&&!(prev>0))L.blinks++;L.lurch=Math.max(L.lurch,-(Math.cos(A.head)*(e.x-L.start.x)+Math.sin(A.head)*(e.y-L.start.y)));}
  if(A.phase==='ram'){if(ph!=='ram'){L.ramStart={x:e.x,y:e.y};L.head=A.head;L.endTell=Math.abs(-Math.sin(A.head)*(e.x-L.start.x)+Math.cos(A.head)*(e.y-L.start.y));}
   else{L.maxSp=Math.max(L.maxSp,Math.hypot(e.x-px,e.y-py)*60);
    const dx=e.x-L.ramStart.x,dy=e.y-L.ramStart.y;L.off=Math.max(L.off,Math.abs(-Math.sin(L.head)*dx+Math.cos(L.head)*dy));}}
  prev=e.flash;ph=A.phase;px=e.x;py=e.y;}
 return L;}"""

CAP = r"""a=>{const [where]=a;stagePlan=[];waveIdx=0;enemies.length=0;let fired=0;
 const cap=stageAiProfile(run.stage).cap;
 for(let i=0;i<cap+1;i++){const e=spawnEnemy('drone',camLeftX()+60+i*30,-60,{});if(e){e.hp=e.maxhp=9999;}}
 const park=()=>{for(const e of enemies)if(!e.dead){e.y=where==='below'?VH+(e.h||20)/2+12:VH*.45;}};
 park();stagePlan.push({t:0,fn:()=>{fired++;}});_waveGap=0;stageTimer=Math.max(stageTimer,1);
 for(let i=0;i<6&&!fired;i++){park();stageLoadTick();stateT+=1/60;updatePlay(1/60);}
 return {fired,cap,live:enemies.filter(e=>!e.dead).length};}"""

port, stop = shoot.serve(str(R))
try:
    with sync_playwright() as pw:
        br = pw.chromium.launch(args=['--no-sandbox', '--mute-audio'])
        idle = scene(br, port, False); fast = scene(br, port, True)
        print('scene idle', idle, 'pressed', fast)
        ok('scene auto-advances without input (unchanged)', idle['secs'] > 30 and idle['stat']['talkSkips'] == 0, f"{idle['secs']} s")
        ok('pressing confirm finishes lines and advances', fast['stat']['talkSkips'] >= 10 and fast['stat']['talkFinishes'] >= 1, json.dumps(fast['stat']))
        ok('pressing makes the scene much shorter', fast['secs'] < idle['secs'] * .6, f"{fast['secs']} s vs {idle['secs']} s")
        ok('Cole demo still fires its lasers when skipping', fast['pilot'] != 'cole' or fast['demo'] > 0, f"pilot {fast['pilot']}, demo rounds {fast['demo']}")
        res = {}
        for diff, init in [('normal', ''), ('normal', 'window.WF14_RAM_OFF=1;'), ('hard', ''), ('hard', 'window.WF14_RAM_OFF=1;')]:
            p = page(br, port, init); start(p, 5, diff)
            p.evaluate('()=>{WT.F.input=()=>{};stagePlan=[];spawnClock=9999;}')
            res[(diff, bool(init))] = p.evaluate(RAM, [240]); p.close()
        n, n0, h, h0 = res[('normal', False)], res[('normal', True)], res[('hard', False)], res[('hard', True)]
        print('rammer normal OFF', n0, '/ normal', n, '/ hard', h, '/ hard OFF', h0)
        ok('Normal tell lasts 0.90 s', abs(n['warm'] - .9) < 1e-6 and abs(n['tellT'] - .9) < .05, f"warm {n['warm']}, measured {n['tellT']:.2f}")
        ok('two white blinks during the tell (Normal and Hard)', n['blinks'] == 2 and h['blinks'] == 2, f"{n['blinks']}/{h['blinks']}")
        ok('lurch eases back against the charge line, charge starts on the warned lane', n['lurch'] >= 6 and n['endTell'] < 1.0 and h['endTell'] < 1.0, f"back {n['lurch']:.1f} px, sideways at charge {n['endTell']:.2f}/{h['endTell']:.2f} px")
        ok('Normal charge slower (360 cap + stage drift) vs OFF', n['maxSp'] <= 370 and n0['maxSp'] > 430, f"{n['maxSp']:.0f} vs OFF {n0['maxSp']:.0f} px/s")
        ok('charge stays on the warned lane', n['off'] < 1 and h['off'] < 1, f"{n['off']:.2f}/{h['off']:.2f} px")
        ok('Hard tell length and speed unchanged vs OFF', abs(h['warm'] - h0['warm']) < 1e-6 and abs(h['maxSp'] - h0['maxSp']) < 5, f"warm {h['warm']} vs {h0['warm']}, {h['maxSp']:.0f} vs {h0['maxSp']:.0f} px/s")
        cap = {}
        for where, init in [('below', ''), ('onscreen', ''), ('below', 'window.WF14_CAP_OFF=1;')]:
            p = page(br, port, init); start(p, 4, 'normal'); p.evaluate('()=>{WT.F.input=()=>{};spawnClock=9999;}')
            cap[(where, bool(init))] = p.evaluate(CAP, [where]); p.close()
        print('cap', cap)
        ok('due wave fires when the cap is full only of units below the screen', cap[('below', False)]['fired'] == 1, json.dumps(cap[('below', False)]))
        ok('units on screen still hold the wave', cap[('onscreen', False)]['fired'] == 0, json.dumps(cap[('onscreen', False)]))
        ok('WF14_CAP_OFF restores the old count', cap[('below', True)]['fired'] == 0, json.dumps(cap[('below', True)]))
        br.close()
finally:
    stop()
ok('zero page errors', not errors, '; '.join(errors[:3]))
print('RESULT', sum(c['pass'] for c in checks), '/', len(checks))
