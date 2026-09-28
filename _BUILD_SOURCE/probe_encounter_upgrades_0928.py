#!/usr/bin/env python3
"""probe_encounter_upgrades_0928.py - the 0928 Stage 2-7 encounter pass, in real Chromium.

For each (encounter, difficulty, attack) it spawns the live owner, forces that attack through the
owner's own setter, steps the REAL loop (TRAP_RAF + synthetic clock, chunked with real pauses so
lazily-loaded art decodes) and records:
  * every targeted ball (tb28): committed target, lane length vs the muzzle->target distance, the
    point it actually arrived at, whether it was shot down / struck the pilot;
  * what the draw asked for: FOV cone keys, reticle keys, ball art keys (XART.get wrapped - the key,
    never the canvas identity or .src);
  * page errors, console errors, swallowed draw errors;
and saves screenshots at the warn / flight / arrival beats.

  python3 _BUILD_SOURCE/probe_encounter_upgrades_0928.py --only magmaward
"""
import os, sys, json, base64, argparse, http.server
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
http.server.SimpleHTTPRequestHandler.log_message = lambda *a: None
import shoot as sh
from playwright.sync_api import sync_playwright

OUT = os.path.join(sh.GAME, '_shots', 'opus0928', 'encounter_upgrades')

CASES = [
  # kind, stage, role, difficulty, modes
  ('magmaward', 2, 'mini', 'normal', ['ember-bombard', 'magma-rain']),
  ('magmaward', 2, 'mini', 'furious', ['ash-eruption', 'ash-rain', 'overdrive', 'ash-meteor', 'reaver-dive']),
  ('frostcruiser', 3, 'mini', 'hard', ['ice-lob']),
  ('frostcruiser', 3, 'mini', 'furious', ['overdrive', 'hail-meteor', 'cruiser-ram']),
  ('cryospear', 3, 'boss', 'normal', ['orb-siege', 'ice-lob']),
  ('cryospear', 3, 'boss', 'furious', ['hail-meteor']),
  ('olivewarden', 4, 'mini', 'hard', ['shell-lob']),
  ('olivewarden', 4, 'mini', 'furious', ['overdrive', 'shell-barrage']),
  ('stormsovereign', 4, 'boss', 'normal', ['storm-orbs']),
  ('stormsovereign', 4, 'boss', 'furious', ['chain-storm', 'giant-strike']),
  ('spacebomber', 5, 'mini', 'normal', ['lob', 'bombs']),
  ('spacebomber', 5, 'mini', 'furious', ['overdrive', 'carpet']),
  ('siegebomber', 6, 'mini', 'hard', ['lob', 'bombs']),
  ('siegebomber', 6, 'mini', 'furious', ['overdrive', 'carpet']),
]

SETUP = r"""
(c) => {
  diffKey=c.diff;DIFF=DIFFS[c.diff];run.mode='arcade';run.pilot='maverick';run.stage=c.stage;curStage=STAGES[c.stage-1];
  beginStage(c.stage);setState(GS.PLAY);player.reset();story=null;special=null;
  stagePlan=[];waveIdx=999;spawnClock=9999;enemies=[];eBullets=[];pBullets=[];powerups=[];
  boss=null;bossActive=false;subBoss=null;subBossActive=false;subBossDone=true;bossDefeated=false;
  if(c.stage===6){s6Opening=null;s6Wing=null;}   // the Stage 6 fly-in and route choice hold play; the fight is what is measured
  if(typeof groundTargetingReset==='function')groundTargetingReset();if(typeof tb28Reset==='function')tb28Reset();
  mapScroll=Math.min(1200,levelScrollRange()*.5);player.x=camLeftX()+viewW()/2;player.y=VH*.80;
  window.__hits=0;window.playerHit=function(){window.__hits++;};
  if(c.role==='mini'){spawnSubBoss__inner(c.kind);subBossActive=true;}else{spawnBoss(c.kind);bossActive=true;}
  const b=c.role==='mini'?subBoss:boss;b.enter=false;b._be=null;b._noHit=false;
  if(b._s3Arrival!=null)b._s3Arrival=9;
  window.__B=b;return {name:b.name,hp:b.hp,maxhp:b.maxhp,owner:!!b._er26};
}
"""

FORCE = r"""
(mode) => {
  const b=window.__B,R=b._er26,B=b._bomber,M=b._s7mod,W=b._whv;
  window.__asked={};window.__tbSeen=[];
  if(!window.__xg){window.__xg=XART.get.bind(XART);XART.get=function(k){window.__asked[k]=(window.__asked[k]||0)+1;return window.__xg(k);};}
  if(R){
    if(R.neutralOpening){R.neutralOpening=false;}
    if(mode==='overdrive'){ b.hp=b.maxhp*.3; R.mode='recover'; R.t=0; R.od=false; if(b._s4war&&b._s4war.shield){b._s4war.shield.rearming=false;} }
    else { if(/meteor|dive|ram|barrage|chain|giant/.test(mode)){ R.od=true; } er26Set(b,mode); }
    b.x=camLeftX()+viewW()/2; b.y=R.home; b._drawY=b.y;
    return {mode:R.mode,dur:R.dur,od:!!R.od,hp:b.hp};
  }
  if(B){
    b.enter=false;
    if(mode==='overdrive'){b.hp=b.maxhp*.4;B.core=Math.max(1,b.hp-B.parts.reduce((s,p)=>s+p.hp,0));B.od=false;B.mode='recover';B.t=99;B.dur=0;}
    else {if(mode==='carpet')B.od=true;siegeBomberSet(b,mode);}
    return {mode:B.mode,dur:B.dur,od:!!B.od,n:B.n};
  }
  if(typeof window.__force28==='function')return window.__force28(b,mode);
  return {err:'no owner'};
}
"""

SAMPLE = r"""
() => {
  const b=window.__B,R=b._er26,B=b._bomber,M=b._s7mod,W=b._whv;
  for(const q of tb28List)if(!window.__tbSeen.includes(q)){window.__tbSeen.push(q);}
  const mode=R?R.mode:B?B.mode:M?M.mode:W?(W.mode+':'+(W.st||'')+':'+(W.can&&W.can.last||'')):null, t=R?R.t:B?B.t:M?M.t:W?W.t:0;
  const od=!!(R&&R.od||B&&B.od||M&&M.od||W&&W.od);
  return {mode,t:+(+t||0).toFixed(2),live:tb28List.length,od,noHit:!!b._noHit,hits:window.__hits,
    rounds:eBullets.length,bx:Math.round(b.x),by:Math.round(b.y)};
}
"""

REPORT = r"""
() => {
  const L=window.__tbSeen.map(q=>({id:q.id,mode:q.mode,art:q.art,tx:Math.round(q.tx),ty:Math.round(q.ty),arrived:q.arrived,
    ax:q.ax==null?null:Math.round(q.ax),ay:q.ay==null?null:Math.round(q.ay),phase:q.phase,dead:q.dead,len:q.len?Math.round(q.len):null}));
  const k=Object.keys(window.__asked);
  return {balls:L,fov:k.filter(x=>/^bmfx_fov_/.test(x)).length,alerts:k.filter(x=>/^bmfx_alert_/.test(x)).length,
    reticle:k.filter(x=>/reticle/.test(x)).length,
    ballArt:k.filter(x=>/^(mwfx_fireball_|l23fx_rime_orb_|l23fx_cryo_ball_|xorb_|s4w_lightning_ball_|polish_ordnance|s7m_orb)/.test(x)).slice(0,12)};
}
"""

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--only', default=None); a = ap.parse_args()
    os.makedirs(OUT, exist_ok=True)
    port, stop = sh.serve(sh.GAME)
    summary = []
    with sync_playwright() as pw:
        br = pw.chromium.launch(args=['--no-sandbox', '--mute-audio'])
        for kind, stage, role, diff, modes in CASES:
            if a.only and a.only not in kind: continue
            for mode in modes:
                pg = br.new_page(viewport={'width': 1000, 'height': 1100})
                errs = []
                pg.on('pageerror', lambda e: errs.append('page:' + str(e)[:200]))
                pg.on('console', lambda m: errs.append('console:' + m.text[:200]) if m.type == 'error' or 'draw error' in m.text else None)
                pg.goto('http://127.0.0.1:%d/index.html' % port, wait_until='load', timeout=120000)
                pg.wait_for_function("() => (window.__bofFrames|0)>4", timeout=120000)
                pg.evaluate(sh.TRAP_RAF)
                info = pg.evaluate(SETUP, {'kind': kind, 'stage': stage, 'role': role, 'diff': diff})
                for _ in range(8): pg.evaluate(sh.STEP, 10); pg.wait_for_timeout(60)   # let the plates decode
                if stage == 3 and diff == 'furious':
                    # Furious Stage 3 opens neutral -> nuclear missile -> elemental form (0926). Play it through
                    # rather than forcing an attack onto a frozen, invulnerable hull.
                    pg.evaluate("() => { const b=window.__B; b.hp=b.maxhp*.74; }")
                    for _ in range(40):
                        pg.evaluate(sh.STEP, 15); pg.wait_for_timeout(20)
                        if pg.evaluate("() => { const b=window.__B; return !!b._s3Nuclear && !b._noHit && b._er26.mode!=='nuclear'; }"): break
                forced = pg.evaluate(FORCE, mode)
                tag = '%s_%s_%s' % (kind, diff, mode)
                trace = []
                shots = {0.45: 'warn', 1.25: 'late', 2.1: 'flight', 3.2: 'arrive'}
                taken = set(); sim = 0.0
                while sim < 6.0:
                    err = pg.evaluate(sh.STEP, 6)
                    if err: errs.append('step:' + err)
                    sim += 0.1; pg.wait_for_timeout(15)
                    s = pg.evaluate(SAMPLE); trace.append(s)
                    for at, name in shots.items():
                        if sim >= at and at not in taken:
                            taken.add(at)
                            d = pg.evaluate("() => document.getElementById('screen').toDataURL('image/png')")
                            open(os.path.join(OUT, tag + '_' + name + '.png'), 'wb').write(base64.b64decode(d.split(',', 1)[1]))
                rep = pg.evaluate(REPORT)
                arrived = [q for q in rep['balls'] if q['arrived']]
                offs = [abs(q['ax'] - q['tx']) + abs(q['ay'] - q['ty']) for q in arrived]
                row = {'case': tag, 'info': info, 'forced': forced, 'balls': len(rep['balls']), 'arrived': len(arrived),
                       'maxArrivalOff': max(offs) if offs else None, 'fovKeys': rep['fov'], 'alertKeys': rep['alerts'],
                       'reticleKeys': rep['reticle'], 'ballArt': rep['ballArt'], 'modes': sorted(set(t['mode'] for t in trace if t['mode'])),
                       'od': any(t['od'] for t in trace), 'noHitSeen': any(t['noHit'] for t in trace), 'hits': trace[-1]['hits'],
                       'errors': errs[:6]}
                summary.append(row)
                print('%-44s balls %2d arrived %2d off %s fov %d reticle %d art %s modes %s errs %d' % (tag, row['balls'], row['arrived'],
                      row['maxArrivalOff'], row['fovKeys'], row['reticleKeys'], len(row['ballArt']), ','.join(row['modes']), len(errs)), flush=True)
                if errs: print('   ', errs[:3])
                pg.close()
        br.close()
    stop()
    json.dump(summary, open(os.path.join(OUT, 'report.json'), 'w'), indent=1)

if __name__ == '__main__':
    main()
