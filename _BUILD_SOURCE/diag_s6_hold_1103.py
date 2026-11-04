"""Stage 6 hold diagnosis: log every clock-hold flag once a second (QA only).
    python _BUILD_SOURCE/diag_s6_hold_1103.py [diff] [seconds] [route]
"""
from pathlib import Path
import json, sys, http.server
from playwright.sync_api import sync_playwright
R = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(R / '_BUILD_SOURCE')); import shoot
http.server.SimpleHTTPRequestHandler.log_message = lambda *a: None
diff = sys.argv[1] if len(sys.argv) > 1 else 'hard'; secs = int(sys.argv[2]) if len(sys.argv) > 2 else 200; route = sys.argv[3] if len(sys.argv) > 3 else 'left'
SNAP = r"""()=>{const C=window.BOF_CARRIER_ASSAULT?.state;return {st:+stageTimer.toFixed(1),wi:typeof waveIdx!=='undefined'?waveIdx:null,
 nE:enemies.filter(e=>!e.dead).length,nB:eBullets.length,
 hold:typeof carrierAssaultHold111==='function'?carrierAssaultHold111():null,
 open:typeof s6OpeningActive==='function'?s6OpeningActive():null,
 blocked:typeof sc12Blocked==='function'?sc12Blocked():null,dlg:typeof sc12DialogueHold==='function'?sc12DialogueHold():null,
 ca:C&&C.active?{k:C.active.key,grp:C.active.group?{done:!!C.active.group.done,n:(C.active.group.carriers||C.active.group.list||[]).length}:null,actor:C.active.actor?{hp:C.active.actor.hp,dead:!!C.active.actor.dead,y:Math.round(C.active.actor.y),ph:C.active.actor._ca111?.phase}:null}:null,
 caQ:C?C.queue.map(q=>q.key):null,caDone:C?[...C.completed]:null,caActors:C?C.actors.map(e=>e._ca111.role+':'+e._ca111.kind+':'+Math.round(e.y)+':'+(e.dead?'D':'L')):null,
 cc:typeof CC111!=='undefined'?CC111.carriers.map(c=>({done:!!c.done,ph:c.phase||c.state,hp:c.hp??c.e?.hp,y:Math.round(c.y??c.e?.y??0)})):null,
 parts:[typeof story,!!story,typeof thaw,!!thaw,typeof fb2Talk,!!fb2Talk,typeof fb2Intro,!!fb2Intro,warnT,String(sc12DialogueHold).slice(0,90)],boss:!!bossActive,thaw:typeof thaw!=='undefined'&&thaw?(typeof thaw==='object'?Object.keys(thaw).slice(0,8).join(','):String(thaw)):null,fb2Talk:typeof fb2Talk!=='undefined'&&fb2Talk?JSON.stringify(fb2Talk).slice(0,240):null,fb2Intro:typeof fb2Intro!=='undefined'&&fb2Intro?String(Object.keys(fb2Intro)).slice(0,120):null,sub:!!subBossActive,warn:!!bossWarned,story:!!story};}"""
port, stop = shoot.serve(str(R))
try:
    with sync_playwright() as pw:
        br = pw.chromium.launch(args=['--no-sandbox', '--mute-audio']); p = br.new_page(viewport={'width': 1100, 'height': 900}); p.set_default_timeout(300000)
        errs = []; p.on('pageerror', lambda e: errs.append(str(e)[:200]))
        p.add_init_script("Object.defineProperty(navigator,'getGamepads',{value:()=>[]});")
        p.goto(f'http://127.0.0.1:{port}/index.html'); p.wait_for_function('()=>window.__bofFrames>4'); p.evaluate(shoot.TRAP_RAF)
        for f in ['enemy_behaviour_lab_1011.js', 'wave_followup_1103/reference_wave_maps.js', 'wave_followup_1103/wave_observe_1102.js', 'wave_telemetry_1103.js']:
            p.add_script_tag(path=str(R / '_BUILD_SOURCE' / f))
        p.evaluate('a=>WT.start(6,a[0],a[1],"novice",3)', [diff, route])
        for _ in range(1200):
            if p.evaluate('()=>{stageLoadTick();return stageLoadReady(6);}'): break
            p.wait_for_timeout(50)
        prev = None
        for sec in range(secs):
            s = p.evaluate('()=>WT.steps(60)')
            for _ in range(1): p.evaluate('()=>{const cb=window.__bofPendingRAF;window.__bofPendingRAF=null;if(cb)cb(performance.now());}')
            snap = p.evaluate(SNAP)
            key = json.dumps({k: v for k, v in snap.items() if k not in ('st', 'nE', 'nB', 'caActors', 'cc')})
            if key != prev or sec % 10 == 0: print(sec, json.dumps(snap), flush=True)
            prev = key
            if s['done'] or s['state'] != 'play': print('END', s); break
        print('errors', errs[:3]); br.close()
finally:
    stop()
