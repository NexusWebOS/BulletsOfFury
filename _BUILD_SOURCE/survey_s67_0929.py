#!/usr/bin/env python3
"""survey_s67_0929.py - look at every Stage 6/7 item on Mike's 0929 list before touching it.

    python _BUILD_SOURCE/survey_s67_0929.py <scenario> [--diff normal|hard|furious] [--out DIR]

Scenarios: s6boss, s6ace, s6assault, s6rebels, s7entry, s7sluice, s7play, s7boss, s7exit.
Each saves frames (the whole game canvas, 960x1024) and a JSON of what it measured.
Real Chromium, TRAP_RAF + STEP, real pauses between chunks so lazily-loaded art decodes.
"""
import os, sys, json, base64, argparse, http.server
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
http.server.SimpleHTTPRequestHandler.log_message = lambda *a, **k: None
import shoot as sh
from playwright.sync_api import sync_playwright

BASE = r"""
(c) => {
  if (typeof ht27Stop === 'function') ht27Stop();
  debugFight = null; coopOn = false; diffKey = c.diff; DIFF = DIFFS[c.diff]; bossDefeated = false;
  run.mode = c.mode || 'campaign'; run.pilot = 'cole'; pilotIndex = PILOTS.findIndex(p => p.key === 'cole');
  window.__hits = 0; playerHit = function(){ window.__hits++; };
  window.__keys = {}; const get = XART.get.bind(XART);
  XART.get = function(k){ window.__keys[k] = (window.__keys[k]||0) + 1; return get(k); };
  return true;
}
"""

SCEN = {
 # the carrier: descend, bay, escorts, hold; on Hard a thruster beam
 's6boss': dict(setup=r"""() => { beginStage(6); setState(GS.PLAY); story=null; special=null; player.reset(); s6Opening=null;
     if (s6Wing) { s6Wing.choice=false; s6Wing.route='left'; }
     stagePlan=[]; waveIdx=999; spawnClock=9999; enemies=[]; eBullets=[]; pBullets=[]; powerups=[]; l5Rocks=[];
     spawnBoss('warhive'); bossActive=true; whvWarm(); return {w:boss.w,h:boss.h,jetN:boss._whv.jetN,hard:boss._whv.hard}; }""",
   shots=[1.2, 2.8, 3.6, 4.6, 6.0, 7.2],
   poke={4.7: r"""() => { const W=boss._whv; if(W.hard){ W.can.cd=0; W.can.i=2; } return W.st; }""",
         6.1: r"""() => { const W=boss._whv; if(W.hard&&W.beam){ return 'beam '+W.beam.t.toFixed(2); } return W.st; }"""}),
 's6ace': dict(setup=r"""() => { beginStage(6); setState(GS.PLAY); story=null; special=null; player.reset(); s6Opening=null;
     if (s6Wing) { s6Wing.choice=false; s6Wing.route='left'; }
     stagePlan=[]; waveIdx=999; spawnClock=9999; enemies=[]; eBullets=[]; pBullets=[]; powerups=[];
     spawnBoss('warhive'); bossActive=true; whvWarm(); return true; }""",
   shots=[3.2, 5.0, 7.0, 9.0, 12.0, 15.0],
   poke={3.0: r"""() => { const W=boss._whv; W.st='hold'; W.t=0; W.cy=WHV_HOME_Y; W.core=0; return 'killed carrier'; }"""}),
 # the opening assault: side gates, bombers, descending gates
 's6assault': dict(setup=r"""() => { beginStage(6); setState(GS.PLAY); story=null; special=null; player.reset();
     stagePlan=[]; waveIdx=999; spawnClock=9999; enemies=[]; eBullets=[]; pBullets=[]; groundTargetingReset();
     const O=missionAssaultStart(); return {events:O.events.length, finish:O.finish, bombs:O.events.filter(e=>e.kind==='bomb').map(e=>+e.at.toFixed(2))}; }""",
   shots=[1.4, 2.2, 12.0, 12.6, 13.02, 13.2, 13.8, 14.6, 15.4, 22.0, 24.0, 26.0, 28.0],
   poke={12.5: r"""() => { const b=enemies.filter(e=>e._mission29); return b.map(e=>({k:e._mission29.kind,x:Math.round(e.x),y:Math.round(e.y),w:e.w,h:e.h,dw:e._drawW,dh:e._drawH,flash:e.flash})); }""",
         13.0: r"""() => { const e=enemies.find(e=>e._mission29&&!e.dead); if(!e) return 'none'; pBullets.push({x:e.x,y:e.y+4,vx:0,vy:0,w:4,h:8,dmg:2,t:0}); return 'shot at '+Math.round(e.x); }"""}),
 # the rebel squad: the V arrives and talks, then the fight
 's6rebels': dict(setup=r"""() => { beginStage(6); setState(GS.PLAY); story=null; special=null; player.reset(); s6Opening=null;
     if (s6Wing) { s6Wing.choice=false; s6Wing.route='right'; }
     stagePlan=[]; waveIdx=999; spawnClock=9999; enemies=[]; eBullets=[]; pBullets=[];
     spawnBoss('rebelsquad'); bossActive=true; return true; }""",
   shots=[3.0, 8.0, 20.0, 27.0, 30.5, 32.0, 34.0, 37.0, 41.0]),
 # the stage 7 start, the real sequence (stage card, launch, arrival)
 's7entry': dict(setup=r"""() => { beginStage(7); return {state}; }""", noforce=True,
   shots=[4.5, 5.5, 7.0, 9.0, 11.5, 12.5, 13.5, 14.5, 15.5, 16.5, 17.5, 18.5]),
 # the sluice vents: scrub the sewer to each vent row and let it fire
 's7sluice': dict(setup=r"""() => { beginStage(7); setState(GS.PLAY); story=null; special=null; player.reset();
     stagePlan=[]; waveIdx=999; spawnClock=9999; enemies=[]; eBullets=[]; pBullets=[]; run._s7Sluices=null; return {srcY:_masterSrcY}; }""",
   shots=[2.0, 4.0, 4.6, 5.0, 5.4, 5.8, 6.2, 6.6, 7.0, 8.0],
   track=r"""() => { const ev=stage7SluiceEvents().filter(e=>e.tier===0); return {srcY:Math.round(_masterSrcY||0), ev:ev.map(e=>({row:e.row,y:Math.round(e.row-_masterSrcY),live:e.live,t:+e.t.toFixed(2),done:e.done}))}; }"""),
 # ordinary stage 7 play: enemies (triangles?), 30 s
 's7play': dict(setup=r"""() => { beginStage(7); setState(GS.PLAY); story=null; special=null; player.reset(); return true; }""",
   shots=[6, 10, 14, 18, 22, 26, 30]),
 # the Warden: portal intro, entry, fight
 's7boss': dict(setup=r"""() => { beginStage(7); setState(GS.PLAY); story=null; special=null; player.reset();
     stagePlan=[]; waveIdx=999; spawnClock=9999; enemies=[]; eBullets=[]; pBullets=[];
     spawnBoss('sludgeemperor'); bossActive=true; s7mInit(boss); return {name:boss.name}; }""",
   shots=[1.0, 3.5, 6.0, 8.0, 9.5, 11.0, 13.0, 16.0, 20.0, 24.0]),
 # the ending: kill the Warden and watch the escape
 's7exit': dict(setup=r"""() => { beginStage(7); setState(GS.PLAY); story=null; special=null; player.reset();
     stagePlan=[]; waveIdx=999; spawnClock=9999; enemies=[]; eBullets=[]; pBullets=[];
     spawnBoss('sludgeemperor'); bossActive=true; const M=s7mInit(boss); M._mission29IntroDone=true; return true; }""",
   shots=[1.0, 4.5, 9.0, 10.5, 12.0, 13.5, 15.0, 16.2, 17.0, 17.6, 18.3, 19.5, 21.0],
   poke={0.5: r"""() => { const b=boss,M=b._s7mod; M.mode='fight'; b.y=b.ty; for(const p of M.parts)p.hp=0; M.shield=0; M.core=0; s7mSet(b,'dead'); M.t=3.4; return 'dead'; }"""},
   track=r"""() => { const b=boss, M=b&&b._s7mod, E=M&&M.frExit; return {st:state, t:E?+E.t.toFixed(2):null, py:Math.round(player.y), px:Math.round(player.x),
        by:b?Math.round(b.y):null, srcY:Math.round(_masterSrcY||0), scroll:Math.round(mapScroll||0), ex:explosions.length,
        exMinY:explosions.length?Math.round(Math.min(...explosions.map(q=>q.y))):null, exMaxY:explosions.length?Math.round(Math.max(...explosions.map(q=>q.y))):null,
        hidden:!!(b&&b._s7warden&&b._s7warden.final&&b._s7warden.final.shipHidden)}; }"""),
}

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('scenario'); ap.add_argument('--diff', default='normal')
    ap.add_argument('--out', default=None); a = ap.parse_args()
    S = SCEN[a.scenario]
    out = a.out or os.path.join(sh.GAME, '_shots', 'survey_0929', a.scenario + '_' + a.diff)
    os.makedirs(out, exist_ok=True)
    port, stop = sh.serve(sh.GAME)
    rep = {'scenario': a.scenario, 'diff': a.diff, 'frames': [], 'pokes': {}, 'track': []}
    with sync_playwright() as pw:
        br = pw.chromium.launch(args=['--no-sandbox', '--mute-audio'])
        pg = br.new_page(viewport={'width': 1000, 'height': 1100}); errs = []
        pg.on('pageerror', lambda e: errs.append('pageerror: ' + str(e)[:200]))
        pg.on('console', lambda m: errs.append('console: ' + m.text[:200]) if m.type == 'error' else None)
        pg.goto('http://127.0.0.1:%d/index.html' % port, wait_until='load', timeout=120000)
        pg.wait_for_function("() => (window.__bofFrames|0)>4", timeout=120000)
        pg.evaluate(sh.TRAP_RAF)
        pg.evaluate(BASE, {'diff': a.diff})
        rep['setup'] = pg.evaluate(S['setup'])
        pg.wait_for_timeout(1500)                     # let the art this state touched decode
        t = 0.0; shots = sorted(S['shots']); pokes = dict(S.get('poke', {}))
        events = sorted(set(shots) | set(pokes.keys()))
        for ev in events:
            while t < ev - 1e-6:
                n = max(1, min(30, int(round((ev - t) * 60))))
                e = pg.evaluate(sh.STEP, n)
                if e: errs.append('STEP: ' + e)
                t += n / 60.0
                if S.get('track'): rep['track'].append(pg.evaluate(S['track']))
                pg.wait_for_timeout(25)
            if ev in pokes:
                rep['pokes'][str(ev)] = pg.evaluate(pokes[ev])
            if ev in shots:
                d = pg.evaluate("() => document.getElementById('screen').toDataURL('image/png')")
                fn = os.path.join(out, 't%05.1f.png' % ev)
                open(fn, 'wb').write(base64.b64decode(d.split(',', 1)[1]))
                rep['frames'].append({'t': ev, 'state': pg.evaluate("() => state"), 'file': os.path.basename(fn)})
        rep['keys'] = pg.evaluate("() => window.__keys")
        rep['errs'] = errs
        br.close()
    stop()
    json.dump(rep, open(os.path.join(out, 'survey.json'), 'w'), indent=1)
    # a contact sheet of the frames, half size
    try:
        from PIL import Image, ImageDraw
        ims = [Image.open(os.path.join(out, f['file'])).convert('RGB') for f in rep['frames']]
        if ims:
            w, h = ims[0].size[0] // 2, ims[0].size[1] // 2; cols = min(4, len(ims)); rows = (len(ims) + cols - 1) // cols
            sheet = Image.new('RGB', (cols * w, rows * (h + 18)), (16, 16, 16)); d = ImageDraw.Draw(sheet)
            for i, (im, f) in enumerate(zip(ims, rep['frames'])):
                x, y = (i % cols) * w, (i // cols) * (h + 18)
                sheet.paste(im.resize((w, h)), (x, y + 18)); d.text((x + 4, y + 3), 't=%.1f %s' % (f['t'], f['state']), fill=(255, 230, 120))
            sheet.save(os.path.join(out, 'sheet.png'))
    except Exception as ex:
        print('sheet failed', ex)
    print(json.dumps({k: rep[k] for k in ('setup', 'pokes', 'errs')}, indent=0)[:3000])
    print('frames ->', out)

if __name__ == '__main__':
    main()
