#!/usr/bin/env python3
"""
probe_sfx_output_0918.py - do the COMBAT sounds actually make noise? Measured on http:// AND file://.

    python _BUILD_SOURCE/probe_sfx_output_0918.py

Mike 0918: "what happened to all my sounds?! my explosions and enemy and projectiles are practically gone!"

Two faults, both measured here:
  1. Every TAME row with an `lp` is routed element -> createMediaElementSource -> lowpass -> shelf -> gain.
     A media element loaded from file:// is cross-origin to WebAudio, so that source outputs ZEROS while its
     currentTime still advances - explosions, every enemy round and missiles played in silence while the
     unfiltered player gun was fine. file:// must now route NOTHING through WebAudio.
  2. 0914 gave expBig/expSmall their first TAME row (g 0.40 + lowpass + shelf, 0.20 s gate). They are native
     again at g 0.80 / 0.74.

For every key and EVERY slot of its round-robin pool (a cold slot is where a sound can be lost), after a real
click: Snd.play, then poll until the element is actually playing. Over http, a WebAudio-routed key is also
tapped with an AnalyserNode for real signal. Exit 1 on any failure.
"""
import os, sys, json, importlib.util, pathlib
HERE = os.path.dirname(os.path.abspath(__file__))
NAMES = ['expBig', 'expSmall', 'explosion', 'enemyShoot', 'enemyMachineGunLight', 'missile', 'machineGun']

JS = r"""async (names) => {
  const ctxA = Snd._audioCtx(); if (ctxA && ctxA.state !== 'running') { try { await ctxA.resume(); } catch(e){} }
  const out = {__proto: location.protocol, __ctx: ctxA ? ctxA.state : 'none'};
  /* the FIRST media playback of a page wakes the audio device (measured 265-642 ms on either build, whatever the
     key); the menu blips have always done that long before combat, so do it here and do not count it */
  Snd.play('select', 0.01); await new Promise(r => setTimeout(r, 900));
  for (const n of names) {
    const p = Snd.pools[n]; if (!p) { out[n] = 'no pool'; continue; }
    const cfg = Snd.TAME[n] || {}, rows = [];
    for (let k = 0; k < p.list.length; k++) {
      const a = p.list[p.i], i = p.i, t0 = performance.now();
      const res = Snd.play(n, 1);
      let started = -1, peak = -1;
      for (let s = 0; s < 40; s++) { await new Promise(r => setTimeout(r, 50));
        if (a.currentTime > 0.01 && !a.paused) { started = Math.round(performance.now() - t0); break; } }
      if (a._bofNode && started >= 0) {
        const an = ctxA.createAnalyser(); an.fftSize = 2048; a._bofNode.connect(an);
        const buf = new Float32Array(an.fftSize); peak = 0;
        for (let s = 0; s < 12; s++) { await new Promise(r => setTimeout(r, 20)); an.getFloatTimeDomainData(buf);
          for (const v of buf) peak = Math.max(peak, Math.abs(v)); }
        a._bofNode.disconnect(an);
      }
      rows.push({i, res, startedMs: started, route: a._bofNode ? 'webaudio' : 'native', peak: Math.round(peak * 1000) / 1000,
                 vol: Math.round(a.volume * 1000) / 1000});
      await new Promise(r => setTimeout(r, 180));      // past every key's TAME gate
    }
    out[n] = {g: cfg.g, lp: cfg.lp || null, native: !!cfg.native, rows};
  }
  return out;
}"""

def main():
    repo = os.path.dirname(HERE)
    spec = importlib.util.spec_from_file_location('shoot', os.path.join(HERE, 'shoot.py'))
    sh = importlib.util.module_from_spec(spec); spec.loader.exec_module(sh)
    from playwright.sync_api import sync_playwright
    port, stop = sh.serve(repo)
    res, errs = {}, []
    with sync_playwright() as p:
        br = p.chromium.launch(args=['--disable-gpu', '--no-sandbox'])   # NO file-access flags: a double-clicked index.html has none
        for label, url in [('http', 'http://127.0.0.1:%d/index.html' % port),
                           ('file', pathlib.Path(repo, 'index.html').resolve().as_uri())]:
            pg = br.new_page(viewport={'width': 900, 'height': 900})
            pg.on('pageerror', lambda e: errs.append(str(e)[:200]))
            pg.goto(url, wait_until='load', timeout=120000)
            pg.wait_for_function("() => typeof state!=='undefined' && (window.__bofFrames|0) > 4", timeout=120000)
            pg.mouse.click(300, 300)                     # a real user gesture, as a player gives one
            pg.wait_for_timeout(3000)
            res[label] = pg.evaluate(JS, NAMES)
            pg.close()
        br.close()
    stop()
    fails = 0
    def ok(c, m):
        nonlocal fails
        print(('  ok   ' if c else '  FAIL ') + m)
        if not c: fails += 1
    for label in ('http', 'file'):
        r = res[label]; print('== %s (AudioContext %s)' % (label, r['__ctx']))
        for n in NAMES:
            q = r.get(n)
            if not isinstance(q, dict): ok(False, '%s %s: %s' % (label, n, q)); continue
            rows = q['rows']
            slow = [x for x in rows if x['startedMs'] < 0 or x['startedMs'] > 400]
            ok(not slow, '%s %-22s every pool slot plays (start ms %s, vol %s)' % (label, n, [x['startedMs'] for x in rows], rows[0]['vol']))
            if label == 'file':
                ok(all(x['route'] == 'native' for x in rows), '%s %-22s nothing routed through WebAudio on file://' % (label, n))
            else:
                web = [x for x in rows if x['route'] == 'webaudio']
                ok(all(x['peak'] > 0.02 for x in web), '%s %-22s WebAudio route carries signal (peaks %s)' % (label, n, [x['peak'] for x in web]))
    ok(res['http']['expBig']['native'] and res['http']['expBig']['g'] >= 0.7, 'expBig is native again at g %s' % res['http']['expBig']['g'])
    ok(res['http']['expSmall']['native'] and res['http']['expSmall']['g'] >= 0.7, 'expSmall is native again at g %s' % res['http']['expSmall']['g'])
    ok(not errs, 'zero page errors (%d)' % len(errs))
    print('%d fail' % fails)
    if len(sys.argv) > 1: json.dump(res, open(sys.argv[1], 'w'), indent=1)
    return 1 if fails else 0

if __name__ == '__main__':
    sys.exit(main())
