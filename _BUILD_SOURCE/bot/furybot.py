#!/usr/bin/env python3
"""furybot.py - run the Furious autopilot (furybot.js) in real Chromium against the real game.

    python _BUILD_SOURCE/bot/furybot.py --stage 3                 # one stage, arcade start, Furious
    python _BUILD_SOURCE/bot/furybot.py --full --pilot cole       # stage 1 to the end, one run
    python _BUILD_SOURCE/bot/furybot.py --stage 6 --shots 4       # a frame every 4 game seconds

The run starts the way a password start does (run.mode 'arcade', diffKey 'furious', startRun) - the same entry the
game's own password screen uses - and from there the ONLY thing that touches the game is furybot.js pressing keys.
Lives are never refilled, i-frames never pinned, weapons never granted. A game over ends the run as a loss.

Every frame is stepped on a synthetic 60 Hz clock with the browser's rAF chain trapped (shoot.py's TRAP_RAF), so the
game sees the same dt a 60 Hz display gives it. Output: a JSON report (--out) with per-stage results, deaths and
what killed the pilot (the stack of each fatal playerHit), plus optional frames.
"""
import os, sys, json, time, base64, argparse
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
sys.path.insert(0, os.path.join(ROOT, '_BUILD_SOURCE'))
import shoot as sh  # noqa: E402

PILOTS = ['cole', 'maverick', 'decker', 'lizzie', 'juggernaut', 'yuri', 'freezer', 'falva', 'axel']

START = r"""(cfg) => {
  ASSETS.ready = true;
  try { achToastPush = function(){}; } catch (e) {}
  const pi = PILOTS.findIndex(p => p.key === cfg.pilot); if (pi >= 0) pilotIndex = pi;
  diffKey = cfg.diff; coopOn = false; run.mode = 'arcade'; run.ngplus = false;
  startRun(cfg.stage);
  return {state, stage: run.stage, lives: run.lives, cont: DIFF.continues, diff: diffKey, pilot: run.pilot};
}"""

STEPN = r"""(n) => {
  if (!Number.isFinite(window.__now)) window.__now = performance.now();
  for (let k = 0; k < n; k++) {
    FB.tick();
    window.__now += 1000 / 60;
    try { loop(window.__now); } catch (e) { FB.err = 'loop ' + String(e).slice(0, 160); }
  }
  return FB.metrics();
}"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--stage', type=int, default=1)
    ap.add_argument('--pilot', default='cole')
    ap.add_argument('--diff', default='furious')
    ap.add_argument('--full', action='store_true', help='keep going stage after stage until victory or game over')
    ap.add_argument('--minutes', type=float, default=25.0, help='game-minutes cap per stage')
    ap.add_argument('--shots', type=float, default=0, help='save a frame every N game seconds')
    ap.add_argument('--out', default=None)
    ap.add_argument('--tag', default='')
    ap.add_argument('--set', default=None, help='JS run after the bot loads, e.g. FB.bigLanes = true')
    ap.add_argument('--audit', action='store_true', help='measure one-step prediction error per round kind')
    ap.add_argument('--until', default=None, help='JS expression: stop the run when it holds')
    ap.add_argument('--dump', default=None, help='JS expression printed when --until holds')
    a = ap.parse_args()
    tag = a.tag or ('%s_s%d%s' % (a.pilot, a.stage, '_full' if a.full else ''))
    outdir = os.path.join(ROOT, '_shots', 'furybot', tag)
    os.makedirs(outdir, exist_ok=True)
    report_path = a.out or os.path.join(outdir, 'report.json')
    bot = open(os.path.join(HERE, 'furybot.js'), encoding='utf-8').read()

    from playwright.sync_api import sync_playwright
    port, stop = sh.serve(sh.GAME)
    errs = []
    rep = {'pilot': a.pilot, 'diff': a.diff, 'start': a.stage, 'full': a.full, 'stages': [], 'result': None}
    t0 = time.time()
    with sync_playwright() as p:
        b = p.chromium.launch(args=['--disable-gpu', '--no-sandbox', '--mute-audio'])
        pg = b.new_page(viewport={'width': 1000, 'height': 1100}, device_scale_factor=1)
        pg.on('pageerror', lambda e: errs.append('page: ' + str(e)[:200]))
        pg.on('console', lambda m: errs.append('console: ' + m.text[:200]) if m.type == 'error' else None)
        pg.goto('http://127.0.0.1:%d/index.html' % port, wait_until='load', timeout=120000)
        pg.wait_for_function("() => typeof setState==='function' && (window.__bofFrames|0) > 4", timeout=120000)
        pg.evaluate(sh.TRAP_RAF)
        pg.wait_for_timeout(60)
        info = pg.evaluate(START, {'pilot': a.pilot, 'diff': a.diff, 'stage': a.stage})
        pg.evaluate(bot)
        if a.audit: pg.evaluate("() => { FB.audit = true; }")
        if a.set: pg.evaluate("() => { " + a.set + " }")
        print('start', json.dumps(info), flush=True)
        cur = a.stage
        stage_t0 = 0
        frames = 0
        next_shot = 0
        last_print = 0
        cap = int(a.minutes * 3600)
        rec = {'stage': cur, 'frames': 0, 'deaths0': 0, 'hits0': 0}
        while True:
            m = pg.evaluate(STEPN, 60)
            frames += 60
            # let lazily-decoded art arrive: a real pause every few chunks
            if frames % 600 == 0: pg.wait_for_timeout(25)
            if m['state'] != 'play': pg.wait_for_timeout(120)   # loading screens wait on real decode time
            gs = frames / 60.0
            if a.until and pg.evaluate('() => !!(' + a.until + ')'):
                print('UNTIL holds at', gs, json.dumps(pg.evaluate('() => (' + (a.dump or 'null') + ')'))[:3000], flush=True)
                d = pg.evaluate("() => document.getElementById('screen').toDataURL('image/png')")
                open(os.path.join(outdir, 'until.png'), 'wb').write(base64.b64decode(d.split(',', 1)[1]))
                rep['result'] = 'until'; break
            if a.shots and gs >= next_shot:
                next_shot = gs + a.shots
                try:
                    d = pg.evaluate("() => document.getElementById('screen').toDataURL('image/jpeg', 0.7)")
                    open(os.path.join(outdir, 'f%06d_s%d_%s.jpg' % (frames, m['stage'], m['state'])), 'wb').write(base64.b64decode(d.split(',', 1)[1]))
                except Exception:
                    pass
            if gs - last_print >= 15:
                last_print = gs
                print('%7.1fs wall %5.0fs  %s' % (gs, time.time() - t0, json.dumps(m)), flush=True)
            if m['stage'] != cur and m['state'] in ('play', 'intro', 'launch', 'opening'):
                rec.update({'cleared': True, 'frames': frames - stage_t0, 'deaths': m['deaths'] - rec['deaths0'], 'hits': m['hits'] - rec['hits0'], 'lives_after': m['lives']})
                rep['stages'].append(rec)
                print('== stage %d CLEARED in %.0f game s, deaths %d, hits %d, lives %d' % (cur, rec['frames'] / 60, rec['deaths'], rec['hits'], m['lives']), flush=True)
                if not a.full:
                    rep['result'] = 'cleared'
                    break
                cur = m['stage']; stage_t0 = frames
                rec = {'stage': cur, 'frames': 0, 'deaths0': m['deaths'], 'hits0': m['hits']}
            if m['state'] in ('continue', 'gameover'):
                rec.update({'cleared': False, 'frames': frames - stage_t0, 'deaths': m['deaths'] - rec['deaths0'], 'hits': m['hits'] - rec['hits0']})
                rep['stages'].append(rec); rep['result'] = 'gameover'
                print('== GAME OVER on stage %d' % cur, flush=True)
                break
            if m['state'] == 'victory':
                rec.update({'cleared': True, 'frames': frames - stage_t0, 'deaths': m['deaths'] - rec['deaths0'], 'hits': m['hits'] - rec['hits0']})
                rep['stages'].append(rec); rep['result'] = 'victory'
                print('== VICTORY', flush=True)
                break
            if frames - stage_t0 > cap:
                rec.update({'cleared': False, 'frames': frames - stage_t0, 'timeout': True}); rep['stages'].append(rec)
                rep['result'] = 'timeout'; print('== TIMEOUT on stage %d (%s)' % (cur, m['state']), flush=True)
                break
        for n, d in pg.evaluate("() => FB.snaps || []"):
            open(os.path.join(outdir, 'death%d.jpg' % n), 'wb').write(base64.b64decode(d.split(',', 1)[1]))
        fb = pg.evaluate("() => ({killers: FB.killers, log: FB.log.slice(-80), err: FB.err || null, m: FB.metrics(), aud: FB.aud || null})")
        if fb.get('aud'):
            for k, v in sorted(fb['aud'].items(), key=lambda kv: -kv[1][1] / max(1, kv[1][0])):
                print('  audit %-16s n %6d  mean %6.2f  max %7.2f' % (k, v[0], v[1] / max(1, v[0]), v[2]))
        rep.update(fb)
        try:
            d = pg.evaluate("() => document.getElementById('screen').toDataURL('image/jpeg', 0.8)")
            open(os.path.join(outdir, 'final.jpg'), 'wb').write(base64.b64decode(d.split(',', 1)[1]))
        except Exception:
            pass
        b.close()
    stop()
    rep['errors'] = errs[:30]
    rep['wall_s'] = round(time.time() - t0)
    json.dump(rep, open(report_path, 'w'), indent=1)
    print('RESULT', rep['result'], 'deaths', rep['m']['deaths'], 'hits', rep['m']['hits'], 'wall', rep['wall_s'], 's', 'errors', len(errs), flush=True)
    for k in rep['killers'][:12]:
        print('  killer', json.dumps(k))


if __name__ == '__main__':
    main()
