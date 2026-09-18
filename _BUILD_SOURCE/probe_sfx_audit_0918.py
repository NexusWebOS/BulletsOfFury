#!/usr/bin/env python3
"""
probe_sfx_audit_0918.py - WHICH SOUNDS ACTUALLY PLAY, measured in real Chromium.

    python _BUILD_SOURCE/probe_sfx_audit_0918.py [--old-js FILE --old-manifest FILE] [--stage N] [--seconds S]

Mike 0918: "what happened to all my sounds?! my explosions and enemy and projectiles are practically gone!"
Plays a real stage with the player auto-firing and invulnerable-by-stub, and wraps Snd.play (the one call every
sample goes through) to record, per sound name: calls, calls that returned true, calls refused by the TAME
retrigger gate, and the element volume it was set to. With --old-js the same run is made against an older
game.js / manifest.js served in place of the repo copy, so two builds are compared on identical input.
"""
import os, sys, json, argparse, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__))

HOOK = r"""() => {
  const R = window.__sfx = {};
  const op = Snd.play.bind(Snd);
  Snd.play = function(name, vol){
    const r = R[name] || (R[name] = {calls:0, ok:0, gated:0, vol:0, ready:0});
    r.calls++;
    const cfg = Snd.TAME[name], t = performance.now()/1000;
    const gated = !!(cfg && cfg.min && Snd._last[name]!=null && t-Snd._last[name] < cfg.min);
    const res = op(name, vol);
    if(res){ r.ok++; const p=Snd.pools[name]; if(p){ const a=p.list[(p.i+p.list.length-1)%p.list.length]; r.vol=Math.max(r.vol, a.volume); if(a.readyState>=3) r.ready++; } }
    else if(gated) r.gated++;
    return res;
  };
  return {sfx:Snd.vol.sfx, master:Snd.vol.master, music:Snd.vol.music};
}"""

def run(sh, repo, stage, seconds, old_js=None, old_man=None):
    from playwright.sync_api import sync_playwright
    port, stop = sh.serve(repo)
    errs = []
    with sync_playwright() as p:
        br = p.chromium.launch(args=['--disable-gpu', '--no-sandbox', '--autoplay-policy=no-user-gesture-required'])
        pg = br.new_page(viewport={'width': 1000, 'height': 1100})
        pg.on('pageerror', lambda e: errs.append(str(e)[:200]))
        if old_js:
            pg.route('http://127.0.0.1:%d/assets/game.js' % port, lambda r: r.fulfill(path=old_js))
        if old_man:
            pg.route('http://127.0.0.1:%d/assets/manifest.js' % port, lambda r: r.fulfill(path=old_man))
        pg.goto('http://127.0.0.1:%d/index.html' % port, wait_until='load', timeout=120000)
        pg.wait_for_function("() => typeof state!=='undefined' && (window.__bofFrames|0) > 4", timeout=120000)
        pg.evaluate(sh.TRAP_RAF)
        vols = pg.evaluate(HOOK)
        pg.evaluate(sh.SETUP, {'state': 'PLAY', 'pilot': 'cole', 'stage': stage, 'invuln': False})
        pg.evaluate("() => { playerHit=function(){}; }")
        frames = int(seconds * 60)
        for f in range(0, frames, 6):
            pg.evaluate("() => { try{ player.fireCd=0; pShoot(); }catch(e){} }")
            e = pg.evaluate(sh.STEP, 6)
            if e: errs.append('STEP: ' + e)
            pg.wait_for_timeout(40)          # real time, so samples can fetch and decode
        R = pg.evaluate("() => window.__sfx")
        br.close()
    stop()
    return vols, R, errs

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--old-js'); ap.add_argument('--old-manifest')
    ap.add_argument('--stage', type=int, default=1); ap.add_argument('--seconds', type=float, default=20)
    ap.add_argument('--json')
    a = ap.parse_args()
    repo = os.path.dirname(HERE)
    spec = importlib.util.spec_from_file_location('shoot', os.path.join(HERE, 'shoot.py'))
    sh = importlib.util.module_from_spec(spec); spec.loader.exec_module(sh)
    vols, R, errs = run(sh, repo, a.stage, a.seconds, a.old_js, a.old_manifest)
    print('volumes', vols, 'errors', len(errs))
    for e in errs[:5]: print('  ', e)
    for k in sorted(R, key=lambda k: -R[k]['calls']):
        r = R[k]; print('%-28s calls %4d  played %4d  gated %4d  ready %4d  vol %.3f' % (k, r['calls'], r['ok'], r['gated'], r['ready'], r['vol']))
    if a.json:
        json.dump({'vols': vols, 'R': R, 'errs': errs}, open(a.json, 'w'), indent=1)

if __name__ == '__main__':
    main()
