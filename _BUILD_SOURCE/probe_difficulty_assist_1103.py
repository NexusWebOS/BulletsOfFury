"""Native probe for assets/difficulty_assist_1103.js (DA13).

    python _BUILD_SOURCE/probe_difficulty_assist_1103.py

Real index.html, today's wave observer fixture, the telemetry dodge bot. Checks:
  - Furious: DA13 never activates, nothing held or capped
  - Normal/Hard Stage 7 waves: rounds are held and every held round comes back (held = released + queued),
    groups release whole, live enemy rounds respect the speed caps
  - a boss fight on Normal: DA13 stands down (no hold, no cap) and releases anything queued
  - Stage 2 Normal: debris thinned, firewall falls at the slower pace
  - Stage 8 Normal: beam/flamethrower warnings extended
  - zero page errors
"""
from pathlib import Path
import json, sys, http.server
from playwright.sync_api import sync_playwright
R = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(R / '_BUILD_SOURCE')); import shoot
http.server.SimpleHTTPRequestHandler.log_message = lambda *a: None
checks, errors = [], []
def ok(name, cond, info=''):
    checks.append({'name': name, 'pass': bool(cond), 'info': info}); print(('PASS ' if cond else 'FAIL ') + name, info, flush=True)
STEP = r"""n=>{const S=DA13.state,T=DA13.tiers[diffKey];let maxOver=0,onFrames=0,wallV=[],groupsWhole=true;
 for(let i=0;i<n;i++){if(state!==GS.PLAY||WT.F.done)break;
  const W=typeof wfx!=='undefined'&&wfx&&wfx.fseq&&wfx.fseq.wave,y0=W?W.y:null;
  const q0=S.queue.length;
  stageLoadTick();WT.F.input(1/60);WT.botInput();stateT+=1/60;run.shield=0;updatePlay(1/60);WT.frame++;
  if(WT.frame%3===0){ctx.setTransform(SS,0,0,SS,0,0);drawWorld(3/60);}
  if(W&&wfx&&wfx.fseq&&wfx.fseq.wave===W&&y0!=null)wallV.push((W.y-y0)*60);
  if(S.on&&T){onFrames++;for(const b of eBullets){if(!b||b.dead)continue;const sp=Math.hypot(b.vx||0,b.vy||0)*60,cap=b._da13Aimed?T.aimed:T.pattern;if(sp>cap*1.03)maxOver=Math.max(maxOver,sp-cap);}}
 }
 const queued=S.queue.reduce((a,g)=>a+g.items.length,0);
 return {on:S.on,onFrames,stat:{...S.stat},queued,maxOver:Math.round(maxOver),wallV:wallV.length?Math.round(wallV.reduce((a,b)=>a+b,0)/wallV.length):null,clock:WT.F.clock,boss:!!(bossActive||subBossActive)};}"""
port, stop = shoot.serve(str(R))
try:
    with sync_playwright() as pw:
        br = pw.chromium.launch(args=['--no-sandbox', '--mute-audio'])
        def page(stage, diff, see=False):
            p = br.new_page(viewport={'width': 1100, 'height': 900}); p.set_default_timeout(300000)
            p.on('pageerror', lambda e: errors.append(f'{stage}/{diff}: ' + str(e)[:200]))
            if see: p.add_init_script('window.WT_SEE_HAZARDS=1;')
            p.goto(f'http://127.0.0.1:{port}/index.html'); p.wait_for_function('()=>window.__bofFrames>4&&typeof DA13!=="undefined"'); p.evaluate(shoot.TRAP_RAF)
            for f in ['enemy_behaviour_lab_1011.js', 'wave_followup_1103/reference_wave_maps.js', 'wave_followup_1103/wave_observe_1102.js', 'wave_telemetry_1103.js']:
                p.add_script_tag(path=str(R / '_BUILD_SOURCE' / f))
            p.evaluate('a=>WT.start(a[0],a[1],"left","novice",3)', [stage, diff])
            for _ in range(1200):
                if p.evaluate('n=>{stageLoadTick();return stageLoadReady(n);}', stage): break
                p.wait_for_timeout(50)
            return p
        def run(p, seconds):
            out = None
            for _ in range(int(seconds * 60 / 600)):
                out = p.evaluate(STEP, 600)
                for _ in range(2): p.evaluate('()=>{const cb=window.__bofPendingRAF;window.__bofPendingRAF=null;if(cb)cb(performance.now());}')
            return out
        ONLY_HAZ = 'hazards' in sys.argv
        # Furious: inert
        if not ONLY_HAZ:
          p = page(7, 'furious'); r = run(p, 90)
          ok('Furious Stage 7: DA13 never activates', r['onFrames'] == 0 and r['stat']['held'] == 0 and r['stat']['capped'] == 0, json.dumps(r['stat']))
          p.close()
          for diff in ['normal', 'hard']:
              p = page(7, diff); r = run(p, 120)
              st = r['stat']
              ok(f'{diff} Stage 7: fire budget holds rounds', st['held'] > 0, f"held {st['held']} in {st['groups']} groups, longest wait {st['maxWait']} s")
              ok(f'{diff} Stage 7: every held round comes back (held = released + queued)', st['held'] == st['released'] + r['queued'], f"released {st['released']}, queued now {r['queued']}")
              ok(f'{diff} Stage 7: no round waits longer than 0.6 s (+1 frame)', st['maxWait'] <= 0.62, str(st['maxWait']))
              ok(f'{diff} Stage 7: live enemy rounds respect the speed caps', r['maxOver'] == 0, f"worst excess {r['maxOver']} px/s, capped {st['capped']}")
              # boss: stand down
              p.evaluate("()=>{const B=STAGES[run.stage-1].boss;subBossDone=subBossTriggered=true;bossWarned=false;spawnBoss(B);bossActive=true;}")
              r2 = run(p, 10)
              ok(f'{diff}: during a boss fight DA13 stands down and holds nothing', not r2['on'] and r2['queued'] == 0 and r2['stat']['held'] == r2['stat']['released'], json.dumps({k: r2['stat'][k] for k in ['held', 'released']}))
              p.close()
        p = page(2, 'normal'); r = run(p, 300); st = r['stat']
        ok('Normal Stage 2: fire debris thinned', st['debrisDropped'] > 0, f"dropped {st['debrisDropped']}, grazes refused {st['debrisRefused']}")
        fwant = round((512 + 300) / 1.7)
        ok('Normal Stage 2: firewall falls at the slower pace', r['wallV'] is None or abs(r['wallV'] - fwant) < fwant * .15, f"measured {r['wallV']} px/s, want ~{fwant} (native {round((512 + 300) / 1.25)})")
        p.close()
        p = page(8, 'normal'); r = run(p, 300); st = r['stat']
        ok('Normal Stage 8: alien beam warnings extended', st['beamExtended'] > 0, f"extended {st['beamExtended']}")
        p.close()
        br.close()
finally:
    stop()
ok('zero page errors', not errors, '; '.join(errors[:3]))
(R / '_shots/waves_1103/assist_probe.json').write_text(json.dumps({'checks': checks, 'errors': errors}, indent=2))
print('RESULT', sum(c['pass'] for c in checks), '/', len(checks))
