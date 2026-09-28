#!/usr/bin/env python3
"""probe_hammer_counter_0928.py - Mike 0928: "shooting the missile into his hammer didnt cause the animation
and effect to stop the healing and bring him to his stun state" (Stage 5, tested on Furious).

For each difficulty the Chrome Hammer is brought into its heal the game's own way (hammerStormStart on
Normal/Hard, fr27Restore on Furious), the pilot is parked under the raised hammer, and a real manual missile
(useBomb) is fired - once unlocked, once with the Retina locked on the hammer. Records the heal status, the
boss state, what happened to the missile (hit / reflected by the barrier / still flying) and the hp change.
"""
import os, sys, json, http.server, base64
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
http.server.SimpleHTTPRequestHandler.log_message = lambda *a: None
import shoot as sh
from playwright.sync_api import sync_playwright

OUT = os.path.join(sh.GAME, '_shots', 'opus0928', 'hammer_counter')
SETUP = r"""
(c) => {
  diffKey=c.diff;DIFF=DIFFS[c.diff];run.mode='arcade';run.pilot='maverick';run.stage=5;curStage=STAGES[4];
  beginStage(5);setState(GS.PLAY);player.reset();story=null;special=null;
  stagePlan=[];waveIdx=999;spawnClock=9999;enemies=[];eBullets=[];pBullets=[];powerups=[];
  boss=null;bossActive=false;subBoss=null;subBossActive=false;subBossDone=true;
  window.__hits=0;window.playerHit=function(){window.__hits++;};
  spawnBoss(curStage.boss);bossActive=true;const b=boss;b.enter=false;b._noHit=false;
  if(b._hammerTime){b._hammerTime.mode='attack';b._hammerTime.shield=false;}
  const h=b._hammer;h.balance0922=true;
  window.__B=b;return {kind:b.kind,state:h.state,hp:Math.round(b.hp),maxhp:Math.round(b.maxhp),ht:!!b._hammerTime};
}
"""
HEAL = r"""
(c) => { const b=window.__B,h=b._hammer;
  if(c.diff==='furious'){ const A=h.frArmor; if(A){ A.hp=A.max*.4; } fr27Restore(b,.10,false,true); }
  else { b.hp=b.maxhp*.6; hammerStormStart(b); }
  return {state:h.state,status:h.recovery&&h.recovery.status,fr:!!(h.recovery&&h.recovery.fr),barrier:h.frArmor?h.frArmor.barrier:null};
}"""
READ = r"""() => { const b=window.__B,h=b._hammer,R=h.recovery,A=h.frArmor;
  const m=pBullets.filter(q=>q.kind==='gmiss'&&!q.dead);
  const hd=typeof hammerHeadPoint==='function'?hammerHeadPoint(b):null;
  return {state:h.state,status:R&&R.status,elapsed:R?+R.elapsed.toFixed(2):null,hp:Math.round(b.hp),armor:A?Math.round(A.hp):null,
    barrier:A?+A.barrier.toFixed(2):null,missiles:m.map(q=>({x:Math.round(q.x),y:Math.round(q.y)})),head:hd?{x:Math.round(hd.x),y:Math.round(hd.y)}:null,
    rev:(window.__rev||0),burst:!!h.coreBurst,destroyed:!!h.hammerDestroyed};}"""

def main():
    os.makedirs(OUT, exist_ok=True)
    port, stop = sh.serve(sh.GAME)
    rows = []; allok = True
    with sync_playwright() as pw:
        br = pw.chromium.launch(args=['--no-sandbox', '--mute-audio'])
        for diff in ('normal', 'hard', 'furious'):
            for lock in (False, True):
                pg = br.new_page(viewport={'width': 1000, 'height': 1100}); errs = []
                pg.on('pageerror', lambda e: errs.append(str(e)[:200]))
                pg.goto('http://127.0.0.1:%d/index.html' % port, wait_until='load', timeout=120000)
                pg.wait_for_function("() => (window.__bofFrames|0)>4", timeout=120000)
                pg.evaluate(sh.TRAP_RAF)
                info = pg.evaluate(SETUP, {'diff': diff})
                # let armor activation (Furious) / the arrival finish, with real pauses for decode
                for _ in range(40):
                    pg.evaluate(sh.STEP, 30); pg.wait_for_timeout(40)
                    if pg.evaluate("() => { const h=window.__B._hammer; return !['flyby','return','unfold','fr_activation'].includes(h.state) && (diffKey!=='furious' || !!(h.frArmor&&h.frArmor.activated)); }"): break
                heal = pg.evaluate(HEAL, {'diff': diff})
                pg.evaluate(sh.STEP, 70); pg.wait_for_timeout(40)   # the hammer is up and the heal is flowing
                pre = pg.evaluate(READ)
                pg.evaluate("""(lock) => { const b=window.__B,hd=hammerHeadPoint(b);player.x=hd.x;player.y=Math.min(PLAY.y+PLAY.h-30,hd.y+230);player.invuln=0;
                  run.bombs=9; let tgt=undefined;
                  if(lock){ const t=(typeof retinaBossTargets==='function'?retinaBossTargets(b):[]).find(p=>p.kind==='hammer'||/hammer/i.test(String(p.id||p.key||p.label||'')));
                    tgt=t||null; window.__lockKey=t?String(t.kind||t.id||t.key):null; }
                  useBomb(tgt); }""", lock)
                trace = []
                for i in range(40):
                    pg.evaluate(sh.STEP, 3)
                    trace.append(pg.evaluate(READ))
                    if trace[-1]['status'] != 'charging' and i > 2: break
                if trace[-1]['status'] == 'charging':
                    for i in range(20): pg.evaluate(sh.STEP, 3); trace.append(pg.evaluate(READ))
                d = pg.evaluate("() => document.getElementById('screen').toDataURL('image/png')")
                open(os.path.join(OUT, '%s_%s.png' % (diff, 'lock' if lock else 'free')), 'wb').write(base64.b64decode(d.split(',', 1)[1]))
                last = trace[-1]
                broke = last['status'] == 'cancelled' and last['state'] in ('storm_stun', 'fr_stun')
                allok &= broke
                row = {'diff': diff, 'lock': lock, 'lockKey': pg.evaluate("() => window.__lockKey||null"), 'heal': heal, 'pre': pre,
                       'end': last, 'broke': broke, 'errs': errs, 'trace': trace}
                rows.append(row)
                print('%-8s lock=%-5s heal=%s pre=%s -> status=%s state=%s hp %s->%s burst=%s errs=%d %s' % (
                    diff, lock, heal['status'], pre['state'], last['status'], last['state'], pre['hp'], last['hp'], last['burst'], len(errs),
                    'BROKE' if broke else 'NOT BROKEN'), flush=True)
                pg.close()
        br.close()
    stop()
    json.dump(rows, open(os.path.join(OUT, 'run.json'), 'w'), indent=1)
    print('ALL BROKE' if allok else 'SOME NOT BROKEN')

if __name__ == '__main__':
    main()
