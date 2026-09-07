#!/usr/bin/env python3
"""probe_shipframes_0907v.py - every ship frame of every pilot, resolved in real Chromium.

    python _BUILD_SOURCE/probe_shipframes_0907v.py

Checks the 0907u atlas rebuild the only way that counts: 369 rows through `_shipCell`, in the
engine, with the console watched.

⚠ A ROW THAT PARSES IS NOT A CELL THAT RESOLVES. The manifest can hold a perfectly-shaped 8-element
row pointing anywhere; what proves the art is that `_shipCell` returns a canvas of the declared
canvas size with ink in it. This repo has shipped "a family referenced by name that does not exist"
more than once, and the guards turn it into a quiet empty frame rather than an error.

⚠ AND THE B-42 IS CHECKED THROUGH `applyLizzieSkin`, NOT BY READING ITS TABLE. `applyLizzieSkin`
repoints `BOFX.ships` AND flushes `XART._shipCells`; 0906g's note is explicit that the flush is the
load-bearing half and that `lizzieSkinOn` cannot detect its absence, because the same function sets
the flag. So the costume is asserted on the PIXELS the cache serves after the swap, never on the
flag - and it has to be, because these rects were broken on HEAD until this drop and every
structural check still passed.
"""
import os, sys, json, subprocess, http.server, socketserver, threading, functools

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PORT = 8199

JS = r"""
(() => {
  const out = {pilots:{}, errors:[]};
  const P = ['axel','cole','decker','falva','freezer','juggernaut','lizzie','maverick','yuri'];
  const SUF = ['','_nf','_l','_r','_pv0','_pv1','_pv2','_pv3','_pv4'];
  for (let i=0;i<8;i++) SUF.push('_br'+i);
  for (let i=0;i<8;i++) SUF.push('_so'+i);
  const ST = ['','_l','_r','_pv0','_pv1','_pv2','_pv3','_pv4'];
  const ALL = [];
  for (const s of SUF) ALL.push(s);
  for (const s of ST) { ALL.push(s+'_g1'); ALL.push(s+'_g2'); }

  function inkOf(c){
    const g=c.getContext('2d'); const d=g.getImageData(0,0,c.width,c.height).data;
    let n=0, x0=1e9,y0=1e9,x1=-1,y1=-1;
    for(let y=0;y<c.height;y++) for(let x=0;x<c.width;x++){
      if(d[(y*c.width+x)*4+3]>40){ n++; if(x<x0)x0=x; if(x>x1)x1=x; if(y<y0)y0=y; if(y>y1)y1=y; }
    }
    return {n, w:x1-x0+1, h:y1-y0+1, y0, y1};
  }

  for (const p of P) {
    const rec = {ok:0, missing:[], empty:[], hull:null, canvas:null, drawH:null};
    for (const s of ALL) {
      const k = 'ship_'+p+s;
      const c = XART.get(k);
      if (!c || !c.width) { rec.missing.push(s||'<base>'); continue; }
      const ink = inkOf(c);
      if (!ink.n) { rec.empty.push(s||'<base>'); continue; }
      rec.ok++;
      if (s === '_nf') {
        rec.canvas = c.width+'x'+c.height;
        rec.hull = ink.h;
        rec.drawH = +(ink.h / c.height * 60).toFixed(1);
      }
    }
    out.pilots[p] = rec;
  }

  // the B-42 costume, through the real swap
  const before = XART.get('ship_lizzie');
  const bi = inkOf(before);
  const okSwap = (typeof applyLizzieSkin === 'function') ? applyLizzieSkin(true) : false;
  const after = XART.get('ship_lizzie');
  const ai = inkOf(after);
  // a bomber is one solid body; the broken rects were fragments of other ships
  function pieces(c){
    const g=c.getContext('2d'); const d=g.getImageData(0,0,c.width,c.height).data;
    const W=c.width,H=c.height; const seen=new Uint8Array(W*H); let big=0, comps=0;
    for(let i=0;i<W*H;i++){
      if(seen[i]||d[i*4+3]<=40) continue;
      let st=[i], n=0; seen[i]=1;
      while(st.length){ const j=st.pop(); n++;
        const x=j%W, y=(j/W)|0;
        const nb=[x>0?j-1:-1, x<W-1?j+1:-1, y>0?j-W:-1, y<H-1?j+W:-1];
        for(const m of nb) if(m>=0 && !seen[m] && d[m*4+3]>40){ seen[m]=1; st.push(m); }
      }
      if(n>=40){ comps++; if(n>big) big=n; }
    }
    return {comps, big};
  }
  const pc = pieces(after);
  out.b42 = {swapReturned:okSwap, stockInk:bi.n, skinInk:ai.n,
             changed: bi.n !== ai.n, components: pc.comps, biggest: pc.big,
             biggestShare: +(pc.big/Math.max(1,ai.n)).toFixed(3)};
  if (typeof applyLizzieSkin === 'function') applyLizzieSkin(false);
  const back = inkOf(XART.get('ship_lizzie'));
  out.b42.restored = back.n === bi.n;
  return out;
})()
"""


def main():
    from playwright.sync_api import sync_playwright
    os.chdir(ROOT)
    H = functools.partial(http.server.SimpleHTTPRequestHandler, directory=ROOT)
    socketserver.TCPServer.allow_reuse_address = True
    srv = socketserver.TCPServer(('127.0.0.1', PORT), H)
    srv.RequestHandlerClass.log_message = lambda *a, **k: None
    threading.Thread(target=srv.serve_forever, daemon=True).start()

    errs = []
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        pg = b.new_page(viewport={'width': 1000, 'height': 900})
        pg.on('console', lambda m: errs.append(m.text) if m.type == 'error' else None)
        pg.on('pageerror', lambda e: errs.append('PAGEERROR ' + str(e)))
        pg.goto('http://127.0.0.1:%d/index.html' % PORT)
        pg.wait_for_timeout(1200)
        # touch every ship key, then give the atlas a real decode window (0905: a frame count is
        # not a clock - shoot.py's own warm never yields, so lazily-loaded art never arrives)
        pg.evaluate("() => { for(const k in BOFX.ships) XART.rdy(k); }")
        pg.wait_for_function("() => { const s=XART.get('ship_cole'); return !!(s && s.width); }",
                             timeout=15000)
        pg.wait_for_timeout(1500)
        res = pg.evaluate(JS)
        b.close()
    srv.shutdown()

    print('%-11s %-7s %-9s %-11s %-11s %s'
          % ('pilot', 'frames', 'canvas', 'hull ink', 'hull draws', 'missing / empty'))
    bad = 0
    for p, r in res['pilots'].items():
        prob = []
        if r['missing']:
            prob.append('MISSING ' + ','.join(r['missing']))
        if r['empty']:
            prob.append('EMPTY ' + ','.join(r['empty']))
        if prob:
            bad += 1
        print('%-11s %-7d %-9s %-11s %-11s %s'
              % (p, r['ok'], r['canvas'] or '?', r['hull'] or '?',
                 ('%.1f px' % r['drawH']) if r['drawH'] else '?', '; '.join(prob) or 'none'))
    print()
    hs = [r['drawH'] for r in res['pilots'].values() if r['drawH']]
    print('hull drawn height across the fleet: %.1f .. %.1f px (spread %.1f%%)'
          % (min(hs), max(hs), (max(hs) / min(hs) - 1) * 100))
    print()
    b42 = res['b42']
    print('B-42 costume through applyLizzieSkin:')
    print('   swap returned true                %s' % b42['swapReturned'])
    print('   the pixels actually changed       %s  (%d -> %d ink px)'
          % (b42['changed'], b42['stockInk'], b42['skinInk']))
    print('   ONE body, not fragments           %d component(s), biggest holds %.0f%% of the ink'
          % (b42['components'], b42['biggestShare'] * 100))
    print('   stock restored on toggle off      %s' % b42['restored'])
    print()
    print('console errors: %d %s' % (len(errs), errs[:3]))
    ok = (bad == 0 and not errs and b42['changed'] and b42['restored']
          and b42['biggestShare'] > 0.80)
    print('RESULT:', 'PASS' if ok else 'FAIL')
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
