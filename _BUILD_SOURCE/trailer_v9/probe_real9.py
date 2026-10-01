"""probe_real9.py - does the take ship really take hits, and does the dodge autopilot avoid them?

Runs the same fights twice in real Chromium, no frames saved: the CONTROL arm flies the old straight-to-target
autopilot with the real playerHit, the DODGE arm flies real9's autopilot. A control with zero hits would mean the hit
path is still stubbed and the dodge number means nothing.
    python probe_real9.py
"""
import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import capture3 as C3, capture9 as C9, real9   # noqa: E402

CASES = [(3, 'boss', 'juggernaut', 'normal'), (1, 'boss', 'axel', 'furious'), (5, 'boss', 'falva', 'normal'),
         (7, 'boss', 'decker', 'hard'), (2, 'mini', 'yuri', 'normal')]
FRAMES = 1800
ARMS = sys.argv[1:] or ['control', 'dodge']


def main():
    from playwright.sync_api import sync_playwright
    port, stop = C3.serve()
    res = []
    with sync_playwright() as pw:
        b = pw.chromium.launch(args=['--mute-audio'], executable_path=C3.CHROME)
        for st, role, pk, diff in CASES:
            for arm in ARMS:
                p = b.new_page(viewport={'width': 1280, 'height': 960})
                errs = []
                p.on('pageerror', lambda e: errs.append(str(e)[:160]))
                p.goto('http://127.0.0.1:%d/index.html?quality=high' % port)
                p.wait_for_function("() => (window.__bofFrames|0) > 4", timeout=90000)
                p.evaluate(C3.LIB); p.evaluate(C9.LIB9); p.evaluate(real9.LIB_REAL)
                p.evaluate("() => { ASSETS.ready = true; }")
                p.evaluate("(d) => { diffKey = d; }", diff)
                p.evaluate("([s, r, k]) => window.__fight(s, r, k)", [st, role, pk])
                p.evaluate("(a) => { window.__mode = 'boss'; window.__fire = true; window.__burst = [36, 66]; window.__noDodge = a; }",
                           arm == 'control')
                n = 0
                while n < FRAMES:
                    p.evaluate("(n) => window.__step(n)", 60)
                    p.wait_for_timeout(60)
                    n += 60
                m = p.evaluate("() => window.__metrics()")
                r = dict(case='%d/%s/%s/%s' % (st, role, pk, diff), arm=arm, hits=m.get('hits'), deaths=m.get('deaths'),
                         rolls=m.get('rolls'), state=m.get('st'), killers=m.get('killers'), err=m.get('err'), page_errors=len(errs))
                print(json.dumps(r)); res.append(r)
                p.close()
        b.close()
    stop()
    ctl = sum(r['hits'] or 0 for r in res if r['arm'] == 'control')
    dod = sum(r['hits'] or 0 for r in res if r['arm'] == 'dodge')
    print('TOTAL hits: control %d  dodge %d' % (ctl, dod))
    print('PASS' if ctl > 0 and dod < ctl else 'FAIL')
    json.dump(res, open(os.path.join(HERE, 'probe_real9.json'), 'w'), indent=1)


if __name__ == '__main__':
    main()
