"""capture10.py - the v10 trailer library (Gasline / rebel-fight cut): frame-perfect 60 fps takes with the game's own sound log.

    python capture9.py --list
    python capture9.py S6L T_hama                   # a subset
    python capture9.py --all --workers 3 --missing

Built on capture3.py (v7/v8): same synthetic clock, same real input map, same sound log, same playerHit stub. New here:

  diff      the take's difficulty. debugStartFight and startRun both assign DIFF from diffKey, so setting diffKey
            before the setup gives the real Normal / Hard / Furious encounter (Mike: "the normal, hard and furious
            variants") rather than a relabelled Normal one.
  when      conditional events, {COND: JS} - each fires once, the first chunk boundary COND holds. Stage 6's
            route choice, the miniboss kill and the boss handoff are timed by the game, not by a frame guess.
  windows   one long run saved as several takes. Stage 6 is 75 s of stage plus a ~76 s opening plus a miniboss
            plus a route plus a boss; saving all of it is ~5 GB. [start, end, suffix] in recorded frames writes
            takes9/<id><suffix>/ with its own rec0, so render_audio.py aligns each window's sound on its own.
            A window may also open on a condition: ['@COND', frames, suffix].
  hama      the HAMA song clock. The encounter reads Snd.music.hama.currentTime; like probe_hama_0928.py the
            element's currentTime is pinned to a value this harness advances by 1/60 s per stepped frame, so
            every STOP / HAMMER / TIME slam lands on a known frame and the mixer can lay the real instrumental
            under the take at exactly the song time the take shows (metrics carry it as 'hc').
  toasts    achievement toasts are stubbed (achToastPush) - a trailer is not a profile.
"""
import os, sys, json, time, base64, shutil, argparse, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import capture3 as C3   # noqa: E402
import real9            # noqa: E402  (REAL GAMEPLAY: the real playerHit, the dodge autopilot)

C3.TAKES.clear()
TAKES = C3.TAKES
take, fight, stage, menu = C3.take, C3.fight, C3.stage, C3.menu
TAKES_DIR = C3.TAKES_DIR
SPECIAL, KILL, LOCK, LAUNCH, UP, DOWN = C3.SPECIAL, C3.KILL, C3.LOCK, C3.LAUNCH, C3.UP, C3.DOWN
tap, held, strikes = C3.tap, C3.held, C3.strikes
RZB_EDGE, RZB_IN = C3.RZB_EDGE, C3.RZB_IN

LIB9 = r"""() => {
  try { achToastPush = function(){}; achToasts.length = 0; } catch (e) {}
  window.__hamaT = null;
  window.__hamaPin = function(){
    const m = Snd && Snd.music && Snd.music.hama; if (!m || m.__pinned) return !!m;
    window.__hamaT = 0; m.__pinned = true;
    Object.defineProperty(m, 'currentTime', {configurable: true, get(){ return window.__hamaT; }, set(v){ window.__hamaT = v; }});
    Object.defineProperty(m, 'paused', {configurable: true, get(){ return false; }});
    return true;
  };
  window.__step = function(n){
    for (let k = 0; k < n; k++) {
      window.__i++;
      try { window.__auto(window.__i); } catch (e) { window.__err = 'auto ' + String(e).slice(0, 140); }
      try {
        if (window.__hamaT != null && typeof boss !== 'undefined' && boss && boss._hammerTime && boss._hammerTime.musicStarted)
          window.__hamaT += 1 / 60;
      } catch (e) {}
      window.__now += 1000 / 60;
      try { loop(window.__now); } catch (e) { window.__err = 'loop ' + String(e).slice(0, 140); }
      try { window.__loopSample(); } catch (e) {}
    }
  };
  /* BURST FIRE for boss takes: a gun on a boss every frame holds its hit flash (0.16 s, re-armed by every round) for the
     whole take, so a laser or an orb stream turns the boss into a white silhouette. [on, off] frames. */
  window.__burst = null;
  const _auto = window.__auto;
  window.__auto = function(i){
    if (window.__burst) { const b = window.__burst; window.__fire = (i % (b[0] + b[1])) < b[0]; }
    return _auto(i);
  };
  const _m = window.__metrics;
  window.__metrics = function(){
    const o = _m();
    try {
      const W = (typeof s6Wing !== 'undefined') ? s6Wing : null;
      o.s6 = W ? [W.ships.length, W.choice ? 1 : 0, W.route || null, W.fake ? 1 : 0] : null;
      o.op = (typeof s6Opening !== 'undefined' && s6Opening) ? s6Opening.phase : null;
      o.hc = (window.__hamaT != null) ? +window.__hamaT.toFixed(4) : null;
      o.hm = (typeof boss !== 'undefined' && boss && boss._hammerTime) ? [boss._hammerTime.mode, boss._hammerTime.hama ? boss._hammerTime.hama.pose : null] : null;
      o.rv = (typeof Rival24 !== 'undefined' && Rival24.active) ? Rival24.active.rival : null;
      o.bk = (typeof boss !== 'undefined' && boss && bossActive) ? (boss.kind || null) : null;
      o.dk = (typeof diffKey !== 'undefined') ? diffKey : null;
      o.stt = +(stageTimer || 0).toFixed(2);
      const T = window.__tgt();
      o.bf = (T && T.flash > 0) ? 1 : 0;          // the boss is mid hit-flash (white) on this frame
    } catch (e) {}
    return o;
  };
  return true;
}"""

# ------------------------------------------------------------------------------------------------------------
# THE TAKE PLAN. Pilots are spread so the edit can keep every pilot within a shot of the others and never cut
# one pilot to himself.
# ------------------------------------------------------------------------------------------------------------

exec(open(os.path.join(HERE, 'plan10.py')).read())


def _js(page, body):
    return page.evaluate("() => { try { %s } catch (e) { return 'ERR ' + String(e).slice(0, 200); } }" % body)


def run_take(browser, port, tid, spec, quality):
    free = shutil.disk_usage(HERE).free / 1e9
    if free < C3.MIN_FREE_GB:
        raise RuntimeError('only %.1f GB free - refusing to record' % free)
    windows = spec.get('windows') or [[0, spec['rec'], '']]
    outs = {}
    for w in windows:
        d = os.path.join(TAKES_DIR, tid + w[2])
        os.makedirs(d, exist_ok=True)
        for f in os.listdir(d):
            os.remove(os.path.join(d, f))
        outs[w[2]] = d
    errs, notes = [], []
    t0 = time.time()
    page = browser.new_page(viewport={'width': 1280, 'height': 960})
    page.on('pageerror', lambda e: errs.append('PAGEERROR ' + str(e)[:180]))
    page.on('console', lambda m: errs.append(m.text[:180]) if m.type == 'error' else None)
    page.goto('http://127.0.0.1:%d/index.html?quality=high' % port)
    page.wait_for_function("() => (window.__bofFrames|0) > 4", timeout=90000)
    page.evaluate(C3.LIB)
    page.evaluate(LIB9)
    page.evaluate(real9.LIB_REAL)
    page.evaluate("() => { ASSETS.ready = true; }")
    page.evaluate("(d) => { diffKey = d; }", spec.get('diff') or 'normal')
    if spec.get('quiet'):
        page.evaluate("() => { dlgBox = function(){}; }")
    js = lambda body: _js(page, body)

    if spec['kind'] == 'menu':
        notes.append('setup -> %s' % js(spec['setup'] + ' return state;'))
    elif spec['kind'] == 'fight':
        notes.append('setup ' + json.dumps(page.evaluate("([s, r, p]) => window.__fight(s, r, p)", [spec['stage'], spec['role'], spec['pilot']])))
    else:
        notes.append('setup ' + json.dumps(page.evaluate("([s, p]) => window.__run(s, p)", [spec['stage'], spec['pilot']])))
    for key in ('until', 'pre_until'):
        if spec.get(key):
            n = 0
            while n < 6000 and js('return !!(%s);' % spec[key]) is not True:
                page.evaluate("(n) => window.__step(n)", 20)
                n += 20
                page.wait_for_timeout(50)
            notes.append('%s after %d frames (state %s)' % (key, n, js('return state;')))
    if spec.get('pre'):
        notes.append('pre -> %s' % js(spec['pre'] + ' return null;'))
    if spec.get('arm'):
        w, lv, wv = spec['arm']
        notes.append('arm ' + json.dumps(page.evaluate("([w, l, v]) => window.__arm(w, l, v)", [w, lv, wv])))
        page.evaluate("(a) => window.__armSpecSet(a)", [w, lv, wv])
    page.evaluate("([m, f]) => { window.__mode = m; window.__fire = f; }", [spec['mode'], spec['fire']])
    page.evaluate("(b) => { window.__burst = b; }", spec.get('burst'))

    events = {int(k): v for k, v in spec['events'].items()}
    whens = list((spec.get('when') or {}).items())
    fired = set()
    total = spec['warm'] + spec['rec']
    f = 0
    # window state: fixed windows by recorded-frame range; conditional ones open when their condition first holds
    wstate = {}
    for w in windows:
        if isinstance(w[0], str):
            wstate[w[2]] = {'cond': w[0][1:], 'len': w[1], 'open': None, 'n': 0, 'rec0': None, 'metrics': []}
        else:
            wstate[w[2]] = {'cond': None, 'lo': w[0], 'hi': w[1], 'open': None, 'n': 0, 'rec0': None, 'metrics': []}
    at_rec_done = False

    def next_event(after):
        later = [k for k in events if k > after]
        return min(later) if later else 10 ** 9

    def any_open(fr):
        rf = fr - spec['warm']
        for k, s in wstate.items():
            if s['cond'] is None:
                if s['lo'] <= rf < s['hi']:
                    return True
            elif s['open'] is not None and s['n'] < s['len']:
                return True
        return False

    def all_done():
        for s in wstate.values():
            if s['cond'] is None and s['n'] < s['hi'] - s['lo']:
                return False
            if s['cond'] is not None and (s['open'] is None or s['n'] < s['len']):
                return False
        return True

    while f < total:
        if f in events:
            r = js(events[f] + ' return null;')
            notes.append('@%d %s -> %s' % (f, events[f][:48], r))
        for i, (cond, body) in enumerate(whens):
            if i in fired:
                continue
            if js('return !!(%s);' % cond) is True:
                fired.add(i)
                notes.append('@%d when %s -> %s' % (f, cond[:44], js(body + ' return null;')))
        if f >= spec['warm'] and not at_rec_done and spec.get('at_rec'):
            notes.append('@%d at_rec -> %s' % (f, js(spec['at_rec'] + ' return null;')))
            at_rec_done = True
        for k, s in wstate.items():
            if s['cond'] is not None and s['open'] is None and f >= spec['warm'] and js('return !!(%s);' % s['cond']) is True:
                s['open'] = f
                notes.append('window %s opens @%d' % (k, f))
        if spec.get('stop') and js('return !!(%s);' % spec['stop']) is True:
            notes.append('stop @%d' % f)
            break
        if all_done():
            notes.append('all windows done @%d' % f)
            break
        if not any_open(f):
            n = min(20, total - f, next_event(f) - f)
            # a fixed window about to open must not be stepped past
            for s in wstate.values():
                if s['cond'] is None and spec['warm'] + s['lo'] > f:
                    n = min(n, spec['warm'] + s['lo'] - f)
            n = max(1, n)
            page.evaluate("(n) => window.__step(n)", n)
            f += n
            page.wait_for_timeout(40)
            continue
        n = max(1, min(6, total - f, next_event(f) - f))
        # do not step a fixed window past its end or before its start in one chunk
        rf = f - spec['warm']
        for s in wstate.values():
            if s['cond'] is None:
                if s['lo'] <= rf < s['hi']:
                    n = min(n, s['hi'] - rf)
                elif rf < s['lo']:
                    n = min(n, s['lo'] - rf)
            elif s['open'] is not None and s['n'] < s['len']:
                n = min(n, s['len'] - s['n'])
        out = page.evaluate("([n, h, q]) => window.__grabN(n, h, q)", [n, spec['hud'], quality])
        i0 = page.evaluate("() => window.__i") - n + 1
        for k in range(n):
            frf = f + k - spec['warm']
            for key, s in wstate.items():
                inside = (s['cond'] is None and s['lo'] <= frf < s['hi']) or \
                         (s['cond'] is not None and s['open'] is not None and s['n'] < s['len'])
                if not inside:
                    continue
                if s['rec0'] is None:
                    s['rec0'] = i0 + k
                d = outs[key]
                with open(os.path.join(d, 's%05d.jpg' % s['n']), 'wb') as fh:
                    fh.write(base64.b64decode(out['s'][k].split(',', 1)[1]))
                if spec['hud']:
                    with open(os.path.join(d, 'h%05d.png' % s['n']), 'wb') as fh:
                        fh.write(base64.b64decode(out['h'][k].split(',', 1)[1]))
                s['metrics'].append(out['m'][k])
                s['n'] += 1
        f += n
    audio = page.evaluate("() => window.__audioDump()")
    page.close()
    dt = time.time() - t0
    metas = []
    for w in windows:
        key = w[2]
        s = wstate[key]
        d = outs[key]
        a2 = dict(audio)
        a2['rec0'] = s['rec0']
        a2['frames'] = s['n']
        json.dump(s['metrics'], open(os.path.join(d, 'metrics.json'), 'w'))
        json.dump(a2, open(os.path.join(d, 'audio_events.json'), 'w'))
        M = s['metrics']
        peak = {k: max((m.get(k) or 0) for m in M) for k in ('e', 'eb', 'pb', 'pa', 'ex')} if M else {}
        mb = sum(os.path.getsize(os.path.join(d, x)) for x in os.listdir(d)) / 1e6
        rec0 = s['rec0']
        in_rec = lambda i: rec0 is not None and rec0 <= i < rec0 + s['n']
        sub = tid + key
        spec2 = dict(spec)
        spec2['window'] = w
        meta = dict(id=sub, parent=tid, spec=spec2, frames=s['n'], seconds=round(dt, 1), mb=round(mb, 1), notes=notes,
                    rec0=rec0, page_errors=errs[:10], step_errors=sorted({m['err'] for m in M if m.get('err')})[:6],
                    peak=peak, targets=sorted({m['tn'] for m in M if m.get('tn')}),
                    specials=sorted({m['sp'] for m in M if m.get('sp')}), states=sorted({m['st'] for m in M}),
                    sound=dict(snd=sum(1 for e in audio['snd'] if in_rec(e[0])), syn=sum(1 for e in audio['syn'] if in_rec(e[0])),
                               loops=sorted(audio['loops']), warp=len(audio['warp'])),
                    event_idx={str(k - spec['warm']): v for k, v in sorted(events.items())})
        json.dump(meta, open(os.path.join(d, 'meta.json'), 'w'), indent=1)
        if s['n']:
            C3.contact(d, s['n'], sub)
        metas.append(meta)
    return metas


def worker(ids, quality):
    from playwright.sync_api import sync_playwright
    port, stop = C3.serve()
    args = ['--autoplay-policy=no-user-gesture-required', '--disable-background-timer-throttling',
            '--disable-renderer-backgrounding', '--mute-audio']
    with sync_playwright() as pw:
        browser = pw.chromium.launch(args=args, executable_path=C3.CHROME)
        for tid in ids:
            try:
                for m in run_take(browser, port, tid, TAKES[tid], quality):
                    print('%-16s %5d fr %6.1fs %6.1fMB peak %s tgt %s sp %s snd %s err %d/%d' % (
                        m['id'], m['frames'], m['seconds'], m['mb'], m['peak'], m['targets'], m['specials'],
                        m['sound']['snd'], len(m['page_errors']), len(m['step_errors'])), flush=True)
                print('   notes: ' + ' | '.join(m['notes'])[:1500], flush=True)
            except Exception as e:
                print('%-16s FAILED: %s' % (tid, str(e)[:400]), flush=True)
                try:
                    browser.close()
                except Exception:
                    pass
                browser = pw.chromium.launch(args=args, executable_path=C3.CHROME)
        browser.close()
    stop()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('ids', nargs='*')
    ap.add_argument('--all', action='store_true')
    ap.add_argument('--list', action='store_true')
    ap.add_argument('--missing', action='store_true')
    ap.add_argument('--workers', type=int, default=1)
    ap.add_argument('--quality', type=float, default=0.90)
    a = ap.parse_args()
    if a.list:
        tot, per = 0, {}
        for tid, s in TAKES.items():
            ws = s.get('windows')
            r = sum((w[1] if isinstance(w[0], str) else w[1] - w[0]) for w in ws) if ws else s['rec']
            tot += r
            if s.get('pilot'):
                per.setdefault(s['pilot'], []).append(tid)
            print('%-14s %-6s warm %5d rec %5d diff %-8s %s' % (tid, s['kind'], s['warm'], r, s.get('diff') or '-',
                  {k: v for k, v in s.items() if k in ('stage', 'role', 'pilot', 'arm')}))
        print('%d takes, %d saved frames (%.1f min, ~%.1f GB)' % (len(TAKES), tot, tot / 3600.0, tot * 0.33 / 1000))
        for p in sorted(per):
            print('  %-11s %2d  %s' % (p, len(per[p]), ' '.join(per[p])))
        return
    ids = list(TAKES) if a.all else a.ids
    bad = [i for i in ids if i not in TAKES]
    if bad:
        sys.exit('unknown takes: %s' % bad)
    if a.missing:
        def done(i):
            ws = TAKES[i].get('windows') or [[0, 0, '']]
            return all(os.path.exists(os.path.join(TAKES_DIR, i + w[2], 'meta.json')) for w in ws)
        ids = [i for i in ids if not done(i)]
    os.makedirs(TAKES_DIR, exist_ok=True)
    if a.workers <= 1 or len(ids) <= 1:
        worker(ids, a.quality)
        return
    order = sorted(ids, key=lambda i: -(TAKES[i]['rec'] + TAKES[i]['warm'] * 0.15))
    shards = [order[k::a.workers] for k in range(a.workers)]
    procs = [subprocess.Popen([sys.executable, '-u', os.path.abspath(__file__)] + s + ['--quality', str(a.quality)],
                              cwd=HERE, env=dict(os.environ, PYTHONIOENCODING='utf-8')) for s in shards if s]
    for p in procs:
        p.wait()


if __name__ == '__main__':
    main()
