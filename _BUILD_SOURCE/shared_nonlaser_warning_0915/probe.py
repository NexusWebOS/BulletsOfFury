"""Real Chromium proof for the shared non-laser boss warning and Overlord charge."""
import base64, json, sys, threading, http.server
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).parent
OUT = ROOT / '_shots' / 'shared_nonlaser_warning_0915'
OUT.mkdir(parents=True, exist_ok=True)
sys.path.insert(0, str(ROOT / '_BUILD_SOURCE'))
import shoot
sys.path.insert(0, str(ROOT / '_BUILD_SOURCE' / 'trailer_v7'))
import capture3
from playwright.sync_api import sync_playwright
from PIL import Image

def main():
    checks, errors, shots = [], [], []
    details = {}
    def ok(value, label):
        checks.append({'pass': bool(value), 'label': label})
        print(('ok  ' if value else 'FAIL ') + label, flush=True)

    class Quiet(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=str(ROOT), **kwargs)
        def log_message(self, *args):
            pass

    server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), Quiet)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    with sync_playwright() as pw:
        browser = pw.chromium.launch(args=['--no-sandbox', '--mute-audio'])
        page = browser.new_page(viewport={'width': 1100, 'height': 1200})
        page.on('pageerror', lambda e: errors.append('page ' + str(e)))
        page.on('console', lambda m: errors.append('console ' + m.text) if m.type == 'error' else None)
        page.goto(f'http://127.0.0.1:{server.server_port}/index.html', wait_until='load', timeout=120000)
        page.wait_for_function('() => (window.__bofFrames|0) > 4', timeout=120000)
        page.evaluate(shoot.TRAP_RAF)
        page.evaluate(capture3.LIB)
        page.evaluate("""() => {
          window.__warningBlits=[];
          const f=l23FovDraw;
          l23FovDraw=function(b,B,i,p,k,lane){
            const phase=l23FovPhase(k), before=ctx.getTransform();
            const drawn=f.apply(this,arguments);
            window.__warningBlits.push({type:'fov',phase:phase,drawn:!!drawn,k:+k.toFixed(3),x:+p.x.toFixed(1),y:+p.y.toFixed(1),lane:lane});
            return drawn;
          };
          const a=l23WarnSymbolDraw;
          l23WarnSymbolDraw=function(b,B){
            const phase=l23FovPhase(clamp(B.t/Math.max(.001,B.warm),0,1));
            const drawn=a.apply(this,arguments);
            window.__warningBlits.push({type:'alert',phase:phase,drawn:!!drawn});
            return drawn;
          };
        }""")

        def step(n):
            for i in range(0, n, 24):
                page.evaluate('n => window.__step(n)', min(24, n-i))
                page.wait_for_timeout(20)

        def capture(name):
            page.evaluate('() => { window.__warningBlits=[]; shake=0; drawWorld(0); }')
            png = page.evaluate("() => document.querySelector('#screen').toDataURL('image/png').split(',')[1]")
            path = OUT / f'{name}.png'
            path.write_bytes(base64.b64decode(png))
            shots.append(path)
            return page.evaluate("() => ({blits:window.__warningBlits.slice(), state:boss._ovState, locked:!!(boss._chargeTell&&boss._chargeTell.locked), p:boss._chargeTell?boss._chargeTell.t/boss._chargeTell.dur:null, x:boss.x, lane:boss._chargeTell?boss._chargeTell.lane:(boss._chg&&boss._chg.lane), y:boss.y, err:window.__err||null})")

        fight = page.evaluate("() => window.__fight(1, 'boss', 'yuri')")
        ok(fight.get('ok'), 'native Stage-1 boss route opens in Chromium')
        page.evaluate("""() => {
          stagePlan=[]; enemies=[]; eBullets=[]; pBullets=[]; particles=[]; story=null; dlgBox=function(){};
          playerHit=function(){}; player.x=240; player.y=430; player.invuln=0;
        }""")
        for _ in range(100):
            if page.evaluate("() => boss && !boss.enter && boss.y > 0"):
                break
            step(6)
        # Decode all three authored FOV and alert colors before measuring their actual draw.
        page.evaluate("() => { l23FovWarm(); ['ovbody_intact','ovrotor_00'].forEach(k=>XART.rdy(k)); }")
        for _ in range(180):
            ready = page.evaluate("() => ['bmfx_fov_green_tall','bmfx_fov_yellow_tall','bmfx_fov_red_tall','bmfx_alert_green_danger','bmfx_alert_yellow_danger','bmfx_alert_red_danger','ovbody_intact'].every(k=>XART.rdy(k))")
            if ready:
                break
            page.wait_for_timeout(35)
        ok(ready, 'all authored FOV, alert and Overlord plates decode before the attack')

        page.evaluate("() => { boss.x=240; boss.y=112; boss._drawY=112; boss._ovState='fight'; boss._ovChargeCd=999; boss.fireCd=999; boss.hp=boss.maxhp; player.x=240; ovStartChargeTell(boss); }")
        step(10)
        green = capture('overlord_charge_green')
        step(38)
        yellow = capture('overlord_charge_yellow_locked')
        page.evaluate('() => { player.x=390; }')
        step(20)
        red = capture('overlord_charge_red_committed')
        step(50)
        dash = capture('overlord_charge_dash')
        details.update({'fight': fight, 'green': green, 'yellow': yellow, 'red': red, 'dash': dash})

        def saw(snapshot, kind, phase):
            return any(x.get('type') == kind and x.get('phase') == phase and x.get('drawn') for x in snapshot['blits'])
        ok(green['state'] == 'chargeTell' and green['p'] < 1/3 and saw(green, 'fov', 'green'),
           'early tracking draws the authored green FOV')
        ok(yellow['state'] == 'chargeTell' and yellow['locked'] and 1/3 <= yellow['p'] < 2/3 and saw(yellow, 'fov', 'yellow'),
           'the attack locks its lane during the authored yellow FOV')
        ok(red['state'] == 'chargeTell' and red['locked'] and red['p'] >= 2/3 and saw(red, 'fov', 'red'),
           'the committed lane turns authored red immediately before release')
        ok(any(saw(q, 'alert', phase) for q, phase in [(green,'green'),(yellow,'yellow'),(red,'red')]),
           'the matching authored overhead alert is visible during the warning')
        ok(dash['state'] == 'chargeOff' and abs(dash['x'] - dash['lane']) < .01 and dash['y'] > red['y'] + 24,
           'the released helicopter charges down the exact warned lane')

        for path in shots:
            im = Image.open(path).convert('RGB')
            ok(im.size == (960, 1024) and im.getbbox() is not None, f'{path.stem} is a non-empty native game frame')
        ok(not errors and not any(x.get('err') for x in [green,yellow,red,dash]),
           'zero Chromium page, console or controlled-loop errors')
        browser.close()
    server.shutdown()

    result = {'checks': checks, 'errors': errors, 'details': details, 'shots': [str(p.relative_to(ROOT)) for p in shots]}
    (OUT / 'results.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
    passed = sum(x['pass'] for x in checks)
    print(f'{passed} passed / {len(checks)-passed} failed', flush=True)
    if passed != len(checks):
        raise SystemExit(1)

if __name__ == '__main__':
    main()
