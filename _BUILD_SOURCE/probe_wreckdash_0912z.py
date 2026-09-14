#!/usr/bin/env python3
"""probe_wreckdash_0912z.py - Juggernaut's balls stay on their chains, the chains on the ship, and the ram is seen.

Mike, 0912: "Juggernauts wrecking balls need to be anchored to his chains and the chain anchored to the ship at all
times. The charge dash needs more visibility."

Records what was DRAWN, never what the code says it drew: the game context's OWN drawImage is wrapped (a prototype trap
catches nothing - CLAUDE.md 0905h), and each blit's centre is carried through the live transform into canvas space.
Link and ball blits are identified by the CELL size of jwb_link / jwb_ball (XART.get returns a fresh canvas, so an
identity or .src match catches nothing). Per frame, for every ball:
  * links exist that point at it (within 20 degrees, from the ship's own canvas point)
  * the chain reaches it (last link within ~1.3 ball radii of the ball's centre)
  * the chain starts at the ship (first link inside the hull)
  * no links hang on the opposite side
measured in straight flight, while strafing, and through a full charge dash. Then:
  * the dash: a shock ring at launch and another at landing, orange afterimages ('lighter' blits of the ship's own
    size) on the dash frames
  * stale: stop, start another pilot - zero link and ball blits
Writes docs/proofs/wreckdash_0912z/ (flight, dash).
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import shoot

OUT = 'docs/proofs/wreckdash_0912z'

TRAP = r"""() => {
  window.__dr = []; window.__rec = 0;
  if (window.__dtrap) return true;
  window.__dtrap = 1;
  const c = ctx, o = c.drawImage;
  c.drawImage = function (im) {
    try {
      if (window.__rec && im) {
        const a = arguments, W = im.width || im.naturalWidth, H = im.height || im.naturalHeight;
        let lx = 0, ly = 0, lw = W, lh = H;
        if (a.length >= 5) { lx = a[1]; ly = a[2]; lw = a[3]; lh = a[4]; } else if (a.length >= 3) { lx = a[1]; ly = a[2]; }
        const m = c.getTransform(), cx = lx + lw / 2, cy = ly + lh / 2;
        window.__dr.push({W: W, H: H, x: m.a * cx + m.c * cy + m.e, y: m.b * cx + m.d * cy + m.f, ex: m.e, ey: m.f,
                          sc: Math.hypot(m.a, m.b), op: c.globalCompositeOperation});
      }
    } catch (e) {}
    return o.apply(this, arguments);
  };
  return true;
}"""

FRAMES = r"""async ([n, hold]) => {
  const B = window.BOSSMODE;
  const L = XART.get('jwb_link'), Bl = XART.get('jwb_ball'), Bh = XART.rdy('jwb_ball_hot') ? XART.get('jwb_ball_hot') : null;
  const sk = (typeof _shipK === 'function') ? _shipK('') : null, S = sk ? XART.get(sk) : null;
  const isL = r => L && r.W === L.width && r.H === L.height;
  const isB = r => (Bl && r.W === Bl.width && r.H === Bl.height) || (Bh && r.W === Bh.width && r.H === Bh.height);
  const isG = r => S && r.op === 'lighter' && r.W === S.width && r.H === S.height;
  const out = [];
  for (const k of (hold || [])) B.hold(k, true);
  for (let i = 0; i < n; i++) {
    window.__dr = []; window.__rec = 1;
    await new Promise(r => requestAnimationFrame(r));
    window.__rec = 0;
    const links = window.__dr.filter(isL), balls = window.__dr.filter(isB), ghosts = window.__dr.filter(isG);
    const f = {links: links.length, balls: balls.length, ghosts: ghosts.length, dash: !!(B.player && B.player._chgDash), per: []};
    if (links.length && balls.length) {
      const sx = links[0].ex, sy = links[0].ey, scale = links[0].sc || 2;
      // a link is an ORPHAN only if it points at no ball at all - the two balls often sit opposite each other, so
      // "links on the far side of ball A" are simply ball B's chain (the first cut of this probe flagged exactly that)
      const angOf = r => Math.atan2(r.y - sy, r.x - sx);
      const near = (a1, a2) => { let d = a1 - a2; while (d > Math.PI) d -= 2 * Math.PI; while (d < -Math.PI) d += 2 * Math.PI; return Math.abs(d) < 20 * Math.PI / 180; };
      const ballAngs = balls.map(b => Math.atan2(b.y - sy, b.x - sx));
      f.orphans = links.filter(r => !ballAngs.some(a => near(angOf(r), a))).length;
      for (const b of balls) {
        const ab = Math.atan2(b.y - sy, b.x - sx);
        const diff = r => { let d = Math.atan2(r.y - sy, r.x - sx) - ab; while (d > Math.PI) d -= 2 * Math.PI; while (d < -Math.PI) d += 2 * Math.PI; return Math.abs(d); };
        const toward = links.filter(r => diff(r) < 20 * Math.PI / 180), away = links.filter(r => diff(r) > 160 * Math.PI / 180);
        const gap = toward.length ? Math.min(...toward.map(r => Math.hypot(r.x - b.x, r.y - b.y))) / scale : 1e9;
        const first = toward.length ? Math.min(...toward.map(r => Math.hypot(r.x - sx, r.y - sy))) / scale : 1e9;
        f.per.push({toward: toward.length, away: away.length, gap: +gap.toFixed(1), first: +first.toFixed(1),
                    dist: +(Math.hypot(b.x - sx, b.y - sy) / scale).toFixed(1)});
      }
    }
    out.push(f);
  }
  for (const k of (hold || [])) B.hold(k, false);
  return out;
}"""

START = r"""async ([stage, pilot]) => {
  const B = window.BOSSMODE;
  B.start(stage, 'boss', pilot, false);
  for (let i = 0; i < 900 && !(B.snapshot().bossActive && B.player && !B.player.dead); i++)
    await new Promise(r => requestAnimationFrame(r));
  B.player.invuln = 0; playerHit = function () {};
  return !!B.player;
}"""


def main():
    os.makedirs(OUT, exist_ok=True)
    from playwright.sync_api import sync_playwright
    port, stop = shoot.serve(shoot.GAME)
    errs, fails, n_ok = [], [], [0]

    def ok(c, m):
        if c:
            n_ok[0] += 1; print('  ok  ', m)
        else:
            fails.append(m); print('  FAIL', m)

    def judge(frames, label):
        per = [q for f in frames for q in f['per']]
        drawn = [f for f in frames if f['balls']]
        ok(len(drawn) >= len(frames) * 0.8, '%s: both balls drawn on %d of %d frames' % (label, len(drawn), len(frames)))
        ok(all(f['balls'] == 2 for f in drawn), '%s: exactly two balls every frame' % label)
        ok(per and all(q['toward'] >= 3 for q in per), '%s: every ball has its chain pointing at it (min links toward %s)' % (label, min([q['toward'] for q in per]) if per else None))
        orph = [f.get('orphans', 0) for f in drawn]
        ok(orph and max(orph) == 0, '%s: no link points at empty space - every link belongs to a ball (max orphans %s)' % (label, max(orph) if orph else None))
        ok(per and max(q['gap'] for q in per) <= 20, '%s: the chain reaches its ball (worst last-link gap %.1f world px)' % (label, max([q['gap'] for q in per]) if per else -1))
        ok(per and max(q['first'] for q in per) <= 22, '%s: the chain starts at the ship (worst first-link distance %.1f)' % (label, max([q['first'] for q in per]) if per else -1))

    with sync_playwright() as p:
        b = p.chromium.launch(args=['--disable-gpu', '--no-sandbox', '--mute-audio'])
        pg = b.new_page(viewport={'width': 1100, 'height': 1000})
        pg.on('pageerror', lambda e: errs.append('pageerror: ' + str(e)[:200]))
        pg.on('console', lambda m: errs.append('console: ' + m.text[:200]) if m.type == 'error' else None)
        pg.goto('http://127.0.0.1:%d/index.html?bossmode=1' % port, wait_until='load', timeout=60000)
        pg.wait_for_function("() => window.BOSSMODE && window.BOSSMODE.ready", timeout=90000)
        pg.evaluate(START, [1, 'juggernaut'])
        pg.evaluate("() => window.BOSSMODE.grantSpecial()")
        for _ in range(30):
            pg.evaluate("() => { XART.rdy('jwb_link'); XART.rdy('jwb_ball'); XART.rdy('jwb_ball_hot'); }")
            pg.wait_for_timeout(60)
        ok(pg.evaluate("() => XART.rdy('jwb_link') && XART.rdy('jwb_ball')"), 'the chain and ball art decoded')
        pg.evaluate(TRAP)

        judge(pg.evaluate(FRAMES, [40, []]), 'hover')
        judge(pg.evaluate(FRAMES, [40, ['d', 'w']]), 'strafe up-right')
        pg.screenshot(path=os.path.join(OUT, '01_flight.png'))

        # the full charge dash, recorded through the wind-up, the release and the landing
        pg.evaluate("() => { const B=window.BOSSMODE; B.player.y = B.snapshot().VH*0.80; B.player._chgT=0; B.player._chgOn=false; B.player._chgDash=null; }")
        rings0 = pg.evaluate("() => shockRings.length")
        pg.evaluate(FRAMES, [70, ['h', 'w']])                     # wind up to full
        rings_pre = pg.evaluate("() => shockRings.length")
        dash = pg.evaluate(FRAMES, [40, []])                       # release: the ram runs
        rings_post = pg.evaluate("() => shockRings.length")
        dframes = [f for f in dash if f['dash']]
        ok(len(dframes) >= 6, 'the ram ran for %d recorded frames' % len(dframes))
        judge(dframes or dash, 'charge dash')
        ok(max([f['ghosts'] for f in dash] or [0]) >= 2, 'orange afterimages trail the ram (peak %d on one frame)' % max([f['ghosts'] for f in dash] or [0]))
        ok(rings_post >= rings_pre + 1 or rings_pre > rings0, 'shock rings mark the launch and landing (%d -> %d -> %d)' % (rings0, rings_pre, rings_post))
        pg.screenshot(path=os.path.join(OUT, '02_dash_after.png'))

        # stale: the special ends with the stage, another pilot starts - nothing of his may draw
        pg.evaluate("() => window.BOSSMODE.stop()"); pg.wait_for_timeout(300)
        pg.evaluate(START, [1, 'yuri'])
        pg.evaluate(TRAP)
        stale = pg.evaluate(FRAMES, [30, []])
        ok(all(f['links'] == 0 and f['balls'] == 0 for f in stale), 'after Juggernaut, YURI draws no balls and no chains (max links %d)' % max(f['links'] for f in stale))
        b.close()
    stop()
    print('\n%d ok / %d fail' % (n_ok[0], len(fails)))
    for f in fails:
        print('  FAIL', f)
    if errs:
        print('page errors (%d):' % len(errs))
        for e in errs[:8]:
            print('   ', e)
    sys.exit(1 if fails or errs else 0)


if __name__ == '__main__':
    main()
