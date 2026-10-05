"""probe_turbulence_1002 - Stage 6 turbulence cues in real Chromium (Mike, 1002).

    python3 _BUILD_SOURCE/probe_turbulence_1002.py [--old]

  - both cues are registered as pools with TAME rows, and their files serve 200;
  - during the opening flyover (the Harrier passing over) the turbulence LOOP is on alongside the carrier
    turbine and its media element actually advances (playing, not just requested);
  - a stealth jet crossing the pilot's row plays the jet wash exactly once for that jet, and the element plays;
  - zero page errors.
--old routes feedback_1002.js to an empty body.
"""
import argparse, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import shoot

SETUP = r"""
()=>{
  ASSETS.ready=true; window.__bofStepNow=performance.now(); diffKey='normal'; if(typeof DIFFS!=='undefined')DIFF=DIFFS.normal;
  run.pilot='cole'; run.stage=6; run.mode='arcade'; curStage=STAGES[5];
  beginStage(6); setState(GS.PLAY); player.reset(); playerHit=function(){};
  const L=window.__L={plays:{}};
  const pl=Snd.play; Snd.play=function(n){L.plays[n]=(L.plays[n]||0)+1; return pl.apply(this,arguments);};
  return {pools:['turbCarrier1002','jetWash1002'].map(n=>!!(Snd.pools&&Snd.pools[n])), tame:['turbCarrier1002','jetWash1002'].map(n=>!!(Snd.TAME&&Snd.TAME[n])), opening:!!s6Opening, phase:s6Opening&&s6Opening.phase};
}
"""
FLY = r"""
()=>{
  if(!s6Opening) return {err:'no opening'};
  s6Opening.phase='flyover'; s6Opening.t=0; s6Opening.carrierJets=[]; s6Opening.carrierLaunchN=0;
  return true;
}
"""
STEP = r"""
(n)=>{for(let i=0;i<n;i++){window.__bofStepNow+=1000/60; loop(window.__bofStepNow);}
  const T=Snd.loops&&Snd.loops.turbCarrier1002, C=Snd.loops&&Snd.loops.carrierTurbine;
  return {turb:T?{on:T.on,ct:+(T.el.currentTime||0).toFixed(3),paused:T.el.paused,rs:T.el.readyState}:null, turbine:C?{on:C.on}:null, phase:s6Opening&&s6Opening.phase, plays:window.__L.plays};}
"""
WASH = r"""
()=>{
  s6Opening=null; run._mission29OpeningDone=true; stagePlan=[]; enemies.length=0; window.__L.plays={};
  player.x=(camLeftX()+camRightX())/2; player.y=VH-150;
  const q={direction:'east',role:'orange',x:0,y:player.y,t:0,warn:0,id:'probe-wash'}; fb2Flights.push(q);
  return true;
}
"""


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--old', action='store_true'); a = ap.parse_args()
    from playwright.sync_api import sync_playwright
    port, stop = shoot.serve(shoot.GAME); errs = []; fails = []; status = {}
    with sync_playwright() as p:
        chrome = os.environ.get('BOF_CHROME', '/opt/pw-browsers/chromium-1194/chrome-linux/chrome')
        b = p.chromium.launch(args=['--disable-gpu', '--no-sandbox', '--autoplay-policy=no-user-gesture-required'], **({'executable_path': chrome} if os.path.exists(chrome) else {}))
        pg = b.new_page(viewport={'width': 1100, 'height': 1200})
        pg.on('pageerror', lambda e: errs.append(str(e)[:300]))
        pg.on('response', lambda r: status.__setitem__(r.url.split('/')[-1], r.status) if ('1002' in r.url and r.url.endswith('.mp3')) else (errs.append('HTTP %d %s' % (r.status, r.url)) if r.status >= 400 else None))
        if a.old:
            pg.route('**/assets/feedback_1002.js', lambda r: r.fulfill(status=200, content_type='application/javascript', body='/* busted arm */'))
        pg.goto(f'http://127.0.0.1:{port}/index.html', wait_until='load', timeout=60000)
        pg.wait_for_function("() => (window.__bofFrames|0) > 4", timeout=45000)
        pg.mouse.click(400, 400)   # a real gesture, so media may play
        pg.evaluate(shoot.TRAP_RAF)
        setup = pg.evaluate(SETUP); print('setup', setup)
        print('flyover', pg.evaluate(FLY))
        samples = []
        for k in range(40):
            r = pg.evaluate(STEP, 6); samples.append(r); pg.wait_for_timeout(60)
        pg.evaluate(WASH)
        washes = []
        for k in range(40):
            r = pg.evaluate(STEP, 6); washes.append(r); pg.wait_for_timeout(30)
        jw = pg.evaluate("()=>{const p=Snd.pools.jetWash1002;if(!p)return null;const v=p.slots.find(s=>s&&s.attached);return v?{ct:v.el.currentTime,paused:v.el.paused,rs:v.el.readyState}:null}")
        b.close()
    stop()
    on = [s for s in samples if s['turb'] and s['turb']['on']]
    print('turb samples on', len(on), 'of', len(samples), on[:1], on[-1:] if on else None)
    print('files', status)
    print('wash plays', washes[-1]['plays'], 'jetwash voice', jw)
    if not all(setup.get('pools', [False])) or not all(setup.get('tame', [False])): fails.append('cues not registered (pools/TAME)')
    if not on: fails.append('the turbulence loop never came on during the flyover')
    elif not (on[-1]['turb']['ct'] > on[0]['turb']['ct'] + .2): fails.append('the turbulence loop did not actually play (currentTime %.2f -> %.2f)' % (on[0]['turb']['ct'], on[-1]['turb']['ct']))
    if not all(s['turbine'] and s['turbine']['on'] for s in on): fails.append('turbulence on without the carrier turbine')
    if washes[-1]['plays'].get('jetWash1002', 0) != 1: fails.append('jet wash played %s times for one pass (want 1)' % washes[-1]['plays'].get('jetWash1002', 0))
    if not jw or (jw['ct'] <= 0 and jw['paused']): fails.append('the jet wash voice never played')
    for f in ('turbulence_carrier_1002.mp3', 'jetwash_1002.mp3'):
        if status.get(f) not in (200, 206): fails.append('%s served %s' % (f, status.get(f)))
    print('errors', errs[:4])
    if errs: fails.append('page errors')
    print('FAIL' if fails else 'PASS', fails)


if __name__ == '__main__':
    main()
