#!/usr/bin/env python3
"""jsq.py - boot the real game in headless Chromium and print the value of JS expressions.

    python _BUILD_SOURCE/jsq.py "SUBBOSS[4]" "typeof olivewardenInit"
    python _BUILD_SOURCE/jsq.py --file snippet.js        # an arrow function () => {...} evaluated once

Each expression is evaluated as `() => (EXPR)` after boot, with shoot.py's TRAP_RAF installed. Values
are JSON-serialised (functions print as their source's first 300 characters)."""
import os, sys, json, argparse
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import shoot as sh  # noqa: E402

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('exprs', nargs='*')
    ap.add_argument('--file')
    a = ap.parse_args()
    from playwright.sync_api import sync_playwright
    port, stop = sh.serve(sh.GAME)
    errs = []
    with sync_playwright() as p:
        b = p.chromium.launch(args=['--disable-gpu', '--no-sandbox', '--mute-audio'])
        pg = b.new_page(viewport={'width': 1000, 'height': 1100})
        pg.on('pageerror', lambda e: errs.append(str(e)[:200]))
        pg.goto('http://127.0.0.1:%d/index.html' % port, wait_until='load', timeout=120000)
        pg.wait_for_function("() => typeof setState==='function' && (window.__bofFrames|0) > 4", timeout=120000)
        pg.evaluate(sh.TRAP_RAF); pg.wait_for_timeout(60)
        fmt = "(v) => { const seen=new WeakSet(); return JSON.stringify(v,(k,x)=>{ if(typeof x==='function') return 'fn: '+String(x).slice(0,300); if(x&&typeof x==='object'){ if(seen.has(x)) return '[circ]'; seen.add(x);} return x; },1); }"
        if a.file:
            v = pg.evaluate(open(a.file, encoding='utf-8').read())
            print(json.dumps(v, indent=1)[:20000])
        for e in a.exprs:
            try:
                v = pg.evaluate('() => { const v = (' + e + '); return (' + fmt + ')(v); }')
            except Exception as ex:
                v = 'ERR ' + str(ex)[:300]
            print('==', e, '\n', (v or 'undefined')[:6000])
        b.close()
    stop()
    if errs: print('page errors:', errs[:5])

if __name__ == '__main__':
    main()
