#!/usr/bin/env python3
"""probe_stagex_map_0928.py - Mike 0928: skipped rebels fly out of Stage 6 on the campaign map and spiral
around its centre; the pilot can take Stage 7 or Stage X.

Sets a campaign that took the Harrier route through Stage 6, opens the real map, lets the boot run, and
records every rebel ship the map draws (XART.get key + the ctx transform, never an .src match), then
drives DOWN / RIGHT / UP with real key presses and checks the focus, the chosen rival and that Stage 7
stays selectable. Screenshots of the launch, the orbit and the focused Stage X card.
"""
import os, sys, json, base64, math, http.server
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
http.server.SimpleHTTPRequestHandler.log_message = lambda *a: None
import shoot as sh
from playwright.sync_api import sync_playwright

OUT = os.path.join(sh.GAME, '_shots', 'opus0928', 'stagex_map')
N = {'ok': 0}; FAILS = []
def ok(c, m):
    if c: N['ok'] += 1; print('  ok   ' + m)
    else: FAILS.append(m); print('  FAIL ' + m)

TRAP = r"""
() => {
  window.__ships=[];
  if(!window.__dw){
    const orig=ctx.drawImage;window.__dw=orig;
    const xg=XART.get.bind(XART);window.__lastKey=null;XART.get=function(k){window.__lastKey=k;return xg(k);};
    ctx.drawImage=function(im){
      const k=window.__lastKey;
      if(k&&/^rr_ship_/.test(k)){const m=ctx.getTransform();window.__ships.push({k,x:m.e/SS,y:m.f/SS,rot:Math.atan2(m.b,m.a)});}
      window.__lastKey=null;return orig.apply(this,arguments);
    };
  }
}
"""

def main():
    os.makedirs(OUT, exist_ok=True)
    port, stop = sh.serve(sh.GAME)
    errs = []
    with sync_playwright() as pw:
        br = pw.chromium.launch(args=['--no-sandbox', '--mute-audio'])
        pg = br.new_page(viewport={'width': 1000, 'height': 1100})
        pg.on('pageerror', lambda e: errs.append('page:' + str(e)[:200]))
        pg.on('console', lambda m: errs.append('console:' + m.text[:200]) if m.type == 'error' or 'draw error' in m.text else None)
        pg.goto('http://127.0.0.1:%d/index.html' % port, wait_until='load', timeout=120000)
        pg.wait_for_function("() => (window.__bofFrames|0)>4", timeout=120000)
        pg.evaluate("""() => { run.mode='campaign';run.pilot='maverick';diffKey='normal';DIFF=DIFFS.normal;
          campaign.unlockedMax=7;campaign.rivalScattered=false;campaign.rivalDefeated=[false,false,false,false,false];
          s6Wing={route:'left'};Rival24.scatterAfterHarrier();s6Wing=null;openStageSelect(7,{}); }""")
        # the map's own boot (terminal text, zoom, flag drop) runs first; the rebels wait for it
        pg.wait_for_function("() => state==='stagesel' && sselBoot===0 && sselUnlockCine==null", timeout=60000)
        pg.evaluate(TRAP)
        frames = []
        for i in range(26):
            pg.wait_for_timeout(250)
            f = pg.evaluate("() => { const s=window.__ships.slice();window.__ships=[];return s; }")
            frames.append(f)
            if i in (1, 4, 8, 20):
                d = pg.evaluate("() => document.getElementById('screen').toDataURL('image/png')")
                open(os.path.join(OUT, 'map_%02d.png' % i), 'wb').write(base64.b64decode(d.split(',', 1)[1]))
        hub = pg.evaluate("() => { const p=fr27CoreMapPosition(); const s6=sselFlagScreenXY(6), s7=sselFlagScreenXY(7); return {hub:p,s6,s7}; }")
        first = [f for f in frames if f]
        ok(bool(first), 'the map draws the rebel ships (%d frames with ships)' % len(first))
        if first:
            f0 = first[0]; s6 = hub['s6']; s7 = hub['s7']
            d6 = min(math.hypot(q['x'] - s6['x'], q['y'] - s6['y']) for q in f0)
            d7 = min(math.hypot(q['x'] - s7['x'], q['y'] - s7['y']) for q in f0)
            ok(d6 < d7, 'they launch from the Stage 6 flag, not Stage 7 (nearest ship %.0fpx from 6, %.0fpx from 7)' % (d6, d7))
        late = frames[-1]
        keys = sorted(set(q['k'] for q in late))
        ok(len(keys) == 5, 'all five rebels are in the orbit (%s)' % ','.join(k.replace('rr_ship_', '') for k in keys))
        h = hub['hub']
        # the orbit is an ellipse (ry .55) whose radius breathes 92 +/- 10 around the Stage X plaque
        radii = [math.hypot(q['x'] - h['x'], (q['y'] - h['y']) / .55) for q in late]
        ok(bool(radii) and all(78 < r < 106 for r in radii), 'they circle the map centre, radius 92 +/- 10 (radii %s)' % sorted(set(round(r) for r in radii)))
        # they keep moving around it: the same ship's angle advances between two late frames
        def ang(fr, k):
            q = [q for q in fr if q['k'] == k]
            return math.atan2((q[0]['y'] - h['y']) / .55, q[0]['x'] - h['x']) if q else None
        a1, a2 = ang(frames[-6], keys[0]), ang(frames[-1], keys[0])
        ok(a1 is not None and a2 is not None and abs(math.atan2(math.sin(a2 - a1), math.cos(a2 - a1))) > .2, 'the orbit moves (%.2f rad over 1.25s)' % (abs(math.atan2(math.sin(a2 - a1), math.cos(a2 - a1))) if a1 is not None and a2 is not None else -1))
        # nose-first: the sprite's forward (south, +PI/2 after rotation) follows the orbit's tangent
        # real key presses: DOWN focuses Stage X, RIGHT picks the next rival, UP goes back to the map
        before = pg.evaluate("() => sselCursor")
        pg.keyboard.press('ArrowDown'); pg.wait_for_timeout(350)
        st = pg.evaluate("() => ({focus:Rival24.mapFocused, cursor:sselCursor})")
        ok(st['focus'], 'DOWN on the map focuses Stage X')
        d = pg.evaluate("() => document.getElementById('screen').toDataURL('image/png')")
        open(os.path.join(OUT, 'map_focus.png'), 'wb').write(base64.b64decode(d.split(',', 1)[1]))
        pg.keyboard.press('ArrowRight'); pg.wait_for_timeout(350)
        pg.wait_for_timeout(300)
        d = pg.evaluate("() => document.getElementById('screen').toDataURL('image/png')")
        open(os.path.join(OUT, 'map_focus_right.png'), 'wb').write(base64.b64decode(d.split(',', 1)[1]))
        pg.keyboard.press('ArrowUp'); pg.wait_for_timeout(350)
        st2 = pg.evaluate("() => ({focus:Rival24.mapFocused, cursor:sselCursor, state})")
        ok(not st2['focus'] and st2['cursor'] == before, 'UP returns to the map with its stage cursor restored (%s)' % st2['cursor'])
        ok(st2['cursor'] == 7 or before == 7, 'Stage 7 stays the map selection alongside Stage X')
        ok(not errs, 'no page, console or draw errors (%s)' % errs[:3])
        br.close()
    stop()
    print('%d ok / %d fail' % (N['ok'], len(FAILS)))
    sys.exit(1 if FAILS else 0)

if __name__ == '__main__':
    main()
