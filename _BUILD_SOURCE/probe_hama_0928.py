#!/usr/bin/env python3
"""probe_hama_0928.py - the HAMA password, played in real Chromium against the real game loop.

The song's clock is PINNED: the real <audio> element keeps loading and decoding, but its currentTime and
paused are own-property getters the probe advances by exactly 1/60 s per stepped frame, so every cue
(STOP, HAMMER, TIME, the breakdowns) lands on a known frame and the run is repeatable. The game reads the
music clock the way it always does (ht27Clock), so nothing in the encounter is bypassed.

Records per frame: mode, pose, lock state, every slam (clock + word), every caption, every toss beat,
every thrown robot, and every XART key the boss draw asks for (identifies which authored plate drew -
never a size or a src check). Saves frames at each beat worth looking at. Exit 1 on any failure.
"""
import os, sys, json, base64, http.server, argparse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
http.server.SimpleHTTPRequestHandler.log_message = lambda *a: None
import shoot as sh
from playwright.sync_api import sync_playwright

OUT = os.path.join(sh.GAME, '_shots', 'opus0928', 'hama'); N = {'ok': 0}; FAILS = []
def ok(c, m):
    if c: N['ok'] += 1; print('  ok   ' + m, flush=True)
    else: FAILS.append(m); print('  FAIL ' + m, flush=True)

BOOT = r"""
(c) => {
  diffKey=c.diff;DIFF=DIFFS[c.diff];debugFight=null;coopOn=false;setState(GS.PASSWORD);pwInput='hama';submitPassword();
  const routed={pending:ht27Pending&&hamaPending,stage:PENDING_STAGE,state,variant:ht27Variant===HAMA_VARIANT};
  pilotIndex=PILOTS.findIndex(p=>p.key===(c.pilot||'maverick'));startRun(PENDING_STAGE);
  const m=Snd.music.hama;window.__hamaT=0;
  Object.defineProperty(m,'currentTime',{configurable:true,get(){return window.__hamaT;},set(v){window.__hamaT=v;}});
  Object.defineProperty(m,'paused',{configurable:true,get(){return false;}});
  window.__hits=0;window.playerHit=function(){window.__hits++;};
  window.__log={slams:[],lines:[],keys:{},modes:{},poses:{},tossHeld:0,thrown:0,thrownHit:0,locked:0,lockedFrames:[],maxThrown:0};
  const L=window.__log;
  const sl=hamaSlam;hamaSlam=function(b,d,w){L.slams.push({t:+d.clock.toFixed(3),word:w});return sl.apply(this,arguments);};
  const sg=hamaSing;hamaSing=function(d,who,text){L.lines.push({t:+d.clock.toFixed(2),who,text});return sg.apply(this,arguments);};
  const xg=XART.get.bind(XART);XART.get=function(k){if(window.__rec)L.keys[k]=(L.keys[k]||0)+1;return xg(k);};
  return {routed,active:ht27Active,hama:hamaOn(),kind:boss&&boss.kind,hp:boss&&boss.hp};
}
"""
RUN = r"""
(n) => { const L=window.__log;let err=null;
  if(!Number.isFinite(window.__bofStepNow))window.__bofStepNow=performance.now();
  for(let i=0;i<n;i++){
    if(boss&&boss._hammerTime&&boss._hammerTime.musicStarted)window.__hamaT+=1/60;
    window.__bofStepNow+=1000/60;
    try{loop(window.__bofStepNow);}catch(e){err=String(e&&e.message||e);break;}
    const d=boss&&boss._hammerTime;if(!d||!d.hama)continue;const H=d.hama;
    L.modes[d.mode]=(L.modes[d.mode]||0)+1;if(H.pose)L.poses[H.pose]=(L.poses[H.pose]||0)+1;
    if(ht27Locked()){L.locked++;}
    if(H.toss&&H.toss.held&&!H.toss.thrown)L.tossHeld++;
    L.maxThrown=Math.max(L.maxThrown,H.thrown.length);
  }
  return err; }
"""
STATE = r"""() => { const d=boss&&boss._hammerTime,H=d&&d.hama;
  return {clock:d?+d.clock.toFixed(2):null,mode:d&&d.mode,pose:H&&H.pose,locked:ht27Locked(),shield:d&&d.shield,
    helpers:d?d.helpers.length:0,thrown:H?H.thrown.length:0,hp:boss?Math.round(boss.hp):null,hx:boss?Math.round(boss.x):null,
    px:Math.round(player.x),py:Math.round(player.y),state,music:Snd.cur===Snd.music.hama,lines:H?H.lines.map(l=>l.who+':'+l.text):[]}; }"""

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--diff', default='normal'); a = ap.parse_args()
    os.makedirs(OUT, exist_ok=True)
    port, stop = sh.serve(sh.GAME); errs = []
    with sync_playwright() as pw:
        br = pw.chromium.launch(args=['--no-sandbox', '--mute-audio', '--autoplay-policy=no-user-gesture-required'])
        pg = br.new_page(viewport={'width': 1000, 'height': 1100})
        pg.on('pageerror', lambda e: errs.append('page:' + str(e)[:200]))
        pg.on('console', lambda m: errs.append('console:' + m.text[:200]) if m.type == 'error' or 'draw error' in m.text else None)
        pg.goto('http://127.0.0.1:%d/index.html' % port, wait_until='load', timeout=120000)
        pg.wait_for_function("() => (window.__bofFrames|0)>4", timeout=120000)
        pg.evaluate(sh.TRAP_RAF)
        info = pg.evaluate(BOOT, {'diff': a.diff})
        ok(info['routed']['pending'] and info['routed']['stage'] == 5 and info['routed']['state'] == 'diff' and info['routed']['variant'],
           'HAMA routes through difficulty selection to Stage 5 on the instrumental (%s)' % info['routed'])
        ok(info['active'] and info['hama'] and info['kind'] == 'chromehammer', 'the run starts the Hammer Time encounter as HAMA (%s)' % info)
        # the song and every plate must actually be there before the clock is allowed to move
        for _ in range(60):
            pg.evaluate(RUN, 2); pg.wait_for_timeout(120)
            if pg.evaluate("() => !!(boss&&boss._hammerTime&&boss._hammerTime.musicStarted)"): break
        ok(pg.evaluate("() => boss._hammerTime.musicStarted && Snd.cur===Snd.music.hama && Snd.music.hama.readyState>=2 && Snd.music.hama.src.indexOf('HAMA_Instrumental.mp3')>0"),
           'the instrumental itself is loaded and is the playing track')
        pg.evaluate("() => { XART.rdy('arch_hammer_throw_0926'); XART.rdy('arch_hammer_spin'); window.__rec=true; }"); pg.wait_for_timeout(800)
        def shot(name):
            d = pg.evaluate("() => document.getElementById('screen').toDataURL('image/png')")
            open(os.path.join(OUT, name + '.png'), 'wb').write(base64.b64decode(d.split(',', 1)[1]))
        def jump(t):
            # move the song, then let one frame read it, so the next run_to starts from the new clock
            pg.evaluate("(t) => { window.__hamaT=t; }", t); pg.evaluate(RUN, 1)
        def run_to(t, shots=()):
            shots = sorted(shots)
            while True:
                s = pg.evaluate(STATE)
                if s['clock'] is None or s['clock'] >= t: return s
                nxt = min([x for x in shots if x > s['clock']] + [t])
                n = max(1, min(90, int(round((nxt - s['clock']) * 60))))
                e = pg.evaluate(RUN, n)
                if e: errs.append('step:' + e); return pg.evaluate(STATE)
                pg.wait_for_timeout(25)
                s2 = pg.evaluate(STATE)
                for x in list(shots):
                    if s['clock'] < x <= s2['clock'] + 1e-6: shot('t%06.2f_%s' % (x, s2['mode'])); shots.remove(x)
        # ---- the intro: ship, unfold, moonwalk, shield rising, locked the whole way
        origin = pg.evaluate("() => ({x:player.x,y:player.y})")
        pg.evaluate("() => { for(const a of ['up','fire'])for(const k of keybind[a])Input.keys[k]=true; }")
        run_to(3.0, [1.2]); s = run_to(9.0, [6.0, 8.0])
        ok(s['mode'] == 'intro' and s['pose'] == 'moonwalk' and s['locked'], 'after the unfold he moonwalks, player locked (%s)' % {k: s[k] for k in ('clock', 'mode', 'pose', 'locked')})
        xs = []
        for _ in range(8):
            pg.evaluate(RUN, 14); xs.append(pg.evaluate("() => boss.x"))
        ok(max(xs) - min(xs) > 20, 'the moonwalk glides back and forth (x %s)' % [round(x) for x in xs])
        s = run_to(12.0)
        wall = pg.evaluate("() => { const w=ht27WallBounds(boss._hammerTime);return {rise:+w.rise.toFixed(2),shield:boss._hammerTime.shield}; }")
        ok(wall['shield'] and 0 < wall['rise'] < 1, 'the shield rises while he moonwalks (%s)' % wall)
        s = run_to(HAMA_INTRO - 0.05)
        me = pg.evaluate("() => ({x:player.x,y:player.y,shots:pBullets.length})")
        ok(me['x'] == origin['x'] and me['y'] == origin['y'] and me['shots'] == 0 and s['helpers'] == 4, 'the intro holds the player still and unarmed, four robots arrive (%s)' % me)
        pg.evaluate("() => { for(const k of Object.keys(Input.keys))Input.keys[k]=false; }")
        # ---- the fight opens with the robot toss
        s = run_to(HAMA_INTRO + 0.2)
        ok(not s['locked'] and s['mode'] in ('dance', 'toss'), 'at the verse the fight starts (%s)' % {k: s[k] for k in ('clock', 'mode', 'locked')})
        s = run_to(HAMA_INTRO + 6.0, [HAMA_INTRO + 2.35, HAMA_INTRO + 3.0, HAMA_INTRO + 3.4, HAMA_INTRO + 4.2])
        L = pg.evaluate("() => window.__log")
        ok(L['tossHeld'] > 20, 'he grabs a robot and holds it up while the lane warns (%d frames)' % L['tossHeld'])
        ok(L['maxThrown'] >= 1, 'then chucks it at the player (%d in the air)' % L['maxThrown'])
        ok(any('THI' in l['text'] and l['who'] == 'robot' for l in L['lines']), 'the thrown robot sings on the way in')
        ok(any(l['text'] == 'HOLD MY HAMMER' for l in L['lines']) and L['keys'].get('arch_hammer_spin', 0) > 0,
           'the hammer goes up in the air behind him first (%d hammer_spin draws)' % L['keys'].get('arch_hammer_spin', 0))
        ok(L['keys'].get('arch_hammer_throw_0926', 0) > 20, 'the toss wears the authored empty-handed throw plate (%d draws)' % L['keys'].get('arch_hammer_throw_0926', 0))
        # a thrown robot can be shot down
        shot_down = pg.evaluate("""() => { const d=boss._hammerTime;hamaTossStart(boss,d);const H=d.hama;
          let guard=0;while(!H.thrown.length&&guard++<400){window.__hamaT+=1/60;window.__bofStepNow+=1000/60;loop(window.__bofStepNow);}
          const r=H.thrown[0];if(!r)return {none:true};const hp0=r.hp;
          for(let i=0;i<40&&!r.dead;i++)pBullets.push({x:r.x,y:r.y+10,vx:0,vy:0,w:4,h:8,dmg:9,t:0,kind:'mg'}),window.__hamaT+=1/60,window.__bofStepNow+=1000/60,loop(window.__bofStepNow);
          return {dead:r.dead,hp0,list:H.thrown.length}; }""")
        ok(shot_down.get('dead') is True, 'a thrown robot is shootable and blows up (%s)' % shot_down)
        # ---- STOP ... HAMMER ... TIME!
        for k, st in enumerate(STOPS):
            jump(st - 3.0)
            s = run_to(st + 2.0, [st - 0.3, st + 0.05, st + P + 0.05])
            L = pg.evaluate("() => window.__log")
            sl = [x for x in L['slams'] if st - 0.5 < x['t'] < st + 2]
            ok(len(sl) == 2 and sl[0]['word'] == 'HAMMER' and sl[1]['word'] == 'TIME!' and abs(sl[0]['t'] - st) < 0.02 and abs(sl[1]['t'] - (st + P)) < 0.02,
               'STOP at %.2f: two ground slams, on HAMMER (%.3f) and on TIME (%.3f) - got %s' % (st, st, st + P, sl))
            ok(any(l['text'] == 'STOP!' and st - 1 < l['t'] < st for l in L['lines']), '  ...and he calls STOP! a beat before')
        lk = pg.evaluate("(t) => { window.__hamaT=t; window.__bofStepNow+=1000/60; loop(window.__bofStepNow); return {locked:ht27Locked(),mode:boss._hammerTime.mode,pose:boss._hammerTime.hama.pose}; }", STOPS[0] + 0.1)
        ok(lk['locked'] and lk['mode'] == 'break', 'the STOP freezes the player for the double slam (%s)' % lk)
        # ---- the breakdown
        b0, b1 = BREAKS[0]
        jump(b0 - 1.0)
        pg.evaluate("() => { window.__log.poses={}; window.__log.modes={}; window.__log.keys={}; }")
        s = run_to(b0 + 8.0, [b0 + 1.2, b0 + 2.2, b0 + 3.2, b0 + 3.9, b0 + 4.3])
        L = pg.evaluate("() => window.__log")
        ok(L['modes'].get('breakdown', 0) > 300 and L['poses'].get('lasso', 0) > 60 and L['poses'].get('spin', 0) > 60,
           'the breakdown alternates lasso bars and jump-turn bars (%s)' % L['poses'])
        chants = [l['text'] for l in L['lines'] if b0 <= l['t'] < b0 + 8]
        ok(chants.count('OH!') >= 4 and 'OH-OH!' in chants and 'OH-OH-OH!' in chants and 'BREAK IT DOWN!' in chants,
           'they chant OH, OH-OH, OH-OH-OH on the beat (%d chants)' % len(chants))
        bd = pg.evaluate("() => { const d=boss._hammerTime;hitBoss(500);return {shield:d.shield,hp:Math.round(boss.hp),locked:ht27Locked()}; }")
        ok(bd['shield'] and not bd['locked'], 'the shield is up and the player flies free during the breakdown (%s)' % bd)
        # ---- the chorus, the hammer jumps
        jump(CHORUS)
        s = run_to(CHORUS + 8.0)
        L = pg.evaluate("() => window.__log")
        ok(sum(1 for l in L['lines'] if l['text'] == 'CANT TOUCH THIS' and CHORUS <= l['t'] < CHORUS + 8) >= 3, 'the chorus is sung on the bar')
        leap = pg.evaluate("""() => { const b=boss,d=b._hammerTime;d.mode='attack';hammerTarget(b);hammerState(b,'warn');
          let g=0;while(b._hammer.state!=='leap'&&g++<400){window.__hamaT+=1/60;window.__bofStepNow+=1000/60;loop(window.__bofStepNow);}
          let g2=0;while(b._hammer.state==='leap'&&g2++<400){window.__hamaT+=1/60;window.__bofStepNow+=1000/60;loop(window.__bofStepNow);}
          return window.__log.lines.slice(-8).map(l=>l.who+':'+l.text); }""")
        ok('boss:AHHH-WOOO!' in leap and 'crew:HEY!' in leap, 'the hammer jump is sung: AHHH-WOOO! up, HEY! down (%s)' % leap)
        pg.evaluate("() => { window.__rec=false; }")
        # ---- HAMMER still plays Mike's remix
        pg.evaluate("() => { setState(GS.TITLE); }"); pg.evaluate(RUN, 2)
        ham = pg.evaluate("() => { setState(GS.PASSWORD);pwInput='HAMMER';submitPassword();startRun(PENDING_STAGE);return {variant:ht27Variant,song:ht27SongName(),hama:hamaOn(),active:ht27Active}; }")
        ok(ham['active'] and ham['variant'] is None and ham['song'] == 'hammerTime' and not ham['hama'], 'HAMMER still runs Mike\'s remix, untouched (%s)' % ham)
        pg.evaluate("() => { setState(GS.TITLE); }"); pg.evaluate(RUN, 2)
        ok(pg.evaluate("() => !ht27Active && ht27Variant===null && Snd.cur!==Snd.music.hama"), 'leaving to the title stops the song and clears the route')
        br.close()
    stop()
    ok(not errs, 'no page, console, draw or step errors (%s)' % errs[:3])
    print('%d ok / %d fail' % (N['ok'], len(FAILS)))
    sys.exit(1 if FAILS else 0)

# the cue sheet the probe checks against is read from the generated file, not retyped
_art = open(os.path.join(sh.GAME, 'assets', 'hama_art_0928.js')).read()
_A = json.loads(_art.split('=', 1)[1].rstrip().rstrip(';'))['audio']
P = 60 / _A['bpm']
HAMA_INTRO = next(s['t1'] for s in _A['sections'] if s['kind'] == 'intro')
STOPS = []
for t, l in _A['stops']:
    if STOPS and t - STOPS[-1] < 12: continue
    STOPS.append(t)
BREAKS = [(s['t0'], s['t1']) for s in _A['sections'] if s['kind'] == 'breakdown']
CHORUS = next(s['t0'] for s in _A['sections'] if s['kind'] == 'chorus') + 0.05

if __name__ == '__main__':
    main()
