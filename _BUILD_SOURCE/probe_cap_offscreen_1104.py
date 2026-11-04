"""How often do units below the screen hold a due wave? (QA only)
    python _BUILD_SOURCE/probe_cap_offscreen_1104.py STAGES DIFF [route]
Wraps updatePlay to replicate game.js's dispatch count each frame (same exclusions) and records frames
where a wave is due but held by the cap, and whether units fully below the screen (top edge > VH) or above
it make the difference. Prints per stage: due-held frames, frames the below-screen units alone cause,
the types involved, and the longest such run.
"""
from pathlib import Path
import json, sys, http.server
from playwright.sync_api import sync_playwright
R = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(R / '_BUILD_SOURCE')); import shoot
http.server.SimpleHTTPRequestHandler.log_message = lambda *a: None
stages = sys.argv[1].split(','); diff = sys.argv[2]; route = sys.argv[3] if len(sys.argv) > 3 else 'left'
SETUP = r"""()=>{const base=updatePlay;window.CQ={held:0,below:0,above:0,types:{},run:0,longest:0,frames:0};
 updatePlay=function(dt){try{if(state===GS.PLAY&&!bossActive&&!bossDefeated){const P=stageAiProfile(run.stage),nxt=waveIdx<stagePlan.length?stagePlan[waveIdx]:null;
  if(nxt&&stageTimer>=nxt.t&&(_waveGap||0)<=0){const np=run.stage===1?((nxt.fn&&nxt.fn._s1Pressure)||4):run.stage===8?3:1,at=P.cap-np;
   let n=0,b=0;const tb=[];for(const e of enemies){if(e.dead||e._dyingT!=null||e._tur||e._bunker||e._mini||e._prop||e.pattern==='naval')continue;n++;
    if(e.y-(e.h||0)/2>VH){b++;tb.push(e.type);}}
   CQ.frames++;if(n>at){CQ.held++;if(n-b<=at){CQ.below++;for(const t of tb)CQ.types[t]=(CQ.types[t]||0)+1;CQ.run++;CQ.longest=Math.max(CQ.longest,CQ.run);}else CQ.run=0;}else CQ.run=0;}}}catch(_e){}
  return base.apply(this,arguments);};}"""
STEP = r"""n=>{for(let i=0;i<n;i++){if(state!==GS.PLAY||WT.F.done)break;stageLoadTick();WT.F.input(1/60);WT.botInput();stateT+=1/60;updatePlay(1/60);WT.frame++;
 if(WT.frame%3===0){ctx.setTransform(SS,0,0,SS,0,0);drawWorld(3/60);}}return {done:WT.F.done||state!==GS.PLAY,clock:WT.F.clock};}"""
port, stop = shoot.serve(str(R))
try:
    with sync_playwright() as pw:
        br = pw.chromium.launch(args=['--no-sandbox', '--mute-audio'])
        for st in stages:
            p = br.new_page(viewport={'width': 1100, 'height': 900}); p.set_default_timeout(300000); errs = []
            p.on('pageerror', lambda e: errs.append(str(e)[:200]))
            p.add_init_script("Object.defineProperty(navigator,'getGamepads',{value:()=>[]});")
            p.goto(f'http://127.0.0.1:{port}/index.html'); p.wait_for_function('()=>window.__bofFrames>4'); p.evaluate(shoot.TRAP_RAF)
            for f in ['enemy_behaviour_lab_1011.js', 'wave_followup_1103/reference_wave_maps.js', 'wave_followup_1103/wave_observe_1102.js', 'wave_telemetry_1103.js']:
                p.add_script_tag(path=str(R / '_BUILD_SOURCE' / f))
            p.evaluate('a=>WT.start(a[0],a[1],a[2],"novice",3)', [int(st), diff, route])
            for _ in range(1200):
                if p.evaluate('n=>{stageLoadTick();return stageLoadReady(n);}', int(st)): break
                p.wait_for_timeout(50)
            p.evaluate(SETUP)
            for _ in range(60):
                s = p.evaluate(STEP, 600)
                for _ in range(3): p.evaluate('()=>{const cb=window.__bofPendingRAF;window.__bofPendingRAF=null;if(cb)cb(performance.now());}')
                if s['done'] or s['clock'] > 420: break
            q = p.evaluate('()=>CQ')
            print('STAGE', st, diff, 'clock', round(s['clock']), 'dueFrames', q['frames'], 'heldFrames', q['held'], 'heldOnlyByBelowScreen', q['below'], f"({q['below']/60:.1f}s)", 'longestRun', f"{q['longest']/60:.1f}s", 'types', q['types'], 'errors', errs[:2], flush=True)
            p.close()
        br.close()
finally:
    stop()
