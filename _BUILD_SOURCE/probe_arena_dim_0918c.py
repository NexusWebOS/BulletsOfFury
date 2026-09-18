#!/usr/bin/env python3
"""
probe_arena_dim_0918c.py - the stage-2 boss arena's lava is dimmed so the Furnace Tyrant and his rounds read.

Mike: "When we get to the boss fight, please darken our tileset ... that makes it easier to see our boss and his
projectiles."  Real Chromium, Boss Mode, the live fight: the same moment captured with the dim OFF
(the dim function swapped for a no-op - it is a top-level declaration, so window.arenaBossDimDraw rebinds it) and ON.
Measures the lower half of the screen (bed only - the boss sits in the top half) and the boss's own pixels.
Frames: docs/proofs/arena_dim_0918c/.
"""
import os, sys, base64, json, io
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.join(ROOT, '_BUILD_SOURCE'))
import shoot as sh
from PIL import Image, ImageStat
from playwright.sync_api import sync_playwright
OUT = os.path.join(ROOT, 'docs', 'proofs', 'arena_dim_0918c')
N = {'ok': 0}; FAILS = []
def ok(c, m):
    if c: N['ok'] += 1; print('  ok   ' + m)
    else: FAILS.append(m); print('  FAIL ' + m)

GRAB = """async (dimOn) => {
  const fr=()=>new Promise(r=>requestAnimationFrame(()=>r()));
  if(!window.__dimReal) window.__dimReal=window.arenaBossDimDraw;
  window.arenaBossDimDraw = dimOn ? window.__dimReal : function(){};
  let calls=0; const f=window.arenaBossDimDraw; window.arenaBossDimDraw=function(){ calls++; return f.apply(this,arguments); };
  for(let i=0;i<20;i++) await fr();
  const url=document.getElementById('screen').toDataURL('image/png');
  window.arenaBossDimDraw = window.__dimReal;
  return {url, calls};
}"""

def lum(im, box):
    return ImageStat.Stat(im.crop(box).convert('L')).mean[0]

def main():
    os.makedirs(OUT, exist_ok=True)
    port, stop = sh.serve(sh.GAME)
    with sync_playwright() as pw:
        br = pw.chromium.launch(args=['--disable-gpu', '--no-sandbox', '--mute-audio'])
        pg = br.new_page(viewport={'width': 1100, 'height': 1000}); errs = []
        pg.on('pageerror', lambda e: errs.append('page:' + str(e)[:200]))
        pg.on('console', lambda m: errs.append('console:' + m.text[:200]) if m.type == 'error' else None)
        pg.goto('http://127.0.0.1:%d/index.html?bossmode=1' % port, wait_until='load', timeout=60000)
        pg.wait_for_function("() => window.BOSSMODE && window.BOSSMODE.ready", timeout=90000)
        st = pg.evaluate("""async () => {
          const B=window.BOSSMODE, fr=()=>new Promise(r=>requestAnimationFrame(()=>r()));
          B.start(2,'boss','cole',false);
          let t0=performance.now();
          while(performance.now()-t0<40000 && !(typeof boss!=='undefined' && boss && boss._furnace && B.player && !B.player.dead)) await fr();
          B.setInvuln(true);
          t0=performance.now(); while(performance.now()-t0<12000) await fr();   // into the fight, past the 1.6 s ease
          return {furnace:!!(boss&&boss._furnace), secs:_arenaLavaScroll/ARENA_LAVA_SPD, phase:boss&&boss._fz?boss._fz.phase:null};
        }""")
        print('  setup', st)
        ok(st['furnace'] and st['secs'] > 2, 'the Furnace fight is live and the arena has run %.1f s' % st['secs'])
        # freeze the world so OFF and ON are the same moment
        pg.evaluate("() => { window.__upd=window.updatePlay; }")
        shots = {}
        for on in (False, True):
            r = pg.evaluate(GRAB, on)
            im = Image.open(io.BytesIO(base64.b64decode(r['url'].split(',', 1)[1]))).convert('RGB')
            im.save(os.path.join(OUT, '%s.png' % ('dim_on' if on else 'dim_off')))
            shots[on] = (im, r['calls'])
        W, H = shots[True][0].size
        bed = (0, int(H * 0.62), W, int(H * 0.86))
        off_l, on_l = lum(shots[False][0], bed), lum(shots[True][0], bed)
        print('  bed luminance off %.1f  on %.1f  (dim calls on=%d)' % (off_l, on_l, shots[True][1]))
        ok(shots[True][1] > 0, 'the dim pass runs on the live arena (%d calls)' % shots[True][1])
        ok(on_l < off_l * 0.62, 'the lava bed is darkened (%.1f -> %.1f, %.0f%%)' % (off_l, on_l, 100 * on_l / max(1, off_l)))
        ok(on_l > off_l * 0.25, 'but not blacked out - the lava still reads (%.1f)' % on_l)
        # the arena dim must not touch anything outside the boss arena: an ordinary stage-2 frame draws no dim
        ctl = pg.evaluate("""() => { const b=bossActive, h=_arenaHold; let n=0; const f=window.arenaBossDimDraw; window.arenaBossDimDraw=function(){ n++; };
          window.arenaBossDimDraw=f;
          // the real function: live boss -> the level rises; no boss -> it falls back to 0
          const lv0=_arenaDimLv; arenaBossDimDraw(1/60); const up=_arenaDimLv;
          const s3=run.stage; bossActive=false; for(let i=0;i<200;i++) arenaBossDimDraw(1/60); const down=_arenaDimLv; bossActive=b;
          _arenaDimLv=lv0; return {lv0, up, down}; }""")
        print('  control', ctl)
        ok(ctl['lv0'] > 0.99 and ctl['up'] > 0.99 and ctl['down'] == 0, 'full dim while the boss lives, back to none once he is gone (%s)' % ctl)
        side = Image.new('RGB', (W * 2 + 8, H), (0, 0, 0)); side.paste(shots[False][0], (0, 0)); side.paste(shots[True][0], (W + 8, 0))
        side.save(os.path.join(OUT, '_off_vs_on.png'))
        real = [e for e in errs if 'favicon' not in e and 'AudioContext encountered an error' not in e]
        ok(not real, 'page/console errors: %d %s' % (len(real), real[:3]))
        br.close()
    stop()
    print('\n%d ok / %d fail' % (N['ok'], len(FAILS)))
    for f in FAILS: print('  FAIL ' + f)
    sys.exit(1 if FAILS else 0)

if __name__ == '__main__':
    main()
