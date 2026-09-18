#!/usr/bin/env python3
"""
probe_fx_0918b.py - Mike's 0918b effects pass, in real Chromium.

  0. the reinstalled BURST strips never touch their cell edge (the "spliced and cut off" complaint), and the
     geyser strips carry no vent at the bottom (their base fades in from nothing);
  1. a STAGE-2 MOUNTAIN VENT warns, then erupts a HOSTILE fire column that hurts the player standing in it and
     throws five chunks of burning debris; a chunk falling on the player hurts;
  2. a HOSTILE ZONE COLUMN (a quarter of the screen) warns without hurting, then pours and hurts the player in
     its zone - and never the player in another zone;
  3. a FRIENDLY zone column (water / lightning) damages an enemy in its zone, and a level-V fire kill can raise one;
  4. the FURNACE TYRANT's flamethrower draws the fire geyser strip, and the boss pours a zone column;
  5. 0 page / console errors.
Frames: docs/proofs/fx_0918b/.
"""
import os, sys, base64, json
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.join(ROOT, '_BUILD_SOURCE'))
import shoot as sh
from PIL import Image
from playwright.sync_api import sync_playwright
OUT = os.path.join(ROOT, 'docs', 'proofs', 'fx_0918b')
FX = os.path.join(ROOT, 'assets', 'game', 'fx_0918')
N = {'ok': 0}; FAILS = []
def ok(c, m):
    if c: N['ok'] += 1; print('  ok   ' + m)
    else: FAILS.append(m); print('  FAIL ' + m)
ELEMS = ['fire','ice','lightning','prism','toxic','kinetic','water','chrome','dark']
KEYS = ['efx_geyser_fire','efx_geyser_water','efx_geyser_lightning','efx_burn','efx_debris_0','efx_debris_1']

def files():
    worst = {}
    for e in ELEMS:
        im = Image.open(os.path.join(FX, 'efx_burst_%s.png' % e)).convert('RGBA'); fw = im.width // 8; a = im.split()[3].load()
        m = 0
        for i in range(8):
            x0 = i * fw
            for t in range(fw):
                for (x, y) in ((x0+t, 0), (x0+t, im.height-1), (x0, t), (x0+fw-1, t)): m = max(m, a[x, y])
        worst[e] = m
    ok(max(worst.values()) <= 8, 'no burst frame touches its cell edge - worst edge alpha %s' % worst)
    base = {}
    for k in ['fire', 'water', 'lightning']:
        im = Image.open(os.path.join(FX, 'efx_geyser_%s.png' % k)).convert('RGBA'); a = im.split()[3].load()
        base[k] = max(a[x, y] for x in range(im.width) for y in range(im.height-3, im.height))
    ok(max(base.values()) <= 40, 'the geysers carry no vent - bottom 3 rows fade to nothing (max alpha %s)' % base)

def main():
    os.makedirs(OUT, exist_ok=True)
    files()
    port, stop = sh.serve(sh.GAME)
    with sync_playwright() as pw:
        br = pw.chromium.launch(args=['--disable-gpu', '--no-sandbox', '--mute-audio'])
        errs = []
        def watch(pg):
            pg.on('pageerror', lambda e: errs.append('page:' + str(e)[:200]))
            pg.on('console', lambda m: errs.append('console:' + m.text[:200]) if m.type == 'error' else None)
        # ======== A. a live stage 2
        pg = br.new_page(viewport={'width': 1000, 'height': 1100}); watch(pg)
        pg.goto('http://127.0.0.1:%d/index.html' % port, wait_until='load', timeout=90000)
        pg.wait_for_function("() => (window.__bofFrames|0) > 4", timeout=90000)
        pg.evaluate(sh.TRAP_RAF)
        pg.evaluate(sh.SETUP, {'state': 'PLAY', 'stage': 2, 'pilot': 'cole'})
        pg.evaluate("() => { window.__step=%s; window.__hits=0; window.playerHit=function(){ window.__hits++; }; }" % sh.STEP)
        def step(n): pg.evaluate("(n) => { for(let i=0;i<n;i++) window.__step(1); }", n)
        def shot(name):
            d = pg.evaluate("() => { const c=document.getElementById('screen'); return c?c.toDataURL('image/png'):null; }")
            if d: open(os.path.join(OUT, name + '.png'), 'wb').write(base64.b64decode(d.split(',', 1)[1]))
        pg.evaluate("(ks) => ks.forEach(k=>XART.rdy(k))", KEYS)
        for _ in range(40):
            if pg.evaluate("(ks) => ks.every(k=>XART.rdy(k))", KEYS): break
            pg.wait_for_timeout(250)
        ok(pg.evaluate("(ks) => ks.every(k=>XART.rdy(k))", KEYS), 'geysers, burn and both debris sprites decode')
        rec = "() => { window.__keys={}; const o=XART.get; window.__oget=o; XART.get=function(k){ window.__keys[k]=(window.__keys[k]|0)+1; return o.apply(this,arguments); }; }"
        unrec = "() => { XART.get=window.__oget; return window.__keys; }"
        calm = "() => { enemies.length=0; eBullets.length=0; s2VentT=999; s2Vents=[]; fireDebris=[]; zoneCols=[]; geysers=[]; window.__hits=0; }"

        # ---- 1. a mountain vent
        pg.evaluate(calm)
        v = pg.evaluate("() => { const L=camLeftX(); player.x=L+200; player.y=420; const v=s2VentSpawn(1,470); return {x:v.x,y:v.y,R:camRightX()}; }")
        pg.evaluate(rec); step(24); k = pg.evaluate(unrec)
        pre = pg.evaluate("() => ({hits:window.__hits, vents:s2Vents.length, geysers:geysers.length})")
        ok(pre['vents'] == 1 and pre['geysers'] == 0 and k.get('efx_burn', 0) > 0,
           'the vent WARNS first - fire starts in it, no column yet (%s, burn blits %d)' % (pre, k.get('efx_burn', 0)))
        shot('01_vent_warning')
        pg.evaluate("(v) => { player.x=v.x; player.y=v.y-160; }", v)
        step(36)   # the warning is 0.95 s = 57 frames; the eruption lands on frame 57
        e0 = pg.evaluate("() => ({hostile:geysers.filter(g=>g.hostile).length, debris:fireDebris.length})")
        ok(e0['hostile'] == 1 and e0['debris'] == 5, 'then erupts a HOSTILE fire column and throws five chunks of burning debris (%s)' % e0)
        pg.evaluate(rec); step(24); k = pg.evaluate(unrec)
        er = pg.evaluate("() => ({hits:window.__hits, h:Math.round((geysers[0]||{}).h||0)})")
        ok(er['h'] >= 300, 'the column rises to a section of the screen (%s px)' % er['h'])
        ok(er['hits'] > 0, 'the column burns the player standing in it (%d hits)' % er['hits'])
        ok((k.get('efx_debris_0', 0) + k.get('efx_debris_1', 0)) > 0, 'the debris draws from the generated sprites (%d blits)' % (k.get('efx_debris_0', 0) + k.get('efx_debris_1', 0)))
        pg.evaluate("() => { player.x=camLeftX()+180; player.y=440; }")
        step(10); shot('02_vent_eruption_debris')
        # the debris comes down on the player
        pg.evaluate(calm)
        pg.evaluate("() => { player.x=camLeftX()+320; player.y=400; const d=debrisLaunch(player.x,player.y-40,0,0); d.vx=0; }")
        step(140)
        dh = pg.evaluate("() => ({hits:window.__hits, left:fireDebris.length})")
        ok(dh['hits'] >= 1 and dh['left'] == 0, 'a chunk thrown up comes back DOWN on the player and hurts (%s)' % dh)
        # no vents while a boss is up / on another stage
        off = pg.evaluate("() => { const r=run.stage; run.stage=3; s2VentT=0; s2VentTick(1/60); const n3=s2Vents.length; run.stage=r; s2VentT=0; bossActive=true; s2VentTick(1/60); const nb=s2Vents.length; bossActive=false; return {n3,nb}; }")
        ok(off['n3'] == 0 and off['nb'] == 0, 'no vents off stage 2 or while the boss is up (%s)' % off)

        # ---- 2. hostile zone column
        pg.evaluate(calm)
        z = pg.evaluate("() => { const L=camLeftX(), R=camRightX(), w=(R-L)/4; player.x=L+w*1.5; player.y=380; const c=zoneColumnSpawn(zoneOf(player.x),'fire',true); return {i:c.i, w:Math.round(c.w), L, R}; }")
        ok(z['i'] == 1 and abs(z['w'] - (z['R'] - z['L']) / 4) < 1, 'a zone is a quarter of the screen (%s)' % z)
        step(30); shot('03_zone_warning')
        ok(pg.evaluate("() => window.__hits") == 0, 'the zone warns first and hurts nobody while it does')
        pg.evaluate(rec); step(50); k = pg.evaluate(unrec)   # warn 1.05 s = 63 frames
        zh = pg.evaluate("() => window.__hits")
        ok(zh > 0 and k.get('efx_geyser_fire', 0) > 0, 'then POURS DOWN the zone and hurts the player in it (%d hits)' % zh)
        shot('04_zone_pour')
        pg.evaluate(calm)
        pg.evaluate("() => { const L=camLeftX(), R=camRightX(), w=(R-L)/4; player.x=L+w*2.5; player.y=380; zoneColumnSpawn(0,'fire',true); }")
        step(150)
        ok(pg.evaluate("() => window.__hits") == 0, 'the player in ANOTHER zone is never touched')

        # ---- 3. friendly zone columns
        pg.evaluate(calm)
        fz = pg.evaluate("""() => { const L=camLeftX(), R=camRightX(), w=(R-L)/4; player.x=L+w*0.5; player.y=440;
            const e=spawnEnemy('drone', L+w*2.5, 220); if(!e) return null; e.shoots=false; e.hp=e.maxhp=400; window.__fe=e;
            window.__zh=0; const oh=window.hitEnemy; window.__ohe=oh; window.hitEnemy=function(t){ if(t===window.__fe) window.__zh++; return oh.apply(this,arguments); };
            window.__snap=()=>{ const o={}; for(const k in e) if(typeof e[k]==='number') o[k]=e[k]; return o; }; window.__s0=window.__snap();
            const cw=zoneColumnSpawn(2,'water',false); zoneColumnSpawn(3,'lightning',false); window.__fx=cw.x0+cw.w/2; return {hp:e.hp}; }""")
        pg.evaluate(rec)
        for _ in range(45):
            # the zone is fixed in WORLD space when it is called - the camera may move after; hold the unit there
            pg.evaluate("() => { const e=window.__fe; if(e){ e.vx=0; e.vy=0; e.y=220; e.x=window.__fx; } window.__step(1); }")
        k = pg.evaluate(unrec)
        zr = pg.evaluate("""() => { window.hitEnemy=window.__ohe; const a=window.__s0, b=window.__snap(), d={};
            for(const k in a) if(b[k]!==a[k] && !/^(x|y|vx|vy|t|_zoneT|flash|_efxAt|ang|_faceAng|spin)$/.test(k)) d[k]=[a[k],b[k]];
            return {calls:window.__zh, hp:window.__fe.hp, soaked:window.__fe._soaked||0, changed:d}; }""")
        print('  friendly:', json.dumps(zr))
        ok(zr['calls'] >= 2 and zr['soaked'] > 0 and (zr['hp'] < fz['hp'] or any('sh' in k.lower() for k in zr['changed'])),
           'a friendly WATER zone column hits the enemy in its zone and soaks it (%d hits, hp %s -> %s)' % (zr['calls'], fz['hp'], zr['hp']))
        ok(k.get('efx_geyser_water', 0) > 0 and k.get('efx_geyser_lightning', 0) > 0, 'water and lightning columns both draw their generated strips')
        shot('05_zone_friendly_water_lightning')
        trig = pg.evaluate("""() => { zoneCols=[]; zoneFriendlyAt=-99; run.infusion={elem:'fire',lv:5,hits:0};
            const e=spawnEnemy('drone', camLeftX()+100, 200); e.hp=0; const r=Math.random; Math.random=()=>0.01;
            try{ infusionOnHit(e,{_inf:'fire'},10); } finally { Math.random=r; }
            return zoneCols.map(c=>({k:c.kind,h:c.hostile})); }""")
        ok(trig and trig[0]['k'] == 'fire' and not trig[0]['h'], 'a level-V FIRE kill raises a friendly fire zone column (%s)' % trig)
        br_ = pg.evaluate("() => { const e=spawnEnemy('drone', camLeftX()+100, 200); e.hp=0; zoneCols=[]; const r=Math.random; Math.random=()=>0.01; try{ infusionOnHit(e,{_inf:'fire'},10); } finally { Math.random=r; } return zoneCols.length; }")
        ok(br_ == 0, 'and the next one waits out the %ss gap' % 4)
        pg.close()

        # ======== B. the Furnace Tyrant (Boss Mode, real rAF)
        pg = br.new_page(viewport={'width': 1100, 'height': 1000}); watch(pg)
        pg.goto('http://127.0.0.1:%d/index.html?bossmode=1' % port, wait_until='load', timeout=60000)
        pg.wait_for_function("() => window.BOSSMODE && window.BOSSMODE.ready", timeout=90000)
        fb = pg.evaluate("""async () => {
          const B=window.BOSSMODE, fr=()=>new Promise(r=>requestAnimationFrame(()=>r()));
          B.start(2,'boss','cole',false);
          let t0=performance.now();
          while(performance.now()-t0<40000 && !(typeof boss!=='undefined' && boss && boss._furnace && B.player && !B.player.dead)) await fr();
          if(!(boss&&boss._furnace)) return {err:'no furnace'};
          B.setInvuln(true); XART.rdy('efx_geyser_fire');
          window.__fk={}; const og=XART.get; XART.get=function(k){ window.__fk[k]=(window.__fk[k]|0)+1; return og.apply(this,arguments); };
          let flameShot=null, flameGeyser=0, flames=0; t0=performance.now();
          while(performance.now()-t0<45000){ await fr();
            const F=boss&&boss._fz; if(!F) break;
            if(F.beams.some(q=>q.kind==='flame')){ flames++; const g0=window.__fk['efx_geyser_fire']|0; await fr();
              if((window.__fk['efx_geyser_fire']|0)>g0) flameGeyser++;
              if(!flameShot && flames>20) flameShot=document.getElementById('screen').toDataURL('image/png');
              if(flames>40) break; } }
          const F=boss._fz; zoneCols=[]; F.zoneT=0.01; let zone=null, zoneShot=null; t0=performance.now();
          while(performance.now()-t0<6000){ await fr(); const c=zoneCols.find(c=>c.hostile);
            if(c){ zone={i:c.i,kind:c.kind}; if(c.t>c.warn+0.35){ zoneShot=document.getElementById('screen').toDataURL('image/png'); break; } } }
          XART.get=og;
          return {flames, flameGeyser, zone, flameShot, zoneShot};
        }""")
        print('  furnace:', json.dumps({k: v for k, v in fb.items() if 'Shot' not in k}))
        for key, name in (('flameShot', '06_furnace_flamethrower'), ('zoneShot', '07_furnace_zone_column')):
            if fb.get(key): open(os.path.join(OUT, name + '.png'), 'wb').write(base64.b64decode(fb[key].split(',', 1)[1]))
        ok(fb.get('flames', 0) > 0 and fb.get('flameGeyser', 0) > fb.get('flames', 0) * 0.5,
           "the Furnace's flamethrower draws the fire GEYSER strip (%s of %s flame frames)" % (fb.get('flameGeyser'), fb.get('flames')))
        ok(fb.get('zone') and fb['zone']['kind'] == 'fire', 'the Furnace pours a fire ZONE COLUMN (%s)' % fb.get('zone'))

        real = [e for e in errs if 'favicon' not in e and 'AudioContext encountered an error' not in e]
        ok(not real, 'page/console errors: %d %s' % (len(real), real[:3]))
        br.close()
    stop()
    print('\n%d ok / %d fail' % (N['ok'], len(FAILS)))
    for f in FAILS: print('  FAIL ' + f)
    sys.exit(1 if FAILS else 0)

if __name__ == '__main__':
    main()
