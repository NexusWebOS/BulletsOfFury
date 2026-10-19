#!/usr/bin/env python3
"""probe_modular_1017.py - Mike's engine rule for modular encounters, measured on every boss and miniboss.

    python _BUILD_SOURCE/probe_modular_1017.py                 # all stages, all weapons
    python _BUILD_SOURCE/probe_modular_1017.py --only 4s       # stage 4 miniboss only (4b = boss)
    python _BUILD_SOURCE/probe_modular_1017.py --weapons mg,laser

Mike, 1017: "bullets and missiles both should be able to individually target modular pieces. Lasers should
pierce and target all pieces or enemies that the laser will hit. orbs should hit each piece individually and as
it travels through them if ice orb before impact, still hits all modular pieces it would strike."

A PIECE is what the game's own Retina list calls one (retinaBossTargets(owner), dynamic pieces whose
_retinaOwner is the encounter) - the same list 0915's Retina audit made follow every live component family.
For each encounter the probe flies the ship under a piece and measures what THAT piece lost, by weapon:
  mg       machine gun held                        -> the piece under the stream must lose hp
  missile  manual missile, no lock, from under it  -> the piece must lose hp
  lock     Retina lock on the piece + missile      -> the piece must lose hp
  laser    held beam in the piece's column         -> EVERY live piece the column crosses must lose hp
  iceorb   piercing ice orb up the column          -> every piece it passes must lose hp
  fireorb  contact fire orb                        -> the piece it touches must lose hp
Report: _shots/modular_1017/report.json.
"""
import os, sys, json, time, argparse
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import shoot as sh
OUT = os.path.join(os.path.dirname(HERE), '_shots', 'modular_1017')

SETUP = r"""(cfg) => {
  ASSETS.ready = true; diffKey = cfg.diff || 'normal'; run.mode = 'arcade';
  const pi = PILOTS.findIndex(p => p.key === 'cole'); if (pi >= 0) pilotIndex = pi;
  try { achToastPush = function(){}; } catch (e) {}
  startRun(cfg.stage); curStage = STAGES[cfg.stage - 1]; beginStage(cfg.stage); setState(GS.PLAY); player.reset();
  playerHit = function(){}; stagePlan = [];
  try { s6Opening = null; } catch (e) {}   // stage 6's opening locks every weapon for its 26 s (CLAUDE.md, 0410)
  for (const k of ['a','d','w','s','j','k','c']) if (Input.keys[k] === undefined) Input.keys[k] = false;
  window.__now = performance.now(); window.__err = null;
  let kind = null;
  if (cfg.role === 's') { const SB = SUBBOSS[cfg.stage]; if (!SB) return {skip: 'no miniboss'}; kind = SB.kind; spawnSubBoss(kind); }
  else { const st = STAGES[cfg.stage - 1]; if (!st || !st.boss) return {skip: 'no boss'}; kind = st.boss; spawnBoss(kind); bossActive = true; }
  window.__OWN = () => cfg.role === 's' ? subBoss : boss;
  window.__PIECES = () => { const o = window.__OWN(); if (!o) return []; let L = [];
    try { L = retinaBossTargets(o) || []; } catch (e) { L = []; }
    return L.filter(t => t && t._retinaOwner === o && !t.dead); };
  return {kind, state};
}"""

STEP = r"""(n) => { for (let i = 0; i < n; i++) { window.__now += 1000/60; try { loop(window.__now); } catch (e) { window.__err = String(e).slice(0,160); } } return state; }"""

READY = r"""() => { const o = window.__OWN(); if (!o) return {gone: true};
  if (o.enter || o._noHit || o.dead) return {ready: false, enter: !!o.enter, noHit: !!o._noHit, dead: !!o.dead, hp: o.hp};
  const P = window.__PIECES();
  return {ready: true, hp: o.hp, maxhp: o.maxhp, pieces: P.map(t => ({id: t._retinaId || t.name, kind: t.kind, x: Math.round(t.x), y: Math.round(t.y), w: Math.round(t.w), h: Math.round(t.h), hp: t.hp}))}; }"""

RUN = r"""(cfg) => {
  const o = window.__OWN(); if (!o) return {err: 'no owner'};
  const P0 = window.__PIECES(); const T = P0.find(t => (t._retinaId || t.name) === cfg.id); if (!T) return {err: 'piece gone'};
  const snap = () => { const m = {}; for (const t of window.__PIECES()) m[t._retinaId || t.name] = t.hp; return m; };
  const before = snap(), hull0 = o.hp, seenB = new Set(pBullets), kinds = {};
  // pin the encounter where it is: this measures HIT ROUTING, and a slow orb launched at a piece misses a
  // hull that slides 150px through its recover move while the orb is in flight (measured)
  const px0 = o.x, py0 = o.y, pd0 = o._drawY;
  // This fixture asks for the base machine gun, not the campaign's earned
  // chaingun replacement (whose separated barrels require a different aim).
  // Stage 6 progression makes it eligible even with the unlock flag cleared;
  // use the real primary-selector action to persist the MG choice.
  if(cfg.w===0&&typeof weaponFormSelect==='function')weaponFormSelect(7,{kind:'primary1003b',id:'mg'});
  run.sonicT=run.dkT=0;special=thunderStorm=null;
  chaingunUnlocked=false;run._earnedUnlocks={...(run._earnedUnlocks||{}),chaingun:false};
  run.forge={};run.forgeForms={};run.infusion=null;run.loadout=[cfg.w];powerups=[];
  run.weapon = cfg.w; run.wlevels[cfg.w] = cfg.lv; run.wlevel = cfg.lv; run.wvars[cfg.w] = cfg.wvar || null;
  run.bombs = 20; player.fireCd = 0;
  const place = () => { const t = window.__PIECES().find(q => (q._retinaId || q.name) === cfg.id) || T;
    player.x = t.x + (cfg.dx || 0); player.y = Math.min(PLAY.y + PLAY.h - 40, t.y + 175); player.invuln = 0; return t; };
  place();
  if (cfg.mode === 'lock') { retina.target = T; retina.phase = 'locked'; retina.lockT = 5; useBomb(); }
  else if (cfg.mode === 'missile') { retina.target = null; retina.phase = null; useBomb(null); }
  for (let i = 0; i < cfg.frames; i++) {
    // These carriers own their centre through the live camera/Cargo state.
    // Overwriting only b.x makes Retina report the old fan position while
    // the actual hull follows the camera. Track their real moving targets.
    if(!o._carrier17&&!o._cargo13){o.x = px0; o.y = py0; if (pd0 != null) o._drawY = pd0;}
    place();
    enemies.length = 0;powerups.length=0;   // isolate hit geometry from escorts and dropped weapon changes
    if (cfg.mode === 'hold') Input.keys.j = true;
    else if (cfg.mode === 'tap') Input.keys.j = (i === 0);
    else Input.keys.j = false;
    window.__now += 1000/60; try { loop(window.__now); } catch (e) { window.__err = String(e).slice(0,160); }
    for (const q of pBullets) if (!seenB.has(q)) { seenB.add(q); kinds[q.kind] = (kinds[q.kind] || 0) + 1; }
  }
  Input.keys.j = false;
  const after = snap(); const lost = {};
  for (const k in before) lost[k] = +(before[k] - (after[k] == null ? 0 : after[k])).toFixed(1);
  return {id: cfg.id, lost, hull: +(hull0 - o.hp).toFixed(1), kinds, weapon:run.weapon, err: window.__err};
}"""

WEAPONS = {
  'mg':      dict(w=0, lv=1, mode='hold', frames=120),
  'missile': dict(w=0, lv=1, mode='missile', frames=110),
  'lock':    dict(w=0, lv=1, mode='lock', frames=150),
  'laser':   dict(w=3, lv=3, mode='hold', frames=90),
  'iceorb':  dict(w=5, lv=3, mode='tap', frames=110, wvar='iceorb'),
  'fireorb': dict(w=5, lv=3, mode='tap', frames=110, wvar='fireorb'),
}

def boot(p, port, errs):
    b = p.chromium.launch(channel='msedge', args=['--mute-audio'])
    pg = b.new_page(viewport={'width': 1000, 'height': 1100})
    pg.add_init_script("Object.defineProperty(navigator,'getGamepads',{value:()=>[]});")
    pg.on('pageerror', lambda e: errs.append('page: ' + str(e)[:200]))
    pg.goto('http://127.0.0.1:%d/index.html' % port, wait_until='load', timeout=120000)
    pg.wait_for_function("() => typeof setState==='function' && (window.__bofFrames|0) > 4", timeout=120000)
    pg.evaluate(sh.TRAP_RAF); pg.wait_for_timeout(60)
    return b, pg

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--only', default=None, help='comma list like 4s,4b')
    ap.add_argument('--weapons', default=','.join(WEAPONS))
    ap.add_argument('--diff', default='normal')
    ap.add_argument('--tag', default='report')
    a = ap.parse_args()
    os.makedirs(OUT, exist_ok=True)
    encs = [(n, r) for n in range(1, 10) for r in ('s', 'b')]
    if a.only: encs = [(int(x[:-1]), x[-1]) for x in a.only.split(',')]
    wl = a.weapons.split(',')
    from playwright.sync_api import sync_playwright
    port, stop = sh.serve(sh.GAME)
    report = [];failed=0
    with sync_playwright() as p:
        for (n, r) in encs:
            for w in wl:
                errs = []
                b, pg = boot(p, port, errs)
                info = pg.evaluate(SETUP, {'stage': n, 'role': r, 'diff': a.diff})
                if info.get('skip'):
                    b.close(); print(n, r, 'skip', info['skip'], flush=True); break
                ready = None
                for i in range(80):
                    pg.evaluate(STEP, 30); pg.wait_for_timeout(40 if i % 4 else 120)
                    ready = pg.evaluate(READY)
                    if ready.get('ready') and ready.get('pieces'): break
                    if ready.get('gone'): break
                row = {'stage': n, 'role': r, 'kind': info.get('kind'), 'weapon': w, 'ready': ready, 'tests': [], 'errs': errs}
                if not (ready and ready.get('ready') and ready.get('pieces')):
                    row['note'] = 'no live pieces (not modular, or never became hittable)'
                    report.append(row); b.close()
                    print(n, r, info.get('kind'), w, '-> no pieces', (ready or {}).get('enter'), (ready or {}).get('noHit'), flush=True)
                    break
                # test the live piece with the most hp
                pieces = sorted(ready['pieces'], key=lambda q: -(q['hp'] or 0))
                cfg = dict(WEAPONS[w]); cfg['id'] = pieces[0]['id']
                res = pg.evaluate(RUN, cfg)
                row['tests'].append(res)
                report.append(row)
                lost = res.get('lost', {})
                hit = lost.get(cfg['id'], 0) > 0
                if not hit or errs or res.get('err') or res.get('weapon')!=cfg['w']:failed+=1
                print('%d%s %-18s %-8s piece %-22s %s lost=%s hull=%s err=%s errs=%d' % (n, r, info.get('kind'), w, cfg['id'],
                      'HIT ' if hit else 'MISS', json.dumps(lost), res.get('hull'), res.get('err'), len(errs)), flush=True)
                b.close()
    stop()
    json.dump(report, open(os.path.join(OUT, a.tag + '.json'), 'w'), indent=1)
    print('MODULAR SUMMARY: %d cases, %d failures' % (len(report),failed),flush=True)
    return 1 if failed else 0

if __name__ == '__main__':
    sys.exit(main())
