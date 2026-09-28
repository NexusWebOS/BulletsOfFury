#!/usr/bin/env python3
"""
probe_sustained_0928.py - PASSOVER_OPUS_0928 Priority 0 #1: sustained, naturally-paced play.

Most probes jump straight to an encounter state, which leaves wave -> miniboss -> boss scheduling,
long-session pacing and the stage-to-stage screens unexercised. This one does not jump:

  * the front end is driven with REAL keys to MODE SELECT -> CAMPAIGN -> difficulty -> pilot -> PLAY;
  * after that the real loop() is stepped (TRAP_RAF + a synthetic 60Hz clock, in chunks with a real
    pause between them so lazily-loaded art can decode), and an AUTOPILOT plays: it holds FIRE, reads
    every enemy round and steers to the cheapest of nine moves over a short look-ahead, collects
    pickups, lines up under its target and holds the Retina (C) during boss fights;
  * every non-PLAY screen (debrief, powers, forge, loadout, map, cutscene, intro, launch, continue) is
    advanced by tapping ENTER, exactly as a player mashing START would;
  * NOTHING is fast-forwarded. No stageTimer edits, no hp edits, no forced kills.

--immune stubs playerHit (counting would-be hits) so the run measures PACING, not the bot's skill.
Without it deaths and continues are real.

Per stage it records: frames to miniboss / miniboss down / boss / boss down, kills, pickups, hits,
deaths, peak enemies/rounds, frame cost, stalls (no scroll progress and no encounter for 20 s), every
page error and every swallowed 'draw error'. Screenshots every N simulated seconds.

  python3 _BUILD_SOURCE/probe_sustained_0928.py --diff furious --pilot cole --immune --stages 1-9
"""
import os, sys, json, base64, time, argparse
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.join(ROOT, '_BUILD_SOURCE'))
import http.server
http.server.SimpleHTTPRequestHandler.log_message = lambda *a: None
import shoot as sh
from playwright.sync_api import sync_playwright

AP = r"""
() => {
  const Q = window.__ap = window.__ap || {};
  Q.cfg = Q.cfg || {immune:false};
  Q.f = 0; Q.log = []; Q.errs = Q.errs || [];
  Q.cur = null; Q.stages = Q.stages || [];
  const K = Input.keys;
  const setK = (k, on) => { if (on && !K[k]) Input.injectTap(k); K[k] = !!on; };
  const MOVE = ['a','d','w','s'];
  const release = () => { for (const k of MOVE.concat(['j','c','enter','k'])) K[k] = false; };
  Q.release = release;
  // count would-be hits in immune mode, real ones otherwise
  if (!Q.hitWrapped) {
    Q.hitWrapped = true;
    const real = window.playerHit;
    window.playerHit = function(src) {
      if (Q.cur) { Q.cur.hitCalls++; if (Q.f - (Q.lastHit || -999) > 90) { Q.cur.hits++; Q.lastHit = Q.f; } }
      if (Q.cfg.immune) return;
      return real.apply(this, arguments);
    };
    const origPU = window.applyPowerup;
    if (typeof origPU === 'function') window.applyPowerup = function(p) {
      if (Q.cur) { Q.cur.pickups++; const t = (p && (p.type||p.kind)) || '?'; Q.cur.pickTypes[t] = (Q.cur.pickTypes[t]|0) + 1; }
      return origPU.apply(this, arguments);
    };
    const origKill = window.killEnemy;
    window.killEnemy = function(e) { if (Q.cur && e && !e._apKilled) { e._apKilled = 1; Q.cur.kills++; } return origKill.apply(this, arguments); };
    // Canvas stack balance (Priority 0 #7): count save/restore on the game's own context instance
    Q.depth = 0; Q.depth0 = null;
    const cs = ctx.save, cr = ctx.restore;
    ctx.save = function() { Q.depth++; return cs.apply(this, arguments); };
    ctx.restore = function() { Q.depth--; return cr.apply(this, arguments); };
    const ce = console.error.bind(console), cl = console.log.bind(console), cw = console.warn.bind(console);
    const grab = (a) => { const s = Array.prototype.map.call(a, x => String(x && x.stack || x)).join(' ');
      if (/draw error|update error|TypeError|ReferenceError|RangeError/.test(s)) { Q.errs.push({f: Q.f, st: state, stage: run && run.stage, s: s.slice(0, 300)}); if (Q.cur) Q.cur.errs++; } };
    console.error = function() { grab(arguments); return ce.apply(null, arguments); };
    console.warn = function() { grab(arguments); return cw.apply(null, arguments); };
    console.log = function() { grab(arguments); return cl.apply(null, arguments); };
  }
  const newStage = (n) => ({stage: n, pilot: run.pilot, diff: diffKey, f0: Q.f, playFrames: 0, mini: null, miniDown: null,
    boss: null, bossDown: null, hitCalls: 0, kills: 0, pickups: 0, pickTypes: {}, hits: 0, deaths: 0, errs: 0, peakEnemies: 0,
    peakRounds: 0, stall: 0, maxStall: 0, frameMs: 0, frameN: 0, worstMs: 0, lives: [], states: [], lastScroll: null,
    ended: null, weapon: null});
  Q.newStage = newStage;

  // ---- the autopilot, called once per stepped frame from window.__qaTick
  window.__qaTick = function() {
    Q.f++;
    const st = state;
    // every screen change is logged with the reward state, so a natural boss kill shows what it granted
    if (st !== Q.lastSt) {
      Q.trans = Q.trans || [];
      let owned = null; try { owned = forgeCombosOwned().map(o => o.elem + (o.w ? ':' + o.w : '')); } catch (_o) {}
      if (Q.trans.length < 600) Q.trans.push({f: Q.f, from: Q.lastSt || null, to: st, stage: run && run.stage, combos: run && run.forgeCombos,
        respecs: run && run.forgeRespecs, owned, weapon: run && run.weapon, wlevel: run && run.wlevel, lives: run && run.lives, cont: run && run.continues});
      Q.lastSt = st;
    }
    if (Q.depth0 == null) Q.depth0 = Q.depth;
    if (Q.depth !== Q.depth0) { if (Q.cur) { Q.cur.stackLeaks = (Q.cur.stackLeaks|0) + 1; if (!Q.cur.leakAt) Q.cur.leakAt = {f: Q.cur.playFrames, st, d: Q.depth - Q.depth0}; } Q.depth0 = Q.depth; }
    if (Q.cur && (!Q.cur.states.length || Q.cur.states[Q.cur.states.length-1] !== st)) Q.cur.states.push(st);
    if (st !== 'play') {
      release();
      // mash START on every screen that is not gameplay, a tap every 24 frames
      if (st !== 'paused' && Q.f % 24 === 0) { Input.injectTap('enter'); K.enter = true; }
      else K.enter = false;
      if (st === 'paused' && Q.f % 24 === 0) { Input.injectTap('enter'); }
      return;
    }
    // stage bookkeeping
    if (!Q.cur || Q.cur.stage !== run.stage) {
      if (Q.cur) { Q.cur.ended = Q.cur.ended || 'left'; }
      Q.cur = newStage(run.stage); Q.stages.push(Q.cur);
    }
    const C = Q.cur; C.playFrames++;
    if (subBossActive && subBoss && C.mini == null) C.mini = C.playFrames;
    if (C.mini != null && C.miniDown == null && (!subBossActive || !subBoss)) C.miniDown = C.playFrames;
    if (bossActive && boss && C.boss == null) C.boss = C.playFrames;
    if (C.boss != null && C.bossDown == null && boss && boss.dead) C.bossDown = C.playFrames;
    if (player.dead && !C._wasDead) C.deaths++;
    C._wasDead = !!player.dead;
    C.peakEnemies = Math.max(C.peakEnemies, enemies.length);
    C.peakRounds = Math.max(C.peakRounds, eBullets.length);
    // stall: neither the scroll nor the stage clock moves and no encounter is up
    const prog = Math.round((typeof mapScroll === 'number' ? mapScroll : 0) + (typeof stageTimer === 'number' ? stageTimer * 100 : 0));
    if (!bossActive && !subBossActive && C.lastScroll === prog && enemies.length === 0) { C.stall++; C.maxStall = Math.max(C.maxStall, C.stall); }
    else C.stall = 0;
    C.lastScroll = prog;
    if (!C.weapon) try { C.weapon = JSON.stringify({w: run.weapon, lv: run.wlv || run.levels || null}); } catch (_) {}

    // ---- choose a move
    const P = player, sp = (typeof playerBaseSpeed === 'function' ? playerBaseSpeed() : 3) * 1.35;
    const H = 26;             // look-ahead frames
    const rounds = [];
    for (const b of eBullets) { if (!b || b.dead) continue; const vx = +b.vx || 0, vy = +b.vy || 0;
      if (!isFinite(b.x) || !isFinite(b.y)) continue;
      const r = Math.max(4, ((b.w || b.r * 2 || 8) + (b.h || b.r * 2 || 8)) / 4);
      if (Math.abs(b.x - P.x) > 220 || Math.abs(b.y - P.y) > 260) continue;
      rounds.push([b.x, b.y, vx, vy, r]); }
    const bodies = [];
    for (const e of enemies) { if (!e || e.dead || e._dyingT != null) continue; if (Math.abs(e.x - P.x) > 200 || Math.abs(e.y - P.y) > 220) continue;
      bodies.push([e.x, e.y, (e.w || 30) / 2 + 10, (e.h || 30) / 2 + 12, +e.vx || 0, +e.vy || 0]); }
    // column hazards the bullet list does not carry: hostile zone columns and hostile geysers (0918b)
    const cols = [];
    try { for (const c of zoneCols) if (c && c.hostile && c.t < c.life) cols.push([c.x0 - 12, c.x0 + c.w + 12, -1e9, 1e9]); } catch (_z) {}
    try { for (const g of geysers) if (g && g.hostile && g.t < g.life) { const l = (typeof geyserLane === 'function' ? geyserLane(g) : 14) * 0.75 + 14; cols.push([g.x - l, g.x + l, g.y - GEYSER_H - 20, g.y + 10]); } } catch (_g) {}
    const T = (bossActive && boss && !boss.dead) ? boss : (subBossActive && subBoss && !subBoss.dead ? subBoss : null);
    // target x: nearest pickup, else the encounter, else the lowest living enemy on screen
    let tx = worldWidth() / 2, ty = VH * 0.78, pick = null;
    for (const p of powerups) { if (!p || p.dead || !isFinite(p.x)) continue; if (p.y < VH * 0.25) continue;
      const d = Math.hypot(p.x - P.x, p.y - P.y); if (!pick || d < pick.d) pick = {x: p.x, y: p.y, d}; }
    if (pick && pick.d < 320) { tx = pick.x; ty = clamp(pick.y + 10, VH * 0.45, VH * 0.9); }
    else if (T) { tx = T.x; ty = VH * 0.8; }
    else { let best = null; for (const e of enemies) { if (!e || e.dead || e._dyingT != null || !isFinite(e.x)) continue;
        if (e.y < 30 || e.y > VH * 0.72) continue; const s = e.y - Math.abs(e.x - P.x) * 0.25; if (!best || s > best.s) best = {x: e.x, s}; }
      if (best) tx = best.x; }
    let bestM = null;
    for (let dx = -1; dx <= 1; dx++) for (let dy = -1; dy <= 1; dy++) {
      const l = Math.hypot(dx, dy) || 1;
      let risk = 0;
      for (let t = 1; t <= H; t += 2) {
        const px = clamp(P.x + dx / l * sp * t, 10, worldWidth() - 10), py = clamp(P.y + dy / l * sp * t, PLAY.y + 12, PLAY.y + PLAY.h - 6);
        const w = 1 - t / (H + 4);
        for (const q of rounds) { const bx = q[0] + q[2] * t, by = q[1] + q[3] * t; const d = Math.hypot(bx - px, by - py) - q[4] - 9;
          if (d < 26) risk += w * (d < 0 ? 40 : (26 - d) * 0.9); }
        for (const e of bodies) { const ex = e[0] + e[4] * t, ey = e[1] + e[5] * t;
          if (Math.abs(ex - px) < e[2] && Math.abs(ey - py) < e[3]) risk += w * 30; }
      }
      for (let t = 2; t <= H; t += 6) { const px = clamp(P.x + dx / l * sp * t, 10, worldWidth() - 10), py = clamp(P.y + dy / l * sp * t, PLAY.y + 12, PLAY.y + PLAY.h - 6);
        for (const c of cols) if (px > c[0] && px < c[1] && py > c[2] && py < c[3]) risk += 25; }
      const fx = clamp(P.x + dx / l * sp * 10, 10, worldWidth() - 10), fy = clamp(P.y + dy / l * sp * 10, PLAY.y + 12, PLAY.y + PLAY.h - 6);
      const goal = Math.abs(fx - tx) * 0.05 + Math.abs(fy - ty) * 0.03 + (fx < 40 || fx > worldWidth() - 40 ? 1.5 : 0);
      const score = risk + goal + (dx || dy ? 0.02 : 0);
      if (!bestM || score < bestM.s) bestM = {s: score, dx, dy};
    }
    setK('a', bestM.dx < 0); setK('d', bestM.dx > 0); setK('w', bestM.dy < 0); setK('s', bestM.dy > 0);
    K.j = true;
    // hold the single Retina during an encounter so missiles have a target
    K.c = !!T && (Q.f % 240) < 200;
    // bomb when the look-ahead is grim and we are not immune
    if (!Q.cfg.immune && bestM.s > 120 && Q.f % 30 === 0) Input.injectTap('k');
    if (Q.f % 60 === 0) C.lives.push(run.lives);
  };
  return true;
}
"""

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--diff', default='furious')
    ap.add_argument('--pilot', default='maverick')
    ap.add_argument('--immune', action='store_true')
    ap.add_argument('--stages', default='1-9')
    ap.add_argument('--cap', type=float, default=480, help='simulated seconds per stage before giving up')
    ap.add_argument('--shot', type=float, default=15, help='simulated seconds between screenshots')
    ap.add_argument('--out', default=None)
    ap.add_argument('--start', type=int, default=1)
    a = ap.parse_args()
    lo, hi = [int(x) for x in a.stages.split('-')] if '-' in a.stages else (int(a.stages), int(a.stages))
    tag = '%s_%s%s' % (a.diff, a.pilot, '_immune' if a.immune else '')
    OUT = a.out or os.path.join(ROOT, '_shots', 'opus0928', 'sustained_' + tag)
    os.makedirs(OUT, exist_ok=True)
    port, stop = sh.serve(sh.GAME)
    report = {'cfg': vars(a), 'path': [], 'stages': [], 'pageErrors': [], 'stepErrors': []}
    t_start = time.time()
    with sync_playwright() as pw:
        br = pw.chromium.launch(args=['--no-sandbox', '--mute-audio', '--autoplay-policy=no-user-gesture-required'])
        pg = br.new_page(viewport={'width': 1000, 'height': 1100})
        pg.on('pageerror', lambda e: report['pageErrors'].append(str(e)[:300]))
        pg.goto('http://127.0.0.1:%d/index.html' % port, wait_until='load', timeout=120000)
        pg.wait_for_function("() => typeof setState==='function' && (window.__bofFrames|0)>4", timeout=120000)
        pg.evaluate("() => { try{ localStorage.clear(); }catch(_){} try{ achievementReload(); }catch(_){} }")
        st = lambda: pg.evaluate("() => state")
        def shot(name):
            d = pg.evaluate("() => { const c=document.getElementById('screen'); return c?c.toDataURL('image/png'):null; }")
            if d: open(os.path.join(OUT, name + '.png'), 'wb').write(base64.b64decode(d.split(',', 1)[1]))
        # ---- front end with real keys (same route as probe_campaign_0917d)
        for _ in range(40):
            if st() == 'modesel': break
            pg.keyboard.press('Enter'); pg.wait_for_timeout(700)
        pg.wait_for_timeout(500)
        for _ in range(8):
            if pg.evaluate("() => { const L=modeList(); const m=L[modeIndex]; return String((m&&(m.key||m.id||m.name))||m).toLowerCase().indexOf('camp')>=0; }"): break
            pg.keyboard.press('ArrowDown'); pg.wait_for_timeout(300)
        pg.keyboard.press('Enter'); pg.wait_for_timeout(900)
        for _ in range(12):
            s = st(); print('  front', s, flush=True)
            if s == 'diff':
                # walk the difficulty cursor with real arrow keys to the requested row
                for _ in range(8):
                    cur = pg.evaluate("() => { const L=diffList(); return L[menuIndex]; }")
                    if cur == a.diff: break
                    pg.keyboard.press('ArrowDown'); pg.wait_for_timeout(250)
                pg.keyboard.press('Enter'); pg.wait_for_timeout(900); continue
            if s == 'pilot':
                for _ in range(12):
                    cur = pg.evaluate("() => { try{ return PILOTS[pilotIndex].key; }catch(_){ return null; } }")
                    print('   pilot cursor', cur, pg.evaluate("() => ({armed:pilotInputArmed, rot:pilotRot, stateT, st:state})"), flush=True)
                    if cur == a.pilot: break
                    pg.keyboard.press('ArrowRight'); pg.wait_for_timeout(500)
                pg.wait_for_timeout(1500)
                pg.keyboard.press('Enter'); pg.wait_for_timeout(1500); break
            pg.keyboard.press('Enter'); pg.wait_for_timeout(900)
        report['frontEnd'] = pg.evaluate("() => ({state, mode:run.mode, diff:diffKey, pilot:run.pilot, stage:run.stage})")
        print('front end ->', report['frontEnd'], flush=True)
        # ---- from here the real loop is stepped with the autopilot
        pg.evaluate(sh.TRAP_RAF)
        pg.evaluate(AP)
        pg.evaluate("(c) => { window.__ap.cfg = c; }", {'immune': a.immune})
        if a.start > 1:
            pg.evaluate("(n) => { PENDING_STAGE=n; run.stage=n; curStage=STAGES[n-1]; beginStage(n); }", a.start)
        CH = 120
        sim = 0.0; next_shot = 0.0; last_stage = None; stage_sim = 0.0; same_state = 0.0; prev_state = None
        STEP = sh.STEP
        while True:
            err = pg.evaluate(STEP, CH)
            if err: report['stepErrors'].append(err); print('STEP ERR', err, flush=True)
            sim += CH / 60.0
            pg.wait_for_timeout(25)
            info = pg.evaluate("() => ({state, stage:run.stage, lives:run.lives, cont:run.continues, boss:!!(bossActive&&boss), mini:!!(subBossActive&&subBoss), en:enemies.length, t:(typeof stageTimer==='number'?stageTimer:0), len:(curStage&&curStage.length)||0})")
            if info['stage'] != last_stage:
                if last_stage is not None: print('  stage %s -> %s at sim %.0fs' % (last_stage, info['stage'], sim), flush=True)
                last_stage = info['stage']; stage_sim = 0.0
            same_state = same_state + CH / 60.0 if info['state'] == prev_state else 0.0; prev_state = info['state']
            # the cap counts PLAY time only: a stage already cleared and sitting in its debrief or cutscene
            # must never be force-advanced mid-transition (that corrupts the flow being measured)
            if info['state'] == 'play': stage_sim += CH / 60.0
            if info['state'] != 'play' and same_state > 90:
                print('STUCK on screen', info['state'], 'for 90 s', flush=True); shot('STUCK_%s' % info['state']); report['stuck'] = info; break
            if not report['path'] or report['path'][-1] != info['state']:
                report['path'].append(info['state'])
            if sim >= next_shot:
                shot('s%d_%05d_%s' % (info['stage'], int(sim), info['state'])); next_shot = sim + a.shot
            if int(sim) % 30 < 2:
                print('  sim %4.0fs st=%-10s stage=%s t=%.0f/%s en=%d boss=%s mini=%s lives=%s real=%.0fs' % (sim, info['state'], info['stage'], info['t'], info['len'], info['en'], info['boss'], info['mini'], info['lives'], time.time()-t_start), flush=True)
            if info['state'] in ('gameover',) :
                print('GAME OVER at stage', info['stage'], flush=True); break
            if info['state'] in ('victory', 'credits', 'title'): print('run ended in', info['state'], flush=True); break
            if info['stage'] > hi and info['state'] == 'play': break
            if stage_sim > a.cap and info['state'] == 'play':
                print('  CAP: stage %s exceeded %ds' % (info['stage'], a.cap), flush=True)
                pg.evaluate("() => { if(window.__ap.cur) window.__ap.cur.ended='cap'; }")
                if info['stage'] >= hi: break
                n = info['stage'] + 1
                pg.evaluate("(n) => { PENDING_STAGE=n; run.stage=n; curStage=STAGES[n-1]; beginStage(n); }", n)
                stage_sim = 0.0
        report['stages'] = pg.evaluate("() => window.__ap.stages.map(s => { const o=Object.assign({}, s); delete o._wasDead; delete o.lastScroll; o.lives=o.lives.filter((v,i,a)=>i===0||v!==a[i-1]); return o; })")
        report['errors'] = pg.evaluate("() => window.__ap.errs.slice(0, 80)")
        report['transitions'] = pg.evaluate("() => (window.__ap.trans || [])")
        report['simSeconds'] = sim; report['realSeconds'] = time.time() - t_start
        br.close()
    stop()
    json.dump(report, open(os.path.join(OUT, 'report.json'), 'w'), indent=1)
    print(json.dumps({k: report[k] for k in ('path', 'pageErrors', 'stepErrors')}, indent=0)[:3000])
    for s in report['stages']:
        fs = lambda v: ('%.0fs' % (v / 60.0)) if v is not None else '-'
        print('stage %d: play %s mini %s->%s boss %s->%s kills %d picks %d hits %d deaths %d errs %d leaks %s peakE %d peakR %d maxStall %s ended %s' % (
            s['stage'], fs(s['playFrames']), fs(s['mini']), fs(s['miniDown']), fs(s['boss']), fs(s['bossDown']), s['kills'], s['pickups'],
            s['hits'], s['deaths'], s['errs'], s.get('stackLeaks', 0), s['peakEnemies'], s['peakRounds'], fs(s['maxStall']), s['ended']))
    print('errors (first):', report['errors'][:6])

if __name__ == '__main__':
    main()
