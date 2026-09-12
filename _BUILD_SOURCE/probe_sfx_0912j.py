#!/usr/bin/env python3
"""
probe_sfx_0912j.py - THE NEW AUDIO, IN THE REAL ENGINE.

    python3 _BUILD_SOURCE/probe_sfx_0912j.py

Mike, 2026-09-12: "get rid of those annoying sounds I've complained about and generate me proper
16-bit shield impact noises, proper boss projectile noises for each one that we have and other
improvement sounds we need like alerts, when the firewall comes and more."

⚠ THE THING BEING TESTED IS MOSTLY THE THROTTLE, NOT THE SAMPLE. Every beeping complaint in this
project's history was REPETITION, not a bad sound:

    0807q  "an annoying noise every time a jet flies"          -> whip, 11 sites, NO gate
    0813a  "that annoying beep noise when homing missiles..."  -> fixed at enemyLockOn, then the
                                                                  same sample came back on boss
                                                                  beam telegraphs, 7 per warn
    0822ae "stop doing the beep beep beep with all these bosses" -> enemyShoot per BULLET, and the
                                                                  documented ESHOOT_GAP fix is
                                                                  DEAD CODE (the synth body it
                                                                  guards is overwritten by the
                                                                  sample bridge)

So this counts PLAYS, by wrapping Snd.play, and asserts the gates hold under a burst. A sound that
cannot be spammed is the deliverable.
"""
import os, sys, argparse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import shoot

NEW_KEYS = ['shieldHitLight', 'shieldHitHeavy', 'shieldBreakCombat', 'shieldGraze', 'shieldUp',
            'shieldLow', 'shieldBossAbsorb',
            'bossfireDamkeeper', 'bossfireInfernoreaver', 'bossfireCryospear',
            'bossfireStormsovereign', 'bossfireXenoregent', 'bossfireDoomsdaycarrier',
            'bossfireSludgeemperor', 'bossfireVileexistence', 'bossfireTidalfusion',
            'alertBossIncoming', 'alertDanger', 'alertLockon', 'alertBeamCharge',
            'firewallArrive', 'firewallPass']


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--out', default='/tmp/sfxprobe'); a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    from playwright.sync_api import sync_playwright
    port, stop = shoot.serve(shoot.GAME); errs = []; fails = []; n_ok = [0]
    def ok(c, m):
        if c: n_ok[0] += 1; print('  ok  ', m)
        else: fails.append(m); print('  FAIL', m)

    with sync_playwright() as p:
        b = p.chromium.launch(args=['--disable-gpu', '--no-sandbox', '--mute-audio'])
        pg = b.new_page(viewport={'width': 900, 'height': 1000})
        pg.on('pageerror', lambda e: errs.append('pageerror: ' + str(e)[:220]))
        missing = []
        pg.on('response', lambda r: missing.append(r.url.split('/')[-1]) if r.status == 404 else None)

        pg.goto(f'http://127.0.0.1:{port}/index.html?bossmode=1', wait_until='load', timeout=60000)
        pg.wait_for_function("() => window.BOFDEBUG && window.BOFDEBUG.ready", timeout=90000)
        ok(True, 'the game boots')

        # ---- every new key is registered AND reachable as a function ----
        reg = pg.evaluate("""(keys) => {
            const o={}; for(const k of keys){
              o[k]={inManifest: !!(window.BOFA&&BOFA.sfx&&BOFA.sfx[k]),
                    callable: !!(window.Audio&&Audio.SFX&&typeof Audio.SFX[k]==='function'),
                    path:(window.BOFA&&BOFA.sfx)?BOFA.sfx[k]:null};
            } return o; }""", NEW_KEYS)
        bad = [k for k, v in reg.items() if not v['inManifest']]
        ok(not bad, 'all %d new cues are registered in BOFA.sfx%s'
           % (len(NEW_KEYS), '' if not bad else ' - MISSING: ' + ', '.join(bad)))
        nf = [k for k, v in reg.items() if not v['callable']]
        ok(not nf, 'and every one is reachable as Audio.SFX.<key>() via the sample bridge%s'
           % ('' if not nf else ' - NOT CALLABLE: ' + ', '.join(nf)))

        # ---- every new key has a TAME row, i.e. a gate ----
        # ⚠ BARE `Snd`, NOT `window.Snd`. Snd is a module-scope const in a classic script, so it
        # lives in the global LEXICAL environment and is not a window property - CLAUDE.md records
        # this exact trap ("window.Snd is undefined while bare Snd works").
        # ⚠ AND READING IT WRONG PRODUCED A VACUOUS PASS: with T={} the "every key has a TAME row"
        # check failed while "every one carries a `min`" PASSED, because an empty list satisfies
        # `all()`. Two checks disagreeing about the same table is the tell. The burst test below
        # was the honest one - it measured 38 refusals, which only happens if the rows are live.
        tame = pg.evaluate("""(keys) => {
            const T=(typeof Snd!=='undefined'&&Snd.TAME)?Snd.TAME:null;
            if(!T) return {__unreadable__:true};
            const o={}; for(const k of keys) o[k]=T[k]||null; return o; }""", NEW_KEYS)
        if tame.get('__unreadable__'):
            ok(False, 'could not read Snd.TAME at all - the probe cannot judge the gates')
            tame = {}
        nog = [k for k, v in tame.items() if not v]
        ok(not nog, 'and every one has a TAME row - a key without one plays at g=1 with NO '
                    'retrigger gate, which is the mechanism behind every beeping complaint%s'
           % ('' if not nog else ' - UNGATED: ' + ', '.join(nog)))
        # ⚠ ANCHORED ON THE FULL KEY LIST, not on whatever happened to be readable - the first
        # cut filtered to `if v` first, so an empty table passed this vacuously.
        withmin = [k for k in NEW_KEYS if tame.get(k) and tame[k].get('min')]
        ok(len(withmin) == len(NEW_KEYS),
           'and all %d carry a `min` retrigger gap (%d do)' % (len(NEW_KEYS), len(withmin)))

        # ---- the two sounds Mike named, which had NO gate before this drop ----
        old = pg.evaluate("""() => { const T=(typeof Snd!=='undefined'&&Snd.TAME)?Snd.TAME:{};
            return {whip:T.whip||null, lockAlert:T.lockAlert||null}; }""")
        ok(old['whip'] and old['whip'].get('min', 0) >= 0.2,
           'whip is gated at last (%s) - "an annoying noise every time a jet flies" (0807q) was '
           'recorded NOT STARTED and had no gate across 11 jet-manoeuvre sites' % old['whip'])
        ok(old['lockAlert'] and old['lockAlert'].get('min', 0) >= 0.4,
           'lockAlert is gated (%s) - Mike killed this beep on missile locks in 0813a and the same '
           'sample came back on boss beam telegraphs' % old['lockAlert'])

        # ---- THE GATE ACTUALLY HOLDS: spam a key and count real plays ----
        burst = pg.evaluate("""() => {
            const orig=Snd.play.bind(Snd);
            /* Snd.play returns undefined on success and false when the gate refuses, so count
               the refusals directly rather than inferring from audio we cannot hear. */
            let played=0, refused=0;
            for(let i=0;i<40;i++){ const r=orig('shieldHitLight'); if(r===false) refused++; else played++; }
            return {played:played, refused:refused}; }""")
        ok(burst['refused'] > 25,
           '40 rapid calls to shieldHitLight -> %d played, %d refused by the gate. Unthrottled '
           'that was 40 overlapping transients, which is what "beep beep beep" sounds like'
           % (burst['played'], burst['refused']))

        # ---- per-boss ordnance: each stage boss resolves to its OWN cue ----
        voices = pg.evaluate("""() => {
            const o={}; const seen={};
            for(const k in BOSS_KIND_SFX){ const v=BOSS_KIND_SFX[k]; o[k]=v; seen[v]=(seen[v]||0)+1; }
            const stageBosses=STAGES.map(s=>s&&s.boss).filter(Boolean);
            const covered=stageBosses.filter(k=>!!BOSS_KIND_SFX[k]);
            return {map:o, distinct:Object.keys(seen).length,
                    stageBosses:stageBosses, covered:covered}; }""")
        ok(len(voices['covered']) == len(voices['stageBosses']),
           'every stage boss has its own ordnance voice (%d of %d): %s'
           % (len(voices['covered']), len(voices['stageBosses']), voices['stageBosses']))
        ok(voices['distinct'] >= 9,
           'and they are %d DISTINCT cues, not one family shared four ways - BOSS_FIRE_SFX buckets '
           'nine bosses into four families, which is why the Rime Wall and the Storm Sovereign '
           'sounded identical' % voices['distinct'])

        # ---- bossAttackSfx prefers the boss's own voice ----
        picked = pg.evaluate("""() => {
            const got=[]; const S=Audio.SFX;
            const wrap={}; for(const k in BOSS_KIND_SFX){ const n=BOSS_KIND_SFX[k];
              if(!wrap[n]){ wrap[n]=S[n]; S[n]=function(){ got.push(n); }; } }
            const out={};
            for(const kind of ['cryospear','stormsovereign','sludgeemperor','tidalfusion']){
              got.length=0; _bossFireAt=0;
              bossAttackSfx({kind:kind, _ship:kind});
              out[kind]=got.slice();
            }
            for(const n in wrap) S[n]=wrap[n];
            return out; }""")
        right = all(picked[k] and picked[k][0] == {'cryospear': 'bossfireCryospear',
                                                   'stormsovereign': 'bossfireStormsovereign',
                                                   'sludgeemperor': 'bossfireSludgeemperor',
                                                   'tidalfusion': 'bossfireTidalfusion'}[k]
                    for k in picked)
        ok(right, 'bossAttackSfx raises the boss OWN cue ahead of the family: %s' % picked)

        # ---- the beam telegraph fires ONCE, not seven times ----
        beam = pg.evaluate("""() => {
            let n=0; const S=Audio.SFX;
            const a=S.alertLockon, d=S.dangerAlert, l=S.lockAlert;
            S.alertLockon=function(){ n++; }; S.dangerAlert=function(){ n++; }; S.lockAlert=function(){ n++; };
            const B={t:0, warm:3.0, released:false};
            for(let i=0;i<=30;i++){ B.t=i*0.1; l23WarnSound(B); }
            S.alertLockon=a; S.dangerAlert=d; S.lockAlert=l;
            return n; }""")
        ok(beam <= 1,
           'a full 3s beam telegraph raises %d alert, not seven - L23_WARN_ARROWS is 7 and it used '
           'to fire on every arrow, from ten beam-start sites' % beam)

        # ---- no 404s on the new files ----
        pg.evaluate("() => { for(const k in BOFA.sfx){ if(/^shield|^bossfire|^alert|^firewall/.test(k)){ const a=new window.Audio(); a.src=BOFA.sfx[k]; a.load(); } } }")
        pg.wait_for_timeout(2500)
        new404 = [m for m in missing if m.endswith('.wav')]
        ok(not new404, 'every new sound file resolves over http%s'
           % ('' if not new404 else ' - 404: ' + ', '.join(sorted(set(new404))[:6])))

        b.close()
    stop()
    print('\n%d ok / %d fail' % (n_ok[0], len(fails)))
    for f in fails: print('  FAIL', f)
    if errs:
        print('page errors (%d):' % len(errs))
        for e in errs[:6]: print('   ', e)
    sys.exit(1 if fails or errs else 0)


if __name__ == '__main__':
    main()
