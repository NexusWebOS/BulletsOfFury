#!/usr/bin/env python3
"""probe_hammer_heal_break_0929.py - Mike 0929: "when I shoot the hammer when he charges it to restore his
energy it is still not breaking and bringing him to his stun state and he just keeps the shield up and keeps
doing it. This is bad"

The Stage-5 Chrome Hammer is put into the heal the way the game does it: the base heal (the one after the
chaingun breaks, hammerStormStart) on every difficulty, and the Hard/Furious restoration checkpoint
(fr27Restore) on Hard and Furious. The pilot sits under the raised hammer, below the energy wall, and HOLDS
FIRE with the real fire key (the space guns, through updatePlay's own collision loop) - or launches one manual
missile at the hammer. Then the probe keeps watching for 12 s and records what a player sees:

  - did the heal break (recovery status 'cancelled')
  - how many of the player's rounds the energy wall swallowed while he healed
  - the stun: its state, whether the authored stun pose (stun_0920) and static are DRAWN, and whether the
    shield (frArmor.barrier) is DOWN while he is stunned
  - a body round during the stun does damage (the punish window)
  - whether a NEW heal starts after the stun (the "keeps doing it" loop)
  - page / console errors

    python _BUILD_SOURCE/probe_hammer_heal_break_0929.py [--only normal|hard|furious] [--secret]

Exit 1 on any failed expectation.
"""
import os, sys, json, base64, argparse, http.server
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
http.server.SimpleHTTPRequestHandler.log_message = lambda *a, **k: None   # the asset server's request log is noise
import shoot as sh
from playwright.sync_api import sync_playwright

OUT = os.path.join(sh.GAME, '_shots', 'hammer_heal_break_0929')

SETUP = r"""
(c) => {
  if (typeof ht27Stop === 'function') ht27Stop();
  diffKey=c.diff; DIFF=DIFFS[c.diff]; run.mode='arcade'; run.pilot='maverick';
  pilotIndex=PILOTS.findIndex(p=>p.key==='maverick');
  if (c.secret) { ht27Pending=true; startRun(5); const d=boss._hammerTime; d.mode='attack'; d.locked=false; d.shield=false; d.musicStarted=true; d.clock=40;
                  try{ Snd.music.hammerTime.pause(); }catch(e){} }
  else { run.stage=5; curStage=STAGES[4]; beginStage(5); spawnBoss(curStage.boss); bossActive=true; }
  setState(GS.PLAY); player.reset(); story=null; special=null;
  stagePlan=[]; waveIdx=999; spawnClock=9999; enemies=[]; eBullets=[]; pBullets=[]; powerups=[];
  l5Rocks=[]; l5RockT=9999;   /* the Stage-5 asteroid field eats a missile at random (as the 0926 hammer probes found) */
  subBoss=null; subBossActive=false; subBossDone=true; subBossTriggered=true;
  window.__hits=0; playerHit=function(){ window.__hits++; };
  const b=boss; b.enter=false; b._noHit=false; b._hammer.balance0922=true;
  window.__B=b;
  /* every blit the boss draw asks for, by KEY (XART.get returns a fresh canvas: never identify by .src) */
  window.__arch=[]; const ab=archBlit;
  archBlit=function(k){ if(window.__archOn) window.__arch.push(String(k)); return ab.apply(this,arguments); };
  window.__stunFx=0; const se=hammerStunEffectsDraw;
  hammerStunEffectsDraw=function(){ if(window.__archOn) window.__stunFx++; return se.apply(this,arguments); };
  /* rounds the energy wall swallowed */
  window.__reflected=0;
  if (typeof fr27Reflect==='function'){ const fr=fr27Reflect;
    fr27Reflect=function(b,A,dt){ const n=pBullets.filter(q=>!q.dead).length; const r=fr.apply(this,arguments);
      window.__reflected+=n-pBullets.filter(q=>!q.dead).length; return r; }; }
  for (const k of Object.keys(Input.keys)) Input.keys[k]=false;
  return {kind:b.kind, state:b._hammer.state, hp:Math.round(b.hp), maxhp:Math.round(b.maxhp), secret:!!b._hammerTime,
          space: typeof spaceWeaponsActive==='function' ? spaceWeaponsActive() : null};
}
"""

SETTLED = r"""() => { const h=window.__B._hammer;
  return !['flyby','return','unfold','fr_activation'].includes(h.state) && (!['hard','furious'].includes(diffKey) || !!h.frArmor) &&
         (diffKey!=='furious' || !!(h.frArmor && h.frArmor.activated)); }"""

HEAL = r"""
(c) => { const b=window.__B, h=b._hammer, A=h.frArmor;
  b.hp=b.maxhp*.55; b.x=(camLeftX()+camRightX())/2; b.y=VH*.34;
  if (A) { A.rage=false; A.stunCritical=false; }
  /* the checkpoint exactly as the Hard/Furious tick fires it: it marks the half-armor / HP threshold as USED, then
     restores. (A probe that skips the mark sees the same checkpoint fire again and calls it a re-heal.) */
  /* HAMMER: the checkpoint fires between moves, i.e. usually while its crew is DANCING - the case that drew the
     whole heal and stun as dance poses. Put it there on purpose. */
  if (c.route==='checkpoint' && b._hammerTime) ht27DanceStart(b,b._hammerTime,1.9);
  if (c.route==='checkpoint') { if (A && A.hp>0) { A.hp=A.max*.40; A.half=true; }
    else if (A) { const r=b.hp/b.maxhp, th=[.75,.50,.35,.15].find(v=>r<=v&&!A.checkpoints.includes(v)); if (th!=null) A.checkpoints.push(th); }
    fr27Restore(b,.10,false,true); }
  else { h.mode='chaingun'; hammerStormStart(b); }
  window.__R=h.recovery;
  return {state:h.state, status:h.recovery.status, fr:!!h.recovery.fr, core:Math.round(h.recovery.coreHP), barrier:A?+A.barrier.toFixed(2):null};
}"""

READ = r"""() => { const b=window.__B, h=b._hammer, R=h.recovery, A=h.frArmor, hd=hammerHeadPoint(b);
  return {t:+(window.__bofStepNow/1000).toFixed(2), state:h.state, mode:h.mode, status:R?R.status:null, same:R===window.__R,
    core:R?Math.round(R.coreHP):null, hp:Math.round(b.hp), armor:A?Math.round(A.hp):null, barrier:A?+A.barrier.toFixed(2):null,
    head:{x:Math.round(hd.x),y:Math.round(hd.y)}, bx:Math.round(b.x), by:Math.round(b.y), refl:window.__reflected,
    dead:!!b.dead};}"""

def run_case(br, port, diff, route, weapon, secret, old=None, label=''):
    pg = br.new_page(viewport={'width': 1000, 'height': 1100}); errs = []
    if old:   # the busted arm: serve the pre-fix furious_review_0927.js in place of the repo copy
        pg.route('**/assets/furious_review_0927.js', lambda r: r.fulfill(path=old, content_type='application/javascript'))
    pg.on('pageerror', lambda e: errs.append('pageerror: ' + str(e)[:220]))
    pg.on('console', lambda m: errs.append('console: ' + m.text[:220]) if m.type == 'error' else None)
    pg.goto('http://127.0.0.1:%d/index.html' % port, wait_until='load', timeout=120000)
    pg.wait_for_function("() => (window.__bofFrames|0)>4", timeout=120000)
    pg.evaluate(sh.TRAP_RAF)
    info = pg.evaluate(SETUP, {'diff': diff, 'secret': secret})
    for _ in range(60):
        pg.evaluate(sh.STEP, 30); pg.wait_for_timeout(40)
        if pg.evaluate(SETTLED): break
    # touch the stun art so it is decoded before it is needed (XART.rdy is false on its first call)
    pg.evaluate("() => { for (const k of ['arch_stun_static_0926','stun_0920']) try{ XART.rdy(k); }catch(e){} }")
    pg.wait_for_timeout(600)
    heal = pg.evaluate(HEAL, {'route': route})
    pg.evaluate(sh.STEP, 20); pg.wait_for_timeout(30)
    # the pilot under the raised hammer, below the energy wall
    pg.evaluate("""(w) => { const b=window.__B, hd=hammerHeadPoint(b); player.x=hd.x; player.y=Math.min(PLAY.y+PLAY.h-40, b.y+160); player.invuln=0;
        for (const k of Object.keys(Input.keys)) Input.keys[k]=false;
        if (w==='gun') Input.keys['j']=true;
        else { run.bombs=9; const t=retinaBossTargets(b).find(t=>t._retinaId==='hammer'); useBomb(t||undefined); }
        window.__archOn=true; }""", weapon)
    timeline = []; shot = {}
    stun_seen = None; stun_rows = []; body_dmg = None
    for i in range(12 * 60 // 6):
        # keep the pilot under the hammer (the fight moves him) and keep firing - until the heal breaks; after
        # that the probe only WATCHES, so a later heal can only come from the boss, not from a pilot still shooting
        if stun_seen is None:
            pg.evaluate("""(w) => { const b=window.__B, hd=hammerHeadPoint(b); if (w==='gun') { Input.keys['j']=true; player.x=hd.x; player.y=Math.min(PLAY.y+PLAY.h-40, b.y+160); } }""", weapon)
        e = pg.evaluate(sh.STEP, 6)
        if e: errs.append('STEP: ' + e)
        r = pg.evaluate(READ); timeline.append(r)
        if r['status'] == 'cancelled' and stun_seen is None and r['same']:
            stun_seen = len(timeline)
            # stop firing: the probe now watches the stun and what follows it
            pg.evaluate("() => { for (const k of Object.keys(Input.keys)) Input.keys[k]=false; window.__arch=[]; window.__stunFx=0; }")
        if stun_seen is not None and len(timeline) - stun_seen == 6:        # ~0.6 s into the stun
            d = pg.evaluate("() => document.getElementById('screen').toDataURL('image/png')")
            shot['stun'] = d
            stun_rows = pg.evaluate("() => ({arch:window.__arch.slice(), fx:window.__stunFx})")
            # one body round in the stun: the punish window
            body_dmg = pg.evaluate("""() => { const b=window.__B, A=b._hammer.frArmor, hp0=b.hp, a0=A?A.hp:0;
                pBullets.push({x:b.x, y:b.y+20, vx:0, vy:0, w:4, h:8, dmg:10, t:0});
                for (let i=0;i<2;i++) updatePlay(1/60);
                return {hp:+(hp0-b.hp).toFixed(1), armor:+(a0-(A?A.hp:0)).toFixed(1), state:b._hammer.state}; }""")
        if i == 8 and 'heal' not in shot:
            shot['heal'] = pg.evaluate("() => document.getElementById('screen').toDataURL('image/png')")
    pg.evaluate("() => { for (const k of Object.keys(Input.keys)) Input.keys[k]=false; }")
    tag = '%s_%s_%s%s%s' % (diff, route, weapon, '_secret' if secret else '', ('_' + label) if label else '')
    for k, d in shot.items():
        open(os.path.join(OUT, '%s_%s.png' % (tag, k)), 'wb').write(base64.b64decode(d.split(',', 1)[1]))
    pg.close()
    broke = stun_seen is not None
    stunned = [r for r in timeline[stun_seen:] if r['state'] in ('storm_stun', 'fr_stun', 'hammer_stun')] if broke else []
    after = timeline[stun_seen:] if broke else []
    # a NEW heal after the break = the recovery object was replaced by one that is charging again
    reheal = [r for r in after if r['status'] == 'charging' and not r['same']]
    shield_in_stun = max([r['barrier'] or 0 for r in stunned], default=0)
    stun_len = len(stunned) * 6 / 60.0
    resumed = next((r['state'] for r in after if r['state'] not in ('storm_stun', 'fr_stun', 'hammer_stun', 'storm_rebuild')), None)
    return {'diff': diff, 'route': route, 'weapon': weapon, 'secret': secret, 'info': info, 'heal': heal, 'broke': broke,
            'breakAt': timeline[stun_seen - 1]['t'] - timeline[0]['t'] if broke else None,
            'reflected': timeline[(stun_seen or len(timeline)) - 1]['refl'],
            'stunStates': sorted(set(r['state'] for r in stunned)), 'stunSec': stun_len, 'shieldInStun': shield_in_stun,
            'stunPoseDrawn': sum(1 for k in (stun_rows or {}).get('arch', []) if k == 'stun_0920') if broke else 0,
            'stunFx': (stun_rows or {}).get('fx', 0) if broke else 0,
            'bodyDmgInStun': body_dmg, 'reheal': len(reheal) > 0, 'rehealAt': (reheal[0]['t'] - timeline[stun_seen - 1]['t']) if reheal else None,
            'resumed': resumed, 'errs': errs, 'end': timeline[-1], 'timeline': timeline[::5]}

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--only'); ap.add_argument('--secret', action='store_true'); ap.add_argument('--json'); ap.add_argument('--old'); ap.add_argument('--label', default=''); ap.add_argument('--route'); ap.add_argument('--weapon')
    a = ap.parse_args()
    os.makedirs(OUT, exist_ok=True)
    port, stop = sh.serve(sh.GAME)
    cases = []
    for diff in ('normal', 'hard', 'furious'):
        if a.only and diff != a.only: continue
        routes = ['base'] + (['checkpoint'] if diff in ('hard', 'furious') else [])
        if a.secret: routes = [r for r in routes if r == 'checkpoint']   # HAMMER never reaches the post-chaingun heal
        for route in routes:
            if a.route and route != a.route: continue
            for weapon in ('gun', 'missile'):
                if a.weapon and weapon != a.weapon: continue
                cases.append((diff, route, weapon, a.secret))
    rows = []; fails = 0
    def ok(c, m):
        nonlocal fails
        print(('  ok   ' if c else '  FAIL ') + m, flush=True)
        if not c: fails += 1
    with sync_playwright() as pw:
        br = pw.chromium.launch(args=['--no-sandbox', '--mute-audio'])
        for c in cases:
            r = run_case(br, port, *c, old=a.old, label=a.label); rows.append(r)
            name = '%-7s %-10s %-7s' % (r['diff'], r['route'], r['weapon'])
            print('%s broke=%s at=%s refl=%s stun=%s %.1fs shield=%s pose=%s fx=%s body=%s reheal=%s(%s) resumed=%s errs=%d' % (
                name, r['broke'], r['breakAt'], r['reflected'], r['stunStates'], r['stunSec'], r['shieldInStun'], r['stunPoseDrawn'],
                r['stunFx'], r['bodyDmgInStun'], r['reheal'], r['rehealAt'], r['resumed'], len(r['errs'])), flush=True)
            ok(r['broke'], name + ' shooting the hammer breaks the heal')
            if r['broke']:
                ok(r['stunSec'] >= 2.0, name + ' he goes into a stun (%.1fs)' % r['stunSec'])
                ok(r['stunPoseDrawn'] > 0 and r['stunFx'] > 0, name + ' the stun is DRAWN: stun pose %d blits, static %d' % (r['stunPoseDrawn'], r['stunFx']))
                ok(r['shieldInStun'] == 0, name + ' the shield is down while he is stunned (barrier %s)' % r['shieldInStun'])
                bd = r['bodyDmgInStun'] or {}
                ok((bd.get('hp', 0) + bd.get('armor', 0)) > 0, name + ' a body round during the stun does damage (%s)' % bd)
                ok(not r['reheal'], name + ' he does NOT start another heal after the stun')
                ok(r['resumed'] is not None, name + ' he resumes fighting after the stun (%s)' % r['resumed'])
            ok(not r['errs'], name + ' zero page/console errors %s' % r['errs'][:2])
        br.close()
    stop()
    json.dump(rows, open(a.json or os.path.join(OUT, 'run.json'), 'w'), indent=1)
    print('%d fail' % fails)
    return 1 if fails else 0

if __name__ == '__main__':
    sys.exit(main())
