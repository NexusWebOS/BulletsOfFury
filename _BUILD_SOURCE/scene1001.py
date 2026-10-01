"""scene1001 - drive the real game through a scripted scene and grab frames along the way.

    python3 _BUILD_SOURCE/scene1001.py scene.js --out DIR [--steps 600] [--every 30]

scene.js is evaluated once after boot (TRAP_RAF already installed). It may define
window.__sceneTick(i) (called every frame before loop) and window.__sceneProbe() (returns a
JSON-able object recorded with each grab). Frames are stepped through shoot.STEP in chunks with a
real pause between chunks, so lazily loaded art decodes (CLAUDE.md: a synchronous burst never
decodes anything).
"""
import argparse, base64, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import shoot

GRAB = ("() => { const g=document.querySelector('#screen-area canvas')||document.querySelector('canvas');"
        " return g?g.toDataURL('image/png'):null; }")


def run(scene_js, out, steps=600, every=30, chunk=10, viewport=(1100, 1200)):
    os.makedirs(out, exist_ok=True)
    for f in os.listdir(out):
        if f.startswith('f_'):
            os.remove(os.path.join(out, f))
    from playwright.sync_api import sync_playwright
    port, stop = shoot.serve(shoot.GAME)
    errs, log = [], []
    with sync_playwright() as p:
        chrome = os.environ.get('BOF_CHROME', '/opt/pw-browsers/chromium-1194/chrome-linux/chrome')
        kw = {'executable_path': chrome} if os.path.exists(chrome) else {}
        b = p.chromium.launch(args=['--disable-gpu', '--no-sandbox', '--mute-audio'], **kw)
        pg = b.new_page(viewport={'width': viewport[0], 'height': viewport[1]}, device_scale_factor=1)
        pg.on('pageerror', lambda e: errs.append(str(e)[:300]))
        pg.on('console', lambda m: errs.append('console.' + m.type + ': ' + m.text[:200])
              if m.type == 'error' else None)
        pg.goto(f'http://127.0.0.1:{port}/index.html', wait_until='load', timeout=60000)
        pg.wait_for_function("() => typeof ASSETS!=='undefined' && typeof setState==='function'", timeout=45000)
        pg.wait_for_function("() => (window.__bofFrames|0) > 4", timeout=45000)
        pg.evaluate(shoot.TRAP_RAF)
        pg.wait_for_timeout(50)
        r = pg.evaluate("(src)=>{try{(0,eval)(src);return null}catch(e){return String(e&&e.stack||e)}}", scene_js)
        if r:
            print('scene threw:', r)
        step = ("(n)=>{for(let i=0;i<n;i++){try{if(window.__sceneTick)window.__sceneTick(window.__sceneI=(window.__sceneI|0)+1);}"
                "catch(e){return 'tick:'+String(e&&e.stack||e)}} return null}")
        for i in range(steps + 1):
            if i % every == 0:
                pr = pg.evaluate("()=>{try{return window.__sceneProbe?window.__sceneProbe():null}catch(e){return {err:String(e)}}}")
                d = pg.evaluate(GRAB)
                if d:
                    with open(os.path.join(out, 'f_%05d.png' % i), 'wb') as fh:
                        fh.write(base64.b64decode(d.split(',', 1)[1]))
                log.append({'i': i, 'probe': pr})
            e = pg.evaluate(step, 1)
            if e:
                errs.append(e)
            e = pg.evaluate(shoot.STEP, 1)
            if e:
                errs.append('step:' + e)
            if i % chunk == chunk - 1:
                pg.wait_for_timeout(15)   # a real pause so lazily loaded art can decode
        b.close()
    stop()
    json.dump({'log': log, 'errors': errs}, open(os.path.join(out, 'log.json'), 'w'), indent=1)
    return log, errs


def sheet(out, cols=6, thumb=300, name='sheet.png'):
    from PIL import Image
    fs = sorted(f for f in os.listdir(out) if f.startswith('f_'))
    if not fs:
        return None
    ims = [Image.open(os.path.join(out, f)).convert('RGB') for f in fs]
    w, h = ims[0].size
    tw, th = thumb, int(thumb * h / w)
    rows = (len(ims) + cols - 1) // cols
    c = Image.new('RGB', (cols * tw, rows * th))
    for k, im in enumerate(ims):
        c.paste(im.resize((tw, th)), ((k % cols) * tw, (k // cols) * th))
    p = os.path.join(out, name)
    c.save(p)
    return p


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('scene')
    ap.add_argument('--out', required=True)
    ap.add_argument('--steps', type=int, default=600)
    ap.add_argument('--every', type=int, default=30)
    ap.add_argument('--cols', type=int, default=6)
    a = ap.parse_args()
    log, errs = run(open(a.scene).read(), a.out, a.steps, a.every)
    print('frames', len(log), 'errors', len(errs))
    for e in errs[:10]:
        print('  ', e)
    print(sheet(a.out, a.cols))
    for L in log:
        print(L['i'], json.dumps(L['probe'])[:300])
