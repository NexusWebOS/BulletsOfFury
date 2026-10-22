#!/usr/bin/env python3
"""
probe_stations_1021b.py - SCENE STATIONS + STARTER BOSSES, DRIVEN LIKE A USER (drop 1021b).

    python3 _BUILD_SOURCE/probe_stations_1021b.py --out /tmp/stations

Real Chromium on bossmode.html. Mike: "drag my boss onto positions in the scene, select an action where
I've placed him such as orbit, fly in, fly out, fly and fire". So this probe:
  - drags the BOSS chip onto the field (real HTML5 drag and drop) and picks ORBIT from the picker,
  - drops a second station with the STATION tool and picks CHARGE (a telegraph lane zone, OFF until armed),
  - drags station 1 and checks the built keys follow, changes a plain-language setting,
  - loads THE CHARGER template, APPLYs it, PLAY TESTs, and watches the real engine walk
    Entrance -> Teach, switch the lane telegraph on, and hand over to the 66% / 33% phases when the HP
    drops (the 1021b engine handoff: a looping phase used to own the boss for ever).
"""
import os, sys, argparse, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import shoot

H="document.getElementById('host').contentWindow"

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--out', default='/tmp/stations'); ap.add_argument('--bust', action='store_true', help='disable the 1021b handoff: the HP handovers must FAIL'); a=ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    from playwright.sync_api import sync_playwright
    port, stop = shoot.serve(shoot.GAME); errs=[]; fails=[]; n_ok=[0]
    def ok(c,m):
        if c: n_ok[0]+=1; print('  ok  ',m)
        else: fails.append(m); print('  FAIL',m)
    with sync_playwright() as p:
        b=p.chromium.launch(executable_path='/opt/pw-browsers/chromium', args=['--disable-gpu','--no-sandbox','--mute-audio'])
        pg=b.new_page(viewport={'width':1600,'height':1000})
        pg.on('pageerror', lambda e: errs.append('pageerror: '+str(e)[:200]))
        pg.on('console', lambda m: errs.append('console.error: '+m.text[:200]) if m.type=='error' else None)
        pg.goto(f'http://127.0.0.1:{port}/bossmode.html', wait_until='load', timeout=60000)
        pg.wait_for_function("() => document.getElementById('boot').classList.contains('gone')", timeout=60000)
        pg.wait_for_timeout(600)
        pg.evaluate("() => { const li=[...document.querySelectorAll('#list-groups .li')].find(e=>e.textContent.includes('INFERNO REAVER')); li.click(); }")
        pg.wait_for_timeout(300)
        pg.evaluate("() => { const d=BM.state.doc; d.scene=null; BM.hooks.onDoc(d); }")
        pg.click('#tabs .tab[data-tab=scene]'); pg.wait_for_timeout(700)
        ok(pg.evaluate("() => document.querySelectorAll('#sc-toolbtns .scb').length===7 && !!document.querySelector('#sc-toolbtns [data-tool=station]')"), 'the STATION tool is on the bar')
        ok(pg.evaluate("() => !!document.getElementById('sc-bosschip') && document.querySelectorAll('#sc-tpl option').length===4"), 'the BOSS drag chip and the three starter bosses are on the bar')
        g=pg.evaluate("() => { const c=document.getElementById('sc-cv'); const r=c.getBoundingClientRect(); return {x:r.left,y:r.top,w:r.width,h:r.height, scale:c.width/480}; }")
        cell=32*g['scale']
        def rel(tx,ty): return {'x':tx*cell, 'y':ty*cell}
        def abs_(tx,ty): return (g['x']+tx*cell, g['y']+ty*cell)
        # 1. drag the boss chip onto the field
        pg.drag_and_drop('#sc-bosschip', '#sc-cv', target_position=rel(5,4)); pg.wait_for_timeout(300)
        st=pg.evaluate("() => BM.state.doc.scene && BM.state.doc.scene.tracks[0] && BM.state.doc.scene.tracks[0].plan")
        ok(st and len(st)==1 and abs(st[0]['x']-5)<0.6 and abs(st[0]['y']-4)<0.6, 'dragging the boss onto the field made station 1 where he was dropped: %s' % (st and [st[0]['x'],st[0]['y']]))
        cards=pg.evaluate("() => [...document.querySelectorAll('#sc-picker .pk-card')].map(c=>[c.dataset.beh, c.querySelector('b').textContent, c.querySelector('i').textContent])")
        ok(len(cards)==17 and all(c[1] and len(c[2])>10 for c in cards), 'the picker opened beside him with %d actions, each a name and a plain sentence' % len(cards))
        ok({'flyin','flyout','orbit','flyfire','charge','spin','wall'}<=set(c[0] for c in cards), 'it offers FLY IN, FLY OUT, ORBIT, FLY & FIRE, CHARGE, SPIN & SPRAY, WALL ...')
        pg.screenshot(path=os.path.join(a.out,'01_picker.png'))
        pg.click('#sc-picker [data-beh=orbit]'); pg.wait_for_timeout(200)
        r=pg.evaluate("() => { const t=BM.state.doc.scene.tracks[0]; return {beh:t.plan[0].beh, keys:t.keys.length, tagged:t.keys.every(k=>k.st===t.plan[0].id), picker:!!document.getElementById('sc-picker')}; }")
        ok(r['beh']=='orbit' and r['keys']>=13 and r['tagged'] and not r['picker'], 'picking ORBIT built %d engine keys, all owned by the station, and closed the picker' % r['keys'])
        # 2. station tool -> CHARGE
        pg.click('#sc-toolbtns .scb[data-tool=station]')
        x,y=abs_(11,3); pg.mouse.click(x,y); pg.wait_for_timeout(250)
        pg.click('#sc-picker [data-beh=charge]'); pg.wait_for_timeout(200)
        r=pg.evaluate("""() => { const sc=BM.state.doc.scene, t=sc.tracks[0]; const s2=t.plan[1]; const z=sc.zones.find(z=>z.st===s2.id);
            const acts=t.keys.filter(k=>k.st===s2.id).flatMap(k=>k.actions||[]); return {n:t.plan.length, beh:s2.beh, zone:z&&{type:z.type,on:z.on,name:z.name},
            on:acts.some(a=>a.type==='zone'&&a.on===true), off:acts.some(a=>a.type==='zone'&&a.on===false)}; }""")
        ok(r['n']==2 and r['beh']=='charge', 'the STATION tool dropped station 2 and CHARGE was picked')
        ok(r['zone'] and r['zone']['type']=='attack' and r['zone']['on']==False and r['on'] and r['off'], 'CHARGE built its warning lane (an attack zone, OFF until armed) and the keys that switch it on and off: %s' % r['zone'])
        # 3. drag station 1, the built path follows
        pg.click('#sc-toolbtns .scb[data-tool=select]')
        before=pg.evaluate("() => BM.state.doc.scene.tracks[0].keys[0].x")
        x0,y0=abs_(5,4); x1,y1=abs_(7,6)
        pg.mouse.move(x0,y0); pg.mouse.down(); pg.mouse.move(x1,y1,steps=8); pg.mouse.up(); pg.wait_for_timeout(200)
        r=pg.evaluate("() => { const t=BM.state.doc.scene.tracks[0]; return {x:t.plan[0].x,y:t.plan[0].y,k0:t.keys[0].x, sel:BM.hooks.scene.state.selSt}; }")
        ok(abs(r['x']-7)<0.6 and abs(r['y']-6)<0.6 and abs(r['k0']-before-2)<0.6 and r['sel']==0, 'dragging station 1 moved it and rebuilt its keys (key 1 x %.2f -> %.2f)' % (before, r['k0']))
        # plain-language setting: laps 1 -> 2
        n1=pg.evaluate("() => BM.state.doc.scene.tracks[0].keys.length")
        pg.fill('#sc-insp .st-sec input[data-s="p.laps"]', '2'); pg.press('#sc-insp .st-sec input[data-s="p.laps"]', 'Enter'); pg.wait_for_timeout(200)
        n2=pg.evaluate("() => BM.state.doc.scene.tracks[0].keys.length")
        ok(n2==n1+12, 'HOW MANY LAPS 1 -> 2 rebuilt the orbit with 12 more keys (%d -> %d)' % (n1,n2))
        ok(pg.evaluate("() => /circle size/i.test(document.getElementById('sc-insp').textContent) && /Circles around this spot/.test(document.getElementById('sc-insp').textContent)"), 'the station inspector speaks plain language (CIRCLE SIZE, "Circles around this spot.")')
        pg.screenshot(path=os.path.join(a.out,'02_two_stations.png'))
        pg.mouse.click(g['x']+g['w']-6, g['y']+g['h']-6); pg.wait_for_timeout(150)   # empty field -> the plan list
        ok(pg.evaluate("() => { const t=document.querySelectorAll('#sc-insp .st-list li'); return t.length===2 && /ORBIT/.test(t[0].textContent) && /CHARGE/.test(t[1].textContent); }"), 'THE PLAN reads as a list of sentences')
        ok(pg.evaluate("() => /in plain words/.test(document.getElementById('sc-code').textContent)"), 'the sequence code carries the plain-words plan too')
        # 4. the Charger template, into the real engine
        pg.once('dialog', lambda d: d.accept())
        pg.select_option('#sc-tpl', '1'); pg.wait_for_timeout(300)
        t=pg.evaluate("() => BM.state.doc.scene.tracks.map(t=>({name:t.name, trig:t.trigger, mode:t.mode, n:t.keys.length, st:t.plan.length}))")
        ok(len(t)==4 and t[0]['trig']['type']=='start' and t[0]['mode']=='once' and t[1]['trig']['type']=='time' and t[2]['trig']=={'type':'hp','hp':0.66} and t[3]['trig']=={'type':'hp','hp':0.33}, 'THE CHARGER: entrance once, then phases at full HP / 66%% / 33%%: %s' % [(x['name'],x['n']) for x in t])
        ok(all(x['n']>0 for x in t), 'every phase was built into engine keys')
        pg.screenshot(path=os.path.join(a.out,'03_charger.png'))
        pg.click('#e-apply'); pg.wait_for_timeout(250)
        pg.evaluate(f"() => {{ {H}.BOSSMODE.tools.god=true; }}")
        pg.click('#b-play')
        pg.wait_for_function(f"() => {{ const s={H}.BOSSMODE.snapshot(); return (s.bossActive||s.subBossActive) && s.boss && !s.boss.enter && s.scene; }}", timeout=25000)
        seen=set(); lane=False
        for _ in range(70):
            s=pg.evaluate(f"() => {H}.BOSSMODE.snapshot().scene")
            if s and s.get('trackName'): seen.add(s['trackName'])
            if s and any(z['name'].startswith('lane-') and z.get('active') for z in s.get('zones',[])): lane=True
            if 'Teach: one ram' in seen and lane: break
            pg.wait_for_timeout(150)
        ok('Teach: one ram' in seen, 'the engine walked the entrance into "Teach: one ram" (%s)' % sorted(seen))
        ok(lane, 'the CHARGE lane telegraph switched on in the real fight')
        pg.screenshot(path=os.path.join(a.out,'04_playtest_charge.png'))
        if a.bust: pg.evaluate(f"() => {{ {H}.sceneHandsOver=function(){{ return false; }}; }}")
        pg.evaluate(f"() => {H}.BOSSMODE.tools.setHpFrac(0.6)")
        try:
            pg.wait_for_function(f"() => {{ const s={H}.BOSSMODE.snapshot().scene; return s && s.trackName==='Combine: ram + strafe'; }}", timeout=12000); h1=True
        except Exception: h1=False
        ok(h1, 'HP to 60%: the looping Teach phase handed over to "Combine: ram + strafe"')
        pg.evaluate(f"() => {H}.BOSSMODE.tools.setHpFrac(0.3)")
        try:
            pg.wait_for_function(f"() => {{ const s={H}.BOSSMODE.snapshot().scene; return s && s.trackName==='Test: double ram'; }}", timeout=12000); h2=True
        except Exception: h2=False
        ok(h2, 'HP to 30%: handed over to "Test: double ram"')
        pg.screenshot(path=os.path.join(a.out,'05_playtest_phase3.png'))
        pg.click('#b-stop'); pg.wait_for_function(f"() => {H}.BOSSMODE.state==='bmhost'", timeout=15000)
        pg.click('#e-cancel'); pg.wait_for_timeout(200)
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
