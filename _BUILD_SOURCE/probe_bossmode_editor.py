#!/usr/bin/env python3
"""
probe_bossmode_editor.py - DRIVE bossmode.html IN REAL CHROMIUM (drop 0910a).

    python3 _BUILD_SOURCE/probe_bossmode_editor.py --out /tmp/bm

Proves the editor against the real engine in its iframe:
  1. the pack UI loads, the boot splash clears once the host reaches bmhost
  2. the boss list is built from the engine's own fight table (18 fights)
  3. opening a fight fills the inspector from SHIPBOSS + shows its plate with anchors
  4. editing a field and APPLY changes the engine's live row (override.get) and persists
  5. PLAY TEST starts the fight in the iframe; telemetry reads the boss; the edit is on the boss
  6. STOP TEST returns the host to bmhost; CANCEL reverts the row to stock
  7. EXPORT produces a schema'd .json; IMPORT of that file applies it back
"""
import os, sys, argparse, base64, json, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import shoot

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--out', default='/tmp/bm'); a=ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    from playwright.sync_api import sync_playwright
    port, stop = shoot.serve(shoot.GAME)
    errs=[]; fails=[]; n_ok=[0]
    def ok(c,m):
        if c: n_ok[0]+=1; print('  ok  ',m)
        else: fails.append(m); print('  FAIL',m)
    with sync_playwright() as p:
        b=p.chromium.launch(args=['--disable-gpu','--no-sandbox','--mute-audio'])
        pg=b.new_page(viewport={'width':1600,'height':1000}, accept_downloads=True)
        pg.on('pageerror', lambda e: errs.append('pageerror: '+str(e)[:200]))
        pg.on('console', lambda m: errs.append('console.error: '+m.text[:200]) if m.type=='error' else None)
        pg.goto(f'http://127.0.0.1:{port}/bossmode.html', wait_until='load', timeout=60000)
        def shot(n): pg.screenshot(path=os.path.join(a.out,n))
        pg.wait_for_timeout(1500); shot('01_boot.png')
        try:
            pg.wait_for_function("() => document.getElementById('boot').classList.contains('gone')", timeout=60000); ok(True,'boot splash cleared: engine reached bmhost')
        except Exception: ok(False,'boot never cleared: '+pg.evaluate("() => document.getElementById('host-txt').textContent"))
        pg.wait_for_timeout(800); shot('02_editor.png')
        n=pg.evaluate("() => document.querySelectorAll('#list-groups .li').length")
        ok(n>=18, 'boss list built from the engine: %d rows' % n)
        # open stage 2 boss (MAGMA WARD = infernoreaver row) via the list
        pg.evaluate("() => { const li=[...document.querySelectorAll('#list-groups .li')].find(e=>e.textContent.includes('MAGMA WARD')); li.click(); }")
        pg.wait_for_timeout(300)
        name=pg.evaluate("() => document.querySelector('#insp [data-f=name]').value")
        ok(name=='MAGMA WARD', 'inspector filled from SHIPBOSS: name=%s' % name)
        anchors=pg.evaluate("() => [...document.querySelectorAll('#insp [data-anch-name]')].map(e=>e.value)")
        ok(set(anchors)=={'L','C','R'}, 'anchors from mounts: %s' % anchors)
        pats=pg.evaluate("() => [...document.querySelectorAll('#insp select[data-f^=\"actions.pats.\"]')].map(e=>e.value)")
        ok(pats==['magmaflame','magmaflamelaser','magmafireball','magmafireshield'], 'pats as phases: %s' % pats)
        # plate tab renders the plate + anchors
        pg.click('#tabs .tab[data-tab=plate]'); pg.wait_for_timeout(1500); shot('03_plate.png')
        pv=pg.evaluate("() => { const c=document.getElementById('plate'); const x=c.getContext('2d'); const d=x.getImageData(0,0,c.width,c.height).data; let n=0; for(let i=3;i<d.length;i+=4) if(d[i]>0) n++; return n; }")
        ok(pv>20000, 'plate canvas has ink: %d px' % pv)
        # edit + apply: name + cooldown, through the inspector
        pg.click('#tabs .tab[data-tab=stage]')
        pg.fill('#insp [data-f=name]', 'MAGMA WARD TEST'); pg.dispatch_event('#insp [data-f=name]','change')
        pg.fill('#insp [data-f="actions.cd"]', '0.5'); pg.dispatch_event('#insp [data-f="actions.cd"]','change')
        pg.click('#e-apply'); pg.wait_for_timeout(200)
        ov=pg.evaluate("() => document.getElementById('host').contentWindow.BOSSMODE.override.get('infernoreaver')")
        ok(ov and ov['name']=='MAGMA WARD TEST' and abs(ov['cd']-0.5)<1e-9, 'APPLY wrote the override into the engine: %s' % (ov and {k:ov[k] for k in ('name','cd')}))
        live=pg.evaluate("() => document.getElementById('host').contentWindow.BOSSMODE.override.live('infernoreaver').name")
        ok(live=='MAGMA WARD TEST', 'and the live SHIPBOSS row carries it: %s' % live)
        st=pg.evaluate("() => JSON.parse(document.getElementById('host').contentWindow.localStorage.getItem('bof_bossmode')||'{}')")
        ok('infernoreaver' in st, 'persisted to the game\'s localStorage store')
        # play test
        pg.click('#b-play')
        try:
            pg.wait_for_function("() => { const s=document.getElementById('host').contentWindow.BOSSMODE.snapshot(); return s.bossActive && s.boss; }", timeout=20000); ok(True,'PLAY TEST spawned the boss in the iframe')
        except Exception: ok(False,'PLAY TEST never spawned a boss')
        pg.wait_for_timeout(1200); shot('04_playtest.png')
        s=pg.evaluate("() => document.getElementById('host').contentWindow.BOSSMODE.snapshot()")
        ok(s['boss']['name']=='MAGMA WARD TEST' and s['fight']['stage']==2 and s['fight']['role']=='boss', 'the edited row is what fights: %s S%s %s' % (s['boss']['name'], s['fight']['stage'], s['fight']['role']))
        tele=pg.evaluate("() => document.getElementById('tele-hp-txt').textContent+' | '+document.getElementById('tf-boss').textContent")
        ok('MAGMA WARD TEST' in tele and '/' in tele, 'telemetry bar reads the boss: %s' % tele)
        ovpx=pg.evaluate("() => { const c=document.getElementById('stage-overlay'); if(c.width<10) return 0; const d=c.getContext('2d').getImageData(0,0,c.width,c.height).data; let n=0; for(let i=3;i<d.length;i+=4) if(d[i]>0) n++; return n; }")
        ok(ovpx>50, 'anchor overlay drawn over the live stage: %d px' % ovpx)
        # kill + stop
        pg.click('#t-kill'); pg.wait_for_timeout(300)
        pg.click('#b-stop')
        try:
            pg.wait_for_function("() => document.getElementById('host').contentWindow.BOSSMODE.state==='bmhost'", timeout=15000); ok(True,'STOP TEST returned the host to bmhost')
        except Exception: ok(False,'host did not return: '+pg.evaluate("() => document.getElementById('host').contentWindow.BOSSMODE.state"))
        # export -> json
        with pg.expect_download() as dl:
            pg.click('#b-export')
        path=dl.value.path(); j=json.load(open(path))
        ok(j['schema']=='bof-bossmode/1' and j['kind']=='infernoreaver' and j['name']=='MAGMA WARD TEST', 'EXPORT wrote a schema\'d doc: %s' % dl.value.suggested_filename)
        # cancel reverts
        pg.click('#e-cancel'); pg.wait_for_timeout(200)
        live=pg.evaluate("() => document.getElementById('host').contentWindow.BOSSMODE.override.live('infernoreaver').name")
        ok(live=='MAGMA WARD', 'CANCEL reverted the row to stock: %s' % live)
        # import the exported file back
        pg.set_input_files('#file-in', path); pg.wait_for_timeout(400)
        live=pg.evaluate("() => document.getElementById('host').contentWindow.BOSSMODE.override.live('infernoreaver').name")
        ok(live=='MAGMA WARD TEST', 'IMPORT applied it again: %s' % live)
        pg.click('#e-cancel'); pg.wait_for_timeout(200)
        # graphics tab lists the boss's art
        pg.click('#tabs .tab[data-tab=graphics]'); pg.wait_for_timeout(2500); shot('05_graphics.png')
        g=pg.evaluate("() => document.querySelectorAll('#gfx-grid .gk').length")
        ok(g>=3, 'graphics browser lists %d keys for infernoreaver' % g)
        pg.click('#tabs .tab[data-tab=json]'); pg.wait_for_timeout(200)
        jl=pg.evaluate("() => document.getElementById('json').value.length")
        ok(jl>500, 'json pane shows the document (%d chars)' % jl)
        shot('06_json.png')
        b.close()
    stop()
    print('\n%d ok / %d fail' % (n_ok[0], len(fails)))
    for f in fails: print('  FAIL', f)
    if errs:
        print('page errors (%d):' % len(errs))
        for e in errs[:10]: print('   ', e)
    sys.exit(1 if fails else 0)

if __name__=='__main__':
    main()
