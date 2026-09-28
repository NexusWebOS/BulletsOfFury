#!/usr/bin/env python3
"""probe_chaingun_0928.py - Mike 0928, in real Chromium:
  "We never get to switch machine-gun to chaingun, nor does my machine-gun default to chaingun anymore
   after level 5 ... anchored chaingun attachments ... spin the barrels ... from stage 6 onward, we've got
   chaingun power baby. chaingun borrows the same elements from machine gun upgrades, just make the bullets
   go faster and appear like .50 cals and stronger with their own impact fx."
  + "When playing level 6, if I die or quit, the wind noise should stop."

Asserts behaviour through the live loop (TRAP_RAF + STEP, FIRE held through Input), identifies every draw by
its XART key, and saves a zoomed frame of the pods firing. Exit 1 on any failure.
"""
import os, sys, json, base64, http.server
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
http.server.SimpleHTTPRequestHandler.log_message = lambda *a: None
import shoot as sh
from playwright.sync_api import sync_playwright

OUT = os.path.join(sh.GAME, '_shots', 'opus0928', 'chaingun'); N = {'ok': 0}; FAILS = []
def ok(c, m):
    if c: N['ok'] += 1; print('  ok   ' + m, flush=True)
    else: FAILS.append(m); print('  FAIL ' + m, flush=True)

SETUP = r"""
(c) => {
  chaingunUnlocked=!!c.unlocked;
  diffKey='normal';DIFF=DIFFS.normal;run.mode='arcade';run.pilot=c.pilot||'maverick';run.stage=c.stage;curStage=STAGES[c.stage-1];
  beginStage(c.stage);setState(GS.PLAY);player.reset();story=null;special=null;s6Opening=null;s6Wing=null;
  stagePlan=[];waveIdx=999;spawnClock=9999;enemies=[];eBullets=[];pBullets=[];powerups=[];
  boss=null;bossActive=false;subBoss=null;subBossActive=false;subBossDone=true;
  run.weapon=0;run.wlevels=WEAPONS.map(()=>0);run.wlevels[0]=c.lv||2;run.wlevel=c.lv||2;run.forge={};run.infusion=null;
  run.loadout=[0,1,2,3,4,5];run._chainSeeded=false;
  player.x=camLeftX()+viewW()/2;player.y=VH*.78;player.invuln=0;
  window.playerHit=function(){};
  window.__asked={};if(!window.__xg){window.__xg=XART.get.bind(XART);XART.get=function(k){window.__asked[k]=(window.__asked[k]||0)+1;return window.__xg(k);};}
  return {weapon:run.weapon};
}
"""
def main():
    os.makedirs(OUT, exist_ok=True)
    port, stop = sh.serve(sh.GAME); errs = []
    with sync_playwright() as pw:
        br = pw.chromium.launch(args=['--no-sandbox', '--mute-audio'])
        pg = br.new_page(viewport={'width': 1000, 'height': 1100})
        pg.on('pageerror', lambda e: errs.append('page:' + str(e)[:200]))
        pg.on('console', lambda m: errs.append('console:' + m.text[:200]) if m.type == 'error' or 'draw error' in m.text else None)
        pg.goto('http://127.0.0.1:%d/index.html' % port, wait_until='load', timeout=120000)
        pg.wait_for_function("() => (window.__bofFrames|0)>4", timeout=120000)
        pg.evaluate(sh.TRAP_RAF)
        pg.evaluate("() => { for(let i=0;i<8;i++){XART.rdy('arch_blaster_gun_'+i);XART.rdy('arch_blaster_fx_'+i);} }"); pg.wait_for_timeout(1500)
        def step(n):
            e = pg.evaluate(sh.STEP, n)
            if e: errs.append('step:' + e)

        # 1. the takeover
        pg.evaluate(SETUP, {'unlocked': True, 'stage': 6, 'lv': 2}); step(2)
        s = pg.evaluate("() => ({w:run.weapon,l0:run.wlevels[0],l7:run.wlevels[7],lv:run.wlevel})")
        ok(s['w'] == 7 and s['l0'] == s['l7'] == 2, 'Stage 6, chaingun unlocked: the MG slot becomes the chaingun at the MG level (%s)' % s)
        # 2. rounds from the pods, faster, .50 cal
        pg.evaluate("""() => { window.__fired=0;window.__traced=0;
          const f=chaingunPlayerFire;chaingunPlayerFire=function(lv){const n=pBullets.length;const r=f.apply(this,arguments);window.__fired+=pBullets.length-n;return r;};
          const d=chaingunRoundDraw;chaingunRoundDraw=function(b){const r=d.apply(this,arguments);if(r)window.__traced++;return r;};
          Input.keys.j=true; }""")
        step(40); pg.wait_for_timeout(40)
        r = pg.evaluate("""() => { const M=chaingunMountPoints();const q=pBullets.filter(b=>b._cal50&&!b.dead);
          return {n:window.__fired,spd:q.length?Math.max(...q.map(b=>Math.hypot(b.vx,b.vy))):0,dmg:q.length?q[0].dmg:0,kind:q.length?q[0].kind:null,
            xs:[...new Set(q.map(b=>Math.round(b.x)))].slice(0,6),mounts:M.map(p=>Math.round(p.x)),px:Math.round(player.x)}; }""")
        ok(r['n'] >= 4 and r['spd'] >= 15 and r['kind'] == 'mg', 'held fire puts .50-cal rounds in the air at %.1f px/frame (was 10.5-12.3), still kind mg (%d fired in 40 frames)' % (r['spd'], r['n']))
        ok(all(abs(x - r['px']) > 5 for x in r['xs']), 'rounds leave the wing pods, not the nose (round x %s, pods %s, ship %s)' % (r['xs'], r['mounts'], r['px']))
        # draws: pods spin (several barrel frames), tracer art, no nose-only MG pellet draw for them
        pg.evaluate("() => { window.__asked={}; }"); step(24); pg.wait_for_timeout(30)
        asked = pg.evaluate("() => Object.keys(window.__asked)")
        pods = sorted(k for k in asked if k.startswith('arch_blaster_gun_')); tr = pg.evaluate("() => window.__traced")   # xartPalette caches, so count the draws, not the key asks
        ok(len(pods) >= 2, 'the pods are drawn and their barrels turn through frames (%s)' % pods)
        ok(tr > 0, 'the rounds draw as the .50-cal tracer (%d tracer draws)' % tr)
        # zoomed frame
        d = pg.evaluate("() => document.getElementById('screen').toDataURL('image/png')")
        open(os.path.join(OUT, 'firing.png'), 'wb').write(base64.b64decode(d.split(',', 1)[1]))
        # 3. impacts on an enemy
        hit = pg.evaluate("""() => { enemies=[];const e=spawnEnemy('s6dart',player.x,player.y-160,{});if(e){e.hp=e.maxhp=999;e.shoots=false;e.vx=0;e.vy=0;e._freezeMove=true;}
          window.__asked={};return !!e; }""")
        for _ in range(4):
            pg.evaluate("() => { for(const e of enemies){e.x=player.x;e.y=player.y-150;e.vx=0;e.vy=0;} }"); step(6)
        asked = pg.evaluate("() => Object.keys(window.__asked)")
        imp = pg.evaluate("() => pImpacts.filter(p=>p.pal==='#ffb347').length")
        ok(hit and imp > 0 and any(k in asked for k in ('arch_blaster_fx_0', 'arch_blaster_fx_1', 'arch_blaster_fx_2', 'arch_blaster_fx_3')), 'hits throw their own amber impact (%d live)' % imp)
        # 3b. no overheat: twenty real seconds of held fire, still firing at the end
        pg.evaluate("() => { enemies=[];window.__fired=0; }")
        for _ in range(20):
            step(60); pg.wait_for_timeout(15)
        late = pg.evaluate("() => { const a=window.__fired;return {a,heat:run._chainHeat||0,oh:run._chainOverheat||0,row:barRows().chaingun==null?null:1}; }")
        pg.evaluate("() => { window.__fired=0; }"); step(60)
        tail = pg.evaluate("() => window.__fired")
        ok(late['heat'] == 0 and late['oh'] == 0 and late['row'] is None and tail >= 20, 'twenty seconds of held fire never overheats, and it is still firing in the 21st (%s, %d rounds in the last second)' % (late, tail))
        pg.evaluate("() => { Input.keys.j=false; }")
        # 4. a death drops you to the MG slot - which is the chaingun again next frame
        pg.evaluate("() => { run.weapon=0;run.wlevels=WEAPONS.map(()=>0);run.wlevel=0; }"); step(2)
        s = pg.evaluate("() => ({w:run.weapon,l:run.wlevel})")
        ok(s['w'] == 7, 'after the death reset the default gun is the chaingun (%s)' % s)
        # 5. an MG crate raises it
        pg.evaluate("() => { applyPowerup({kind:'weapon',wtype:0,x:player.x,y:player.y}); }"); step(2)
        s = pg.evaluate("() => ({w:run.weapon,l0:run.wlevels[0],l7:run.wlevels[7]})")
        ok(s['w'] == 7 and s['l7'] >= 1 and s['l0'] == s['l7'], 'an MG crate raises the chaingun (%s)' % s)
        # 6. the MG's forged element rides the chaingun
        pg.evaluate("() => { run.forge={0:{elem:'fire',lv:1}};run.infusion=null;run.weapon=0; }"); step(2)
        s = pg.evaluate("() => ({w:run.weapon,forge:(forgeEntry(7)||{}).elem,inf:run.infusion&&run.infusion.elem})")
        ok(s['w'] == 7 and s['forge'] == 'fire' and s['inf'] == 'fire', 'the MG forged element applies to the chaingun (%s)' % s)
        # 7. where it must NOT engage
        for label, cfg in [('Stage 5', {'unlocked': True, 'stage': 5}), ('Stage 7 before the unlock', {'unlocked': False, 'stage': 7})]:
            pg.evaluate(SETUP, cfg); step(2)
            ok(pg.evaluate("() => run.weapon") == 0, '%s keeps the machine gun' % label)
        for lv in (2, 6):
            pg.evaluate(SETUP, {'unlocked': True, 'stage': 7, 'pilot': 'cole', 'lv': lv}); step(2)
            c = pg.evaluate("() => ({w:run.weapon,bay:run.loadout.indexOf(7),pool:crateWeaponPool(true).indexOf(7)})")
            ok(c['w'] == 0 and c['bay'] < 0 and c['pool'] < 0, 'Cole keeps his machine gun at MG level %d: no chaingun, no bay, no pool slot (%s)' % (lv, c))
        # 7b. the loadout screen between stages is where the choice is made
        pg.evaluate(SETUP, {'unlocked': True, 'stage': 5}); step(1)
        L = pg.evaluate("() => { run._chainSeeded=false;loadoutStart(function(){});return {bays:run.loadout.slice(),pool:loadoutScr&&loadoutScr.pool.slice(),state}; }")
        ok(7 in L['bays'] and 0 not in L['bays'] and 0 in (L['pool'] or []), 'the loadout after Stage 5 opens with the chaingun in the MG bay and the MG still in the pool (%s)' % L)
        pg.evaluate("() => { setState(GS.PLAY); }")
        # 8. the wind bed (Stage 6)
        pg.evaluate(SETUP, {'unlocked': True, 'stage': 6}); step(4)
        w0 = pg.evaluate("() => ({on:!!_ambEl,stage:_ambStage})")
        pg.evaluate("() => { setState(GS.GAMEOVER); }"); step(2)
        w1 = pg.evaluate("() => ({on:!!_ambEl})")
        pg.evaluate("() => { setState(GS.PLAY); }"); step(2)
        w2 = pg.evaluate("() => ({on:!!_ambEl})")
        pg.evaluate("() => { setState(GS.TITLE); }"); step(2)
        w3 = pg.evaluate("() => ({on:!!_ambEl})")
        ok(w0['on'], 'the Stage 6 wind bed plays during the stage')
        ok(not w1['on'], 'a game over stops the wind')
        ok(w2['on'], 'play resuming (a continue) brings the wind back')
        ok(not w3['on'], 'quitting to the title stops the wind')
        br.close()
    stop()
    ok(not errs, 'no page, console, draw or step errors (%s)' % errs[:3])
    print('%d ok / %d fail' % (N['ok'], len(FAILS)))
    sys.exit(1 if FAILS else 0)

if __name__ == '__main__':
    main()
