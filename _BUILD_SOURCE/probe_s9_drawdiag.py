#!/usr/bin/env python3
"""probe_s9_drawdiag.py - why did the ramp probe tally ZERO art-key blits for units it watched
spawn? Spawn one of each specialist directly and ask the draw path, step by step, where it stops.
Throwaway diagnostic for 0905z."""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import shoot as sh
from playwright.sync_api import sync_playwright

UNITS = ['wskim', 'pneedle', 'pmine', 'gleech', 'vmanta', 'echof', 'tsplit', 'cbreak',
         'horizon', 'dreadv']

DIAG = r"""
() => {
  const out = {xartSeen:false, wrapped:false, drewKeys:0, sample:[], units:[]};
  out.xartSeen = (typeof XART !== 'undefined');
  if (out.xartSeen) {
    window.__d = {};
    const real = XART.get.bind(XART);
    XART.get = function(k){ window.__d[k] = (window.__d[k]||0)+1; return real(k); };
    out.wrapped = true;
  }
  for (const u of %UNITS%) {
    const e = spawnEnemy(u, 100 + Math.random()*200, 140);
    const rec = {u:u, spawned:!!e};
    if (e) {
      rec.art = e.art; rec.s9 = e._s9; rec.hp = e.hp;
      rec.enemyArt = (typeof ENEMY_ART !== 'undefined') ? ENEMY_ART[e.art] : '(no ENEMY_ART)';
      rec.state = (typeof enemyArtState === 'function') ? enemyArtState(e) : '?';
      rec.rdyState = XART.rdy(e.art + '_' + rec.state);
      rec.rdyIdle = XART.rdy(e.art + '_idle');
      rec.srcState = !!(XART._src && XART._src[e.art + '_' + rec.state]);
      rec.srcIdle = !!(XART._src && XART._src[e.art + '_idle']);
    }
    out.units.push(rec);
  }
  return out;
}
"""

AFTER = r"""
() => {
  const d = window.__d || {};
  const ks = Object.keys(d);
  ks.sort((a,b) => d[b] - d[a]);
  return {total:ks.length, top:ks.slice(0,25).map(k => k + '=' + d[k]),
          ns9:ks.filter(k => k.indexOf('ns9') === 0).map(k => k + '=' + d[k])};
}
"""


def main():
    port, stop = sh.serve(sh.GAME)
    try:
        with sync_playwright() as pw:
            b = pw.chromium.launch()
            pg = b.new_page(viewport={'width': 480, 'height': 512})
            errs = []
            pg.on('pageerror', lambda e: errs.append(str(e)))
            pg.goto('http://127.0.0.1:%d/index.html' % port)
            pg.wait_for_function('typeof ASSETS!=="undefined" && typeof loop==="function"', timeout=30000)
            pg.wait_for_timeout(2500)
            pg.evaluate(sh.TRAP_RAF)
            r = pg.evaluate(sh.SETUP, {'state': 'PLAY', 'stage': 9, 'pilot': 'cole', 'invuln': True})
            print('setup:', r)
            pg.evaluate(sh.STEP, 30)                       # settle a few real frames first
            d = pg.evaluate(DIAG.replace('%UNITS%', json.dumps(UNITS)))
            print('\nXART visible: %s   get() wrapped: %s' % (d['xartSeen'], d['wrapped']))
            print('\n%-9s %-14s %-9s %-16s %-7s  rdy(state) rdy(idle)  _src(state) _src(idle)'
                  % ('unit', 'art', '_s9', 'ENEMY_ART[art]', 'state'))
            for u in d['units']:
                if not u.get('spawned'):
                    print('  %-9s ** spawnEnemy returned nothing **' % u['u']); continue
                print('  %-9s %-14s %-9s %-16s %-7s     %-6s    %-6s      %-6s     %-6s'
                      % (u['u'], u['art'], u['s9'], u['enemyArt'], u['state'],
                         u['rdyState'], u['rdyIdle'], u['srcState'], u['srcIdle']))
            pg.evaluate(sh.STEP, 120)                      # two seconds of real drawing
            a = pg.evaluate(AFTER)
            print('\nXART.get keys tallied over 120 frames: %d distinct' % a['total'])
            print('  ns9* keys: %s' % (', '.join(a['ns9']) if a['ns9'] else '(NONE)'))
            print('  busiest:   %s' % ', '.join(a['top'][:12]))
            if errs:
                print('\npage errors (%d): %s' % (len(errs), errs[0][:300]))
            b.close()
    finally:
        stop()


if __name__ == '__main__':
    main()
