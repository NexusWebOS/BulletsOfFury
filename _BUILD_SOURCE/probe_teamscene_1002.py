"""probe_teamscene_1002 - Stage 6's "who stayed behind?" scene and Secret Weapon Callisto, real Chromium.

    python3 _BUILD_SOURCE/probe_teamscene_1002.py [--pilot cole] [--old]

Drives the real s6Wing flow to its post-flyover beat (W.fake) and asserts:
  - the scene starts at the end of the beat and the split-the-wing CHOICE waits for it, then follows it;
  - the game is not paused (stateT advances) and the pilot cannot move or be hit meanwhile;
  - Cole's rage lines draw the generated shouting frames (fb2_cole_rage_*), and more than one of them;
  - PLAYING COLE: "SECRET WEAPON CALLISTO" and "ACTIVATED" are lettered through stageText, ACTIVATED tinted
    green, five beeps; the demo releases the fusion cannon and fires the laser, then restores the pilot's
    weapon; the shocked lines follow. NOT COLE: none of that, straight to the choice.
--old routes feedback_1002.js to an empty body.
"""
import argparse, base64, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import shoot

SETUP = r"""
(cfg)=>{
  ASSETS.ready=true; window.__bofStepNow=performance.now(); diffKey='normal'; if(typeof DIFFS!=='undefined')DIFF=DIFFS.normal;
  run.pilot=cfg.pilot; run.stage=6; run.mode='campaign'; curStage=STAGES[5];
  beginStage(6); setState(GS.PLAY); player.reset();
  s6Opening=null; run._mission29OpeningDone=true; stagePlan=[]; enemies.length=0;
  const W=s6Wing; if(!W) return {err:'no s6Wing'};
  subBossDone=true; W.beats=2; s6WingLaunch(8,true); W.all=true; W.postMiniT=4;   // straight to the flyover beat
  run.weapon=1; run.wlevel=3; if(run.wlevels)run.wlevels[1]=3;
  const L=window.__L={texts:{},tints:{},beeps:0,keys:{},hits:0};
  const st=stageText; stageText=function(art,text,cx,cy,H,tint){const t=String(text||''); if(/CALLISTO|ACTIVATED/.test(t)){L.texts[t]=1; if(/ACTIVATED/.test(t))L.tints[tint||'none']=1;} return st.apply(this,arguments);};
  const bp=Audio.SFX.retinaLockBeep; Audio.SFX.retinaLockBeep=function(){L.beeps++; return bp&&bp.apply(this,arguments);};
  const g=XART.get; XART.get=function(k){if(/fb2_cole_rage|comm_/.test(k))L.keys[k]=(L.keys[k]||0)+1; return g.apply(this,arguments);};
  const ph=playerHit; playerHit=function(){L.hits++; return ph.apply(this,arguments);};
  for(let i=0;i<3;i++)XART.rdy('fb2_cole_rage_'+i);
  return {wing:!!W, ships:W.ships.length};
}
"""
STEP = r"""
(a)=>{
  const L=window.__L,W=s6Wing,out=[];
  for(let i=0;i<a.n;i++){
    window.__bofStepNow+=1000/60; loop(window.__bofStepNow);
    const S=(typeof fb2Talk!=='undefined')?fb2Talk:null, B=S&&!S.done?S.beats[S.i]:null;
    if(S&&!S.done&&L.lastBeat==='demo'&&!(B&&B.kind==='demo')&&!L.weaponAfter)L.weaponAfter=[run.weapon,run.wlevel];   // the frame the demo hands back
    if(S&&!S.done){L.sceneSeen=1; if(W.choice)L.choiceDuring=1; L.lastBeat=B?(B.kind||B.who+':'+B.text.slice(0,18)):null;
      if(B&&B.kind==='demo'&&S.demo){L.demoFired=S.demo.fired; L.released=!!S.demo.released;}
      L.beatsN=S.beats.length; L.maxI=Math.max(L.maxI||0,S.i);}
    if(L.sceneSeen&&(!S||S.done)&&W.choice&&!L.choiceAfter){L.choiceAfter=1;}
  }
  const S=(typeof fb2Talk!=='undefined')?fb2Talk:null;
  return {stateT:+(stateT||0).toFixed(2), px:+player.x.toFixed(1), scene:S?{i:S.i,done:S.done,kind:S.beats[S.i]&&(S.beats[S.i].kind||S.beats[S.i].who)}:null, choice:!!W.choice, fake:W.fake?+W.fake.t.toFixed(2):null};
}
"""


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--pilot', default='cole'); ap.add_argument('--old', action='store_true')
    ap.add_argument('--out', default='_shots/teamscene_1002')
    a = ap.parse_args(); os.makedirs(a.out, exist_ok=True)
    from playwright.sync_api import sync_playwright
    port, stop = shoot.serve(shoot.GAME); errs = []; fails = []; samples = []; grabs = {}
    with sync_playwright() as p:
        chrome = os.environ.get('BOF_CHROME', '/opt/pw-browsers/chromium-1194/chrome-linux/chrome')
        b = p.chromium.launch(args=['--disable-gpu', '--no-sandbox', '--mute-audio'], **({'executable_path': chrome} if os.path.exists(chrome) else {}))
        pg = b.new_page(viewport={'width': 1100, 'height': 1200})
        pg.on('pageerror', lambda e: errs.append(str(e)[:300]))
        pg.on('response', lambda r: errs.append('HTTP %d %s' % (r.status, r.url)) if r.status >= 400 else None)
        if a.old:
            pg.route('**/assets/feedback_1002.js', lambda r: r.fulfill(status=200, content_type='application/javascript', body='/* busted arm */'))
        pg.goto(f'http://127.0.0.1:{port}/index.html', wait_until='load', timeout=60000)
        pg.wait_for_function("() => (window.__bofFrames|0) > 4", timeout=45000)
        pg.evaluate(shoot.TRAP_RAF)
        print('setup', pg.evaluate(SETUP, {'pilot': a.pilot}))
        pg.wait_for_timeout(1500)
        stun = None
        for k in range(400):
            r = pg.evaluate(STEP, {'n': 10}); samples.append(r); pg.wait_for_timeout(5)
            sc = r.get('scene')
            if sc and not sc['done']:
                tag = str(sc['kind'])
                key = {'COLE': 'cole', 'callisto': 'callisto', 'demo': 'demo'}.get(tag, 'team')
                if key == 'cole' and 'rage' not in grabs:
                    rk = pg.evaluate("()=>{const B=fb2Talk.beats[fb2Talk.i];return !!(B&&B.rage)}")
                    if rk: key = 'rage'
                if key not in grabs and (key != 'callisto' or pg.evaluate("()=>fb2Talk.t>2.6")) and (key != 'demo' or pg.evaluate("()=>fb2Talk.t>.8")):
                    grabs[key] = pg.evaluate("()=>document.querySelector('#screen').toDataURL('image/png')")
                if stun is None:
                    x0 = pg.evaluate("()=>player.x"); pg.keyboard.down('ArrowRight'); pg.evaluate(STEP, {'n': 25}); pg.keyboard.up('ArrowRight')
                    stun = (x0, pg.evaluate("()=>player.x"))
            if r['choice'] and k > 5 and (not sc or sc['done']):
                pg.evaluate(STEP, {'n': 10}); break
        L = pg.evaluate("()=>window.__L")
        b.close()
    stop()
    for kk, d in grabs.items():
        with open(os.path.join(a.out, '%s_%s.png' % (a.pilot, kk)), 'wb') as fh: fh.write(base64.b64decode(d.split(',', 1)[1]))
    sc_samples = [s for s in samples if s.get('scene') and not s['scene']['done']]
    print('scene seen', L.get('sceneSeen'), 'beats', L.get('beatsN'), 'max beat', L.get('maxI'), 'choice during', L.get('choiceDuring'), 'choice after', L.get('choiceAfter'))
    print('rage keys', sorted(k for k in L['keys'] if 'rage' in k), 'texts', L['texts'], 'tints', L['tints'], 'beeps', L['beeps'])
    print('demo fired', L.get('demoFired'), 'fusion released', L.get('released'), 'weapon after', L.get('weaponAfter'), 'stun', stun, 'hits', L['hits'])
    if not L.get('sceneSeen'): fails.append('the team scene never started')
    if L.get('choiceDuring'): fails.append('the choice opened during the scene')
    if not L.get('choiceAfter'): fails.append('the choice never followed the scene')
    if sc_samples and not sc_samples[-1]['stateT'] > sc_samples[0]['stateT']: fails.append('stateT did not advance (paused)')
    if stun and abs(stun[1] - stun[0]) > .5: fails.append('the pilot moved during the scene')
    if len([k for k in L['keys'] if 'rage' in k]) < 2: fails.append('Cole\'s shouting frames did not animate')
    if L['hits']: fails.append('the pilot was hit during the scene')
    if a.pilot == 'cole':
        if not any('CALLISTO' in t for t in L['texts']): fails.append('no SECRET WEAPON CALLISTO lettering')
        if not any('ACTIVATED' in t for t in L['texts']): fails.append('no ACTIVATED lettering')
        if '#39ff5a' not in L['tints']: fails.append('ACTIVATED is not green')
        if L['beeps'] < 5: fails.append('fewer than five beeps (%d)' % L['beeps'])
        if not L.get('released'): fails.append('the fusion cannon never released')
        if not (L.get('demoFired') or 0) > 0: fails.append('the level-7 laser fired nothing')
        if L.get('weaponAfter') != [1, 3]: fails.append('weapon not restored after the demo: %s' % L.get('weaponAfter'))
    else:
        if L['texts']: fails.append('Callisto played for a pilot who is not Cole')
    print('errors', errs[:4])
    if errs: fails.append('page errors')
    print('FAIL' if fails else 'PASS', fails)


if __name__ == '__main__':
    main()
