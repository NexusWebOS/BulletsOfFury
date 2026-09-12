#!/usr/bin/env python3
"""
probe_scene_0911a.py - THE SCENE DIRECTOR, DRIVEN IN THE REAL ENGINE (drop 0911a).

    python3 _BUILD_SOURCE/probe_scene_0911a.py --out /tmp/scene

Through the boss-mode host: attaches an authored scene to the live stage-2 boss and proves
  1. a track moves the hull through its keys on the grid (horizontal, diagonal, then a spin)
  2. the rotation keyed on the scene reaches the drawn pose (shipBossVisualPose)
  3. a fire action on a key puts rounds into eBullets from the named anchor, in the shape asked
  4. a SAFE zone removes enemy rounds that enter it; an ATTACK zone with a FOV telegraph blits
     the pack's cone; a BOSS zone fences the engine's own manoeuvre once the track is done
  5. `ownFire:false` keeps the engine's own patterns quiet
  6. the snapshot reports the scene state the editor reads
"""
import sys, os, argparse, base64, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import shoot

SCENE = {
  "schema":"bof-bossscene/1", "grid":{"cell":32}, "ownFire":False,
  "tracks":[{"name":"opening","trigger":{"type":"start"},"mode":"once","speed":1,
    "keys":[
      {"x":3,"y":4,"rot":0,"t":0.6,"ease":"inout","hold":0.35},
      {"x":12,"y":4,"rot":0,"t":0.8,"ease":"inout","hold":0.35,"actions":[{"type":"fire","shape":"fan","n":5,"spread":50,"speed":3,"anchor":"C"}]},
      {"x":7.5,"y":8,"rot":0,"t":0.7,"ease":"inout","hold":0.35,"actions":[{"type":"fire","shape":"radial","n":8,"speed":2.5,"anchor":"C","flash":"bpfx_muzzle_kinetic"}]},
      {"x":7.5,"y":8,"rot":360,"t":1.0,"ease":"linear","hold":0.3}
    ]}],
  "zones":[
    {"name":"safe","type":"safe","x":1,"y":13,"w":4,"h":2,"enforce":True,"fizzle":False},
    {"name":"kill","type":"attack","x":5,"y":9,"w":5,"h":3,"telegraph":"fov","anchor":"C"},
    {"name":"box","type":"boss","x":4,"y":2,"w":7,"h":3}
  ]
}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--out', default='/tmp/scene'); a=ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    from playwright.sync_api import sync_playwright
    port, stop = shoot.serve(shoot.GAME); errs=[]; fails=[]; n_ok=[0]
    def ok(c,m):
        if c: n_ok[0]+=1; print('  ok  ',m)
        else: fails.append(m); print('  FAIL',m)
    with sync_playwright() as p:
        b=p.chromium.launch(args=['--disable-gpu','--no-sandbox','--mute-audio'])
        pg=b.new_page(viewport={'width':1100,'height':1200}); pg.on('pageerror', lambda e: errs.append('pageerror: '+str(e)[:200]))
        pg.on('console', lambda m: errs.append('console.error: '+m.text[:200]) if m.type=='error' else None)
        pg.goto(f'http://127.0.0.1:{port}/index.html?bossmode=1', wait_until='load', timeout=60000)
        pg.wait_for_function("() => window.BOSSMODE && BOSSMODE.state==='bmhost'", timeout=60000)
        pg.evaluate(shoot.TRAP_RAF); pg.wait_for_timeout(50)
        def step(n):
            while n>0:
                k=min(60,n); e=pg.evaluate(shoot.STEP,k)
                if e: fails.append('step threw '+e); print('  step threw', e); return
                pg.wait_for_timeout(10); n-=k
        def J(expr): return pg.evaluate('() => ('+expr+')')
        def grab(name):
            d=pg.evaluate("() => document.getElementById('screen').toDataURL('image/png')")
            open(os.path.join(a.out,name),'wb').write(base64.b64decode(d.split(',',1)[1]))
        # the stage-2 boss, cole, no recording
        pg.evaluate("() => BOSSMODE.start(2,'boss','cole')")
        for i in range(40):
            step(30)
            if J("BOSSMODE.snapshot().bossActive && BOSSMODE.snapshot().boss && !BOSSMODE.snapshot().boss.enter"): break
        ok(J("bossActive && boss && boss._ship==='infernoreaver'"), 'stage-2 boss up and entered')
        pg.evaluate("() => { player.invuln=1e9; }")
        # attach the scene to the live boss
        ok(J("BOSSMODE.scene.attach("+json.dumps(SCENE)+")"), 'scene attached to the live boss')
        ok(J("boss._scene && boss._scene.def.tracks.length===1 && boss._scene.zones.length===3"), 'director holds one track and three zones')
        step(2)
        s=J("BOSSMODE.scene.state()")
        ok(s and s['trackName']=='opening', 'the start-triggered track went live: %s' % (s and s['trackName']))
        # the keyed flash family must be decoded before the key that fires it - sceneWarm touched it at attach
        pg.wait_for_function("() => XART.rdy('bpfx_muzzle_kinetic_0')", timeout=8000)
        ok(True, 'the keyed muzzle family was warmed at attach (rdy after a real wait)')
        # key 1: x=3 tiles -> 96px, y=4 -> 128px, reached at 0.6s and HELD 0.35s: sample inside the hold
        step(42)
        x,y=J("[boss.x,boss.y]")
        ok(abs(x-96)<3 and abs(y-128)<3, 'key 1 reached on the grid: boss at (%.0f,%.0f) for tiles (3,4) @32' % (x,y))
        nb0=J("eBullets.length")
        # key 2: 0.35 hold + 0.8 run = 69 frames from key 1's arrival; sample inside key 2's hold
        step(66)   # 0.6 + 0.35 + 0.8 s = 105 frames after attach; sampled at 42 + 66 = 108, inside key 2's hold
        x,y=J("[boss.x,boss.y]"); nb=J("eBullets.length")
        ok(abs(x-384)<3 and abs(y-128)<3, 'key 2: horizontal run to (12,4) -> (%.0f,%.0f)' % (x,y))
        ok(nb-nb0>=5, 'the fan on key 2 put %d rounds in eBullets' % (nb-nb0))
        m=J("shipBossMount(boss,'C')")
        near=J("eBullets.filter(q=>Math.hypot(q.x-%f,q.y-%f)<40).length" % (m['x'],m['y']))
        ok(near>=3, '%d of them left from the C anchor (%.0f,%.0f)' % (near, m['x'], m['y']))
        fam=J("[...new Set(eBullets.map(q=>q._bfam))].join(',')")
        ok('magma' in fam, "and they carry the boss's own round family (%s) - kind:boss goes through _shipShot" % fam)
        # key 3: diagonal to (7.5,8) fires a radial 8 with a keyed muzzle flash. Step until the director
        # reports key 3 reached (kf===2 and inside its hold), then read the flash within its 0.16s life.
        for i in range(120):
            step(1)
            if J("boss._scene && boss._scene.kf===2 && boss._scene.fired[2]"): break
        step(2)
        x,y=J("[boss.x,boss.y]")
        ok(abs(x-240)<3 and abs(y-256)<3, 'key 3: diagonal to (7.5,8) -> (%.0f,%.0f)' % (x,y))
        ok(J("_navalFlashes.some(f=>f.fam==='bpfx_muzzle_kinetic')"), 'the keyed muzzle family flashed')
        # key 4: a full spin, rot 0 -> 360 over 1s: step to mid-spin (0.35 hold + 0.5s)
        step(21+30)
        rot=J("BOSSMODE.scene.state().rotDeg")
        ok(120<rot<240, 'mid-spin the scene rotation reads %.0f deg' % rot)
        pose=J("shipBossVisualPose(boss).rot*180/Math.PI")
        ok(abs(pose-rot)<1, 'and the drawn pose carries it (%.0f deg)' % pose)
        grab('01_spin.png')
        # attack zone telegraph: trap the FOV cone blit
        blits=J("(function(){ let n=0; const o=ctx.drawImage; ctx.drawImage=function(im){ if(im&&im.width===320&&im.height===320) n++; return o.apply(ctx,arguments); }; try{ drawWorld(1/60); }catch(e){} ctx.drawImage=o; return n; })()")
        ok(blits>=1, 'the attack zone draws the pack FOV cone (%d cone blits in one frame)' % blits)
        # safe zone: drop a round inside it and step once
        pg.evaluate("() => { eBullets.push({x:32*3,y:32*14,vx:0,vy:0,w:6,h:6,dmg:1,t:0,kind:'eshot'}); }")
        n_in=J("eBullets.filter(q=>q.x>=32&&q.x<=160&&q.y>=416&&q.y<=480&&!q.dead).length")
        step(2)
        n_after=J("eBullets.filter(q=>q.x>=32&&q.x<=160&&q.y>=416&&q.y<=480&&!q.dead).length")
        ok(n_in>=1 and n_after==0, 'a round inside the SAFE zone is removed (%d -> %d)' % (n_in, n_after))
        # ownFire:false kept the engine's own patterns quiet: every round so far came from the scene
        ok(J("boss.fireCd>=0.4"), "ownFire:false holds the engine's own cooldown up (fireCd=%.2f)" % J("boss.fireCd"))
        # finish the spin + hold, track done -> engine manoeuvre resumes inside the boss zone
        step(80)
        s=J("BOSSMODE.scene.state()")
        ok(s['done']==1 and s['trackName'] is None, 'the once-track finished and released the hull')
        step(120)
        x,y=J("[boss.x,boss.y]")
        ok(128<=x<=352+1 and 64<=y<=160+1, 'with no track live the BOSS zone (4,2 7x3) fences the manoeuvre: (%.0f,%.0f)' % (x,y))
        grab('02_fenced.png')
        # detach restores the fight
        ok(J("BOSSMODE.scene.detach() && boss._scene===null"), 'detach clears the scene')
        # snapshot carries it for the editor
        pg.evaluate("() => BOSSMODE.scene.attach("+json.dumps(SCENE)+")")
        snap=J("BOSSMODE.snapshot()")
        ok(snap.get('scene') and 'zones' in snap['scene'] and snap.get('worldW')>0, 'the snapshot reports the scene and the world width (%s)' % snap.get('worldW'))
        pal=J("BOSSMODE.scene.fx()")
        ok(len(pal['muzzle'])>=5 and len(pal['explode'])>=8 and len(pal['round'])>=10, 'the palette lists %d muzzle, %d explode, %d round families' % (len(pal['muzzle']),len(pal['explode']),len(pal['round'])))
        ok(len(J("BOSSMODE.scene.kinds()"))>=40, 'and %d FIRETYPES kinds' % len(J("BOSSMODE.scene.kinds()")))
        b.close()
    stop()
    print('\n%d ok / %d fail' % (n_ok[0], len(fails)))
    for f in fails: print('  FAIL', f)
    if errs:
        print('page errors (%d):' % len(errs))
        for e in errs[:10]: print('   ', e)
    sys.exit(1 if fails or errs else 0)

if __name__=='__main__':
    main()
