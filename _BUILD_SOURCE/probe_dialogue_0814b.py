#!/usr/bin/env python3
"""
probe_dialogue_0814b.py — Mike's item 10: "Still using plain dialogue where the game has its own
boxes." Asked for twice.

    python3 _BUILD_SOURCE/probe_dialogue_0814b.py

WHAT IT MEASURES, per in-play dialogue surface, in real Chromium on real frames:

    1. was `dlg_window` — the AUTHORED panel — actually drawn?
    2. did the surface draw a FAUX box instead (ctx.fillRect + ctx.strokeRect of its own)?
    3. did the body text go through the BOF bitmap face (msgTextLeft), or through the browser's
       font engine (ctx.fillText)?

⚠ (2) AND (3) ARE THE POINT, NOT (1). A surface can draw the authored panel and still lay canvas
BOFmil text on top of it, which is half of what Mike is complaining about — the faux box and the
wrong face travelled together in every case found here. So all three counters are taken, and a
pass needs the panel present AND no faux rect AND no fillText.

⚠ COUNTERS ARE SCOPED TO THE SURFACE, NOT THE FRAME. The HUD, the boss gauge and the scanlines
all draw rects and text every frame; counting them would make every surface look guilty. Each
draw function is wrapped individually and the counters are read around that ONE call.

⚠⚠ AND THE COUNTERS ALONE WERE GREEN ON A BROKEN PICTURE. First pass: authored panel, authored
face, zero faux rects on all four surfaces — and the saved frames showed the thaw's text running
off the right rail over the EQUIPPED box, and TWO panels stacked on top of each other on stage 3.
The box was right and the layout was wrong, which is CLAUDE.md rule 2 happening inside the very
probe written to enforce it. So two more measurements, both of what was actually drawn:

    FITS    every line handed to msgTextLeft is re-measured with msgMeasure at the height it was
            drawn at, and compared to the panel's own inner width. A line wider than its box is
            a fail no matter how authentic the font is.
    ONE     how many distinct panels were laid down. Two is a collision, not a dialogue.
"""
import os, sys, base64, http.server, socketserver, threading, functools

ROOT = os.path.dirname(os.path.abspath(__file__))
GAME = os.path.abspath(os.path.join(ROOT, '..'))
PROOF = os.path.join(GAME, 'docs', 'proofs')


def serve(directory, port=0):
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=directory)
    handler.log_message = lambda *a, **k: None
    httpd = socketserver.TCPServer(("127.0.0.1", port), handler)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return httpd.server_address[1], httpd.shutdown


# Wrap the instruments ONCE, globally, but only count while `window.__armed` is a surface name.
ARM = r"""
() => {
  const C = ctx;
  window.__tally = {};
  const T = () => { const a = window.__armed; if (!a) return null;
    return window.__tally[a] = window.__tally[a] ||
      {panel:0, rect:0, text:0, msg:0, boxes:[], lines:[]}; };
  const bump = (what) => { const t = T(); if (t) t[what]++; };

  const _fr = C.fillRect.bind(C), _sr = C.strokeRect.bind(C), _ft = C.fillText.bind(C);
  C.fillRect   = function(){ bump('rect'); return _fr.apply(C, arguments); };
  C.strokeRect = function(){ bump('rect'); return _sr.apply(C, arguments); };
  C.fillText   = function(){ bump('text'); return _ft.apply(C, arguments); };

  const _get = XART.get.bind(XART);
  XART.get = function(k){ if (k === 'dlg_window') bump('panel'); return _get(k); };

  /* THE PANEL'S OWN RECT, taken from drawPanel's arguments — the box every line must fit inside.
     Not inferred, not recomputed: the numbers the draw was handed. */
  const _dp = window.drawPanel;
  window.drawPanel = function(key, pal, x, y, w, h){
    const t = T();
    if (t && key === 'dlg_window') t.boxes.push({x, y, w, h});
    return _dp.apply(null, arguments);
  };

  /* EVERY LINE, RE-MEASURED AT THE HEIGHT IT WAS DRAWN AT. msgMeasure is the game's own metric
     for this face, so this asks the renderer how wide the thing it just drew actually is. */
  const _mtl = window.msgTextLeft;
  window.msgTextLeft = function(txt, x, y, h){
    const t = T();
    if (t) {
      let w = -1;
      try { w = window.msgMeasure(txt, h); } catch(e) {}
      t.lines.push({txt: String(txt).slice(0, 40), x, y, h, w});
      t.msg++;
    }
    return _mtl.apply(null, arguments);
  };
  return true;
}
"""

SETUP = r"""
(cfg) => {
  const out = {ok:false, err:null};
  try {
    ASSETS.ready = true;
    run.pilot = cfg.pilot; run.stage = cfg.stage;
    curStage = STAGES[cfg.stage-1];
    beginStage(cfg.stage); setState(GS.PLAY);
    player.reset(); player.invuln = 1e9;
    enemies.length = 0; eBullets.length = 0; pBullets.length = 0; particles.length = 0;
    /* the panel plate and the glyph sheet both have to have decoded, or the fallback draws and
       the measurement is of the fallback (0810o: stageText bails to NOTHING when its sheet is
       not up while its map is) */
    XART.rdy('dlg_window');
    out.ok = true;
  } catch(e){ out.err = String(e && e.message || e); }
  return out;
}
"""

GRAB = ("() => { const g = document.querySelector('#screen-area canvas')"
        " || document.querySelector('canvas'); return g ? g.toDataURL('image/png') : null; }")


def main():
    from playwright.sync_api import sync_playwright
    os.makedirs(PROOF, exist_ok=True)

    # label, pilot, stage, JS that puts the surface on screen and draws it once
    CASES = [
        ('thaw / SHIP beat', 'yuri', 3, "thawStart(); window.__armed='thaw'; "
                                        "for(let i=0;i<8;i++){ thawTick(1/60); thawDraw(); }"),
        ('thaw / PILOT beat', 'yuri', 3, "thawStart(); thaw.i=1; thaw.t=0.5; window.__armed='thaw'; "
                                         "for(let i=0;i<8;i++){ thawDraw(); }"),
        # ⚠ THE THAW HAS TO FINISH FIRST, because 0814b makes this narration DEFER to it — both
        # fire on stage 3 and both now draw a full-width panel. A probe that skipped the thaw
        # measured this surface drawing nothing and called it a regression; it was the queue
        # working. Drive the real sequence: thaw to completion, then Freezer speaks.
        ('freezer L3 narration', 'freezer', 3,
         "thawStart(); for(let i=0;i<600 && !thaw.done;i++) thawTick(1/60);"
         "freezerL3Begin(); window.__armed='frzL3';"
         "for(let i=0;i<8;i++){ freezerL3Tick(1/60); freezerL3Draw(); }"),
        ('stage story (0811m ref)', 'cole', 1,
         "story={lines:[['COLE','CIVILIAN EVACUATION IS BLOCKED ON THREE SIDES.']],i:0,typed:99,fade:1,t:0};"
         "window.__armed='story'; for(let i=0;i<8;i++){ storyDraw(); }"),
    ]

    port, stop = serve(GAME)
    url = 'http://127.0.0.1:%d/index.html' % port
    rows, fails = [], 0

    with sync_playwright() as p:
        b = p.chromium.launch(args=['--disable-gpu', '--no-sandbox', '--mute-audio'])
        for (label, pilot, stage, script) in CASES:
            pg = b.new_page(viewport={'width': 1100, 'height': 1200}, device_scale_factor=1)
            pg.goto(url, wait_until='load', timeout=60000)
            pg.wait_for_function("() => typeof ASSETS!=='undefined' && typeof setState==='function'", timeout=45000)
            pg.wait_for_function("() => (window.__bofFrames|0) > 4", timeout=45000)

            r = pg.evaluate(SETUP, {'pilot': pilot, 'stage': stage})
            if not r.get('ok'):
                print('setup failed for %s: %s' % (label, r.get('err')))
                fails += 1; pg.close(); continue

            pg.evaluate(ARM)
            pg.wait_for_timeout(1500)            # the await boundary the lazy decode needs
            pg.evaluate("(s) => { window.__armed=null; eval(s); window.__armed=null; }", script)
            t = pg.evaluate("() => window.__tally") or {}
            key = [k for k in t.keys()]
            m = t[key[0]] if key else {'panel': 0, 'rect': 0, 'text': 0, 'msg': 0,
                                       'boxes': [], 'lines': []}

            # how many DISTINCT panels — the same box redrawn each frame is one, two is a collision
            uniq = {(b['x'], b['y'], b['w'], b['h']) for b in m.get('boxes', [])}
            panels = len(uniq)

            # does every drawn line fit its box? the inner width is the frame inset dlgBox uses
            over = []
            for ln in m.get('lines', []):
                if ln['w'] is None or ln['w'] < 0:
                    continue
                box = None
                for bx, by, bw, bh in uniq:
                    if bx - 2 <= ln['x'] <= bx + bw and by - 2 <= ln['y'] <= by + bh + 4:
                        box = (bx, by, bw, bh); break
                if not box:
                    continue
                right_limit = box[0] + box[2] - 16          # dlgBox's own frame inset
                if ln['x'] + ln['w'] > right_limit + 1:
                    over.append('%s (+%dpx right)' % (ln['txt'][:16], ln['x'] + ln['w'] - right_limit))
                # ⚠ AND VERTICALLY. The last body row sat ON the bottom rail because the draw
                # tested the row's TOP against the limit and then drew its full height below it.
                # A horizontal-only check cannot see that; the proof frame could.
                bot_limit = box[1] + box[3] - int(box[3] * 0.10)
                if ln['y'] + ln['h'] > bot_limit + 1:
                    over.append('%s (+%dpx low)' % (ln['txt'][:16], ln['y'] + ln['h'] - bot_limit))

            # ⚠ OCCLUSION IS NOT OVERRUN, AND THE FIRST VERSION OF THIS PROBE COULD NOT TELL THEM
            # APART. Anchored bottom-right the panel fitted its box perfectly and was then drawn
            # OVER by the EQUIPPED corner, which lands after it: "show them" read as "SHOW TH".
            # overrun was 0 and correct. So the panel's rect is now checked against the HUD
            # element that owns that corner.
            eq = pg.evaluate("() => { if(typeof XART==='undefined'||!XART.rdy('nequipbox')) return null;"
                             " const im=XART.get('nequipbox'), H=64, W=H*(im.naturalWidth/im.naturalHeight);"
                             " return {x:(PLAY.x+PLAY.w)-W-6, y:(PLAY.y+PLAY.h)-H-6, w:W, h:H}; }")
            occl = 0
            if eq:
                for bx, by, bw, bh in uniq:
                    if bx < eq['x'] + eq['w'] and bx + bw > eq['x'] and \
                       by < eq['y'] + eq['h'] and by + bh > eq['y']:
                        occl += 1

            good = (m['panel'] > 0 and m['rect'] == 0 and m['text'] == 0 and m['msg'] > 0
                    and panels == 1 and not over and occl == 0)
            m['occl'] = occl
            if not good:
                fails += 1
            m['panels'] = panels
            m['over'] = over
            png = pg.evaluate(GRAB)
            if png:
                open(os.path.join(PROOF, 'dialogue_0814b_%s.png' %
                                  label.split('/')[0].strip().replace(' ', '_')), 'wb').write(
                    base64.b64decode(png.split(',', 1)[1]))
            rows.append((label, m, good))
            pg.close()
        b.close()
    stop()

    print('\n%-26s %8s %8s %9s %8s %7s %8s %6s' %
          ('SURFACE', 'dlg_win', 'faux box', 'ctx.text', 'BOF face', 'panels', 'overrun', 'hidden'))
    print('-' * 100)
    for (label, m, good) in rows:
        print('%-26s %8d %8d %9d %8d %7d %8d %6d   %s' %
              (label, m['panel'], m['rect'], m['text'], m['msg'],
               m.get('panels', 0), len(m.get('over', [])), m.get('occl', 0),
               'OK ' if good else 'FAIL'))
        for o in m.get('over', [])[:3]:
            print('%-26s   overruns its box: %s' % ('', o))
    print('\nfaux box / ctx.text must be ZERO (authored panel, authored face);')
    print('panels must be 1 (two stacked is a collision); overrun 0 (text past its rail);')
    print('hidden 0 (panel under the EQUIPPED corner, which is drawn on top of it).')
    print('frames saved to docs/proofs/dialogue_0814b_*.png')
    print('%d of %d surfaces clean' % (len(rows) - fails, len(rows)))
    sys.exit(1 if fails else 0)


if __name__ == '__main__':
    main()
