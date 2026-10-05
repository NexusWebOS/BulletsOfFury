"""probe_hammer_intro_1002 - the Stage 5 hammer's arrival as an in-play beat, in real Chromium.

    python3 _BUILD_SOURCE/probe_hammer_intro_1002.py [--pilot cole] [--mode campaign] [--old]

Asserts, from the running game:
  1. the intro starts when the hammer finishes unfolding, and the 0930 LIVE (pausing) director scene
     never runs (BOFCinematicDirector.live stays false);
  2. the game is NOT paused: updatePlay keeps advancing (the stage-5 space scroll and stateT move);
  3. the pilot is stunned: a held real LEFT key does not move the ship;
  4. the hammer holds the unfolded plate and cannot be hit (_noHit) until the dialogue ends, then
     becomes hittable;
  5. the dialogue blits the hammer avatar box and the chosen dispatcher box (identified by KEY via a
     wrap on XART.get - never by size or .src), and the dispatcher follows Mike's rule;
  6. the arena is darkened: a background pixel under the box region drops in luminance.
--old routes feedback_1002.js to an empty body (the busted arm: the 0930 pausing scene).
"""
import argparse, base64, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import shoot

SETUP = r"""
(cfg)=>{
  ASSETS.ready=true; window.__bofStepNow=performance.now(); diffKey='normal'; if(typeof DIFFS!=='undefined')DIFF=DIFFS.normal;
  run.pilot=cfg.pilot; run.stage=5; run.mode=cfg.mode; curStage=STAGES[4];
  if(cfg.p2){coopOn=true; run2.pilot=cfg.p2;}
  beginStage(5); setState(GS.PLAY); player.reset(); playerHit=function(){};
  spawnBoss('chromehammer'); bossActive=true; boss._be=null; boss._symEntry=null; boss.enter=false;
  const L=window.__L={keys:{},liveSeen:false,introSeen:false,states:[]};
  const g=XART.get; XART.get=function(k){L.keys[k]=(L.keys[k]||0)+1; return g.apply(this,arguments);};
  return {kind:boss.kind, state:boss._hammer&&boss._hammer.state};
}
"""
STEP = r"""
(a)=>{
  const L=window.__L,out=[];
  for(let i=0;i<a.n;i++){
    window.__bofStepNow+=1000/60; loop(window.__bofStepNow);
    if(BOFCinematicDirector&&BOFCinematicDirector.live)L.liveSeen=true;
    const I=(typeof fb2Intro!=='undefined')?fb2Intro:null;
    if(I&&!I.done)L.introSeen=true;
    const h=boss&&boss._hammer;
    if(h&&L.states[L.states.length-1]!==h.state)L.states.push(h.state);
  }
  const I=(typeof fb2Intro!=='undefined')?fb2Intro:null,h=boss&&boss._hammer;
  return {state:h&&h.state,t:h&&+h.t.toFixed(2),noHit:!!boss._noHit,intro:I?{i:I.i,done:I.done,disp:I.disp,who:I.lines[I.i]&&I.lines[I.i].who,kind:I.lines[I.i]&&I.lines[I.i].kind,dim:+I.dim.toFixed(2)}:null,
    px:+player.x.toFixed(1), scroll:(typeof _stage5SpaceScroll!=='undefined'?_stage5SpaceScroll:null), stateT:+(stateT||0).toFixed(2),
    live:!!(BOFCinematicDirector&&BOFCinematicDirector.live)};
}
"""
GRAB = "() => document.querySelector('#screen').toDataURL('image/png')"
LUM = r"""
()=>{const c=document.querySelector('#screen'),g=c.getContext('2d'),W=c.width,H=c.height;
 // a column strip at the far left of the play field, rows 10-30% (above the box, away from the boss)
 // the MEDIAN, so an asteroid drifting through the strip cannot move the answer
 const d=g.getImageData(Math.round(W*.02),Math.round(H*.10),Math.round(W*.16),Math.round(H*.22)).data,v=[];
 for(let i=0;i<d.length;i+=4)v.push(.299*d[i]+.587*d[i+1]+.114*d[i+2]); v.sort((a,b)=>a-b); return v[v.length>>1];}
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--pilot', default='cole'); ap.add_argument('--p2', default='')
    ap.add_argument('--mode', default='campaign'); ap.add_argument('--old', action='store_true')
    ap.add_argument('--out', default='_shots/hammer_intro_1002')
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    from playwright.sync_api import sync_playwright
    port, stop = shoot.serve(shoot.GAME)
    errs = []; fails = []; rec = {}
    with sync_playwright() as p:
        chrome = os.environ.get('BOF_CHROME', '/opt/pw-browsers/chromium-1194/chrome-linux/chrome')
        b = p.chromium.launch(args=['--disable-gpu', '--no-sandbox', '--mute-audio'], **({'executable_path': chrome} if os.path.exists(chrome) else {}))
        pg = b.new_page(viewport={'width': 1100, 'height': 1200})
        pg.on('pageerror', lambda e: errs.append(str(e)[:300]))
        pg.on('console', lambda m: errs.append('console.error: ' + m.text[:200]) if m.type == 'error' and '404' not in m.text else None)
        pg.on('response', lambda r: errs.append('404 ' + r.url) if r.status >= 400 else None)
        if a.old:
            pg.route('**/assets/feedback_1002.js', lambda r: r.fulfill(status=200, content_type='application/javascript', body='/* busted arm */'))
        pg.goto(f'http://127.0.0.1:{port}/index.html', wait_until='load', timeout=60000)
        pg.wait_for_function("() => (window.__bofFrames|0) > 4", timeout=45000)
        pg.evaluate(shoot.TRAP_RAF)
        rec['setup'] = pg.evaluate(SETUP, {'pilot': a.pilot, 'mode': a.mode, 'p2': a.p2})
        pg.wait_for_timeout(1200)
        # warm the boxes so the first dialogue frame is drawn against decoded art
        pg.evaluate("()=>{for(const k of ['fb2_hammer_avatar','fb2_dispatch_cole','fb2_dispatch_decker','fb2_dispatch_axel','fb2_dispatch_lizzie','fb2_dispatch_falva','dlg_window'])try{XART.rdy(k)}catch(e){}}")
        pg.wait_for_timeout(800)
        lum0 = None; samples = []; shots = {}
        # The integrated trap taunt adds two lines; allow the complete opening
        # jump, landing recovery, return and chromium activation afterward.
        for k in range(360):
            r = pg.evaluate(STEP, {'n': 10}); pg.wait_for_timeout(8)
            samples.append(r)
            if lum0 is None and r['state'] in ('flyby', 'return'):
                lum0 = pg.evaluate(LUM)
            I = r.get('intro')
            if I and not I['done']:
                key = I['kind'] + str(I['i'])
                if key not in shots and r['stateT'] > 0:
                    pg.wait_for_timeout(250); pg.evaluate(STEP, {'n': 40})
                    shots[key] = pg.evaluate(GRAB)
                    rec.setdefault('lum_intro', pg.evaluate(LUM))
                    # stunned: hold a real LEFT key for 30 frames, the ship must not move
                    if 'stun' not in rec:
                        x0 = pg.evaluate("()=>player.x")
                        pg.keyboard.down('ArrowLeft'); pg.evaluate(STEP, {'n': 30}); pg.keyboard.up('ArrowLeft')
                        rec['stun'] = {'x0': x0, 'x1': pg.evaluate("()=>player.x")}
            if r['state'] == 'hammer' and (not I or I['done']):
                # a few seconds of the fight
                after = pg.evaluate(STEP, {'n': 60}); rec['after'] = after
                rec['after_move'] = None
                x0 = pg.evaluate("()=>player.x"); pg.keyboard.down('ArrowLeft'); pg.evaluate(STEP, {'n': 30}); pg.keyboard.up('ArrowLeft')
                rec['after_move'] = {'x0': x0, 'x1': pg.evaluate("()=>player.x")}
                break
            if r['state'] == 'leap' and 'opening_leap' not in shots:
                shots['opening_leap'] = pg.evaluate(GRAB)
        rec['lum0'] = lum0
        rec['L'] = pg.evaluate("()=>({keys:Object.keys(window.__L.keys).filter(k=>/fb2_|comm_|cin30_/.test(k)),live:window.__L.liveSeen,intro:window.__L.introSeen,states:window.__L.states})")
        for k, d in shots.items():
            with open(os.path.join(a.out, 'intro_%s.png' % k), 'wb') as fh:
                fh.write(base64.b64decode(d.split(',', 1)[1]))
        b.close()
    stop()
    L = rec['L']
    intro_samples = [s for s in samples if s.get('intro') and not s['intro']['done']]
    print('setup', rec['setup']); print('states', ' > '.join(L['states']))
    print('live (pausing) scene seen:', L['live'], ' in-play intro seen:', L['intro'])
    print('keys', sorted(L['keys']))
    if not L['intro']: fails.append('the in-play intro never started')
    if L['live']: fails.append('the 0930 live director scene ran (the game paused)')
    expected = ['warn', 'leap', 'recover', 'back', 'fr_activation', 'hammer']
    if not all(s in L['states'] for s in expected) or sorted(L['states'].index(s) for s in expected if s in L['states']) != [L['states'].index(s) for s in expected if s in L['states']]:
        fails.append('opening jump must land and return before chromium activation')
    if intro_samples:
        disp = intro_samples[0]['intro']['disp']
        print('dispatcher', disp, 'for', a.pilot, a.p2)
        sc = [s['scroll'] for s in intro_samples if s['scroll'] is not None]
        st = [s['stateT'] for s in intro_samples]
        print('scroll during intro', sc[:1], sc[-1:], ' stateT', st[0], st[-1])
        if sc and not (sc[-1] != sc[0]): fails.append('the stage-5 scroll did not advance during the intro (paused?)')
        if st[-1] <= st[0]: fails.append('stateT did not advance during the intro')
        if any(not s['noHit'] for s in intro_samples): fails.append('the hammer was hittable during the dialogue')
        if any(s['state'] not in ('unfold',) for s in intro_samples): fails.append('the hammer left unfold during the dialogue: %s' % sorted({s['state'] for s in intro_samples}))
        if 'fb2_hammer_avatar' not in L['keys']: fails.append('the hammer avatar box was never drawn')
        if 'fb2_dispatch_' + disp not in L['keys']: fails.append('the dispatcher box %s was never drawn' % disp)
        want = {'cole': 'decker', 'decker': 'cole'}.get(a.pilot)
        if a.p2 and {a.pilot, a.p2} == {'cole', 'decker'}: want = 'axel'
        if want and disp != want: fails.append('dispatcher %s, expected %s' % (disp, want))
        if not want and disp not in ('cole', 'decker'): fails.append('dispatcher %s for %s should be Cole or Decker' % (disp, a.pilot))
    st = rec.get('stun')
    print('stun', st, 'after', rec.get('after_move'))
    if st and abs(st['x1'] - st['x0']) > .5: fails.append('the pilot moved while stunned (%.1f -> %.1f)' % (st['x0'], st['x1']))
    am = rec.get('after_move')
    if not am: fails.append('the fight never began after the intro')
    elif abs(am['x1'] - am['x0']) < 5: fails.append('the pilot still cannot move after the intro')
    if rec.get('after') and rec['after']['noHit']: fails.append('the hammer is still untargetable after the intro')
    print('luminance before', rec.get('lum0'), 'during', rec.get('lum_intro'))
    if rec.get('lum0') and rec.get('lum_intro') and not rec['lum_intro'] < rec['lum0'] * .8: fails.append('the arena was not darkened')
    print('errors', len(errs), errs[:3])
    if errs: fails.append('page errors')
    json.dump({'rec': {k: v for k, v in rec.items()}, 'samples': samples[-5:], 'errors': errs, 'failures': fails}, open(os.path.join(a.out, 'probe.json'), 'w'), indent=1)
    print('FAIL' if fails else 'PASS', fails)
    if fails: raise SystemExit(1)


if __name__ == '__main__':
    main()
