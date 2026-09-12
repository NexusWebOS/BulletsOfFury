#!/usr/bin/env python3
"""
probe_scene_editor_0911a.py - THE SCENE TAB, DRIVEN WITH THE MOUSE (drop 0911a).

    python3 _BUILD_SOURCE/probe_scene_editor_0911a.py --out /tmp/scene_ed

Real Chromium on bossmode.html: opens the Magma Ward, goes to SCENE, lays three waypoints by
CLICKING the field, drags a SAFE zone, adds a FIRE action through the inspector, checks the doc's
scene is what the engine consumes, APPLYs it, PLAY TESTs, and reads the engine's scene state back
through the snapshot while the boss flies the path. Then the overlay on the live stage.
"""
import os, sys, argparse, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import shoot

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--out', default='/tmp/scene_ed'); a=ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    from playwright.sync_api import sync_playwright
    port, stop = shoot.serve(shoot.GAME); errs=[]; fails=[]; n_ok=[0]
    def ok(c,m):
        if c: n_ok[0]+=1; print('  ok  ',m)
        else: fails.append(m); print('  FAIL',m)
    with sync_playwright() as p:
        b=p.chromium.launch(args=['--disable-gpu','--no-sandbox','--mute-audio'])
        pg=b.new_page(viewport={'width':1600,'height':1000})
        pg.on('pageerror', lambda e: errs.append('pageerror: '+str(e)[:200]))
        pg.on('console', lambda m: errs.append('console.error: '+m.text[:200]) if m.type=='error' else None)
        missing=[]; pg.on('response', lambda r: missing.append(r.url.split(f':{port}/')[-1]) if r.status==404 else None)   # name the 404s, not just count them
        pg.goto(f'http://127.0.0.1:{port}/bossmode.html', wait_until='load', timeout=60000)
        pg.wait_for_function("() => document.getElementById('boot').classList.contains('gone')", timeout=60000)
        pg.wait_for_timeout(600)
        pg.evaluate("() => { const li=[...document.querySelectorAll('#list-groups .li')].find(e=>e.textContent.includes('MAGMA WARD')); li.click(); }")
        pg.wait_for_timeout(300)
        # a clean slate: any scene left in the store from a previous run must not leak in
        pg.evaluate("() => { const d=BM.state.doc; d.scene=null; BM.hooks.onDoc(d); }")
        pg.click('#tabs .tab[data-tab=scene]'); pg.wait_for_timeout(600)
        ok(pg.evaluate("() => document.getElementById('pane-scene').classList.contains('on') && !!document.getElementById('sc-cv')"), 'SCENE tab opens with the field canvas')
        ok(pg.evaluate("() => document.querySelectorAll('#sc-toolbtns .scb').length===6 && document.querySelectorAll('#sc-paths [data-path]').length>=12 && document.querySelectorAll('#sc-paths [data-man]').length>=8"), 'tools, path presets and maneuver presets are on the bar')
        pg.screenshot(path=os.path.join(a.out,'01_scene_empty.png'))
        # geometry: the canvas maps tiles
        g=pg.evaluate("() => { const c=document.getElementById('sc-cv'); const r=c.getBoundingClientRect(); return {x:r.left,y:r.top,w:r.width,h:r.height, scale:c.width/480}; }")
        cell=32*g['scale']
        def tile_xy(tx,ty): return (g['x']+tx*cell, g['y']+ty*cell)
        # WAYPOINT tool, three clicks: (3,4), (12,4), (7.5,8)
        pg.click('#sc-toolbtns .scb[data-tool=waypoint]')
        for tx,ty in [(3,4),(12,4),(7.5,8)]:
            x,y=tile_xy(tx,ty); pg.mouse.click(x,y); pg.wait_for_timeout(120)
        ks=pg.evaluate("() => BM.state.doc.scene.tracks[0].keys.map(k=>[k.x,k.y])")
        ok(ks==[[3,4],[12,4],[7.5,8]], 'three clicks laid three snapped waypoints: %s' % ks)
        # SAFE zone by drag: tiles (1,13) -> (5,15)
        pg.click('#sc-toolbtns .scb[data-tool=zsafe]')
        x0,y0=tile_xy(1,13); x1,y1=tile_xy(5,15)
        pg.mouse.move(x0,y0); pg.mouse.down(); pg.mouse.move(x1,y1, steps=8); pg.mouse.up(); pg.wait_for_timeout(150)
        z=pg.evaluate("() => BM.state.doc.scene.zones.map(z=>[z.type,z.x,z.y,z.w,z.h,z.enforce])")
        ok(len(z)==1 and z[0][0]=='safe' and z[0][1:5]==[1,13,4,2] and z[0][5]==True, 'a SAFE zone dragged on the grid: %s' % z)
        # ATTACK zone (5,9)->(10,12), then set its telegraph to the FOV cone through the inspector
        pg.click('#sc-toolbtns .scb[data-tool=zattack]')
        x0,y0=tile_xy(5,9); x1,y1=tile_xy(10,12)
        pg.mouse.move(x0,y0); pg.mouse.down(); pg.mouse.move(x1,y1, steps=8); pg.mouse.up(); pg.wait_for_timeout(150)
        pg.select_option('#sc-insp select[data-s=telegraph]', 'fov'); pg.wait_for_timeout(150)
        z=pg.evaluate("() => BM.state.doc.scene.zones.find(z=>z.type==='attack')")
        ok(z and z['telegraph']=='fov' and z['symbol']=='danger', 'an ATTACK zone with the FOV cone telegraph: %s' % ({k:z[k] for k in ('x','y','w','h','telegraph')} if z else None))
        # select waypoint 2 and add a FIRE action: fan-five from C
        pg.click('#sc-toolbtns .scb[data-tool=select]')
        x,y=tile_xy(12,4); pg.mouse.click(x,y); pg.wait_for_timeout(150)
        ok(pg.evaluate("() => BM.hooks.scene.state.selKey===1"), 'clicking waypoint 2 selects it')
        pg.click('#sc-insp [data-add=fire]'); pg.wait_for_timeout(150)
        pg.click('#sc-insp [data-shape=fan-five]'); pg.wait_for_timeout(150)
        act=pg.evaluate("() => BM.state.doc.scene.tracks[0].keys[1].actions[0]")
        ok(act and act['type']=='fire' and act['shape']=='fan' and act['n']==5 and act['kind']=='boss', 'FIRE action on key 2 via the pattern picker: %s' % act)
        # a spin on the last key via the MOVE preset
        x,y=tile_xy(7.5,8); pg.mouse.click(x,y); pg.wait_for_timeout(100)
        pg.click('#sc-paths [data-man=spin-clockwise]'); pg.wait_for_timeout(150)
        rots=pg.evaluate("() => BM.state.doc.scene.tracks[0].keys.map(k=>k.rot)")
        ok(len(rots)==5 and rots[-1]==360, 'spin-clockwise preset appended two rotation keys: %s' % rots)
        pg.screenshot(path=os.path.join(a.out,'02_scene_authored.png'))
        # the scene rides the patch, and APPLY lays it on the engine row
        pg.click('#e-apply'); pg.wait_for_timeout(250)
        ov=pg.evaluate("() => document.getElementById('host').contentWindow.BOSSMODE.override.get('infernoreaver')")
        ok(ov and ov.get('scene') and len(ov['scene']['tracks'][0]['keys'])==5 and len(ov['scene']['zones'])==2, 'APPLY put the scene on the override (5 keys, 2 zones)')
        ok(pg.evaluate("() => document.getElementById('host').contentWindow.BOSSMODE.override.live('infernoreaver').scene.tracks[0].keys.length===5"), 'and the live SHIPBOSS row carries it')
        # PLAY TEST: the engine attaches it at spawn and flies it
        pg.click('#b-play')
        pg.wait_for_function("() => { const s=document.getElementById('host').contentWindow.BOSSMODE.snapshot(); return s.bossActive && s.boss && !s.boss.enter && s.scene; }", timeout=25000)
        ok(True, 'PLAY TEST spawned the boss with the scene attached at init (snapshot.scene present)')
        pg.wait_for_timeout(2600)
        s=pg.evaluate("() => document.getElementById('host').contentWindow.BOSSMODE.snapshot()")
        ok(s['scene']['trackName']=='track 1' and s['scene']['kf']>=1, 'the director is walking the track in the real fight: key %s, t %.1fs' % (s['scene']['kf']+1, s['scene']['t']))
        pg.screenshot(path=os.path.join(a.out,'03_playtest_overlay.png'))
        ovpx=pg.evaluate("() => { const c=document.getElementById('stage-overlay'); if(c.width<10) return 0; const d=c.getContext('2d').getImageData(0,0,c.width,c.height).data; let n=0; for(let i=3;i<d.length;i+=4) if(d[i]>0) n++; return n; }")
        ok(ovpx>800, 'the STAGE overlay draws the path and zones over the live fight (%d px)' % ovpx)
        # the safe zone is enforced in the real engine
        r=pg.evaluate("() => { const w=document.getElementById('host').contentWindow; return w.BOSSMODE.snapshot().scene.zones; }")
        ok(any(q['name'].startswith('safe') and q['active'] for q in r), 'the SAFE zone is active in the engine')
        pg.click('#b-stop'); pg.wait_for_function("() => document.getElementById('host').contentWindow.BOSSMODE.state==='bmhost'", timeout=15000)
        # export carries the scene
        with pg.expect_download() as dl:
            pg.click('#b-export')
        j=json.load(open(dl.value.path()))
        ok(j.get('scene') and j['scene']['schema']=='bof-bossscene/1' and len(j['scene']['tracks'][0]['keys'])==5, 'EXPORT writes the scene into the fight document')
        # CANCEL reverts the row and clears the scene from the engine
        pg.click('#e-cancel'); pg.wait_for_timeout(200)
        ok(pg.evaluate("() => !document.getElementById('host').contentWindow.BOSSMODE.override.live('infernoreaver').scene"), 'CANCEL reverts: the shipped row has no scene')
        b.close()
    stop()
    if missing:
        from collections import Counter
        print('404s:'); [print('   %3d  %s' % (n,u)) for u,n in Counter(missing).most_common(10)]
    print('\n%d ok / %d fail' % (n_ok[0], len(fails)))
    for f in fails: print('  FAIL', f)
    if errs:
        print('page errors (%d):' % len(errs))
        for e in errs[:10]: print('   ', e)
    sys.exit(1 if fails or errs else 0)

if __name__=='__main__':
    main()
