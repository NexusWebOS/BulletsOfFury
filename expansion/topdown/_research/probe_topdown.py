"""Real-Chromium probe for the Overdrive ground stages (Level 2, the tank).
   Serve the BulletsOfFury folder (the `bof` launch config, port 8712) and run:
       python probe_topdown.py [--port 8712] [--shots DIR]
   Every check drives the real page through real key events and the game's own step hook; page and
   console errors are counted, because a draw that throws is otherwise invisible."""
import argparse, json, os, sys
from playwright.sync_api import sync_playwright

ap = argparse.ArgumentParser(); ap.add_argument('--port', default='8712'); ap.add_argument('--shots', default='')
A = ap.parse_args()
URL = f'http://localhost:{A.port}/expansion/topdown/index.html'
OK, FAIL = [], []
def check(name, cond, info=''):
    (OK if cond else FAIL).append(name); print(('ok   ' if cond else 'FAIL ') + name + ('  ' + str(info) if info else ''))

PRESS = "window.press=(k,d)=>window.dispatchEvent(new KeyboardEvent(d?'keydown':'keyup',{key:k}));"
FRESH = """() => { TDGAME.start(); TD.Stealth.reset(); TD.Stealth.alerts = 0; return true; }"""

with sync_playwright() as pw:
    br = pw.chromium.launch(); pg = br.new_page(viewport={'width': 1000, 'height': 760})
    errors = []
    pg.on('pageerror', lambda e: errors.append('pageerror: ' + str(e)))
    pg.on('console', lambda m: errors.append('console: ' + m.text) if m.type == 'error' else None)
    pg.on('response', lambda r: errors.append('404: ' + r.url) if r.status >= 400 else None)
    pg.goto(URL); pg.evaluate(PRESS)
    pg.evaluate('TDGAME.freeze()')
    pg.wait_for_function('window.ART && ART.progress(["nst4b_master","tk3_inta_n","rzb_hull_0","bmfx_fov_green_wide","logo","bmbar_frame_boss"]) >= 1 || (TDGAME.G.t > 0)', timeout=30000)
    for _ in range(20):
        pg.evaluate('TDGAME.step(60)'); pg.wait_for_timeout(150)
        if pg.evaluate('TDGAME.G.state') == 'title': break
    check('loads to the title', pg.evaluate('TDGAME.G.state') == 'title')
    if A.shots: os.makedirs(A.shots, exist_ok=True)
    def shot(name):
        if A.shots:
            pg.evaluate('TDGAME.render()'); pg.locator('#screen').screenshot(path=os.path.join(A.shots, name + '.png'))
    shot('01_title')
    # title -> brief -> play through real Enter presses
    pg.evaluate("press('enter',1)"); pg.evaluate('TDGAME.step(2)'); pg.evaluate("press('enter',0)"); pg.evaluate('TDGAME.step(60)')
    check('Enter opens the Level 2 briefing', pg.evaluate('TDGAME.G.state') == 'brief')
    pg.wait_for_timeout(400); pg.evaluate('TDGAME.step(60)'); shot('02_brief')
    pg.evaluate("press('enter',1)"); pg.evaluate('TDGAME.step(2)'); pg.evaluate("press('enter',0)"); pg.evaluate('TDGAME.step(2)')
    check('Enter deploys into play', pg.evaluate('TDGAME.G.state') == 'play')
    pg.wait_for_timeout(500); pg.evaluate('TDGAME.step(20)'); shot('03_play_start')

    r = pg.evaluate("""() => { const G=TDGAME.G; const y0=G.player.y; press('w',1); TDGAME.step(90); press('w',0); TDGAME.step(2);
      const x0=G.player.x; press('d',1); TDGAME.step(10); const dx10=G.player.x-x0; TDGAME.step(40); const dx50=G.player.x-x0; press('d',0); TDGAME.step(2);
      return {fwd:y0-G.player.y, dx10, dx50}; }""")
    check('the tank drives ~2 px a frame', 170 < r['fwd'] < 200, r)
    check('turn-then-move: no travel while the hull is still turning', abs(r['dx10']) < 0.5 and r['dx50'] > 40, r)

    r = pg.evaluate("""() => { TDGAME.start(); TD.Stealth.reset(); const G=TDGAME.G;
      const c=G.units.find(u=>u.type==='rifle'); c.wp=null; c.a=0; c.base=0; c.look=0;   // faces south down the road
      for(const o of G.units) if(o!==c) o.dead=true;
      G.player.x=c.x; G.player.y=c.y+150; G.player.inv=9999; const seq=[];
      for(let i=0;i<40;i++){ TDGAME.step(3); seq.push(c.mode); if(TD.Stealth.phase==='ALERT') break; }
      return {phase:TD.Stealth.phase, sawSuspect:seq.includes('suspect'), frames:seq.length*3}; }""")
    check('standing in a cone fills the meter: suspect, then ALERT', r['phase'] == 'ALERT' and r['sawSuspect'], r)

    r = pg.evaluate("""() => { TDGAME.start(); TD.Stealth.reset(); const G=TDGAME.G;
      const c=G.units.find(u=>u.type==='rifle'); c.wp=null; c.a=0; c.base=0; c.look=0; for(const o of G.units) if(o!==c) o.dead=true;
      G.player.x=150; G.player.y=3566; G.player.inv=9999; TDGAME.step(5);           // inside the south hedge
      const hidden=G.player.hidden; c.x=150; c.y=3566-150; TDGAME.step(120); return {hidden, phase:TD.Stealth.phase, aware:c.aware}; }""")
    check('a tank inside a hedge is hidden from a cone 150px away', r['hidden'] and r['phase'] == 'SNEAK', r)

    r = pg.evaluate("""() => { TDGAME.start(); TD.Stealth.reset(); const G=TDGAME.G; const c=G.units.find(u=>u.type==='rifle'); for(const o of G.units) if(o!==c) o.dead=true;
      TD.Stealth.raise(c, G.player, G.units); G.player.x=150; G.player.y=3566; G.player.inv=9999; const seen=[];
      for(let i=0;i<45;i++){ TDGAME.step(60); seen.push(TD.Stealth.phase); if(TD.Stealth.phase==='SNEAK') break; } return [...new Set(seen)]; }""")
    check('ALERT decays through EVASION and CAUTION back to SNEAK', r == ['ALERT', 'EVASION', 'CAUTION', 'SNEAK'], r)

    r = pg.evaluate("""() => { TDGAME.start(); TD.Stealth.reset(); const G=TDGAME.G; const u=G.units.find(x=>x.type==='heavy'); for(const o of G.units) if(o!==u) o.dead=true;
      u.wp=null; u.a=Math.PI; u.base=Math.PI; u.look=Math.PI; G.player.x=u.x; G.player.y=u.y+110; G.player.a=Math.PI; G.player.inv=9999; G.player.canCd=0; TDGAME.step(2);
      const hp0=u.hp; press('k',1); TDGAME.step(1); press('k',0); TDGAME.step(10); return {hp0, hp1:u.hp, msgs:G.msgs.map(m=>m.text)}; }""")
    check('a cannon shell on an unaware tank is a SNEAK STRIKE (double damage)', r['hp0'] - r['hp1'] >= 12 and 'SNEAK STRIKE' in r['msgs'], r)

    r = pg.evaluate("""() => { TDGAME.start(); const G=TDGAME.G; for(const o of G.units) o.dead=true; G.player.inv=9999; const res={};
      for(const id of ['vulcan','crash','laser','homing']) for(let lv=1;lv<=3;lv++){ G.player.weapons=[{id,lv}]; G.player.wi=0; G.player.fireCd=0; const n0=G.shots.length; press('j',1); TDGAME.step(1); press('j',0); res[id+lv]=G.shots.length-n0; TDGAME.step(30); }
      return res; }""")
    check('all four Hard Corps weapons fire at every level', all(v >= 1 for v in r.values()) and r['vulcan3'] == 3 and r['homing3'] == 3, r)

    r = pg.evaluate("""() => { TD.World.smokes.push({x:400,y:3000,r:72,t:5,life:7}); const a=TD.World.los(400,2900,400,3100), b=TD.World.los(300,2900,300,3100); TD.World.smokes.length=0; return {smoke:a, clear:b}; }""")
    check('smoke blocks line of sight', r['smoke'] is False and r['clear'] is True, r)

    r = pg.evaluate("""() => { TDGAME.start(); const G=TDGAME.G; G.player.weapons=[{id:'vulcan',lv:1},{id:'laser',lv:2}]; G.player.wi=1; G.player.inv=0; G.player.hp=1;
      TD.hurtPlayer(G,2,G.player.x,G.player.y); const dead=G.player.dead; TDGAME.step(110); return {dead, lives:G.lives, alive:!G.player.dead, hp:G.player.hp, weapons:G.player.weapons.map(w=>w.id)}; }""")
    check('death respawns at the checkpoint and loses the held gun', r['dead'] and r['alive'] and r['lives'] == 2 and r['weapons'] == ['vulcan'], r)

    # the boss
    r = pg.evaluate("""() => { TDGAME.start(); const G=TDGAME.G; for(const u of G.units) u.dead=true; G.player.x=400; G.player.y=690; TDGAME.step(5); return !!G.boss; }""")
    check('crossing the plaza line starts the Razorback', r)
    seen = set()
    # the attack picker is random: sample every 6 frames (not every 30) so a short rack is not missed between looks
    for i in range(40):
        seen.update(pg.evaluate("() => { const G=TDGAME.G, s=new Set(); for (let k=0;k<5;k++){ G.player.inv=9999; TDGAME.step(6); s.add(G.boss.state); } return [...s]; }"))
        if i == 10: pg.wait_for_timeout(300); shot('04_boss')
    for i in range(60):
        if {'drive', 'cannon', 'rack'} <= seen: break
        seen.update(pg.evaluate("() => { const G=TDGAME.G, s=new Set(); for (let k=0;k<10;k++){ G.player.inv=9999; TDGAME.step(6); s.add(G.boss.state); } return [...s]; }"))
    check('the boss runs its attack cycle', {'drive', 'cannon', 'rack'} <= seen, sorted(seen))
    r = pg.evaluate("""() => { const G=TDGAME.G, B=G.boss; const cam=TD.Cam; return {bossOnScreen: B.y > cam.y - 20 && B.y < cam.y + TD.VH + 20, playerOnScreen: G.player.y > cam.y && G.player.y < cam.y + TD.VH}; }""")
    check('the camera frames both the player and the boss', r['bossOnScreen'] and r['playerOnScreen'], r)
    r = pg.evaluate("""() => { const G=TDGAME.G, B=G.boss; const h0=B.parts.hull; const q=B.world(0,-112); B.hit(q.x,q.y,4,10); const shielded=h0-B.parts.hull;
      B.parts.turret=0.1; B.hit(B.x,B.y,4,1); const h1=B.parts.hull; const q2=B.world(0,-112); B.hit(q2.x,q2.y,4,10); return {shielded, exposed:h1-B.parts.hull}; }""")
    check('the hull takes 15% until the turret falls, then full damage', abs(r['shielded'] - 1.5) < 0.01 and abs(r['exposed'] - 10) < 0.01, r)
    seen = set()
    # the attack picker is random: sample every 6 frames over 20 s, or a nova can fall between looks
    seen.update(pg.evaluate("() => { const G=TDGAME.G, s=new Set(); for (let i=0;i<200;i++){ G.player.inv=9999; TDGAME.step(6); s.add(G.boss.state); } return [...s]; }"))
    check('without its turret the Razorback fires the sonic nova', 'nova' in seen and 'cannon' not in seen, sorted(seen))
    r = pg.evaluate("""() => { const G=TDGAME.G, B=G.boss; B.parts.hull=1; B.hit(B.x,B.y,4,10); for(let i=0;i<12;i++) TDGAME.step(30); return {state:G.state, rank:G.results&&G.results.rank, wrecked:B.wrecked}; }""")
    check('killing the hull ends in MISSION COMPLETE with a rank plate', r['state'] == 'clear' and r['wrecked'] and r['rank'], r)
    pg.wait_for_timeout(400); pg.evaluate('TDGAME.step(240)'); shot('05_results')
    check('no page or console errors', not errors, errors[:5])
    br.close()
print(f'\n{len(OK)} ok / {len(FAIL)} fail')
sys.exit(1 if FAIL else 0)
