#!/usr/bin/env python3
"""
probe_warhive_0918.py - THE WARHIVE CARRIER and THE NIGHTWING ACE, stage 6's boss, IN REAL CHROMIUM.

    python _BUILD_SOURCE/probe_warhive_0918.py [--diff normal|hard] [--out DIR]

Drives the real game through shoot.py's server, TRAP_RAF and STEP, and the real spawn path
(BOSSMODE.start(6,'boss') raises the warning; updatePlay spawns STAGES' stage-6 boss):
  * stage 6's boss IS the Warhive; it spawns with NO hp bar and does NOT start the boss track
  * it descends, opens the bay, launches 6 (Normal) / 8 (Hard) hivewing escorts, climbs away, and
    comes back only once the escorts are gone
  * a REAL player round on a thruster lowers that thruster's pool; a round on bare hull does nothing
  * Hard: the thruster cannons fire energy balls and the one-third-screen beam
  * both thrusters down -> the carrier falls, the ace emerges, the hp bar appears, the boss track starts
  * the ace rolls out of a round aimed at it, somersaults out of a missile, and locks a Retina on the player
  * the kill runs the spin-out death; zero page / console errors
The pilot is kept alive by STUBBING playerHit (never by pinning invuln - 0912v).
Writes <out>/NN_*.png and _contact.png. LOOK AT THEM.
"""
import os, sys, io, base64, argparse, importlib.util, traceback
HERE = os.path.dirname(os.path.abspath(__file__))

STATE = r"""() => { const b = boss; if(!b) return {none:true};
  const W = b._whv; if(!W) return {kind:b.kind};
  const alive = W.jets.filter(e=>e&&!e.dead&&e._dyingT==null&&enemies.indexOf(e)>=0).length;
  const A = W.ace;
  return {kind:b.kind, mode:W.mode, st:W.st, cy:Math.round(W.cy), cycle:W.cycle, launched:W.launched, jets:alive,
    L:W.parts.L.hp, R:W.parts.R.hp, door:W.parts.door.hp, Lmax:W.parts.L.max, doorMax:W.parts.door.max,
    bar: bossHealthVisible(b), hp:b.hp, maxhp:b.maxhp, dead:!!b.dead, shots:W.shots.length, beam:!!W.beam,
    ace: A ? {st:A.st, x:Math.round(A.x), y:Math.round(A.y), roll:!!A.roll, somer:!!A.somer, dash:!!A.dash, orb:!!A.orb,
      inv:!!A.inverted, desp:A.desp?A.desp.st:null} : null,
    locks: (typeof playerLocks!=='undefined') ? playerLocks.length : 0,
    music: (window.__mus||[]).join(',')};
}"""
CAP = "() => { const c = document.getElementById('screen'); return c ? c.toDataURL('image/png') : null; }"

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--diff', default='normal')
    ap.add_argument('--out', default=None)
    a = ap.parse_args()
    repo = os.path.dirname(HERE)
    spec = importlib.util.spec_from_file_location('shoot', os.path.join(HERE, 'shoot.py'))
    sh = importlib.util.module_from_spec(spec); spec.loader.exec_module(sh)
    from playwright.sync_api import sync_playwright
    from PIL import Image
    out = a.out or os.path.join(repo, 'docs', 'proofs', 'warhive_0918', a.diff)
    os.makedirs(out, exist_ok=True)
    fails, n_ok, errs, caps = [], [0], [], []
    def ok(c, m):
        if c: n_ok[0] += 1; print('  ok  ', m, flush=True)
        else: fails.append(m); print('  FAIL', m, flush=True)
    port, stop = sh.serve(repo)
    with sync_playwright() as p:
        br = p.chromium.launch(args=['--disable-gpu', '--no-sandbox', '--mute-audio'])
        pg = br.new_page(viewport={'width': 1100, 'height': 1200})
        pg.on('pageerror', lambda e: errs.append('pageerror: ' + str(e)[:240]))
        pg.on('console', lambda m: errs.append('console.error: ' + m.text[:240]) if m.type == 'error' else None)
        def step(k, wait=16):
            e = pg.evaluate(sh.STEP, k)
            if e: errs.append('STEP threw: ' + str(e)[:200])
            if wait: pg.wait_for_timeout(wait)
        st = lambda: pg.evaluate(STATE)
        def until(cond, frames, per=3):
            s = st()
            for _ in range(0, frames, per):
                if cond(s): return s
                step(per); s = st()
            return s
        def shot(name, label):
            d = pg.evaluate(CAP)
            if not d: return
            im = Image.open(io.BytesIO(base64.b64decode(d.split(',', 1)[1]))).convert('RGB')
            im.save(os.path.join(out, name)); caps.append((label, im))

        pg.goto('http://127.0.0.1:%d/index.html' % port, wait_until='load', timeout=120000)
        pg.wait_for_function("() => typeof state!=='undefined' && (window.__bofFrames|0) > 4", timeout=120000)
        pg.evaluate(sh.TRAP_RAF); pg.wait_for_timeout(60)
        pg.evaluate("() => { ASSETS.ready = true; }")
        ok(pg.evaluate("() => STAGES.find(s=>s.n===6).boss") == 'warhive', "stage 6's boss is the WARHIVE")
        pg.evaluate("() => { window.__mus=[]; const o=Audio.startMusic; Audio.startMusic=function(n){ window.__mus.push(n); return o.apply(this, arguments); }; }")
        started = pg.evaluate("() => !!BOSSMODE.start(6, 'boss', 'cole', false)")
        pg.evaluate("() => { window.__mus=[]; }")
        pg.evaluate("(d) => { diffKey=d; DIFF=DIFFS[d]; window.__hits=0; playerHit=function(){ window.__hits++; }; }", a.diff)
        # warm the plates: rdy() is false on its first call
        pg.evaluate("() => { for(const k of ['whv_closed','whv_open','whv_broken','whv_fan','whv_twreck','whv_ace','whv_ace_belly','whv_ace_dmg','xelite_hivewing_idle']) XART.rdy(k); for(let i=0;i<8;i++){XART.rdy('whv_ace_br'+i);XART.rdy('whv_ace_so'+i);XART.rdy('florb_'+i);} }")
        pg.wait_for_timeout(1500)
        s = until(lambda s: not s.get('none'), 900, 6)
        ok(started and s.get('kind') == 'warhive', 'the warning spawned the Warhive (%s)' % s.get('kind'))
        if s.get('none'):
            br.close(); stop(); print('%d ok / %d fail' % (n_ok[0], len(fails))); return 1
        ok(s['bar'] is False, 'no hp bar while the carrier fights')
        ok('boss6' not in (s.get('music') or ''), 'the carrier does not start the boss track (%s)' % s.get('music'))
        s = until(lambda s: s['st'] == 'launch', 400)
        step(12); shot('01_bay_open.png', 'bay open, escorts launching')
        s = until(lambda s: s['st'] in ('hold', 'retreat'), 600)
        exp = 8 if a.diff in ('hard', 'furious') else 6
        ok(s['launched'] == exp, '%d escorts launched (want %d)' % (s['launched'], exp))
        # a REAL player round: fire from under the left thruster and let the bullet loop collide it
        def fire_at(part, dmg=12):
            return pg.evaluate("""([id,d]) => { const W=boss._whv, q=whvPartPos(boss,id);
                pBullets.push({x:q.x, y:q.y, vx:0, vy:0, w:4, h:8, dmg:d, t:0}); return q; }""", [part, dmg])
        L0 = s['L']; fire_at('L'); step(8)
        s = st(); ok(s['L'] < L0, 'a real round on the LEFT thruster took its pool (%d -> %d)' % (L0, s['L']))
        hull0 = (s['L'], s['R'], s['door'])
        pg.evaluate("() => { const W=boss._whv; pBullets.push({x:W.cx+80, y:W.cy+95, vx:0, vy:0, w:4, h:8, dmg:12, t:0}); }")
        step(8); s = st()
        ok((s['L'], s['R'], s['door']) == hull0, 'a round on bare hull armour does nothing')
        if a.diff in ('hard', 'furious'):
            seen = {'shots': 0, 'beam': False}
            for _ in range(160):
                step(3); s = st(); seen['shots'] = max(seen['shots'], s['shots']); seen['beam'] = seen['beam'] or s['beam']
                if s['beam'] and not caps[-1][0].startswith('beam'): shot('02_beam.png', 'beam')
                if s['st'] in ('retreat', 'away'): break
            ok(seen['shots'] > 0, 'Hard: the thrusters fired energy balls (peak %d on screen)' % seen['shots'])
            ok(seen['beam'], 'Hard: a thruster charged and fired the one-third-screen beam')
        s = until(lambda s: s['st'] == 'away', 600)
        ok(s['st'] == 'away' and s['cy'] < -100, 'the carrier climbed away off screen (cy %d)' % s['cy'])
        esc = pg.evaluate("() => boss._whv.jets.map(e => ({sh: !!e._esh, hp: e.hp}))")
        ok(esc and not any(x['sh'] for x in esc), 'Mike 0918: the escorts carry NO shield (%d jets)' % len(esc))
        pg.evaluate("() => { window.__eb=0; window.__seenB=new WeakSet(); }")
        dives = 0; maxdiv = 0; seen = set()
        for _ in range(110):
            step(3)
            d = pg.evaluate("""() => { let n=0, ids=[]; for(const e of boss._whv.jets) if(e&&!e.dead&&e._hwD){ if(e._hwD.st!=='climb') n++; ids.push(e._hwSlot+':'+e._hwD.st); }
                for(const q of eBullets) if(q&&q.kind==='dart'&&!window.__seenB.has(q)){ window.__seenB.add(q); window.__eb++; }
                return {n:n, ids:ids, eb:window.__eb}; }""")
            maxdiv = max(maxdiv, d['n'])
            for x in d['ids']:
                if x.endswith(':run'): seen.add(x.split(':')[0])
            if d['n'] and not any(c[0] == 'dive' for c in caps): shot('03b_dive.png', 'dive')
        s = st()
        ok(len(seen) >= 2, 'the squadron takes strafing dives (%d different jets dived)' % len(seen))
        ok(maxdiv <= 1, 'one dive at a time (peak %d)' % maxdiv)
        ok(d['eb'] >= 12, 'the escorts fire aimed bursts (%d rounds)' % d['eb'])
        ok(s['st'] == 'away', 'it waits while escorts live (%d alive)' % s['jets'])
        shot('03_escorts.png', 'escorts on their own')
        pg.evaluate("() => { for(const e of boss._whv.jets.slice()) if(!e.dead) killEnemy(e); }")
        s = until(lambda s: s['cycle'] >= 1 and s['st'] in ('open', 'launch'), 600)
        ok(s['cycle'] >= 1, 'with the escorts gone it came back (cycle %d, %s)' % (s['cycle'], s['st']))
        # smoke escalation: bring both thrusters low, look, then finish them
        pg.evaluate("() => { const W=boss._whv; W.parts.L.hp=W.parts.L.max*.2; W.parts.R.hp=W.parts.R.max*.45; W.parts.door.hp=W.parts.door.max*.6; }")
        step(30); shot('04_damaged.png', 'thrusters burning (20% / 45%)')
        for part in ('door', 'L', 'R'):
            for _ in range(80):
                s = st()
                if s['mode'] != 'carrier' or s[part] <= 0: break
                fire_at(part, 70); step(4)
        s = st(); ok(s['mode'] in ('death', 'ace'), 'both thrusters down -> the carrier goes down (%s)' % s['mode'])
        step(40); shot('05_falling.png', 'carrier falling')
        s = until(lambda s: s['mode'] == 'ace', 600)
        ok(s['mode'] == 'ace' and s['ace'], 'the NIGHTWING ACE emerged and became the boss')
        ok(s['bar'] is True, 'the hp bar appears with the ace')
        ok('boss6' in (s.get('music') or ''), 'the boss track starts with the ace (%s)' % s.get('music'))
        step(60); shot('06_ace.png', 'the ace')
        rolled = somer = False; locks = 0
        for i in range(260):
            if i % 5 == 0:
                pg.evaluate("() => { const A=boss._whv.ace; pBullets.push({x:A.x, y:A.y+100, vx:0, vy:-14, w:6, h:14, dmg:4, t:0}); }")
            if i == 90:
                pg.evaluate("() => { const A=boss._whv.ace; pBullets.push({x:A.x, y:A.y+120, vx:0, vy:-7, w:10, h:18, dmg:24, kind:'gmiss', t:0}); }")
            step(2); s = st()
            rolled = rolled or s['ace']['roll']; somer = somer or s['ace']['somer']; locks = max(locks, s['locks'])
            if s['ace']['roll'] and not any(c[0] == 'roll' for c in caps): shot('07_roll.png', 'roll')
        ok(rolled, 'the ace barrel-rolled out of a round climbing into it')
        ok(somer, 'the ace somersaulted out of an incoming missile')
        ok(locks > 0, 'the ace put a Retina lock on the player (%d)' % locks)
        if a.diff in ('hard', 'furious'):
            pg.evaluate("() => { boss.hp = boss.maxhp*0.45; }")
            s = until(lambda s: s['ace']['orb'], 120, 3); ok(s['ace']['orb'], 'Hard: the helper orb joined at 50%')
            step(20); shot('08_orb.png', 'helper orb')
            pg.evaluate("() => { boss.hp = boss.maxhp*0.2; }")
            seen = set()
            for _ in range(400):
                step(3); s = st(); seen.add(s['ace']['desp'])
                if s['ace']['desp'] == 'cross' and not any(c[0] == 'cross' for c in caps): shot('09_cross.png', 'cross')
                if s['ace']['desp'] == 'done': break
            ok({'warn', 'south', 'cross', 're'} <= seen, 'Hard 25%%: warn -> south dash -> criss-cross -> re-entry (%s)' % sorted(x for x in seen if x))
            step(40); s = st(); ok(s['ace']['inv'], 'then it holds INVERTED and shadows the player')
            shot('10_inverted.png', 'inverted')
        pg.evaluate("() => { boss.hp = 1; }")
        for _ in range(200):
            pg.evaluate("() => { const A=boss._whv.ace; if(A&&!boss.dead) pBullets.push({x:A.x, y:A.y+60, vx:0, vy:-14, w:6, h:14, dmg:40, t:0}); }")
            step(3); s = st()
            if s['dead']: break
        ok(s['dead'], 'a real round killed the ace')
        step(60); shot('11_spinout.png', 'spin-out')
        pg.wait_for_timeout(300)
        ok(not errs, 'zero page / console errors (%d)' % len(errs))
        for e in errs[:8]: print('   ', e)
        br.close()
    stop()
    if caps:
        W = 360; H = int(caps[0][1].height * W / caps[0][1].width)
        sheet = Image.new('RGB', (W * min(4, len(caps)), H * ((len(caps) + 3) // 4)), (0, 0, 0))
        for i, (lab, im) in enumerate(caps):
            sheet.paste(im.resize((W, H)), ((i % 4) * W, (i // 4) * H))
        sheet.save(os.path.join(out, '_contact.png'))
    print('\n%d ok / %d fail' % (n_ok[0], len(fails)))
    return 1 if fails else 0

if __name__ == '__main__':
    sys.exit(main())
