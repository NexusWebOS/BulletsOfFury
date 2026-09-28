#!/usr/bin/env python3
"""probe_rebel_fury_0928.py - the Stage 6 REBEL FURY fight (the right-hand route's boss), in real Chromium.

Mike 0928: "ensure the fury fight is great for stage 6". This measures the fight as the route plays it:
Stage 6 with the Fury Wing split to the right (four allies stay), the rebel squad spawned by the same
spawnBoss call the stage makes, the pilot parked under the weakest rebel with FIRE held through the real
input path (immune; would-be hits are counted, never applied). Per second it records every rebel's mode,
hp, cast/cloak state, the rounds on screen and the would-be hits; every attack is logged by wrapping the
squad's own turn/attack functions; screenshots every few seconds.

  python3 _BUILD_SOURCE/probe_rebel_fury_0928.py --diff normal --seconds 150
"""
import os, sys, json, base64, argparse, http.server
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
http.server.SimpleHTTPRequestHandler.log_message = lambda *a: None
import shoot as sh
from playwright.sync_api import sync_playwright

SETUP = r"""
(c) => {
  diffKey=c.diff;DIFF=DIFFS[c.diff];run.mode='arcade';run.pilot=c.pilot;run.stage=6;curStage=STAGES[5];
  beginStage(6);setState(GS.PLAY);player.reset();story=null;special=null;
  stagePlan=[];waveIdx=999;spawnClock=9999;enemies=[];eBullets=[];pBullets=[];powerups=[];
  boss=null;bossActive=false;subBoss=null;subBossActive=false;subBossDone=true;bossDefeated=false;
  s6Opening=null;
  if(c.wing){
    s6WingInit();const W=s6Wing;W.beats=2;W.all=true;W.fakeDone=true;W.choice=true;W.route='right';W.supplyIndex=3;
    s6WingLaunch(8,true);
    for(const q of W.ships){q.all=true;if((q.slot&1)===0){q.phase='leave';}else{q.phase='fight';q.y=VH*.72;q.t=2;}}
  }else s6Wing=null;
  if(c.weapon!=null){run.weapon=c.weapon;run.wlevel=c.level||3;}
  if(typeof groundTargetingReset==='function')groundTargetingReset();if(typeof tb28Reset==='function')tb28Reset();
  mapScroll=Math.min(1200,levelScrollRange()*.5);player.x=camLeftX()+viewW()/2;player.y=VH*.80;
  window.__hits=0;window.playerHit=function(){window.__hits++;};
  window.__log=[];
  const T=()=>+(boss&&boss._rebels?boss._rebels.t:0).toFixed(2);
  if(!window.__wrapped){window.__wrapped=true;
    const rt=rival27Turn;rival27Turn=function(R,q){const r=rt(R,q);if(r)window.__log.push({t:T(),k:q.key,ev:'turn'});return r;};
    const fa=fr27RebelAttack;fr27RebelAttack=function(q,R){const r=fa(q,R);window.__log.push({t:T(),k:q.key,ev:r?(q.rfSig?'sig-'+q.rfSig.kind:q.frCast?'cast-'+q.frCast.kind:q.frCloak>0?'cloak':'claim'):(q.i%3===0?'fan':q.i%3===1?'lightning':'dash')});return r;};
    if(typeof rf28FormStart==='function'){const fs=rf28FormStart;rf28FormStart=function(b,R,kind){window.__log.push({t:T(),k:'squad',ev:'form-'+kind,alive:R.ships.filter(q=>!q.dead).length});return fs(b,R,kind);};}
    if(typeof rf28Fallen==='function'){const ff=rf28Fallen;rf28Fallen=function(b,R,q){const r=ff(b,R,q);window.__log.push({t:T(),k:q.key,ev:'fallen',last:!!R.rf.lastStand});return r;};}
  }
  spawnBoss('rebelsquad');bossActive=true;window.__B=boss;
  if(c.skipIntro){const R=boss._rebels;R.frIntro={t:29,beat:4,done:true};boss._noHit=false;R.t=0;R.releaseAt=1.6;
    for(const q of R.ships){q.x=q.homeX;q.y=q.homeY;q.mode='fight';q.t=0;q.cd=1.6+q.i*.4;}}
  return {name:boss.name,hp:Math.round(boss.hp),maxhp:Math.round(boss.maxhp),weapon:run.weapon,wlevel:run.wlevel,
    allies:s6Wing?s6Wing.ships.filter(q=>q.phase==='fight').map(q=>q.key):[]};
}
"""

AUTOPILOT = r"""
() => { window.__qaTick = () => {
  if(!boss||!boss._rebels)return; const R=boss._rebels;
  const live=R.ships.filter(q=>!q.dead&&q.mode!=='entry');
  if(!live.length){Input.keys.j=false;return;}
  live.sort((a,b)=>a.hp-b.hp); const q=live[0];
  const tx=clamp(q.x,camLeftX()+30,camRightX()-30), ty=clamp(q.y+230,PLAY.y+140,PLAY.y+PLAY.h-30);
  player.x+=clamp(tx-player.x,-5,5); player.y+=clamp(ty-player.y,-5,5); Input.keys.j=true;
}; }
"""

SAMPLE = r"""
() => { if(!boss||!boss._rebels)return {gone:true,state,hits:window.__hits};
  const R=boss._rebels;
  return {t:+R.t.toFixed(1),intro:!!(R.frIntro&&R.frIntro.done),hp:Math.round(boss.hp),dead:!!boss.dead,state,
    form:R.rf&&R.rf.form?R.rf.form.kind+':'+R.rf.form.phase:null,last:!!(R.rf&&R.rf.lastStand),
    ships:R.ships.map(q=>({k:q.key,m:q.mode,hp:Math.round(q.hp),max:Math.round(q.max),dead:!!q.dead,cast:q.frCast?q.frCast.kind:null,cloak:(q.frCloak||0)>0,
      sig:q.rfSig?q.rfSig.kind+':'+q.rfSig.phase:null,sh:Math.round(q.shield||0),shm:Math.round(q.shieldMax||0),
      mods:(q.frModules||[]).map(m=>Math.round(m.hp)),x:Math.round(q.x),y:Math.round(q.y)})),
    eb:eBullets.length,gt:groundTargetingFx.length,hits:window.__hits,
    allies:s6Wing?s6Wing.ships.filter(q=>q.phase==='fight').length:0,pb:pBullets.length};
}
"""

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--diff', default='normal')
    ap.add_argument('--pilot', default='maverick')
    ap.add_argument('--seconds', type=int, default=150)
    ap.add_argument('--no-wing', action='store_true')
    ap.add_argument('--intro', action='store_true', help='play the radio intro instead of skipping it')
    ap.add_argument('--weapon', type=int, default=None)
    ap.add_argument('--level', type=int, default=3)
    ap.add_argument('--shots', type=float, default=5.0, help='seconds between screenshots')
    ap.add_argument('--tag', default='')
    a = ap.parse_args()
    out = os.path.join(sh.GAME, '_shots', 'opus0928', 'rebel_fury', a.diff + (a.tag and '_' + a.tag))
    os.makedirs(out, exist_ok=True)
    port, stop = sh.serve(sh.GAME)
    errs = []
    with sync_playwright() as pw:
        br = pw.chromium.launch(args=['--no-sandbox', '--mute-audio'])
        pg = br.new_page(viewport={'width': 1000, 'height': 1100})
        pg.on('pageerror', lambda e: errs.append('page:' + str(e)[:220]))
        pg.on('console', lambda m: errs.append('console:' + m.text[:220]) if m.type == 'error' or 'draw error' in m.text else None)
        pg.goto('http://127.0.0.1:%d/index.html' % port, wait_until='load', timeout=120000)
        pg.wait_for_function("() => (window.__bofFrames|0)>4", timeout=120000)
        pg.evaluate(sh.TRAP_RAF)
        info = pg.evaluate(SETUP, {'diff': a.diff, 'pilot': a.pilot, 'wing': not a.no_wing, 'weapon': a.weapon, 'level': a.level, 'skipIntro': not a.intro})
        print('setup', json.dumps(info), flush=True)
        # let the rebel plates decode before the clock starts
        pg.evaluate("() => { for(const id of REBEL_SHIPS){XART.rdy('rr_ship_'+id);for(let f=0;f<8;f++)XART.rdy('rr_roll_'+id+'_'+f);} }")
        pg.wait_for_timeout(1500)
        pg.evaluate(AUTOPILOT)
        samples = []; nextShot = 0.0; t = 0.0; killed = None
        while t < a.seconds:
            e = pg.evaluate(sh.STEP, 30)
            if e: errs.append('step:' + e)
            pg.wait_for_timeout(25)
            t += .5
            if abs(t - round(t)) < 1e-6:
                s = pg.evaluate(SAMPLE); s['wall'] = t; samples.append(s)
                if s.get('gone') or s.get('dead'):
                    if killed is None: killed = t
            if t >= nextShot:
                d = pg.evaluate("() => document.getElementById('screen').toDataURL('image/png')")
                open(os.path.join(out, 'f_%05.1f.png' % t), 'wb').write(base64.b64decode(d.split(',', 1)[1]))
                nextShot += a.shots
            if killed is not None and t >= killed + 3: break
        log = pg.evaluate("() => window.__log")
        br.close()
    stop()
    json.dump({'info': info, 'samples': samples, 'log': log, 'errs': errs[:20], 'killed': killed}, open(os.path.join(out, 'run.json'), 'w'), indent=1)
    # summary
    print('killed at', killed, 'errors', len(errs))
    for s in samples[::5]:
        if s.get('gone'): print('%5.1f gone state=%s hits=%d' % (s['wall'], s['state'], s['hits'])); continue
        print('%5.1f t=%5.1f hp=%5d eb=%3d gt=%2d hits=%3d allies=%d form=%-14s %s' % (s['wall'], s['t'], s['hp'], s['eb'], s['gt'], s['hits'], s['allies'], s.get('form') or '-',
              ' '.join('%s:%s%s%s' % (q['k'][:3], 'X' if q['dead'] else q['m'][:2], '' if q['dead'] else '%d' % q['hp'], ('/s%d' % q['sh']) if q.get('shm') else '') for q in s['ships'])), flush=True)
    kinds = {}
    for e in log:
        if e['ev'] != 'turn': kinds[e['k'] + ':' + e['ev']] = kinds.get(e['k'] + ':' + e['ev'], 0) + 1
    print('attacks', json.dumps(kinds, sort_keys=True))
    print('events', [(e['t'], e['k'], e['ev']) for e in log if e['ev'].startswith(('form', 'fallen', 'sig'))][:60])
    for e in errs[:8]: print('ERR', e)

if __name__ == '__main__':
    main()
