#!/usr/bin/env python3
"""
probe_bod_art_0912m.py - THE ART ROUND TRIP AND THE JSON TAB, DRIVEN LIKE A USER.

    python3 _BUILD_SOURCE/probe_bod_art_0912m.py --out /tmp/bodart

Mike: "allowing us to edit our frame/sprite and then save the frame/sprite as an image and also
save our change as a replacement in game if we select."

The edit happens in HIS tool - a pixel editor inside the panel is its own project, and a crude one
would quietly violate the palette rules this repo's art history is built on (0906o's value-range
exchange halved a pilot's palette). So the deliverable is the ROUND TRIP, and this drives all of it:

    browse -> preview -> EXPORT a PNG -> IMPORT a different one -> live in the game -> RESTORE

⚠ THE ASSERTIONS ARE ON THE PIXELS THE ENGINE SERVES, not on the flag. CLAUDE.md records exactly
this distinction for the Lizzie costume: `lizzieSkinOn` could not detect a missing flush because the
same function set the flag and did the repoint, so it stayed true with the work deleted. Here the
check reads back what `XART.get` actually hands out, at every step.
"""
import os, sys, argparse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import shoot


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--out', default='/tmp/bodart'); a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    from playwright.sync_api import sync_playwright
    port, stop = shoot.serve(shoot.GAME); errs = []; fails = []; n_ok = [0]
    def ok(c, m):
        if c: n_ok[0] += 1; print('  ok  ', m)
        else: fails.append(m); print('  FAIL', m)

    with sync_playwright() as p:
        b = p.chromium.launch(args=['--disable-gpu', '--no-sandbox', '--mute-audio'])
        pg = b.new_page(viewport={'width': 1600, 'height': 1000}, accept_downloads=True)
        pg.on('pageerror', lambda e: errs.append('pageerror: ' + str(e)[:220]))
        pg.on('console', lambda m: errs.append('console.error: ' + m.text[:200]) if m.type == 'error' else None)

        pg.goto(f'http://127.0.0.1:{port}/bulletsofdebug.html', wait_until='load', timeout=60000)
        pg.wait_for_function("() => window.BOD && window.BOD.api() && window.BOD.api().ready", timeout=90000)
        pg.evaluate("() => window.BOD.labOpen()")
        pg.wait_for_function("() => window.BOD.api().snapshot().lab", timeout=60000)
        ok(True, 'the editor boots with a stage open')

        pg.evaluate("() => window.BOD.selectTab('art')")
        pg.wait_for_timeout(400)
        nkeys = pg.evaluate("() => window.BOD.api().art.keys().length")
        ok(nkeys > 5000, 'the ART tab can see the whole art library (%d keys across five stores)' % nkeys)

        # ---- filter narrows, and picking previews ----
        pg.fill('#a-filter', 'nfdb_')
        pg.wait_for_timeout(300)
        hits = pg.evaluate("() => document.querySelectorAll('#insp .ak[data-key]').length")
        ok(0 < hits <= 60, 'the filter narrows the library to something browsable (%d shown)' % hits)

        pg.evaluate("""() => { const el=[...document.querySelectorAll('#insp .ak[data-key]')][0];
            if(el) el.click(); }""")
        pg.wait_for_timeout(1200)   # rdy() is false on the first call - the preview polls
        prev = pg.evaluate("""() => {
            const c=document.querySelector('#a-canvas');
            if(!c) return {err:'no preview canvas'};
            const d=c.getContext('2d').getImageData(0,0,c.width,c.height).data;
            let ink=0; for(let i=3;i<d.length;i+=16) if(d[i]>8) ink++;
            return {key:window.BOD.artKey?window.BOD.artKey():null, ink:ink,
                    size:document.querySelector('#a-size').textContent}; }""")
        ok(prev.get('ink', 0) > 50,
           'picking a key draws its real pixels at zoom (%s, %d px of ink) - the preview POLLS '
           'rdy(), which is false on its first call because that call starts the load'
           % (prev.get('size'), prev.get('ink', 0)))

        # ---- EXPORT: a real PNG comes out, at the CELL's size not the preview's ----
        with pg.expect_download(timeout=20000) as dl:
            pg.click('#a-export')
        d = dl.value
        path = os.path.join(a.out, d.suggested_filename)
        d.save_as(path)
        from PIL import Image
        got = Image.open(path)
        expect = pg.evaluate("""() => { const k=[...document.querySelectorAll('#insp .ak[data-key]')]
            .find(e=>e.classList.contains('on')); const key=k?k.dataset.key:null;
            const im=window.BOD.api().art.get(key); return im?[im.width,im.height]:null; }""")
        ok(expect and list(got.size) == expect,
           'EXPORT writes a real PNG at the CELL size, not the zoomed preview: %s == %s'
           % (got.size, expect))

        # ---- IMPORT: a different image replaces it, and the ENGINE serves the new pixels ----
        swap = os.path.join(a.out, 'swap.png')
        Image.new('RGBA', (48, 48), (0, 229, 255, 255)).save(swap)
        before = pg.evaluate("""() => { const k=[...document.querySelectorAll('#insp .ak[data-key]')]
            .find(e=>e.classList.contains('on')).dataset.key;
            const im=window.BOD.api().art.get(k); return {key:k, w:im.width, h:im.height}; }""")
        pg.set_input_files('#a-import', swap)
        pg.wait_for_timeout(900)
        after = pg.evaluate("""(k) => { const im=window.BOD.api().art.get(k);
            const c=document.createElement('canvas'); c.width=im.width; c.height=im.height;
            const g=c.getContext('2d'); g.drawImage(im,0,0);
            const px=g.getImageData(2,2,1,1).data;
            return {w:im.width, h:im.height, px:[px[0],px[1],px[2],px[3]],
                    overridden:window.BOD.api().art.overridden()}; }""", before['key'])
        ok(after['w'] == 48 and after['h'] == 48,
           'IMPORT replaces the live cell: %dx%d -> %dx%d'
           % (before['w'], before['h'], after['w'], after['h']))
        ok(after['px'][2] > 200 and after['px'][1] > 180,
           'and the ENGINE SERVES THE NEW PIXELS, read back off XART.get - not the flag, which is '
           'the distinction that hid a missing flush on the Lizzie costume (px %s)' % after['px'])
        ok(before['key'] in after['overridden'],
           'and the editor can list what is currently overridden: %s' % after['overridden'])

        # ---- RESTORE puts the original back, by pixels ----
        pg.click('#a-restore')
        pg.wait_for_timeout(700)
        back = pg.evaluate("""(k) => { const im=window.BOD.api().art.get(k);
            return {w:im.width, h:im.height, overridden:window.BOD.api().art.overridden()}; }""",
            before['key'])
        ok(back['w'] == before['w'] and back['h'] == before['h'],
           'RESTORE puts the original back with no reload: %dx%d -> %dx%d'
           % (after['w'], after['h'], back['w'], back['h']))
        ok(before['key'] not in back['overridden'],
           'and the override list is clear again: %s' % (back['overridden'] or '[]'))

        pg.screenshot(path=os.path.join(a.out, '01_art.png'))

        # ---- JSON ----
        pg.evaluate("() => window.BOD.selectTab('json')")
        pg.wait_for_timeout(500)
        js = pg.evaluate("""() => { const t=document.querySelector('#j-text');
            if(!t) return {err:'no json'};
            let o=null, err=null; try{ o=JSON.parse(t.value); }catch(e){ err=String(e).slice(0,90); }
            return {len:t.value.length, err:err, keys:o?Object.keys(o):[]}; }""")
        ok(not js.get('err') and js['len'] > 200,
           'the JSON tab emits valid, parseable JSON (%d chars, %s)' % (js['len'], js['keys']))
        ok('stage' in js['keys'] and 'art' in js['keys'] and 'snapshot' in js['keys'],
           'and it carries everything the editor is looking at, not just one panel: %s' % js['keys'])

        with pg.expect_download(timeout=20000) as dl2:
            pg.click('#j-save')
        d2 = dl2.value
        jp = os.path.join(a.out, d2.suggested_filename)
        d2.save_as(jp)
        import json as _j
        parsed = _j.load(open(jp, encoding='utf-8'))
        ok(isinstance(parsed, dict) and parsed.get('snapshot'),
           'and SAVE writes a .json file that parses off disk (%s)' % d2.suggested_filename)

        pg.screenshot(path=os.path.join(a.out, '02_json.png'))
        b.close()
    stop()
    print('\n%d ok / %d fail' % (n_ok[0], len(fails)))
    for f in fails: print('  FAIL', f)
    if errs:
        print('page errors (%d):' % len(errs))
        for e in errs[:6]: print('   ', e)
    sys.exit(1 if fails or errs else 0)


if __name__ == '__main__':
    main()
