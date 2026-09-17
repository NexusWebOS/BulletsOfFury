#!/usr/bin/env python3
"""
profile_space_0916.py - WHO IS EATING THE FRAME? A real CPU profile of the real game.

    python _BUILD_SOURCE/profile_space_0916.py --stage 9 --seconds 8
    python _BUILD_SOURCE/profile_space_0916.py --stage 3 --seconds 8      # the control
    python _BUILD_SOURCE/profile_space_0916.py --stage 9 --compare 3

CLAUDE.md names this route at the atlas section -- CDP `Profiler`, attribute native time to the
nearest game.js frame -- and records it finding the Magma Ward's 78 ms/frame `shadowBlur` cost in
one run. The script it names (`scratchpad/miniprof.py`) is gone: scratchpad/ is gitignored, so it
never survived the session that wrote it. This is that tool, rebuilt and committed this time.

WHY SELF TIME AND NOT TOTAL
  Canvas work -- drawImage, fill, the compositing a `globalCompositeOperation` triggers -- is
  NATIVE. It does not appear as its own JS stack frame; V8's sampling profiler attributes it as
  SELF time to the JS function that called it. So the function with the largest self time is the
  one issuing the expensive draw calls, which is exactly the question. Ranking by total time just
  returns `loop` every time.

⚠ THIS MEASURES THE SAME SOFTWARE-RASTERISED HEADLESS CHROMIUM the fps numbers came from, which
  has no GPU. That is a real limitation and it is stated in the output: a cost that is native
  compositing will be inflated here relative to a GPU machine. It is still the right instrument
  for finding the OWNER -- the ratio between two functions in the same run is not affected by the
  absence of a GPU nearly as much as the absolute milliseconds are.
"""
import argparse, json, os, sys, time
from collections import defaultdict

ROOT = os.path.dirname(os.path.abspath(__file__))
GAME = os.path.abspath(os.path.join(ROOT, '..'))
sys.path.insert(0, ROOT)
from shoot import serve  # noqa: E402

SETUP = r"""
(cfg) => {
  const out = {ok:false};
  try {
    if (typeof ASSETS === 'undefined') { out.err='no ASSETS'; return out; }
    ASSETS.ready = true;
    if (cfg.pilot && typeof run !== 'undefined') run.pilot = cfg.pilot;
    if (typeof STAGES !== 'undefined') curStage = STAGES[(cfg.stage||1)-1];
    run.stage = cfg.stage || 1;
    beginStage(cfg.stage || 1);
    setState(GS.PLAY);
    if (typeof player !== 'undefined' && player.reset) player.reset();
    out.ok = true;
  } catch(e) { out.err = String(e && e.message || e); }
  return out;
}
"""

# Same autopilot the capture tool uses, for the same reason: a stage with nobody shooting is not
# the stage anyone plays, and the profile would miss every projectile draw.
AUTOPILOT = r"""
() => {
  window.__bofAuto = {t:0, shots:0};
  if (typeof window.playerHit === 'function') window.playerHit = function(){};
  if (typeof player !== 'undefined') player.invuln = 0;
  if (typeof window.debugRecOverlay === 'function') window.debugRecOverlay = function(){};
  window.__bofAutoTick = function(){
    const A = window.__bofAuto; A.t += 1/60;
    try {
      if (typeof player !== 'undefined') {
        player.x += (VW*0.5 + Math.sin(A.t*0.55)*VW*0.30 - player.x)*0.06;
        player.y += (VH*0.62 + Math.sin(A.t*0.37+1.1)*VH*0.16 - player.y)*0.06;
        if (player.invuln > 0) player.invuln = 0;
      }
      if (typeof pShoot === 'function' && (!player.fireCd || player.fireCd <= 0)) { pShoot(); A.shots++; }
    } catch(_e){}
  };
  if (!window.__bofHooked) {
    const inner = window.loop;
    window.loop = function(){ const r = inner.apply(this, arguments);
      try { if (window.__bofAutoTick) window.__bofAutoTick(); } catch(_e){} return r; };
    window.__bofHooked = true;
  }
  return true;
}
"""

FRAMES = "() => (window.__bofFrames|0)"

PROF_CACHE = []


def walk(nodes):
    """CDP returns a flat node list with children ids. Index it, and build parent links.

    The parent map is the load-bearing part. A sample that lands inside `drawImage` is recorded
    against a node whose callFrame is the NATIVE function -- url '', line 0 -- so a self-time
    ranking returns `drawImage` and tells you nothing about which of the ~700 draw calls in this
    file issued it. The profile tree knows: the node's ancestors are the real call path.
    """
    by_id = {n['id']: n for n in nodes}
    parent = {}
    for n in nodes:
        for c in n.get('children', ()) or ():
            parent[c] = n['id']
    return by_id, parent


# ⚠ `ctx.drawImage` IS WRAPPED TWICE IN game.js AND BOTH WRAPPERS ARE game.js FRAMES.
# Drops 0724dq and 0724dr each installed a guard on the context itself -- deliberately, because
# there are ~377 call sites and one reaching a null used to kill the whole frame. The consequence
# for a profile is that "the nearest game.js ancestor" of every single blit in the game is one of
# those two wrappers, so the ranking comes back as `ctx.drawImage 70%` and names nobody. Walk
# straight through them to the call site that actually issued the draw.
WRAPPERS = {'ctx.drawImage', 'ctx.fill', 'ctx.stroke'}


def owner_of(nid, by_id, parent, depth=24):
    """The nearest ancestor that is OUR code, skipping the context wrappers.

    CLAUDE.md describes miniprof as attributing native time 'to the nearest game.js frame', which
    is this. Returns (owner_label, native_label_or_None).
    """
    native = None
    cur = nid
    for _ in range(depth):
        n = by_id.get(cur)
        if not n:
            break
        cf = n['callFrame']
        url = cf.get('url') or ''
        name = cf.get('functionName') or '(anonymous)'
        if ('game.js' in url or 'index.html' in url) and name not in WRAPPERS:
            return ('%s  [%s:%d]' % (name, url.rsplit('/', 1)[-1], cf.get('lineNumber', -1) + 1),
                    native)
        if native is None and name not in ('(root)', '(program)', '(idle)',
                                           '(garbage collector)'):
            native = name
        cur = parent.get(cur)
        if cur is None:
            break
    n = by_id.get(nid)
    nm = (n['callFrame'].get('functionName') if n else None) or '(unknown)'
    return ('(no game.js ancestor) ' + nm, native)


def dump_paths(prof, wall, frames, top=8):
    """Print the FULL ancestry of the heaviest sampled nodes.

    Written because the attribution above charged 82% of the frame to `A.blit`, and a direct
    trap on A.blit then measured it running TWICE a frame. One of the two was wrong and no
    amount of re-reasoning about the walk could say which. The tree itself can.
    """
    nodes = prof['nodes']
    by_id, parent = walk(nodes)
    cnt = defaultdict(int)
    for nid in prof.get('samples', []):
        cnt[nid] += 1
    ms = (wall * 1000.0) / max(1, len(prof.get('samples', [])))
    print('')
    print('--- heaviest sampled nodes, full ancestry ---')
    for nid, c in sorted(cnt.items(), key=lambda kv: -kv[1])[:top]:
        chain = []
        cur = nid
        for _ in range(14):
            n = by_id.get(cur)
            if not n:
                break
            cf = n['callFrame']
            nm = cf.get('functionName') or '(anon)'
            url = (cf.get('url') or '').rsplit('/', 1)[-1]
            ln = cf.get('lineNumber', -1) + 1
            chain.append('%s%s' % (nm, (':%d' % ln) if url else ''))
            cur = parent.get(cur)
            if cur is None:
                break
        print('  %7.2f ms/frame  %s' % (c * ms / max(1, frames), '  <-  '.join(chain)))


def profile(pg, cdp, seconds):
    cdp.send('Profiler.enable')
    # 100us sampling: fine enough to separate two draw calls, cheap enough not to distort a
    # frame that is already slow.
    cdp.send('Profiler.setSamplingInterval', {'interval': 100})
    f0 = pg.evaluate(FRAMES)
    t0 = time.time()
    cdp.send('Profiler.start')
    pg.wait_for_timeout(int(seconds * 1000))
    res = cdp.send('Profiler.stop')
    wall = time.time() - t0
    f1 = pg.evaluate(FRAMES)
    return res['profile'], wall, f1 - f0


def summarise(prof, wall, frames, top=16):
    """Rank by time CHARGED to each game.js function -- its own plus the native calls it makes."""
    nodes = prof['nodes']
    by_id, parent = walk(nodes)
    total_samples = 0
    charged = defaultdict(int)
    natives = defaultdict(lambda: defaultdict(int))

    for nid in prof.get('samples', []):
        total_samples += 1
        n = by_id.get(nid)
        if not n:
            continue
        name = (n['callFrame'].get('functionName') or '')
        if name in ('(program)', '(idle)', '(garbage collector)', '(root)'):
            charged[name] += 1
            continue
        owner, native = owner_of(nid, by_id, parent)
        charged[owner] += 1
        if native:
            natives[owner][native] += 1

    if not total_samples:
        return []
    ms_per_sample = (wall * 1000.0) / total_samples
    rows = sorted(charged.items(), key=lambda kv: -kv[1])[:top]
    out = []
    for k, c in rows:
        ms = c * ms_per_sample
        nat = sorted(natives.get(k, {}).items(), key=lambda kv: -kv[1])[:3]
        out.append({
            'fn': k,
            'samples': c,
            'pct': 100.0 * c / total_samples,
            'ms_total': ms,
            'ms_per_frame': (ms / frames) if frames else 0.0,
            'native': ['%s %.0f%%' % (nm, 100.0 * v / c) for nm, v in nat],
        })
    return out


def run_one(stage, seconds, pilot, weapon=None, wlevel=None, headed=False, suppress=None):
    from playwright.sync_api import sync_playwright
    port, stop = serve(GAME)
    url = 'http://127.0.0.1:%d/index.html' % port
    with sync_playwright() as p:
        b = p.chromium.launch(headless=not headed, args=['--no-sandbox', '--mute-audio'])
        pg = b.new_page(viewport={'width': 1100, 'height': 1250}, device_scale_factor=1)
        errs = []
        pg.on('pageerror', lambda e: errs.append(str(e)[:160]))
        pg.goto(url, wait_until='load', timeout=60000)
        pg.wait_for_function("() => typeof ASSETS!=='undefined' && typeof setState==='function'",
                             timeout=45000)
        pg.wait_for_function("() => (window.__bofFrames|0) > 4", timeout=45000)

        r = pg.evaluate(SETUP, {'stage': stage, 'pilot': pilot})
        if not r.get('ok'):
            print('setup failed:', r.get('err')); b.close(); stop(); sys.exit(1)
        pg.evaluate(AUTOPILOT)
        if weapon is not None:
            pg.evaluate("(w) => { run.weapon = w; }", weapon)
        if wlevel is not None:
            pg.evaluate("(l) => { run.wlevel = l; }", wlevel)
        if suppress:
            # Replace a named global function with a no-op, to CONFIRM an owner by removing it.
            got = pg.evaluate("""(names) => names.map(n => {
                if (typeof window[n] === 'function') { window['__real_'+n] = window[n];
                  window[n] = function(){ return false; }; return n + ':stubbed'; }
                return n + ':NOT-A-WINDOW-FUNCTION';
            })""", suppress)
            print('  suppress:', ', '.join(got))

        # let the scene settle and its lazy art decode before the profiler opens
        pg.wait_for_timeout(4000)

        cdp = pg.context.new_cdp_session(pg)
        prof, wall, frames = profile(pg, cdp, seconds)
        PROF_CACHE[:] = [prof, wall, frames]
        fps = frames / wall if wall else 0
        rows = summarise(prof, wall, frames)
        b.close()
    stop()
    return fps, frames, wall, rows, errs


def show(label, fps, frames, wall, rows, errs):
    print('\n=== %s ===' % label)
    print('  %.1f fps   (%d frames in %.1fs)' % (fps, frames, wall))
    print('  %-50s %7s %10s  %s' % ('charged to (incl. its native draw calls)', 'pct',
                                     'ms/frame', 'native'))
    for r in rows:
        print('  %-50s %6.1f%% %10.2f  %s' % (r['fn'][:50], r['pct'], r['ms_per_frame'],
                                              ', '.join(r.get('native') or [])))
    for e in errs[:4]:
        print('  err', e)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--stage', type=int, default=9)
    ap.add_argument('--seconds', type=float, default=8)
    ap.add_argument('--pilot', default='cole')
    ap.add_argument('--weapon', type=int, default=None)
    ap.add_argument('--wlevel', type=int, default=None)
    ap.add_argument('--compare', type=int, default=None, help='also profile this stage as a control')
    ap.add_argument('--suppress', default=None,
                    help='comma-separated global function names to stub out, to confirm an owner')
    ap.add_argument('--json', default=None)
    ap.add_argument('--paths', action='store_true')
    ap.add_argument('--headed', action='store_true')
    args = ap.parse_args()

    sup = args.suppress.split(',') if args.suppress else None
    fps, frames, wall, rows, errs = run_one(args.stage, args.seconds, args.pilot,
                                            args.weapon, args.wlevel, args.headed, sup)
    show('stage %d' % args.stage, fps, frames, wall, rows, errs)
    if args.paths:
        dump_paths(PROF_CACHE[0], PROF_CACHE[1], PROF_CACHE[2])
    payload = {'stage': args.stage, 'fps': fps, 'rows': rows}

    if args.compare:
        f2, fr2, w2, rows2, e2 = run_one(args.compare, args.seconds, args.pilot,
                                         args.weapon, args.wlevel, args.headed, sup)
        show('stage %d (control)' % args.compare, f2, fr2, w2, rows2, e2)
        payload['control'] = {'stage': args.compare, 'fps': f2, 'rows': rows2}
        print('\n  ratio  stage %d is %.1fx slower than stage %d'
              % (args.stage, (f2 / fps) if fps else 0, args.compare))

    print('\n  NOTE headless Chromium here has NO GPU. Native compositing costs are inflated')
    print('       against a GPU machine; the RANKING within one run is the trustworthy part.')

    if args.json:
        open(args.json, 'w').write(json.dumps(payload, indent=2))
        print('  wrote', args.json)


if __name__ == '__main__':
    main()
