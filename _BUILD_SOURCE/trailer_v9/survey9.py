"""survey9.py - fly a stage headless on the trailer harness and log WHEN things happen, saving no frames.

    python survey9.py --stage 6 --pilot cole --diff normal --frames 9000 --every 60 \
        --probe "({t:stageTimer|0, sb:!!subBossActive, bo:!!bossActive, ...})" \
        --event "3000:Input.injectTap('d')" --when "s6Wing&&s6Wing.choice&&!s6Wing.route:Input.injectTap('enter')"

Takes are expensive (~0.33 MB a frame) and the disk is not, so every take window is found here first.
"""
import os, sys, json, argparse
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import capture3 as C3   # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--stage', type=int)
    ap.add_argument('--fight', default=None, help='stage/role, e.g. 7/boss')
    ap.add_argument('--pilot', default='cole')
    ap.add_argument('--diff', default='normal')
    ap.add_argument('--frames', type=int, default=3000)
    ap.add_argument('--every', type=int, default=60)
    ap.add_argument('--mode', default='weave')
    ap.add_argument('--probe', default='({t:stageTimer|0,st:state})')
    ap.add_argument('--setup', default='')
    ap.add_argument('--event', action='append', default=[])
    ap.add_argument('--when', action='append', default=[], help='COND:JS, fired once when COND first holds')
    ap.add_argument('--shot', action='append', default=[], help='frame numbers to save a PNG at')
    ap.add_argument('--out', default=os.path.join(HERE, 'survey'))
    a = ap.parse_args()
    from playwright.sync_api import sync_playwright
    port, stop = C3.serve()
    os.makedirs(a.out, exist_ok=True)
    errs = []
    with sync_playwright() as pw:
        b = pw.chromium.launch(args=['--mute-audio'], executable_path=C3.CHROME)
        p = b.new_page(viewport={'width': 1280, 'height': 960})
        p.on('pageerror', lambda e: errs.append(str(e)[:200]))
        p.goto('http://127.0.0.1:%d/index.html?quality=high' % port)
        p.wait_for_function("() => (window.__bofFrames|0) > 4", timeout=90000)
        p.evaluate(C3.LIB)
        p.evaluate("() => { ASSETS.ready = true; dlgBox = dlgBox; }")
        p.evaluate("(d) => { diffKey = d; }", a.diff)
        if a.setup:
            print('setup', p.evaluate("() => { try { %s } catch (e) { return 'ERR ' + e; } }" % a.setup))
        if a.fight:
            s, r = a.fight.split('/')
            print(p.evaluate("([s, r, pl]) => window.__fight(s, r, pl)", [int(s), r, a.pilot]))
        else:
            print(p.evaluate("([s, pl]) => window.__run(s, pl)", [a.stage, a.pilot]))
        p.evaluate("([m]) => { window.__mode = m; window.__fire = true; }", [a.mode])
        ev = {}
        for e in a.event:
            k, js = e.split(':', 1)
            ev[int(k)] = js
        whens = [w.split(':', 1) for w in a.when]
        fired = set()
        shots = set(int(s) for s in a.shot)
        log = []
        f = 0
        while f < a.frames:
            later = [k for k in ev if k > f]
            n = min(a.every, a.frames - f, (min(later) - f) if later else 10 ** 9)
            if f in ev:
                print('@%d event %s' % (f, p.evaluate("() => { try { %s ; return 'ok'; } catch (e) { return 'ERR ' + e; } }" % ev[f])))
            p.evaluate("(n) => window.__step(n)", n)
            f += n
            for i, (cond, js) in enumerate(whens):
                if i in fired:
                    continue
                if p.evaluate("() => { try { return !!(%s); } catch (e) { return false; } }" % cond):
                    fired.add(i)
                    print('@%d when %s -> %s' % (f, cond[:40], p.evaluate("() => { try { %s ; return 'ok'; } catch (e) { return 'ERR ' + e; } }" % js)))
            r = p.evaluate("() => { try { return %s; } catch (e) { return 'ERR ' + String(e).slice(0, 120); } }" % a.probe)
            log.append([f, r])
            print(f, json.dumps(r)[:400], flush=True)
            if any(f - n < s <= f for s in shots):
                import base64
                d = p.evaluate("() => document.querySelector('#screen').toDataURL('image/png')")
                open(os.path.join(a.out, 'f%05d.png' % f), 'wb').write(base64.b64decode(d.split(',', 1)[1]))
            p.wait_for_timeout(40)
        b.close()
    stop()
    print('page errors', len(errs), errs[:5])
    json.dump(log, open(os.path.join(a.out, 'log.json'), 'w'))


if __name__ == '__main__':
    main()
