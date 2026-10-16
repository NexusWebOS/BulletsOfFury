"""inspect9.py - evaluate one JS expression in a booted game page and print the JSON.

    python inspect9.py "debugFightList().map(e => [e.stage, e.role, e.kind, e.name])"
"""
import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import capture3 as C3   # noqa: E402


def main():
    expr = sys.argv[1]
    from playwright.sync_api import sync_playwright
    port, stop = C3.serve()
    with sync_playwright() as pw:
        b = pw.chromium.launch(args=['--mute-audio'], executable_path=C3.CHROME)
        p = b.new_page(viewport={'width': 1280, 'height': 960})
        p.goto('http://127.0.0.1:%d/index.html?quality=high' % port)
        p.wait_for_function("() => (window.__bofFrames|0) > 4", timeout=90000)
        r = p.evaluate("() => { try { return %s; } catch (e) { return 'ERR ' + e; } }" % expr)
        print(json.dumps(r, indent=1)[:20000])
        b.close()
    stop()


if __name__ == '__main__':
    main()
